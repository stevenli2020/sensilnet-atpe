# INVESTMENT_FRAMEWORK.md
**Version:** 1.0 | **Status:** Approved by Investment Committee | **Type:** Canonical Investment Framework | **Audience:** Future Architects, AI Agents, Quant Researchers, Engineers, Product Owners

---
# 1. Purpose
## 1.1 Why This Document Exists
Records complete investment philosophy behind AI Investment Prediction Platform. **NOT**: implementation doc, ML spec, or architecture doc. Answers: **"What investment philosophy should the AI learn and why?"**
Created after review of original project proposal/architecture: proposal had strong tech architecture, data sources, ML design, but lacked explicit investment philosophy justifying *why* data sources collected and *how* they should jointly drive decisions → risk of platform becoming capable prediction engine w/ no investment identity. Doc closes this gap.

## 1.2 Scope
Defines: platform's investment philosophy; reasoning behind each adopted philosophy; why each selected; why some prioritized over others; how philosophies complement each other; implementation preferences to preserve; design principles from Committee discussions.
Does **NOT** define: software architecture, ML implementation, DB design, infra, APIs, deployment, programming language, cloud platform → belongs in **ARCHITECTURE.md**.

## 1.3 Relationship With Other Project Docs
Reading/dependency order:
```
INVESTMENT_FRAMEWORK.md
        │
        ▼
INITIAL_PROPOSAL.md
        │
        ▼
ARCHITECTURE.md
        │
        ▼
Implementation
```
Philosophy→proposal→architecture→implementation. Intentional: philosophy must lead AI design, not the reverse.

## 1.4 Intended Audience
Written for newcomers w/ no prior context: future SWEs, quant researchers, AI engineers, architects, product owners, future AI assistants, original author returning later. Reader must grasp **what** was decided AND **why** — reasoning preserved (not just conclusions) to avoid reopening resolved debates.

---
# 2. Project Philosophy
Recurring decision criteria from Committee discussions (not investment philosophies themselves, but institutional knowledge):

## Principle 1 — Investment Philosophy Before AI
Most important conclusion overall: **"The AI exists to implement an investment philosophy."** Philosophy must never be invented to justify a model.
- Wrong: `We have a TFT model. Let's find some financial features.`
- Correct: `Professional investors think this way. Let's design an AI capable of learning those behaviours.`
Influences every later architectural decision.

## Principle 2 — Do Not Reinvent the Wheel
Adopt mature research/institutional practice/quality OSS over rebuilding: Financial NLP, financial LMs, event detection, sentiment analysis, proven investment factors. Alpha ≠ recreating existing tech; Alpha = intelligent combination. Reduced complexity, increased realism.

## Principle 3 — Complexity Must Justify Itself
Every component adds: engineering effort, maintenance cost, debugging complexity, data requirements, operational risk. **"Complexity carries the burden of proof."** Adopt only if produces ≥1 of: measurable prediction improvement, significantly better explainability, materially simpler design, clear institutional value. "Interesting" alone ≠ sufficient.

## Principle 4 — Preserve Explainability
No black box. Every major feature maps to identifiable philosophy: Momentum indicators→Momentum Philosophy; financial ratios→Quality Philosophy; economic indicators→Macro Philosophy. Enables predictions explainable in language familiar to institutional investors.

## Principle 5 — AI Learns Relationships, Not Rules
Rejected hard-coded rules, e.g.:
```
IF PE < 10
THEN BUY
```
or
```
RSI < 30
=
BUY
```
Instead AI learns: when Momentum works / Value fails / Macro dominates / Events override trends / Sentiment matters / earnings revisions are meaningful. Goal: discover relationships from data, not encode decades of rules.

## Principle 6 — Avoid Infinite Scope Expansion
V1 stays focused; adopt existing mature research rather than turning discussions into new research projects. Applied to: sentiment analysis, financial NLP, earnings revisions, event detection, + various architecture debates.

