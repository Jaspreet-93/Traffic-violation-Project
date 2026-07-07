import os
import shutil
from ultralytics import YOLO

def main():
    # Load pretrained yolov8n.pt to fine-tune it
    # Resolve the path relative to the root project directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path = os.path.join(root_dir, "models", "yolo", "yolov8n.pt")
    
    print(f"Loading base YOLO model from: {model_path}")
    model = YOLO(model_path)
    
    # Path to datasets/Dataset of helmet detection/data.yaml
    data_yaml = os.path.join(root_dir, "datasets", "Dataset of helmet detection", "data.yaml")
    
    print(f"Starting YOLOv8 training on dataset config: {data_yaml}")
    # Train for 1 epoch on CPU. Set workers=0 to avoid multiprocessing lock issues on Windows.
    # Set fraction=0.01 to run on a very small subset of images, speeding up training.
    model.train(
        data=data_yaml,
        epochs=1,
        imgsz=640,
        device="cpu",
        workers=0,
        fraction=0.01,
        verbose=True
    )
    
    # Locate the best weights
    best_weights = os.path.join(root_dir, "runs", "detect", "train", "weights", "best.pt")
    target_dir = os.path.join(root_dir, "models", "helmet")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "helmet_model.pt")
    
    if os.path.exists(best_weights):
        shutil.copy(best_weights, target_path)
        print(f"Trained helmet model saved successfully to: {target_path}")
        # Clean up runs directory
        shutil.rmtree(os.path.join(root_dir, "runs"), ignore_errors=True)
    else:
        print("Warning: training did not produce runs/detect/train/weights/best.pt. Copying yolov8n.pt as placeholder.")
        shutil.copy(model_path, target_path)

if __name__ == "__main__":
    main()
