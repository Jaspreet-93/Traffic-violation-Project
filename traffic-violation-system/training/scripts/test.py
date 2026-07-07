import os
import argparse
import yaml
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="AI Model Inference Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to config YAML file")
    parser.add_argument("--weights", type=str, default="", help="Path to model weights file")
    parser.add_argument("--source", type=str, required=True, help="Path to input image/video or camera index")
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
        models_dir = os.path.join(root_dir, "models", model_name)
        if model_name == "number_plate":
            filename = "plate_detector.pt"
        else:
            filename = f"{model_name}_model.pt"
        weights_path = os.path.join(models_dir, filename)
        
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights file not found: {weights_path}")
        
    print(f"Loading weights from: {weights_path}")
    model = YOLO(weights_path)
    
    # Target directory to store inference output
    project_dir = os.path.join(root_dir, "experiments", "results")
    name_dir = f"inference_{model_name}"
    
    print(f"Running inference on source: {args.source}")
    results = model.predict(
        source=args.source,
        save=True,
        project=project_dir,
        name=name_dir,
        exist_ok=True,
        verbose=True
    )
    
    saved_run_path = os.path.join(project_dir, name_dir)
    print(f"\nInference completed successfully. Annotated outputs saved under: {saved_run_path}\n")

if __name__ == "__main__":
    main()
