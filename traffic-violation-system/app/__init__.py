import torch

# Monkeypatch torch.load to default to weights_only=False in PyTorch 2.6
# This fixes WeightsUnpickler exceptions when loading third-party models (like Ultralytics YOLOv8)
original_load = torch.load
def safe_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = safe_torch_load
