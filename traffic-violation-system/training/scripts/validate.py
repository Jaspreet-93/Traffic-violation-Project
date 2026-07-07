import os
import argparse
import yaml
import json
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="AI Model Validation Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to config YAML file")
    parser.add_argument("--weights", type=str, default="", help="Path to model weights file")
    return parser.parse_args()

def main():
    args = parse_args()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    
    # Read config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
        
    model_name = config.get("model_name")
    
    # Resolve weights
    if args.weights:
        weights_path = args.weights
    else:
        # Defaults to the active system model path
        models_dir = os.path.join(root_dir, "models", model_name)
        if model_name == "number_plate":
            filename = "plate_detector.pt"
        else:
            filename = f"{model_name}_model.pt"
        weights_path = os.path.join(models_dir, filename)
        
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights file not found: {weights_path}")
        
    # Get prepared dataset YAML configuration
    # (If train.py was run, it cache prepared standard yaml configs in cache/<model_name>/data.yaml)
    cache_yaml = os.path.join(root_dir, "training", "cache", model_name, "data.yaml")
    if os.path.exists(cache_yaml):
        data_yaml_path = cache_yaml
    else:
        # Fallback to checking paths relative to dataset folder
        dataset_root = os.path.abspath(os.path.join(root_dir, config['path']))
        data_yaml_path = os.path.join(dataset_root, "data.yaml")
        if not os.path.exists(data_yaml_path):
            # Write a basic temporary one
            data_yaml_path = os.path.join(root_dir, "training", "cache", model_name, "data.yaml")
            os.makedirs(os.path.dirname(data_yaml_path), exist_ok=True)
            yaml_content = f"""
path: {dataset_root.replace(os.sep, '/')}
train: {config.get('train', 'train/images')}
val: {config.get('val', 'valid/images')}
nc: {config['nc']}
names: {config['names']}
"""
            with open(data_yaml_path, "w") as tf:
                tf.write(yaml_content.strip())
                
    print(f"Loading weights from: {weights_path}")
    model = YOLO(weights_path)
    
    print(f"Validating model on config: {data_yaml_path}")
    results = model.val(
        data=data_yaml_path,
        imgsz=640,
        device="cpu",
        workers=0,
        verbose=True
    )
    
    # Extract validation metrics
    metrics = {
        "mAP50": float(results.results_dict.get("metrics/mAP50(B)", 0.0)),
        "mAP50-95": float(results.results_dict.get("metrics/mAP50-95(B)", 0.0)),
        "precision": float(results.results_dict.get("metrics/precision(B)", 0.0)),
        "recall": float(results.results_dict.get("metrics/recall(B)", 0.0)),
        "box_loss": float(results.results_dict.get("val/box_loss", 0.0)),
        "cls_loss": float(results.results_dict.get("val/cls_loss", 0.0))
    }
    
    # Save validation metrics
    metrics_dir = os.path.join(root_dir, "experiments", "metrics")
    os.makedirs(metrics_dir, exist_ok=True)
    val_log_path = os.path.join(metrics_dir, f"validation_{model_name}.json")
    with open(val_log_path, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print("\n--- Validation Summary ---")
    print(f"Model: {model_name}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"mAP50: {metrics['mAP50']:.4f}")
    print(f"mAP50-95: {metrics['mAP50-95']:.4f}")
    print(f"Metrics saved to: {val_log_path}\n")

if __name__ == "__main__":
    main()
