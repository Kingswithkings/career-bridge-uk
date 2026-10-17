"""Run locally in an interactive terminal; never paste credentials into chat."""

import getpass
import json
import os
from pathlib import Path
import tempfile
import urllib.error
import urllib.parse
import urllib.request


ERROR_HINTS = {
    "invalid_code": "The authorization code is expired, already used, or invalid. Generate a fresh code from the same Self Client.",
    "invalid_client": "Check the Client ID and that the Self Client was created in the .com API Console.",
    "invalid_client_secret": "Copy the Client Secret again from the same Self Client as the Client ID.",
    "invalid_scope": "Use exactly ZohoMail.messages.CREATE,ZohoMail.accounts.READ when generating the code.",
    "invalid_grant": "Generate a fresh authorization code from the same Self Client and try again.",
    "access_denied": "Zoho denied access. Check the account permissions in Zoho.",
}


def safe_error(payload):
    # Only display known error identifiers, never arbitrary provider content.
    error = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error, str) and error in ERROR_HINTS:
        return f"{error}: {ERROR_HINTS[error]}"
    return "Zoho rejected the request; no private response details are displayed."


def request_json(url, data=None, token=None):
    stage = "Account lookup" if token else "Token exchange"
    headers = {}
    if token:
        headers["Authorization"] = f"Zoho-oauthtoken {token}"
    body = urllib.parse.urlencode(data).encode() if data else None
    request = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read(16384))
        except (ValueError, OSError):
            payload = {}
        hint = safe_error(payload)
        if exc.code == 429:
            hint = "Too many attempts. Wait before trying again."
        elif exc.code >= 500:
            hint = "Zoho reported a server error. Try again later."
        raise ValueError(f"{stage} failed (HTTP {exc.code}). {hint}") from None
    if isinstance(payload, dict) and payload.get("error"):
        raise ValueError(f"{stage} failed. {safe_error(payload)}")
    return payload


def main():
    print("Zoho Mail .com setup for kings@1st-kings.com. No emails will be sent.")
    client_id = getpass.getpass("Zoho Client ID (hidden): ").strip()
    client_secret = getpass.getpass("Zoho Client Secret (hidden): ").strip()
    print("Now generate a Self Client code with these scopes:")
    print("ZohoMail.messages.CREATE,ZohoMail.accounts.READ")
    code = getpass.getpass("Paste the newly generated code (hidden): ").strip()
    if not all((client_id, client_secret, code)):
        raise ValueError("All three values are required; run the helper again.")
    tokens = request_json("https://accounts.zoho.com/oauth/v2/token", {
        "grant_type": "authorization_code", "client_id": client_id,
        "client_secret": client_secret, "code": code,
    })
    if not tokens.get("refresh_token") or not tokens.get("access_token"):
        raise ValueError("Zoho did not issue tokens. Check your credentials and generate a fresh code.")

    # Preserve the refresh token immediately, even if account discovery fails.
    fd, filename = tempfile.mkstemp(prefix="careerbridge-zoho-", suffix=".env")
    with os.fdopen(fd, "w") as output:
        output.write(f"ZOHO_REFRESH_TOKEN={tokens['refresh_token']}\n")
    print(f"Refresh token saved privately in: {filename}")
    accounts = request_json("https://mail.zoho.com/api/accounts", token=tokens["access_token"])
    for account in accounts.get("data", []):
        addresses = [account.get("primaryEmailAddress", ""), account.get("mailboxAddress", "")]
        addresses.extend(item.get("mailId", "") for item in account.get("emailAddress", []))
        if "kings@1st-kings.com" in [address.lower() for address in addresses]:
            account_id = str(account.get("accountId", ""))
            if not account_id.isdigit():
                raise ValueError("Zoho returned an invalid account ID.")
            with Path(filename).open("a") as output:
                output.write(f"ZOHO_ACCOUNT_ID={account_id}\n")
            print("Setup complete. Open that file locally and copy its two values into Render Environment.")
            print("Do not share the file in chat or commit it. Delete it after saving the values in Render.")
            return
    raise ValueError("Sender account was not found. Check you signed in as kings@1st-kings.com.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nSetup cancelled.")
        raise SystemExit(1)
    except Exception as exc:
        # Do not print HTTP response bodies or tokens.
        print(str(exc) if isinstance(exc, ValueError) else f"Setup failed ({type(exc).__name__}). Check your connection and Zoho setup.")
        raise SystemExit(1)
