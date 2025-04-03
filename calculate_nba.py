import pandas as pd
import numpy as np

# Dataframe
df = pd.read_csv("measurements_top100.csv")

# Convert height from feet-inches to total inches
def convert_height_to_inches(height_str):
    feet, inches = map(int, height_str.split('-'))
    return feet * 12 + inches

# print(df)
# Convert height column
df['height_inches'] = df['height'].apply(convert_height_to_inches)

# # Calculate statistics
height_stats = {
    'mean': np.mean(df['height_inches']),
    'variance': np.var(df['height_inches']),
    'std': np.std(df['height_inches'])
}

weight_stats = {
    'mean': np.mean(df['weight']),
    'variance': np.var(df['weight']),
    'std': np.std(df['weight'])
}

# Print results
print("\nNBA Player Height Statistics:")
print(f"Mean height: {height_stats['mean']:.2f} inches ({height_stats['mean']/12:.1f} feet)")
print(f"Height variance: {height_stats['variance']:.2f} sq inches")
print(f"Height standard deviation: {height_stats['std']:.2f} inches")

print("\nNBA Player Weight Statistics:")
print(f"Mean weight: {weight_stats['mean']:.2f} lbs")
print(f"Weight variance: {weight_stats['variance']:.2f} sq lbs")
print(f"Weight standard deviation: {weight_stats['std']:.2f} lbs")

stats_df = pd.DataFrame({
    'Metric': ['Height (inches)', 'Weight (lbs)'],
    'Mean': [height_stats['mean'], weight_stats['mean']],
    'Variance': [height_stats['variance'], weight_stats['variance']],
    'Std Dev': [height_stats['std'], weight_stats['std']]
})

stats_df.to_csv('player_statistics_100.csv', index=False)
print("\nStatistics saved to player_statistics_100.csv")
