#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def bootstrap_django() -> None:
    root = repo_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaccination_project.settings_local")

    import django

    django.setup()


def build_cookie(token: str, base_url: str) -> dict:
    from django.contrib.sessions.backends.db import SessionStore
    from vaccinations.models import Doctor

    doctor = Doctor.objects.filter(portal_token=token).first()
    if not doctor:
        raise SystemExit(f"No doctor found for portal token: {token}")

    session = SessionStore()
    session["doctor_auth"] = {
        "token": doctor.portal_token,
        "doctor_id": doctor.id,
        "email": doctor.email,
    }
    session.create()

    return {
        "name": "sessionid",
        "value": session.session_key,
        "url": base_url,
        "path": "/",
        "httpOnly": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local doctor-auth session cookie.")
    parser.add_argument("--token", required=True, help="Doctor portal token")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL for the cookie")
    parser.add_argument("--output", help="Optional JSON file to write")
    args = parser.parse_args()

    bootstrap_django()
    cookie = build_cookie(args.token, args.base_url.rstrip("/"))

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(cookie, indent=2), encoding="utf-8")
    else:
        print(json.dumps(cookie, indent=2))


if __name__ == "__main__":
    main()
