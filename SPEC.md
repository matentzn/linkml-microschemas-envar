# SPEC — EnVar environmental-exposure microschema (TMAX + PM2.5), v0.1 draft

**Status:** draft for community review. The tier assignments below are a **strawman authored to be challenged** — see [`PLAN.md`](PLAN.md).
**Companion data:** the worked sidecars under [`tests/data/valid/`](tests/data/valid/) — a `core` → `recommended` → `ideal` gradient per variable, all passing validation — plus the `core_missing` counter-examples under [`tests/data/invalid/`](tests/data/invalid/) showing what an incomplete (invalid) record looks like.
**Scope:** TMAX (daily maximum near-surface air temperature) fully worked; PM2.5 (fine particulate matter) as a generalisation check. The general `EnvironmentalExposureRecord` frame underlies both.

Every Core element and every high-controversy element below carries a **verified** reference (PubMed / DOI / standards body). References are listed by short key inline and resolved in full in §10. Structural elements whose justification *is* a standard (units, CRS, vocabularies) cite that standard as their source of truth.

---

## 1. What this specifies

A **sidecar**: a structured metadata document that travels alongside an environmental-exposure value (or value series) emitted by an upstream tool (Amadeus, DeGAUSS, …) and consumed by a health-data layer (the OMOP common data model's `external_exposure` table, BioData Catalyst, …). The sidecar carries no protected health information (PHI); it stops at the hooks that link it to the patient data and never carries the clinical data itself.

The design goal governs every element decision:

> **A result must be reproducible from raw data plus this metadata alone — without access to the analysis pipeline.**

An element earns its place only if its absence would block reproduction, correct interpretation, or discovery. The three tiers (§3) record *how much* it blocks.

---

## 2. The data model

One exposure record composes a graph of typed objects, one module per concern. A module may be omitted when not applicable (e.g. `DerivedHeatMetric` for a non-heat variable) without breaking validation.

| Module | Concern | Cardinality |
|---|---|---|
| `EnvironmentalExposureRecord` | Top composite; identity + links to the value(s) | one per (variable, run) |
| `VariableIdentity` | What physical quantity, in what units, bound to which vocabularies | one per record |
| `DataLayout` | Column bindings from the sidecar into the companion data file (value / subject / time / uncertainty / QA columns) plus wide-vs-long orientation | one per record |
| `SpatialReference` | Native grid, CRS, extent, extraction footprint | one per record |
| `TemporalReference` | Resolution, aggregation, day-boundary convention, coverage | one per record |
| `SourceDataset` | The upstream product the values originate from | one per record |
| `ExposureModel` | Model class, equation, inputs, known biases | one per record (null for direct measurement) |
| `Uncertainty` | Per-value and aggregate uncertainty, quality flags, missing-data handling | one per record |
| `LinkageMethod` | How a gridded value is attached to a patient's location *and* clinical date (spatiotemporal trajectory resolution) | one per record |
| `ToolRun` + `ProvenanceChain` | Exact invocation + the ordered chain of upstream runs | one per record |
| `DerivedHeatMetric` | Equation variant, indoor/outdoor, percentile baseline (heat indices only) | where applicable |
| `HealthLayerLinkage` + `DepositMetadata` | Health-data-layer findability hooks (OMOP, BDC, …; no single model privileged) + the subset needed to publish as a FAIR (findable, accessible, interoperable, reusable) data deposit | one per record |

Naming note: the top-level keys use **readable domain names** (`variable_identity`, `spatial_reference`, `temporal_reference`, `exposure_model`), and the schema now matches: each maps to its LinkML Microschema Profile anatomy slot (`observation_type`, `location`, `temporality`, `methodology`) via slot-level `implements`/`exact_mappings` — `instantiates` conformance does not constrain slot names. Decided 2026-07; rationale and mechanism in the schema README.

---

## 3. Tier legend

Tiers are **machine-readable annotations on the LinkML slots** (the single-source-of-truth decision in `PLAN.md` §1), so the completeness checker reads them directly and can never disagree with this document.

| Tier | Meaning | Checker behaviour |
|---|---|---|
| **Core** | The record is meaningless or non-reproducible without it. | Missing → **BLOCKING** |
| **Recommended** | Reproducible in principle without, but real reproduction needs it. | Missing → ⚠ warning |
| **Optional** | Enriches discovery / cross-linking, not reproduction. | Missing → noted, not penalised heavily |
| **Conditionally-Core** | Optional in general, **mandatory in a stated context** (e.g. derived heat metrics, percentile thresholds). | Missing *in context* → **BLOCKING** |

**Null with reason.** Every nullable element, when null, must carry a `*_missing_reason` from the controlled vocabulary: `not_provided_by_source`, `available_but_not_extracted`, `upstream_data_not_propagated`, `under_investigation`, `not_applicable`. A blank is a bug; a null-with-reason is information. (This lifts the CF `_FillValue`-with-reason pattern to the metadata layer.)

---

## 4. TMAX — worked element by element

Columns: **Element** · **Tier** · **Type / vocabulary** · **Definition & why it must be captured** · **Ref**. Example values are in [`tests/data/valid/`](tests/data/valid/).

### 4.1 `VariableIdentity`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `variable_name` | Core | string | The short machine name of the variable as the upstream tool emitted it (`tmax`, `tmmx`). Pure identity — locating the values in the data file is `DataLayout.value_column`'s job (§4.11), so this stays meaningful even when the file is long-format and the value column is literally named `value`. | tool |
| `variable_label` | Recommended | string | Human-readable label. Disambiguates for a reader; not machine-critical. | — |
| `standard_name` | Core | CURIE | The cross-agency identifier for the physical quantity, as a prefixed CURIE so no single naming authority is baked into the slot. Use a CF Standard Name where one exists (`CF:air_temperature`); for health-relevant quantities CF never defined (Heat Index, WBGT) mint a project term (`ENVAR:heat_index`) or reuse an ontology term. The prefix carries the authority. Without it the variable is not interoperable. | [CF] |
| `cf_cell_methods` | Core | CF cell_methods | How the value summarises sub-period values; `time: maximum` is what makes this *Tmax* rather than Tmean. Omitting it loses the distinction between a daily max and a daily mean. | [CF] |
| `units_ucum` | Core | UCUM | Units in UCUM syntax (`Cel`). A number without units is uninterpretable; UCUM is what OMOP's `unit_concept_id` aligns to. | [UCUM] |
| `units_display` | Optional | string | Pretty-printed units (`°C`). Cosmetic. | — |
| `value_data_type` | Core | enum | `continuous_numeric` \| `categorical` \| `binary_flag` \| `count` \| `event_marker`. Tells the consumer whether to average it or count it. | EnVar |
| `target_concept_vocabulary` | Recommended | string | The downstream health-data vocabulary `target_concept_id`/`concept_status` refer to (e.g. `omop`, `bdc`). Names the vocabulary so the schema privileges no single health-data layer. | EnVar |
| `target_concept_id` | Recommended | string (null+reason) | Concept id in `target_concept_vocabulary` (e.g. an OHDSI concept id). Ambient Tmax has **no OMOP concept today**, so this is usually null with reason — but recording the attempt matters. | [Athena] |
| `concept_status` | Core | enum | `existing` \| `proposed` \| `gap`. Makes the vocabulary gap explicit rather than silent; a downstream system must know whether to expect a concept id. | EnVar |
| `concept_mappings` | Optional | list of CURIEs | One generic cross-reference list instead of a slot per standard, so adding a vocabulary is a new prefix, not a schema change. Holds ECTO (`ECTO:0000012`, cross-ontology alignment), ENVO (material/process), and LOINC/SNOMED clinical codes where applicable. Enrichment, not needed to reproduce the value. The *primary* health-data binding with its gap status stays in `target_concept_*`. | [ECTO]/[ENVO]/[LOINC]/[SNOMED] |
| `value_range_plausible_min`/`max` | Recommended | float | Physical sanity bounds (−50 / 60 °C). A cheap guard against unit-conversion and sentinel-value errors. | domain |

### 4.2 `SpatialReference`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `native_spatial_resolution_m` | Core | number | Native grid spacing (Daymet 1000, GridMET ~4000, NARR ~32000). Exposure misclassification scales with cell size; a 32 km value at a residence means something very different from a 1 km value. | source |
| `native_spatial_resolution_descriptor` | Recommended | string | Human label (`"1 km regular grid"`, `"point station"`). | source |
| `crs` | Core | EPSG / PROJ | Coordinate reference system (`EPSG:4326`). Without it the grid cannot be located on the Earth correctly. | [EPSG] |
| `spatial_extent_bbox` / `spatial_extent_descriptor` | Recommended | array / string | Product footprint. Distinguishes "no value here" (outside extent) from "missing value". | source |
| `extraction_method` | Core | enum | `nearest_cell` \| `bilinear` \| `inverse_distance_weighted_4_nearest_cells` \| `area_weighted_polygon_mean` \| `population_weighted_mean` \| `point_station_lookup`. The single biggest lever in turning a grid into a person value; different methods give different exposures at the same point. | EnVar; [Brokamp2018] |
| `extraction_buffer_m` | Conditionally-Core | number (null+reason) | Buffer radius, where a buffer is used. **Mandatory for buffer strategies** (the radius is a hyperparameter that changes assignment); `not_applicable` otherwise. | EnVar |
| `population_weighting_source` | Conditionally-Core | string | Census vintage used for population weighting. **Mandatory for population-weighted products** — 2010 vs 2020 weights assign different exposure to the same person. | [Spangler2022] |
| `target_geography_type` | Core | enum | `point_residence` \| `census_block_group` \| `census_tract` \| `zcta` \| `county` \| `h3_hex_<r>` \| `public_water_system`. The geographic unit the value is attached to; mixing point and tract values silently is a known error. | EnVar |

### 4.3 `TemporalReference`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `temporal_resolution` | Core | enum | `instantaneous` \| `hourly` \| `three_hourly` \| `daily` \| `monthly` \| `seasonal` \| `annual`. | EnVar |
| `temporal_aggregation_method` | Core | CF-aligned enum | `mean` \| `maximum` \| `minimum` \| `sum` \| `percentile_<n>` \| `point_in_time`. "Daily max" and "daily mean" are different exposures with different health associations; this is the field that separates them. | [CF] |
| `temporal_aggregation_window_seconds` | Recommended | integer | Explicit window length (86400 for daily). Machine-checkable redundancy with `temporal_resolution`. | computed |
| **`day_boundary_convention`** | **Core** | enum | `local_midnight` \| `utc_midnight` \| `ending_1200_gmt` \| `solar_noon_centered` \| `observation_dependent`. **The single most-omitted slot in the heat literature.** Daymet uses local midnight; PRISM uses 24h-ending-1200-GMT; a "daily Tmax" depends on which window you chose, and cross-product comparison is sensitive to it. We make it Core deliberately; the workshop may downgrade it. | EnVar; [Gasparrini2015] |
| `temporal_coverage_start`/`end` | Recommended | ISO 8601 | The product's full coverage. Distinguishes out-of-coverage from missing. | source |
| `extraction_window_start`/`end` | Recommended | ISO 8601 | The dates this run actually extracted. | run |
| `calendar` | Recommended | CF calendar | `gregorian` (default) \| `noleap` \| `day_360` (CF `360_day`). Matters when the source (climate-model output) uses a non-standard calendar; misalignment shifts daily values. | [CF] |

> **`lag_alignment_applied` was relocated to §4.8 `LinkageMethod`.** It documents how an exposure value is attached to a clinical event (a linkage concern), not an intrinsic property of the temporal grain. `day_boundary_convention` stays here — it *is* intrinsic to the data, and it is the exposure-side half of the day-boundary cross-check now completed by `clinical_date_assignment_convention` in §4.8 (validation rule §7.8).

### 4.4 `SourceDataset`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `source_dataset_name` | Core | string | Producer's product name (`"Daymet V4 Daily Surface Weather Data"`). | producer |
| `source_dataset_short_code` | Recommended | string | Registry key (`daymet_v4`). | community |
| `source_dataset_version` | Core | string | Product version (`"V4 R1"`). **Version differences materially change values** (e.g. ACAG V5 vs V6 PM2.5); a value without a version is not reproducible. | producer |
| `source_dataset_doi` | Recommended | DOI | Dataset DOI (`10.3334/ORNLDAAC/2129`). The durable handle for the source; Recommended only because a few products lack one. | producer |
| `source_producer_institution` | Recommended | string | `"NASA ORNL DAAC"`. | producer |
| `source_citation_apa` | Recommended | string | Full citation for attribution and retrieval. | producer |
| `source_citation_bibtex` | Optional | string | Machine-parseable citation. | producer |
| `source_license_spdx` | Recommended | SPDX | Redistribution terms (`public-domain-us-gov`, `CC-BY-4.0`). | [SPDX] |
| `source_access_url` | Recommended | URL | Stable landing page (not a rot-prone download link). | producer |
| `source_native_format` | Recommended | enum | `netcdf4_cf` \| `geotiff` \| `grib2` \| `csv_station_observations` … | producer |
| `source_homogenisation_status` | Conditionally-Core | enum (null+reason) | `homogenised` \| `not_homogenised` \| `partial`. **Mandatory for station-based products** — GHCN-D is not homogenised; using it for trend work without saying so is a known trap. | producer |
| `source_acdd_attributes` | Optional | object | Passthrough of NetCDF ACDD global attributes when present. | [ACDD] |

### 4.5 `ExposureModel`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `exposure_model_type` | Core | enum | `direct_measurement` \| `spatial_interpolation` \| `reanalysis` \| `statistical_blend` \| `chemical_transport_model` \| `ensemble_machine_learning` \| `single_machine_learning` \| `equation_derived` \| `satellite_retrieval`. A measured value, an interpolated value, and an ML-predicted value have **different error structures** and cannot be pooled naively; this is the field that tells them apart. | EnVar; [Di2019] |
| `exposure_model_inputs` | Recommended | list | The model's input datasets/variables. Needed to trace what the value actually derives from. | producer |
| `exposure_model_paper_doi` | Recommended | DOI | The methods paper (Daymet [Thornton2022]; GridMET [Abatzoglou2013]; NARR [Mesinger2006]; ERA5 [Hersbach2020]). The reproducibility anchor for *how* the value was made. | producer |
| `exposure_model_cross_validation_r2` | Recommended | number (null+reason) | Reported cross-validation R² (how well the model predicts held-out observations). The single most useful one-number quality signal for a modeled product. | producer |
| `exposure_model_known_biases` | Recommended | list | Free-text-with-optional-tag flags (e.g. Daymet warm-season warm bias; NLDAS-2 coastal Tmax underestimation). The field reviewers care about most; bites coastal and sparse-station analyses. | producer; [Xia2012] |
| `exposure_model_uncertainty_field` | Recommended | string (null+reason) | Name of any per-value uncertainty column. Daymet ships a per-cell SE that most pipelines drop (`available_but_not_extracted`). | producer |
| `exposure_model_ensemble_member_count` | Conditionally-Core | integer (null+reason) | **Mandatory for ensemble products**; `not_applicable` for single-realisation. | producer |
| `bias_correction_applied` | Recommended | enum (null+reason) | `none` \| `quantile_mapping` \| `linear_scaling` \| `delta_method` \| `other`. Pooling bias-corrected and raw values silently mixes apples and oranges. | EnVar |

### 4.6 `DerivedHeatMetric` (conditional module — heat indices only)

Present only when the variable is a derived heat metric. For plain Tmax the module is omitted. These slots capture the methodological choices the heat-epi literature flags as the main sources of cross-study disagreement.

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `heat_metric_family` | Core (of module) | enum | `tmax` \| `tmin` \| `tmean` \| `heat_index` \| `wbgt_outdoor` \| `wbgt_indoor` \| `utci` \| `apparent_temperature` \| `humidex` \| `heat_wave_flag` \| `consecutive_extreme_heat_days` \| `cooling_degree_days`. | EnVar |
| `equation_variant` | Conditionally-Core | enum (null+reason) | Wet-bulb globe temperature (WBGT): `liljegren_2008` \| `acsm_simplified` \| `bernard_simplified`; Heat Index (HI): `rothfusz_1990_nws` \| `steadman_1979`; Universal Thermal Climate Index (UTCI): `brode_2012_polynomial`. **Mandatory for derived metrics** — WBGT approximations diverge materially from the reference model (well beyond 2–3 °C in hot-humid conditions). | [Liljegren2008]; [KongHuber2022]; [Brode2012] |
| `equation_inputs` | Conditionally-Core | list of typed refs (`EquationInput`) | Per-input references (T, RH, wind, radiation), each naming its `input_role` (CF standard name) and pointing by `input_provenance_id` to the upstream sidecar that carries that input's full spatial/temporal/model context — an index into `provenance_chain`, **not** an inline copy. **Option-B decomposition:** when inputs come from different products and diverge in resolution, day-boundary, or aggregation, each input stays a full sidecar so the divergence remains explicit and checkable (see rule 9 and `examples/scenarios/heat_index/`). Conditionally-Core: optional for single-input metrics, mandatory once a metric has more than one input. | EnVar |
| `equation_validity_range` | Conditionally-Core | object (null) | e.g. Heat Index `{min_temperature_F: 80, min_relative_humidity_pct: 40}`. **The Rothfusz HI is undefined below ~80 °F / 40 % RH**; using it outside that range produces nonsense. | [Rothfusz1990]; [Anderson2013] |
| `indoor_outdoor` | Conditionally-Core | enum | `outdoor` \| `indoor_modeled` \| `indoor_measured` \| `mixed_unspecified`. **Mandatory for WBGT** — indoor vs outdoor changes the equation and the health interpretation. | EnVar |
| `wind_speed_measurement_height_m` | Recommended | number (null) | 2 m standard vs the 10 m reanalysis often supplies; the log-law correction affects WBGT. | producer |
| `solar_radiation_basis` | Recommended | enum (null) | `surface_downwelling_shortwave_flux` \| `mean_radiant_temperature_modeled` \| `not_available`. | producer |
| `heat_wave_threshold_definition` | Conditionally-Core | enum (null) | `absolute_<v>_<unit>` \| `percentile_<n>_local` \| `percentile_<n>_climatological` \| `nws_heat_advisory_criteria` \| `etccdi_warm_spell_duration_index`. **Mandatory for heat-wave flags** — at least seven definitions are in use and none are convertible after the fact; the definition changes which days are flagged and the mortality estimate. | EnVar; [Anderson2011]; [Zhang2011] |
| `heat_wave_min_consecutive_days` | Conditionally-Core | integer (null) | The N-consecutive-days rule (2 or 3). Changes which days qualify. | EnVar |
| `percentile_reference_period_start`/`end` | Conditionally-Core | ISO 8601 (null) | **Mandatory for percentile thresholds** — "95th percentile" over 1971–2000 vs 2000–2019 is a different threshold in a warming climate, and the delta is real. | [Anderson2011] |
| `percentile_reference_geographic_scope` | Recommended | enum (null) | `local_tract` \| `local_county` \| `local_climate_region` \| `national`. | study design |
| `percentile_reference_seasonal_window` | Recommended | enum (null) | `annual` \| `warm_season_may_sep` \| `calendar_month`. | study design |
| `metric_temporal_aggregation_rule` | Recommended | string (null) | How a multi-day event is stamped on days (`first_day_of_event` \| `each_day_of_event` \| `last_day_of_event`). | study design |

### 4.7 `Uncertainty`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `per_value_uncertainty_field_name` | Recommended | string (null+reason) | Column carrying per-value uncertainty. | producer |
| `per_value_uncertainty_type` | Recommended | enum (null) | `standard_error` \| `prediction_interval_<n>_pct` \| `ensemble_std_dev` \| `monte_carlo_std_dev`. | EnVar |
| `model_aggregate_uncertainty` | Recommended | object (null) | Whole-model summary (`cv_r2`, `cv_rmse`, `reported_in`). | producer |
| `quality_flag_field_name` / `quality_flag_vocabulary` | Optional | string (null) | Per-value QA flag column + its vocabulary (CF `ancillary_variables` analogue). | producer |
| `missing_data_handling_method` | Recommended | enum (null) | `none` \| `spatiotemporal_interpolation` \| `forward_fill` \| `nearest_neighbour`. How gaps (snow-covered Daymet pixels) were filled — often invisible downstream. | producer |
| `data_completeness_pct` | Recommended | number (null) | Percent of (location, date) cells with a non-missing value. | run |

### 4.8 `LinkageMethod`

**Spatial and temporal linkage are two projections of one step.** Attaching a gridded value to a person is the resolution of the patient's spatiotemporal trajectory — *where the body was, over time* — down to the resolution the exposure data supports. Each axis carries two lossy reductions: **locating** the messy reality (address → point; clinical timestamp → date, residence/travel interval → which days) and **attaching** it to the exposure value (point → grid cell; date → exposure window). The schema has long documented the spatial axis (`geocoding_*`, `linkage_strategy`, `address_period_alignment`); the temporal twins (`clinical_date_assignment_convention`, `partial_day_attribution_rule`, `lag_alignment_applied`) are below. Critically, the Core `day_boundary_convention` (§4.3) describes only the *exposure-side* ruler; a boundary mismatch needs **both** rulers to detect, and `clinical_date_assignment_convention` supplies the clinical-side one (validation rule §7.8).

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `linkage_strategy` | Core | enum | `point_extraction_at_residence` \| `buffer_aggregation_around_residence` \| `area_membership_residence_in_polygon` \| `nearest_station_with_max_distance` \| `population_weighted_area_to_residence`. The "linkage descriptor" the GECC/EIRENE forum names as the central gap — how a place-based value becomes a person value. | EnVar; [Brokamp2018] |
| `linkage_buffer_radius_m` / `linkage_buffer_aggregation_method` | Conditionally-Core | number / enum (null) | **Mandatory for buffer strategies.** | study design |
| `linkage_max_distance_to_station_m` | Conditionally-Core | number (null) | **Mandatory for nearest-station strategies** — beyond it the assignment is meaningless and should be null. | study design |
| `geocoding_precision_propagated` | Recommended | enum | `range` \| `street` \| `intersection` \| `zip` \| `city` \| `unknown`. Rural addresses geocode coarser; ignoring this gives differential exposure misclassification. | [Brokamp2018] |
| `geocoding_score_propagated` | Recommended | number (null) | The geocoder's 0–1 score, propagated so the exposure knows the precision of its anchor. | upstream |
| `address_period_alignment` | Recommended | enum | `single_static_address` \| `address_history_from_emr` \| `known_travel_interval` \| `synthetic_residence_period`. How patient location-over-time was resolved — the *spatial* axis of trajectory resolution. `known_travel_interval` covers a documented trip away from the residence (the holiday case), where assuming a static address smears home-city exposure across days the patient was elsewhere. | EnVar |
| `clinical_date_assignment_convention` | Conditionally-Core | enum (null+reason) | The clinical-side mirror of `day_boundary_convention`: which timezone/boundary collapsed the clinical timestamp to the join date — `local_midnight` \| `utc_midnight` \| `source_system_local_time` \| `date_only_no_time` \| `unknown`. **Mandatory when a lagged or event-matched analysis is declared** (`lag_alignment_applied != none`); without it the Core `day_boundary_convention` cannot be checked against anything. Metadata *about the join* — never the clinical timestamp itself (the PHI line holds). | EnVar; [Gasparrini2015] |
| `partial_day_attribution_rule` | Recommended | enum (null+reason) | How boundary/transition days of a trajectory are attributed — `origin_location` \| `destination_location` \| `both_days_included` \| `excluded` \| `not_applicable`. Trip start/end and flight days otherwise attach exposure to the wrong place; the temporal partner to the spatial `known_travel_interval`. | EnVar |
| `lag_alignment_applied` | Recommended | enum (null+reason) | Whether values were already lag-aligned to a clinical event (`none` \| `lag_<n>_days` \| `distributed_lag_<min>_<max>`). Double-lagging is a silent analytic error. *Relocated here from §4.3 — it documents how a value is attached to an event (linkage), not an intrinsic temporal property.* | EnVar |

### 4.9 `ToolRun` + `ProvenanceChain`

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `tool_name` | Core | string | The tool that produced the value (`daymet`, `amadeus`). | tool |
| `tool_version` | Core | semver | Tool version. Reproducibility is impossible without knowing which tool version ran. | tool |
| `container_image_digest` | Recommended | string (null) | SHA256 of the image actually used (not just the tag). The strongest reproducibility anchor for a containerised run. | runtime |
| `run_arguments` | Recommended | object | Exact argument map at invocation. | runtime |
| `run_timestamp_utc` | Recommended | ISO 8601 | When the run started. | runtime |
| `run_environment` | Optional | object | OS, runtime, language/library versions. | runtime |
| `input_file_sha256` / `output_file_sha256` | Recommended | string | Hashes for verification that inputs/outputs are what the record claims. | runtime |
| `input_row_count` / `output_row_count` | Recommended | integer | Row counts; a cheap integrity check. | runtime |
| `provenance_chain` (steps) | Recommended | ordered list | The ordered upstream runs (geocoder → daymet). Lets a consumer walk the full derivation. Patterned on W3C PROV. | [PROV] |
| `provenance_chain_terminus_type` | Recommended | enum | `raw_source_download` \| `synthetic_data` \| `pre_existing_curated_dataset`. The root of the chain. | EnVar |

### 4.10 `HealthLayerLinkage` + `DepositMetadata`

The linkage hooks privilege no single health-data model: the target is named
in `health_layer_target` rather than baked into slot names. `phi_status` is a
record-root assertion (it applies to the whole sidecar, not just linkage).

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `provenance_id` | Core | ULID/UUID | The sidecar's stable id; this is what the downstream layer's source-value field holds (for OMOP, `external_exposure.exposure_source_value`). Without it the value cannot be linked back to its metadata. | run |
| `health_layer_target` | Recommended | enum | The downstream health-data layer (`omop_external_exposure` \| `bdc` \| `other`). Names the target so `health_layer_link_field` is read against the right model. | EnVar |
| `health_layer_link_field` | Recommended | string | Which field in the target layer carries `provenance_id` (for OMOP, `exposure_source_value`). | EnVar |
| `cohort_size_anchored` | Optional | integer (null) | Distinct persons this record was extracted for. | run |
| `phi_status` | Core (record root) | enum | `no_phi` \| `aggregated_no_phi` \| `phi_present`. A safety assertion; sidecars must be PHI-free. | EnVar |
| `deposit_*` (DOI, repository, license, citation, DCAT url) | Optional | mixed | The required-for-deposit subset for the published-FAIR-object case. Optional because most records never get deposited. | [SPDX]/[DOI] |
| `schema_version` | Core | string | The schema version this document targets; downstream branches on it for evolution. | EnVar |

### 4.11 `DataLayout`

The binding between the sidecar and the companion data file. `VariableIdentity`
says *what* the variable is; `DataLayout` says *where in the file* its values
live. The split matters as soon as the file is not wide-format: in long/tidy
data the value column is literally named `value` and a record's rows are
selected by a discriminator column, which identity slots cannot express.
Required at the record root — without it a consumer cannot locate the values
the sidecar describes.

| Element | Tier | Type / vocab | Definition & why it matters | Ref |
|---|---|---|---|---|
| `table_orientation` | Core | enum | `wide` \| `long`. Every other binding is read relative to the orientation; without it the bindings are uninterpretable. | EnVar |
| `value_column` | Core | string | The column carrying this record's values. The record carries no inline observation result, so this is the only pointer to the values. | EnVar |
| `variable_column` | Conditionally-Core (long) | string | The discriminator column in long format; without it the shared value column is ambiguous. | EnVar |
| `variable_key` | Conditionally-Core (long) | string | The label that selects this record's rows in `variable_column`. | EnVar |
| `subject_column` | Recommended | string | The join key back to the health-data layer. | EnVar |
| `time_column` | Recommended | string | Places each value in time for lag/window analyses. | EnVar |
| `value_uncertainty_column` | Recommended | string (null+reason) | Binds the per-value uncertainty most pipelines silently drop. | EnVar |
| `value_uncertainty_column_missing_reason` | Optional | enum | Distinguishes "unavailable upstream" from "lost". | EnVar |
| `quality_flag_column` | Optional | string (null+reason) | CF `ancillary_variables` analogue for per-value QA flags. | [CF] |
| `quality_flag_column_missing_reason` | Optional | enum | Documents why no QA-flag column is bound. | EnVar |

---

## 5. PM2.5 — generalisation check (the deltas)

PM2.5 reuses the entire frame; it exercises different elements than heat does. What changes:

| Aspect | TMAX | PM2.5 | Why it matters for the schema |
|---|---|---|---|
| `standard_name` | `CF:air_temperature` | `CF:mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air` (canonical units kg m⁻³; reported in UCUM `ug/m3`) | Confirms the CF + UCUM elements generalise to a mass-concentration variable. [CF-PM] |
| `exposure_model_type` | `spatial_interpolation` (Daymet) | `direct_measurement` (EPA AQS) → `ensemble_machine_learning` ([Di2019]) → `satellite_retrieval` ([vanDonkelaar2021]); also `single_machine_learning` ([Brokamp2018b]) | Exercises the model-type enum's non-interpolation branches; ML/satellite values have different error structure than monitors. |
| `temporal_aggregation_method` + averaging window | daily maximum | **daily mean vs annual mean** | The averaging window is itself a health-relevant attribute: acute (≈2-day) and chronic (annual) PM2.5 effects are distinct exposures. The schema must make daily-vs-annual explicit, not implicit. [Shi2016] |
| `day_boundary_convention` | the headline heat trap | still applies for daily PM2.5; `not_applicable` for annual means | Shows Core elements can be contextually `not_applicable` without being dropped. |
| `linkage_strategy` | point extraction | nearest-station (monitors) vs population-weighted-area (satellite/tract) | Stresses the linkage enum's station and area branches. |
| `concept_status` (vocab `omop`) | `gap` | `proposed` (PM2.5 is within the OHDSI GIS/Exposome vocabulary effort, no single canonical concept id yet) | Demonstrates the status enum spanning the gap-to-proposed range. |
| ontology IRIs | `ECTO:0000012` / temperature | `ECTO:7000117` (exposure to fine respirable suspended PM) / `ENVO:01000415` (fine respirable suspended PM) | Confirms the optional ontology hooks resolve for a pollutant. |

**Health-relevance anchors for PM2.5** (the "why capture this variable at all" evidence, for the workshop): foundational long-term cohorts [Dockery1993], [Pope2002]; modern large-cohort effects below current standards [Di2017]; regulatory and guideline levels [EPA-NAAQS], [WHO2021]; wildfire-smoke-specific PM2.5 as a distinct exposure [Childs2022].

The PM2.5 records (`tests/data/valid/EnvironmentalExposureRecord-pm25_{core,recommended,ideal}.yaml`) walk the same `core` → `recommended` → `ideal` completeness gradient as TMAX.

---

## 6. Controlled vocabularies

| Vocabulary | Used by | Source |
|---|---|---|
| CF Standard Names (v85+) | `standard_name` (`CF:` prefix) | external — [CF] |
| CF cell_methods | `cf_cell_methods` | external — [CF] |
| UCUM | `units_ucum` | external — [UCUM] |
| EPSG / PROJ | `crs` | external — [EPSG] |
| ECTO / ENVO / LOINC / SNOMED CT | `concept_mappings` (`ECTO:`, `ENVO:`, `LOINC:`, `SNOMED:` prefixes); local terms under `ENVAR:` | external — [ECTO], [ENVO], [LOINC], [SNOMED] |
| Health-data-layer vocabulary (OHDSI, BDC, …) | `target_concept_vocabulary`, `target_concept_id` | external — e.g. [Athena] |
| SPDX licenses | `*_license_spdx` | external — [SPDX] |
| ACDD attributes | `source_acdd_attributes` | external — [ACDD] |
| W3C PROV | `provenance_chain` modelling | external — [PROV] |
| ETCCDI indices | `heat_wave_threshold_definition` (ETCCDI variants) | external — [Zhang2011] |
| ISO 7243 | WBGT `equation_variant` | external (paywalled; cite by id) |
| EnVar-authored enums | `exposure_model_type`, `extraction_method`, `day_boundary_convention`, `linkage_strategy`, `equation_variant`, `heat_metric_family`, `heat_wave_threshold_definition`, `indoor_outdoor`, `target_geography_type`, `bias_correction_applied`, `concept_status`, `health_layer_target`, `clinical_date_assignment_convention`, `partial_day_attribution_rule`, `address_period_alignment`, missing-reason | EnVar — value lists in §4 |

---

## 7. Validation rules

1. Every emitted sidecar validates against the LinkML schema (via its JSON Schema export, or its SHACL export — SHACL being a shape-validation language for graph data).
2. Every null nullable element **must** carry a `*_missing_reason` from the controlled vocabulary (conditional requirement, SHACL-enforced).
3. Every controlled-vocabulary element validates against its enum / external term list; external resolution (CF, UCUM, ECTO) must work offline against a vendored term cache.
4. DOIs and IRIs must be syntactically valid; live-URL resolution is out of scope (network-fragile).
5. A `CF:`-prefixed `standard_name` + `cf_cell_methods` + `units_ucum` should be a CF-consistent triple; the validator **warns** on inconsistency (e.g. `CF:air_temperature` + `time: maximum` + `mol/mol`). The check applies only when `standard_name` uses the `CF:` prefix; locally-minted `ENVAR:` terms are exempt.
6. `provenance_chain` must be a connected directed acyclic graph (a DAG — steps link in one direction and never loop) terminating at a `provenance_chain_terminus_type` — no orphaned steps.
7. **Conditionally-Core enforcement:** when a context predicate holds (derived metric present; percentile threshold; buffer/nearest-station strategy; ensemble model; station-based source), the associated Conditionally-Core elements become required.
8. **Day-boundary cross-check (declaration-consistency).** When a lagged or event-matched analysis is declared (`lag_alignment_applied != none`), `clinical_date_assignment_convention` is required (Conditionally-Core), and the checker **warns** when it is absent or names a day boundary that disagrees with `temporal_reference.day_boundary_convention` (e.g. exposure-side `local_midnight` vs clinical-side `utc_midnight`). This is a metadata-consistency check only — the clinical timestamps sit across the PHI line and are never read; the rule compares the two *declared conventions*, not the data.
9. **Cross-input consistency (multi-input derived metrics).** When `derived_heat_metric.equation_inputs` has more than one entry, the checker dereferences each `input_provenance_id` and **warns** when the referenced input sidecars disagree on `day_boundary_convention`, `temporal_aggregation_method`/window, or `native_spatial_resolution_m` — e.g. a Heat Index built from a 1 km local-midnight daily *max* temperature and a ~31 km UTC daily *mean* humidity. The divergence is permitted but must be recorded via the decomposed input sidecars (Option B), not absorbed silently into the single output value. This is the input-internal analogue of rule 8. Worked example: `examples/scenarios/heat_index/`.
10. The schema exports to LinkML's standard targets (JSON Schema, SHACL, OWL, Markdown) without error.

---

## 8. The questions for the community

For each element above, the evaluation session collects five judgements:

1. **Core?** — mandatory, or the record is meaningless.
2. **Necessary for reproducibility?** — Recommended.
3. **Nice-to-have?** — Optional.
4. **Well described?** — is the definition clear and correct?
5. **Missing?** — what belongs here that isn't.

Two assignments we most want ratified or overturned: **`day_boundary_convention` as Core**, and the **Conditionally-Core treatment of `equation_variant` / percentile-reference** (vs flatly Core).

---

## 9. Reconciliation with the existing prototype

The repository already contains a 14-module LinkML implementation (`src/linkml_microschemas_envar/schema/`). This spec was **re-derived from the source requirements** (`envar-heat-scenario-requirements.md`) and the primer, then reconciled against that prototype. Findings:

| Area | Status | Action for v0.2 |
|---|---|---|
| Module set (`VariableIdentity`, `SpatialReference`, … `DerivedHeatMetric`, `HealthLayerLinkage`) | **Match.** The prototype's modules correspond 1:1 to §2, including `DataLayout` (added when the sidecar-to-file column binding was split out of `VariableIdentity`; §4.11). | none |
| Element coverage | **Near-complete match.** The §4 elements are present in the prototype's modules (it was built from the same requirements). | spot-check a few PM2.5-stressed elements (`exposure_model_ensemble_member_count`, annual-vs-daily aggregation) are present and correctly typed |
| **Tier annotations** | **Done (v0.2).** Every slot now carries an `annotations.tier` of `core` / `recommended` / `optional` / `conditionally_core` (the §4 strawman), and the LinkML `required:` flags were relaxed so only Core slots are hard-required — the two now agree. | Completeness checker reads `annotations.tier` directly (Approach A). |
| **Health-layer de-coupling** | **Done (v0.2).** `OmopLinkage`→`HealthLayerLinkage`; `omop_concept_*`→`target_concept_*`/`concept_status`; the link field is generalised and the target named in `health_layer_target`; `phi_status` moved to the record root; the privileged `OMOP:` prefix dropped. | none — the schema now privileges no single health-data model (OMOP is one `health_layer_target` value). |
| **Reference annotations** | **Done (v0.2, first pass).** Every slot now carries a uniform documentation bundle: curated `examples` (values drawn from the ideal-tier scenario records so they stay coherent across modules), a `justification` annotation (why the slot earns its place — the per-slot version of the §4 "why it matters" column), an `explanation` annotation (plain-language, for readers with no climate/health-informatics background), and `see_also` references where a canonical external URL exists (standards chapters, dataset pages, DOIs). Conventions documented in the schema README. | The exhaustive per-claim *verified-citation* pass (PMIDs for every Recommended/Optional element) remains scheduled per PLAN §5. |
| **`cf_cell_methods` generality** | **Resolved (2026-07): stays CF-specific.** The vocabulary-neutral capture of aggregation semantics is the required `temporal_aggregation_method` enum; `cf_cell_methods` preserves the verbatim CF expression for round-tripping and the rule-5 consistency check. `cell_methods` is an expression mini-language with no cross-vocabulary equivalent, so "generalising" it would mean an unspecified free string or a home-grown grammar. Rationale recorded as a `comments:` block on the slot (envar_variable.yaml). | none |
| **Top-level naming** | **Resolved (readable names).** The schema now uses the readable domain names (`variable_identity`, `spatial_reference`, `temporal_reference`, `exposure_model`) at the top level, each mapped to its profile anatomy slot via slot-level `implements`/`exact_mappings` (`instantiates` does not constrain slot names). | none — decision recorded in the schema README; examples and spec now agree. |
| Example data | **Resolved.** Relocated to `tests/data/valid/` (passing `core`/`recommended`/`ideal` gradient) and `tests/data/invalid/` (`core_missing` counter-examples). Now written with the readable top-level names, matching the schema; the profile names are recorded as `aliases` on the renamed slots. `observation_result` is no longer bound at the record root (values live in the companion data file). | none. |
| Conditionally-Core as a first-class tier | **New.** The prototype/requirements treat several slots as "mandatory in context" in prose; this spec elevates that to a named tier. | Encode the context predicates as LinkML rules (§7.7). |
| **Temporal-linkage symmetry** | **New (v0.2).** Spatial and temporal linkage are two projections of one trajectory-resolution step; the prototype modelled the spatial axis but scattered the temporal one. | `lag_alignment_applied` relocated `TemporalReference`→`LinkageMethod`; added `clinical_date_assignment_convention` (the clinical-side mirror of the Core `day_boundary_convention`) and `partial_day_attribution_rule`; `address_period_alignment` extended with `known_travel_interval`; day-boundary cross-check added (§7.8). Folds in the GECC "linkage descriptor" gap on the temporal axis. |

Net: the prototype is a faithful implementation of the requirements. Of the
substantive v0.2 work, **(a) tier annotations and the health-layer
de-coupling are done**, **(b) the per-slot documentation bundle (examples +
justification + explanation + see_also first pass) is done**, and **(c) the
top-level naming decision is resolved** (readable names; still open to
workshop challenge). What remains is the exhaustive verified-citation pass
(§5) — not a structural rebuild.

---

## 10. References (verified)

Heat / temperature and methods:

- **[Gasparrini2015]** Gasparrini A, et al. Mortality risk attributable to high and low ambient temperature: a multicountry observational study. *Lancet* 2015;386(9991):369–375. PMID 26003380 · doi:10.1016/S0140-6736(14)62114-0
- **[VicedoCabrera2021]** Vicedo-Cabrera AM, et al. The burden of heat-related mortality attributable to recent human-induced climate change. *Nat Clim Chang* 2021;11:492–500. PMID 34221128 · doi:10.1038/s41558-021-01058-x
- **[Liljegren2008]** Liljegren JC, et al. Modeling the wet bulb globe temperature using standard meteorological measurements. *J Occup Environ Hyg* 2008;5(10):645–655. PMID 18668404 · doi:10.1080/15459620802310770
- **[Brode2012]** Bröde P, et al. Deriving the operational procedure for the Universal Thermal Climate Index (UTCI). *Int J Biometeorol* 2012;56(3):481–494. PMID 21626294 · doi:10.1007/s00484-011-0454-1
- **[Rothfusz1990]** Rothfusz LP. The Heat Index "Equation". NWS Southern Region Tech. Attachment SR 90-23, 1990. https://www.weather.gov/media/ffc/ta_htindx.PDF
- **[Anderson2013]** Anderson GB, Bell ML, Peng RD. Methods to calculate the heat index as an exposure metric in environmental health research. *Environ Health Perspect* 2013;121(10):1111–1119. PMID 23934704 · doi:10.1289/ehp.1206273
- **[Anderson2011]** Anderson GB, Bell ML. Heat waves in the United States: mortality risk during heat waves and effect modification by heat wave characteristics in 43 U.S. communities. *Environ Health Perspect* 2011;119(2):210–218. PMID 21084239 · doi:10.1289/ehp.1002313
- **[KongHuber2022]** Kong Q, Huber M. Explicit calculations of wet-bulb globe temperature compared with approximations and why it matters for labor productivity. *Earth's Future* 2022;10(3):e2021EF002334. doi:10.1029/2021EF002334 — *supports the "WBGT approximations diverge materially" claim; not a literal Liljegren-vs-ACSM-vs-Bernard comparison.*
- **[Foster2024]** Foster J, et al. Identifying the optimal heat exposure metric for predicting the physiological response to dry or humid heat stress. *Environ Health Perspect* 2024;132(1):017002. PMID 38214893 · doi:10.1289/EHP13733
- **[Zhang2011]** Zhang X, et al. Indices for monitoring changes in extremes based on daily temperature and precipitation data. *WIREs Clim Change* 2011;2(6):851–870. doi:10.1002/wcc.147
- **[Spangler2022]** Spangler KR, et al. Wet-bulb globe temperature, universal thermal climate index, and other heat metrics for US counties, 2000–2020. *Sci Data* 2022;9:326. doi:10.1038/s41597-022-01405-3

Data products:

- **[Thornton2022]** Thornton MM, et al. Daymet: Daily Surface Weather Data on a 1-km Grid for North America, Version 4 R1. ORNL DAAC, 2022. doi:10.3334/ORNLDAAC/2129
- **[Abatzoglou2013]** Abatzoglou JT. Development of gridded surface meteorological data for ecological applications and modelling. *Int J Climatol* 2013;33(1):121–131. doi:10.1002/joc.3413
- **[Mesinger2006]** Mesinger F, et al. North American Regional Reanalysis. *Bull Am Meteorol Soc* 2006;87(3):343–360. doi:10.1175/BAMS-87-3-343
- **[Hersbach2020]** Hersbach H, et al. The ERA5 global reanalysis. *Q J R Meteorol Soc* 2020;146(730):1999–2049. doi:10.1002/qj.3803
- **[Xia2012]** Xia Y, et al. Continental-scale water and energy flux analysis and validation for NLDAS-2, part 1. *J Geophys Res Atmos* 2012;117:D03109. doi:10.1029/2011JD016048 — *canonical NLDAS-2 forcing reference; the specific −1.48 °C coastal Tmax figure circulating in project notes is unverified.*

PM2.5:

- **[Di2019]** Di Q, et al. An ensemble-based model of PM2.5 concentration across the contiguous United States with high spatiotemporal resolution. *Environ Int* 2019;130:104909. PMID 31272018 · doi:10.1016/j.envint.2019.104909
- **[vanDonkelaar2021]** van Donkelaar A, et al. Monthly global estimates of fine particulate matter and their uncertainty. *Environ Sci Technol* 2021;55(22):15287–15300. PMID 34724610 · doi:10.1021/acs.est.1c05309 (ACAG dataset versions: https://sites.wustl.edu/acag/datasets/surface-pm2-5/)
- **[Brokamp2018b]** Brokamp C, et al. Predicting daily urban fine particulate matter concentrations using a random forest model. *Environ Sci Technol* 2018;52(7):4173–4179. PMID 29537833 · doi:10.1021/acs.est.7b05381
- **[Childs2022]** Childs ML, et al. Daily local-level estimates of ambient wildfire smoke PM2.5 for the contiguous US. *Environ Sci Technol* 2022;56(19):13607–13621. PMID 36134580 · doi:10.1021/acs.est.2c02934
- **[Dockery1993]** Dockery DW, et al. An association between air pollution and mortality in six U.S. cities. *N Engl J Med* 1993;329(24):1753–1759. PMID 8179653 · doi:10.1056/NEJM199312093292401
- **[Pope2002]** Pope CA 3rd, et al. Lung cancer, cardiopulmonary mortality, and long-term exposure to fine particulate air pollution. *JAMA* 2002;287(9):1132–1141. PMID 11879110 · doi:10.1001/jama.287.9.1132
- **[Di2017]** Di Q, et al. Air pollution and mortality in the Medicare population. *N Engl J Med* 2017;376(26):2513–2522. PMID 28657878 · doi:10.1056/NEJMoa1702747
- **[Shi2016]** Shi L, et al. Low-concentration PM2.5 and mortality: estimating acute and chronic effects in a population-based study. *Environ Health Perspect* 2016;124(1):46–52. PMID 26038801 · doi:10.1289/ehp.1409111
- **[Brokamp2018]** Brokamp C, et al. Decentralized and reproducible geocoding and characterization of community and environmental exposures for multisite studies (DeGAUSS). *J Am Med Inform Assoc* 2018;25(3):309–314. PMID 29126118 · doi:10.1093/jamia/ocx128

Standards & vocabularies:

- **[CF]** CF Standard Name Table & Conventions — https://cfconventions.org/ · **[CF-PM]** PM2.5 standard name — https://vocab.nerc.ac.uk/standard_name/mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air/
- **[UCUM]** https://ucum.org/ · **[EPSG]** https://epsg.io/ · **[SPDX]** https://spdx.org/licenses/ · **[ACDD]** https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3 · **[PROV]** https://www.w3.org/TR/prov-overview/
- **[ECTO]** https://obofoundry.org/ontology/ecto.html · **[ENVO]** https://obofoundry.org/ontology/envo.html · **[LOINC]** https://loinc.org/ · **[SNOMED]** https://www.snomed.org/ · **[Athena]** https://athena.ohdsi.org/
- **[EPA-NAAQS]** US EPA NAAQS table (PM2.5 annual 9.0 µg/m³, 24-hr 35 µg/m³, 2024) — https://www.epa.gov/criteria-air-pollutants/naaqs-table · EPA AQS — https://www.epa.gov/aqs
- **[WHO2021]** WHO global air quality guidelines, 2021 (PM2.5 AQG 5 µg/m³ annual / 15 µg/m³ 24-hr) — https://iris.who.int/handle/10665/345329
