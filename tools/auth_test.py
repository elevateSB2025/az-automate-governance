import os
import msal
import requests

client_id = os.environ["GRAPH_CLIENT_ID"]
tenant_id = os.environ["GRAPH_TENANT_ID"]
client_secret = os.environ["GRAPH_CLIENT_SECRET"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

result = app.acquire_token_for_client(scopes=scope)

if "access_token" not in result:
    raise Exception("Authentication failed: %s" % result)

print("Authenticated successfully!")

# Test call: list first 5 users
resp = requests.get(
    "https://graph.microsoft.com/v1.0/users?$top=5",
    headers={"Authorization": f"Bearer {result['access_token']}"}
)

print("Graph response:", resp.json())
