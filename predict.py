# predict.py
import joblib
import pandas as pd
from utils import fetch_and_process_data

MODEL_PATH = "inflation_model.joblib"

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return None

def predict_next_month():
    """
    Fetches latest data, prepares the feature vector for 'Next Month',
    and runs the model.
    """
    # 1. Load Model
    artifact = load_model()
    if not artifact:
        raise RuntimeError("Model not found! Run train.py first.")
    
    model = artifact["model"]
    feature_names = artifact["features"]

    # 2. Get Latest Data
    # In a real system, you might pass specific inputs. 
    # Here, we re-fetch FRED data to get the very latest numbers.
    df = fetch_and_process_data()
    
    # 3. Prepare Input Vector
    # To predict month (t+1), we use the data from month (t)
    latest_data = df.iloc[[-1]][feature_names]
    latest_date = df.index[-1]

    # 4. Inference
    prediction = model.predict(latest_data)[0]
    
    return {
        "reference_date": str(latest_date.date()),
        "forecast_value": float(prediction),
        "forecast_label": f"{prediction:.2%}"
    }

if __name__ == "__main__":
    result = predict_next_month()
    print("Forecast Result:", result)