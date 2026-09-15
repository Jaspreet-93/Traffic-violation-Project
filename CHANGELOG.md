# ?? Project Changelog & Recent Updates

All notable changes, bug fixes, model upgrades, and setup enhancements for the **Smart Traffic Violation Detection System (AURA Engine)** are documented below.

---

## [v2.4.0] - 2026-09-15

### ?? Major Highlights & One-Click Setup
- **Automated Cross-Platform Setup Scripts**:
  - Added `setup.bat` and `start.bat` for Windows: One-click installation of Python venv, pip requirements, npm packages, directory trees, and dual-server startup.
  - Added `setup.sh` and `start.sh` for Linux/macOS with automated signal trapping and parallel process management.
- **Root-Level `requirements.txt`**:
  - Added standard root-level requirements file and updated backend requirements with all essential libraries: `torch`, `torchvision`, `easyocr`, `openpyxl`, `matplotlib`, `psutil`, `pillow`, and `requests`.
- **Preconfigured Environment Configuration**:
  - Added default `.env` and updated `.env.example` preconfigured with `DATABASE_URL=sqlite:///./test.db` so the system boots out of the box with zero external PostgreSQL dependencies.
- **Bundled Testing Sample Media**:
  - Created `traffic-violation-system/samples/` directory with verified test media:
    - `samples/images/sample_traffic.png`
    - `samples/images/sample_motorcycle_violation.jpeg`
    - `samples/videos/sample_traffic_video.mp4`

---

### ?? Bug Fixes & Video Pipeline Optimization
- **Resolved OpenCV `lkpyramid.cpp:1415` Assertion Crash**:
  - **Issue**: Default Ultralytics BoT-SORT tracking invoked OpenCV's Lucas-Kanade optical flow (`calcOpticalFlowPyrLK`), crashing on preprocessed video frames where pyramid dimensions mismatched.
  - **Fix**: Replaced BoT-SORT with pure Kalman-filter **ByteTrack** (`tracker="bytetrack.yaml"`), completely eliminating optical flow crashes and increasing video processing speed by over 2.5x.
  - Added `yolo_detector.reset_tracker()` to clear Kalman history between video files.
- **Fixed Missing `re` Import in Video Processing Worker**:
  - Resolved `NameError: name 're' is not defined` during license plate pattern validation.
- **Multi-Violation & Object Panel Visibility in UI**:
  - Previously, video results only recorded vehicle bounding boxes in `all_detections`.
  - Now, all detected violations (`No Helmet`, `No Seat Belt`, `Distracted Driving`, `Smoking`, `Wrong Lane`) and recognized `license plate (...)` are pushed to the UI object breakdown panel with exact bounding boxes and confidences.
- **ALPR Number Plate Contour & Gradient Candidate Fallback**:
  - When the 1-epoch YOLO plate detector misses a plate on low-resolution crops, an OpenCV Sobel-X + Otsu thresholding candidate extractor isolates the high-contrast plate region, enabling EasyOCR to reliably extract the plate number.
- **Universal Video Codec Compatibility**:
  - Switched video writers from `avc1` to `mp4v`, eliminating OpenH264 DLL missing errors on Windows while providing `openh264-1.8.0-win64.dll` for H.264 support.
- **Relaxed Overly Rigid Vehicle Suitability Filters**:
  - Expanded vehicle bounding box minimum size from 100x100 to 40x40 and aspect ratio boundaries to 0.35–3.2, removing keyword-based file rejection.

---

## [v2.3.0] - 2026-09-14

### ?? License Plate & Multi-Violation Refactor
- Implemented multi-frame candidate pooling: tracks top 8 highest-quality vehicle frames for OCR extraction.
- Enhanced EasyOCR with bilateral filtering, CLAHE contrast enhancement, and padding.
- Enabled simultaneous multi-violation detection per vehicle (e.g., No Helmet + Wrong Lane).
- Fixed threshold drop bug in Violation Decision Engine.
