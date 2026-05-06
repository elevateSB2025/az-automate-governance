import json
import yaml
from pathlib import Path

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    base = Path(__file__).resolve().parents[1]  # repo root
    config_dir = base / "config"

    groups = load_yaml(config_dir / "groups.yml")
    roles = load_yaml(config_dir / "roles.yml")
    ca    = load_yaml(config_dir / "conditional-access.yml")

    combined = {
        "groups": groups.get("groups", []),
        "roleAssignments": roles.get("roleAssignments", []),
        "conditionalAccess": ca.get("conditionalAccess", {}),
    }

    output_path = base / "identity_config.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    print(f"Wrote {output_path}")

if __name__ == "__main__":
    main()
