# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status — VERY EARLY PROTOTYPE

This repository is a **very early prototype for illustration purposes**. The schemas, examples, and design decisions are exploratory and will change. Do not treat anything here as stable, normative, or production-ready. Worked examples may be partial; cross-references between modules may not yet be fully consistent.

## Tooling baseline

- Python is managed with `uv` (lock file: `uv.lock`); install with `just install` (= `uv sync --group dev`).
- All Python entry-points run inside `uv run` — never invoke `linkml`, `gen-project`, `pytest`, etc. directly from the host environment.
- The command runner is [`just`](https://github.com/casey/just/). The root `justfile` reads project variables from `config.public.mk` (loaded via `set dotenv-load`); `LINKML_SCHEMA_NAME=linkml_microschemas_envar` and `LINKML_SCHEMA_SOURCE_DIR=src/linkml_microschemas_envar/schema` come from there.
- `just --list` shows all recipes. Hidden recipes are prefixed with `_`.

## Commands

- `just install` — install dev dependencies.
- `just gen-project` — regenerate all artifacts under `project/` (JSON Schema, SHACL, OWL TTL, Java, TypeScript, Pydantic, dataclasses). This is what surfaces schema errors.
- `just gen-doc` — regenerate Markdown docs into `docs/elements/` plus a merged `docs/schema/<schema_name>.yaml`.
- `just site` — `gen-project` + `gen-doc`.
- `just lint` — `linkml-lint` over `src/linkml_microschemas_envar/schema/`.
- `just test` — runs `_test-schema` (gen-project into `tmp/`), `_test-python` (pytest, after regenerating Python datamodel), and `_test-examples` (`linkml-run-examples` over `tests/data/valid` and `tests/data/invalid`, writing into `examples/output/`). `tests/data/valid` holds the passing `core`/`recommended`/`ideal` gradient (`EnvironmentalExposureRecord-{tmax,pm25}_*.yaml`) and `tests/data/invalid` holds the `core_missing` counter-examples that must fail validation.
- `just testdoc` — generate docs and serve them locally via `mkdocs serve`.
- `just clean` — remove generated artifacts under `project/` and regenerated docs under `docs/elements/`.
- Run a single Python test: `uv run pytest tests/path/to/test_file.py::test_name`.

**ALWAYS run the full CI suite (`just test`) after any change to datasets and/or the schema, and confirm it exits 0 before considering the work done.** `just test` is exactly what CI (`.github/workflows/main.yaml`) runs, so a green `just test` locally is the gate. A single-test run or a partial `gen-project` is not sufficient — the suite also cross-checks the datasets ledger, the tier/required invariants, and the standards index against `todo.md`. Note that `tests/test_standards_index.py::test_every_todo_candidate_has_a_verdict` reads the repo-root `todo.md` (the survey candidate list under its `## Environmental standards` heading) and asserts every candidate has a verdict in `docs/standards-index/standards.yaml`. `todo.md` is a **local-only scratch file (gitignored)**, so this candidate-coverage gate only runs locally where the file is present; the test `pytest.skip`s when `todo.md` is absent (e.g. in CI). If you add a candidate to `todo.md`, run `just test` locally to confirm it has a verdict — CI will not catch a missing one.

## Architecture

The substantive content is the LinkML schema set under `src/linkml_microschemas_envar/schema/`. Everything else is scaffolding from the `linkml-project-copier` template (`.copier-answers.yml` records the template version).

### Schema layout (microschema-per-concern)

`linkml_microschemas_envar.yaml` is an umbrella that imports fourteen sibling modules. Each module isolates one concern:

| Module | Class(es) | Concern |
|---|---|---|
| `envar_common.yaml` | enums + shared slots | `MissingReasonEnum`, `DataTypeEnum`, `ConceptStatusEnum`, `PhiStatusEnum`; shared `schema_version`, `provenance_id`, `phi_status`; imports the **LinkML Microschema Profile** |
| `envar_variable.yaml` | `VariableIdentity` | CF standard name, UCUM, target-vocabulary concept id + status, ECTO, ENVO |
| `envar_layout.yaml` | `DataLayout` | column bindings into the companion data file (value/subject/time/uncertainty/QA columns, wide-vs-long orientation) |
| `envar_spatial.yaml` | `SpatialReference` | grid, CRS, extraction method |
| `envar_temporal.yaml` | `TemporalReference` | resolution, day-boundary convention, calendar |
| `envar_source.yaml` | `SourceDataset` | upstream product identity, DOI, license |
| `envar_model.yaml` | `ExposureModel` | model class, inputs, biases |
| `envar_uncertainty.yaml` | `Uncertainty` | per-value + aggregate uncertainty |
| `envar_linkage.yaml` | `LinkageMethod` | gridded-to-patient linkage |
| `envar_toolrun.yaml` | `ToolRun`, `ProvenanceChain` | exact invocation + W3C-PROV chain |
| `envar_heat_metric.yaml` | `DerivedHeatMetric` | WBGT/HI/UTCI/heat-wave methodology |
| `envar_health_layer.yaml` | `HealthLayerLinkage`, `DepositMetadata` | health-data-layer linkage (OMOP, BDC, …) + FAIR deposit |
| `envar_record.yaml` | `EnvironmentalExposureRecord` | top composite — binds profile slots to envar ranges |
| `envar_examples.yaml` | `DailyMaxTemperatureRecord`, `DailyMinTemperatureRecord`, `WetBulbGlobeTemperatureOutdoorRecord`, `ExtremeHeatDayFlagRecord` | concrete record subclasses |

### Key design decision: readable top-level names, mapped to the profile

`EnvironmentalExposureRecord` `instantiates: MicroschemaDefinition` from the [LinkML Microschema Profile](https://github.com/linkml/linkml-microschema-profile). `instantiates` is a metaclass relationship — it does not constrain slot names — so the record uses **readable domain names** for the profile anatomy: `variable_identity`, `spatial_reference`, `temporal_reference`, `exposure_model` (mapped to the profile's `observation_type`, `location`, `temporality`, `methodology` via slot-level `implements`/`exact_mappings` with the `msprofile:` prefix). Only `subject` is used verbatim. `observation_result` is intentionally **not** bound: a batch sidecar carries values in the companion data file, and the profile marks `observation_result` required — keeping it would force every record to inline an (abstract-ranged) value and breaks `linkml-run-examples` (which instantiates the Python dataclass, where the optional override does not propagate). It was therefore dropped from the record's slot list. Do not try to rename via the metamodel's `alias` in `slot_usage` — the 2026-07 spike showed `linkml-validate`/`gen-json-schema`/`gen-pydantic` honour it but `gen-python` fails with "alias not permitted in slot_usage slot", and re-declaring the imported profile slot locally fails with "Conflicting URIs"; `aliases` (plural) is documentation-only. Plain rename + slot-level `implements`/`exact_mappings` is the only route that survives the whole generator pipeline. Envar concerns with no profile equivalent (`data_layout`, `source_dataset`, `linkage_method`, `tool_run`, `provenance_chain`, `derived_heat_metric`, `health_layer_linkage`, `deposit_metadata`, `uncertainty`, and the record-root `phi_status`) are added as additional top-level slots. `variable_name` in `VariableIdentity` is pure identity; the column binding into the companion data file lives in `data_layout` (`DataLayout.value_column` etc.), which is required. Rationale for the split: identity and column binding come apart for long/tidy data files, where the value column is literally named `value` and the record's rows are selected by `variable_column`/`variable_key` — do not fold column names back into `VariableIdentity`. The full rationale and known drawbacks are documented in `src/linkml_microschemas_envar/schema/README.md` — read that before renaming top-level slots or restructuring `EnvironmentalExposureRecord`.

### Tier annotations vs `required:` — keep them aligned

Every slot carries `annotations.tier` (`core` / `recommended` / `optional` / `conditionally_core`); the completeness checker (`src/linkml_microschemas_envar/checker.py`) reads tiers from the schema and BLOCKS on missing Core slots. The invariant is **`tier: core` implies `required: true`** on induced slots (so `slot_usage` overrides count) — otherwise LinkML validation passes sidecars the checker rejects. It is enforced by `tests/test_schema.py::test_core_tier_implies_required`; the converse (required-implies-core) is deliberately not asserted. When a Core slot cannot honestly be hard-required (e.g. it only applies to some products), the fix is **not** a soft `core` but re-tiering to `conditionally_core` with its context encoded in the schema. **Conditionally-core contexts are single-sourced from the schema (SPEC §7.7, done 2026-07)**: either a LinkML class `rule` on the owning class (preconditions restricted to `equals_string` / `equals_string_in` / `pattern` / `value_presence` — the vocabulary the whole generator pipeline and the checker's evaluator support; exported as JSON-Schema `if`/`then`, so validation itself enforces in-context requiredness) or `required: true` inside a conditional block (block-presence contexts like the equation slots in `DerivedHeatMetric`). The only Python predicates left are the two cross-class contexts in `RESIDUAL_CONTEXT_PREDICATES` (`extraction_buffer_m`, `population_weighting_source` — class rules cannot see across classes); these and the not-machine-decidable `source_homogenisation_status` carry a `tier_context` annotation. Two tests pin this: `test_conditionally_core_contexts_are_single_sourced` (no context may exist only in prose or only in Python) and `test_rule_precondition_values_are_permissible` (renaming an enum value cannot silently kill a rule). When adding a conditionally-core slot, write the rule in the owning module's YAML — do not add lambdas to the checker. The §4 tier tables in SPEC.md re-state the tiers in prose and must be updated in the same change.

### Edit-vs-generated boundary

- **Edit:** `src/linkml_microschemas_envar/schema/*.yaml` only.
- **Do not edit:** anything under `project/` (regenerated by `just gen-project`), anything under `src/linkml_microschemas_envar/datamodel/` except `__init__.py` (Python dataclasses + Pydantic regenerated from the schema), and `docs/elements/` (regenerated by `just gen-doc`).
- Also generated but **git-tracked** (regenerate after schema/tier changes, never hand-edit): `docs/schema_overview.md` + `docs/overview/index.html` (`just render-schema-overview`) and `docs/datasets/index.html` (`just gen-datasets-ledger`); both recipes live in `project.justfile` and run scripts under `scripts/`.
- The canonical worked example is `examples/daymet_tmax_phoenix_2022_07_19.yaml`. The tier-branded gradient lives in `tests/data/valid/` (passing) and `tests/data/invalid/` (`core_missing`, must fail), exercised by `just test` via `linkml-run-examples`.

## Other context

- Project-specific `just` recipes go in `project.justfile` (imported by the root `justfile`). The root `justfile` cannot be edited to override recipes due to a known `just` bug (#2540) — overrides must live in the root file itself.
- `.pre-commit-config.yaml` and `.yamllint.yaml` exist; pre-commit is not wired into a `just` recipe.
- Codespell / typos ignore the generated datamodel files and `project/*`; add new generated paths to both lists in `pyproject.toml` if you add new generators.
- The published Pages site (gh-pages, built by `mkdocs gh-deploy` in `.github/workflows/deploy-docs.yaml`) mixes mkdocs-material-rendered pages with standalone HTML that mkdocs copies verbatim from `docs/`: the hand-authored `docs/slides/*.html` (self-contained slide decks) and the generated `docs/overview/index.html` + `docs/datasets/index.html`. These carry their own styling and are outside the mkdocs theme, so the site looks visually inconsistent between them — this is known and deliberate; do not try to "fix" them into the mkdocs theme.
- The hand-embedded, illustrative completeness dashboard was **retired (2026-07)** in favour of the computed datasets ledger: it lives on as a design artefact at `specs/dashboard/index.html` next to `specs/SPEC_DASHBOARD.md` (whose §4 scoring/BLOCKED semantics the checker implements, and §5 visual design the ledger follows). Do not re-add it to the mkdocs nav or wire it to checker JSON — one completeness page, the ledger, so they cannot drift apart.
- The **standards index** (`docs/standards-index/`) catalogues external metadata standards and pipeline sidecars for environmental-exposure data. `standards.yaml` is the hand-curated source of truth, validated against the standalone `standards_index.schema.yaml` (deliberately **not** imported into the umbrella, so it never enters `just gen-project`); `docs/standards-index/index.md` is generated from it by `just standards-index` (git-tracked, in the mkdocs nav, never hand-edit — regenerate after editing `standards.yaml`). Entries carry deep-research-verified `evidence` URLs. It is distinct from `docs/related-approaches.md` (narrative deep-dives of five standards) and the per-slot coverage work (`docs/superpowers/specs/2026-07-03-standard-coverage-design.md`). The survey that populated it lives under `surveys/study-env-exposure-metadata-standards/` (rerun via that dir's `DESIGN.md`; launch deep-research at concurrency <= 2 to avoid Perplexity rate limits).
