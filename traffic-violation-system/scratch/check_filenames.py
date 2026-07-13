import os

uploads_dir = r"c:\Users\Jaspreet\OneDrive\Desktop\Traffic violation Project\traffic-violation-system\uploads"
files = os.listdir(uploads_dir)

print("All files in uploads starting with 'violation':")
for file in files:
    if file.startswith("violation") or "sample" in file.lower() or "mock" in file.lower():
        print(f"  - {file} ({os.path.getsize(os.path.join(uploads_dir, file))} bytes)")
