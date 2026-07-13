import os

reports_dir = r"c:\Users\Jaspreet\OneDrive\Desktop\Traffic violation Project\traffic-violation-system\reports"
if os.path.exists(reports_dir):
    files = os.listdir(reports_dir)
    print(f"Total files in reports: {len(files)}")
    for f in files:
        fp = os.path.join(reports_dir, f)
        size = os.path.getsize(fp)
        if size > 100 or f.endswith(".xlsx") or f.endswith(".csv"):
            print(f"  - {f} ({size} bytes)")
else:
    print("Reports directory does NOT exist!")
