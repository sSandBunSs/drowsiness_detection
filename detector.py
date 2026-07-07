"""
==============================================================
  Drowsiness Detection System - Deteksi Kantuk Pengemudi
  Berbasis MediaPipe Face Mesh + EAR/MAR Adaptive Threshold
==============================================================
  Kompatibel: Windows 10 (PC/Laptop) & Raspberry Pi 4
  Author  : [Nama Kamu]
  Version : 1.0.0
==============================================================
"""

import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
import time
import os
import urllib.request
import platform
import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Optional, Tuple
from datetime import datetime

# ─── Logging Setup ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/session.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ─── Konfigurasi ───────────────────────────────────────────
@dataclass
class Config:
    # Kamera
    camera_index: int = 0
    frame_width: int = 640
    frame_height: int = 480
    fps_target: int = 30

    # EAR (Eye Aspect Ratio)
    ear_threshold_base: float = 0.25      # threshold dasar mata tertutup
    ear_consec_frames: int = 20           # frame berturut-turut sebelum alarm

    # MAR (Mouth Aspect Ratio)
    mar_threshold: float = 0.65           # threshold mulut terbuka (menguap)
    mar_consec_frames: int = 15

    # PERCLOS (Percentage of Eye Closure)
    perclos_window: int = 150             # jumlah frame untuk window PERCLOS
    perclos_threshold: float = 0.35       # 35% waktu mata tertutup = kantuk

    # Adaptive threshold
    calibration_frames: int = 100         # frame untuk kalibrasi awal
    adaptive_enabled: bool = True         # aktifkan adaptive threshold

    # Alarm
    alarm_enabled: bool = True
    alarm_sound_path: str = "sounds/alarm.wav"

    # UI
    show_landmarks: bool = False          # tampilkan semua landmark (debug)
    show_fps: bool = True
    record_video: bool = False
    output_video_path: str = "logs/recorded_session.avi"

    # Platform
    is_raspberry_pi: bool = field(default_factory=lambda: Config._detect_rpi())

    @staticmethod
    def _detect_rpi() -> bool:
        try:
            with open("/proc/device-tree/model", "r") as f:
                return "Raspberry Pi" in f.read()
        except Exception:
            return False


# ─── Landmark Indices (MediaPipe Face Mesh 468 points) ─────
# Mata kiri (dari perspektif kamera = sebelah kanan wajah)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
# Mata kanan
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
# Mulut (luar)
MOUTH_OUTER = [61, 291, 0, 17, 39, 269, 405, 146]
# Iris untuk deteksi arah pandang (opsional)
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]


# ─── State Deteksi ─────────────────────────────────────────
@dataclass
class DetectionState:
    ear_counter: int = 0          # frame berturut-turut EAR di bawah threshold
    mar_counter: int = 0          # frame berturut-turut MAR di atas threshold
    yawn_count: int = 0           # total jumlah menguap
    drowsy_count: int = 0         # total deteksi kantuk
    alarm_active: bool = False
    status: str = "NORMAL"        # NORMAL / WARNING / DROWSY
    status_color: tuple = (0, 255, 0)

    # Riwayat EAR untuk PERCLOS & adaptive
    ear_history: deque = field(default_factory=lambda: deque(maxlen=300))
    perclos_window: deque = field(default_factory=lambda: deque(maxlen=150))

    # Kalibrasi
    calibrated: bool = False
    calibration_ear_values: list = field(default_factory=list)
    ear_threshold_adaptive: float = 0.25

    # Waktu
    session_start: float = field(default_factory=time.time)
    last_alarm_time: float = 0.0

    # FPS
    fps: float = 0.0
    frame_count: int = 0
    fps_start_time: float = field(default_factory=time.time)


# ─── Utilitas Geometri ─────────────────────────────────────
def euclidean(p1, p2) -> float:
    return np.linalg.norm(np.array(p1) - np.array(p2))


