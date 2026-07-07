import os
import xml.etree.ElementTree as ET
import shutil
from ultralytics import YOLO

def main():
    # Resolve the path relative to the root project directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Paths
    dataset_dir = os.path.join(root_dir, "datasets", "Indian vehicle license plate dataset", "State-wise_OLX", "DL")
    temp_dir = os.path.join(root_dir, "models", "temp_plate_train")
    
    train_img_dir = os.path.join(temp_dir, "images", "train")
    train_lbl_dir = os.path.join(temp_dir, "labels", "train")
    val_img_dir = os.path.join(temp_dir, "images", "val")
    val_lbl_dir = os.path.join(temp_dir, "labels", "val")
    
    os.makedirs(train_img_dir, exist_ok=True)
    os.makedirs(train_lbl_dir, exist_ok=True)
    os.makedirs(val_img_dir, exist_ok=True)
    os.makedirs(val_lbl_dir, exist_ok=True)
    
    # Process first 12 files as a tiny training/validation set
    xml_files = [f for f in os.listdir(dataset_dir) if f.endswith(".xml")]
    xml_files.sort()
    
    def convert_xml_to_yolo(xml_file_path, out_txt_path):
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)
        
        if width == 0 or height == 0:
            return False
            
        dw = 1.0 / width
        dh = 1.0 / height
        
        with open(out_txt_path, "w") as f:
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
                
                # Class 0: number plate
                f.write(f"0 {x_center:.6f} {y_center:.6f} {bbox_w:.6f} {bbox_h:.6f}\n")
        return True

    # Copy files and convert xml labels
    count = 0
    for i, xml_name in enumerate(xml_files):
        base_name = os.path.splitext(xml_name)[0]
        jpg_name = base_name + ".jpg"
        
        src_xml = os.path.join(dataset_dir, xml_name)
        src_jpg = os.path.join(dataset_dir, jpg_name)
        
        if not os.path.exists(src_jpg):
            continue
            
        if count < 10:
            dest_jpg = os.path.join(train_img_dir, jpg_name)
            dest_txt = os.path.join(train_lbl_dir, base_name + ".txt")
        elif count < 12:
            dest_jpg = os.path.join(val_img_dir, jpg_name)
            dest_txt = os.path.join(val_lbl_dir, base_name + ".txt")
        else:
            break
            
        shutil.copy(src_jpg, dest_jpg)
        if convert_xml_to_yolo(src_xml, dest_txt):
            count += 1
        
    # Create data.yaml config file
    data_yaml_content = f"""
path: {temp_dir}
train: images/train
val: images/val

nc: 1
names: ['number plate']
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
            
    target_dir = os.path.join(root_dir, "models", "number_plate")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "plate_detector.pt")
    
    if best_path and os.path.exists(best_path):
        shutil.copy(best_path, target_path)
        print(f"Trained number plate model saved successfully to: {target_path}")
    else:
        print("Warning: training did not produce best.pt. Copying yolov8n.pt as placeholder.")
        shutil.copy(base_model_path, target_path)
        
    # Clean up temp folder and runs outputs
    shutil.rmtree(temp_dir, ignore_errors=True)
    shutil.rmtree(runs_detect_dir, ignore_errors=True)

if __name__ == "__main__":
    main()
