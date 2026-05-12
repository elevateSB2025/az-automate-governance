import os, msal, requests, json, sys

client_id = os.environ["GRAPH_CLIENT_ID"]
tenant_id = os.environ["GRAPH_TENANT_ID"]
client_secret = os.environ["GRAPH_CLIENT_SECRET"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    client_id, authority=authority, client_credential=client_secret
)

token = app.acquire_token_for_client(scopes=scope)

if "access_token" not in token:
    print(f"Token Error: {token.get('error_description')}", file=sys.stderr)
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {token['access_token']}",
    "Content-Type": "application/json",
    "ConsistencyLevel": "eventual"
}

# Theory: Beta 'reports' path is more restrictive than 'security' path
url = "https://graph.microsoft.com/v1.0/security/secureScores"
params = {"$top": 1}

try:
    resp = requests.get(url, headers=headers, params=params)
    
    if resp.status_code != 200:
        # This will tell us if it's a licensing, filter, or permission issue
        print(f"Graph API Error: {resp.status_code}", file=sys.stderr)
        print(f"Response: {resp.text}", file=sys.stderr) 
        
        # FALLBACK: Try the stable V1.0 security endpoint if Beta fails
        print("Attempting fallback to v1.0 security endpoint...", file=sys.stderr)
        url = "https://graph.microsoft.com/v1.0/security/secureScores"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()

    data = resp.json().get("value", [])

    if not data:
        print("null")
    else:
        # Beta identitySecureScores uses 'currentScore'
        # v1.0 secureScores uses 'azureActiveDirectoryScore'
        score = data[0].get("currentScore") or data[0].get("azureActiveDirectoryScore")
        print(score if score is not None else "null")

except Exception as e:
    print(f"Final script failure: {e}", file=sys.stderr)
    sys.exit(1)
