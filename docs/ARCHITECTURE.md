# Sensilnet ATPE — Master Technical Blueprint & Architecture Specification

*Status: Approved by Cola technical review. All 10 audit findings verified against text and dispositioned. Ready for Phase 1 execution.*

---

## Document Governance (added 2026-07-24, TEAM_STRUCTURE.md v3.0)

This document has **Protected Sections** and **Implementation Notes** sections with different edit authority. See `TEAM_STRUCTURE.md` §5 for the full rule. Summary:

| Section Below | Classification | Edit Authority |
| :--- | :--- | :--- |
| §1 Executive System Overview | Protected (Vision) | Cola — requires approved ADP to change |
| §2 Mathematical Framework & PIT Compliance | Protected (Data Contracts) | Cola — requires approved ADP to change |
| §3 Storage Architecture & DuckDB Schemas | Protected (Data Contracts) | Cola — requires approved ADP to change |
| §4 Subsystem Deep-Dive | Protected (Component Responsibilities) | Cola — requires approved ADP to change |
| §5 Technical Roadmap & Phase Breakdown | Shared (Module Layout / planning) | Beer may propose directly; Cola notified |
| §6 Disposition Matrix for Audit Findings | Historical record | Append-only — do not edit past entries, add new rows for new findings |
| §7 Handoff Contract | Implementation Notes | Beer — freely editable, reflects current operational process |

Any diff touching a Protected Section must be accompanied by a linked, approved ADP in `docs/decision_log/` or it should be treated as a gatekeeper violation per `TEAM_STRUCTURE.md` §8.4.

---

## 1. Executive System Overview

Sensilnet ATPE (Automated Trading & Prediction Engine) is a multi-modal quantitative prediction and execution framework engineered specifically for SGX (Singapore Exchange) Blue Chip equities.

### Pilot Universe

The pilot universe comprises five core STI constituents:

- DBS Group Holdings (D05.SI)
- OCBC Bank (O39.SI)
- UOB Ltd (U11.SI)
- Singtel (Z74.SI)
- Singapore Airlines (C6L.SI)

**Note on Universe Selection:** The inclusion of UOB alongside DBS and OCBC is required for peer-bank contagion and relative-value cross-sectional features. SIA provides macro, transport, and jet-fuel sensitivity.

The primary objective of the engine is to generate daily Point-In-Time (PIT) compliant probabilistic return and directional forecasts using a multi-task Temporal Fusion Transformer (TFT) architecture. Model evaluation is conducted via out-of-sample event-driven backtesting incorporating SGX-specific brokerage commissions, clearing fees, access fees, and market-impact slippage.

```
               +-------------------------------------------------+
               |          SGX Market & Macro Data Ingestion      |
               |    (yfinance / EOD Feeds / Corporate Actions)   |
               +-----------------------+-------------------------+
                                       |
                                       v
               +-------------------------------------------------+
               |       DuckDB Point-In-Time (PIT) Storage        |
               |  (Raw Prices + Unadjusted Actions + ASOF Join)  |
               +-----------------------+-------------------------+
                                       |
                                       v
               +-------------------------------------------------+
               |        Feature Engineering & NLP Pipeline       |
               |  (pandas-ta + FinBERT Sentiment + SHAP Pruning) |
               +-----------------------+-------------------------+
                                       |
                                       v
               +-------------------------------------------------+
               |   PyTorch Lightning Multi-Task TFT Predictor    |
               |  (Quantile Regression + Directional Probability) |
               +-----------------------+-------------------------+
                                       |
                                       v
               +-------------------------------------------------+
               |          Execution & Backtesting Engine         |
               |   (Cost-adjusted metrics, Sharpe, STI Bench)    |
               +-------------------------------------------------+
```

---

## 2. Mathematical Framework & PIT Compliance

### 2.1 Point-In-Time (PIT) Filtration Guarantee & Adjustment Engine

