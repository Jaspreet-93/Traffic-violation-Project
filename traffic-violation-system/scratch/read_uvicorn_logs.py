log_path = r"C:\Users\Jaspreet\.gemini\antigravity\brain\9dfc1f27-4129-4b0b-bffe-f8fb2a32cd88\.system_generated\tasks\task-7288.log"

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
matches = []
for line in lines:
    if "/reports" in line:
        matches.append(line.strip())

print(f"Found {len(matches)} matches:")
for m in matches[-30:]:
    print(m)
