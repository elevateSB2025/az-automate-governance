import os, msal, requests, json

client_id = os.environ["GRAPH_CLIENT_ID"]
tenant_id = os.environ["GRAPH_TENANT_ID"]
client_secret = os.environ["GRAPH_CLIENT_SECRET"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    client_id, authority=authority, client_credential=client_secret
)

token = app.acquire_token_for_client(scopes=scope)
headers = {"Authorization": f"Bearer {token['access_token']}"}

url = "https://graph.microsoft.com/beta/reports/identitySecureScores"

resp = requests.get(url, headers=headers)
resp.raise_for_status()

data = resp.json().get("value", [])

if not data:
    print("null")
    exit(0)

score = data[0].get("currentScore", None)

print(score if score is not None else "null")
