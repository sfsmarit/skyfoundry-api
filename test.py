import json
from skfapi import format_data
import config


file = "tmp/DG030-N-OSK.json"
dst = "tmp/fmt_" + file[4:]


with open(file, encoding="utf-8") as f:
    data = json.load(f)

formatted_data = format_data(data)

with open(config.URL_FILE, encoding="utf-8") as f:
    urls = json.load(f)

part = formatted_data["TapeOutName"]
formatted_data["url"] = urls.get(part, "")

with open(dst, "w", encoding="utf-8") as f:
    data = json.dump(formatted_data, f, indent=4)
