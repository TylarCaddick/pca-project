"""
Step 2: Clean and prep the raw Statcast data into a game-level dataframe
with the rolling averages and split flags we'll need for analysis.

Run after 01_pull_data.py has produced data/raw/pca_statcast_2026.csv
"""

import pandas as pd

# ---------------------------------------------------------------------
# 1. Load raw pitch-level Statcast data
# ---------------------------------------------------------------------
df = pd.read_csv("../data/raw/pca_statcast_2026.csv")

df["game_date"] = pd.to_datetime(df["game_date"])
df = df.sort_values("game_date")

# ---------------------------------------------------------------------
# 2. Collapse pitch-level rows down to one row per plate appearance,
#    then aggregate to one row per game
# ---------------------------------------------------------------------
# Statcast has one row per pitch; a plate appearance ends on rows where
# `events` is not null (e.g. "single", "strikeout", "home_run", "walk")
pa_df = df[df["events"].notna()].copy()

# Map event outcomes to simple flags for aggregation
hit_events = {"single", "double", "triple", "home_run"}
pa_df["is_hit"] = pa_df["events"].isin(hit_events).astype(int)
pa_df["is_home_run"] = (pa_df["events"] == "home_run").astype(int)
pa_df["is_walk"] = (pa_df["events"] == "walk").astype(int)
pa_df["is_strikeout"] = (pa_df["events"] == "strikeout").astype(int)
pa_df["is_stolen_base"] = pa_df["events"].astype(str).str.contains(
    "stolen_base", na=False
).astype(int)
pa_df["at_bat"] = (~pa_df["events"].isin(
    ["walk", "hit_by_pitch", "sac_fly", "sac_bunt", "catcher_interf"]
)).astype(int)

# Handedness of the opposing pitcher, for splits later
pa_df["p_throws"] = pa_df["p_throws"]  # 'L' or 'R', already in Statcast data
pa_df["home_away"] = (pa_df["inning_topbot"] == "Bot").map(
    {True: "home", False: "away"}
)

# ---------------------------------------------------------------------
# 3. Aggregate to game level
# ---------------------------------------------------------------------
game_level = (
    pa_df.groupby("game_date")
    .agg(
        at_bats=("at_bat", "sum"),
        hits=("is_hit", "sum"),
        home_runs=("is_home_run", "sum"),
        walks=("is_walk", "sum"),
        strikeouts=("is_strikeout", "sum"),
        stolen_bases=("is_stolen_base", "sum"),
    )
    .reset_index()
)

game_level["batting_avg_game"] = (
    game_level["hits"] / game_level["at_bats"]
).round(3)

# ---------------------------------------------------------------------
# 4. Rolling averages and cumulative season totals
# ---------------------------------------------------------------------
game_level["cum_hits"] = game_level["hits"].cumsum()
game_level["cum_at_bats"] = game_level["at_bats"].cumsum()
game_level["cum_avg"] = (game_level["cum_hits"] / game_level["cum_at_bats"]).round(3)
game_level["cum_home_runs"] = game_level["home_runs"].cumsum()
game_level["cum_stolen_bases"] = game_level["stolen_bases"].cumsum()

game_level["rolling_avg_7g"] = (
    game_level["hits"].rolling(7).sum() / game_level["at_bats"].rolling(7).sum()
).round(3)
game_level["rolling_avg_30g"] = (
    game_level["hits"].rolling(30).sum() / game_level["at_bats"].rolling(30).sum()
).round(3)

game_level["month"] = game_level["game_date"].dt.month_name()

# ---------------------------------------------------------------------
# 5. Save cleaned game-level data
# ---------------------------------------------------------------------
game_level.to_csv("../data/processed/pca_game_level_2026.csv", index=False)
print(f"Saved cleaned game-level data: {game_level.shape}")
print(game_level.head(10))

# Also save the splits-ready plate appearance data (for step 4 analysis)
pa_df.to_csv("../data/processed/pca_plate_appearances_2026.csv", index=False)
print(f"Saved plate appearance-level data: {pa_df.shape}")
