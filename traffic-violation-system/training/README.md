# AI Model Training & Experiment Management Pipeline

This pipeline provides a reusable interface to train, validate, and test custom YOLOv8 models for the Traffic Violation Detection System.

## Directory Structure
```
training/
├── configs/
│   ├── helmet.yaml
│   ├── number_plate.yaml
│   ├── seat_belt.yaml
│   ├── traffic_light.yaml
│   └── driver_behavior.yaml
├── scripts/
│   ├── train.py
│   ├── validate.py
│   └── test.py
├── utils/
│   ├── dataset_checker.py
│   └── model_manager.py
└── README.md
```

## Running Training

To train a model:
```bash
python training/scripts/train.py --config training/configs/helmet.yaml --epochs 1 --fraction 0.01
```

## Running Validation

To validate a model:
```bash
python training/scripts/validate.py --config training/configs/helmet.yaml
```

## Running Testing

To run inference on a test image/video:
```bash
python training/scripts/test.py --config training/configs/helmet.yaml --source path/to/test.jpg
```