## Principle 7 — Every Philosophy Answers a Different Question
Rule: if 2 philosophies answer the same question, one is unnecessary → produced 8 complementary (not competing) philosophies.

---
# 3. Definition of Alpha
## 3.1 What Alpha Is NOT
NOT: using TFT vs another model; larger NNs; more indicators; more data; more features; downloading FinBERT/other OSS model; new prediction algorithm. All tools — none = sustainable Alpha.

## 3.2 What Alpha IS
> **Alpha = the AI's ability to intelligently integrate multiple proven investment philosophies under different market conditions, discovering predictive relationships/interactions unavailable to individual strategies in isolation.**
Platform doesn't invent new philosophy; combines decades of institutional research into unified learning framework. Edge = integration, not invention.

## 3.3 Why This Definition Matters
Drove decisions: leverage mature financial NLP (not custom sentiment engine); adopt proven factors (not new indicators); use established economic relationships (not proprietary macro theories). Engineering effort → integration, learning interactions, explainability, prediction quality (most likely to yield sustainable Alpha).

## 3.4 AI vs Alpha Relationship
Deliberately separated: **Investment Knowledge** = "what should be learned?"; **AI** = "how should it be learned?" Simple distinction, profound architectural implications — preserve this separation.

---
# 4. Investment Framework Overview
8 complementary philosophies adopted (NOT 8 independent trading strategies) — 8 analytical lenses per opportunity, each answering a different question, together = 1 integrated framework. Not equal weight:

**Core Philosophies:** Momentum, Quality, Macro Regime, Relative Value, Event-Driven
**Supporting Philosophies:** Value, Earnings Revision, Market Perception

---
# 5. Investment Philosophies
Goal: not "the best" strategy, but a set that is: academically defensible, widely institutionally adopted, complementary (no duplication), naturally mapped to proposed AI architecture, jointly explains every major feature's existence.
Evaluation criteria (all philosophies): conceptual soundness; academic evidence; institutional adoption; applicability to SGX; compatibility w/ proposed AI architecture; contribution across multiple prediction horizons; expected implementation complexity.

---
## 5.1 Momentum (Core)
**Status:** Approved | **Decision:** Adopt | **Role:** Core | **Priority:** Very High | **Confidence:** ★★★★★

**Exec Summary:** Unanimous. Most researched/institutionally accepted factor. Momentum Investing ≠ Technical Analysis — not building a technical trading system; indicators = measurements of underlying philosophy. Question: **"What is the market currently rewarding?"**

**Thesis:** Markets show persistence — winners keep outperforming, losers underperforming (intermediate term). Explanations: behavioral finance (underreaction, gradual info diffusion, institutional buy/sell constraints, herding) vs traditional finance (risk compensation). Committee avoided picking an explanation — AI learns whether Momentum predicts under varying conditions.

**Why selected:** decades of academic validation; institutional adoption; extensive implementation experience; strong ML compatibility; direct SGX applicability. Survived multiple market cycles → suitable foundation.

**NOT:** blindly following price; buying every breakout; relying on RSI alone; MAs as trading rules. Indicators = observations of behavior; AI determines predictive value.
```
Momentum → Observed through indicators → Learned by AI
```
NOT:
```
Moving Average Cross → BUY
```

**Primary question:** *What is the market currently rewarding?* — every Momentum feature must serve this; else reconsider inclusion.

**Data sources:** historical prices, returns, trading volume, volatility, moving averages, trend strength, relative strength, breakout behaviour, momentum oscillators (observations, not decisions).

**Horizon contribution:** 1D: Medium | 5D: Medium | 20D: Very High | 60D: High | 120D: Moderate. Best at intermediate horizons; long-term increasingly driven by fundamentals.

