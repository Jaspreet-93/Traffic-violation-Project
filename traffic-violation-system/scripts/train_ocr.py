import os
import torch
import torch.nn as nn

class OCRModel(nn.Module):
    def __init__(self):
        super().__init__()
        # Simple convolutional network to process cropped 64x64 number plate images
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Linear(32 * 16 * 16, 36) # Classify characters (letters + digits)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Initialize model structure
    model = OCRModel()
    
    # Save path setup
    target_dir = os.path.join(root_dir, "models", "ocr")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, "ocr_model.pt")
    
    # Save the PyTorch model
    torch.save(model, target_path)
    print(f"OCR model structure saved successfully to: {target_path}")

if __name__ == "__main__":
    main()
