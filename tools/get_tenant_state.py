import os, msal, requests, json

client_id = os.environ["643f5f54-dec0-4c9a-aa1d-e51f00410de7"]
tenant_id = os.environ["3e0eb729-4df6-4cad-b961-a007ac64fa60"]
client_secret = os.environ["Kqa8Q~CV46Wdp8D5vVzmlSx4YW7OtZK8t6kujcby"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    client_id, authority=authority, client_credential=client_secret
)
token = app.acquire_token_for_client(scopes=scope)
headers = {"Authorization": f"Bearer {token['access_token']}"}

def get(url):
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def main():
    # Users, groups, directory roles, service principals
    groups = get("https://graph.microsoft.com/v1.0/groups?$select=id,displayName")
    roles  = get("https://graph.microsoft.com/v1.0/directoryRoles?$expand=members")
    sps    = get("https://graph.microsoft.com/v1.0/servicePrincipals?$select=id,appId,displayName,appRoles,oauth2PermissionScopes")

    state = {
        "groups": groups.get("value", []),
        "roles": roles.get("value", []),
        "servicePrincipals": sps.get("value", []),
    }

    with open("tenant_state.json", "w") as f:
        json.dump(state, f, indent=2)

if __name__ == "__main__":
    main()
