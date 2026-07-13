import re

log_path = r"C:\Users\Jaspreet\.gemini\antigravity\brain\9dfc1f27-4129-4b0b-bffe-f8fb2a32cd88\.system_generated\tasks\task-7288.log"

with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    log_content = f.read()

# Look for tracebacks
tracebacks = re.findall(r"(Traceback .*?)(?=INFO:|\d{4}-\d{2}-\d{2}|$)", log_content, re.DOTALL)
print(f"Total tracebacks found: {len(tracebacks)}")
for tb in tracebacks[-5:]:
    print("--- TRACEBACK ---")
    print(tb.strip())
    print("-----------------\n")
