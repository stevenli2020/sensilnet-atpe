# Review Artifact Format — Sensilnet ATPE

**Status:** ACTIVE — reference standard for all reviews filed in this folder.
**Established:** 2026-07-24, agreed by Sprite following the PIT Corporate-Action and Data-Vintage Contract trial round.
**Applies to:** All independent reviews by Matcha, Cola, or Beer's disagreement-loop responses.

---

## Purpose

Prior to this standard, review findings (e.g. Cola's four-round review of the Master Technical Blueprint, and Matcha's review of `docs/specs/pit_adjustment_engine_v1.md`) existed only as conversational output in chat sessions, not as versioned artifacts in the repository. This meant Sprite could not act on a finding without reconstructing the argument from chat history — a direct violation of the standard Team Structure v2 was designed to meet ("preserves an immutable disposition trail; leaves Sprite able to make a clear decision without reconstructing the argument from chat history").

Every independent review from this point forward must be filed here using this format.

---

## Filename Convention

```
reviews/YYYY-MM-DD_<artifact-name>_<reviewer>.md
```

- `YYYY-MM-DD` — date the review was conducted, not filed (backdate if filing retroactively, and note the filing date separately inside the document).
- `<artifact-name>` — short slug identifying what was reviewed, matching the reviewed file's name where possible (e.g. `pit-adjustment-engine-v1`).
- `<reviewer>` — `matcha`, `cola`, or `beer` (for disagreement-loop responses).

Example: `reviews/2026-07-24_pit-adjustment-engine-v1_matcha.md`

---

## Required Template

```markdown
# Review: <Artifact Name and Version>

**Reviewer:** Matcha (or Cola / Beer — whoever authored this review)
**Date:** YYYY-MM-DD
**Artifact reviewed:** path/to/file.md
**Artifact version at time of review:** (git commit hash or version string from the artifact's own header)
**Review type:** Independent technical review | Red-team audit | Math validation | Disagreement-loop response

---

## Summary Verdict
One or two sentences: approve / approve-with-conditions / reject / needs-rework.

---

## Findings

### Finding 1: <short title>
​```
Confidence: High | Medium | Low
Evidence Basis: Verified from direct text comparison | Inference | Recomputation | Domain knowledge
​```
**Description:** What was found.
**Reason:** Why it matters / what breaks if unaddressed.
**Recommendation:** What should happen next.

### Finding 2: ...
(repeat per finding)

---

## Disagreement Loop (if applicable)
- **Matcha finding:** ...
- **Beer response:** ... (bounded, one reply per Condition 2)
- **Matcha final reply:** ...
- **Sprite decision:** *(filled in by Sprite only — Accepted / Deferred / Rejected)*

---

## Disposition
*(Owned by PM/Sprite per Condition 1 — Beer does not fill this in.)*

| Finding # | Status | Disposition Note | Decided By |
|---|---|---|---|
| 1 | Open / Accepted / Deferred / Closed | | |
```

---

## Rules Governing This Format

1. **The Disposition table is never filled in by Beer.** Per Team Structure v2 Condition 1, Beer authors findings responses but does not own resolution status. Only PM (recording) and Sprite (deciding) write to that table.
2. **The Disagreement Loop section stays present even when empty**, so it's visible at a glance whether a review triggered the bounded response cycle (Matcha finding → Beer response → Matcha final reply → Sprite decision) or was accepted without contest.
3. **Artifact version must be pinned** (commit hash or the version string already present in the reviewed document's own header) — without this, a filed review becomes ambiguous once the underlying artifact changes again.
4. **Retroactive filing is permitted and encouraged** for reviews that already happened informally (e.g. verbally, or in a chat session) before this format existed — backdate the review `Date` field to when the review actually occurred, and note the filing date in a footer line if it differs materially.
5. **One file per review, not per artifact.** If an artifact is reviewed twice (e.g. v1 and a later v2), file two separate review documents rather than editing the first in place — this preserves history rather than overwriting it, consistent with the same immutability principle applied to corporate-action data in `docs/specs/pit_adjustment_engine_v1.md` §3.3.
6. **File within the same working session as the review, not retroactively.** On 2026-07-24, a Matcha review of `pit_adjustment_engine_v1.md` that was never filed became unrecoverable once the original conversation could no longer be located — the finding was real, but became unusable as evidence simply because it wasn't captured in time. Retroactive filing (Rule 4) remains permitted for reviews that predate this document, but going forward, filing is not a cleanup task to defer — it is the last step of the review itself. A review is not complete until it exists in `reviews/`.
