# 1. Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 2. Load Your Data
# (Update the path to your file)
input_file = r"C:\Users\holden.coffman\optimization_engine\Handyman Data for Python_Cleaned.csv"
data = pd.read_csv(input_file)

# 3. Set up a folder to save plots
output_folder = r"C:\Users\holden.coffman\optimization_engine\Profit Optimization Model\Data Sanity Checks"
os.makedirs(output_folder, exist_ok=True)

# 4. Basic Data Overview
print("\n🔎 Basic Data Overview:")
print(data.head())

# 5. Win/Loss Balance Check
print("\n📊 Win/Loss Balance (%):")
print(data['outcome'].value_counts(normalize=True) * 100)

# Plot Win/Loss Balance
plt.figure(figsize=(6,4))
sns.countplot(x='outcome', data=data)
plt.title('Win vs Loss Counts')
plt.xlabel('Outcome (1 = Win, 0 = Loss)')
plt.ylabel('Count')
plt.xticks([0,1], ['Loss', 'Win'])
plt.savefig(os.path.join(output_folder, 'win_loss_counts.png'))
plt.close()

# 6. Price Spread Check
print("\n📈 Rate Summary Statistics:")
print(data['rate'].describe())

# Plot Rate Distribution
plt.figure(figsize=(8,4))
sns.histplot(data['rate'], bins=30, kde=True)
plt.title('Distribution of Rates Offered')
plt.xlabel('Rate ($)')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_folder, 'rate_distribution.png'))
plt.close()

# 7. Price vs Win Rate Relationship
print("\n📈 Win Rate by Price Range:")
data['price_bin'] = pd.cut(data['rate'], bins=10)
win_rate_by_price = data.groupby('price_bin')['outcome'].mean()
print(win_rate_by_price)

# Plot Win Rate by Price
plt.figure(figsize=(8,5))
win_rate_by_price.plot(kind='line', marker='o')
plt.title('Win Rate vs Rate Bins')
plt.xlabel('Rate Range')
plt.ylabel('Win Rate')
plt.grid(True)
plt.savefig(os.path.join(output_folder, 'win_rate_vs_price.png'))
plt.close()

# 8. Latitude/Longitude Coverage Check
print("\n🗺️ Latitude and Longitude Spread:")
print(f"Latitude: {data['latitude'].min():.2f} to {data['latitude'].max():.2f}")
print(f"Longitude: {data['longitude'].min():.2f} to {data['longitude'].max():.2f}")

# Scatter plot of locations
plt.figure(figsize=(8,6))
sns.scatterplot(x='longitude', y='latitude', data=data, alpha=0.3)
plt.title('Geographic Spread of Bids')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig(os.path.join(output_folder, 'geographic_spread.png'))
plt.close()

# 9. Duplicate Rows Check
print("\n📋 Duplicate Rows Check:")
duplicate_count = data.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_count}")

# Done!
print(f"\n✅ All plots saved to: {output_folder}")