def compute_ear(eye_landmarks) -> float:
    """
    Eye Aspect Ratio (EAR) = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
    Referensi: Soukupova & Cech, 2016
    """
    p1, p2, p3, p4, p5, p6 = eye_landmarks
    vertical_1 = euclidean(p2, p6)
    vertical_2 = euclidean(p3, p5)
    horizontal = euclidean(p1, p4)
    if horizontal < 1e-6:
        return 0.0
    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def compute_mar(mouth_landmarks) -> float:
    """
    Mouth Aspect Ratio (MAR) — adaptasi dari EAR untuk deteksi menguap
    """
    p1, p2, p3, p4, p5, p6, p7, p8 = mouth_landmarks
    vertical_1 = euclidean(p3, p7)
    vertical_2 = euclidean(p4, p8)
    vertical_3 = euclidean(p5, p1)
    horizontal = euclidean(p1, p2)
    if horizontal < 1e-6:
        return 0.0
    return (vertical_1 + vertical_2 + vertical_3) / (3.0 * horizontal)


def get_landmark_coords(landmarks, indices, w, h) -> list:
    """Konversi landmark mediapipe ke koordinat pixel."""
    return [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]


def compute_perclos(perclos_window: deque, threshold: float) -> float:
    """
    PERCLOS = proporsi frame di mana EAR < threshold dalam window tertentu.
    """
    if len(perclos_window) == 0:
        return 0.0
    closed = sum(1 for ear in perclos_window if ear < threshold)
    return closed / len(perclos_window)


# ─── Alarm ─────────────────────────────────────────────────
class AlarmSystem:
    def __init__(self, config: Config):
        self.config = config
        self._alarm_proc = None
        self._system = platform.system()
        logger.info(f"AlarmSystem initialized on {self._system}")

    def trigger(self):
        if not self.config.alarm_enabled:
            return
        try:
            if os.path.exists(self.config.alarm_sound_path):
                if self._system == "Windows":
                    import winsound
                    winsound.PlaySound(
                        self.config.alarm_sound_path,
                        winsound.SND_FILENAME | winsound.SND_ASYNC
                    )
                elif self._system == "Linux":
                    # Raspberry Pi / Linux
                    os.system(f"aplay -q {self.config.alarm_sound_path} &")
            else:
                # Fallback: beep sistem
                if self._system == "Windows":
                    import winsound
                    winsound.Beep(1000, 500)
                else:
                    os.system("echo -e '\\a'")
        except Exception as e:
            logger.warning(f"Alarm gagal diputar: {e}")

    def stop(self):
        pass  # async alarm berhenti sendiri


