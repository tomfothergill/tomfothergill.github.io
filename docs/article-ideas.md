# Article ideas

A backlog of case studies and notes for the site, in the order they are worth
writing. Each entry is a brief, not a draft: the angle, the evidence to pull,
the gaps only Thomas can fill, and anything that must stay out. The prose is
his to write.

House rules that apply to every entry:

- **Anonymise clients.** Decided 2026-09-09. Selco, Toolstation and JD Sports
  are named in the source material; on the site they are "a national builders'
  merchant", "a UK trade retailer", "a sportswear retailer" or similar. Keep the
  specifics, lose the logo. A named client needs sign-off first.
- **Voice** (CLAUDE.md §8): first person, past tense, specific numbers,
  headlines that name the finding rather than the technology, admit limits, no
  adjectives about yourself.
- **Nothing invented.** Every figure below was measured or read from a source at
  the time of writing. Re-check against the live repo before publishing —
  pointers are given so you can.
- **The home index is three deep** (CLAUDE.md §5). Case studies compete for
  three rows; everything else is a note.

---

## Next: the Ask HyperFinity build (analytics-agent)

**What it is, in one line Thomas writes.** A natural-language analytics agent
that turns a business question into grounded SQL over a retailer's warehouse
and returns findings, charts, the SQL and an audit trail. Single-agent tool loop
on Bedrock (Claude), one deployment per client on AWS.

**Why this one next.** It is the most substantial thing he has built, it is
current, and the project's own knowledge wiki already contains the war stories
with numbers attached — the evidence-gathering is mostly done.

### The spine to consider

The strongest single thread is **corroboration that could not fail**: the day
a full profiling pass on a client's pricing portal reconciled to the warehouse
at 99.98% and produced three published rules — and the next day the portal's own
function definitions showed every table was a nightly `TRUNCATE`+`MERGE` from
the very sales fact it was being checked against. Agreement was guaranteed by
construction and proved nothing. Underneath: a "discount allowance" that was
`(TARGET_DISCOUNT - 0.1) * CURRENT_SHELF_PRICE` with manually set constants;
"fixed prices" inferred from behaviour (>9 orders, ≥75% discounted, ≥60% at the
modal price), not read from agreements; a 25-month "history" re-derived nightly
over a rolling window, so last March's figure changes with no transaction
changing. It shipped wrong to two live environments before it was caught.

Evidence: `docs/knowledge/concepts/2026-09-02-selco-fixed-prices-semantics.md`
and `2026-09-03-selco-portal-is-derived.md` in the analytics-agent repo; commit
`0933851` ("the portal is derived, not authoritative — correct three rules").

Pair it with the **base-rate trap** from the same programme: a discount reason
code on 925/926 (99.9%) of the cohort's lines looked like a perfect attribution
key, until the chain-wide base rate turned out to be 96% (879,405/915,919). In-
cohort rate proved nothing without the control.

### Other angles from the same build, each a possible section or a separate note

1. **The same question, three defensible answers.** "Most important customers"
   run three times → three reasonable methods; agreement with the client's own
   VIP list swung 3/15 → 2/15 → 8/15 on method alone. Then the twist: the
   client's list was not ground truth either — one nominee ranked about 8th on
   actual spend, and the nomination figures did not reconcile on any 12-month
   cut for two stores. (Wiki, 2026-07-09.)
