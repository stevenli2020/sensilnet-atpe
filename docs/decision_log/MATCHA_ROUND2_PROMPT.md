# Prompt for Matcha — Round 2: Final Reply on ADP Bundle Amendments

Matcha — this is a **follow-up round**, not a fresh review. You already reviewed this bundle once (`reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`) and filed six findings. Cola has responded to all six within that same file, in the Disagreement Loop section. Per the bounded disagreement loop (`WORKFLOWS.md` §10.1), you get **one final reply** — not a new review, not renewed back-and-forth. This prompt tells you what changed and what to check before you write that reply.

---

## What Happened Since Your Review

All six of your findings were **accepted, not contested**. Cola amended the five affected ADPs directly (they were still `Status: OPEN`, so pre-approval revision is the normal path). Nothing was disputed — your job now is to verify the amendments actually close the gaps you identified, not to re-litigate whether the gaps existed.

## What to Read (in this order)

### 1. Start here — the response itself
**`reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`** — your own findings are unchanged (immutable, as they should be). Read Cola's response in the **Disagreement Loop** section at the bottom. It maps each of your six findings to a specific amendment and names exactly where in each ADP to find it.

### 2. Then check each amendment against the finding it answers

You don't need to re-read the full ADPs top to bottom — go straight to the amendment sections, each clearly marked and dated:

| Your Finding | File to Check | Section |
|---|---|---|
| Finding 1 (provenance gap in PIT replay) | `docs/decision_log/ADP-002-bitemporal-versioning-calendar.md` | "Amendment 1 (post-Matcha-review)" |
| Finding 2 (ESTIMATED calendar rows) | `docs/decision_log/ADP-002-bitemporal-versioning-calendar.md` | "Amendment 2 (post-Matcha-review)" |
| Finding 3 (extraction becoming canonical) | `docs/decision_log/ADP-003-fundamentals-filings-schema.md` | "Amendment 1 (post-Matcha-review)" |
| Finding 4 (weak benchmark ladder) | `docs/decision_log/ADP-005-champion-challenger-governance.md` | "Amendment 1 (post-Matcha-review)" |
| Finding 5 (regime-validation gap, cross-ADP) | `docs/decision_log/ADP-004-macro-regime-redesign.md` **and** `docs/decision_log/ADP-005-champion-challenger-governance.md` | Both: "Amendment (cross-ADP, post-Matcha-review)" — read both, they're designed as a matched pair |
| Finding 6 (dashboard-name overfitting) | `docs/decision_log/ADP-006-pilot-universe-and-data-rights.md` | "Amendment 1 (post-Matcha-review)" |

### 3. Two things Cola explicitly left for you, not resolved unilaterally

Check these specifically — Cola did not guess at these on your behalf, and your final reply is the place to settle them:

- **`ADP-005`, Open Question 2** (now annotated in the file): no numeric threshold has been set for "minimum regime-episode count / confidence-interval width below which the stability gate should be treated as inconclusive rather than pass/fail." Cola's note asks you to propose a specific number in your final reply, or explicitly defer it to the Phase 3/4 implementation spec. Pick one.
- **`ADP-006`, Open Question 3**: minimum peer-group size per sector (e.g., "no sector with fewer than N names") is still unset. Cola's note defers this to Sprite once the Phase 0 vendor trial shows actual per-sector coverage — confirm whether you agree that's an acceptable place to defer it, or whether you think it needs a floor value locked into the ADP now regardless of trial results.

---

## What You're Actually Doing This Round

Per finding, your final reply should land on one of:
- **Satisfied** — the amendment closes the gap as described; no further action needed on this finding.
- **Satisfied with a note** — closes the gap, but flag a residual concern for Sprite's awareness (not a new finding, just a caveat).
- **Not satisfied** — the amendment doesn't actually close the gap; explain specifically what's still missing. (This would be unusual given the amendments directly mirror your own recommendations, but if something was lost in translation, say so plainly.)

This is **not** an invitation to raise new findings unrelated to the original six. If you notice something genuinely new and material while reading the amendments, it's fine to flag it separately and clearly as a **new** observation (not folded into your final reply on the original six) — but don't let it turn this into a second full review pass.

## Where to Write Your Reply

Same file: `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md`, in the Disagreement Loop section, replacing the `*(awaiting)*` placeholder under **Matcha final reply**. Do not edit your original findings text or Cola's response — both are immutable at this point; only fill in your own final-reply placeholder.

After your final reply, this goes to Sprite for disposition. That's the end of your role in this round.

---

## File Checklist (What Sprite Should Share With You for This Round)

You should already have everything from Round 1. For this round specifically, make sure you have the **current** (amended) versions of:

- [ ] `reviews/2026-07-26_sensilnet-atpe-adps_matcha.md` (contains your findings + Cola's response)
- [ ] `docs/decision_log/ADP-002-bitemporal-versioning-calendar.md` (amended)
- [ ] `docs/decision_log/ADP-003-fundamentals-filings-schema.md` (amended)
- [ ] `docs/decision_log/ADP-004-macro-regime-redesign.md` (amended)
- [ ] `docs/decision_log/ADP-005-champion-challenger-governance.md` (amended)
- [ ] `docs/decision_log/ADP-006-pilot-universe-and-data-rights.md` (amended)

`ADP-001-lens-hierarchy-and-traceability.md` and `ARCHITECTURE_v2_PROPOSED.md` are unchanged from Round 1 — no need to re-send unless you want to double check something against them.
