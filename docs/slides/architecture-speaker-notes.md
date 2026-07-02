# Architecture deck — speaker notes (component slides)

Deliverable notes for the eleven **component** slides of `architecture.html`.
Each block: a spoken intro (**Say**), a bank of concrete **Examples** to make it land, and
a one-line **Punchline**. Read it all for ~45–60 s per slide; trim examples to hit ~12 min.

Running example throughout: the Phoenix cohort's daily-max temperature, **46.7 °C**, extracted
from **Daymet V4** via **DeGAUSS**.

---

## 01 · VariableIdentity — *core*

**Say:** "The bedrock: *what is actually being measured?* This component carries the cross-agency
identity of the quantity — its CF standard name, how it was summarised over time, and its units."

**Examples:**
- `standard_name: air_temperature` **+** `cf_cell_methods: time: maximum` = **Tmax**. The *same*
  standard name with `time: mean` is Tmean, and `time: minimum` is Tmin — the CF triple is the only
  thing that tells them apart.
- Units in UCUM: `Cel` vs `K` vs `[degF]`. A number without units is uninterpretable — and UCUM is
  what OMOP's `unit_concept_id` aligns to.
- `value_data_type`: `continuous_numeric` (temperature) vs `binary_flag` (extreme-heat-day yes/no) vs
  `count` (consecutive heat days). It tells the consumer whether to *average* it or *count* it.
- `concept_status: gap` — there is **no OMOP concept id** for ambient Tmax today. That gap is
  *recorded*, not hidden. (PM2.5 would be `proposed`.)

**Punchline:** "The CF triple is what stops a daily *max* from being silently pooled with a daily *mean*."

---

## 02 · DataLayout — *core*

**Say:** "The values live in a companion CSV or parquet file, not in the sidecar. This component is
the map between the two — which column carries the values, which the subject, which the date."

**Examples:**
- `table_orientation: wide` (a `tmax` column per variable) vs `long` (one shared `value` column,
  rows discriminated by a `variable` column — tidy format). Every other binding is read relative
  to this flag.
- `value_column: tmax` — the record carries **no inline observation result**; without this binding
  the sidecar describes values nobody can find.
- `subject_column: subject_id` / `time_column: date` — what lets the values be joined back to
  people and aligned with clinical dates.
- `value_uncertainty_column: tmax_stderr` — Daymet ships per-value standard errors that most
  pipelines silently drop; naming the column keeps them attached.

**Punchline:** "Identity says *what* the variable is; layout says *where in the file* its values are. Split on purpose."

---

## 03 · SpatialReference — *core*

**Say:** "Where on Earth the value sits — and how a *grid cell* became a *single point* value."

**Examples:**
- `native_spatial_resolution_m`: `1000` (Daymet) vs `~4000` (GridMET) vs `~32000` (NARR). A 32 km
  value at someone's house means something very different from a 1 km value.
- `crs: EPSG:4326` — without the coordinate system you can't even place the grid on the Earth correctly.
- `extraction_method`: `nearest_cell` vs `inverse_distance_weighted_4_nearest_cells` vs
  `area_weighted_polygon_mean` vs `population_weighted_mean`. **The same point gets a different value
  under each rule.**
- `target_geography_type`: `point_residence` vs `census_tract` vs `zcta` vs `county`. Mixing a point
  value and a tract value in the same column is a known, silent error.

**Punchline:** "Resolution + extraction method is the single biggest lever turning a map into a person's exposure."

---

## 04 · TemporalReference — *core*

**Say:** "Over what window, aggregated how — and under *which definition of a day*."

**Examples:**
- `temporal_resolution`: `daily` vs `hourly` vs `monthly` vs `annual`.
- `temporal_aggregation_method`: `maximum` vs `mean` vs `minimum`. "Daily max" and "daily mean" are
  *different exposures* with different health associations.
- `day_boundary_convention`: `local_midnight` (Daymet) vs `24h_ending_1200_GMT` (PRISM). The same hot
  afternoon lands on **different calendar days** — this is the single most-omitted field in the heat
  literature, and why two honest studies can disagree.
- `calendar`: `gregorian` vs `noleap` / `360_day` — matters when the source is climate-model output;
  misalignment shifts the daily values.

**Punchline:** "The field that quietly breaks cross-study comparison — that's why it's Core."

---

## 05 · SourceDataset — *core*

**Say:** "The identity of the upstream product the values originate from — name **and version**."

**Examples:**
- `source_dataset_name` / `source_dataset_short_code`: *Daymet V4* / `daymet_v4`; version `"V4 R1"`.
- **Version is not cosmetic:** ACAG PM2.5 **V5 vs V6** changes the numbers. A value without a version
  is simply not reproducible.
- `source_dataset_doi: 10.3334/ORNLDAAC/2129` is the durable handle; `source_license_spdx`
  (`public-domain-us-gov` vs `CC-BY-4.0`) governs whether you can redistribute it.
- `source_homogenisation_status`: GHCN-Daily is **not** homogenised — using it for trend work without
  saying so is a documented trap.

**Punchline:** "'Daymet' isn't enough. 'Daymet V4 R1' is."

---

## 06 · ExposureModel — *core*

**Say:** "How the values were produced — the model class, its inputs, and its known biases."

**Examples:**
- `exposure_model_type`: `direct_measurement` (a monitor) vs `spatial_interpolation` (Daymet) vs
  `reanalysis` (ERA5) vs `ensemble_machine_learning` (Di PM2.5) vs `satellite_retrieval`. These have
  **different error structures and cannot be pooled naively.**
- `exposure_model_paper_doi`: the methods paper — Daymet (Thornton 2022), GridMET (Abatzoglou 2013).
  The reproducibility anchor for *how* the value was made.
