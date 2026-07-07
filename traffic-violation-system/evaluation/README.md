# AI Model Testing & Evaluation Pipeline

This module provides a unified pipeline to evaluate, benchmark, and visualize the performance of all 7 AI models in the Traffic Violation System.

---

## 1. Directory Structure

```text
evaluation/
│
├── metrics/
│   ├── accuracy.py          # Classification accuracy calculations
│   ├── precision_recall.py  # Classification precision, recall, F1
│   └── map_score.py         # Detection mAP score utilities
│
├── scripts/
│   ├── benchmark.py         # Inference latency & FPS benchmark
│   ├── confusion_matrix.py  # Confusion matrix renderer (OpenCV)
│   └── evaluate.py          # Master validation evaluator
│
├── reports/
│   ├── model_report.json    # Consolidated evaluation metrics database
│   └── performance_report.md# Detailed comparative summary & MLOps guidance
│
└── README.md                # System documentation (this file)
```

---

## 2. Running Benchmarking

The benchmarking script measures the raw inference speed, latency (ms), and frame throughput (FPS) of each model on dummy tensors:

```bash
python -m evaluation.scripts.benchmark
```

Output is written to `experiments/results/benchmark_report.json`.

---

## 3. Running Consolidated Evaluation

The master evaluation script:
1. Dynamically compiles standard YOLO training/validation split cache paths if they do not exist.
2. Validates custom YOLO detection and classification models against their respective test/valid splits.
3. Tests the PyTorch OCR model forward pass.
4. Generates visual confusion matrices as PNG files under `experiments/results/`.
5. Compiles accuracy, precision, recall, F1, and mAP metrics into a final report.

```bash
python -m evaluation.scripts.evaluate
```

Reports are generated at:
* `evaluation/reports/model_report.json`
* `evaluation/reports/performance_report.md`
