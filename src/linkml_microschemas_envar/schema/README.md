# EnVar Microschemas

These LinkML microschemas describe the *sidecar metadata* that travels
alongside a value (or value series) emitted by an upstream environmental-data
tool (Amadeus, DeGAUSS, …) and consumed downstream by OMOP or another
health-data layer. The top class is `EnvironmentalExposureRecord`; it
composes variable identity, spatial / temporal reference, source dataset,
exposure model, uncertainty, linkage method, tool-run / W3C-PROV provenance
chain, optional derived-heat-metric methodology, health-data-layer linkage
hooks (OMOP, BDC, …), and FAIR-deposit metadata. The schema implements §1.1 of
`pipeline/heat-omop-slice/envar-heat-scenario-requirements.md`.

## Modules

| File | Class(es) | Purpose |
|---|---|---|
| `envar_common.yaml` | (enums, shared slots) | Shared `MissingReasonEnum`, `DataTypeEnum`, `ConceptStatusEnum`, `PhiStatusEnum`; `schema_version`, `provenance_id`, `phi_status`. Imports the LinkML Microschema Profile. |
| `envar_variable.yaml` | `VariableIdentity` | CF standard name, UCUM units, target-vocabulary concept id + status, ECTO / ENVO bindings, plausible value range. Covers req §2. |
| `envar_spatial.yaml` | `SpatialReference` | Native grid, CRS, extent, extraction method, target geography. Covers req §3. |
| `envar_temporal.yaml` | `TemporalReference` | Resolution, aggregation, day-boundary convention, coverage, calendar, lag alignment. Covers req §4. |
| `envar_source.yaml` | `SourceDataset` | Upstream product identity, DOI, version, license, native format, homogenisation status. Covers req §5. |
| `envar_model.yaml` | `ExposureModel` | Model type, inputs, paper DOI, known biases, uncertainty field, bias correction. Covers req §6. |
| `envar_uncertainty.yaml` | `Uncertainty` | Per-value and aggregate uncertainty, quality flags, missing-data handling. Covers req §8. |
| `envar_linkage.yaml` | `LinkageMethod` | Gridded-to-patient linkage strategy, buffer parameters, propagated geocoder quality. Covers req §9. |
| `envar_toolrun.yaml` | `ToolRun`, `ProvenanceChain` | Exact tool invocation and the ordered W3C-PROV chain of upstream runs. Covers req §10 and §11. |
| `envar_heat_metric.yaml` | `DerivedHeatMetric` | Heat-metric methodology: family, equation variant, indoor / outdoor, percentile reference period. Covers req §7. |
| `envar_health_layer.yaml` | `HealthLayerLinkage`, `DepositMetadata` | Health-data-layer linkage hooks (OMOP, BDC, …; target named in a slot) and FAIR-deposit slots. Covers req §12 and §13. |
| `envar_record.yaml` | `EnvironmentalExposureRecord` | Top composite class — binds the microschema-profile slots to envar-specific ranges and lists the top-level slots. |
| `envar_examples.yaml` | `DailyMaxTemperatureRecord`, `DailyMinTemperatureRecord`, `WetBulbGlobeTemperatureOutdoorRecord`, `ExtremeHeatDayFlagRecord` | Concrete record subclasses for the canonical heat-exposure variables. |
| `linkml_microschemas_envar.yaml` | (umbrella) | Manifest schema importing the eleven modules above. |

## Worked example

A concrete Daymet Tmax sidecar for Phoenix on 2022-07-19 is provided at
[`../../../examples/daymet_tmax_phoenix_2022_07_19.yaml`](../../../examples/daymet_tmax_phoenix_2022_07_19.yaml).
It replicates the JSON block in
`pipeline/heat-omop-slice/envar-heat-scenario.md` §4 of the EnVar project
notes.

## Design decisions

### Top-level anatomy slots use readable domain names, mapped to the profile

