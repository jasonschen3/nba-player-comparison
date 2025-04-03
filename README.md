# NBA Player Comparison Tool

Compare your physical measurements to NBA players and see where you stand amongst both NBA athletes and average US males.

## Description

This tool helps you:

- Compare your height and weight to current NBA players
- See how you measure up against average US male statistics
- Find NBA players with similar physical builds relative to their peer groups

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/nba-player-comparison.git
cd nba-player-comparison
```

2. Install required packages:

```bash
pip install pandas numpy scipy matplotlib
```

## Usage

Run the comparison tool:

```bash
python3 compare.py
```

You'll be prompted to enter:

- Your height (feet and inches)
- Your weight (pounds)

The program will show:

- Your percentile among US males
- Equivalent NBA measurements at your percentile
- NBA players with similar builds relative to their peers

## Data Sources

- NBA player measurements: basketball-reference.com (2023-24 season)
- US male average statistics: CDC data (2024)

## Files

- `compare.py`: Main comparison script
- `measurements_top100.csv`: Current NBA player measurements
- `player_statistics.csv`: Statistical analysis of NBA measurements
