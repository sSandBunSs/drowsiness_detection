"""
Evaluasi akurasi klasifikasi EAR pada dataset gambar berlabel (bukan video).

Dataset yang dipakai: datasets/{train,val,test}/{active,fatigue}/*.jpg
Setiap gambar sudah punya label dari nama foldernya sendiri (ground truth
otomatis, tidak perlu anotasi manual seperti untuk video).

Menggunakan ulang compute_ear/get_landmark_coords/LEFT_EYE/RIGHT_EYE persis
dari detector.py agar hasil evaluasi konsisten dengan sistem live.

Usage:
    python evaluate_dataset_images.py datasets/test --ear-threshold 0.25 --max-per-class 200
"""
import argparse
import os
import random
import urllib.request

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode

from detector import LEFT_EYE, RIGHT_EYE, compute_ear, get_landmark_coords

MODEL_PATH = "models/face_landmarker.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/face_landmarker/"
             "face_landmarker/float16/1/face_landmarker.task")
CLASSES = ("active", "fatigue")


def ensure_model() -> str:
    os.makedirs("models", exist_ok=True)
    if not os.path.exists(MODEL_PATH):
        print("Mengunduh model MediaPipe face_landmarker.task ...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    return MODEL_PATH


def build_landmarker() -> FaceLandmarker:
    options = FaceLandmarkerOptions(
        base_options=mp_python.BaseOptions(
            model_asset_path=ensure_model(),
            delegate=mp_python.BaseOptions.Delegate.CPU,  # hindari GPU/GLX di headless
        ),
        running_mode=RunningMode.IMAGE,  # gambar independen, bukan stream video
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return FaceLandmarker.create_from_options(options)


def compute_ear_for_image(landmarker: FaceLandmarker, path: str):
    frame = cv2.imread(path)
    if frame is None:
        return None
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = landmarker.detect(mp_image)
    if not result.face_landmarks:
        return None
    lm = result.face_landmarks[0]
    left_eye = get_landmark_coords(lm, LEFT_EYE, w, h)
    right_eye = get_landmark_coords(lm, RIGHT_EYE, w, h)
    return (compute_ear(left_eye) + compute_ear(right_eye)) / 2.0


def classify_image(landmarker: FaceLandmarker, path: str, ear_threshold: float):
    ear = compute_ear_for_image(landmarker, path)
    if ear is None:
        return None
    predicted = "fatigue" if ear < ear_threshold else "active"
    return predicted, ear


def print_report(name, confusion, no_face, total):
    evaluated = total - no_face
    correct = sum(confusion[c][c] for c in CLASSES)

    print(f"\n=== {name} ===")
    print(f"Total gambar dicoba    : {total}")
    print(f"Wajah tidak terdeteksi : {no_face}")
    if not evaluated:
        print("Tidak ada gambar yang bisa dievaluasi.")
        return
    print(f"Akurasi (dari yang wajahnya terdeteksi): {correct / evaluated * 100:.2f}%")

    print("Confusion matrix (baris=aktual, kolom=prediksi):")
    print("           " + "".join(f"{c:>10}" for c in CLASSES))
    for actual in CLASSES:
        row = "".join(f"{confusion[actual][p]:>10}" for p in CLASSES)
        print(f"{actual:>11}{row}")

    for label in CLASSES:
        tp = confusion[label][label]
        fp = sum(confusion[a][label] for a in CLASSES if a != label)
        fn = sum(confusion[label][p] for p in CLASSES if p != label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        print(f"  {label:>8}: precision={precision:.3f}  recall={recall:.3f}  f1={f1:.3f}")


def run_adaptive_comparison(landmarker, split_dirs, calibration_frames, max_per_class):
    """Bandingkan threshold fixed (0.25) vs adaptive (0.75x baseline) pada gambar.

    Dataset ini tidak punya ID subjek (nama file cuma indeks numerik, lihat
    catatan verifikasi di BAB4.md) sehingga kalibrasi per-pengemudi asli tidak
    bisa direplikasi. Sebagai proksi jujur: N gambar 'active' pertama per split
    dipakai sebagai "baseline kalibrasi" (analog calibration_frames di
    detector.py), sisanya dievaluasi. Ini menguji mekanisme kalibrasi yang sama
    persis, hanya unit kalibrasinya split/populasi, bukan individu.
    """
    for split_dir in split_dirs:
        records = {c: [] for c in CLASSES}
        for actual in CLASSES:
            folder = os.path.join(split_dir, actual)
            files = sorted(os.listdir(folder))
            if max_per_class:
                random.Random(42).shuffle(files)
                files = files[:max_per_class]
            for fname in files:
                ear = compute_ear_for_image(landmarker, os.path.join(folder, fname))
                if ear is not None:
                    records[actual].append(ear)

        calib = records["active"][:calibration_frames]
        eval_active = records["active"][calibration_frames:]
        eval_fatigue = records["fatigue"]

        print(f"\n=== {split_dir}: fixed vs adaptive ===")
        if not calib:
            print("Tidak cukup gambar 'active' untuk kalibrasi, dilewati.")
            continue

        baseline = sum(calib) / len(calib)
        adaptive_threshold = 0.75 * baseline
        print(f"Kalibrasi: {len(calib)} gambar 'active' (proksi {calibration_frames} frame pertama sesi)")
        print(f"Baseline EAR rata-rata: {baseline:.4f} -> threshold adaptif = {adaptive_threshold:.4f}")

        for label, threshold in (("Fixed (0.25)", 0.25), ("Adaptive", adaptive_threshold)):
            confusion = {a: {p: 0 for p in CLASSES} for a in CLASSES}
            for ear in eval_active:
                confusion["active"]["fatigue" if ear < threshold else "active"] += 1
            for ear in eval_fatigue:
                confusion["fatigue"]["fatigue" if ear < threshold else "active"] += 1
            total_eval = len(eval_active) + len(eval_fatigue)
            correct = confusion["active"]["active"] + confusion["fatigue"]["fatigue"]
            acc = correct / total_eval * 100 if total_eval else 0.0

            print(f"\n  -- {label}: threshold={threshold:.4f} --")
            print(f"  n_eval={total_eval} (active={len(eval_active)}, fatigue={len(eval_fatigue)})  Akurasi: {acc:.2f}%")
            for c in CLASSES:
                tp = confusion[c][c]
                fp = sum(confusion[a][c] for a in CLASSES if a != c)
                fn = sum(confusion[c][p] for p in CLASSES if p != c)
                precision = tp / (tp + fp) if (tp + fp) else 0.0
                recall = tp / (tp + fn) if (tp + fn) else 0.0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
                print(f"    {c:>8}: precision={precision:.3f}  recall={recall:.3f}  f1={f1:.3f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("split_dirs", nargs="+", help="mis. datasets/train datasets/val datasets/test")
    parser.add_argument("--ear-threshold", type=float, default=0.25)
    parser.add_argument("--max-per-class", type=int, default=None,
                         help="batasi jumlah gambar per kelas per split (default: semua)")
    parser.add_argument("--compare-adaptive", action="store_true",
                         help="jalankan mode perbandingan fixed vs adaptive threshold (lihat run_adaptive_comparison)")
    parser.add_argument("--calibration-frames", type=int, default=100,
                         help="jumlah gambar 'active' dipakai sbg baseline kalibrasi (default 100, sama dengan Config.calibration_frames di detector.py)")
    args = parser.parse_args()

    landmarker = build_landmarker()

    if args.compare_adaptive:
        run_adaptive_comparison(landmarker, args.split_dirs, args.calibration_frames, args.max_per_class)
        landmarker.close()
        return
    overall_confusion = {a: {p: 0 for p in CLASSES} for a in CLASSES}
    overall_no_face = 0
    overall_total = 0

    for split_dir in args.split_dirs:
        split_confusion = {a: {p: 0 for p in CLASSES} for a in CLASSES}
        split_no_face = 0
        split_total = 0

        for actual in CLASSES:
            folder = os.path.join(split_dir, actual)
            files = sorted(os.listdir(folder))
            if args.max_per_class:
                random.Random(42).shuffle(files)
                files = files[:args.max_per_class]
            for fname in files:
                split_total += 1
                result = classify_image(landmarker, os.path.join(folder, fname), args.ear_threshold)
                if result is None:
                    split_no_face += 1
                    continue
                predicted, _ = result
                split_confusion[actual][predicted] += 1

        print_report(split_dir, split_confusion, split_no_face, split_total)

        for a in CLASSES:
            for p in CLASSES:
                overall_confusion[a][p] += split_confusion[a][p]
        overall_no_face += split_no_face
        overall_total += split_total

    landmarker.close()

    if len(args.split_dirs) > 1:
        print_report("TOTAL (semua split)", overall_confusion, overall_no_face, overall_total)


if __name__ == "__main__":
    main()