To eliminate lookahead bias during feature construction and backtesting, all temporal operations adhere strictly to the information filtration $\mathcal{F}_t$ available at or before cutoff timestamp $t$:

$$\mathcal{F}_t = \sigma\left(\{X_{i,s}, \, A_{i,s} \mid s \le t, \, i \in \mathcal{U}\}\right)$$

Where $X_{i,s}$ represents raw observable market attributes and $A_{i,s}$ represents corporate actions (dividends and stock splits) announced and effective on or before timestamp $s$ for asset $i$ in universe $\mathcal{U}$.

**PIT Corporate Action Adjustment Factor**

To prevent retroactive price rewrites (a primary cause of PIT leakage in third-party feeds), raw market prices $P_{i,s}^{\text{raw}}$ are stored unadjusted. Adjusted historical price $P_{i,s \mid t}^{\text{adj}}$ for date $s \le t$ as known at decision cutoff $t$ is calculated dynamically:

$$P_{i,s \mid t}^{\text{adj}} = P_{i,s}^{\text{raw}} \times \prod_{\tau = s+1}^{t} f_{i, \tau \mid t}$$

Where the adjustment factor $f_{i, \tau \mid t}$ for event date $\tau$ known at cutoff $t$ is:

$$f_{i, \tau \mid t} = \begin{cases} \frac{1}{S_{i,\tau}} & \text{if split event at } \tau \le t \\ 1 - \frac{D_{i,\tau}}{P_{i,\tau-1}^{\text{raw}}} & \text{if ex-dividend event at } \tau \le t \\ 1 & \text{otherwise} \end{cases}$$

Here $S_{i,\tau}$ is the split ratio and $D_{i,\tau}$ is the dividend amount per share known at time $t$.

### 2.2 Asset Return & Multi-Horizon Target Formulations

The engine forecasts targets across a complete set of prediction horizons $\mathcal{H} = \{1, 3, 5, 10, 20, 60\}$ trading days, spanning short-term (1–5 days), medium-term (2–4 weeks), and long-term (3 months) windows.

Simple daily return $R_{i,t}$ and multi-horizon target return $Y_{i,t}^{(h)}$ for horizon $h \in \mathcal{H}$:

$$R_{i,t} = \frac{P_{i,t \mid t}^{\text{adj}} - P_{i,t-1 \mid t}^{\text{adj}}}{P_{i,t-1 \mid t}^{\text{adj}}}$$

$$Y_{i,t}^{(h)} = \frac{P_{i,t+h \mid t+h}^{\text{adj}} - P_{i,t \mid t}^{\text{adj}}}{P_{i,t \mid t}^{\text{adj}}}$$

Directional classification target $Y_{\text{dir}, i, t}^{(h)} \in \{0, 1\}$:

$$Y_{\text{dir}, i, t}^{(h)} = \mathbb{I}\left(Y_{i,t}^{(h)} > 0\right)$$

Where $\mathbb{I}(\cdot)$ is the indicator function. Note that feature construction uses $P_{i,t \mid t}^{\text{adj}}$ (knowable at cutoff $t$), while label generation uses $P_{i,t+h \mid t+h}^{\text{adj}}$ (realized forward price), strictly separating feature information from target realizations.

### 2.3 Multi-Task TFT Hybrid Loss Formulation

The Temporal Fusion Transformer optimizes a joint loss function combining multi-quantile regression and directional binary cross-entropy across all prediction horizons $h \in \mathcal{H}$.

**Quantile Regression Loss (Pinball Loss)**

For forecast quantile $q \in \mathcal{Q} = \{0.10, 0.50, 0.90\}$ and predicted value $\hat{y}_{q}^{(h)}$:

$$\mathcal{L}_{q}\left(y, \hat{y}_{q}^{(h)}\right) = \max\left(q\left(y - \hat{y}_{q}^{(h)}\right), \, (1 - q)\left(\hat{y}_{q}^{(h)} - y\right)\right)$$

