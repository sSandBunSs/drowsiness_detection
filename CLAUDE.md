# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-time driver drowsiness detection system using MediaPipe Face Mesh. Detects
drowsiness via EAR (Eye Aspect Ratio), yawning via MAR (Mouth Aspect Ratio), and
sustained eye closure via PERCLOS, with an adaptive threshold calibrated from the
driver's own baseline. Written in Indonesian (comments, log messages, README) for
a research/thesis (SINTA 2 publication) context. Targets Windows 10 (PC/laptop)
and Raspberry Pi 4.

Note: the README describes a `src/` layout, but the actual scripts
(`detector.py`, `metrics_logger.py`, `generate_alarm.py`) live at the repo root,
not under `src/`. Follow the actual file locations, not the README diagram.

## Setup & Commands

```bash
pip install -r requirements.txt

# Generate the alarm sound once (creates sounds/alarm.wav)
python generate_alarm.py

# Run the detector (opens webcam window)
python detector.py

# Or process a video file instead of a live camera (e.g. a downloaded dataset clip)
python detector.py path/to/clip.mp4
```

No build step. Self-checks (stdlib-only, no test framework) — run directly:
```bash
python test_metrics_logger.py      # MetricsLogger CSV schema
python test_validate_accuracy.py   # validate_accuracy confusion-matrix logic
```

Runtime keyboard controls inside the detector window: `q` quit, `r` reset
counters, `s` save screenshot, `l` toggle landmark overlay, `a` toggle adaptive
threshold.

### Research tooling (accuracy validation)

- **`validate_accuracy.py <metrics_csv> <ground_truth.csv>`** — scores a
  recorded session's `logs/metrics_*.csv` against a hand-authored
  `ground_truth.csv` (`start_sec,end_sec,label` intervals, label ∈
  `NORMAL`/`WARNING`/`DROWSY`) and prints a confusion matrix + precision/recall/F1,
  including a DROWSY-vs-rest breakdown (the safety-relevant number).
- **`evaluate_dataset_images.py <split_dir>...`** — scores the EAR-threshold
  logic against a labeled *image* dataset (see `datasets/` below) instead of
  video. Reuses `compute_ear`/`LEFT_EYE`/`RIGHT_EYE`/`get_landmark_coords`
  directly from `detector.py` so results stay consistent with the live system.
  `--ear-threshold` (default 0.25, matches `Config.ear_threshold_base`) and
  `--max-per-class` (default: no cap) are optional.

**`datasets/`** (local, not part of the repo checkout) holds a downloaded
Kaggle image dataset — **not UTA-RLDD** (that one is video-only and wasn't
obtainable non-interactively). Structure: `datasets/{train,val,test}/{active,fatigue}/*.jpg`,
~11.8k images, label given by folder name (no manual annotation needed). Since
the EAR-threshold method has no learned parameters, there's no train/test
leakage concern here — evaluating across all three splits combined is valid
and was done deliberately (see Known Findings below).

### Known findings from `evaluate_dataset_images.py` (fixed `ear_threshold=0.25`)

| Split | n | Accuracy | active recall | fatigue recall |
|---|---|---|---|---|
| train | 9,054 | 67.23% | 0.565 | 0.870 |
| val | 1,824 | 89.96% | 0.931 | 0.868 |
| test | 909 | 91.18% | 0.936 | 0.887 |
| combined | 11,787 | 72.60% | 0.634 | 0.872 |

`val`/`test` agree closely (~90%); `train` is a harder/more varied outlier that
drags the pooled ("combined") figure down because it's 77% of the dataset by
count — this is a size-weighting artifact, not evidence that val/test are
unrepresentative. Report ~90% (val+test) as the headline number; use the
`train` gap to argue for the adaptive/calibrated threshold over a fixed one.

### Running MediaPipe headless (no display/GPU)

In a headless/no-GPU sandbox, `FaceLandmarker.create_from_options` can fail
trying to init a GPU/GLX context (`BadAccess` on `X_GLXMakeCurrent`, or a
missing `libGLESv2.so.2`). Fix: pass `delegate=mp_python.BaseOptions.Delegate.CPU`
in `BaseOptions`, and if a real GL library is present anywhere on the machine
(e.g. Chrome's bundled `libGLESv2.so`/`libEGL.so`), symlink versioned names
(`libGLESv2.so.2`, `libEGL.so.1`) into a directory on `LD_LIBRARY_PATH`, plus
`export ANGLE_DEFAULT_PLATFORM=swiftshader` to force software rendering. Not
needed on a normal machine with a real display/GPU — this is sandbox-only.

## Architecture

Everything runs through a single long-lived `DrowsinessDetector` instance in
`detector.py`:

- **`Config`** (dataclass) — all tunable parameters (thresholds, frame size,
  calibration length, alarm/recording toggles). Auto-detects Raspberry Pi via
  `/proc/device-tree/model` to adjust camera backend/buffering. Edit values in
  the `if __name__ == "__main__":` block at the bottom of `detector.py` to
  change runtime behavior — there's no config file.
- **`DetectionState`** (dataclass) — mutable per-session state: EAR/MAR
  consecutive-frame counters, rolling `deque` windows for PERCLOS and EAR
  history, calibration progress/results, FPS tracking.
- **Landmark index constants** (`LEFT_EYE`, `RIGHT_EYE`, `MOUTH_OUTER`, etc.) —
  fixed indices into MediaPipe's 468-point face mesh.
- **Geometry functions** (`compute_ear`, `compute_mar`, `compute_perclos`,
  `get_landmark_coords`) — pure functions operating on landmark coordinate
  lists.
- **`AlarmSystem`** — plays `sounds/alarm.wav` via `winsound` on Windows or
  `aplay` on Linux/RPi; falls back to a system beep if the file is missing.
- **`Visualizer`** — draws the on-frame HUD (EAR/MAR/PERCLOS readout, status
  banner, PERCLOS bar, eye/mouth outlines).
- **`DrowsinessDetector`** — orchestrates everything:
  1. Downloads the MediaPipe `face_landmarker.task` model into `models/` on
     first run if not already present (`_download_model`).
  2. Opens the camera (`_init_camera`), optionally an `XVID` video writer.
  3. Per-frame in `_process_frame`: runs `FaceLandmarker.detect_for_video`,
     computes EAR/MAR/PERCLOS, feeds the adaptive calibration
     (`_calibrate` — averages the first `calibration_frames` EAR samples,
     threshold = 75% of that baseline), updates consecutive-frame counters,
     derives `NORMAL` / `WARNING` / `DROWSY` status, and triggers the alarm
     (rate-limited to once per 3s) when `DROWSY`.
  4. `run()` is the main OpenCV capture/display/keyboard loop; `_cleanup()`
     releases the camera/writer and closes the landmarker.

`metrics_logger.py` (`MetricsLogger`) writes per-frame EAR/MAR/PERCLOS data and
discrete events (`DROWSY`/`YAWN`/`CALIBRATED`) to timestamped CSVs under
`logs/` for research analysis, tagged with `platform`/`lighting_condition`.
Wired into `DrowsinessDetector.__init__` (toggle: `Config.log_metrics`) and
called from `_process_frame`/`_calibrate`. Set `Config.lighting_condition`
(`"siang"`/`"malam"`) per test session before running.

`generate_alarm.py` is a one-off script (not imported elsewhere) that
synthesizes `sounds/alarm.wav` (a repeated 1kHz beep) using only `numpy` +
stdlib `wave`/`struct`.

`logs/session.log` accumulates across runs via the module-level
`logging.basicConfig` in `detector.py` (file + console handlers).
