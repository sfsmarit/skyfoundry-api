import json
import skfapi as api


tapeout = "DF030-P-OSK"

# ---------------------------------


token = api.acquire_token_client_credentials()

print(f"\tRequesting {tapeout}...")
try:
    data = api.get_tapeout_data(token, tapeout)
except Exception as e:
    print(e)
    exit()

# Write tape-out file
dst = f"test_{tapeout}.json"
with open(dst, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
