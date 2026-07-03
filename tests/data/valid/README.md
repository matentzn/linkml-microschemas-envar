# Worked records — the completeness gradient

Each variable (TMAX, PM2.5) is worked at three tiers, branded by the
[`SPEC.md`](../../../SPEC.md) terminology. All files here **validate** against
`EnvironmentalExposureRecord`; the deliberately-incomplete `core_missing`
counter-examples live in [`../invalid/`](../invalid/) and **fail** validation.

| Tier | File suffix | What it carries |
|---|---|---|
| **core** | `_core` | Only the required Core fields — the minimum that still validates. |
| **recommended** | `_recommended` | Core + the Recommended fields needed for real reproducibility. |
| **ideal** | `_ideal` | Everything, including Optional discovery/deposit enrichment. |

Files (the `EnvironmentalExposureRecord-` prefix is required by the
`linkml-run-examples` `ClassName-suffix.yaml` convention):

- `EnvironmentalExposureRecord-tmax_core.yaml` · `-tmax_recommended.yaml` · `-tmax_ideal.yaml`
- `EnvironmentalExposureRecord-pm25_core.yaml` · `-pm25_recommended.yaml` · `-pm25_ideal.yaml`

Run the whole gradient (valid must pass, invalid must fail) with `just test`
(or `just _test-examples`).

Notes:
- **Naming.** These use the readable domain top-level keys (`variable_identity`,
  `spatial_reference`, `temporal_reference`, `exposure_model`), which are now the
  schema's canonical names; each maps to its LinkML Microschema Profile anatomy
  slot via `implements` (decision recorded in the schema
  [`README.md`](../../../src/linkml_microschemas_envar/schema/README.md)).
- **No inline value / no PHI.** Records bind no `observation_result`; the value(s)
  live in the companion CSV/parquet (shown as a trailing comment). Subjects are
  opaque cohort handles.
