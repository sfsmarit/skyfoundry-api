import sys
import json

import skfapi as api


word = sys.argv[1]

# ---------------------------------


token = api.acquire_token_client_credentials()

print(f"Requesting tapeouts named '{word}'...")
try:
    tapeouts = api.find_tapeouts(token, word)
except Exception as e:
    print(e)
    exit()

for data in tapeouts:
    tapeout = data["TapeOutName"]

    print(f"\tRequesting {tapeout}...")
    try:
        data = api.get_tapeout_data(token, tapeout)
    except Exception as e:
        print(e)
        continue

    # Write tape-out file
    dst = f"raw/{tapeout}.json"
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
