SINGLE = "single"
DOUBLE = "double"
TRIPLE = "triple"
HOME_RUN = "home_run"

SINGLE_RBI = "single_rbi"
DOUBLE_RBI = "double_rbi"
TRIPLE_RBI = "triple_rbi"
WALK_RBI = "walk_rbi"

WALK = "walk"
INTENTIONAL_WALK = "intent_walk"
HIT_BY_PITCH = "hit_by_pitch"

STRIKEOUT = "strikeout"
STRIKEOUT_ALT = "strike_out"
STRIKEOUT_LOOKING = "strikeout_looking"

ERROR = "error"
FIELDERS_CHOICE = "fielders_choice"

FIELD_OUT = "field_out"
FIELD_OUT_FLY = "field_out_fly"
FIELD_OUT_LINE = "field_out_line"
FIELD_OUT_GROUND = "field_out_ground"
FIELD_OUT_POP = "field_out_pop"

SACRIFICE_BUNT = "sac_bunt"
SACRIFICE_FLY = "sac_fly"

DOUBLE_PLAY = "double_play"
DOUBLE_PLAY_ALT = "grounded_into_double_play"

STOLEN_BASE_2B = "stolen_base_2b"
STOLEN_BASE_3B = "stolen_base_3b"
STOLEN_BASE_HOME = "stolen_base_home"

HITS = [SINGLE, DOUBLE, TRIPLE, HOME_RUN, SINGLE_RBI, DOUBLE_RBI, TRIPLE_RBI, WALK_RBI, FIELD_OUT, FIELD_OUT_FLY, FIELD_OUT_LINE, FIELD_OUT_GROUND, FIELD_OUT_POP, SACRIFICE_BUNT, SACRIFICE_FLY, ERROR, FIELDERS_CHOICE, DOUBLE_PLAY, DOUBLE_PLAY_ALT]

OUTS = [FIELD_OUT, FIELD_OUT_FLY, FIELD_OUT_LINE, FIELD_OUT_GROUND, FIELD_OUT_POP, SACRIFICE_BUNT, FIELDERS_CHOICE, DOUBLE_PLAY, DOUBLE_PLAY_ALT]

SCORING = [HOME_RUN, SINGLE_RBI, DOUBLE_RBI, TRIPLE_RBI, SACRIFICE_FLY, STOLEN_BASE_HOME, WALK_RBI]

WALKS = [WALK, INTENTIONAL_WALK, HIT_BY_PITCH, STOLEN_BASE_2B, STOLEN_BASE_3B, STOLEN_BASE_HOME, WALK_RBI]

OTHERS = [ERROR, FIELDERS_CHOICE, DOUBLE_PLAY, DOUBLE_PLAY_ALT]

STRIKEOUTS = [STRIKEOUT, STRIKEOUT_ALT, STRIKEOUT_LOOKING]

PLAY_RESULTS = {
    SINGLE: {"short": "1B", "long": "Single"},
    DOUBLE: {"short": "2B", "long": "Double"},
    TRIPLE: {"short": "3B", "long": "Triple"},
    HOME_RUN: {"short": "HR", "long": "Home Run"},
    WALK: {"short": "BB", "long": "Walk"},
    INTENTIONAL_WALK: {"short": "IBB", "long": "Int Walk"},
    STRIKEOUT: {"short": "K", "long": "StrKeout"},
    STRIKEOUT_ALT: {"short": "K", "long": "StrKeout"},
    STRIKEOUT_LOOKING: {"short": "ꓘ", "long": "Strꓘeout"},
    HIT_BY_PITCH: {"short": "HBP", "long": "Hit Bttr"},
    ERROR: {"short": "E", "long": "Error"},
    FIELDERS_CHOICE: {"short": "FC", "long": "Fld Chce"},
    FIELD_OUT_FLY: {"short": "FO", "long": "Flyout"},
    FIELD_OUT_LINE: {"short": "LO", "long": "Lineout"},
    FIELD_OUT_GROUND: {"short": "GO", "long": "Grndout"},
    FIELD_OUT_POP: {"short": "PO", "long": "Popout"},
    FIELD_OUT: {"short": "O", "long": "Out"},
    DOUBLE_PLAY: {"short": "DP", "long": "Dbl Play"},
    DOUBLE_PLAY_ALT: {"short": "DP", "long": "Dbl Play"},
    SACRIFICE_BUNT: {"short": "ScB", "long": "Sac Bunt"},
    SACRIFICE_FLY: {"short": "ScF", "long": "Sac Fly"},
    SINGLE_RBI: {"short": "1B", "long": "RBI Sngl"},
    DOUBLE_RBI: {"short": "2B", "long": "RBI Dble"},
    TRIPLE_RBI: {"short": "3B", "long": "RBI Trpl"},
    WALK_RBI: {"short": "BB", "long": "RBI Walk"},
    STOLEN_BASE_2B: {"short": "SB", "long": "Stoln Bs"},
    STOLEN_BASE_3B: {"short": "SB", "long": "Stoln Bs"},
    STOLEN_BASE_HOME: {"short": "SB", "long": "Stole Home"},
}
