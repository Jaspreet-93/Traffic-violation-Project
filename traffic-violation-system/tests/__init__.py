# Init tests package
import os
import sys

# Ensure traffic-violation-system root is on sys.path
sys_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

try:
    import torch
    # Monkeypatch torch.load to default to weights_only=False in PyTorch 2.6
    original_load = torch.load
    def safe_torch_load(*args, **kwargs):
        if 'weights_only' not in kwargs:
            kwargs['weights_only'] = False
        return original_load(*args, **kwargs)
    torch.load = safe_torch_load
except ImportError:
    pass

try:
    from app.database.connection import engine
    from app.database.base import Base
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

import httpx

original_httpx_init = httpx.Client.__init__

def patched_httpx_init(self, *args, **kwargs):
    kwargs.pop('app', None)
    original_httpx_init(self, *args, **kwargs)

httpx.Client.__init__ = patched_httpx_init
