import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Read NBA statistics from CSV
nba_stats_df = pd.read_csv('player_statistics_100.csv')

# Display the statistics
print("\nNBA Player Statistics:")
print("-" * 50)
for _, row in nba_stats_df.iterrows():
    metric = row['Metric']
    mean = row['Mean']
    variance = row['Variance']
    std = row['Std Dev']
    
    print(f"\n{metric}:")
    print(f"Mean: {mean:.2f}")
    print(f"Variance: {variance:.2f}")
    print(f"Standard Deviation: {std:.2f}")

# Convert to dictionary for easier access
nba_stats = {}
for _, row in nba_stats_df.iterrows():
    metric = row['Metric'].lower().split(' ')[0]  # 'Height (inches)' -> 'height'
    nba_stats[metric] = {
        'mean': row['Mean'],
        'variance': row['Variance'],
        'std': row['Std Dev']
    }


# US male statistics (2024 data)
us_male_stats = {
    'height': {
        'mean': 69.1,  # inches (5'9")
        'std': 2.9,
        'variance': 2.9**2
    },
    'weight': {
        'mean': 199.8,  # pounds
        'std': 40.8,
        'variance': 40.8**2
    }
}

# Display US male statistics
print("\nUS Male Average Statistics:")
print("-" * 50)
for metric, stats in us_male_stats.items():
    print(f"\n{metric.capitalize()} (inches if height, lbs if weight):")
    print(f"Mean: {stats['mean']:.2f}")
    print(f"Variance: {stats['variance']:.2f}")
    print(f"Standard Deviation: {stats['std']:.2f}")

# Compare NBA vs US Male averages
print("\nComparison (NBA vs US Male):")
print("-" * 50)
for metric in ['height', 'weight']:
    print(f"\n{metric.capitalize()}:")
    print(f"NBA Mean: {nba_stats[metric]['mean']:.2f} vs US Male Mean: {us_male_stats[metric]['mean']:.2f}")
    print(f"NBA Std Dev: {nba_stats[metric]['std']:.2f} vs US Male Std Dev: {us_male_stats[metric]['std']:.2f}")

def calculate_percentile(value, mean, std):
    """Calculate the percentile of a value in a normal distribution"""
    return norm.cdf((value - mean) / std) * 100

def find_equivalent_nba_value(percentile, mean, std):
    """Find the NBA measurement that corresponds to the same percentile"""
    return norm.ppf(percentile/100) * std + mean

# Get user input
print("\nEnter your measurements:")
height_ft = int(input("Height (feet): "))
height_in = int(input("Height (inches): "))
weight = float(input("Weight (lbs): "))

# Convert height to total inches
user_height = height_ft * 12 + height_in

# Calculate percentiles in US male population
height_percentile_us = calculate_percentile(user_height, us_male_stats['height']['mean'], 
                                          us_male_stats['height']['std'])
weight_percentile_us = calculate_percentile(weight, us_male_stats['weight']['mean'], 
                                          us_male_stats['weight']['std'])

# Find equivalent NBA measurements at same percentiles
equivalent_nba_height = find_equivalent_nba_value(height_percentile_us, 
                                                nba_stats['height']['mean'],
                                                nba_stats['height']['std'])
equivalent_nba_weight = find_equivalent_nba_value(weight_percentile_us,
                                                nba_stats['weight']['mean'],
                                                nba_stats['weight']['std'])

print("\nYour measurements compared to US males:")
print(f"Height: {user_height} inches ({height_ft}'{height_in}\") - {height_percentile_us:.1f}th percentile")
print(f"Weight: {weight} lbs - {weight_percentile_us:.1f}th percentile")

print("\nEquivalent NBA measurements (same percentile):")
print(f"Height: {equivalent_nba_height:.1f} inches ({int(equivalent_nba_height//12)}'{int(equivalent_nba_height%12)}\")")
print(f"Weight: {equivalent_nba_weight:.1f} lbs")

# Read measurements.csv to find closest NBA player
measurements_df = pd.read_csv('measurements_top100.csv', comment='#')

def convert_height_to_inches(height_str):
    feet, inches = map(int, height_str.split('-'))
    return feet * 12 + inches

measurements_df['height_inches'] = measurements_df['height'].apply(convert_height_to_inches)

## Estimation part
# Calculate standardized differences
measurements_df['height_diff_std'] = abs(
    (measurements_df['height_inches'] - equivalent_nba_height) / nba_stats['height']['std']
)
measurements_df['weight_diff_std'] = abs(
    (measurements_df['weight'].astype(float) - equivalent_nba_weight) / nba_stats['weight']['std']
)

# Calculate total difference using Euclidean distance of standardized differences
measurements_df['total_diff'] = np.sqrt(
    measurements_df['height_diff_std']**2 + 
    measurements_df['weight_diff_std']**2
)

closest_player = measurements_df.nsmallest(1, 'total_diff').iloc[0]

print(f"\nMost similar NBA player (relative to their peers):")
print(f"{closest_player['Player']}: {closest_player['height']}, {closest_player['weight']} lbs")