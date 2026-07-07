import os
import shutil
from ultralytics import YOLO

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Paths
    dataset_yaml = os.path.join(
        root_dir, "datasets", "Driver behaviors.v10i.yolov8", "data.yaml"
    )
    
    # Modify data.yaml content dynamically to ensure absolute paths to train/valid/test
    # Since Roboflow yaml usually contains relative paths like '../train/images'
    # which can fail depending on execution directory context.
    dataset_dir = os.path.dirname(dataset_yaml)
    
    # Read YAML
    with open(dataset_yaml, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if line.startswith("train:"):
            new_lines.append(f"train: {os.path.join(dataset_dir, 'train', 'images')}\n")
        elif line.startswith("val:"):
            new_lines.append(f"val: {os.path.join(dataset_dir, 'valid', 'images')}\n")
        elif line.startswith("test:"):
            new_lines.append(f"test: {os.path.join(dataset_dir, 'test', 'images')}\n")
        else:
            new_lines.append(line)
            
    temp_yaml = os.path.join(dataset_dir, "temp_data.yaml")
    with open(temp_yaml, "w") as f:
        f.writelines(new_lines)
        
    base_model_path = os.path.join(root_dir, "models", "yolo", "yolov8n.pt")
    model = YOLO(base_model_path)
    
    print(f"Starting training on temporary dataset config: {temp_yaml}")
    model.train(
        data=temp_yaml,
        epochs=1,
        imgsz=640,
        device="cpu",
        workers=0,
        fraction=0.01,
        verbose=True
    )
    
    # Locate the best weights in runs/detect/
    best_path = None
    runs_detect_dir = os.path.join(root_dir, "runs", "detect")
    if os.path.exists(runs_detect_dir):
        subdirs = sorted([d for d in os.listdir(runs_detect_dir) if d.startswith("train")])
        if subdirs:
            latest_run = subdirs[-1]
            best_path = os.path.join(runs_detect_dir, latest_run, "weights", "best.pt")
            
    # Parent runs directory search fallback
    parent_runs = os.path.abspath(os.path.join(root_dir, "..", "runs", "detect"))
    if not best_path and os.path.exists(parent_runs):
        subdirs = sorted([d for d in os.listdir(parent_runs) if d.startswith("train")])
        if subdirs:
            latest_run = subdirs[-1]
            best_path = os.path.join(parent_runs, latest_run, "weights", "best.pt")
            
    target_dir = os.path.join(root_dir, "models", "driver_behavior")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "driver_behavior_model.pt")
    
    if best_path and os.path.exists(best_path):
        shutil.copy(best_path, target_path)
        print(f"Trained driver behavior model saved successfully to: {target_path}")
    else:
        print("Warning: training did not produce best.pt. Copying yolov8n.pt as fallback placeholder.")
        shutil.copy(base_model_path, target_path)
        
    # Clean up
    if os.path.exists(temp_yaml):
        os.remove(temp_yaml)
    if os.path.exists(runs_detect_dir):
        shutil.rmtree(runs_detect_dir, ignore_errors=True)
    if os.path.exists(parent_runs):
        shutil.rmtree(parent_runs, ignore_errors=True)

if __name__ == "__main__":
    main()
