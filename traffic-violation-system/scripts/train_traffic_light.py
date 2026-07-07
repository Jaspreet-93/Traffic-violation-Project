import os
import json
import cv2
import shutil
from ultralytics import YOLO

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Paths
    dataset_dir = os.path.join(root_dir, "datasets", "Traffic Light Detection Dataset")
    train_dataset_dir = os.path.join(dataset_dir, "train_dataset")
    json_path = os.path.join(train_dataset_dir, "train.json")
    
    temp_dir = os.path.join(root_dir, "models", "temp_light_train")
    
    train_img_dir = os.path.join(temp_dir, "images", "train")
    train_lbl_dir = os.path.join(temp_dir, "labels", "train")
    val_img_dir = os.path.join(temp_dir, "images", "val")
    val_lbl_dir = os.path.join(temp_dir, "labels", "val")
    
    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_lbl_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_lbl_dir, exist_ok=True)
    
    # Read custom json annotations
    print("Reading annotations from train.json...")
    with open(json_path) as f:
        data = json.load(f)
        
    annotations = data.get("annotations", [])
    
    count = 0
    for item in annotations:
        filename = item["filename"].replace('\\', '/') # e.g. "train_images/00001.jpg"
        src_jpg = os.path.join(train_dataset_dir, filename)
        
        if not os.path.exists(src_jpg):
            continue
            
        inbox = item.get("inbox", [])
        if not inbox:
            continue
            
        color = inbox[0].get("color")
        if color not in ["red", "yellow", "green"]:
            continue
            
        cls_id = ["red", "yellow", "green"].index(color)
        
        # Load image to get width and height
        img = cv2.imread(src_jpg)
        if img is None:
            continue
        h, w = img.shape[:2]
        
        # Parse box
        bndbox = item["bndbox"]
        xmin, ymin, xmax, ymax = bndbox["xmin"], bndbox["ymin"], bndbox["xmax"], bndbox["ymax"]
        
        # Normalize coordinates
        dw = 1.0 / w
        dh = 1.0 / h
        x_center = (xmin + xmax) / 2.0 * dw
        y_center = (ymin + ymax) / 2.0 * dh
        bbox_w = (xmax - xmin) * dw
        bbox_h = (ymax - ymin) * dh
        
        # Split into splits
        base_name = os.path.splitext(os.path.basename(filename))[0]
        jpg_name = base_name + ".jpg"
        txt_name = base_name + ".txt"
        
        if count < 10:
            dest_jpg = os.path.join(train_img_dir, jpg_name)
            dest_txt = os.path.join(train_lbl_dir, txt_name)
        elif count < 12:
            dest_jpg = os.path.join(val_img_dir, jpg_name)
            dest_txt = os.path.join(val_lbl_dir, txt_name)
        else:
            break
            
        shutil.copy(src_jpg, dest_jpg)
        with open(dest_txt, "w") as tf:
            tf.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}\n")
            
        count += 1
        
    # Create data.yaml
    data_yaml_content = f"""
path: {temp_dir}
train: images/train
val: images/val

nc: 3
names: ['red', 'yellow', 'green']
"""
    data_yaml_path = os.path.join(temp_dir, "data.yaml")
    with open(data_yaml_path, "w") as f:
        f.write(data_yaml_content.strip())
        
    # Start training
    base_model_path = os.path.join(root_dir, "models", "yolo", "yolov8n.pt")
    model = YOLO(base_model_path)
    
    print(f"Starting training on temporary dataset config: {data_yaml_path}")
    model.train(
        data=data_yaml_path,
        epochs=1,
        imgsz=640,
        device="cpu",
        workers=0,
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
            
    target_dir = os.path.join(root_dir, "models", "traffic_light")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "traffic_light_model.pt")
    
    if best_path and os.path.exists(best_path):
        shutil.copy(best_path, target_path)
        print(f"Trained traffic light model saved successfully to: {target_path}")
    else:
        print("Warning: training did not produce best.pt. Copying yolov8n.pt as fallback placeholder.")
        shutil.copy(base_model_path, target_path)
        
    # Clean up
    shutil.rmtree(temp_dir, ignore_errors=True)
    if os.path.exists(runs_detect_dir):
        shutil.rmtree(runs_detect_dir, ignore_errors=True)
    if os.path.exists(parent_runs):
        shutil.rmtree(parent_runs, ignore_errors=True)

if __name__ == "__main__":
    main()
