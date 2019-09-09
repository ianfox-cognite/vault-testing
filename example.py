import requests
import os

VAULT_ADDR = os.environ.get("VAULT_ADDR") or "http://127.0.0.1:8200"
VAULT_TOKEN = os.environ.get("VAULT_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {VAULT_TOKEN}"
}

# Helpers for making requests
class Vault:
    @classmethod
    def request(cls, method, url, *args, **kwargs):
        r = requests.request(method, VAULT_ADDR + "/v1" + url, headers=HEADERS, *args, **kwargs)
        if r.status_code > 299:
            raise Exception(f"{r.status_code}: {r.text}")
        return r

    @classmethod
    def post(cls, url, *args, **kwargs):
        return cls.request("post", url, *args, **kwargs)

    @classmethod
    def get(cls, url, *args, **kwargs):
        return cls.request("get", url, *args, **kwargs)

    @classmethod
    def delete(cls, url, *args, **kwargs):
        return cls.request("delete", url, *args, **kwargs)

# Clean up
Vault.delete("/identity/oidc/role/myrole")
Vault.delete("/identity/oidc/key/mykey")

# Create the entity
Vault.post("/identity/entity", json = {
    "name": "entity-1"
})

# Create the role
r = Vault.post("/identity/oidc/role/myrole", json = {
    "key": "mykey"
})

CLIENT_ID = Vault.get("/identity/oidc/role/myrole").json()['data']['client_id']

# Create the key
Vault.post("/identity/oidc/key/mykey", json = {
    "allowed_client_ids": CLIENT_ID
})

# TODO: login with https://www.vaultproject.io/api/auth/gcp/index.html#login and set the VAULT_TOKEN to the result from that

# Get id token with https://www.vaultproject.io/docs/secrets/identity/index.html#identity-tokens
# Note: the docs say this should be a POST request, but vault replies with a 405. So I think it's a get.
# TODO: figure out how to associate the entity we created on line 36 with our token
Vault.get("/identity/oidc/token/myrole")

# TODO: make request to the Cognite API using this ID token (under `Authorization: Bearer`)
