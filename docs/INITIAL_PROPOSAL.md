# Multi-Modal AI Trading & Prediction Engine for SGX Blue Chips

## 1. Project Scope & Assumptions

* **Primary Objective:** A daily batch prediction and decision-support platform designed for SGX blue-chip equities (pilot watchlist: **DBS, Singtel, OCBC, SIA**).
* **Execution Frequency:** Optimized for end-of-day / pre-market batch processing, **not** intraday or high-frequency trading (HFT).
* **Data Environment:** Built using publicly or commercially accessible APIs and point-in-time open-source pipelines.
* **Predictive Scope:** The system estimates directional probabilities, expected price target ranges, and risk bounds. It is designed to generate statistical edge and decision support, not guarantee future returns.

---

## 2. Executive Summary & System Objectives

This proposal outlines the technical architecture for an institution-inspired, **daily batch execution prediction engine**. The framework captures a broad range of widely used quantitative factor categories across company fundamentals, macroeconomics, technicals, market microstructure, and sentiment.

The engine delivers a **hybrid target output** across three distinct horizons:

1. **Short-Term (1–3 Days):** Tactical entry/exit timing and event-driven reactions.
2. **Mid-Term (2–4 Weeks):** Technical trend continuation and sector rotation tracking.
3. **Long-Term (3 Months):** Fundamental valuation adjustments and macro regime drifts.

### Target Specifications:

* **Directional Probability (Classification):** Model-assigned confidence ($0.0$ to $1.0$) of upward vs. downward movement.
* **Price Bounds & Expected Returns (Regression):** Point estimates of price targets alongside dynamic volatility boundaries.

By leveraging mature open-source frameworks (**`pytorch-forecasting`**, **`FinNLP`**, **`pandas-ta`**), the system maintains a lightweight operational footprint capable of generating daily predictions in **under 5 minutes** on a standard home PC.

---

## 3. High-Level System Architecture

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                   STAGE 1: ASYNCHRONOUS DATA INGESTION                      │
  │                                                                             │
  │  [ Daily Feeds ]       [ Quarterly / Financials ]    [ Event-Driven / News ]│
  │  Prices, Macro, FX,    EPS, Debt/Equity, Ratios,     FinNLP Downloader,     │
  │  Yields, Short Vol     Point-In-Time Filings         SGX Announcements      │
  └────────┬─────────────────────────┬─────────────────────────────┬────────────┘
           │                         │                             │
           ▼                         ▼                             ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │             STAGE 2: POINT-IN-TIME (PIT) FEATURE STORE & ETL                │
  │                                                                             │
  │  • Strict Timestamp Alignment: Zero Look-Ahead Bias                         │
  │  • Technical Generation: pandas-ta / TA-Lib (130+ candidate indicators)     │
  │  • Natural Language Processing: FinBERT Sentiment Scoring (-1.0 to +1.0)    │
  │  • Dynamic Feature Selection: Collinearity Filter + Out-of-Sample SHAP Rank │
  └──────────────────────────────────┬──────────────────────────────────────────┘
                                     │
                                     ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                  STAGE 3: TEMPORAL FUSION TRANSFORMER (TFT)                 │
  │                     (via pytorch-forecasting framework)                     │
  │                                                                             │
  │   [ Static Encoders ]    [ Time-Varying Encoders ]    [ Known Future Head ] │
  │   Stock_ID, Sector       Prices, Macro, Sentiment,    Earnings Dates,       │
  │                          Regime Tag, Technicals       Ex-Dividend Dates     │
  │                                     │                                       │
  │                                     ▼                                       │
  │                      [ Variable Selection Gating ]                          │
  │                   Dynamically re-weights features daily                     │
  └──────────────────────────────────┬──────────────────────────────────────────┘
                                     │
                                     ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                 STAGE 4: EVALUATION & REPORT CARD MODULE                    │
  │                                                                             │
  │   • Directional Precision & Win Rate % (1-3d, 2-4w, 3mo)                    │
  │   • Mean Absolute Error (MAE) on Price Target Bounds                        │
  │   • Strategy Risk Metrics: Maximum Drawdown, Sharpe/Sortino, Profit Factor  │
  └─────────────────────────────────────────────────────────────────────────────┘