**Failure modes:**
- *Sudden market reversal* — winners→losers rapidly.
- *Major corporate events* — earnings/regulatory/M&A can invalidate trends immediately → complements Momentum via Event-Driven.
- *Macro regime changes* — sector leadership shifts fast; Momentum reacts too slowly → Macro Regime provides context.
- *Crowded trades* — institutional crowding → violent unwinds; AI learns these rather than assuming persistence.

**Relationships:** Does NOT measure business quality, valuation, econ conditions, or investor perception — measures observable market behavior only. Strongest interactions: Event-Driven (events create new trends), Market Perception (sentiment accelerates/weakens Momentum).

**AI learning objective:** when Momentum predicts returns; when it fails; which measures matter most; interaction w/ regimes; variance across industries; variance across horizons. Goal = predictive relationships, not indicator optimization.

**Architecture mapping:** historical market data, technical indicators, volume/return/volatility features. Future features may expand provided they serve same philosophy.

**Implementation prefs:** avoid hard-coded trading rules; prefer feature engineering, historical learning, probabilistic prediction, explainability. Momentum = learned, not programmed.

**Discussion summary:** minimal disagreement; main point was separating Momentum Investing from Technical Analysis (indicators are instruments, not the philosophy itself) — improves conceptual organization.

**Final decision:** **Adopt.** Reasoning: exceptional academic support, institutional adoption, ML compatibility, complements all other philosophies w/o overlap → Core Philosophy.

---
## 5.2 Quality (Core)
**Status:** Approved | **Decision:** Adopt | **Role:** Core | **Priority:** Very High | **Confidence:** ★★★★★

**Exec Summary:** 2nd pillar. Momentum = market behavior; Quality = underlying business. Question: **"Is this a fundamentally strong company?"** Indispensable since long-term performance depends on business performance, not price alone.

**Thesis:** High-quality firms: durable profitability, healthy balance sheets, consistent cash generation, disciplined capital allocation, resilient earnings, sustainable competitive advantages. Markets may temporarily mis-price these, but quality matters more over longer horizons. Deliberately NOT defined via single metric — emerges from multiple complementary measurements.

**Why selected:** unanimous; strong institutional adoption; intuitive rationale; fits SGX blue-chips; strong synergy w/ Value; naturally explainable. Considered the fundamental anchor of the thesis.

**Primary question:** *Is this a fundamentally strong business?* — metrics not improving this understanding should be questioned.

**Data sources:** ROE, ROA, operating margins, net margins, earnings consistency, FCF, debt ratios, interest coverage, cash flow stability, capital efficiency. No single ratio dominates — intentionally multi-dimensional.

**Horizon contribution:** 1D: Low | 5D: Low | 20D: Moderate | 60D: High | 120D: Very High. Business quality matters increasingly at longer horizons.

**Failure modes:**
- *Value traps hidden as Quality* — historically strong financials but structural decline (tech disruption, changing consumer behavior, regulatory change, eroding moat). Historical Quality ≠ future Quality; AI must learn changing trends, not assume permanence.
- *Accounting distortion* — one-off gains, adjustments, aggressive revenue recognition, unusual tax treatments → evaluate via multiple complementary indicators, not one metric.
- *Slow reaction* — Quality changes slowly; can't react fast to earnings surprises, M&A, CEO changes, macro shocks → hence Event-Driven + Market Perception adopted as complements.

**Relationships (central to framework):**
- *Value*: Value asks "cheap?"; Quality asks "good?" — deliberately separate; cheap ≠ good, good ≠ cheap. Evaluate Quality before letting Value strengthen thesis → reduces value-trap exposure.
- *Relative Value*: e.g., 14% ROE looks attractive alone, but if peer banks generate 18–20%, assessment changes — Relative Value contextualizes Quality metrics.
- *Macro Regime*: desirable financial characteristics shift w/ rate environment; AI learns how Macro affects Quality's predictive power.

**AI learning objective:** which Quality metrics predict best; industry-specific Quality definitions; Quality across economic cycles; interaction w/ valuation; contribution across horizons. No assumed equal importance across metrics.

