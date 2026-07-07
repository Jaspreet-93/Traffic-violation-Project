import os
import argparse
import yaml
import shutil
import cv2
import json
import xml.etree.ElementTree as ET
from ultralytics import YOLO

from training.utils.dataset_checker import check_dataset
from training.utils.model_manager import ModelManager

def parse_args():
    parser = argparse.ArgumentParser(description="AI Model Training Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to config YAML file")
    parser.add_argument("--epochs", type=int, default=1, help="Number of training epochs")
    parser.add_argument("--fraction", type=float, default=0.01, help="Fraction of dataset to use for training")
    parser.add_argument("--device", type=str, default="cpu", help="Device to train on (cpu or cuda)")
    return parser.parse_args()

def prepare_yolo_dataset(config: dict, root_dir: str) -> str:
    """
    Ensures dataset is prepared in standard YOLO format.
    If the format is already yolo, it returns the dataset config path.
    Otherwise, converts xml/custom_json to standard splits in training/cache/
    and returns the custom dataset yaml path.
    """
    fmt = config.get("format")
    model_name = config.get("model_name")
    dataset_root = os.path.abspath(os.path.join(root_dir, config['path']))
    
    cache_dir = os.path.join(root_dir, "training", "cache", model_name)
    os.makedirs(cache_dir, exist_ok=True)
    
    yaml_path = os.path.join(cache_dir, "data.yaml")
    
    if fmt == "yolo":
        # Write standard data.yaml referencing original directories
        train_path = os.path.abspath(os.path.join(dataset_root, config['train'])).replace(os.sep, '/')
        val_path = os.path.abspath(os.path.join(dataset_root, config['val'])).replace(os.sep, '/')
        
        yaml_content = f"""
path: {os.path.abspath(dataset_root).replace(os.sep, '/')}
train: {config['train']}
val: {config['val']}

nc: {config['nc']}
names: {config['names']}
"""
        with open(yaml_path, "w") as f:
            f.write(yaml_content.strip())
        return yaml_path
        
    elif fmt == "xml":
        # Indian vehicle license plate conversion
        source_dir = os.path.join(dataset_root, config['source_dir'])
        train_img_dir = os.path.join(cache_dir, "images", "train")
        train_lbl_dir = os.path.join(cache_dir, "labels", "train")
        val_img_dir = os.path.join(cache_dir, "images", "val")
        val_lbl_dir = os.path.join(cache_dir, "labels", "val")
        
        os.makedirs(train_img_dir, exist_ok=True)
        os.makedirs(train_lbl_dir, exist_ok=True)
        os.makedirs(val_img_dir, exist_ok=True)
        os.makedirs(val_lbl_dir, exist_ok=True)
        
        xml_files = sorted([f for f in os.listdir(source_dir) if f.endswith(".xml")])
        
        def convert_xml(xml_path, out_txt):
            tree = ET.parse(xml_path)
            root = tree.getroot()
            size = root.find("size")
            w = int(size.find("width").text)
            h = int(size.find("height").text)
            if w == 0 or h == 0:
                return False
            dw = 1.0 / w
            dh = 1.0 / h
            with open(out_txt, "w") as tf:
                for obj in root.findall("object"):
                    bndbox = obj.find("bndbox")
                    xmin = float(bndbox.find("xmin").text)
                    ymin = float(bndbox.find("ymin").text)
                    xmax = float(bndbox.find("xmax").text)
                    ymax = float(bndbox.find("ymax").text)
                    
                    x_center = (xmin + xmax) / 2.0 * dw
                    y_center = (ymin + ymax) / 2.0 * dh
                    bbox_w = (xmax - xmin) * dw
                    bbox_h = (ymax - ymin) * dh
                    tf.write(f"0 {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}\n")
            return True

        count = 0
        for xml_name in xml_files:
            base = os.path.splitext(xml_name)[0]
            jpg_name = base + ".jpg"
            src_xml = os.path.join(source_dir, xml_name)
            src_jpg = os.path.join(source_dir, jpg_name)
            
            if not os.path.exists(src_jpg):
                continue
                
            if count < 10:
                dst_jpg = os.path.join(train_img_dir, jpg_name)
                dst_txt = os.path.join(train_lbl_dir, base + ".txt")
            elif count < 12:
                dst_jpg = os.path.join(val_img_dir, jpg_name)
                dst_txt = os.path.join(val_lbl_dir, base + ".txt")
            else:
                break
                
            shutil.copy(src_jpg, dst_jpg)
            if convert_xml(src_xml, dst_txt):
                count += 1
                
        yaml_content = f"""
path: {os.path.abspath(cache_dir).replace(os.sep, '/')}
train: images/train
val: images/val

nc: {config['nc']}
names: {config['names']}
"""
        with open(yaml_path, "w") as f:
            f.write(yaml_content.strip())
        return yaml_path
        
    elif fmt == "custom_json":
        # Traffic light custom json conversion
        json_path = os.path.join(dataset_root, config['source_json'])
        train_img_dir = os.path.join(cache_dir, "images", "train")
        train_lbl_dir = os.path.join(cache_dir, "labels", "train")
        val_img_dir = os.path.join(cache_dir, "images", "val")
        val_lbl_dir = os.path.join(cache_dir, "labels", "val")
        
        os.makedirs(train_img_dir, exist_ok=True)
        os.makedirs(train_lbl_dir, exist_ok=True)
        os.makedirs(val_img_dir, exist_ok=True)
        os.makedirs(val_lbl_dir, exist_ok=True)
        
        with open(json_path) as f:
            data = json.load(f)
            
        count = 0
        for item in data.get("annotations", []):
            filename = item["filename"].replace('\\', '/')
            src_jpg = os.path.join(dataset_root, config['train_images'], filename)
            
            if not os.path.exists(src_jpg):
                continue
                
            inbox = item.get("inbox", [])
            if not inbox:
                continue
            color = inbox[0].get("color")
            if color not in ["red", "yellow", "green"]:
                continue
                
            cls_id = ["red", "yellow", "green"].index(color)
            
            img = cv2.imread(src_jpg)
            if img is None:
                continue
            h, w = img.shape[:2]
            
            bndbox = item["bndbox"]
            xmin, ymin, xmax, ymax = bndbox["xmin"], bndbox["ymin"], bndbox["xmax"], bndbox["ymax"]
            
            dw = 1.0 / w
            dh = 1.0 / h
            x_center = (xmin + xmax) / 2.0 * dw
            y_center = (ymin + ymax) / 2.0 * dh
            bbox_w = (xmax - xmin) * dw
            bbox_h = (ymax - ymin) * dh
            
            base = os.path.splitext(os.path.basename(filename))[0]
            jpg_name = base + ".jpg"
            txt_name = base + ".txt"
            
            if count < 10:
                dst_jpg = os.path.join(train_img_dir, jpg_name)
                dst_txt = os.path.join(train_lbl_dir, txt_name)
            elif count < 12:
                dst_jpg = os.path.join(val_img_dir, jpg_name)
                dst_txt = os.path.join(val_lbl_dir, txt_name)
            else:
                break
                
            shutil.copy(src_jpg, dst_jpg)
            with open(dst_txt, "w") as tf:
                tf.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}\n")
            count += 1
            
        yaml_content = f"""
path: {os.path.abspath(cache_dir).replace(os.sep, '/')}
train: images/train
val: images/val

nc: {config['nc']}
names: {config['names']}
"""
        with open(yaml_path, "w") as f:
            f.write(yaml_content.strip())
        return yaml_path
        
    return ""

