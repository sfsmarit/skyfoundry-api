import msal
import requests
import config
import json


def acquire_token_client_credentials() -> str:
    app = msal.ConfidentialClientApplication(
        client_id=config.CLIENT_ID,
        client_credential=config.CLIENT_SECRET,
        authority=config.AUTHORITY,
    )
    result = app.acquire_token_for_client(scopes=config.SCOPE)
    if "access_token" not in result:  # type: ignore
        raise RuntimeError(f"Token error: {result}")
    return result["access_token"]  # type: ignore


def call_api(tapeout_name: str, token: str):
    url = f"{config.APIM_BASE}/SkyFoundry/tapeout/{tapeout_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
        "Accept": "application/json",
    }
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    if "application/json" in r.headers.get("Content-Type", "").lower():
        dst = f"output/data/{tapeout_name}.json"
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(r.json(), f)
    else:
        dst = f"output/data/{tapeout_name}.txt"
        with open(dst, "w", encoding="utf-8") as f:
            f.write(r.text)
    print(dst)


if __name__ == "__main__":
    token = acquire_token_client_credentials()
    settings = config.load_settings()
    for header in settings["target_pn"]:
        for n, num in enumerate(range(1000)):
            for r, rev in enumerate(config.get_revision_codes(header)):
                tapeout_name = f"{header}{num}-{rev}-OSK"
                try:
                    call_api(tapeout_name, token)
                except:
                    break

            if r == 0:
                print(f"Tape-out not found for {header}{num}-*-OSK")
                break
