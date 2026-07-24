# CLAUDE.md — Repository Guide for Claude Code

**Purpose:** This file exists to keep Claude Code (operating as "Beer," the implementation authority — see `WORKFLOWS.md`) consistently effective across sessions. It is not written for humans; it is written so that a fresh Claude Code session can orient itself quickly without re-deriving conventions from scratch or drifting from established patterns.

**Governance context:** Read `WORKFLOWS.md` first if this is a new session with no prior context on the project's process. This file assumes familiarity with that document and focuses on repository-specific mechanics.

---

## 1. What This Project Is

Sensilnet ATPE (Automated Trading & Prediction Engine) — a daily-batch, Point-In-Time (PIT) compliant prediction and decision-support system for SGX blue-chip equities, using a multi-task Temporal Fusion Transformer. Full technical design lives in `docs/ARCHITECTURE.md`. This file does not duplicate that content — it covers *how to work in this repo*, not *what the system does*.

---

## 2. Before You Touch Anything: Protected Sections

`docs/ARCHITECTURE.md` and `docs/specs/*.md` have sections with different edit authority. See `WORKFLOWS.md` §5 for the full table. The short version:

- **Vision, Design Principles, Data Contracts, Component Responsibilities → Cola's authority.** Do not edit these directly. If you believe one needs to change, draft an ADP (see §5 below) instead of editing the file.
- **Implementation Notes → yours to edit freely.**
- **Module Layout → shared**, propose directly, no ADP required unless it changes a responsibility boundary.

If you're not sure which category an edit falls into, treat it as Protected and draft an ADP — the cost of an unnecessary ADP is small; the cost of a silent architectural drift is not.

---

## 3. Coding Conventions

*(To be filled in as real conventions solidify during Phase 1 implementation. Placeholder structure below — update this section directly, it is Implementation Notes territory.)*

- Python version: — pin once `requirements.txt` is generated from a real environment.
- Formatting: `black`, enforced by the gatekeeper — do not hand-format against your own judgment.
- Linting: `ruff`.
- Type checking: `mypy` — new code should be typed; do not silently loosen existing type coverage to make a check pass.
- Docstring style: — TBD, adopt whatever the first substantive module establishes and stay consistent.

---

## 4. Required Commands

```bash
# Full gatekeeper (run before considering any task done)
ruff check .
black --check .
mypy .
pytest
coverage report --fail-under=<threshold TBD>
pip check
git status --porcelain   # should be empty of unintended files

# Individual test run
pytest tests/<path> -v

# Environment
# .venv already exists at project root — activate it, do not create a second one
```

Do not summarize a failing gate result into a passing narrative. Raw gatekeeper output goes into the evidence trail as-is — this is a hard rule from `WORKFLOWS.md` §8, not a style preference.

---

## 5. When to Stop and Draft an ADP

Draft an ADP in `HANDOFF.md` instead of proceeding when:

- A spec in `docs/ARCHITECTURE.md` or `docs/specs/` is contradictory, infeasible, or would require implementing a known defect to satisfy as written.
- You've identified an implementation-level improvement (e.g., a simpler module boundary) that touches a Protected Section.
- You've hit the error-escalation threshold: 2 consecutive failures with the same error signature, or repeated signature-cycling with no test progress.

Do not silently patch around a bad spec. Do not implement a known defect because the spec technically calls for it. Stop, document the conflict, route to Cola (or Sprite if it's business-scope-level — see `WORKFLOWS.md` §4).

---

## 6. HANDOFF.md Discipline

You own `HANDOFF.md` operationally, but it's append-only-per-author once other agents (Sprite, Cola, Matcha) start contributing entries. Do not edit or remove another agent's entry — supersede it with a new dated entry if it's out of date. Tag every entry you add with `Author: Beer` and a timestamp.

---

## 7. Repository Norms

- **Never commit directly to `main`.** All implementation work happens on feature branches; Sprite approves merges.
- **Never mark a Matcha finding resolved yourself.** You may respond to a finding (one bounded reply, see `WORKFLOWS.md` §10.1); disposition is Sprite's alone.
- **File reviews same-session, not retroactively.** If you're ever in a position to file a review-like artifact, do it before the session ends — see `reviews/REVIEW_FORMAT.md` Rule 6 for why this matters (a real review was lost this way once already on this project).
- **Generate `requirements.txt` from a real environment**, not by hand-listing what you believe is installed — freeze against the actual `.venv`.

---

## 8. Common Pitfalls (populate as they're discovered)

*(This section should grow over time — when a mistake happens once, document it here so it doesn't happen twice. This is Implementation Notes territory — edit freely.)*

- *(none recorded yet — Phase 1 has not started)*

---

## 9. Architecture Map (quick orientation, not a substitute for `docs/ARCHITECTURE.md`)

```text
docs/ARCHITECTURE.md     — canonical system design, Protected + Implementation sections
docs/specs/               — component specs in draft, pending Matcha review + Sprite disposition
docs/RISK_REGISTER.md    — persistent domain risks (PIT leakage, sandboxing status, etc.)
docs/KNOWN_LIMITATIONS.md — accepted constraints, don't re-litigate these without new evidence
docs/decision_log/        — ADRs, permanent record of resolved architecture drift
reviews/                  — independent review artifacts, immutable once filed
HANDOFF.md                — active task board, append-only shared ownership
src/data/                 — ingestion, PIT storage
src/features/             — technical indicators, sentiment, SHAP selection
src/models/                — TFT model definition
src/backtest/              — event-driven backtesting engine
```
