import json

with open("identity_config.json") as f:
    desired = json.load(f)

with open("tenant_state.json") as f:
    actual = json.load(f)

drift = []

# Identity drift: groups
desired_group_names = {g["name"] for g in desired["groups"]}
actual_group_names  = {g["displayName"] for g in actual["groups"]}

missing_groups = desired_group_names - actual_group_names
extra_groups   = actual_group_names - desired_group_names

for g in missing_groups:
    drift.append({
        "type": "group_missing",
        "name": g,
        "severity": "medium",
        "message": f"Desired group '{g}' is missing in tenant."
    })

# OAuth drift: apps + permissions (simplified)
desired_apps = {a["displayName"]: a for a in desired.get("oauth", [])}
actual_sps   = {sp["displayName"]: sp for sp in actual["servicePrincipals"]}

for name, app in desired_apps.items():
    if name not in actual_sps:
        drift.append({
            "type": "app_missing",
            "name": name,
            "severity": "critical",
            "message": f"Required app '{name}' is missing in tenant."
        })
        continue

    sp = actual_sps[name]
    # You can expand this to compare appRoles/oauth2PermissionScopes
    # For now, just record presence
    # TODO: map requiredApplicationPermissions to appRoles, etc.

with open("drift.json", "w") as f:
    json.dump(drift, f, indent=2)

print(json.dumps(drift))
