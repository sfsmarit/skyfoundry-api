import msal
import requests
import config
import json
import time


def format_data(data: dict):
    result = {}
    for k, v in data.items():
        if k in config.KEYS_TO_EXCLUDE:
            continue

        if "Date" in k:
            result[k] = v[:10].replace("-", "/")
            continue

        match k:
            case "WaferSize":
                result[k] = v[:v.index('"')] + "inch"
            case "Approvals":
                result[k] = {d["Function"]: bool(d["SignedOffDateTime"]) for d in v}
            case "Bands":
                result[k] = "/".join(d["Band"] for d in v)
            case "DXFDetails":
                result[k] = v[0]["DRC"]
            case "MaskLayers":
                result[k] = {
                    d["Layer"]: {
                        "OrderMask": True if d["OrderMask"].lower() == "yes" else False,
                        "SFSMaskName": d["SFSMaskName"],
                    } for d in v
                }
            case "PurchaseOrders":
                result[k] = {d["RequestNo"]: d["TechnologyArea"] for d in v}
            case "StackLayers":
                result[k] = {d["StackLayerName"]: d["StackLayerValue"] for d in v}
            case "Waivers":
                result[k] = {d["WaiverType"][1:]: d["WaiverStatus"] for d in v}
            case _:
                result[k] = v

    return result


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


def find_tapeouts(token: str, word: str):
    url = f"{config.APIM_BASE}/SkyFoundry/search_tapeout/{word}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
        "Accept": "application/json",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()["TapeOut"]

    if not isinstance(data, list):
        data = [data]

    keys = ["TapeOutName", "Status", "ScheduledTapeOutDate"]
    return [{k: d[k] for k in keys} for d in data]


def get_tapeout_data(token: str, tapeout: str):
    url = f"{config.APIM_BASE}/SkyFoundry/tapeout/{tapeout}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Ocp-Apim-Subscription-Key": config.SUBSCRIPTION_KEY,
        "Accept": "application/json",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()["PartTapeOut"]


if __name__ == "__main__":
    token = acquire_token_client_credentials()

    while True:
        settings = config.load_settings()

        # Load summary
        try:
            with open(config.SUMMARY_FILE, encoding="utf-8") as f:
                summary = json.load(f)
        except:
            print(f"{config.SUMMARY_FILE} not found")
            summary = {}

        # Load url
        try:
            with open(config.URL_FILE, encoding="utf-8") as f:
                urls = json.load(f)
        except:
            print(f"{config.URL_FILE} not found")
            urls = {}

        for word in settings["target_parts"]:
            print(f"Requesting {word} data...")
            tapeouts = find_tapeouts(token, word)

            for data in tapeouts:
                tapeout = data["TapeOutName"]

                status_in_summary = summary.get(tapeout, {}).get("Status", "")
                if status_in_summary in config.STATUSES_TO_EXLUDE:
                    print("\t\t", f"Skip {tapeout} ({status_in_summary})")
                    continue

                print(f"\tRequesting {tapeout} data...")
                data = get_tapeout_data(token, tapeout)
                data = format_data(data)

                # Add url
                data["url"] = urls.get(tapeout, "")

                # Write tape-out file
                dst = config.TAPEOUT_DIR / f"{tapeout}.json"
                with open(dst, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print("\t\t", dst)

                # Write into summary
                summary[tapeout] = {k: data[k] for k in config.SUMMARY_KEYS}
                with open(config.SUMMARY_FILE, "w", encoding="utf-8") as f:
                    json.dump(summary, f, ensure_ascii=False, indent=4)

                # exit()

        time.sleep(settings["sleep_sec"])
