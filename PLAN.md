# PLAN — EnVar environmental-exposure microschema, first community draft

**Status:** draft for internal review, then community circulation.
**Companion documents:** [`SPEC.md`](SPEC.md) (the element-by-element specification), the worked records under [`tests/data/valid/`](tests/data/valid/) (with counter-examples in [`tests/data/invalid/`](tests/data/invalid/)), and the workshop materials under [`docs/workshop/`](docs/workshop/).
**Owner:** Nico Matentzoglu (EnVar implementation lead), TIS Lab (Haendel / Thessen), UNC.

---

## 1. Thesis — what this is and why

When an environmental-exposure value (a daily maximum temperature, a PM2.5 concentration) is geo-joined to a patient record, almost everything that makes the value *interpretable* is thrown away: which product it came from, at what grid resolution, under which day-boundary convention, through which interpolation, with what known biases. The OMOP common data model (the OHDSI standard for health records) and its proposed `external_exposure` table carry the value and a concept id; they cannot carry the rest. The result is that a downstream analyst — or a reviewer, or a meta-analyst pooling across sites — cannot reproduce or even correctly interpret the exposure from the data alone.

**EnVar's microschema is the sidecar that carries the rest.** It travels alongside the value (or value series) emitted by an upstream tool (Amadeus, DeGAUSS, …) and consumed by OMOP or another health-data layer. The design goal is sharp:

> **Provide just enough context that a result is reproducible from raw data plus metadata alone — without access to the analysis pipeline.**

This document is the plan for turning the existing prototype into a **community rally point**: a draft that domain experts can argue over along four axes — which elements are mandatory, which are needed for full reproducibility, which are nice-to-have, and whether anything is missing or poorly described.

The framing we put to the community is three tiers, which map onto Nico's original "minimum / ideal / theoretical-maximum" intuition:

| Tier | Question it answers | Slogan |
|---|---|---|
| **Core** | What must be present or the record is meaningless? | *the minimum* |
| **Recommended** | What is needed to actually reproduce the result? | *the ideal* |
| **Optional** | What enriches discovery and cross-linking but is not needed to reproduce? | *the theoretical maximum* |

The tier assignment in [`SPEC.md`](SPEC.md) is a **strawman authored to be challenged**, not a settled standard. The workshop exists to move elements between tiers and to surface what is missing.

---

## 2. Scope

**In scope for this draft:**

- **TMAX (daily maximum near-surface air temperature)** as the primary, fully-worked, fully-referenced variable.
- **PM2.5 (fine particulate matter mass concentration)** as a second worked example — chosen because it stresses different parts of the schema than heat does (machine-learning / satellite model types rather than interpolation; the annual-mean-vs-daily aggregation controversy; a different exposure-assignment story). PM2.5 demonstrates that the schema generalises beyond heat without committing us to the full 38-variable priority list yet.
- The **general `EnvironmentalExposureRecord` frame** and its component modules (variable identity, spatial reference, temporal reference, source dataset, exposure model, uncertainty, linkage, tool-run + provenance chain, derived-heat-metric, and the hooks for linking into a health-data layer — OMOP, BioData Catalyst, … — and for publishing as a FAIR — findable, accessible, interoperable, reusable — data deposit).
- Heat conceptual **layers 1–3** (physical state → derived index → person-day exposure) plus deterministic heat-wave flags (layer 4 where computable). See the heat primer for the layer model.

**Out of scope for this draft (named so reviewers know the edges):**

- The remaining 36 priority variables (air toxics, water contaminants, and environmental-justice / socioeconomic-status indices). The schema is designed to accept them; they are not worked here.
- Clinical / outcome metadata — the sidecar carries no protected health information and stops at the hooks that link it to the patient data; it never holds the patient data itself.
- Effect-modifying context — urban-heat-island intensity, air-conditioning access, area-level deprivation (heat layers 5–6). Downstream of this metadata layer.
- Building the production completeness checker and registry — those are demo deliverables, planned in §6, not built in this draft.

---

## 3. Method — how the element set was derived

Per the decision to **re-derive rather than rubber-stamp**, the element set in `SPEC.md` was built as follows:

