# Customer Pricing Model

The initial prototype of the customer price sensitivity model was developed using scikit-learn and logistic regression, trained on a binary classification dataset to predict win/loss outcomes as a function of customer hourly rate, trade, and location. This model was a simple proof-of-concept built on highly generalized RFP data (often state-level contracts that don’t necessarily correlate to customer spend), but we are working to source the required data to track revenue realization on a store-by-store level for our next model.

The next iteration of the customer price sensitivity model will be a gradient boosted decision tree model from the XGBoost library in Python. Here is a quick sketch of the model’s blueprint as of today:

### Features (Not an Exhaustive List)
- Latitude
- Longitude
- Customer
- Customer Industry
- Customer Hourly Rate
- Service Trade
- Total Addressable Spend Per Store For That Trade
- Customer’s Total Revenue
- Store size (square feet)
- Local population
- State
- County
- CBSA

### Output (Target Variable)
- Gross Revenue Realized

### Granularity
- Per Year Per Store

The model will be trained on a dataset containing the features and outputs listed above, in order to learn to map the relationship between revenue realization and each feature. The result will be a regression model that can accurately predict revenue realization at the annualized store level as a function of customer hourly rate, service trade, customer industry, customer size, location, and other features.
