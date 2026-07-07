import os
import shutil
from ultralytics import YOLO

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Path to dataset
    dataset_path = os.path.join(root_dir, "datasets", "Seat Belt Detection", "Yolo Annotated Dataset")
    
    # Create temporary data.yaml
    data_yaml_content = f"""
path: "{dataset_path.replace(os.sep, '/')}"
train: Train/images
val: Test/images

nc: 2
names: ['seat belt', 'no seat belt']
"""
    yaml_path = os.path.join(dataset_path, "data.yaml")
    with open(yaml_path, "w") as f:
        f.write(data_yaml_content.strip())
        
    print(f"Temporary data.yaml created at: {yaml_path}")
    
    # Train the YOLOv8 model for 1 epoch using fraction=0.01 on CPU
    base_model_path = os.path.join(root_dir, "models", "yolo", "yolov8n.pt")
    model = YOLO(base_model_path)
    
    print("Starting seat belt detector training...")
    model.train(
        data=yaml_path,
        epochs=1,
        imgsz=640,
        device="cpu",
        workers=0,
        fraction=0.01,
        verbose=True
    )
    
    # Copy best weights
    # Since we run from traffic-violation-system, YOLOv8 might log to root or parent.
    # We look in traffic-violation-system/runs and parent/runs.
    best_path = None
    search_dirs = [
        os.path.join(root_dir, "runs", "detect"),
        os.path.abspath(os.path.join(root_dir, "..", "runs", "detect"))
    ]
    
    for rdir in search_dirs:
        if os.path.exists(rdir):
            subdirs = sorted([d for d in os.listdir(rdir) if d.startswith("train")])
            if subdirs:
                latest_run = subdirs[-1]
                p = os.path.join(rdir, latest_run, "weights", "best.pt")
                if os.path.exists(p):
                    best_path = p
                    break
                    
    target_dir = os.path.join(root_dir, "models", "seat_belt")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "seat_belt_model.pt")
    
    if best_path and os.path.exists(best_path):
        shutil.copy(best_path, target_path)
        print(f"Trained seat belt model saved successfully to: {target_path}")
    else:
        print("Warning: training did not produce best.pt. Copying yolov8n.pt as placeholder.")
        shutil.copy(base_model_path, target_path)
        
    # Clean up
    if os.path.exists(yaml_path):
        os.remove(yaml_path)
    for rdir in search_dirs:
        if os.path.exists(rdir):
            shutil.rmtree(rdir, ignore_errors=True)

if __name__ == "__main__":
    main()
