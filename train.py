# train.py
import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from utils import fetch_and_process_data, get_feature_columns

MODEL_PATH = "inflation_model.joblib"

def train():
    # 1. Get Data
    df = fetch_and_process_data()
    features = get_feature_columns(df)
    target = 'Inflation_MoM'

    X = df[features]
    y = df[target]

    print(f"Training on {len(df)} months of data...")

    # 2. Train Models
    # In a real app, you might choose just the "best" model from your experiments.
    # Here we will train a Random Forest as the production model.
    model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X, y)

    # 3. Save Artifacts
    # We save a dictionary containing the model AND the expected feature names
    # This ensures safety during inference.
    artifact = {
        "model": model,
        "features": features,
        "last_train_date": df.index.max()
    }

    joblib.dump(artifact, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()