# ─── Visualisasi UI ────────────────────────────────────────
class Visualizer:
    COLORS = {
        "NORMAL":  (0, 200, 0),
        "WARNING": (0, 165, 255),
        "DROWSY":  (0, 0, 255),
        "bg":      (20, 20, 20),
        "white":   (255, 255, 255),
        "gray":    (150, 150, 150),
        "cyan":    (255, 220, 0),
    }

    @staticmethod
    def draw_eye(frame, eye_coords, color):
        pts = np.array(eye_coords, dtype=np.int32)
        cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=1)
        for pt in eye_coords:
            cv2.circle(frame, pt, 2, color, -1)

    @staticmethod
    def draw_mouth(frame, mouth_coords, color):
        pts = np.array(mouth_coords, dtype=np.int32)
        cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=1)

    @staticmethod
    def draw_hud(frame, state: DetectionState, config: Config,
                 ear: float, mar: float, perclos: float):
        h, w = frame.shape[:2]

        # ── Panel kiri atas ──
        panel_w, panel_h = 230, 210
        overlay = frame.copy()
        cv2.rectangle(overlay, (5, 5), (panel_w, panel_h),
                      Visualizer.COLORS["bg"], -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        cv2.rectangle(frame, (5, 5), (panel_w, panel_h),
                      Visualizer.COLORS["gray"], 1)

        def put(text, y, color=Visualizer.COLORS["white"], scale=0.52, thick=1):
            cv2.putText(frame, text, (12, y), cv2.FONT_HERSHEY_SIMPLEX,
                        scale, color, thick, cv2.LINE_AA)

        put("[ DROWSINESS DETECTOR ]", 25,
            color=Visualizer.COLORS["cyan"], scale=0.5, thick=1)

        # Threshold adaptif
        thr = state.ear_threshold_adaptive if config.adaptive_enabled else config.ear_threshold_base

        put(f"EAR  : {ear:.3f}  [thr:{thr:.3f}]", 52)
        put(f"MAR  : {mar:.3f}  [thr:{config.mar_threshold:.2f}]", 74)
        put(f"PERCLOS : {perclos*100:.1f}%", 96)

        session_sec = int(time.time() - state.session_start)
        put(f"Sesi : {session_sec//60:02d}:{session_sec%60:02d}", 118)
        put(f"Menguap  : {state.yawn_count}x", 140)
        put(f"Kantuk   : {state.drowsy_count}x", 162)

        cal_txt = "Kalibrasi: SELESAI" if state.calibrated else \
                  f"Kalibrasi: {len(state.calibration_ear_values)}/{config.calibration_frames}"
        put(cal_txt, 184,
            color=(0, 255, 120) if state.calibrated else (0, 165, 255))

        if config.show_fps:
            put(f"FPS: {state.fps:.1f}", 204, color=Visualizer.COLORS["gray"])

        # ── Status Banner ──
        status_color = Visualizer.COLORS.get(state.status, (255, 255, 255))
        banner_h = 55
        overlay2 = frame.copy()
        cv2.rectangle(overlay2, (0, h - banner_h), (w, h), status_color, -1)
        cv2.addWeighted(overlay2, 0.45, frame, 0.55, 0, frame)

        status_map = {
            "NORMAL":  "✓  NORMAL  - Pengemudi Waspada",
            "WARNING": "!  PERINGATAN  - Tanda Mengantuk",
            "DROWSY":  "!!  KANTUK TERDETEKSI  - HARAP ISTIRAHAT",
        }
        label = status_map.get(state.status, state.status)
        font_scale = 0.7 if w >= 640 else 0.5
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX,
                                    font_scale, 2)[0]
        tx = (w - text_size[0]) // 2
        ty = h - banner_h + 35
        cv2.putText(frame, label, (tx, ty), cv2.FONT_HERSHEY_DUPLEX,
                    font_scale, (255, 255, 255), 2, cv2.LINE_AA)

        # ── Bar PERCLOS ──
        bar_x, bar_y, bar_w_total, bar_h2 = 5, h - banner_h - 18, 220, 10
        cv2.rectangle(frame, (bar_x, bar_y),
                      (bar_x + bar_w_total, bar_y + bar_h2), (50, 50, 50), -1)
        fill = int(perclos * bar_w_total)
        bar_color = (0, 200, 0) if perclos < 0.2 else \
                    (0, 165, 255) if perclos < config.perclos_threshold else (0, 0, 255)
        cv2.rectangle(frame, (bar_x, bar_y),
                      (bar_x + fill, bar_y + bar_h2), bar_color, -1)
        cv2.putText(frame, "PERCLOS", (bar_x + bar_w_total + 5, bar_y + 9),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, Visualizer.COLORS["gray"],
                    1, cv2.LINE_AA)

        return frame


