import os
import json
import xml.etree.ElementTree as ET

def check_dataset(config: dict, root_project_dir: str) -> bool:
    """
    Checks the validity of the dataset structure described in the config dict.
    Returns True if valid, raises ValueError or FileNotFoundError if invalid.
    """
    print(f"Checking dataset for: {config.get('model_name')}")
    dataset_path = os.path.abspath(os.path.join(root_project_dir, config['path']))
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset root directory not found: {dataset_path}")
        
    fmt = config.get("format")
    
    if fmt == "yolo":
        train_img_path = os.path.join(dataset_path, config['train'])
        val_img_path = os.path.join(dataset_path, config['val'])
        
        if not os.path.exists(train_img_path):
            raise FileNotFoundError(f"YOLO train images path not found: {train_img_path}")
        if not os.path.exists(val_img_path):
            raise FileNotFoundError(f"YOLO validation images path not found: {val_img_path}")
            
        # Basic check of folder content
        train_imgs = [f for f in os.listdir(train_img_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        val_imgs = [f for f in os.listdir(val_img_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        print(f"Found {len(train_imgs)} training images and {len(val_imgs)} validation images.")
        
    elif fmt == "xml":
        source_dir = os.path.join(dataset_path, config['source_dir'])
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"XML source path not found: {source_dir}")
            
        xml_files = [f for f in os.listdir(source_dir) if f.endswith(".xml")]
        jpg_files = [f for f in os.listdir(source_dir) if f.lower().endswith(".jpg")]
        
        print(f"Found {len(xml_files)} xml files and {len(jpg_files)} images in source directory.")
        if len(xml_files) == 0:
            raise ValueError(f"No XML files found in: {source_dir}")
            
    elif fmt == "custom_json":
        json_path = os.path.join(dataset_path, config['source_json'])
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Custom JSON annotations not found: {json_path}")
            
        # Parse JSON keys briefly
        with open(json_path) as f:
            data = json.load(f)
        if "annotations" not in data:
            raise ValueError(f"Invalid custom JSON annotations schema, missing 'annotations' key in: {json_path}")
            
        print(f"Found {len(data['annotations'])} items in custom JSON annotations file.")
        
    else:
        raise ValueError(f"Unsupported dataset format: {fmt}")
        
    return True