```

---

## 4. Comprehensive Feature Matrix (All 6 Sectors)

Data is ingested into a **Point-In-Time (PIT) Asynchronous Feature Store** using strict timestamp locks to ensure no data is leaked prior to its official public availability.

| Feature Category | Features Ingested | Processing & Open-Source Tools |
| --- | --- | --- |
| **1. Company Fundamentals** | Quarterly EPS, Debt/Equity, Quick Ratio, P/E, Forward P/E, P/B, Dividend Yield, Share Buybacks.<br>

<br>**Known Future Events:** Ex-Dividend Dates, **Earnings Release Dates**. | Ingested via `yfinance` / Finnhub. Earnings and ex-dividend dates feed into TFT's **Known Future Encoder**. |
| **2. Sector Dynamics** | Peer Earnings Contagion (DBS $\leftrightarrow$ OCBC $\leftrightarrow$ UOB), Commodity Mappings (Jet Fuel $\rightarrow$ SIA, Yield Spreads $\rightarrow$ Banks). Categorical Stock Embeddings replace static industry life-cycle metrics. | Mapped dynamically in ETL based on asset type. |
| **3. Macro & Cross-Asset** | Federal Reserve Rates, SORA (MAS API), US 10Y Yield, DXY Index, Brent Crude, **Gold**, **Copper Futures**, **VIX Index**, **USD/SGD**, **USD/JPY**, **Nikkei 225**, **Hang Seng**, **Baltic Dry Index (BDI)**, SG/US CPI & PMI. | Extracted via FRED API, Yahoo Finance, and MAS Open APIs. Forward-filled for non-trading days. |
| **4. Technical Signals** | Trend (ADX, Moving Averages), Momentum (RSI), Volatility (ATR), Volume (OBV), Levels (Distance to 52-Week High/Low, Support/Resistance). | Computed automatically via **`pandas-ta`** / **`TA-Lib`**. Passed through a dynamic SHAP selection filter. |
| **5. Market Microstructure** | Daily Short Volume %, Free Float %, VWAP Deviation %, Daily Bid-Ask Spread %, STI/MSCI Index Rebalance Dates. | Rebalance dates feed into TFT's **Known Future Encoder**. Microstructure metrics derived from daily SGX summary data. |
| **6. Sentiment & Regime** | Continuous Sentiment Polarity Scores (-1.0 to +1.0).<br>

<br>**Market Regime Indicator:** Categorical tag (`0: Bull-Low Vol`, `1: Sideways-Med Vol`, `2: Bear-High Vol`) derived strictly from past data. | Extracted via **`FinNLP`** + **FinBERT** from Yahoo News, Reuters, SGX Announcements, and Reddit `r/singaporefi`. |

---

## 5. Modeling Backbone & Retraining Pipeline

### Temporal Fusion Transformer (TFT) Setup

The engine uses `pytorch-forecasting` to implement TFT:

* **Variable Selection Networks:** Automatically suppress noisy indicators on quiet days while amplifying macro signals during central bank interest rate decisions or earnings announcements.
* **Multi-Horizon Heads:** Simultaneously forecasts outcomes for 1–3 days, 2–4 weeks, and 3 months in a single forward pass.

### Configurable Retraining & Governance Loop

Model retraining is **configurable** (Weekly by default; Monthly or Event-Triggered upon structural model updates) using a 4-step feature governance workflow:

```
  Candidate Features (130+ pandas-ta indicators + Macro + Sentiment)
                                  │
                                  ▼
   [ Step 1: Collinearity Filter ] ──► Drops features with correlation |r| > 0.85
                                  │
                                  ▼
   [ Step 2: SHAP Importance ] ───► Ranks top 20–25 predictive features on Training Set Only
                                  │
                                  ▼
   [ Step 3: Feature Governance ] ──► Verifies Availability, Timeliness, and Stability
                                  │
                                  ▼
   [ Step 4: TFT Model Re-fit ] ───► Trains PyTorch Transformer on pruned feature matrix

```

---

## 6. Daily Execution Workflow (Pre-Market 8:30 AM SGT)

Every morning prior to the SGX 9:00 AM SGT opening bell:

1. **8:00 AM SGT — Automated Ingestion:** Fetch overnight US/Asian closes (S&P 500, Nikkei, Hang Seng), FX rates, news headlines via `FinNLP`, and SGX corporate announcements.
2. **8:15 AM SGT — Feature Matrix Assembly:** Append new rows to the PIT database and compute rolling technicals via `pandas-ta`.
3. **8:25 AM SGT — Inference Pass:** Execute trained TFT model checkpoint. Running inference on 5–10 stocks takes **$< 5$ seconds** on a consumer GPU/CPU.
4. **8:30 AM SGT — Output Delivery:** Generate daily dashboard with direction probabilities, price targets, and volatility boundaries.

---

## 7. Performance Evaluation & Strategy Risk Metrics

The backtesting and evaluation module generates a comprehensive report card covering both statistical model precision and portfolio risk management:

* **Directional Win Rate (%):** Accuracy of directional calls across the 1–3d, 2–4w, and 3mo horizons.
* **Mean Absolute Error (MAE):** Deviation between predicted price target bounds and actual closing prices.
* **Maximum Drawdown (Max DD):** Peak-to-trough decline of simulated portfolio equity curves.
* **Sharpe & Sortino Ratios:** Risk-adjusted return performance per unit of total and downside volatility.
* **Profit Factor:** Gross profits divided by gross losses across backtested signal executions.

---

## 8. Implementation Roadmap

### Phase 1: Environment & Pipeline Infrastructure (Weeks 1–2)

* Install core dependencies (`pytorch-forecasting`, `FinNLP`, `pandas-ta`, `TA-Lib`, `DuckDB`/`PostgreSQL`).
* Build Point-In-Time (PIT) data ingestion scripts for price history, FRED macro metrics, MAS SORA rates, and news sentiment feeds.

### Phase 2: Feature Engineering & TFT Integration (Weeks 3–4)

* Build the automated `pandas-ta` indicator generator and training-set SHAP feature selection module.
* Configure the TFT architecture in PyTorch Lightning, integrating static inputs, time-varying past inputs, and known future event encoders (earnings & ex-dividend dates).

### Phase 3: Backtesting & Strategy Evaluation (Weeks 5–6)

* Conduct out-of-sample historical backtesting across historical market regimes (bull, bear, sideways).
* Calculate directional accuracy, price MAE, Maximum Drawdown, Sharpe Ratio, and Profit Factor against the Straits Times Index (STI) benchmark.
* Deploy the daily 8:30 AM automated execution pipeline.