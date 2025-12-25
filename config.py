import os
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


SCRIPT_DIR = Path(__file__).resolve().parent

SETTING_FILE = SCRIPT_DIR / "settings.json"


def load_settings():
    with open(SETTING_FILE, encoding="utf-8") as f:
        return json.load(f)


if os.name == "nt":
    URL_FILE = SCRIPT_DIR / "tmp" / "url.json"
else:
    URL_FILE = "/home/marit/python/skyfoundry-scraper/output/url.json"

SUMMARY_FILE = SCRIPT_DIR / "output" / "summary.json"
UPDATE_LOG_FILE = SCRIPT_DIR / "output" / "update.log"
TAPEOUT_DIR = SCRIPT_DIR / "output" / "tapeout"
os.makedirs(TAPEOUT_DIR, exist_ok=True)


AUTHORITY = os.getenv("AUTHORITY")
CLIENT_ID = os.getenv("CLIENT_ID")
SCOPE = [os.getenv("SCOPE")]
APIM_BASE = os.getenv("APIM_BASE")

CLIENT_SECRET = os.getenv("AAD_CLIENT_SECRET")
SUBSCRIPTION_KEY = os.getenv("APIM_SUBSCRIPTION_KEY")


STATUSES_TO_EXLUDE = [
    "Taped Out", "Cancelled"
]

SUMMARY_KEYS = [
    "ScheduledTapeOutDate",
    "Status",
    "Application",
    "Bands",
    "SkyNumber",
    "LeadDesigner",
    "TeamLeader",
    "url",
]

KEYS_TO_EXCLUDE = [
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
    # "RevisionReasonDetail",
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
