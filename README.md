# Pete Crow-Armstrong's 2026 Season: An Exploratory Analysis

**TL;DR:** I believe PCA is having one of the best individual seasons in Chicago Cubs history. Looking at his batting stats, it is fair to say that his increase in production is not a fluke. His batting average and HR slowly increased until it hit a spot during June where it skyrocketed. And it is not just his offense either. Defensively, his OAA and dWAR are so elite that his OAA ties a record for most in a single season by an outfielder. When comparing his stats to some of the greatest Chicago Cubs players, almost all of his stats keep up with the legends Sammy Sosa and Ryne Sandberg. He leads defensively in dWAR, defensive value, and WAR compared to them. He is a legitimate NL MVP candiate for the 2026 MLB season.

## Question

Is Pete Crow-Armstrong's 2026 season with the Chicago Cubs a genuine breakout, and how does
it compare to historic Cubs seasons (Sammy Sosa 1998, Ryne Sandberg 1984, Ernie Banks 1958-59)?

## Data

- MLB Statcast data pulled via [`pybaseball`](https://github.com/jldbc/pybaseball)
- Historical comparison seasons pulled via Baseball-Reference (through `pybaseball`)
- Advanced metrics (WAR, wOBA, wRC+) for PCA's 2026 season sourced manually from [FanGraphs](https://www.fangraphs.com), since their site blocks automated scraping

## Project structure

```
pca-project/
├── data/
│   ├── raw/          # raw pulls, untouched
│   └── processed/    # cleaned, game-level data
├── notebooks/
│   └── pca_season_analysis.ipynb   # main analysis notebook
├── scripts/
│   ├── 01_pull_data.py    # pulls raw data (run locally — needs network access)
│   └── 02_clean_data.py   # cleans + aggregates to game-level
└── README.md
```
## Notes

Initial stolen base tracking was miscounted due to how Statcast records baserunning events separately from batting events. This was caught by cross-checking against FanGraphs' season totals, and fixed by using the season-total figure instead of a per-game aggregation.

## How to reproduce

```bash
pip install pybaseball pandas matplotlib seaborn
cd scripts
python 01_pull_data.py
python 02_clean_data.py
cd ../notebooks
jupyter notebook pca_season_analysis.ipynb
```

## Key findings

- PCA's 2026 season posted 9.8 WAR, outproducing both Sammy Sosa's 1998 season (6.46 WAR) and Ryne Sandberg's 1984 season (8.52 WAR).
- Elite Defense: 26 Outs Above Average (OAA) and a 96% catch success rate in center field, tying the single season record for most OAA for an outfielder.
- Achieved a 30-30 season (41 HR, 36 SB) while his batting average settled down at around .280. He is now aiming for a 40-40 season in last couple weeks of the season.
  