import pandas as pd
import numpy as np
import joblib

# 1. Load trained model and scaler
model = joblib.load(r"C:\Users\holden.coffman\optimization_engine\Price Sensitivity Models\customer_price_sensitivity_model_20250420_003939.pkl")
scaler = joblib.load(r"C:\Users\holden.coffman\optimization_engine\Price Sensitivity Models\scaler_20250420_003939.pkl")

# 2. Define cost per hour
cost = 50

# 3. Define a function to suggest optimal rate for a given lat/lon
def suggest_optimal_rate_from_coords(lat, lon):
    # Create a range of rates to simulate
    rate_range = np.linspace(0, 1000, 2000)
    simulation_df = pd.DataFrame({
        'rate': rate_range,
        'latitude': [lat] * len(rate_range),
        'longitude': [lon] * len(rate_range)
    })

    # Create interaction terms
    simulation_df['rate_lat'] = simulation_df['rate'] * simulation_df['latitude']
    simulation_df['rate_lon'] = simulation_df['rate'] * simulation_df['longitude']
    simulation_df['rate_squared'] = simulation_df['rate'] ** 2

    # Scale
    simulation_scaled = scaler.transform(simulation_df)

    # Predict win probability
    simulation_df['win_probability'] = model.predict_proba(simulation_scaled)[:, 1]

    # Calculate expected profit
    simulation_df['expected_profit'] = simulation_df['win_probability'] * (simulation_df['rate'] - cost)

    # Find the optimal rate
    optimal_row = simulation_df.loc[simulation_df['expected_profit'].idxmax()]
    optimal_rate = optimal_row['rate']
    anticipated_win_rate = optimal_row['win_probability']
    target_margin = 1 - (cost / optimal_row['rate'])

    return optimal_rate, anticipated_win_rate, target_margin

# 4. Load your batch of locations
input_file_path = r"C:\Users\holden.coffman\optimization_engine\Rate Sheet Input File.csv"
locations_df = pd.read_csv(input_file_path, encoding='latin1')

# 5. Assume your CSV has columns 'latitude' and 'longitude'
#    Create new columns to store the results
locations_df['optimal_customer_rate'] = np.nan
locations_df['anticipated_win_rate'] = np.nan
locations_df['target_margin'] = np.nan
locations_df['anticipated_provider_rate'] = np.nan

# 6. Loop over each row and calculate optimal rate
for idx, row in locations_df.iterrows():
    lat = row['latitude']
    lon = row['longitude']

    if pd.notnull(lat) and pd.notnull(lon):
        optimal_rate, anticipated_win_rate, target_margin = suggest_optimal_rate_from_coords(lat, lon)
        locations_df.at[idx, 'optimal_customer_rate'] = optimal_rate
        locations_df.at[idx, 'anticipated_win_rate'] = anticipated_win_rate
        locations_df.at[idx, 'target_margin'] = target_margin
        locations_df.at[idx, 'anticipated_provider_rate'] = cost # <--- manually assigned fixed provider rate

# 7. Save the results to a new CSV
output_file_path = r"C:\Users\holden.coffman\optimization_engine\Optimized Handyman Rates.csv"
locations_df.to_csv(output_file_path, index=False)

print(f"✅ Done! Results saved to {output_file_path}")