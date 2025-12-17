YOUR_EMAIL = "himanshu.24mas10005@vitbhopal.ac.in" 
MAX_RESULTS_PER_SOURCE = 50 
REQUEST_DELAY = 2.0 
REQUEST_TIMEOUT = 30

RESEARCH_KEYWORDS = [
    "3D cell culture toxicology",
    "3D in vitro liver",
    "organ-on-chip liver",
    "hepatic spheroids",
    "liver toxicity models",
    "hepatotoxicity in vitro"
]

TITLE_KEYWORDS = [
    "toxicology", "toxicologist", "safety", "hepatic",
    "preclinical", "director", "head", "vp", "chief",
    "principal", "senior", "lead", "professor", "pi"
]

HUB_LOCATIONS = [
    "boston", "cambridge", "massachusetts", "ma",
    "san francisco", "bay area", "palo alto", "california",
    "san diego", "la jolla",
    "basel", "zurich", "switzerland",
    "london", "oxford", "cambridge", "uk", "united kingdom",
    "munich", "germany",
    "new jersey", "princeton",
    "research triangle", "north carolina",
    "maryland", "bethesda", "nih"
]

SCORING_WEIGHTS = {
    "title_match": 30,
    "funding_stage": 20,
    "uses_invitro": 15,
    "location_hub": 10,
    "recent_dili_publication": 40
}

OUTPUT_DIR = "output"
CSV_FILENAME = "3d_invitro_leads"
EXCEL_FILENAME = "3d_invitro_leads"