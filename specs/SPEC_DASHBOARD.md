# SPEC — EnVar completeness dashboard (static)

**Status:** draft for the workshop. A first, static implementation lives at
[`docs/dashboard/index.html`](../docs/dashboard/index.html) and is wired into the
mkdocs site so it renders alongside the generated LinkML element docs.
**Companion documents:** [`PLAN.md`](../PLAN.md) §6 (demo & evaluation strategy),
[`SPEC.md`](../SPEC.md) (the element-by-element tiering it visualises).

---

## 1. What it is

A single, static, dependency-free HTML page that turns the abstract tiering of
[`SPEC.md`](../SPEC.md) into **a moving number on real records**. Each row is one
microschema-conformant sidecar (some authored by us, some that *reference*
external products and are ETL'd into the microschema shape). The page is the
browsable, table-shaped face of the metadata-completeness checker described in
`PLAN.md` §6 — it shows the score climb from **minimum → ideal → maximal**.

It is **not** the checker engine. The checker (a `uv run` tool, not yet built)
reads the tier annotations from the schema and scores an instance. The dashboard
consumes the checker's output. Until the checker exists, the per-row scores are
**precomputed and embedded** in the page (clearly marked as illustrative).

## 2. Scope of this draft

- **Three rows**, the worked TMAX completeness gradient:
  1. `tmax_01` — Amadeus → GridMET 4 km (the "before" picture: free-text + hashes)
  2. `tmax_02` — DeGAUSS → Daymet 1 km, point-at-residence (full reproducibility)
  3. `tmax_03` — EnVar-enriched OMOP/GAIA deposit (ECTO/ENVO, ACDD, FAIR deposit)
- The PM2.5 gradient and additional referenced products are **out of scope** for
  this draft but the data model below accepts them with no code change.

## 3. Data model (one object per row)

The page reads an embedded `SCENARIOS` array. Each entry:

| Field | Meaning |
|---|---|
| `id`, `rank`, `tier` | stable id; sort order; tier label (Minimum / Ideal / Maximal) |
| `variable`, `title` | `TMAX`; human title (`Amadeus → GridMET 4 km`) |
| `pipeline`, `source` | emitting tool; upstream product |
| `resolution`, `dayBoundary`, `value`, `date` | headline interpretable facts (a null `dayBoundary` is rendered as a gap) |
| `scores` | `{ core:[got,of], recommended:[…], optional:[…] }` |
| `readiness` | reproducibility-readiness %, see §4 |
| `blocking` | list of Core slots missing (drives the BLOCKED stamp) |
| `modules` | per-module `{ name, state: full\|partial\|absent, note }` for the drawer |

When the real checker lands, this array is generated from its JSON report;
the page does not change.

## 4. Scoring

- **Tier meters** show `got / of` as a segmented bar. Denominators are the
  TMAX-relevant slot counts (heat-metric- and PM2.5-only slots excluded), aligned
  with the example report in `PLAN.md` §6 (Core 8, Recommended 9, Optional 7).
- **Reproducibility-readiness** is a single weighted roll-up:
  `readiness = 100 · (0.5·core_frac + 0.4·rec_frac + 0.1·opt_frac)`.
  Core is weighted highest because Core gaps block reproduction outright.
- **BLOCKED stamp.** If any Core slot is missing, the row is stamped `BLOCKED`
  regardless of readiness %, mirroring the checker's `BLOCKING` behaviour and
  the C-HER registration-time completeness gate.

## 5. Visual design

Deliberately distinct from the rare-disease dashboard (dark-blue gradient + card
list): a **warm editorial "lab-ledger"** — cream paper, ink serif display type,
and a **thermal accent ramp** (cool → ember) for the meters, fitting a
temperature variable. Layout is a dense, sortable **table** with expandable
per-row drawers, not cards. Self-contained: inline CSS/JS, fonts from Google
Fonts CDN with graceful serif/sans fallback offline.

## 6. Integration

- Self-contained file at `docs/dashboard/index.html`; added to the mkdocs `nav`
  so it sits beside `Schema` (the generated element docs). Reviewers browse the
  ledger and the element reference in one site.
- The page links each row back to its sidecar under `examples/scenarios/tmax/`
  and to the relevant `SPEC.md` tier.

## 7. Not in this draft (named so reviewers know the edges)

- The checker engine (scores are embedded, not computed).
- PM2.5 rows and external referenced products (model accepts them; not authored).
- Live filtering/search beyond tier (the rare-disease faceted filter rail is
  overkill for a handful of rows; revisit when the registry grows — `PLAN.md` §6 Phase 2).