**Architecture mapping:** financial statements, profitability/balance-sheet/cash-flow metrics, earnings quality, capital efficiency, financial ratios. Future feature engineering must not alter conceptual purpose.

**Implementation prefs:** remain highly interpretable — explainable via recognizable financial metrics, not opaque latents; favor robust widely-accepted measures over specialized proprietary ratios.

**Discussion summary:** almost no disagreement; focus was keeping Quality conceptually distinct from Value (Quality=business strength; Value=price attractiveness) — improves explainability, matches institutional practice.

**Final decision:** **Adopt.** Long-term foundation of thesis; complements all other philosophies; strong academic/institutional support; maps naturally to available data; improves interpretability → Core Philosophy.

---
## 5.3 Macro Regime (Core)
**Status:** Approved | **Decision:** Adopt | **Role:** Core | **Priority:** High | **Confidence:** ★★★★★

**Exec Summary:** Provides economic context for all other philosophies. Rarely gives direct buy/sell signals. Question: **"What economic environment are we investing in?"** Identical fundamentals → different outcomes under different macro conditions; ignoring this reduces robustness.

**Thesis:** Corporate performance, sector leadership, investor preference, valuation multiples all shaped by: interest-rate cycles, inflation, economic growth, monetary policy, currency moves, unemployment, market liquidity. Macro Regime doesn't predict company performance directly — it contextualizes interpretation of other philosophies.

**Why selected:** indispensable as context (not competition) — without it, AI might assume relationships from one economic period hold universally; Macro lets model recognize changing environments vs treating markets as stationary.

**Primary question:** *What economic environment are we currently operating in?* — focuses on context, not individual companies.

**Data sources:** interest rates, inflation, GDP growth, PMI, exchange rates, government bond yields, central bank announcements, money supply, market indices, sector indices. Preference: indicators w/ long histories & clear economic interpretation.

**Horizon contribution:** 1D: Low | 5D: Moderate | 20D: High | 60D: High | 120D: Very High. Influence grows w/ horizon.

**Failure modes:**
- *Short-term noise* — daily moves often lack meaningful macro shifts; macro shouldn't dominate short-term predictions.
- *Delayed economic data* — many indicators published monthly/quarterly; AI must learn to use stale-but-informative data appropriately.
- *Unexpected shocks* (pandemics, geopolitical conflict, financial crises) — historical macro relationships may temporarily break; model learns these rather than assuming stability.

**Relationships:** influences every philosophy — Momentum (trends strengthen/weaken w/ macro backdrop); Quality (defining financial characteristics shift by rate environment); Value (multiples expand/contract w/ macro); Event-Driven (same announcement, different reaction by economic conditions). Acts as contextual layer, not a competing philosophy.

**AI learning objective:** most predictive macro variables; how macro alters factor effectiveness; sector-specific responses; influence across horizons; when macro dominates company-specific info.

**Architecture mapping:** economic datasets, market indices, central bank data, interest-rate data, inflation data, sector performance.

**Implementation prefs:** treat as contextual features; rejected simplistic rules (e.g., "Rising rates = Sell"); AI learns interaction w/ all other philosophies.

**Discussion summary:** Macro shouldn't compete with company-level analysis — purpose is environmental context; improves conceptual clarity.

**Final decision:** **Adopt.** Strengthens every other philosophy via economic context → Core Philosophy despite rarely being a direct signal.

---
## 5.4 Relative Value / Peer Analysis (Core)
**Status:** Approved | **Decision:** Adopt | **Role:** Core | **Priority:** Very High | **Confidence:** ★★★★★

**Exec Summary:** One of the most significant additions vs. original proposal (which focused on isolated companies). Professional investors rarely evaluate in isolation — ask: **"How does this company compare with its peers?"** Fundamentally improved platform's conceptual design.

