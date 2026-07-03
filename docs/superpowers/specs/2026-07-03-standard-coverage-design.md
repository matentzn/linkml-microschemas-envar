# Standard-coverage design — answering "why not use X?"

**Date:** 2026-07-03
**Status:** Approved design, pending implementation plan
**Author:** Nico Matentzoglu

## 1. Problem

EnVar is repeatedly asked *"isn't this the same as X?"* — where X is GAIA, DeGAUSS,
Amadeus, C-HER, or the CODATA Essential Variables / CDIF work. We need to answer
**"why not just use X?"** *specifically*: for each standard, what does it carry, what
does it fail to carry that EnVar needs, and therefore where it falls short of
instance-level reproducibility. The immediate secondary use is **gap analysis** —
which EnVar slots no existing standard supplies (EnVar's novel contribution) versus
which are table stakes. Later, we want real **mappings/crosswalks**, both to validate
the coverage claims and to check data produced in a foreign file format against the
EnVar requirements.

`docs/related-approaches.md` already makes this argument in prose and with a
hand-authored matrix. The sibling repo `~/ws/projects/EnVar` already has a working
three-way example pipeline (`examples/heat/{degauss,amadeus,omop-gaia}`) that emits
real sidecars and auto-generates per-slot coverage reports (`COVERED.md`/`GAPS.md`)
via `envar-utils`, plus a hand-written `COMPARISON.md`. What is missing is a
**single, authoritative, machine-queryable record of coverage that lives with the
schema, covers all five standards (including the conceptual ones), and stays in sync
as the schema evolves.**

## 2. Considered approaches

Three approaches were on the table. They are **not competitors** — they are three
layers of the same thing at different cost and fidelity, and the design sequences
them rather than choosing one.

1. **linkml-map crosswalks with reverse-engineered source schemas.** Machine-actionable
   and runnable, but requires guessing a source LinkML schema from example files, and
   **structurally cannot represent C-HER or CODATA/EV**, which emit no per-value
   instances. Highest cost, narrowest fit. → deferred to a later layer.
2. **Example library + mapping scripts.** Already substantially built in
   `~/ws/projects/EnVar` for three of five standards; strong, concrete evidence.
   Still cannot represent the conceptual standards, and is tied to an older schema
   version that has drifted from this repo. → becomes the *evidence* layer.
3. **Curated `covered_by` metaslot annotations + a generator.** Cheap, complete,
   covers all five standards including conceptual ones, reuses the existing
   tier-scoring machinery in `checker.py`, and generates an always-in-sync matrix.
   → **the authoritative spine, built first.**

**Chosen path:** Approach 3 is the authoritative core. Approach 2 supplies verified
evidence for the standards that emit instances. Approach 1 is the eventual crosswalk
built on top of Approach 2. This ordering is what answers "why not X?" for *all five*
standards, dodges the "fake source schema" problem (annotate first, map later only
where it pays off), and is honest by construction (asserted vs verified).

### Settled decisions
- **Location:** local annotations in this repo's `src/.../schema/*.yaml`; generator
  next to `checker.py`; evidence links point out to `~/ws/projects/EnVar`. No
  metamodel change to `linkml-microschema-profile` for now.
- **Granularity:** per-slot, **Core + Recommended** tiers first; Optional deferred.

## 3. Data model — the `covered_by` annotation

On each Core and Recommended slot, extend the existing `annotations:` block (which
already carries `tier` / `justification` / `explanation`) with a `covered_by` payload
holding one entry per standard. Standards keyed by short id:
`gaia`, `degauss`, `amadeus`, `cher`, `codata`.

Each entry records:

| Field | Meaning |
|---|---|
| `extent` | controlled vocabulary (below) — the core judgment |
| `status` | `verified` (a runnable example emits it) or `asserted` (curated judgment) |
| `where` | concrete column / file / slot in the standard's output (grep target) |
| `evidence` | pointer to the example/crosswalk in `~/ws/projects/EnVar` (for `verified`) |
| `note` | short free text |

### `extent` controlled vocabulary
- **`full`** — carried first-class on a stable column / named slot / standard file.
- **`partial`** — present but only embedded or free-text; recoverable, not first-class
  (COMPARISON.md's ➖).
- **`absent`** — the standard operates at this layer but does not carry the field (❌).
- **`out_of_layer`** — N/A *by design*: the standard operates at a different layer
  (CODATA/EV at the conceptual layer; GAIA at the dataset layer for run-specific
  fields). **Not a failure**, and **excluded from that standard's score denominator.**

### Technical risk to retire first (implementation step 1)
LinkML generators must tolerate this annotation without `gen-project` errors — the
same class of risk as the 2026-07 `alias` spike documented in the schema README.
The first implementation step is a TDD spike: add **one** `covered_by` entry, run
`just gen-project`, confirm the whole generator pipeline (JSON Schema, SHACL, OWL,
Java, TypeScript, Pydantic, dataclasses) stays clean, and confirm `SchemaView` can
read the value back in the shape the generator expects. If a nested value breaks any
generator, fall back to flat annotation keys
(`coverage_degauss_extent:`, `coverage_degauss_where:`, …). **Serialization is settled
empirically, not guessed.**

## 4. The generator — `coverage.py` (sibling to `checker.py`)

Reuses `checker.py`'s slot-walk (every tier-annotated slot reachable from
`EnvironmentalExposureRecord`, counted once per slot name) and its tier weighting.
For the five standards it emits three artifacts:

1. **Coverage matrix** — slots × standards, tier-grouped, glyphs
   (`full`/`partial`/`absent`/`out_of_layer`) plus the `where` reference. A generated,
   always-in-sync replacement for the hand-authored COMPARISON.md.
2. **Per-standard "WHY NOT X?" scorecard** — the payoff. Treat that standard's `full`
   and `partial` slots as *present*, run the existing tiered readiness formula
   (`100·(0.5·core_frac + 0.4·recommended_frac + 0.1·optional_frac)`), and list the
   missing Core slots as BLOCKING. Produces sentences like *"DeGAUSS alone scores ~45%
   EnVar-readiness, BLOCKED on exposure_model_type, uncertainty,
   day_boundary_convention."* `out_of_layer` slots leave that standard's denominator
   so no standard is faulted for a layer it never claimed. `partial` counts as present
   but is flagged.
3. **Inverse gap analysis** — slots that *no* standard covers (EnVar's novel
   contribution) versus slots *every* standard covers (table stakes). This is the
   gap-analysis secondary use, for free.

Every rendered value carries a `verified`/`asserted` badge so the argument never
overclaims. Asserted C-HER/CODATA scores must be visibly marked so a reviewer cannot
read a manufactured low score into a standard that was never trying to play at the
instance layer.

### Scoring honesty rules
- `full`, `partial` → present (partial flagged).
- `absent` → missing (counts against the score).
- `out_of_layer` → removed from the denominator for that standard.

## 5. Output surface

- New generated `docs/coverage/` (matrix + per-standard scorecards) behind a
  `just coverage` recipe (project-specific recipes live in `project.justfile`).
- `docs/related-approaches.md` remains the **hand-authored narrative** and links to the
  generated evidence. Prose makes the argument; generated tables prove it.

## 6. First-pass scope

- **Standards:** GAIA, DeGAUSS, Amadeus, C-HER, CODATA/Essential Variables.
- **Slots:** Core + Recommended only.
- **Seed data:**
  - DeGAUSS / Amadeus / GAIA `verified` entries lifted from the existing
    `~/ws/projects/EnVar/examples/heat/COMPARISON.md` and `omop-gaia/envar/COVERED.md`.
  - C-HER `asserted` from `~/ws/notes/niehs_standards/surveys/_raw/relatedwork/projects_inventory.md §3.2`
    (limited public documentation of formats — most entries will be `absent`/`asserted`
    or `out_of_layer`).
  - CODATA / EV `asserted` from `docs/related-approaches.md §4` (conceptual layer —
    most instance-level slots are `out_of_layer`, not `absent`).

## 7. Explicitly deferred (documented, not built now)

- **Approach 2 wiring.** Reconcile the schema drift between the EnVar-repo examples
  (old `observation_type` / `variable.name` / `cf_standard_name` naming) and this
  repo's current `variable_identity` / `data_layout` naming, so `evidence:` links
  resolve and COVERED.md-style reports regenerate against the live schema.
- **Approach 1 crosswalks.** Build real source LinkML schemas + linkml-map for
  degauss / amadeus / gaia, upgrading those `covered_by` entries `asserted → verified`
  and unlocking foreign-format *validation* ("check data produced in a different file
  format").

## 8. Success criteria

- Every Core and Recommended slot carries a `covered_by` entry for all five standards.
- `just gen-project` stays clean with the annotations present.
- `just coverage` regenerates the matrix, the five scorecards, and the inverse gap
  analysis from the schema alone, with verified/asserted clearly distinguished.
- The output answers, in one number plus a specific slot list, *why each standard is
  insufficient on its own* — without contradicting `checker.py` (shared slot universe
  and tier weighting).

## 9. Out of scope

- No changes to `linkml-microschema-profile`.
- No Optional-tier annotations in this pass.
- No runnable crosswalks or foreign-format validation in this pass.
- No reconciliation of the EnVar-repo example schema drift in this pass.