The `EnvironmentalExposureRecord` class `instantiates: MicroschemaDefinition`
from the [LinkML Microschema Profile](https://github.com/linkml/linkml-microschema-profile).
`instantiates` is a *metaclass* relationship: it governs which annotations
are valid on the class definition and neither inherits nor constrains slot
names (see the LinkML how-to "Implements vs Instantiates vs Inheritance").
The record therefore uses **readable domain names** for the profile anatomy;
each is a local envar slot that maps back to its profile counterpart via
slot-level `implements` and `exact_mappings` (prefix
`msprofile: https://w3id.org/linkml/linkml-microschema-profile/`):

| Readable slot (validated key) | Profile slot | Bound range | Envar concept |
|---|---|---|---|
| `subject` | `subject` (used verbatim) | `string` | Opaque patient / cohort handle (PHI-free) |
| `variable_identity` | `msprofile:observation_type` | `VariableIdentity` | What variable is being captured |
| `spatial_reference` | `msprofile:location` | `SpatialReference` | Where — native grid + extraction |
| `temporal_reference` | `msprofile:temporality` | `TemporalReference` | When — resolution + day boundary |
| `exposure_model` | `msprofile:methodology` | `ExposureModel` | How — the exposure model |
| — | `observation_result` | not bound | Values live in the companion data file |

The remaining envar concerns that have no profile equivalent —
`data_layout`, `source_dataset`, `linkage_method`, `tool_run`,
`provenance_chain`, `derived_heat_metric`, `health_layer_linkage`,
`deposit_metadata`, `uncertainty`, and the record-root `phi_status` — are
surfaced as additional top-level slots alongside the anatomy slots.

### Why this choice

- **First-read clarity for domain experts.** Exposure scientists read the
  sidecar before they read the profile. `spatial_reference:` is
  self-explanatory in a way `location:` (native grid + CRS + extraction
  rule) is not; the profile-abstract names carried documented
  adoption-friction costs.
- **Profile conformance is unaffected.** Because `instantiates` does not
  constrain slot names, the readable names cost nothing at the meta level;
  the per-slot `implements` / `exact_mappings` assertions preserve the
  machine-readable anatomy mapping for cross-domain consumers.
- **The examples already read this way.** The worked sidecars were authored
  with the readable names; this decision realigns the schema with them
  rather than the reverse.

**History.** The first prototype used the profile slot names verbatim
(`observation_type`, `location`, `temporality`, `methodology`) bound to
envar ranges via `slot_usage`, prioritising literal cross-domain slot-name
identity. That was reversed once the `instantiates` semantics above were
confirmed. A middle route — keeping the profile names and switching the
*serialized key* with the metamodel's `alias` (singular) — was spiked and
rejected: `linkml-validate`, `gen-json-schema`, and `gen-pydantic` honour
`alias`, but `gen-python` (the dataclass generator used by `just test`)
rejects `alias` in `slot_usage`, and re-declaring the imported profile
slot locally fails with conflicting-URI errors. Full trail in
`issue_naming.md`.

### Known drawbacks

- **No literal slot-name identity across domains.** A meta-analyst reading
  a clinical-microschema record and an envar sidecar no longer sees the
  same anatomy keys; the correspondence is machine-readable (via
  `implements` / `exact_mappings`) but not eyeball-visible. `implements`
  is documentative — current tooling does not enforce the conformance it
  declares.
- **`exposure_model` is narrower than the profile's `methodology`.** The
  profile has one `methodology` slot, but environmental exposures need to
  describe several methodology-adjacent concerns (the upstream source
  product, the model class, the tool that ran, the W3C-PROV chain, the
  heat-derivation logic). We map `exposure_model` to `methodology` and
  surface the rest as separate envar-extension slots. The split is a
  judgment call; someone could reasonably argue everything-methodology
  should hang off a single composite.
- **`observation_result` is not bound.** Per-batch sidecars describe a
  CSV / parquet file that contains many values; there is no single value
  to attach, so the profile's required `observation_result` is dropped
  from the record's slot list (see the comment in `envar_record.yaml`).

### When to revisit

Revisit this decision if (a) the profile maintainers rule that conformance
requires the literal slot names after all, (b) profile tooling starts
*enforcing* `implements` and flags the mapping, or (c) the profile evolves
its anatomy vocabulary. The four readable slot definitions in
`envar_record.yaml` are the single place to change.

## Per-slot documentation conventions

Every slot in every module carries a uniform documentation bundle, in this
order inside the slot definition:

1. **`description`** — the normative definition (LinkML metaslot).
2. **`examples`** — at least one curated example (LinkML metaslot), with
   values drawn from the two ideal-tier scenario records in
   `tests/data/valid/` (Daymet Tmax / ACAG PM2.5) so examples stay mutually
   coherent across modules. Conventions: scalar and enum slots use `value:`;
   class-ranged slots use `object:` with a minimal abridged instance;
   multivalued scalar slots use one `value:` per list element. Do **not**
   put a bare YAML list under `object:` — the metamodel's `Anything` range
   rejects top-level arrays (`linkml-lint` valid-schema errors).
3. **`comments`** — non-normative design notes (e.g. the do-not-generalise
   rationale on `cf_cell_methods`).
4. **`see_also`** — authoritative external references (standards chapters,
   dataset landing pages, DOIs/PMIDs) where a canonical one exists. Never a
   guessed URL.
5. **`annotations`** — the EnVar-specific tags, in this order:
   - `tier` — `core` / `recommended` / `optional` / `conditionally_core`;
     machine-read by the completeness checker (SPEC.md §3).
   - `justification` — 1–2 sentences on *why the slot earns its place*: the
     concrete analytical, reproducibility, or legal consequence of omitting
     it. This is the per-slot version of SPEC.md's "why it matters" column.
   - `explanation` — 1–3 sentences of plain-language explanation for a
     reader with no climate-data or health-informatics background; goes one
     level more basic than the description rather than restating it.

`justification` and `explanation` are annotations rather than new metaslots
deliberately: LinkML has no mechanism for adding true metaslots without
forking the metamodel, and annotations are exactly its extension point for
this (the `tier` tag set the precedent). Anything reading the schema
programmatically (dashboard, docs generation, completeness checker) can pick
them up from `annotations`, same as `tier`.

## How to validate

From the project root, run `just setup` once (installs LinkML and the rest
of the dev toolchain via `uv`), then `just gen-project` to generate the
target artefacts (JSON Schema, SHACL, OWL, Python, …) and surface any
schema errors. Run `just lint` to lint the schema source files in
`src/linkml_microschemas_envar/schema/`. All Python entry-points are wrapped
in `uv run`; see the project root `justfile` for the exact recipes.
