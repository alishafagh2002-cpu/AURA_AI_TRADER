
import getpass
import requests

token = getpass.getpass("Paste exposed Nobitex token: ").strip()

s = requests.Session()
s.trust_env = False

r = s.post(
    "https://apiv2.nobitex.ir/auth/logout/",
    headers={
        "Authorization": f"Token {token}",
        "Accept": "application/json",
        "User-Agent": "TraderBot/AURA-1.0"
    },
    timeout=30
)

print("STATUS:", r.status_code)
print(r.text)
