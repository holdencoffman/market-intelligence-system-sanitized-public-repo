# 1. Import libraries
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split

# 2. Load your data
# Assuming you have a CSV with columns: 'rate', 'latitude', 'longitude', 'outcome'
df = pd.read_csv(r"C:\Users\holden.coffman\optimization_engine\Handyman Data for Python_Cleaned.csv")

# Drop blank rows
df = df.dropna(how='all')

# 3. Create interaction terms
df['rate_lat'] = df['rate'] * df['latitude']
df['rate_lon'] = df['rate'] * df['longitude']
df['rate_squared'] = df['rate'] ** 2

# 4. Select features and target
X = df[['rate', 'latitude', 'longitude', 'rate_lat', 'rate_lon', 'rate_squared']]
y = df['outcome']

# 5. Normalize (standardize) the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 7. Build and fit the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# 8. Predict probabilities
y_pred_probs = model.predict_proba(X_test)[:, 1]

# 9. Calculate average log-loss
avg_log_loss = log_loss(y_test, y_pred_probs)

print(f'Average Log-Loss: {avg_log_loss:.4f}')

import os
import shutil
import glob
import joblib
from datetime import datetime

# Define full save folder
save_folder = r"C:\Users\holden.coffman\optimization_engine\Price Sensitivity Models"

# Make sure the folder exists
os.makedirs(save_folder, exist_ok=True)

# Create a timestamp string
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Save the model with timestamp
model_filename = os.path.join(save_folder, f"customer_price_sensitivity_model_{timestamp}.pkl")
scaler_filename = os.path.join(save_folder, f"scaler_{timestamp}.pkl")

joblib.dump(model, model_filename)
joblib.dump(scaler, scaler_filename)

print(f"Model saved as: {model_filename}")
print(f"Scaler saved as: {scaler_filename}")

# Create a 'history' folder inside your save folder
history_folder = os.path.join(save_folder, 'History')
os.makedirs(history_folder, exist_ok=True)

# Find all model and scaler files
model_files = sorted(glob.glob(os.path.join(save_folder, "customer_price_sensitivity_model_*.pkl")), reverse=True)
scaler_files = sorted(glob.glob(os.path.join(save_folder, "scaler_*.pkl")), reverse=True)

# Move older models into history/
for old_file in model_files[5:]:
    shutil.move(old_file, history_folder)

for old_file in scaler_files[5:]:
    shutil.move(old_file, history_folder)
