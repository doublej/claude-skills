#!/usr/bin/env python3
"""End-to-end Enable Banking AIS flow: ASPSPs → auth → session → balances → transactions.

Adapted from https://github.com/enablebanking/enablebanking-api-samples (Apache-2.0).
Run: python ais_flow.py
Expects ../config.json with {"applicationId": "...", "keyPath": "..."} at repo root.
"""
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pprint import pprint
from urllib.parse import parse_qs, urlparse

import requests

from jwt_token import make_jwt

API = "https://api.enablebanking.com"
ASPSP_NAME = os.environ.get("ASPSP_NAME", "ING")
ASPSP_COUNTRY = os.environ.get("ASPSP_COUNTRY", "NL")


def main() -> None:
    cfg = json.load(open("config.json"))
    jwt = make_jwt(cfg["applicationId"], cfg["keyPath"])
    h = {"Authorization": f"Bearer {jwt}"}

    app = requests.get(f"{API}/application", headers=h).json()
    print("App:", app["name"], "redirect_urls:", app["redirect_urls"])

    aspsps = requests.get(f"{API}/aspsps", headers=h).json()["aspsps"]
    matches = [a for a in aspsps if a["name"] == ASPSP_NAME and a["country"] == ASPSP_COUNTRY]
    if not matches:
        print(f"ASPSP {ASPSP_NAME}/{ASPSP_COUNTRY} not found. Available NL:")
        pprint([a["name"] for a in aspsps if a["country"] == "NL"])
        sys.exit(1)

    body = {
        "access": {"valid_until": (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()},
        "aspsp": {"name": ASPSP_NAME, "country": ASPSP_COUNTRY},
        "state": str(uuid.uuid4()),
        "redirect_url": app["redirect_urls"][0],
        "psu_type": "personal",
    }
    auth = requests.post(f"{API}/auth", json=body, headers=h)
    auth.raise_for_status()
    print(f"Open this URL to authenticate:\n{auth.json()['url']}\n")

    redirected = input("Paste redirect URL after bank auth: ")
    code = parse_qs(urlparse(redirected).query)["code"][0]

    sess = requests.post(f"{API}/sessions", json={"code": code}, headers=h)
    sess.raise_for_status()
    session = sess.json()
    sid = session["session_id"]
    print(f"session_id={sid}, {len(session['accounts'])} accounts")

    for acc in session["accounts"]:
        uid = acc["uid"]
        print(f"\n=== Account {acc.get('iban') or uid} ===")
        bal = requests.get(f"{API}/accounts/{uid}/balances", headers=h).json()
        for b in bal["balances"]:
            print(f"  {b['balance_type']}: {b['balance_amount']['amount']} {b['balance_amount']['currency']}")

        query = {"date_from": (datetime.now(timezone.utc) - timedelta(days=90)).date().isoformat()}
        key = None
        total = 0
        while True:
            if key:
                query["continuation_key"] = key
            r = requests.get(f"{API}/accounts/{uid}/transactions", params=query, headers=h).json()
            total += len(r["transactions"])
            key = r.get("continuation_key")
            if not key:
                break
        print(f"  {total} transactions in last 90d")

    requests.delete(f"{API}/sessions/{sid}", headers=h)
    print("\nSession deleted.")


if __name__ == "__main__":
    main()
