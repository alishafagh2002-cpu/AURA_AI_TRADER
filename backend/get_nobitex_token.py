
import requests
import getpass
from pathlib import Path

BASE = "https://apiv2.nobitex.ir"

email = input("Nobitex email: ").strip()
password = getpass.getpass("Nobitex password: ")
totp = input("2FA code: ").strip()

session = requests.Session()
session.trust_env = False

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "TraderBot/AURA-1.0",
    "X-TOTP": totp
}

payload = {
    "username": email,
    "password": password,
    "captcha": "api",
    "remember": "yes"
}

r = session.post(
    BASE + "/auth/login/",
    json=payload,
    headers=headers,
    timeout=30
)

data = r.json()

if r.status_code != 200 or data.get("status") != "success":
    print("LOGIN FAILED:", r.status_code, data)
    raise SystemExit(1)

token = data["key"]

env = Path(".env")
text = env.read_text(encoding="utf-8") if env.exists() else ""

lines = []
found = False

for line in text.splitlines():
    if line.startswith("NOBITEX_TOKEN="):
        lines.append("NOBITEX_TOKEN=" + token)
        found = True
    else:
        lines.append(line)

if not found:
    lines.append("NOBITEX_TOKEN=" + token)

env.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("NOBITEX TOKEN SAVED")
print("Expires in:", data.get("expiresIn"))