# ─── Detektor Utama ────────────────────────────────────────
class DrowsinessDetector:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.state = DetectionState()
        self.alarm = AlarmSystem(self.config)
        self.viz = Visualizer()

        # MediaPipe setup (Tasks API — kompatibel mediapipe >= 0.10)
        model_path = self._download_model()
        options = FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=model_path),
            running_mode=RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.6,
            min_face_presence_confidence=0.6,
            min_tracking_confidence=0.6,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )
        self.face_landmarker = FaceLandmarker.create_from_options(options)
        self._frame_timestamp_ms = 0

        self.cap: Optional[cv2.VideoCapture] = None
        self.writer: Optional[cv2.VideoWriter] = None
        logger.info("DrowsinessDetector siap.")
        logger.info(f"Platform: {'Raspberry Pi' if self.config.is_raspberry_pi else platform.system()}")

    def _download_model(self) -> str:
        """Download MediaPipe face landmarker model jika belum ada."""
        model_dir = "models"
        model_path = os.path.join(model_dir, "face_landmarker.task")
        os.makedirs(model_dir, exist_ok=True)
        if not os.path.exists(model_path):
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            logger.info("Mengunduh model MediaPipe face_landmarker.task ...")
            print("⏳ Mengunduh model MediaPipe (sekali saja, ~29MB)...")
            urllib.request.urlretrieve(url, model_path)
            logger.info(f"Model berhasil diunduh: {model_path}")
            print(f"✅ Model tersimpan di: {model_path}")
        return model_path

    # ── Kamera ───────────────────────────────────────────────
    def _init_camera(self) -> bool:
        backend = cv2.CAP_V4L2 if self.config.is_raspberry_pi else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(self.config.camera_index, backend)
        if not self.cap.isOpened():
            logger.error(f"Kamera index {self.config.camera_index} tidak bisa dibuka.")
            return False
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.config.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS,          self.config.fps_target)

        # Raspberry Pi: turunkan buffer agar latency kecil
        if self.config.is_raspberry_pi:
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        logger.info(f"Kamera berhasil dibuka: {self.config.frame_width}x{self.config.frame_height}")
        return True

    def _init_writer(self, w, h):
        if self.config.record_video:
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.writer = cv2.VideoWriter(
                self.config.output_video_path, fourcc,
                self.config.fps_target, (w, h)
            )

    # ── Kalibrasi Adaptive Threshold ─────────────────────────
    def _calibrate(self, ear: float):
        if self.state.calibrated:
            return
        self.state.calibration_ear_values.append(ear)
        if len(self.state.calibration_ear_values) >= self.config.calibration_frames:
            baseline = np.mean(self.state.calibration_ear_values)
            # Threshold = 75% dari baseline EAR saat mata terbuka normal
            self.state.ear_threshold_adaptive = round(baseline * 0.75, 3)
            self.state.calibrated = True
            logger.info(f"Kalibrasi selesai. Baseline EAR={baseline:.3f}, "
                        f"Threshold={self.state.ear_threshold_adaptive:.3f}")

    # ── Update FPS ────────────────────────────────────────────
    def _update_fps(self):
        self.state.frame_count += 1
        elapsed = time.time() - self.state.fps_start_time
        if elapsed >= 1.0:
            self.state.fps = self.state.frame_count / elapsed
            self.state.frame_count = 0
            self.state.fps_start_time = time.time()

    # ── Logika Deteksi ────────────────────────────────────────
    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        self._frame_timestamp_ms += int(1000 / max(self.config.fps_target, 1))
        detection_result = self.face_landmarker.detect_for_video(
            mp_image, self._frame_timestamp_ms
        )

        ear, mar, perclos = 0.0, 0.0, 0.0

        if detection_result.face_landmarks:
            lm = detection_result.face_landmarks[0]

            # Ekstrak koordinat
            left_eye  = get_landmark_coords(lm, LEFT_EYE,    w, h)
            right_eye = get_landmark_coords(lm, RIGHT_EYE,   w, h)
            mouth     = get_landmark_coords(lm, MOUTH_OUTER, w, h)

            # Hitung metrik
            ear_left  = compute_ear(left_eye)
            ear_right = compute_ear(right_eye)
            ear = (ear_left + ear_right) / 2.0
            mar = compute_mar(mouth)

            # Kalibrasi & adaptive threshold
            if self.config.adaptive_enabled:
                self._calibrate(ear)
            thr_ear = (self.state.ear_threshold_adaptive
                       if self.config.adaptive_enabled and self.state.calibrated
                       else self.config.ear_threshold_base)

            # Update PERCLOS window
            self.state.perclos_window.append(ear)
            self.state.ear_history.append(ear)
            perclos = compute_perclos(self.state.perclos_window, thr_ear)

            # ── Logika EAR (kantuk) ──
            if ear < thr_ear:
                self.state.ear_counter += 1
            else:
                if self.state.ear_counter >= self.config.ear_consec_frames:
                    self.state.drowsy_count += 1
                    logger.warning(f"Kantuk terdeteksi! EAR={ear:.3f} "
                                   f"selama {self.state.ear_counter} frame")
                self.state.ear_counter = 0

            # ── Logika MAR (menguap) ──
            if mar > self.config.mar_threshold:
                self.state.mar_counter += 1
            else:
                if self.state.mar_counter >= self.config.mar_consec_frames:
                    self.state.yawn_count += 1
                    logger.info(f"Menguap terdeteksi! MAR={mar:.3f}")
                self.state.mar_counter = 0

            # ── Tentukan Status ──
            is_ear_alert = self.state.ear_counter >= self.config.ear_consec_frames
            is_perclos_alert = perclos >= self.config.perclos_threshold
            is_yawn_warning = self.state.mar_counter >= self.config.mar_consec_frames

            if is_ear_alert or is_perclos_alert:
                self.state.status = "DROWSY"
            elif is_yawn_warning or self.state.ear_counter >= self.config.ear_consec_frames // 2:
                self.state.status = "WARNING"
            else:
                self.state.status = "NORMAL"

            # ── Alarm ──
            now = time.time()
            if self.state.status == "DROWSY" and \
               (now - self.state.last_alarm_time) > 3.0:
                self.alarm.trigger()
                self.state.last_alarm_time = now

            # ── Gambar landmark mata & mulut ──
            eye_color = (0, 0, 255) if ear < thr_ear else (0, 255, 100)
            mouth_color = (0, 165, 255) if mar > self.config.mar_threshold else (200, 200, 200)
            self.viz.draw_eye(frame, left_eye, eye_color)
            self.viz.draw_eye(frame, right_eye, eye_color)
            self.viz.draw_mouth(frame, mouth, mouth_color)

            # Semua landmark (debug)
            if self.config.show_landmarks:
                for lm_pt in lm:
                    cx, cy = int(lm_pt.x * w), int(lm_pt.y * h)
                    cv2.circle(frame, (cx, cy), 1, (180, 180, 180), -1)

        else:
            # Wajah tidak terdeteksi
            self.state.status = "NORMAL"
            self.state.ear_counter = 0
            self.state.mar_counter = 0
            cv2.putText(frame, "Wajah tidak terdeteksi", (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

        # ── HUD ──
        self.viz.draw_hud(frame, self.state, self.config, ear, mar, perclos)
        return frame

    # ── Loop Utama ────────────────────────────────────────────
    def run(self):
        os.makedirs("logs", exist_ok=True)
        if not self._init_camera():
            return

        ret, first = self.cap.read()
        if ret:
            h, w = first.shape[:2]
            self._init_writer(w, h)

        logger.info("Sistem berjalan. Tekan 'q' untuk keluar, "
                    "'r' reset counter, 's' screenshot, 'l' toggle landmarks")

        print("\n" + "="*55)
        print("  SISTEM DETEKSI KANTUK PENGEMUDI")
        print("="*55)
        print("  Tekan 'q'  → Keluar")
        print("  Tekan 'r'  → Reset counter")
        print("  Tekan 's'  → Screenshot")
        print("  Tekan 'l'  → Toggle landmark wajah")
        print("  Tekan 'a'  → Toggle adaptive threshold")
        print("="*55 + "\n")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                logger.error("Frame tidak terbaca dari kamera.")
                break

            # Flip horizontal (mirror)
            frame = cv2.flip(frame, 1)
            self._update_fps()

            # Proses & tampilkan
            output = self._process_frame(frame)

            if self.writer:
                self.writer.write(output)

            cv2.imshow("Drowsiness Detection System", output)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                logger.info("Keluar dari program.")
                break
            elif key == ord("r"):
                self.state.ear_counter = 0
                self.state.mar_counter = 0
                self.state.yawn_count = 0
                self.state.drowsy_count = 0
                logger.info("Counter direset.")
            elif key == ord("s"):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = f"logs/screenshot_{ts}.jpg"
                cv2.imwrite(path, output)
                logger.info(f"Screenshot disimpan: {path}")
            elif key == ord("l"):
                self.config.show_landmarks = not self.config.show_landmarks
            elif key == ord("a"):
                self.config.adaptive_enabled = not self.config.adaptive_enabled
                logger.info(f"Adaptive threshold: {self.config.adaptive_enabled}")

        self._cleanup()

    def _cleanup(self):
        if self.cap:
            self.cap.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()
        self.face_landmarker.close()
        logger.info("Resource dibebaskan. Program selesai.")


# ─── Entry Point ───────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config(
        camera_index=0,
        frame_width=640,
        frame_height=480,
        ear_threshold_base=0.25,
        mar_threshold=0.65,
        adaptive_enabled=True,
        alarm_enabled=True,
        show_fps=True,
        record_video=False,
    )
    detector = DrowsinessDetector(config=cfg)
    detector.run()
