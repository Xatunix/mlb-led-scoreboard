# the following were created like so
# import statsapi
# teams = statsapi.get('teams', {'sportIds':1})['teams']
#
# TEAM_FULL = {t['teamName']:t['name'] for t in teams}
# TEAM_ABBR_LN = {t['name']:t['abbreviation'] for t in teams}

TEAM_FULL = {
    "Athletics": "Oakland Athletics",
    "Pirates": "Pittsburgh Pirates",
    "Padres": "San Diego Padres",
    "Mariners": "Seattle Mariners",
    "Giants": "San Francisco Giants",
    "Cardinals": "St. Louis Cardinals",
    "Rays": "Tampa Bay Rays",
    "Rangers": "Texas Rangers",
    "Blue Jays": "Toronto Blue Jays",
    "Twins": "Minnesota Twins",
    "Phillies": "Philadelphia Phillies",
    "Braves": "Atlanta Braves",
    "White Sox": "Chicago White Sox",
    "Marlins": "Miami Marlins",
    "Yankees": "New York Yankees",
    "Brewers": "Milwaukee Brewers",
    "Angels": "Los Angeles Angels",
    "D-backs": "Arizona Diamondbacks",
    "Orioles": "Baltimore Orioles",
    "Red Sox": "Boston Red Sox",
    "Cubs": "Chicago Cubs",
    "Reds": "Cincinnati Reds",
    "Guardians": "Cleveland Guardians",
    "Rockies": "Colorado Rockies",
    "Tigers": "Detroit Tigers",
    "Astros": "Houston Astros",
    "Royals": "Kansas City Royals",
    "Dodgers": "Los Angeles Dodgers",
    "Nationals": "Washington Nationals",
    "Mets": "New York Mets",
    "American": "American League All-Stars",
    "National": "National League All-Stars",
    "American": "AL All-Stars",
    "National": "NL All-Stars",
    "American League All-Stars": "American",
    "National League All-Stars": "National",
    "AL All-Stars": "American",
    "NL All-Stars": "National",
}

TEAM_ABBR_LN = {
    "Oakland Athletics": "OAK",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SD",
    "Seattle Mariners": "SEA",
    "San Francisco Giants": "SF",
    "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Minnesota Twins": "MIN",
    "Philadelphia Phillies": "PHI",
    "Atlanta Braves": "ATL",
    "Chicago White Sox": "CWS",
    "Miami Marlins": "MIA",
    "New York Yankees": "NYY",
    "Milwaukee Brewers": "MIL",
    "Los Angeles Angels": "LAA",
    "Arizona Diamondbacks": "AZ",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC",
    "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KC",
    "Los Angeles Dodgers": "LAD",
    "Washington Nationals": "WSH",
    "New York Mets": "NYM",
    "American League All-Stars": "AL",
    "National League All-Stars": "NL",
    "AL All-Stars": "AL",
    "NL All-Stars": "NL",
}
