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
- `just test` — runs `_test-schema` (gen-project into `tmp/`), `_test-python` (pytest, after regenerating Python datamodel), and `_test-examples` (`linkml-run-examples` over `tests/data/valid` and `tests/data/invalid`, writing into `examples/output/`). The `tests/data/valid` and `tests/data/invalid` directories are currently empty — example-based tests will run but find nothing until they are populated.
- `just testdoc` — generate docs and serve them locally via `mkdocs serve`.
- `just clean` — remove generated artifacts under `project/` and regenerated docs under `docs/elements/`.
- Run a single Python test: `uv run pytest tests/path/to/test_file.py::test_name`.

## Architecture

The substantive content is the LinkML schema set under `src/linkml_microschemas_envar/schema/`. Everything else is scaffolding from the `linkml-project-copier` template (`.copier-answers.yml` records the template version).

### Schema layout (microschema-per-concern)

`linkml_microschemas_envar.yaml` is an umbrella that imports thirteen sibling modules. Each module isolates one concern:

| Module | Class(es) | Concern |
|---|---|---|
| `envar_common.yaml` | enums + shared slots | `MissingReasonEnum`, `DataTypeEnum`, `OmopConceptStatusEnum`; imports the **LinkML Microschema Profile** |
| `envar_variable.yaml` | `VariableIdentity` | CF standard name, UCUM, OMOP, ECTO, ENVO |
| `envar_spatial.yaml` | `SpatialReference` | grid, CRS, extraction method |
| `envar_temporal.yaml` | `TemporalReference` | resolution, day-boundary convention, calendar |
| `envar_source.yaml` | `SourceDataset` | upstream product identity, DOI, license |
| `envar_model.yaml` | `ExposureModel` | model class, inputs, biases |
| `envar_uncertainty.yaml` | `Uncertainty` | per-value + aggregate uncertainty |
| `envar_linkage.yaml` | `LinkageMethod` | gridded-to-patient linkage |
| `envar_toolrun.yaml` | `ToolRun`, `ProvenanceChain` | exact invocation + W3C-PROV chain |
| `envar_heat_metric.yaml` | `DerivedHeatMetric` | WBGT/HI/UTCI/heat-wave methodology |
| `envar_omop.yaml` | `OmopLinkage`, `DepositMetadata` | OMOP/BDC linkage + FAIR deposit |
| `envar_record.yaml` | `EnvironmentalExposureRecord` | top composite — binds profile slots to envar ranges |
| `envar_examples.yaml` | `DailyMaxTemperatureRecord`, `DailyMinTemperatureRecord`, `WetBulbGlobeTemperatureOutdoorRecord`, `ExtremeHeatDayFlagRecord` | concrete record subclasses |

### Key design decision: profile-slot names at the top level

`EnvironmentalExposureRecord` `instantiates: MicroschemaDefinition` from the [LinkML Microschema Profile](https://github.com/linkml/linkml-microschema-profile). The six profile anatomy slots (`subject`, `observation_type`, `location`, `temporality`, `methodology`, `observation_result`) are used **verbatim** at the top level, with envar-specific classes bound as their ranges via `slot_usage`. Envar concerns with no profile equivalent (`source_dataset`, `linkage_method`, `tool_run`, `provenance_chain`, `derived_heat_metric`, `omop_linkage`, `deposit_metadata`, `uncertainty`) are added as additional top-level slots. The full rationale and known drawbacks are documented in `src/linkml_microschemas_envar/schema/README.md` — read that before renaming top-level slots or restructuring `EnvironmentalExposureRecord`.

### Edit-vs-generated boundary

- **Edit:** `src/linkml_microschemas_envar/schema/*.yaml` only.
- **Do not edit:** anything under `project/` (regenerated by `just gen-project`), anything under `src/linkml_microschemas_envar/datamodel/` except `__init__.py` (Python dataclasses + Pydantic regenerated from the schema), and `docs/elements/` (regenerated by `just gen-doc`).
- The canonical worked example is `examples/daymet_tmax_phoenix_2022_07_19.yaml`. `tests/data/valid` and `tests/data/invalid` are empty placeholders for `linkml-run-examples`-based test cases.

## Other context

- Project-specific `just` recipes go in `project.justfile` (imported by the root `justfile`). The root `justfile` cannot be edited to override recipes due to a known `just` bug (#2540) — overrides must live in the root file itself.
- `.pre-commit-config.yaml` and `.yamllint.yaml` exist; pre-commit is not wired into a `just` recipe.
- Codespell / typos ignore the generated datamodel files and `project/*`; add new generated paths to both lists in `pyproject.toml` if you add new generators.
