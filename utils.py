# utils.py
import pandas_datareader.data as web
import pandas as pd
from datetime import datetime

def fetch_and_process_data():
    """
    Fetches data from FRED and creates all lag features.
    Returns: A cleaned DataFrame ready for training or inference.
    """
    print("Fetching data from FRED...")
    start_date = datetime(1990, 1, 1)
    end_date = datetime.now()

    tickers = ['CPIAUCSL', 'DCOILWTICO', 'FEDFUNDS', 'M2SL', 'UNRATE']
    
    try:
        raw_data = web.DataReader(tickers, 'fred', start_date, end_date)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data: {e}")

    # Resample to Monthly Start
    df = raw_data.resample('MS').mean()
    df.columns = ['US_CPI', 'Oil_Price', 'Fed_Rate', 'Money_Supply', 'Unemployment']

    # 1. Calculate Rates of Change (Stationarity)
    df['Inflation_MoM'] = df['US_CPI'].pct_change()
    df['Oil_Pct_Change'] = df['Oil_Price'].pct_change()
    df['Money_Supply_Pct'] = df['Money_Supply'].pct_change()
    df['Fed_Rate_Diff'] = df['Fed_Rate'].diff()
    df['Unemployment_Diff'] = df['Unemployment'].diff()

    # 2. Generate Lag Features
    # We must use the EXACT same lags as the training script
    lags = [1, 3, 6, 12] 
    
    for lag in lags:
        df[f'Inflation_lag_{lag}'] = df['Inflation_MoM'].shift(lag)
        df[f'Oil_lag_{lag}'] = df['Oil_Pct_Change'].shift(lag)
        df[f'Fed_lag_{lag}'] = df['Fed_Rate_Diff'].shift(lag)
        df[f'Money_lag_{lag}'] = df['Money_Supply_Pct'].shift(lag)
        df[f'Unemp_lag_{lag}'] = df['Unemployment_Diff'].shift(lag)

    # Remove rows with NaN (due to lags or differencing)
    # For inference, we usually only care about the last row, 
    # but for consistency we drop NaNs.
    df_ready = df.dropna()
    
    return df_ready

def get_feature_columns(df):
    """Returns the list of feature column names used for the model."""
    return [col for col in df.columns if 'lag' in col]