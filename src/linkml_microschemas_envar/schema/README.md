# EnVar Microschemas

These LinkML microschemas describe the *sidecar metadata* that travels
alongside a value (or value series) emitted by an upstream environmental-data
tool (Amadeus, DeGAUSS, …) and consumed downstream by OMOP or another
health-data layer. The top class is `EnvironmentalExposureRecord`; it
composes variable identity, spatial / temporal reference, source dataset,
exposure model, uncertainty, linkage method, tool-run / W3C-PROV provenance
chain, optional derived-heat-metric methodology, OMOP linkage hooks, and
FAIR-deposit metadata. The schema implements §1.1 of
`pipeline/heat-omop-slice/envar-heat-scenario-requirements.md`.

## Modules

| File | Class(es) | Purpose |
|---|---|---|
| `envar_common.yaml` | (enums, shared slots) | Shared `MissingReasonEnum`, `DataTypeEnum`, `OmopConceptStatusEnum`; `schema_version`, `provenance_id`. Imports the LinkML Microschema Profile. |
| `envar_variable.yaml` | `VariableIdentity` | CF standard name, UCUM units, OMOP concept ID, ECTO / ENVO bindings, plausible value range. Covers req §2. |
| `envar_spatial.yaml` | `SpatialReference` | Native grid, CRS, extent, extraction method, target geography. Covers req §3. |
| `envar_temporal.yaml` | `TemporalReference` | Resolution, aggregation, day-boundary convention, coverage, calendar, lag alignment. Covers req §4. |
| `envar_source.yaml` | `SourceDataset` | Upstream product identity, DOI, version, license, native format, homogenisation status. Covers req §5. |
| `envar_model.yaml` | `ExposureModel` | Model type, inputs, paper DOI, known biases, uncertainty field, bias correction. Covers req §6. |
| `envar_uncertainty.yaml` | `Uncertainty` | Per-value and aggregate uncertainty, quality flags, missing-data handling. Covers req §8. |
| `envar_linkage.yaml` | `LinkageMethod` | Gridded-to-patient linkage strategy, buffer parameters, propagated geocoder quality. Covers req §9. |
| `envar_toolrun.yaml` | `ToolRun`, `ProvenanceChain` | Exact tool invocation and the ordered W3C-PROV chain of upstream runs. Covers req §10 and §11. |
| `envar_heat_metric.yaml` | `DerivedHeatMetric` | Heat-metric methodology: family, equation variant, indoor / outdoor, percentile reference period. Covers req §7. |
| `envar_omop.yaml` | `OmopLinkage`, `DepositMetadata` | OMOP / BDC linkage hooks and FAIR-deposit slots. Covers req §12 and §13. |
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

### Top-level slot names conform to the LinkML Microschema Profile (Option A)

The `EnvironmentalExposureRecord` class `instantiates: MicroschemaDefinition`
from the [LinkML Microschema Profile](https://github.com/linkml/linkml-microschema-profile),
which contributes six required anatomy slots: `subject`, `observation_type`,
`location`, `temporality`, `methodology`, `observation_result`.

We chose to **use the profile slot names verbatim at the top level of the
sidecar document**, with envar-specific complex classes bound as their
ranges via `slot_usage`:

| Profile slot | Bound range | Envar concept |
|---|---|---|
| `subject` | `string` | Opaque patient / cohort handle (PHI-free) |
| `observation_type` | `VariableIdentity` | What variable is being captured |
| `location` | `SpatialReference` | Where — native grid + extraction |
| `temporality` | `TemporalReference` | When — resolution + day boundary |
| `methodology` | `ExposureModel` | How — the exposure model |
| `observation_result` | `ValueMicroschemaDefinition` (optional) | Single value, if applicable |

The remaining envar concerns that have no profile equivalent —
`source_dataset`, `linkage_method`, `tool_run`, `provenance_chain`,
`derived_heat_metric`, `omop_linkage`, `deposit_metadata`, `uncertainty` —
are surfaced as additional top-level slots alongside the profile slots.

### Why this choice

- **Semantic interoperability across domains.** A meta-analyst reading both
  a clinical-microschema record (`measurement_value`, `subject_identifier`)
  and an environmental sidecar sees the same six anatomy slots in both. The
  microschema-profile's role as a cross-domain anchor only works if domain
  schemas actually use its slots.
- **Schema reusability.** Other environmental-exposure schemas can compose
  our microschema classes (e.g. `LinkageMethod`) without inheriting an
  envar-specific top-level vocabulary.
- **Conformance over readability.** The profile is opinionated; partially
  opting out (Option B in the design conversation) signals to downstream
  consumers that we're a special case, which has higher long-run cost than
  the readability hit.

### Known drawbacks

- **Less obvious to a domain-data reader.** A first-time reader looking at
  a Daymet sidecar sees `observation_type:` instead of `variable_identity:`,
  `location:` instead of `spatial_reference:`, `temporality:` instead of
  `temporal_reference:`. The names are abstract; without the schema docs
  open, the mapping is not self-evident. The worked example
  ([`examples/daymet_tmax_phoenix_2022_07_19.yaml`](../../../../examples/daymet_tmax_phoenix_2022_07_19.yaml))
  is the canonical Rosetta-stone.
- **`methodology` is narrower than the noun suggests.** The profile has
  one `methodology` slot, but environmental exposures need to describe
  several methodology-adjacent concerns (the upstream source product, the
  model class, the tool that ran, the W3C-PROV chain, the heat-derivation
  logic). We bind `methodology` to `ExposureModel` only and surface the
  rest as separate envar-extension slots. The split is a judgment call;
  someone could reasonably argue everything-methodology should hang off a
  single composite under `methodology:`.
- **`observation_result` is overridden to optional.** Per-batch sidecars
  describe a CSV / parquet file that contains many values; there is no
  single value to attach. The profile's `required: true` is relaxed via
  `slot_usage`. Per-record sidecars (one value per document) may still
  populate it with a `Quantity`.
- **Adoption friction for environmental-data engineers.** Cole Brokamp,
  Kyle Messier, and the C-HER team are domain experts; they will read the
  sidecar before they read the profile. The chosen names trade their
  first-read clarity for cross-domain consistency.

### When to revisit

Revisit this decision if (a) the environmental-data community
substantially adopts a different anatomy vocabulary (e.g. CF / DCAT /
DataCite slot names) that conflicts with the profile, or (b) the profile
itself evolves its slot naming. The mapping in `slot_usage` on
`EnvironmentalExposureRecord` is the single place to change.

## How to validate

From the project root, run `just setup` once (installs LinkML and the rest
of the dev toolchain via `uv`), then `just gen-project` to generate the
target artefacts (JSON Schema, SHACL, OWL, Python, …) and surface any
schema errors. Run `just lint` to lint the schema source files in
`src/linkml_microschemas_envar/schema/`. All Python entry-points are wrapped
in `uv run`; see the project root `justfile` for the exact recipes.
