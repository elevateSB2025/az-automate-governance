import json
import sys

with open("opa_results.json", "r") as f:
    data = json.load(f)

violations = []

for result in data:
    for failure in result.get("failures", []):
        violations.append(failure.get("msg"))

# Print violations as a single JSON array for GitHub Actions
print(json.dumps(violations))
