# Intergalactic Webhook Service Writeup

## Additional notes

The intended solution is DNS rebinding (e.g. via `rbndr.us`): register a webhook whose hostname alternately resolves to a public IP (which passes the registration check; any HTTP server on port 5001 will do) and to `127.0.0.1`. When the webhook fires and the name resolves to `127.0.0.1`, the server-side fetcher requests the internal flag server on `127.0.0.1:5001/flag` (SSRF). Because it needs outbound DNS and a publicly reachable server, `solve.py` (configured with `URL` and `REBIND_IP`) is meant for live use and is not registered as an offline `pwnmake check`.