- `exposure_model_cross_validation_r2`: Di et al. PM2.5 reports **0.86** — the single most useful
  one-number quality signal for a modeled product.
- `exposure_model_known_biases`: Daymet's warm-season warm bias; an ML surface that smooths away
  high-concentration peaks. The field reviewers care about most.

**Punchline:** "A measured value and an ML-predicted value at the same place are not interchangeable."

---

## 07 · Uncertainty — *recommended*

**Say:** "Per-value and whole-model uncertainty, quality flags, and how gaps were filled."

**Examples:**
- `per_value_uncertainty_field_name: tmax_stderr`, `per_value_uncertainty_type: standard_error` (vs
  `prediction_interval_<n>_pct`, `ensemble_std_dev`). Daymet ships a per-cell standard error that most
  pipelines silently drop.
- `model_aggregate_uncertainty`: `cv_r2` / `cv_rmse` — the whole-model summary.
- `missing_data_handling_method`: `spatiotemporal_interpolation` vs `forward_fill` — how, say,
  snow-covered Daymet pixels were filled. Usually invisible downstream.
- `data_completeness_pct`: `100` vs `78` — what fraction of (location, date) cells actually had a value.

**Punchline:** "Recommended, not Core — you *can* reproduce without it, but you won't know how much to trust the number."

---

## 08 · LinkageMethod — *core*

**Say:** "How a place-based value was attached to a patient location — the join itself."

**Examples:**
- `linkage_strategy`: `point_extraction_at_residence` vs `buffer_aggregation_around_residence` vs
  `nearest_station_with_max_distance` vs `population_weighted_area_to_residence`.
- `geocoding_precision_propagated` (`range`/`street`/`zip`/`city`) + `geocoding_score_propagated: 0.95`
  — rural addresses geocode coarser; ignoring that gives **differential exposure misclassification**.
- `linkage_max_distance_to_station_m`: beyond it the nearest-station assignment is meaningless and
  should be **null**, not a number.
- `address_period_alignment`: `single_static_address` vs `address_history_from_emr`.

**Punchline:** "This is the 'linkage descriptor' the GECC/EIRENE forum calls the central gap — how a place becomes a person."

---

## 09 · ToolRun + ProvenanceChain — *core* (chain: *recommended*)

**Say:** "The exact invocation that produced the value — plus the ordered upstream runs, patterned on W3C PROV."

**Examples:**
- `tool_name: daymet`, `tool_version: 1.0.0`. Reproducibility is impossible without knowing which tool
  version ran.
- `container_image_digest: sha256:a8b3c2…` — the strongest reproducibility anchor, because it pins the
  *exact* image, not a mutable tag.
- `input_file_sha256` / `output_file_sha256` let someone re-run and confirm identical bytes;
  `input_row_count` / `output_row_count` are a cheap integrity check.
- `provenance_chain`: `geocoder 3.3.0 → daymet 1.0.0`, terminating at `raw_source_download`. A
  connected DAG with no orphan steps — if the geocoder version changed, the coordinates (and the cell)
  could move.

**Punchline:** "It pins the exact execution — not 'Daymet' in the abstract."

---

## 10 · DerivedHeatMetric — *conditionally-core*

**Say:** "Present **only** when the variable is a derived heat index — the equation, indoor/outdoor, and
the percentile baseline. For plain Tmax this whole module is omitted."

**Examples:**
- `heat_metric_family`: `wbgt_outdoor` vs `heat_index` vs `utci` vs `heat_wave_flag`.
- `equation_variant`: `liljegren_2008` vs `acsm_simplified` vs `bernard_simplified` — WBGT
  approximations diverge **well beyond 2–3 °C** from the reference model in hot-humid conditions.
- `equation_validity_range`: the Rothfusz Heat Index is **undefined below ~80 °F / 40 % RH** — used
  outside that range it produces nonsense.
- `heat_wave_threshold_definition` + `percentile_reference_period_start/end`: "95th percentile of
  **1971–2000**" vs "**2000–2019**" flags *different days* in a warming climate. At least seven
  heat-wave definitions are in use, none convertible after the fact.

**Punchline:** "Irrelevant for Tmax; non-negotiable for a WBGT or a heat-wave flag. That's what 'conditionally-core' means."

---

## 11 · HealthLayerLinkage + DepositMetadata — *recommended* (deposit: *optional*)

**Say:** "The forward-facing hooks: how the record links into the health-data layer, and what it needs
to travel as a FAIR deposit."

**Examples:**
- `health_layer_target: omop_external_exposure` + `health_layer_link_field: exposure_source_value`
  — names the downstream health-data layer and the field in it that carries the sidecar's
  `provenance_id`, so a per-person exposure row can link **back** to all this metadata (no single
  health-data model is privileged — BDC is another target).
- `phi_status: no_phi` — the safety assertion. (It actually lives at the record root and is **Core**;
  by design the sidecar is PHI-free.)
- `deposit_doi: 10.5281/zenodo.…`, `deposit_license_spdx: CC-BY-4.0`, `dcat_distribution_url: …` —
  the subset needed to publish the record as a citable FAIR object. **Optional**, because most records
  never get deposited.

**Punchline:** "The hooks that point forward — into OMOP, and into a published deposit."

---

## Appendix — record-root scalars (not a component, but on every record)

Three scalars sit directly on `EnvironmentalExposureRecord`, all **Core**:

- `schema_version` — which schema version this sidecar targets; downstream branches on it.
- `provenance_id` — the sidecar's stable id (ULID); this is what OMOP's `exposure_source_value` holds.
- `phi_status` — `no_phi` | `aggregated_no_phi` | `phi_present`; the PHI-free safety assertion.

**One-liner if asked:** "These three are the record's own identity card — version, stable id, and the
promise that it carries no PHI."
