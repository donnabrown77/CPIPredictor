# serve.py
from fastapi import FastAPI, HTTPException
from predict import predict_next_month, load_model
import uvicorn

app = FastAPI(title="Inflation Forecast API")

@app.on_event("startup")
def check_model():
    """Check if model exists on startup."""
    if not load_model():
        print("WARNING: Model artifact not found. Please run train.py.")

@app.get("/")
def home():
    return {"message": "Inflation Forecaster is running. Go to /predict to get a forecast."}

@app.get("/predict")
def predict():
    """
    Endpoint to trigger a fresh forecast based on latest FRED data.
    """
    try:
        result = predict_next_month()
        return {
            "status": "success",
            "data": result
        }
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

if __name__ == "__main__":
    # Run with: python serve.py
    uvicorn.run(app, host="0.0.0.0", port=8000)