#!/usr/bin/env python3
"""
Interactive setup:
1) asks for WhatsApp phone + tokens
2) runs Google OAuth InstalledApp flow to obtain a refresh token
3) writes .env
4) offers to deploy on Vercel using vercel CLI (must be logged in)
"""
import json, os, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar"]
ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"

CLIENT_JSON_PATH = ROOT / "client_secret.json"

def prompt(msg: str, default: str = "") -> str:
    v = input(f"{msg} [{default}]: ").strip()
    return v or default

def google_oauth() -> dict:
    if not CLIENT_JSON_PATH.exists():
        print("Place your OAuth client JSON at:", CLIENT_JSON_PATH)
        sys.exit(1)
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_JSON_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
        return {
            "GOOGLE_CLIENT_ID": flow.client_config["client_id"],
            "GOOGLE_CLIENT_SECRET": flow.client_config["client_secret"],
            "GOOGLE_REFRESH_TOKEN": creds.refresh_token,
        }

def write_env(env: dict):
    lines = []
    for k, v in env.items():
        lines.append(f"{k}={v}")
    ENV_FILE.write_text("\n".join(lines) + "\n")
    print("Written:", ENV_FILE)

def deploy_vercel():
    try:
        subprocess.run(["vercel", "--version"], check=True)
    except Exception:
        print("Install Vercel CLI first: npm i -g vercel")
        return
    # Link & deploy
    subprocess.run(["vercel", "link", "--yes"], check=True)
    subprocess.run(["vercel", "env", "pull", ".env"], check=False)
    subprocess.run(["vercel", "deploy", "--prod", "--yes"], check=True)

def main():
    print("=== WhatsApp + Google Calendar Setup ===")
    env = {}
    env["TZ"] = prompt("Timezone", "America/Sao_Paulo")

    print("-- WhatsApp Cloud API --")
    env["WABA_VERIFY_TOKEN"] = prompt("Webhook Verify Token", "my-verify-token")
    env["WABA_ACCESS_TOKEN"] = prompt("Access Token (Meta Graph)")
    env["WABA_PHONE_NUMBER_ID"] = prompt("Phone Number ID")
    env["RECIPIENT_PHONE_E164"] = prompt("Recipient phone (E.164)")
    env["ALLOWED_SENDER_PHONE_E164"] = prompt("Allowed sender (optional)", env["RECIPIENT_PHONE_E164"])

    print("-- Google OAuth --")
    g = google_oauth()
    env.update(g)
    env["GOOGLE_CALENDAR_ID"] = prompt("Calendar ID", "primary")

    env["DAILY_SEND_HOUR_LOCAL"] = prompt("Daily send hour (0-23)", "8")
    env["DAILY_SEND_MINUTE_LOCAL"] = prompt("Daily send minute (0-59)", "0")

    write_env(env)

    if prompt("Deploy to Vercel now? y/N", "N").lower() == "y":
        deploy_vercel()

if __name__ == "__main__":
    main()