2. **We deleted the fast path because it wasn't fast.** A router and a cheap
   route were built, measured live, and removed on 2026-06-12 when the "slow,
   thorough" path proved no slower and a better product. Every turn now takes
   the expensive road. (`docs/architecture.md`; AGENTS.md "no router or fast
   path".)
3. **Banning regex from an AI product.** AGENTS.md forbids keyword/pattern
   heuristics for anything semantic. Commit `c34aa67` deleted 124 and 92 lines
   of tokenizer-and-stopword matching from the interview and planner agents and
   replaced them with model decisions. The eval-routing carve-out ("CI plumbing,
   not agent logic") shows where the line sits. Also: prompt-injection
   containment by structural fencing with a per-turn nonce, explicitly because
   keyword scanning is forbidden.
4. **A distinct-count coincidence is not a grain proof.** "Daily snapshot, take
   the latest run date" would have silently dropped most of a 77.8M-row product
   dimension; `PRODUCT_ID` was exactly unique and `RUN_DATE` was the load batch.
   Testing the join took minutes. (JD Sports, 2026-09-09.)
5. **Three ways to lose a fix you already made.** (a) A trace-pairing fix for
   concurrent tool completions lived on an unmerged branch and had to be
   rediscovered five days later (`6e37b90`, guard test added). (b) A CRLF fix
   recorded in `.gitattributes` was never committed; it came back as
   `/bin/sh^M: bad interpreter` and every streaming request 502'd (`e3313e5`).
   (c) Lambda caps the API invoke policy at 20KB; five routes pushed it to
   20.8KB and rolled the stack back, the `ANY` workaround then swallowed the
   CORS preflight and returned 401 (`df60346` → `46d7e5f`). The cure caused the
   disease, twice.
6. **Where the time actually goes.** p50 turn ~106s, 85–90% of it sequential
   model rounds; SQL p50 1.7s. Opus: ~58s in 3 rounds, batching two queries.
   Sonnet: 70–101s across 4–6 rounds, one query at a time, plus an unnecessary
   step. Cheaper model, more rounds, no saving; stayed on Opus for trust.
   (`docs/knowledge/decisions/2026-06-24-production-review-p1-mitigations.md`,
   `2026-06-22-agentic-loop-stays-on-opus.md`.)
7. **A model version that got slower.** Opus 4.7 took 25–38s to answer "Hello"
   where 4.6 took ~4.5s; isolated with a bare `converse` probe, rolled back.
   (`2026-05-26-opus-46-investigation-orchestrator-rollback.md`.)
8. **The guardrail a CTE walked through.** `with x as (select customer_email as
   e ...) select e from x` passed a PII check that only inspected the outer
   SELECT. Found in code review, not production — that is the good version of
   the story. (`e647096`.)
9. **"Not in the warehouse" almost became a false negative.** A complete profile
   of one database "proved" two quantities did not exist; both were in a second
   Snowflake database no onboarding artefact mentioned. Rule now: `SHOW
   DATABASES` before declaring something absent.
10. **Two allowlists that must agree.** Describing a table in metadata without
    adding it to policy produces "the worst failure available: the agent plans
    confidently, then every query dies". Now a consistency test.
11. **How do you know the agent is right?** Keystone evals: 16/16 hand-graded,
    zero silent-wrong, all six trap questions beaten (Selco); 16/17 clean, one
    marginal (JD Sports). Evals live in `evals/` with fixtures and goldens.

### Figures available (verify before use)

p50 106s; SQL 1.7s; Opus 58s/3 rounds vs Sonnet 70–101s/4–6; 7-table vs 15-table
turn ~106s vs ~66s at ~$0.20; 20–30k cached vs 6–7.6k fresh tokens per turn;
77.8M product rows; 545M vs 80M sales lines (total vs loyalty); 99.98%
reconciliation; 3/15 → 2/15 → 8/15; 925/926 vs 96%; 20.8KB vs 20KB.

### Gaps only Thomas can fill

- What the build felt like from inside: the decision to keep the multi-agent
  orchestrator disabled rather than deleted; why single-tenant per account.
- Which client-specific details are genuinely sensitive versus merely named.
  The anonymisation map above is a suggestion.
- Whether "Ask HyperFinity" is the public name to use.
- The ending. The table tennis piece had one; this build is live and ongoing.

### Keep out

Client names without sign-off; anything that reads as HyperFinity marketing;
internal AWS account ids, ARNs, role names, or anything from the memory notes
that is operational rather than narrative.

---

## The IPL auction simulator

**Angle.** The LLM is the escalation path, not the system. A deterministic
bidding policy handles ~95% of in-lot decisions; the model fires only at
pressure moments (price near ~90% of private valuation, a rival going purse-
constrained, pool depletion) — 10–30 heavyweight calls per team per auction,
"tens of dollars, not thousands" (`docs/VISION.md`).

**Evidence.** CRPS against the real IPL 2025 mega-auction improving 241.06 →
232.9 → 230.5; Brier 0.244; spend MAE 813 → 789. The anonymised-vs-named
two-track backtest as a training-data-leakage control — the sharpest idea in the
repo and possibly its own note. Real 2025 data falsified a baked-in premium
(26/38 overseas spinners unsold). A fix that was correct and changed CRPS by
byte-for-byte nothing, written up as a null result.

**Honest limit.** As of the last commit (27 Jul 2026) nothing calls the real
API — Layer 3 has not run live. Say so.

**Gaps.** Why Fireworks/GLM rather than Bedrock; what happens next; whether the
persona-from-behavioural-priors approach held up.

---

## The village cricket club stack

**Angle.** Real software with real users who don't know it is software.
`cricket-graphics` generates matchday fixtures, lineups and performance cards,
themed via CSS, rendered through headless Chrome, and pushed to a digital sign.
A counterweight to the AI material.

**Gaps.** Which club (the local sweep found Oakworth CC paperwork; the repo's
vendored code says "Alleyn" — confirm). Who uses it and how often. Photos would
help and are the one place the site allows imagery (CLAUDE.md §7).

**Corrections to carry.** `pyplaycricket` is an unmodified fork of
`ewanharris12/pyplaycricket` — not yours, don't claim it. `raincalc` implements
one league's own rain rule (HCL Rule L 8(l)(iv)), not Duckworth–Lewis.
`similar-player-detector` is football, and appears to be an adapted template.

---

## Notes column — shorter pieces

- The outsiders finding from the table tennis log, if it wants a standalone
  note: edge widening to +25.5% ROI in the 5.00–8.00 band, then 2 winners from
  94 above 8.00.
- Items 1–11 above, any of which stands alone.
- Git as a ledger: 3,510 commits, 3,490 titled "committing files", and why that
  made a betting claim checkable when most are not.

---

## Status

| Piece | State |
| --- | --- |
| Table tennis | Published; two TODO gaps still in the page source |
| Ask HyperFinity build | Next. Evidence gathered above; prose not started |
| IPL auction simulator | Brief only; wait for Layer 3 to run live, or write it as a design piece |
| Village cricket stack | Brief only; needs club confirmation and photos |
