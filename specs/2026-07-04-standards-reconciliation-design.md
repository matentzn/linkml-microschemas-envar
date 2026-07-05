# Standards-index reconciliation — design

**Date:** 2026-07-04
**Status:** Implemented (2026-07-04)
**Author:** Nico Matentzoglu

## 1. Problem

The standards index (`docs/standards-index/standards.yaml`, 32 entries) carries a
`reconciliation` field (`new` vs `already_catalogued`) meant to record whether each
standard was already catalogued in the prior niehs landscape work. Only 3 of 32 entries
are set; the other 29 defaulted to `new` with no cross-check. Separately, the synthesized
`surveys/study-env-exposure-metadata-standards/REPORT.md` still carries **6 `[SUSPECT]`
references** (404/DNS from deep-research). Neither blocks — the registry validates and tests
pass — but both leave the survey short of its quality bar.

## 2. Reconciliation source (corrected path)

The niehs inventory is at **`~/ws/notes/niehs_standards/surveys/_raw/relatedwork/projects_inventory.md`**
(NOT `surveys/projects_inventory.md` — the issue's path was wrong). Secondary source:
`~/ws/notes/niehs_standards/surveys/study-env-vars-health-outcomes/REPORT.md`. The inventory
names standards in its per-project "Standards/vocabularies" fields; a `grep` confirms real
signal (OMOP, FHIR, PROV, OGC, Schema.org, DeGauss, ISO 19115, DDI, DCAT all appear).

## 3. Decisions

- **`already_catalogued`** iff the standard is named (by name or unambiguous acronym) in
  `projects_inventory.md` or the study `REPORT.md`. Otherwise **`new`**.
- **`reconciliation_ref`** for `already_catalogued` points at the niehs source with a locating
  hint: `projects_inventory.md §<section> (<context>)` or `study REPORT.md (<context>)`. The two
  existing entries whose refs currently point at deep-research agent files (`omop-cdm`, `degauss`)
  are **re-pointed** to the niehs inventory, since `reconciliation` means "catalogued in the niehs
  work", not "mentioned by a survey agent". `dcat` already points correctly.
- **Scope: the 32 `entries` only.** The 51 `triaged` items (vocabularies/portals) are out of scope
  for this pass.
- **Suspect refs:** for each of the 6 `[SUSPECT]` references in `REPORT.md`, find a verified
  replacement URL (web check); if none exists, drop the reference and reword so nothing dangles.
  None are load-bearing, so no claim is lost.

## 4. Deliverables

- `standards.yaml` — all 32 entries carry a non-empty `reconciliation`; every `already_catalogued`
  entry carries a `reconciliation_ref`.
- `docs/standards-index/index.md` — regenerated (`just standards-index`); its reconciliation table
  now fully populated.
- `REPORT.md` — zero `[SUSPECT]` references.
- A new test `test_every_entry_has_reconciliation` making reconciliation completeness enforceable.

## 5. Verification

- `uv run linkml-validate -s docs/standards-index/standards_index.schema.yaml -C StandardsIndex docs/standards-index/standards.yaml` → clean.
- `uv run pytest tests/test_standards_index.py` → all pass (existing 4 + the new reconciliation test).
- `just standards-index` → regenerates cleanly.
- `grep -c '\[SUSPECT\]' surveys/study-env-exposure-metadata-standards/REPORT.md` → `0`.

## 6. Out of scope

- No new `entries`, no changes to `triaged`, no schema changes.
- No re-running of the deep-research survey.
- No deepening of `evidence` URLs beyond what a suspect-ref fix requires.
