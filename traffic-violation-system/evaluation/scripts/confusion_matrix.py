import os
import cv2
import numpy as np

def generate_confusion_matrix_image(y_true: list, y_pred: list, labels: list, output_path: str):
    """
    Draws a visual confusion matrix using OpenCV and saves it as a PNG image.
    Avoids external plotting dependencies like matplotlib.
    """
    num_classes = len(labels)
    if num_classes == 0:
        return
        
    # Construct confusion matrix array
    cm = np.zeros((num_classes, num_classes), dtype=np.int32)
    label_to_idx = {l: i for i, l in enumerate(labels)}
    
    for yt, yp in zip(y_true, y_pred):
        if yt in label_to_idx and yp in label_to_idx:
            cm[label_to_idx[yt]][label_to_idx[yp]] += 1
            
    # Parameters for drawing
    cell_size = 80
    header_offset = 60
    border = 20
    
    width = num_classes * cell_size + header_offset + border * 2
    height = num_classes * cell_size + header_offset + border * 2
    
    # White canvas
    img = np.zeros((height, width, 3), dtype=np.uint8) + 255
    
    # Draw title
    cv2.putText(img, "Confusion Matrix", (border, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    
    # Draw axes labels
    cv2.putText(img, "Predicted", (header_offset + int((num_classes * cell_size)/2) - 40, border + 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1, cv2.LINE_AA)
                
    # Draw grid cells
    for i in range(num_classes):
        # Y axis label (Actual)
        cv2.putText(img, labels[i][:8], (border, header_offset + i * cell_size + int(cell_size/2) + 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 1, cv2.LINE_AA)
                    
        # X axis label (Predicted)
        cv2.putText(img, labels[i][:8], (header_offset + i * cell_size + 10, header_offset - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 50, 50), 1, cv2.LINE_AA)
                    
        for j in range(num_classes):
            x1 = header_offset + j * cell_size
            y1 = header_offset + i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            val = cm[i][j]
            
            # Diagonal cells: Green highlight. Off-diagonal: Red highlight for non-zero errors.
            if i == j:
                color = (200, 255, 200) # Soft green
            elif val > 0:
                color = (200, 200, 255) # Soft red/blue
            else:
                color = (240, 240, 240) # Soft grey
                
            cv2.rectangle(img, (x1, y1), (x2, y2), color, cv2.FILLED)
            cv2.rectangle(img, (x1, y1), (x2, y2), (180, 180, 180), 1) # border
            
            # Write value inside cell
            cv2.putText(img, str(val), (x1 + int(cell_size/2) - 10, y1 + int(cell_size/2) + 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                        
    # Ensure target directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, img)
    print(f"Confusion matrix visualization saved successfully to: {output_path}")

def main():
    # Helper to verify matrix drawing locally
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(root_dir, "experiments", "results")
    
    # Generate a dummy confusion matrix report test
    y_true = ["red", "red", "green", "green", "yellow", "red", "green"]
    y_pred = ["red", "yellow", "green", "green", "yellow", "red", "red"]
    labels = ["red", "yellow", "green"]
    
    dest = os.path.join(out_dir, "confusion_matrix_test.png")
    generate_confusion_matrix_image(y_true, y_pred, labels, dest)

if __name__ == "__main__":
    main()
