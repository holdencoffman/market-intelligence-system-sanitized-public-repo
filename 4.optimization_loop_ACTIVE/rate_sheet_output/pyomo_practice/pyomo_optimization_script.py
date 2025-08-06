import pandas as pd
import numpy as np
import joblib
from pyomo.environ import (ConcreteModel, Var, Param, Objective, Expression, SolverFactory, maximize, exp, value)

# 1. Load trained model and scaler
model = joblib.load(r"C:\Users\holden.coffman\Documents\GitHub\market-intelligence-system-public-repo\1.customer_models\V0_logistic_model\trained_models\customer_price_sensitivity_model_20250420_003939.pkl")
scaler = joblib.load(r"C:\Users\holden.coffman\Documents\GitHub\market-intelligence-system-public-repo\1.customer_models\V0_logistic_model\trained_models\scaler_20250420_003939.pkl")

# 2. Pull fixed pieces out of the sklearn objects so Pyomo can use them

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