import os
import json
from datetime import datetime, timedelta
import string
from pathlib import Path


def load_settings():
    with open("settings.json", encoding="utf-8") as f:
        return json.load(f)


def get_start_date():
    settings = load_settings()
    days = settings["lookback_days"]
    return (datetime.now() - timedelta(days=days)).strftime("%m/%d/%Y")


def get_revision_codes(part: str):
    codes = string.ascii_uppercase
    if part[0] in ["D", "J"]:
        # MPS starts from "N"
        return codes[codes.index("N"):]
    return codes


DST_ROOT_DIR = Path("/data/tapeout")
DST_DATA_DIR = DST_ROOT_DIR / "data"


AUTHORITY = f"https://login.microsoftonline.com/a6f77e9a-f53b-4802-9d7b-201cd6376692"
CLIENT_ID = "5aa19a25-9f1a-4e97-8748-84b856c3907c"
SCOPE = ["e66e21b4-6c6b-4f0d-9765-f6e818884c25/.default"]
APIM_BASE = "https://skyworks.azure-api.net"

# .cshrc.local
CLIENT_SECRET = os.getenv("AAD_CLIENT_SECRET")
SUBSCRIPTION_KEY = os.getenv("APIM_SUBSCRIPTION_KEY")


SLEEP_TIME = 60*60
IGNORED_STATUSES = ["taped out", "cancelled"]


SUMMARY_KEYS = [
    "ScheduledTapeOutDate",
    "StatusName",
    "url",
    "BandNames",
    "ApplicationName",
    "DesignerName",
    "SFSTeamLeaderName",
]

SAVED_KEYS = [
    "TapeOutNumber",  # : 23752,
    "ScheduledTapeOutDate",  # ": \/Date(1761894000000)\/"
    "NewOrRevision",  # : "New",
    "ProductTypeName",  # : "MPS",
    "TapeOutTypeLabel",  # : "Engineering",
    "StatusName",  # : "Scheduled",
    "DesignSiteCode",  # : "IRV",
    "ApplicationName",  # : "Filter",
    "ProductDescription",  # : "2027_MPS_B12Rx+B13Rx+B14Rx/B28FRx_SKY53980 (PFAS Free + Modified cavity, MPS2.6, CSP5) MIMO",

    "DesignerID",  # : "marit",
    "DesignerName",  # : "Tomoo Mari",
    "SFSTeamLeaderName",  # : "Masafumi Iwaki",
    "Frequency",  # : "764M",
    "BandNames",  # : ["12","13","14","28"],
    "ProductManagerName",  # : "Ayumi Nishitaki",
    "TechnologyName",  # : "MPS LB2.6",
    "BETechnologyName",  # : "WLCSP5.1",
    "SolderTechnologyName",  # : "Solder",
    "PDKFETechnologyName",  # : "fe26",
    "PDKBETechnologyName",  # : "mps5",
    "SkyName",  # : "53980",
    "ProjectName",  # : "Stratosphere",
    "KeyCustomer",  # : "",

    "MDRNumber",  # : "Not found",

    "DXFFileDescriptions",
    "ChipSizeX",  # : 1100,
    "ChipSizeY",  # : 990,
    "ProductSizeX",  # : 1100,
    "ProductSizeY",  # : 990,
    "GDPW",  # : 9860,
    "DicingTypeName",  # : "Stealth Dicing",
    "DicingWidthX",  # : 0,
    "DicingWidthY",  # : 0,
    "WaferRotation",  # : "None",

    "OneSIDTPitch",  # : 4.677,
    "DutyFactorOffsetValue",  # : 0.6,
    "OneSSpaceWidthInCAD",  # : 1.1721,
    "OneSLineWidthInCAD",  # : 1.1664,
    "MParFileUsedInDesign",  # : "MPS2.5_LB03b_R042_Mo140_Al400_SiN20_LT0900_SiO2_0800_r1.0.mpar",
    "MParFileUsedInDesign2",  # : "",
    "MParFileUsedInDesign3",  # : "",

    "PurchaseRequests",

    "StackedFilterTapeOutName",  # : null,
    # "PDKFETechnologyVersion", #: "fe26_lb",
    # "PDKBETechnologyVersion", #: "mps5sd",
]