**Directional Classification Loss**

For predicted upward probability $\hat{p}^{(h)} \in [0, 1]$ output by the classification head:

$$\mathcal{L}_{\text{dir}}\left(y_{\text{dir}}, \hat{p}^{(h)}\right) = - \left[ y_{\text{dir}} \ln\left(\hat{p}^{(h)}\right) + (1 - y_{\text{dir}}) \ln\left(1 - \hat{p}^{(h)}\right) \right]$$

**Multi-Task Composite Objective Function**

$$\mathcal{L}_{\text{total}} = \sum_{h \in \mathcal{H}} \left( \sum_{q \in \mathcal{Q}} \mathcal{L}_{q}\left(Y^{(h)}, \hat{Y}_{q}^{(h)}\right) + \lambda \, \mathcal{L}_{\text{dir}}\left(Y_{\text{dir}}^{(h)}, \hat{p}^{(h)}\right) \right)$$

Where $\lambda > 0$ is a loss-balancing hyperparameter (default $\lambda = 0.5$).

### 2.4 Risk & Portfolio Execution Metrics

Annualized Sharpe Ratio $\text{SR}$ relative to 3-month SORA benchmark rate $R_f$:

$$\text{SR} = \frac{\mathbb{E}[R_p - R_f]}{\sigma_p} \times \sqrt{252}$$

Maximum Drawdown $\text{MDD}$ over portfolio equity trajectory $E_t$:

$$\text{MDD} = \max_{t \ge s} \left( \frac{\max_{\tau \le t} E_\tau - E_t}{\max_{\tau \le t} E_\tau} \right)$$

---

## 3. Storage Architecture & DuckDB Schemas

All structured data and engineered feature matrices are stored in DuckDB (`data/sensilnet.duckdb`).

### 3.1 Raw Unadjusted SGX Price Table (`raw_sgx_daily`)

```sql
CREATE TABLE IF NOT EXISTS raw_sgx_daily (
    symbol VARCHAR NOT NULL,
    trade_date DATE NOT NULL,
    raw_open DOUBLE NOT NULL,
    raw_high DOUBLE NOT NULL,
    raw_low DOUBLE NOT NULL,
    raw_close DOUBLE NOT NULL,
    volume BIGINT NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, trade_date)
);
```

### 3.2 Corporate Actions Table (`raw_sgx_corporate_actions`)

```sql
CREATE TABLE IF NOT EXISTS raw_sgx_corporate_actions (
    symbol VARCHAR NOT NULL,
    ex_date DATE NOT NULL,
    action_type VARCHAR NOT NULL, -- 'DIVIDEND' or 'SPLIT'
    action_value DOUBLE NOT NULL, -- Dividend amount in SGD or Split ratio
    announced_date DATE,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, ex_date, action_type)
);
```

### 3.3 Corporate Calendar Table (`raw_sgx_corporate_calendar`)

```sql
CREATE TABLE IF NOT EXISTS raw_sgx_corporate_calendar (
    symbol VARCHAR NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR NOT NULL, -- 'EARNINGS', 'EX_DIVIDEND', 'INDEX_REBALANCE'
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (symbol, event_date, event_type)
);
```

### 3.4 Raw News & Sentiment Table (`raw_sgx_news_sentiment`)

