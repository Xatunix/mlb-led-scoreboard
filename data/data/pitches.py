# A list of mlb pitch types appearing in statcast
# from statsapi.meta("pitchTypes")
# Dont change the index, but feel free to change
# the descriptions

PITCH_LONG = {
    "AB": "Auto Ball",  # MLB default is "Automatic Ball"
    "AS": "Auto Strike",  # MLB default is "Automatic Strike"
    "CH": "Change-up",
    "CU": "Curveball",
    "CS": "Slow Curve",
    "EP": "Eephus",
    "FC": "Cutter",
    "FA": "Fastball",
    "FF": "Fastball",  # MLB default is "Four-Seam Fastball"
    "FO": "Forkball",
    "FS": "Splitter",
    "FT": "2 Seamer",  # MLB default is "Two-Seam Fastball"
    "GY": "Gyroball",
    "IN": "Int Ball",  # MLB default is "Intentional Ball"
    "KC": "Knuckle Curve",
    "KN": "Knuckleball",
    "NP": "No Pitch",
    "PO": "Pitchout",
    "SC": "Screwball",
    "SI": "Sinker",
    "SL": "Slider",
    "ST": "Sweeper",
    "SV": "Slurve",
    "UN": "Unknown",
}

PITCH_SHORT = {
    "AB": "AB",
    "AS": "AS",
    "CH": "CH",
    "CU": "CV",
    "CS": "SCV",
    "EP": "EP",
    "FC": "CT",
    "FA": "FB",
    "FF": "4S",
    "FO": "FO",
    "FS": "SP",
    "FT": "2S",
    "GY": "GY",
    "IN": "IN",
    "KC": "KCV",
    "KN": "KN",
    "NP": "NP",
    "PO": "PO",
    "SC": "SCR",
    "SI": "SNK",
    "SL": "SL",
    "SV": "SV",
    "ST": "SW", # MLB default is "ST"
    "UN": "UN",
}


def fetch_long(value):
    return PITCH_LONG.get(value, PITCH_LONG["UN"])


def fetch_short(value):
    return PITCH_SHORT.get(value, PITCH_SHORT["UN"])
