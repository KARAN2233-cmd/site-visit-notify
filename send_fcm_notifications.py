#!/usr/bin/env python3
"""
Sends a push notification to every saved device token using the
FCM HTTP v1 API.
"""

import json
import os
import sys
import urllib.request
import urllib.error

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
except ImportError:
    print("Missing dependency. Run: pip install google-auth", file=sys.stderr)
    sys.exit(1)

GAS_APPS_SCRIPT_URL = os.environ["GAS_APPS_SCRIPT_URL"]
FIREBASE_PROJECT_ID = os.environ["FIREBASE_PROJECT_ID"]
SERVICE_ACCOUNT_JSON = os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"]

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]
FCM_V1_URL = f"https://fcm.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/messages:send"


def get_access_token():
    info = json.loads(SERVICE_ACCOUNT_JSON)
    credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    credentials.refresh(Request())
    return credentials.token


def fetch_tokens():
    req = urllib.request.Request(
        GAS_APPS_SCRIPT_URL,
        data=json.dumps({"action": "listTokens"}).encode("utf-8"),
        headers={"Content-Type": "text/plain;charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body.get("tokens", [])


def send_notification(access_token, device_token, title, body_text):
    payload = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body_text,
            },
        }
    }
    req = urllib.request.Request(
        FCM_V1_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; UTF-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  -> OK ({resp.status}) for token {device_token[:12]}...")
    except urllib.error.HTTPError as e:
        print(f"  -> FAILED ({e.code}) for token {device_token[:12]}...: {e.read().decode('utf-8')}")


def main():
    print("Fetching device tokens from Apps Script...")
    tokens = fetch_tokens()
    if not tokens:
        print("No device tokens found. Nothing to send.")
        return

    print(f"Found {len(tokens)} token(s). Getting access token...")
    access_token = get_access_token()

    title = "Site Visit Reminder"
    body_text = "Please complete today's site visit form."

    for t in tokens:
        send_notification(access_token, t, title, body_text)

    print("Done.")


if __name__ == "__main__":
    main()
