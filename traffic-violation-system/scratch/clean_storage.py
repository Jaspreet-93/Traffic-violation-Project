import os
import shutil

storage_root = r"c:\Users\Jaspreet\OneDrive\Desktop\Traffic violation Project\traffic-violation-system\storage"
orig_dir = os.path.join(storage_root, "original")
ann_dir = os.path.join(storage_root, "annotated")

for d in [orig_dir, ann_dir]:
    if os.path.exists(d):
        for f in os.listdir(d):
            fp = os.path.join(d, f)
            try:
                if os.path.isfile(fp):
                    os.unlink(fp)
                elif os.path.isdir(fp):
                    shutil.rmtree(fp)
                print(f"Deleted: {f}")
            except Exception as e:
                print(f"Failed to delete {f}: {e}")

print("Cleaned storage/original/ and storage/annotated/ successfully.")