**Thesis:** *"Everything is relative."* Financial performance/valuation/profitability/market performance only fully meaningful vs. similar businesses. PMs rarely ask "Is DBS good?" — they ask "Is DBS better than OCBC or UOB today?" Enables AI to move beyond absolute measures to competitive positioning — considered one of the largest conceptual improvements to the original proposal.

**Why selected:** complements nearly every other philosophy (improves Quality, Value, Momentum, Event interpretation) w/o overlap. Especially important for SGX's concentrated sectors w/ few direct competitors: Banks, REITs, Telecoms, Property Developers, Shipping, Industrial Conglomerates → comparative analysis both practical and informative.

**Primary question:** *How attractive is this company relative to comparable businesses?* — distinct from Value ("cheap?"): RV asks "better than peers?" A company can be expensive yet the strongest opportunity in-sector; conversely a cheap company may be the weakest competitor. Distinction is critical.

**Data sources (multi-dimensional, no fixed formula):**
- *Financial performance:* Revenue Growth, Earnings Growth, ROE, ROA, Operating Margin, Net Margin
- *Valuation:* P/E, P/B, EV/EBITDA, Dividend Yield, FCF Yield
- *Market behaviour:* Momentum, Relative Strength, Volatility
- *Capital structure:* Debt Ratios, Liquidity, Capital Efficiency
AI learns which comparisons carry the greatest predictive value.

**Dynamic Peer Analysis:** significant discussion topic — simple for one company (e.g. DBS) but platform must scale across many SGX names → peer analysis must be dynamic (objective rules), not manually maintained. Determinants: industry classification, sector classification, business-model similarity, market cap, geographic exposure. Avoid hard-coded peer lists → improves scalability.

**Horizon contribution:** 1D: Low | 5D: Moderate | 20D: High | 60D: Very High | 120D: Very High. Value grows over medium/long horizons as business-performance differences emerge.

**Failure modes:**
- *Incorrect peer selection* — poor selection → misleading conclusions; reinforces need for dynamic peer construction.
- *Structural industry differences* — same-sector peers may differ in business model; AI must learn this, not assume full comparability.
- *Temporary market divergence* — markets sometimes reward weaker firms in speculative periods; underperformance ≠ poor long-term quality; AI learns exceptions from history.

**Relationships:**
- *Quality*: Quality measures strength; RV determines if that strength is exceptional or average.
- *Value*: Value = attractively priced?; RV = are other opportunities even more attractive? Together improve decision quality.
- *Momentum*: Relative Momentum vs. direct competitors often stronger signal than absolute Momentum; reveals info hidden by broad market moves.
- *Event-Driven*: after major announcements, RV assesses whether market reaction is justified vs. peers facing similar conditions.

**AI learning objective:** most important peer characteristics; industry differences; when relative > absolute analysis; how peer relationships evolve over time; industry-specific comparison methods. No fixed weighting schemes prescribed.

**Architecture mapping:** peer datasets, industry classifications, comparative financial/valuation/technical metrics. Future engineering should strengthen comparative analysis over isolated metrics.

**Implementation prefs:** dynamic peer analysis preferred; rejected manually curated lists (maintenance burden, poor scalability); support auto-generated peer groups that evolve w/ market — key architectural objective.

**Discussion summary:** one of most productive Phase 1 discussions; original proposal analyzed companies in isolation; Committee concluded institutional investors don't; systematic peer analysis strengthened both philosophy and architecture; produced requirement for dynamic peer analysis to scale beyond a small manually-selected SGX set.

**Final decision:** **Adopt.** Improves institutional realism, complements every major philosophy, scales naturally, aligns w/ professional practice → Core Philosophy.

---
## 5.5 Value (Supporting)
**Status:** Approved with Modifications | **Decision:** Adopt with Modifications | **Role:** Supporting | **Priority:** Medium | **Confidence:** ★★★★☆