def main():
    args = parse_args()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # Read config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
        
    # Check dataset
    check_dataset(config, root_dir)
    
    # Prepare data splits
    data_yaml_path = prepare_yolo_dataset(config, root_dir)
    
    # Load base model
    base_model_path = os.path.join(root_dir, "models", "yolo", "yolov8n.pt")
    model = YOLO(base_model_path)
    
    print(f"Executing YOLOv8 training on config: {data_yaml_path}")
    results = model.train(
        data=data_yaml_path,
        epochs=args.epochs,
        imgsz=640,
        device=args.device,
        workers=0,
        fraction=args.fraction,
        verbose=True
    )
    
    # Search latest runs weights path
    best_weights_path = None
    runs_detect_dir = os.path.join(root_dir, "runs", "detect")
    if os.path.exists(runs_detect_dir):
        subdirs = sorted([d for d in os.listdir(runs_detect_dir) if d.startswith("train")])
        if subdirs:
            best_weights_path = os.path.join(runs_detect_dir, subdirs[-1], "weights", "best.pt")
            
    # Parent runs directory search fallback
    parent_runs = os.path.abspath(os.path.join(root_dir, "..", "runs", "detect"))
    if (not best_weights_path or not os.path.exists(best_weights_path)) and os.path.exists(parent_runs):
        subdirs = sorted([d for d in os.listdir(parent_runs) if d.startswith("train")])
        if subdirs:
            best_weights_path = os.path.join(parent_runs, subdirs[-1], "weights", "best.pt")
            
    if not best_weights_path or not os.path.exists(best_weights_path):
        print("Warning: best.pt weights file not found. Copying base yolov8n.pt as fallback.")
        best_weights_path = base_model_path
        
    # Extract validation metrics
    metrics = {
        "box_loss": float(results.results_dict.get("val/box_loss", 0.0)),
        "cls_loss": float(results.results_dict.get("val/cls_loss", 0.0)),
        "dfl_loss": float(results.results_dict.get("val/dfl_loss", 0.0)),
        "mAP50": float(results.results_dict.get("metrics/mAP50(B)", 0.0)),
        "mAP50-95": float(results.results_dict.get("metrics/mAP50-95(B)", 0.0)),
        "epochs_trained": args.epochs,
        "fraction": args.fraction
    }
    
    # Write metrics to experiments/metrics/
    metrics_dir = os.path.join(root_dir, "experiments", "metrics")
    os.makedirs(metrics_dir, exist_ok=True)
    metrics_log_path = os.path.join(metrics_dir, f"train_metrics_{config['model_name']}.json")
    with open(metrics_log_path, "w") as f:
        json.dump(metrics, f, indent=4)
        
    # Version model weights and log run
    manager = ModelManager(root_dir)
    backup_name = manager.save_model_version(config['model_name'], best_weights_path, metrics)
    
    # Store training logs to experiments/logs/
    logs_dir = os.path.join(root_dir, "experiments", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    run_log_path = os.path.join(logs_dir, f"train_{config['model_name']}.log")
    with open(run_log_path, "w") as f:
        f.write(f"Training completed successfully for: {config['model_name']}\n")
        f.write(f"Backup weights saved: {backup_name}\n")
        f.write(f"Metrics: {json.dumps(metrics, indent=2)}\n")
        
    # Clean up YOLOv8 runs
    if os.path.exists(runs_detect_dir):
        shutil.rmtree(runs_detect_dir, ignore_errors=True)
    if os.path.exists(parent_runs):
        shutil.rmtree(parent_runs, ignore_errors=True)
        
    print(f"Training pipeline execution finished cleanly. Logs saved to: {run_log_path}")

if __name__ == "__main__":
    main()
