import os
import json
from datetime import datetime, timedelta
import string
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


if os.name == "nt":
    URL_FILE = "tmp/url.json"
else:
    URL_FILE = "/home/marit/python/skyfoundry-scraper/output/url.json"

DST_ROOT_DIR = Path("/data/tapeout")
DST_DATA_DIR = DST_ROOT_DIR / "data"


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


AUTHORITY = os.getenv("AUTHORITY")
CLIENT_ID = os.getenv("CLIENT_ID")
SCOPE = [os.getenv("SCOPE")]
APIM_BASE = os.getenv("APIM_BASE")

CLIENT_SECRET = os.getenv("AAD_CLIENT_SECRET")
SUBSCRIPTION_KEY = os.getenv("APIM_SUBSCRIPTION_KEY")


SLEEP_TIME = 60*60
IGNORED_STATUSES = ["taped out", "cancelled"]


SUMMARY_KEYS = [
    "ScheduledTapeOutDate",
    "Status",
    "url",
    "BandNames",
    "Application",
    "LeadDesigner",
    "TeamLeader",
]

KEYS_TO_IGNORE = [
    "OriginalTapeOutName",
    "CreatedByID",
    "CreatedBy",
    "CreatedDate",
    "UpdatedByID",
    "UpdatedBy",
    "UpdatedDate",
    "Location",
    "PartName",
    "FoundryPartName",
    "Version",
    "MaskShop",
    "EdgeExclusion",
    "BondingOptions",
    "BondingOptionsSub",
    "PostProcessingDetails",
    "ScribePassivationRequirements",
    "SubstrateEPIDetails",
    "RevisionReason",
    "RevisionReasonDetail",
    "RevisionReasonText",
    "VersionNo",
    "TeamLeaderID",
    "ProductTestEngineerID",
    "ProductTestEngineer",
    "ProductManagerID",
    "ProgramManagerID",
    "ProgramManager",
    "ReleasedToMaskShopDate",
    "ActualTapeOutDate",
    "DataReadyDateTime",
    "AlignmentLayoutNo",
    "ThicknessAlMgCu",
    "ThicknessMo",
    "ThicknessSiO2_1",
    "ThicknessSiO2_2",
    "ThicknessSiO2_3",
    "SiO2ThicknessTrimming",
    "FrequencyTrimming",
    "MarkerLocationInProductBottomView",
    "IDTDirection",
    "ProvidingInternalReticleFloorplan",
    "ReticleLayoutFile",
    "DieMapMaskLayoutFile",
    "MaskLayerNotes",
    "SpecialRequest",
    "WaveLength",
    "DutyFactor",
    "LineWidth",
    "SpaceWidth",
    "MinimumLineWidthInDesign",
    "M1MetallizedAreaRatio",
    "CarrierAggr",
    "NumberOfPins",
    "IsPurchaseOrderFree",
    "PurchaseOrderFreeReason",
    "Pellicle",
    "BudgetCodeNotes",
    "Split",
    "WaferType",
    "Architecture",
    "PinPosition",
    "DesignNumber",
    "TapeOutDescription",
    "ProcessStartDate",
    "AlignmentLocationX",
    "AlignmentLocationY",
    "RecipeListFile",
    "MaskPONumber",
    "DesignReviewTemplate",
    "DesignParameterChecklist",
    "MDRMessage",
    "MDRComments",
    "MDRReleaseDate",
    "Attachments",
    "Comments",
    "GDSDetails",
    "LotStartRequests",
    "ThirdPartyIP",
    "UsersOnProject",
    "WaferOrders",
]