**Exec Summary:** Required most discussion of any philosophy. Value = one of the most successful philosophies ever, overwhelming academic/institutional support — BUT common weakness: often flags stocks cheap for legitimate reasons ("value traps") historically reducing pure-valuation strategy effectiveness. Committee repositioned (not rejected) Value: **Supporting Philosophy** — strengthens/weakens a thesis already established by Core Philosophies. Preserves strengths, reduces weaknesses.

**Thesis:** *"Markets occasionally misprice good businesses"* — price/intrinsic value converge over time. But valuation alone insufficient — many cheap companies stay cheap due to deteriorating business. Goal ≠ buy low-valuation indiscriminately. Value should answer: **"Is this fundamentally strong company also attractively priced?"** — a key committee distinction.

**Why modified:** Value has exceptional academic support; many top investors are Value investors; valuation is essential to professional analysis — BUT standalone Value strategies historically weak (cheap stocks often stay/never recover). Repositioned as confirmation rather than independent driver → reduces value-trap exposure, preserves long-term strengths.

**Primary question:** *Is this company attractively priced relative to its underlying quality?* — deliberately NOT "is this company cheap?" Cheapness alone ≠ objective; attractive pricing + strong quality = objective.

**Data sources:** P/E, P/B, EV/EBITDA, Dividend Yield, FCF Yield, Enterprise Value, Earnings Yield — interpreted collectively, not individually.

**Horizon contribution:** 1D: Very Low | 5D: Low | 20D: Moderate | 60D: High | 120D: Very High. Increasingly informative at longer horizons.

**Relationships:** rarely operates independently.
- *Quality*: strong Quality + attractive Value = much stronger candidate than either alone.
- *Relative Value*: cheap company may still be less attractive than competing opportunities (context).

**AI learning objective:** when valuation predicts returns; when cheap→value trap; valuation behavior across industries; macro's influence on valuation multiples; when valuation deserves more/less emphasis.

**Committee decision:** unanimous **Adopt with Modifications** — Value = Supporting Philosophy, strengthens thesis rather than defining it.

---
## 5.6 Event-Driven (Core)
**Status:** Approved | **Role:** Core | **Confidence:** ★★★★★

**Exec Summary:** Markets respond to new info, not just long-term fundamentals. Question: **"Has new information materially changed the investment thesis?"** Unlike Momentum (price behavior), Event-Driven focuses on underlying cause of moves.

**Typical events:** earnings releases, SGX announcements, M&A, dividend changes, management changes, regulatory announcements, litigation, major contracts, capital raising. Not every announcement matters — AI must distinguish meaningful events from routine disclosures.

**Why selected:** explains abrupt moves that financial ratios can't; complements Momentum, Market Perception, Earnings Revision; well-suited to AI given NLP advances.

**Failure modes:** insignificant announcements; duplicate news coverage; delayed market reaction; false positives from routine disclosures. AI learns event significance rather than assuming uniform importance.

**AI learning objective:** which events matter; industry-specific reactions; event persistence; historical post-event behavior; interaction w/ other philosophies.

**Implementation preference:** leverage mature OSS event-extraction/financial NLP where practical — don't build an event engine from first principles.

**Committee decision:** **Adopt.** One of 5 Core Philosophies — captures information unavailable from historical financial data alone.

---
## 5.7 Earnings Revision (Supporting)
**Status:** Approved (Modular) | **Role:** Supporting | **Confidence:** ★★★★☆

**Exec Summary:** Markets respond to changing expectations, not just earnings. Question: **"Have expectations for future performance changed?"** Valuable but data-dependent.

**Preferred inputs:** analyst forecasts, consensus revisions, target price revisions. Fallbacks: management guidance, earnings reports, historical earnings trends — keeps philosophy useful where analyst coverage limited.

**Why Supporting not Core:** unlike Quality/Momentum, depends heavily on external data availability → classified Supporting; predictive value remains high but implementation stays flexible.

**AI learning objective:** how expectation changes influence returns; when revisions matter; when markets already priced revisions; interaction w/ Event-Driven.

