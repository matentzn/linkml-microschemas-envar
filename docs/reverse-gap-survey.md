# Reverse gap survey — standards' fields with no EnVar home

All other coverage work in this repository runs in one direction: *for each
EnVar slot, does GAIA / DeGAUSS / Amadeus / C-HER / CODATA carry it?*
([Related approaches](related-approaches.md), the `covered_by` matrix design,
the emitted-only translations in `examples/scenarios/standards/`). By
construction that matrix cannot show the opposite: **fields these systems
record that EnVar has no slot for at all.** This survey is that opposite
direction.

It is **not** the "inverse gap analysis" of the coverage design (its §4.3
still ranges over EnVar's own slot universe — EnVar slots no standard covers).
This survey ranges over the *standards'* field universes, which EnVar's slots
never mention. Keep the two apart.

## Method and evidence base

- **Instance-emitting standards** (DeGAUSS, Amadeus, OMOP/GAIA): every field,
  column, attribute, and key in the native outputs of the three real heat
  pipelines under `~/ws/projects/EnVar/examples/heat/{degauss,amadeus,omop-gaia}/`,
  cross-checked against `COMPARISON.md` there. Only what the pipelines
  themselves emit counts — the EnVar sidecars, `MANIFEST.json`, and the
  hand-added `envar:*` PropertyValues in the GAIA JSON-LD are excluded (those
  are the layer EnVar proposes to add, not the standard).
- **Conceptual-layer standards** (C-HER, CODATA Essential Variables / CDIF):
  the local survey notes (`~/ws/notes/niehs_standards/surveys/_raw/relatedwork/`)
  and [Related approaches](related-approaches.md) §4. Evidence limits are
  stated per standard rather than papered over.
- Each field was matched against the full induced slot universe of
  `EnvironmentalExposureRecord` (182 tier-annotated slots, via SchemaView, so
  `slot_usage` overrides count).

**Verdicts** for fields with no EnVar home:

| Verdict | Meaning |
|---|---|
| **ADD** | belongs in EnVar as a new slot — proposal recorded below |
| **ABSORB** | representable in an existing slot; the survey records how |
| **OUT** | out of scope, with the reason written down |

Fields *with* an EnVar home are summarised per standard but not verdict-ed —
the forward coverage matrix already handles that direction.

---

## 1. DeGAUSS

Native output is two CSVs (geocoder, daymet) with the container name/version
baked into the filenames, plus AppEEARS artefacts fetched by the daymet
container. Fields with EnVar homes: `id` → `subject`/`subject_column`;
`start_date`/`end_date` → `extraction_window_start`/`_end`; `score`/`precision`
→ `geocoding_score_propagated`/`geocoding_precision_propagated`; `date` →
`time_column`; `tmax` → `value_column`; filename-embedded tool name/version/
`score_threshold_0.5` → `tool_name`/`tool_version`/`run_arguments`; the
AppEEARS request parameters map onto `spatial_extent_bbox`,
`source_dataset_version`, `source_native_format`, `crs`.

Fields with no home:

| Field (where) | Verdict | Reason |
|---|---|---|
| `address`, `matched_street/_zip/_city/_state`, `lat`, `lon` (both CSVs); geocoder-cache `number`, `prenum`, `fips_county` | **OUT** | Address-level and coordinate PHI. The sidecar is PHI-free by design (`phi_status`); the spatial anchor is *described* (`target_geography_type`, `address_period_alignment`), never carried. This is a design reaffirmation, not an oversight. |
| `geocode_result` (match-status flag, per row) | **ABSORB** | Per-row QA is data, not sidecar metadata: bind the column via `DataLayout.quality_flag_column` and name its value set in `quality_flag_vocabulary`. |
| Daymet pixel `Elevation` (archival fixture) | **OUT** | A different variable, not metadata about this one. EnVar's unit of description is one variable series per sidecar — an elevation series gets its own record. |
| AppEEARS job telemetry (`task_id`, `task_name`, `task_type`, `api_version`, `svc_version`, `estimate.*`, `expires_on`) | **OUT** | Service-job bookkeeping, not reproducibility metadata. The request *parameters* (which do matter) already map to EnVar slots; the job wrapper does not. |
| `DAYMET-004-Statistics.csv` tile-wide stats (Count, Min, Max, Mean, SD, quartiles …) | **OUT** | Aggregates over the whole requested tile, not properties of the linked per-subject values. Value-level uncertainty lives in the `uncertainty` module; tile summaries reproduce nothing. |
| AppEEARS `user_id` (an account email in `2022-tmax-request.json`) | **OUT** (schema) | Not a schema gap — **PII in a local pipeline artefact** (see side findings). |

## 2. Amadeus

The richest harvest. Native outputs: the per-day CSV (`value_kelvin` +
`value_celsius` side by side), R-attribute JSON blocks (versions, calls,
timestamps, row counts, SpatRaster summary), and the THREDDS/CF metadata
(`cf_metadata.json`, `thredds_dataset.xml`). Fields with homes include:
`package_version`/`amadeus_version` → `tool_version`; `r_version`/
`terra_version`/`attached_pkgs`/`rocker_image` → `run_environment` (and
`container_image_repository`); `call*` → `run_arguments`;
`datetime_*_utc` → `run_timestamp_utc`/`run_duration_seconds`;
row counts → `input_row_count`/`output_row_count`; SpatRaster `crs`/
`resolution`/`extent` → `crs`/`native_spatial_resolution_m`/`spatial_extent_bbox`;
`calendar` → `calendar`; `lat_lon_box` → `spatial_extent_bbox`; `time_span` →
`temporal_coverage_start`/`_end`; variable `units`/`long_name`/`description` →
`units_ucum` (native)/`variable_name`/`variable_label`.

Fields with no home:

| Field (where) | Verdict | Reason |
|---|---|---|
| `scale_factor` (0.1), `add_offset` (220.0), `_Unsigned` (variable attributes) | **ADD** | The packed-int16→Kelvin decode convention. Mis-decoding produces garbage temperatures; the translation currently drops it into a YAML comment ("the schema has no slot for it"). The single most load-bearing gap this survey found — see proposal 1. |
| `value_kelvin` (second, native-unit value column) | **ADD** (rider on proposal 1) | `DataLayout` binds exactly one `value_column`; the native-unit twin column has no binding. An optional `native_value_column` rider on the unit-conversion record covers it. |
| `_FillValue` / `missing_value` (32767) | **ADD** | The missing-data *sentinel value*. `missing_data_handling_method` records policy, not the number; a consumer re-reading the source grid needs 32767. GAIA independently surfaces the same field (`nodata`). See proposal 2. |
| time-axis epoch (`days since 1900-01-01`, axis `units`/`description`) | **ABSORB** | CF axis metadata needed only when re-reading the raw grid; the sidecar stores decoded dates. Belongs in the `source_acdd_attributes` passthrough, not a first-class slot. |
| CF structural attributes (axis roles, `_CoordinateAxisType`, `_ChunkSizes`, `coordinates`, `dimensions`, `grid_mapping`, shapes, dtypes, gridSet/axisRef, `projectionBox`, AcceptList format menus) | **OUT** | Serialization structure of the NetCDF/THREDDS container, restating what EnVar models semantically (or pure server plumbing). `source_acdd_attributes` can carry any of it verbatim if a use-case appears. |
| axis `increment` (0.041666° ≈ 4 km) | **ABSORB** | This *is* the native resolution, in degrees — `native_spatial_resolution_m` is its home after unit conversion; `native_spatial_resolution_descriptor` can record "1/24 degree regular grid". |
| `thredds_url_queried`, `dataset_location`, `source.endpoint`, AppEEARS granule URLs | **ABSORB** | The machine endpoint actually queried is run-scoped: it belongs in `tool_run.run_arguments`. `source_access_url` stays a landing page by definition; deposit-side distributions have `dcat_distribution_url`. |
| `execution_mode` (real-amadeus vs python-THREDDS fallback) | **ABSORB** | A genuine provenance fact, but it describes the execution context: record it in `run_environment` (or `tool_description` where the fallback is permanent). |
| `input_dates_n`, `nlyr` | **OUT** | Derivable from `extraction_window_start`/`_end`; no independent information. |
| HTTP headers (`content-type`, `date`, `server`, CORS, …), R object plumbing (`class`, `row.names`, `names`, `locale`, `platform`) | **OUT** | Network-transport and language-runtime noise; not dataset provenance. |

## 3. OMOP / GAIA

The densest overlap of the three: gaiaCatalog's DCAT/JSON-LD discovery
block and gaia-db's `variable_source` land almost entirely on existing EnVar
slots (`source_dataset_name`/`_version`/`_doi`, `source_license_spdx`,
`source_producer_institution`, `source_access_url`, `variable_name`/`_label`,
NERC `property_id` → `standard_name`, `unit_code`/`unit_text` →
`units_ucum`/`units_display`, `min/max_value` →
`value_range_plausible_min`/`_max`, coverage dates →
`temporal_coverage_start`/`_end`, `measurement_technique` →
`exposure_model_type`/`_inputs`). GAIA is also the only pipeline natively
emitting a health-layer concept binding (`exposure_concept_id`,
`exposure_source_value` → `target_concept_id`, `provenance_id`/
`health_layer_link_field`).

Fields with no home:

| Field (where) | Verdict | Reason |
|---|---|---|
| `local_epsg` (EPSG:5070 — the equal-area CRS the spatial join actually ran in) | **ADD** | Reprojection can shift point-to-cell assignment; the working CRS is a linkage hyperparameter distinct from the native `crs`. See proposal 3. |
| `nodata` (`[float4, -9999]`) | **ADD** | Same field as Amadeus's `_FillValue` — folded into proposal 2. |
| `structure` / `geometry` (`raster`), JSON-LD `measurementTechnique.termCode` | **ABSORB** | Gridded-vs-vector nature of the source: `native_spatial_resolution_descriptor` already encodes it ("1 km regular grid" vs "point station"); `target_geography_type` covers the anchor side. |
| Dataset discovery block: `description`/`dct:description`, `keywords`/`dcat:keyword`, `datePublished`/`dct:issued`, `dateModified`, publisher `@id`, `update_frequency` | **OUT** | Catalog-copy metadata, dereferenceable via `source_dataset_doi`/`source_access_url`. EnVar records source *identity*, not a mirror of the source's catalog entry; data currency is pinned by `run_timestamp_utc` + `source_dataset_version`. (Caveat noted: for products versioned "current", the version slot should carry a date-stamped value — that is curation guidance, not a new slot.) |
| ETL/deployment plumbing: `file`, `download`, `table`, `up`, `podID`, `derive`; DB surrogate keys and audit columns (`*_uuid`, `*_id` PKs/FKs, `created_at`/`updated_at`); `spatial_join_log.txt` | **OUT** | Internal bookkeeping of one deployment, not portable provenance. The ETL run itself, when it matters, is a `ToolRun`. |
| OMOP target-layer bookkeeping: `exposure_type_concept_id` (32885), `exposure_source_concept_id`, `location_id` FK, `location_history.domain_id`/`entity_id`, `value_as_concept_id` | **OUT** | These live in (and belong to) the health layer's own record; the sidecar links via `health_layer_link_field`, it does not mirror OMOP columns. |
| PHI columns: `person` demographics (gender, birth, race, ethnicity, source values), `location` address components + `latitude`/`longitude`/`geom`, `location_source_value` | **OUT** | Same design reaffirmation as DeGAUSS: PHI-free sidecar; anchor described, not carried. `location_history` periods are *described* by `address_period_alignment`. |

## 4. C-HER

**Field-level survey not possible from available material.** The local notes
record explicitly that C-HER's internal data formats and standards are not
publicly documented, and the coverage design already treats C-HER as
`asserted` for the same reason. What the notes attribute to C-HER are
descriptive dimensions, not a field schema:

| Dimension | Verdict | Reason |
|---|---|---|
| Spatial indexing at multiple geographic levels | *(has home)* | `target_geography_type` + `native_spatial_resolution_m`. |
| Exposomic domain tags (air quality, climate, water, built environment, social context) | **OUT** | Catalogue-level thematic tagging; EnVar identifies variables (`standard_name`), it does not tag datasets by theme. Revisit if a concrete C-HER registration schema is published. |
| "Analysis-ready" status | **OUT** | A catalogue readiness flag, not per-value provenance; `source_homogenisation_status` is the nearest EnVar concept but answers a different question. |
| Catalogue scale (30+ datasets) | **OUT** | Inventory metric of the resource itself. |

The actionable overlap with C-HER is procedural, not field-level: its
registration-time completeness gate is already cited as precedent for the
EnVar checker's BLOCKING behaviour. **This section should be redone when
C-HER publishes its registration/catalog schema** — that is the one genuine
to-do this survey could not discharge.

## 5. CODATA Essential Variables / CDIF

Conceptual layer by design (`out_of_layer` in the coverage matrix, not
`absent`). The concrete element set in the local material is the DDI-CDI
variable cascade, the I-ADOPT decomposition, and the packaging targets — and
the cascade lands cleanly on EnVar: `ConceptualVariable` → `variable_identity`
(`standard_name`), `RepresentedVariable` → `units_ucum` + `value_data_type`,
`InstanceVariable` → `data_layout` (EnVar's whole layer *is* the instance
layer), Croissant `cr:Field` → `value_column`, CF/UCUM → `standard_name`/`units_ucum`.

Fields with no home:

| Element | Verdict | Reason |
|---|---|---|
| I-ADOPT `object` and `matrix` (and the decomposition pattern as a whole) | **ABSORB** (now) | Today: hang ontology terms off `concept_mappings` (ENVO material/medium terms already fit there). A first-class I-ADOPT projection is already tracked as its own issue (#2) — this survey adds the evidence that only `object`/`matrix` lack homes; `property` rides inside the CF `standard_name`. |
| Cascade-layer label (tagging each field conceptual / represented / instance) | **OUT** | Documentation-level alignment metadata about the *schema*, not about any record. If wanted, it is a slot `annotations.*` entry, not an instance slot. |

---

## Consolidated verdicts — proposed schema changes

Three **ADD** proposals survive the sweep (everything else absorbed or ruled
out above). **All three were adopted on 2026-07-04**: `native_units_ucum` /
`native_value_scale_factor` / `native_value_offset` /
`unit_conversion_formula` (envar_variable, with a schema rule making the
formula mandatory once native units are declared) plus
`DataLayout.native_value_column` (envar_layout); `missing_value_sentinel`
(envar_uncertainty); `linkage_working_crs` (envar_linkage). Each slot's
`comments:` block records how this survey surfaced it. Cross-standard
pressure noted per row:

| # | Proposal | Surfaced by | Sketch |
|---|---|---|---|
| 1 | **Native-unit / packing conversion record** on `VariableIdentity` (or `SourceDataset`): `native_units_ucum`, plus a structured conversion (`scale`, `offset`, or formula string), plus an optional `DataLayout.native_value_column` binding | Amadeus (`scale_factor`/`add_offset`/`_Unsigned`, `value_kelvin` twin column), GAIA (K→°C math recorded nowhere), DeGAUSS (container converts silently) — and the `envar:*` JSON-LD extension already prototyped exactly these keys | Recommended tier; the known worked example is packed-int16 → K → °C |
| 2 | **`missing_value_sentinel`** (optional), next to `missing_data_handling_method` in the `uncertainty` module | Amadeus (`_FillValue`/`missing_value` 32767), GAIA (`nodata` −9999), Daymet fixtures | Policy slot says *how* gaps were handled; this says *which stored value means missing* |
| 3 | **`linkage_working_crs`** (optional) on `LinkageMethod` | GAIA (`local_epsg` EPSG:5070 — the CRS the join ran in) | Distinct from the native `crs`; reprojection is a linkage hyperparameter that can move points across cells |

## Side findings

- **PII in a local EnVar pipeline artefact** (not this repo, not a schema
  matter): `~/ws/projects/EnVar/examples/heat/degauss/_docker_workdir/daymet/Daymet_Data/2022_tmax/2022-tmax-request.json`
  carries the EarthData account email in its `user_id` field. The
  `_docker_workdir/` path is gitignored and the file was never tracked, so
  this is a local artefact to scrub against future accidental exposure, not
  a checked-in leak — tracked as `issues/issue_appeears_pii_scrub.md` in the
  EnVar repo.
- The three-pipeline comparison (`COMPARISON.md` in the EnVar repo) lists
  twelve "no pipeline carries this" features; this survey is its mirror and
  confirms the two lists do not overlap — the forward gaps (day-boundary,
  aggregation method, extraction method, …) are exactly the fields EnVar
  adds, and the reverse gaps above are exactly the fields EnVar still lacks.
