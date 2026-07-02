# Heat Index demo — multi-input derived metric, Option-B decomposition

Workshop material for the question: *what happens when a derived heat metric is
computed from inputs that come from different products and disagree with each
other?* (See `SPEC.md` §4.6 `DerivedHeatMetric` / `equation_inputs` and
`PLAN.md` §4 tiering, §7 validation.)

## The point in one number

A single output value — **"Heat Index 44 °C"** — is computed from two physical
inputs that **diverge** on three axes that each independently change the result:

| Input | role | product | resolution | day boundary | aggregation |
|---|---|---|---|---|---|
| A | `air_temperature` | Daymet V4 | **1 km** | **local_midnight** | **maximum** |
| B | `relative_humidity` | ERA5 | **~31 km** | **utc** | **mean** |

The derived value silently inherits the **coarser** 31 km resolution and sits
across a **day-boundary mismatch** (a local-midnight daily max combined with a
UTC daily mean). A consumer who sees only "44 °C" cannot recover any of this.

## How Option B keeps it visible

Rather than flattening the inputs into light free-text descriptors on the
derived record, each input is its **own full sidecar**, and the derived record
references them as a **typed index into the provenance chain**:

- [`heat_index_input_a_tmax_daymet.yaml`](heat_index_input_a_tmax_daymet.yaml) — full TMAX sidecar (`provenance_id: 01HFA7K8R3M6XP-daymet-tmax`)
- [`heat_index_input_b_rh_era5.yaml`](heat_index_input_b_rh_era5.yaml) — full RH sidecar, the divergent one (`provenance_id: 01HFA7K8R3M6XP-era5-rh`)
- [`heat_index_derived.yaml`](heat_index_derived.yaml) — the `DerivedHeatMetric` record; its `derived_heat_metric.equation_inputs` lists each input's role and points (by `provenance_id`) at the sidecar above, and `provenance_chain` lists both upstream runs.

```yaml
equation_inputs:
- input_role: air_temperature
  input_provenance_id: "01HFA7K8R3M6XP-daymet-tmax"
  input_source_short_code: daymet_v4
- input_role: relative_humidity
  input_provenance_id: "01HFA7K8R3M6XP-era5-rh"
  input_source_short_code: era5
```

## The check it enables (`PLAN.md` §7)

Because each input is a dereferenceable sidecar, the completeness checker can
run a **cross-input consistency check**: with more than one `equation_inputs`
entry, follow each `input_provenance_id` and **WARN** when the inputs' day-
boundary conventions, temporal aggregation windows, or native spatial
resolutions differ. Here it would fire on all three. The divergence is allowed —
but it must be recorded through the decomposed sidecars, not absorbed into the
output value. This is the input-internal analogue of the exposure-vs-clinical
day-boundary check.

## Tiering note

`equation_inputs` (and the per-input role/provenance reference) is
**Conditionally-Core**: optional for a single-input metric, mandatory the moment
a metric has more than one input — mirroring the existing treatment of
`equation_variant` and the percentile-reference slots.

## Caveats (as with the sibling scenarios)

- These files use readable domain-grouped top-level keys (`variable_identity`,
  `spatial_reference`, …), which are now the schema's canonical names (the
  naming question in `SPEC.md` was resolved in favour of the readable names).
  They remain illustrative rather than validated.
- `cf_standard_name: heat_index` is **not** an official CF Standard Name — none
  exists for Heat Index; the slot is required, so a flagged placeholder is used.
- Hashes, digests, and numeric values are representative, not from a real run.
