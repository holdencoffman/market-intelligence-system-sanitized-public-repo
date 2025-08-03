import pandas as pd
import numpy as np
import joblib
from pyomo.environ import (ConcreteModel, Var, Param, Objective, Expression, SolverFactory, maximize, exp, value)

# 1. Load trained model and scaler
model = joblib.load(r"C:\Users\holden.coffman\Documents\GitHub\market-intelligence-system-public-repo\1.customer_models\V0_logistic_model\trained_models\customer_price_sensitivity_model_20250420_003939.pkl")
scaler = joblib.load(r"C:\Users\holden.coffman\Documents\GitHub\market-intelligence-system-public-repo\1.customer_models\V0_logistic_model\trained_models\scaler_20250420_003939.pkl")

# 2. Pul fixed pieces out of the sklearn objects so Pyomo can use them

feature_order = [
    "rate",
    "latitude",
    "longitude",
    "rate_lat",
    "rate_lon",
    "rate_squared",
]
coef = dict(zip(feature_order, model.coef_.flatten()))
intercept = float(model.intercept_[0])

µ = dict(zip(feature_order, scaler.mean_))     # means
σ = dict(zip(feature_order, scaler.scale_))    # std-devs

# 3. Pyomo optimization for a single (lat, lon)

def optimize_rate(lat: float, lon: float, cost: float = 50, lower: float = 0.0, upper: float = 1000.0):
    m = ConcreteModel()

    # -- decision variable --
    m.rate = Var(bounds=(lower, upper))

    # -- parameters (fixed for this location) --
    m.lat = Param(initialize=lat)
    m.lon = Param(initialize=lon)
    m.cost = Param (initialize=cost)

    # -- helper expressions: scaled features --
    def _z_expr(m):
        # original (unscaled) features
        r = m.rate
        r_lat = r * m.lat
        r_lon = r * m.lon
        r_sq = r**2

        # build linear term:
        linear = (
            coef["rate"]        * (r      - μ["rate"])        / σ["rate"]        +
            coef["latitude"]    * (m.lat  - μ["latitude"])    / σ["latitude"]    +
            coef["longitude"]   * (m.lon  - μ["longitude"])   / σ["longitude"]   +
            coef["rate_lat"]    * (r_lat  - μ["rate_lat"])    / σ["rate_lat"]    +
            coef["rate_lon"]    * (r_lon  - μ["rate_lon"])    / σ["rate_lon"]    +
            coef["rate_squared"]* (r_sq   - μ["rate_squared"])/ σ["rate_squared"]
        )
        return intercept + linear
    m.z = Expression(rule=_z_expr)

    # logistic win-probability
    m.win_prob = Expression(rule=lambda m: 1 / (1 + exp(-m.z)))

    # -- objective: maximize expected profit --
    m.obj = Objective(
        expr = m.win_prob * (m.rate - m.cost),
        sense = maximize
    )

    # -- solve --
    solver = SolverFactory("ipopt")
    # speed tweaks
    solver.options.update({"tol": 1e-8, "print_level": 0})
    solver.solve(m, tee=False)

    # -- results --
    opt_rate = value(m.rate)
    win_prob = value(m.win_prob)
    tgt_margin = 1 - (cost/opt_rate) if opt_rate else np.nan
    return opt_rate, win_prob, tgt_margin

# 4. Batch process the csv county rate card

input_file = (r"C:\Users\holden.coffman\Documents\GitHub\market-intelligence-system-public-repo\4.optimization_loop\rate_sheet_output\Rate Sheet Input File.csv")
output_file = (r"C:\Users\holden.coffman\Documents\GitHub\market-intelligence-system-public-repo\4.optimization_loop\rate_sheet_output\pyomo_optimized_rate_card.csv")

df = pd.read_csv(input_file, encoding="latin1")

df["optimal_customer_rate"] = np.nan
df["anticipated_win_rate"] = np.nan
df["target_margin"] = np.nan
df["anticipated_provider_rate"] = 50 # fixed cost I set earlier

for idx, row in df.iterrows():
    lat, lon, = row["latitude"], row["longitude"]
    if pd.notnull(lat) and pd.notnull(lon):
        rate, win, margin = optimize_rate(lat, lon)
        df.loc[idx, ["optimal_customer_rate", "anticipated_win_rate", "target_margin"]] = [rate, win, margin]

df.to_csv(output_file, index=False)
print(f"☑️ Done! Results saved to {output_file}:")


























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
input_file_path = r"C:\Users\holden.coffman\Divisions, Inc\DMG RFP Working Site - Documents\Analysis, Data, Levers, Soft Savings\Adhoc\Holden\Python Scripts\Profit Model Scripts\Rate Sheet Input File.csv"
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
output_file_path = r"C:\Users\holden.coffman\Divisions, Inc\DMG RFP Working Site - Documents\Analysis, Data, Levers, Soft Savings\Adhoc\Holden\Python Scripts\Profit Model Scripts\Optimized Handyman Rates.csv"
locations_df.to_csv(output_file_path, index=False)

print(f"✅ Done! Results saved to {output_file_path}")