1. **Re-derive from the source requirements.** The naked requirements in `niehs_standards/pipeline/heat-omop-slice/envar-heat-scenario-requirements.md` (70+ slots across 13 sections, each with a stated source-of-truth) and the conceptual model in `envar-heat-variable-primer.md` are the backbone.
2. **Ground each element in evidence.** Every Core and high-controversy element carries a reference (PMID / DOI / standard URL) justifying *why it must be captured* — see §5.
3. **Add PM2.5.** Extend the set with the elements PM2.5 needs that heat does not exercise (ensemble-ML model type, cross-validation R², averaging-window semantics, satellite retrieval provenance).
4. **Reconcile against the existing prototype.** The repository already contains a 13-module LinkML implementation. `SPEC.md`'s reconciliation appendix records, element by element, where the re-derived set **matches**, **adds to**, **drops from**, or **renames** the existing schema — so the prototype can be updated deliberately, not silently.

The reconciliation appendix is also where we surface the **one open design question the existing schema already flags**: whether the top-level record should use the LinkML Microschema Profile's abstract slot names (`subject`, `observation_type`, `location`, `temporality`, `methodology`, `observation_result`) or readable domain names (`variable_identity`, `spatial_reference`, …). The profile-conformant naming is a deliberate choice with documented adoption-friction costs; the workshop is the right venue to confirm or revisit it.

---

## 4. Tiering proposal (summary)

The full per-element tiering is in `SPEC.md`. The shape of the strawman:

- **Core** — variable identity essentials (`standard_name`, `units_ucum`, `value_data_type`), temporal semantics (`temporal_resolution`, `temporal_aggregation_method`, **`day_boundary_convention`**), spatial semantics (`native_spatial_resolution_m`, `crs`, `extraction_method`, `target_geography_type`), model class (`exposure_model_type`), source identity (`source_dataset_name` + `version`), and provenance minimum (`tool_name` + `version`, `provenance_id`, `schema_version`).
- **Recommended** — DOIs and citations, model paper + known biases, geocoder precision/score propagation, container image digest + input/output hashes, the full provenance chain, uncertainty fields, homogenisation status, calendar, plausible ranges.
- **Optional** — ontology IRIs (ECTO/ENVO), clinical codes (LOINC/SNOMED), ACDD passthrough, BibTeX, FAIR-deposit slots, run-log excerpts, DCAT distribution URL.
- **Conditionally-Core** — elements that are Optional in general but **mandatory in context**: for any derived heat metric, `equation_variant`, `indoor_outdoor` (WBGT), `heat_wave_threshold_definition`, `percentile_reference_period_{start,end}`; for PM2.5, the model-type and averaging-window elements; for a declared lagged or event-matched analysis, `clinical_date_assignment_convention` (the clinical-side day-boundary ruler that makes the Core `day_boundary_convention` checkable).

Two deliberate, defensible-but-arguable calls we want the community to ratify or overturn:

- **`day_boundary_convention` is Core.** It is the single most-omitted slot in the literature and a known source of cross-study disagreement (Daymet local-midnight vs PRISM 24h-ending-1200-GMT). Omitting it is precisely the reproducibility bug we are trying to kill, so we make it mandatory and invite the community to downgrade it if they disagree.
- **`equation_variant` and percentile-reference elements are Conditionally-Core.** Liljegren vs ACSM WBGT can differ by 2–3 °C; "95th percentile" over different reference periods flags different days. These are non-negotiable *for derived metrics*.

---

## 5. Reference / citation plan

