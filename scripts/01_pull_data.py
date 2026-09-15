"""
Step 1: Pull data for the PCA 2026 season analysis.

Run this on your own machine (not in a sandboxed environment) since it
needs to reach baseballsavant.mlb.com and baseball-reference.com.

Usage:
    pip install pybaseball pandas
    python 01_pull_data.py
"""

import pandas as pd
from pybaseball import statcast_batter, playerid_lookup, batting_stats_range

# ---------------------------------------------------------------------
# 1. Look up Pete Crow-Armstrong's MLBAM player ID
# ---------------------------------------------------------------------
lookup = playerid_lookup("crow-armstrong", "pete")
print(lookup)
PCA_ID = int(lookup.loc[0, "key_mlbam"])
print(f"PCA MLBAM id: {PCA_ID}")

# ---------------------------------------------------------------------
# 2. Pull pitch-by-pitch Statcast data for the 2026 season
#    (adjust the end date to "today" as the season progresses)
# ---------------------------------------------------------------------
SEASON_START = "2026-03-26"
SEASON_END = "2026-08-31"  # update this as more games are played

statcast_df = statcast_batter(SEASON_START, SEASON_END, PCA_ID)
statcast_df.to_csv("../data/raw/pca_statcast_2026.csv", index=False)
print(f"Saved statcast data: {statcast_df.shape}")

# ---------------------------------------------------------------------
# 3. Pull game-by-game batting log (easier for trend charts than
#    pitch-level data)
# ---------------------------------------------------------------------
# batting_stats_range pulls all players in a date range; we'll filter to PCA
game_log = batting_stats_range(SEASON_START, SEASON_END)
game_log.to_csv("../data/raw/all_batters_2026.csv", index=False)
print(f"Saved league-wide batting range data: {game_log.shape}")

# ---------------------------------------------------------------------
# 4. NOTE on historical comparison seasons (Sosa 1998, Sandberg 1984):
#    Statcast data only goes back to 2015, so for older seasons you'll
#    want pybaseball's `batting_stats_bref` or Baseball-Reference's
#    season pages instead. Example:
#
#    from pybaseball import batting_stats_bref
#    sosa_1998 = batting_stats_bref(1998)
#    sosa_1998.to_csv("../data/raw/nl_batting_1998.csv", index=False)
#
#    You'd then filter that dataframe down to Sosa's row for comparison
#    stats (not full game logs, since Statcast doesn't cover 1998).
# ---------------------------------------------------------------------

print("Done. Check data/raw/ for the CSVs.")
