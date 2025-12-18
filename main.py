import msal
import requests
import config
import json


def format_json(data: dict):
    return data


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


def get_and_save_data(token: str, word: str):
    url = f"{config.APIM_BASE}/SkyFoundry/search_tapeout/{word}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
        "Accept": "application/json",
    }
    print(f"Requesting {word} data...")
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()["TapeOut"]

    if not isinstance(data, list):
        data = [data]

    for d in data:
        d = format_json(d)
        name = d["TapeOutName"]
        dst = config.DST_DATA_DIR / f"{name}.json"
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=4)
        print(dst)


if __name__ == "__main__":
    token = acquire_token_client_credentials()
    settings = config.load_settings()

    for word in settings["target_parts"]:
        get_and_save_data(token, word)
        exit()