The community asked (implicitly, via Nico's brief) for each element to be **validatable against a webpage or PMID**. Approach:

- **Now (this draft):** every Core element and every high-controversy element (day-boundary, WBGT equation variance, Heat-Index validity range, percentile-reference sensitivity, model-type-affects-uncertainty, PM2.5 averaging-window) carries a verified reference. References are verified to resolve (PubMed / doi.org / CrossRef / standards body) before inclusion; unverifiable claims are marked rather than dropped.
- **Scheduled (tracked task):** a **full per-element citation pass** extending verified references to every Recommended and Optional element, and across the remaining priority variables. This is deliberately deferred until after the community has weighed in on scope — citing 70 elements exhaustively before the community trims the set is over-investment (see the "absorptive capacity" risk, §10).
- Citations live **inline in `SPEC.md`** and are also encoded as `see_also` / annotation references on the LinkML slots, so the schema itself carries its evidence base.

> **Optional escalation:** a deeper multi-agent literature sweep (the `study` / Perplexity workflow) can be run for the full pass when scope is settled. It is not needed for the first community round.

---

## 6. Demo & evaluation strategy

Two phases, checker first.

### Phase 1 — Metadata completeness checker (built for the workshop)

A small `uv run`-able tool that takes a sidecar (optionally with its data file) and emits a **scored completeness report**:

```
Core         8/8   ✓
Recommended  5/9   ⚠   missing: source_dataset_doi, container_image_digest, ...
Optional     2/7
Reproducibility-readiness: 78%
BLOCKING (Core missing): day_boundary_convention
```

- Tiers are read **directly from the schema annotations** (the Approach-A single-source-of-truth decision), so the checker can never disagree with `SPEC.md`.
- It validates the instance against the LinkML schema, then classifies present/absent elements by tier and scores.
- It is the centrepiece of the workshop: run it live on the three TMAX scenarios and watch the score climb from minimum → ideal → maximal.

This aligns with two things the community already does: **C-HER's registration-time completeness gate** (a resource is not "metadata-complete" until required fields are filled) and **gaiaCatalog's required-vs-recommended split** (enforced with SHACL, a shape-validation language for graph data). The checker is the EnVar-native, tier-aware version of the same idea.

### Phase 2 — Mini registry (stretch)

A static, browsable page listing microschema-conformant sidecars with completeness badges — a mini gaiaCatalog. Useful for "show me conformant data" once there is conformant data to show. Sketched, not built, for the first round. The intended integration target is gaiaCatalog (LinkML can emit the Schema.org linked-data JSON — JSON-LD — that gaiaCatalog consumes), so the registry is a stepping stone, not a competing catalogue.

### The three scenarios per variable (example data)

Each scenario is one example sidecar + its data row, forming a **completeness gradient anchored in real pipelines**:

| Variable | ① Minimum | ② Ideal (full-reproducibility) | ③ Maximal (theoretical) |
|---|---|---|---|
| **TMAX** | Amadeus → GridMET 4 km (reflects today's free-text/hash metadata) | DeGAUSS → Daymet 1 km, point-at-residence | EnVar-enriched OMOP/GAIA deposit (ECTO/ENVO, ACDD, uncertainty, FAIR deposit) |
| **PM2.5** | EPA air-quality-monitor value, nearest-station | Di et al. ensemble machine-learning 1 km surface (model DOI, cross-validation R², biases, uncertainty) | ACAG / van Donkelaar satellite-derived, fully enriched deposit |

The passing gradient lives under `tests/data/valid/` (the `core` / `recommended` / `ideal` records per variable); the deliberately-incomplete `core_missing` cases live under `tests/data/invalid/` and fail validation — the "before" picture that motivates the schema.

---

## 7. Community evaluation session

**Goal:** move elements between tiers, find what's missing, and confirm descriptions are clear — producing the input for schema v0.2.

**Format:** a 60–90 minute structured working session, with an asynchronous pre-read so live time is spent on judgement, not exposition.

**Pre-read (sent ~1 week ahead):** `SPEC.md`, the two worked variables, the six scenario sidecars, and a sample checker report.

**Run of show:**
1. **Frame (10 min).** The reproducibility-from-metadata thesis and the three tiers. Use the workshop narrative in [`docs/workshop/narrative.md`](docs/workshop/narrative.md).
2. **Ground it (10 min).** Run the completeness checker live on the three TMAX scenarios — minimum → ideal → maximal — so the abstract tiers become a moving number on a real Daymet/Phoenix record.
3. **Walk TMAX module by module (30–40 min).** For each element, collect the **five questions** on a shared scoring sheet (one row per element):
   1. Is this **Core** (mandatory)?
   2. Is it **necessary for full reproducibility** (Recommended)?
   3. Is it merely **nice-to-have** (Optional)?
   4. Is it **well described**?
   5. Is **anything missing** around it?
4. **Generalisation check with PM2.5 (10 min).** Does the same frame hold for a non-heat variable? Where does it strain?
5. **Close (5 min).** Confirm the deltas and assign follow-ups.

**Capture mechanism:** a shared spreadsheet (one row per element, columns for the five questions and free-text), **or** one GitHub issue per module for asynchronous voting — chosen by audience preference. Either way the output is a structured per-element verdict.

**Output:** a tier-reclassification list + a missing-element list → folded into schema v0.2 and a revised `SPEC.md`.

**Invitees:** C-HER (Cole Brokamp, Kyle Messier, the Hanson team), the OHDSI GIS / gaia team, the Amadeus team, Anne Thessen and Melissa Haendel, and a slot for the GECC / EIRENE / NEXUS coordinating forum (Anne is already positioned as the standards-collector there). Domain experts read the sidecar literally — keep the live walk-through on real data, not abstractions.

---

## 8. Stakeholder alignment

| Stakeholder | What they care about | How this draft aligns |
|---|---|---|
| **C-HER (ORNL)** | Their ~25-table PostgreSQL metadata model, lineage with inheritable fields, registration-time completeness rules | The tiering + completeness checker mirror their completeness gate; the spatial/temporal/data-level elements are designed to map to their table-naming codes. Engagement window is open (Hanson requested meetings). |
| **OHDSI GIS / gaia** | `external_exposure` table, gaiaCatalog (Schema.org JSON-LD), SHACL required/recommended | The sidecar fills exactly the gaps `external_exposure` cannot carry; LinkML emits the JSON-LD gaiaCatalog consumes; the checker mirrors their SHACL split. |
| **Amadeus / NIEHS (Messier)** | Standardising Amadeus output for OMOP integration (Schmitt directive) | The TMAX minimum scenario *is* Amadeus-today; the schema is the metadata layer that lets Amadeus output land in OMOP. Build for the maintainer, not the first user. |
| **GECC / EIRENE / NEXUS** | "Linkage descriptors" — how a place-based exposure is assigned to a person | The `LinkageMethod` module is precisely this — now framed as one trajectory-resolution step spanning both axes: spatial (geocoding, residence/travel) and temporal (clinical-date assignment, partial-day attribution, lag). Anne carries materials into the forum. |
| **GA4GH exposomics** | ECTO-referenced environmental exposure blocks for Phenopackets | An `ECTO:` entry in the optional `concept_mappings` list is the hook. |

---

## 9. Milestones

| When | Milestone |
|---|---|
| Week 0 (now) | PLAN.md + SPEC.md + six scenario sidecars + workshop narrative drafted; internal review. |
| Week 1 | Completeness checker (Phase 1) working against the six scenarios; references for Core/controversial elements verified and inlined. |
| Week 2 | Pre-read circulated to invitees; logistics + scoring sheet set up. |
| Week 3 | Community evaluation session. |
| Week 4 | Schema v0.2 + revised SPEC reflecting the session; full citation pass scheduled. |

---

## 10. Risks

- **Absorptive capacity / over-specification.** 70+ elements is a lot for a NIEHS-adjacent team to maintain past the project. Mitigation: the Core tier is deliberately small; the workshop's job is to keep it small. Build for the second user (the maintainer), not the first.
- **Health-vocabulary gap.** 27–30 of 38 priority variables (including ambient TMAX and PM2.5 at most aggregations) lack OMOP concept ids. The schema handles this with `concept_status` + `target_concept_vocabulary` + null-with-reason rather than blocking on it — and is vocabulary-neutral, so the same mechanism covers BDC or any other health-data layer. The gap is real and not ours alone to close.
- **Profile-slot-naming friction.** The abstract top-level names cost domain experts their first-read clarity. Flagged as an explicit open question for the session (§3).
- **Citing ahead of scope.** Exhaustively referencing all 70 elements before the community trims the set wastes effort. Mitigation: cite Core/controversial now, defer the full pass (§5).
- **Registry scope creep.** The registry is a stretch; do not let it displace the checker, which is what actually drives the tiering discussion.

---

## 11. Open decisions

1. **Tier granularity** — keep "Conditionally-Core" as a visible fourth category, or fold it into per-element notes? (Currently visible.)
2. **Top-level naming** — profile-conformant abstract slots vs readable domain names? (Workshop question.)
3. **Capture mechanism** — shared spreadsheet vs GitHub-issue-per-module for the session?
4. **Full citation pass** — run the deep multi-agent `study` sweep, or hand-curate, once scope settles?
5. **Registry host** — standalone static site vs contribute completeness badges directly into gaiaCatalog?

> **Resolved (pre-circulation):** the placement of `lag_alignment_applied` — moved from `TemporalReference` to `LinkageMethod`, and the temporal twin of geocoding (`clinical_date_assignment_convention`, `partial_day_attribution_rule`) added there, modelling spatial + temporal linkage as one trajectory-resolution step (SPEC §4.8, §7.8). The top-level profile-vs-domain naming question (#2) remains open.
