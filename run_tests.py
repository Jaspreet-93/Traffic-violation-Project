#!/usr/bin/env python
"""
Smart Traffic Violation Detection System - Test Suite Runner
Runs all unit, api, and model tests with proper environment initialization.
"""
import os
import sys
import unittest

# Ensure traffic-violation-system is on the path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(PROJECT_ROOT, "traffic-violation-system")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# PyTorch 2.6 weights_only patch
try:
    import torch
    original_load = torch.load
    def safe_torch_load(*args, **kwargs):
        if "weights_only" not in kwargs:
            kwargs["weights_only"] = False
        return original_load(*args, **kwargs)
    torch.load = safe_torch_load
except ImportError:
    pass

# Patch httpx for FastAPI TestClient
try:
    import httpx
    original_httpx_init = httpx.Client.__init__
    def patched_httpx_init(self, *args, **kwargs):
        kwargs.pop("app", None)
        original_httpx_init(self, *args, **kwargs)
    httpx.Client.__init__ = patched_httpx_init
except ImportError:
    pass

# Initialize database schema if available
try:
    from app.database.connection import engine
    from app.database.base import Base
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[WARN] DB initialization skipped: {e}")

def main():
    test_dir = os.path.join(APP_DIR, "tests")
    print(f"[*] Discovering and running tests in: {test_dir}")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n[SUCCESS] All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n[FAILURE] {len(result.failures)} failure(s), {len(result.errors)} error(s).")
        sys.exit(1)

if __name__ == "__main__":
    main()