```sql
CREATE TABLE IF NOT EXISTS raw_sgx_news_sentiment (
    article_id VARCHAR PRIMARY KEY,
    symbol VARCHAR NOT NULL,
    published_at TIMESTAMP NOT NULL,
    headline VARCHAR NOT NULL,
    sentiment_score DOUBLE, -- FinBERT polarity score: [-1.0, 1.0]
    regime_tag VARCHAR,     -- Article classification: 'BULLISH', 'BEARISH', 'NEUTRAL'
                            -- Diagnostic metadata; feature pipeline consumes continuous sentiment_score
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.5 Feature Matrix Table (`features_sgx_daily`)

```sql
CREATE TABLE IF NOT EXISTS features_sgx_daily (
    symbol VARCHAR NOT NULL,
    trade_date DATE NOT NULL,
    -- PIT Adjusted Prices & Technicals
    adj_close DOUBLE NOT NULL,
    rsi_14 DOUBLE,
    macd_signal DOUBLE,
    atr_14 DOUBLE,
    volume_ratio DOUBLE,
    -- Macro & Sentiment Features
    sora_3m_rate DOUBLE,
    news_sentiment_avg_3d DOUBLE,
    market_regime_code INT, -- Composite Code: 0 (Bull-LowVol), 1 (Sideways-MedVol), 2 (Bear-HighVol)
    -- Known Future Inputs for TFT Encoder
    days_to_earnings INT,
    days_to_ex_dividend INT,
    is_index_rebalance_window INT,
    day_of_week INT,
    month_of_year INT,
    -- Prediction Return Targets (Full Horizon Set H = {1, 3, 5, 10, 20, 60})
    target_return_h1 DOUBLE,
    target_return_h3 DOUBLE,
    target_return_h5 DOUBLE,
    target_return_h10 DOUBLE,
    target_return_h20 DOUBLE,
    target_return_h60 DOUBLE,
    -- Prediction Direction Targets (Full Horizon Set H = {1, 3, 5, 10, 20, 60})
    target_dir_h1 INT,
    target_dir_h3 INT,
    target_dir_h5 INT,
    target_dir_h10 INT,
    target_dir_h20 INT,
    target_dir_h60 INT,
    as_of_timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (symbol, trade_date)
);
```

---

## 4. Subsystem Deep-Dive

### 4.1 Ingestion & PIT Storage Engine (`src/data/`)

- `ingest_sgx.py`: Ingests raw unadjusted daily OHLCV prices, corporate action events (dividends/splits), and corporate calendar schedules.
- `pit_store.py`: Manages DuckDB connections and executes dynamic ASOF JOIN logic and corporate action factor scaling to generate PIT price series. Ensures historical snapshots remain unaltered by subsequent events. *(See `docs/specs/pit_adjustment_engine_v1.md` for the detailed operational contract — currently DRAFT, open questions pending Cola/PE routing.)*

### 4.2 Feature Engineering & Selection Pipeline (`src/features/`)

- `build_features.py`: Calculates technical indicators (pandas-ta), macro spreads (SORA 3-month rates), and corporate calendar proximity features (`days_to_earnings`, `days_to_ex_dividend`).

**`market_regime_code` Derivation Protocol:** To harmonize technical volatility with headline sentiment, `market_regime_code` is computed as a categorical state $\{0, 1, 2\}$ combining rolling technical conditions (20-day ATR quantile and ADX trend strength) with the rolling 3-day mean FinBERT news polarity (`news_sentiment_avg_3d`).

- **0 (Bull / Low Volatility):** ADX > 20, ATR₂₀ below 50th percentile, Sentiment ≥ 0.05
- **2 (Bear / High Volatility):** ATR₂₀ above 75th percentile OR Sentiment ≤ −0.20
- **1 (Sideways / Medium Volatility):** All other market regimes

*(Verified disjoint: Bull requires ATR₂₀ < 50th pct, Bear requires ATR₂₀ > 75th pct or Sentiment ≤ −0.20 — no day can satisfy both conditions simultaneously.)*

- `shap_selector.py`: Applies rolling TreeSHAP feature selection to eliminate collinear predictors before passing feature tensors into the TFT encoder.

### 4.3 Model Architecture Subsystem (`src/models/`)

`tft_model.py`: Implements PyTorch Lightning Multi-Task Temporal Fusion Transformer.

- **Static Inputs:** Asset Sector, Market Cap classification bucket.
- **Known Future Inputs:** Calendar proximity (`days_to_earnings`, `days_to_ex_dividend`), index rebalance flags, day-of-week, month.
- **Observed Past Inputs:** Historical PIT returns, RSI, MACD, ATR, macro rates, news sentiment scores, `market_regime_code`.
- **Outputs:** Dual forecast heads delivering Quantile Predictions ($q_{10}, q_{50}, q_{90}$) and Upward Directional Probabilities $\hat{p}^{(h)}$ across the full set of horizons $h \in \{1, 3, 5, 10, 20, 60\}$.

### 4.4 NLP & Sentiment Subsystem (`src/features/sentiment.py`)

- Extracts financial news headlines from EOD feeds/Finnhub.
- Calculates headline polarity scores using FinBERT ($[-1.0, 1.0]$) and assigns per-article `regime_tag` (BULLISH, BEARISH, NEUTRAL) as diagnostic metadata for raw record inspection.
- Downstream feature aggregation processes raw numerical `sentiment_score` values into rolling averages (`news_sentiment_avg_3d`) used directly by `build_features.py` for regime derivation.
- Enforces strict PIT timestamp filtering ($t_{\text{published}} < t_{\text{cutoff}}$) before rolling up daily sentiment averages into `features_sgx_daily`.

### 4.5 Execution & Backtesting Engine (`src/backtest/`)

`engine.py`: Event-driven backtesting module executing portfolio allocation decisions.

**SGX Transaction Cost Model:**

- Brokerage Commission: 0.08% of trade value (minimum SGD 10.00)
- SGX Clearing Fee: 0.0075% of trade value
- SGX Trading Access Fee: 0.005% of trade value
- Market Impact Slippage: $S_{i,t} = \alpha \times \left(\frac{\text{Trade Volume}}{\text{ADV}_{20}}\right)^\beta \times \text{ATR}_{14}$

---

## 5. Technical Roadmap & Phase Breakdown

*(Shared / Module Layout section — Beer may propose directly per Document Governance table above.)*

### Phase 1: Infrastructure, Ingestion & PIT Schema (Weeks 1–2)

- Setup project directory layout, virtual environment, and DuckDB storage layer.
- Implement raw price ingestion (`raw_sgx_daily`), corporate actions table (`raw_sgx_corporate_actions`), and dynamic PIT adjustment engine in `src/data/pit_store.py`, per `docs/specs/pit_adjustment_engine_v1.md` once its open questions are resolved.
- Gatekeeper verification via unit tests in `tests/test_ingestion.py`.

### Phase 2: Feature Engineering, NLP & Multi-Task TFT Pipeline (Weeks 3–4)

- Build technical features (`build_features.py`), sentiment extraction (`sentiment.py`), and corporate calendar encoder inputs.
- Implement PyTorch Lightning multi-task TFT (`tft_model.py`) with hybrid loss (quantile + directional) covering all horizons $h \in \mathcal{H}$.
- Gatekeeper verification via tests in `tests/test_features.py` and `tests/test_models.py`.

### Phase 3: Out-of-Sample Backtesting & Strategy Audit (Weeks 5–6)

- Implement event-driven backtesting engine with realistic SGX cost structure (`engine.py`).
- Generate performance reports against STI ETF benchmark (E17.SI).
- Matcha (ChatGPT) independent red-team audit review completed and findings dispositioned; final phase sign-off by Sprite.

---

## 6. Disposition Matrix for Audit Findings

*(Historical record — append-only. Do not edit rows below; add new rows for new findings.)*

| Finding # | Description | Resolution Status | Architectural Action Taken |
|---|---|---|---|
| 1 | Horizon Mismatch | Resolved | Expanded horizon set to $\mathcal{H} = \{1, 3, 5, 10, 20, 60\}$ trading days. Synchronized DuckDB schema in 3.5 with explicit return and directional target columns for all six horizons. |
| 2 | Target Formulation | Resolved | Added hybrid multi-task output head combining Quantile Regression and Directional Classification ($\hat{p}^{(h)}$). |
| 3 | Pilot Universe | Resolved | Consolidated pilot watchlist to 5 STI stocks: DBS, OCBC, UOB, Singtel, SIA. |
| 4 | Sentiment Pipeline | Resolved | Added Subsystem 4.4 (`sentiment.py`) and DuckDB table `raw_sgx_news_sentiment` with explicit PIT timestamps. |
| 5 | Known Future Inputs | Resolved | Restored corporate calendar inputs (`days_to_earnings`, `days_to_ex_dividend`, `is_index_rebalance_window`). |
| 6 | Corporate Action PIT Leakage | Resolved (Rule 12) | Replaced retroactively adjusted prices with unadjusted raw OHLCV and dynamic PIT adjustment factor engine. |
| 7 | Transaction Cost Model | Resolved | Removed non-applicable stamp duties; added explicit SGX Clearing Fee (0.0075%), Access Fee (0.005%), and Brokerage Commission (0.08%). |
| 8 | Document Location | Resolved | Consolidated master technical specification directly into `docs/ARCHITECTURE.md`. |
| 9 | Gatekeeping Authority | Resolved | Updated Phase 3 verification gate wording to reflect Sprite as the final sign-off authority (Matcha advises, Sprite decides). |
| 10 | Market Regime Semantics | Resolved | Added explicit aggregation protocol in Section 4.2 mapping per-article news sentiment polarity and technical volatility (ADX/ATR) into daily categorical `market_regime_code`. |
| 11 | Team Structure Realignment | Noted, not a technical finding | Document governance table added 2026-07-24 reflecting TEAM_STRUCTURE.md v3.0 (Cola as Chief Architect / Protected Section owner, Beer as Claude Code implementation authority). §7 below updated to remove stale PM/PE references. See `TEAM_STRUCTURE.md` for full role definitions. |

---

## 7. Handoff Contract (Phase 1 Launch)

*(Implementation Notes — Beer may edit this section freely; it reflects current operational process, not architectural intent.)*

**Updated 2026-07-24** to reflect TEAM_STRUCTURE.md v3.0. This section previously referenced "PM" and "PE" roles from the retired three-Gemini-persona structure; those roles no longer exist. Current process:

With all schema targets synchronized and regime aggregation rules formalized in this document, Phase 1 initialization proceeds as follows:

1. Beer (Claude Code) initializes the Git feature branch `feature/phase-1-infrastructure`.
2. Beer populates `HANDOFF.md` with granular implementation tasks for Phase 1 (raw price schema, corporate actions table, and PIT adjustment engine per `docs/specs/pit_adjustment_engine_v1.md`).
3. Beer works through Task 1.1 (WSL Scaffolding & Virtual Environment Initialization) and subsequent tasks directly, running the Automated Gatekeeper (`TEAM_STRUCTURE.md` §8) before considering any task complete.
4. Any item touching a material-risk category (`TEAM_STRUCTURE.md` §6) — which includes the PIT adjustment engine — requires mandatory Matcha review before disposition.
5. Cola checks in at phase boundaries (or sooner if a Protected Section ADP is raised) rather than continuously.

---

## Review Sign-off

```
Confidence: High
Evidence Basis: Verified — all 10 original disposition matrix entries checked against source text (formulas, schema DDL, subsystem descriptions), not merely the matrix's claims.
Reviewer: Cola (Claude Desktop + Local MCP)
Reason: PIT adjustment math verified correct (split/dividend factors, feature/label information separation); horizon set fully synchronized across math spec and schema; market_regime_code Bull/Bear conditions confirmed logically disjoint; regime_tag now correctly scoped as diagnostic-only metadata.
```

*(Note: this sign-off predates the v3.0 governance restructuring and applies to the technical content of §1–§6 only, which was not altered by the 2026-07-24 governance update — only the document-governance header, §5/§7 role references, and the append-only Finding #11 note were added.)*
