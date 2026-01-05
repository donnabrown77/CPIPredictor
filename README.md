# CPIPredictor
Predicting Consumer Prices with Data

# Macro-Economic Inflation Forecasting Pipeline

## 📌 Project Overview
This project implements an end-to-end machine learning pipeline to forecast **US Consumer Price Index (CPI) Inflation** with a one-month horizon.

Unlike standard textbook examples that use static datasets and random train-test splits, this project utilizes **Walk-Forward Validation (Expanding Window)** to simulate real-world trading/forecasting scenarios. It fetches live economic data from the Federal Reserve (FRED) API, tests for statistical causality, and compares a baseline Linear Regression model against an XGBoost regressor.

## 🚀 Key Features
* **Live Data Ingestion:** Automated ETL pipeline using `pandas_datareader` to fetch real-time data from FRED.
* **Walk-Forward Validation:** Implements an "expanding window" backtest to retrain the model every month, strictly preventing look-ahead bias/data leakage.
* **Statistical Rigor:** Pre-screening of features using **Granger Causality Tests** to verify predictive power before modeling.
* **Ensemble Modeling:** Benchmarks a non-linear gradient boosting model (XGBoost) against a linear baseline.
* **Regime Detection:** Visualizes model performance during high-volatility periods (e.g., the 2020 Covid Shock).

## 📊 Data Sources
The model ingests 30+ years of monthly economic indicators from the [Federal Reserve Bank of St. Louis (FRED)](https://fred.stlouisfed.org/):

| Indicator | Ticker | Economic Rationale |
| :--- | :--- | :--- |
| **US CPI (Target)** | `CPIAUCSL` | The standard measure of inflation. |
| **Crude Oil Prices** | `DCOILWTICO` | Proxy for energy input costs and supply shocks. |
| **Fed Funds Rate** | `FEDFUNDS` | The primary tool for monetary policy transmission. |
| **M2 Money Supply** | `M2SL` | Measures liquidity in the economy (Monetarist theory). |
| **Unemployment Rate** | `UNRATE` | Phillips Curve relationship (wage-push inflation). |

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/donnabrown77/CPIPredictor.git](https://github.com/donnabrown77/CPIPredictor.git)
   cd CPIPredictor