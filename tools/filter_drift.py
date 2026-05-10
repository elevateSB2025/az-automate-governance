import json, sys 

with open("drift.json")as f:
    drift = json.load(f) 

filtered = [d for d in drift if d["severity"] in ("critical", "medium")]
print(json.dumps(filtered))