**Committee decision:** **Adopt (Modular).** Future implementations may strengthen as richer data becomes available.

---
## 5.8 Market Perception / Sentiment (Supporting)
**Status:** Approved with Modifications | **Role:** Supporting | **Confidence:** ★★★★☆

**Exec Summary:** Evolved beyond traditional "sentiment analysis" → platform measures **Market Perception** (how investors collectively interpret info), not simply positive/negative sentiment.

**Why modified:** generic sentiment analysis = little competitive advantage. Preferred: financial NLP, earnings-call interpretation, management tone, narrative changes, uncertainty, confidence, news importance — better reflects institutional practice.

**Preferred sources:** SGX announcements, financial news, earnings call transcripts, management commentary, analyst reports. Heavy reliance on retail social media discouraged (lower signal quality, esp. within SGX).

**AI learning objective:** which narratives matter; how sentiment changes over time; which news sources have predictive value; interaction w/ Event-Driven; interaction w/ Momentum.

**Implementation preference:** rejected building proprietary sentiment models — leverage mature OSS financial LMs/sentiment frameworks. Alpha = integration, not recreating NLP tech.

**Committee decision:** **Adopt with Modifications.** Market Perception acts primarily as a confidence modifier, not an independent thesis.

---
# 6. How the Philosophies Work Together
NOT 8 separate trading systems — each answers a different investment question:

| Philosophy | Primary Question |
|---|---|
| Momentum | What is the market rewarding? |
| Quality | Is this a fundamentally strong business? |
| Macro Regime | What economic environment are we operating in? |
| Relative Value | How does this compare with its peers? |
| Value | Is this quality business attractively priced? |
| Event-Driven | Has new information changed the investment thesis? |
| Earnings Revision | Have future expectations changed? |
| Market Perception | How is the market interpreting the information? |

Together = complementary evidence, not competing predictions. Not equal-vote systems: Core Philosophies establish the thesis; Supporting Philosophies strengthen/weaken/refine confidence in it. AI learns how these relationships evolve across market conditions.

---
# 7. Multi-Horizon Investment Philosophy
Platform = multi-horizon prediction engine by design; no single philosophy dominates every horizon.
- **Short-term:** Event-Driven, Market Perception, Earnings Revision
- **Medium-term:** Momentum, Macro Regime, Relative Value
- **Long-term:** Quality, Value
Diversity preserved deliberately — AI learns which philosophies contribute most per forecasting objective, rather than forcing all to predict all horizons.

---
# 8. Implementation Preferences
Preserve wherever practical:
- Investment philosophy drives AI architecture.
- Prefer mature academic research over invention.
- Leverage open-source financial AI where appropriate.
- Avoid hard-coded investment rules.
- Organise features by investment philosophy.
- Preserve explainability.
- Keep V1 focused and practical.
- Avoid unnecessary architectural complexity.
- Design modules that evolve independently.
- Let AI learn interactions rather than manually defining them.
Conceptual (not technical) — should shape future architectural decisions.

---
# 9. Scope Boundaries
Project does **NOT** seek to: invent a new investment philosophy; replace institutional investment practice; create proprietary NLP models where mature alternatives exist; optimise for only one prediction horizon; maximise model complexity; hard-code investment rules.
Instead: build an AI system learning from multiple proven philosophies while remaining explainable, scalable, practical.

---
# 10. Closing Statement
Review began after identifying a conceptual gap (strong architecture, no explicit investment framework) — now closed. Platform is no longer defined by ML models alone; grounded in a coherent investment philosophy from 8 complementary, institutionally recognised approaches. Committee deliberately did NOT invent a new investment theory — instead synthesised decades of proven practice into one framework the AI can learn, adapt, improve over time.
This document = canonical reference for the project's investment philosophy. Future architectural/implementation decisions must remain consistent with the principles, reasoning, and committee decisions recorded herein.
