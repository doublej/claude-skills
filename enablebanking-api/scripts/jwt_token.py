#!/usr/bin/env python3
"""Mint an Enable Banking JWT (RS256). Usage: python jwt_token.py [config.json]"""
import json
import sys
from datetime import datetime
from pathlib import Path

import jwt as pyjwt


def make_jwt(app_id: str, key_path: str, ttl_seconds: int = 3600) -> str:
    iat = int(datetime.now().timestamp())
    return pyjwt.encode(
        {
            "iss": "enablebanking.com",
            "aud": "api.enablebanking.com",
            "iat": iat,
            "exp": iat + ttl_seconds,
        },
        Path(key_path).read_bytes(),
        algorithm="RS256",
        headers={"kid": app_id},
    )


if __name__ == "__main__":
    cfg_path = Path(sys.argv[1] if len(sys.argv) > 1 else "config.json")
    cfg = json.loads(cfg_path.read_text())
    print(make_jwt(cfg["applicationId"], cfg["keyPath"]))
