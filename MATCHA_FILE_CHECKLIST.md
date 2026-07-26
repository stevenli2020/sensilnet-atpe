# Files to Share with Matcha — Complete Package

**Send all of these files to Matcha (ChatGPT Web UI) for the ADP review. These are the exact artifacts referenced in `docs/decision_log/MATCHA_INITIAL_PROMPT.md`.**

---

## Reading Order & Files

### Tier 1 — Foundational (Read first)
1. `docs/decision_log/MATCHA_INITIAL_PROMPT.md` — this prompt itself, tells Matcha what to do and what to expect
2. `docs/INVESTMENT_PHILOSOPHY.md` — the 8-lens framework that all 6 ADPs trace back to
3. `WORKFLOWS.md` — team structure, material-risk categories, how findings work, immutability rules

### Tier 2 — Context (Read for background)
4. `docs/INITIAL_PROPOSAL.md` — what was originally intended (6-week project, feature scope)
5. `docs/ARCHITECTURE.md` — current v1 implementation; shows what's missing/wrong

### Tier 3 — The Proposals (Read carefully)
6. `docs/decision_log/ARCHITECTURE_v2_PROPOSED.md` — full proposed v2 specification (vendor-agnostic, gated, lens-mapped)
7. `docs/decision_log/ADP-001-lens-hierarchy-and-traceability.md` — Core/Supporting model hierarchy
8. `docs/decision_log/ADP-002-bitemporal-versioning-calendar.md` — source versioning, available_at, calendar tiering
9. `docs/decision_log/ADP-003-fundamentals-filings-schema.md` — fundamentals schema + data-rights discipline
10. `docs/decision_log/ADP-004-macro-regime-redesign.md` — remove market_regime_code, restore macro features
11. `docs/decision_log/ADP-005-champion-challenger-governance.md` — baseline-first model governance, named benchmarks
12. `docs/decision_log/ADP-006-pilot-universe-and-data-rights.md` — two-tier universe, reopens Finding #3

### Tier 4 — Process (Skim for reference)
13. `reviews/REVIEW_FORMAT.md` — template for how to file findings (immutable artifacts, same session)
14. `SESSION_HANDOFF.md` — background on what's been done; context only

---

## Total Package Size

~180 KB of text artifacts across 14 files. Readable in ~2–3 hours if read carefully (not skimming).

---

## How to Deliver

**Option A (Recommended):** Pack these 14 files into a single archive or paste into a gist, with a note: *"Matcha, please read in the order listed in the checklist above, starting with MATCHA_INITIAL_PROMPT.md. That prompt explains what to do and why."*

**Option B:** Paste the files one at a time into the ChatGPT Web UI conversation, in the order above.

Either way, start with the prompt itself — it tells Matcha everything he needs to know about role, context, and what counts as a finding worth filing.

---

## What to Tell Matcha in a Cover Message

Something like:

> Hi Matcha,
> 
> We have six interlocking Architecture Decision Proposals (ADPs) that propose a major redesign of the Sensilnet system architecture, all of which hit the material-risk categories that trigger mandatory independent review.
> 
> Your job: review for domain-correctness risks — PIT leakage, backtest validity, label leakage, hidden data dependencies, structural weaknesses. File any findings as immutable artifacts per the REVIEW_FORMAT template, same session you produce them.
> 
> Start with the prompt file (MATCHA_INITIAL_PROMPT.md) — it explains everything. The reading order is in that file too.
> 
> Take the time you need. This is a deep review. Quality over speed.
> 
> Files attached.

---

## Matcha's Deliverable

One immutable finding artifact filed in `reviews/YYYY-MM-DD_sensilnet-atpe-adps_matcha.md`, containing:
- Summary of what was reviewed
- Each finding (Confidence / Evidence Basis / Reason)
- Bounded disagreement space if Cola responds to findings
- Matcha's final reply (once)

Sprite then records a disposition (Accepted / Deferred / Closed) for each finding.

**The finding is immutable once filed** — Matcha does not edit it; if a finding is wrong, that gets recorded as a new finding in a follow-up review, never retroactively erased.
