# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status — VERY EARLY PROTOTYPE

Everything here is exploratory and will change. Do not treat schemas, examples, or design decisions as stable, normative, or production-ready. Worked examples may be partial; cross-references between modules may not yet be fully consistent.

## Tooling

- Python is managed with `uv`. ALL Python entry-points run inside `uv run` — never invoke `linkml`, `gen-project`, `pytest`, etc. directly from the host environment.
- The command runner is [`just`](https://github.com/casey/just/); project variables (`LINKML_SCHEMA_NAME=linkml_microschemas_envar`, `LINKML_SCHEMA_SOURCE_DIR=src/linkml_microschemas_envar/schema`) load from `config.public.mk`.
- Project-specific recipes go in `project.justfile`. It cannot override recipes defined in the root `justfile` (`just` bug #2540) — an override must be edited into the root file directly.

## Commands

- `just install` — install dev dependencies.
- `just gen-project` — regenerate all artifacts under `project/`. This is what surfaces schema errors.
- `just gen-doc` — regenerate Markdown docs into `docs/elements/`.
- `just site` — `gen-project` + `gen-doc`.
- `just lint` — `linkml-lint` over the schema sources.
- `just test` — full suite: schema gen, pytest, and `linkml-run-examples` over `tests/data/valid` (the passing `core`/`recommended`/`ideal` gradient) and `tests/data/invalid` (`core_missing` counter-examples that MUST fail validation).
- `just testdoc` — generate docs and serve locally via `mkdocs serve`.
- `just clean` — remove generated artifacts.
- Single Python test: `uv run pytest tests/path/to/test_file.py::test_name`.

**ALWAYS run `just test` after any change to the schema and/or datasets, and confirm it exits 0 before considering the work done.** It is exactly what CI runs; a single-test run or partial `gen-project` is not sufficient — the suite also cross-checks the datasets ledger, the tier/required invariants, and the standards index.

Gotcha: `tests/test_standards_index.py::test_every_todo_candidate_has_a_verdict` reads the repo-root `todo.md` (gitignored, local-only survey scratch list) and asserts every candidate has a verdict in `docs/standards-index/standards.yaml`; it skips when `todo.md` is absent, so **CI will never catch a missing verdict — only a local `just test` will**.

## Architecture

The substantive content is the LinkML schema set under `src/linkml_microschemas_envar/schema/`; everything else is scaffolding from the `linkml-project-copier` template. `linkml_microschemas_envar.yaml` is an umbrella importing fourteen sibling `envar_*.yaml` modules, one concern each (variable identity, data layout, spatial, temporal, source dataset, exposure model, uncertainty, linkage, tool run/provenance, heat metrics, health-layer/deposit, record composite, example record subclasses). Non-obvious placements: `envar_common.yaml` holds the shared enums/slots and imports the LinkML Microschema Profile; `envar_record.yaml` defines the top composite `EnvironmentalExposureRecord`.

### Readable top-level names, mapped to the profile

- `EnvironmentalExposureRecord` `instantiates: MicroschemaDefinition` from the [LinkML Microschema Profile](https://github.com/linkml/linkml-microschema-profile). `instantiates` is a metaclass relationship and does not constrain slot names, so the record uses readable domain names (`variable_identity`, `spatial_reference`, `temporal_reference`, `exposure_model`) mapped to the profile's `observation_type`/`location`/`temporality`/`methodology` via slot-level `implements` + `exact_mappings` (`msprofile:` prefix). Only `subject` is used verbatim.
- The profile's `observation_result` is deliberately **not** bound: values live in the companion data file (batch sidecar), and the profile marks it required — binding it would force an inline value and breaks `linkml-run-examples` (the Python dataclass does not honour the optional override).
- **Do not rename via the metamodel's `alias` in `slot_usage`** — the 2026-07 spike showed `gen-python` rejects it ("alias not permitted in slot_usage slot") even though validate/json-schema/pydantic accept it; re-declaring the imported profile slot locally fails with "Conflicting URIs"; `aliases` (plural) is documentation-only. Plain rename + `implements`/`exact_mappings` is the only route that survives the whole generator pipeline.
- `variable_name` in `VariableIdentity` is pure identity; column bindings into the companion data file live in the required `data_layout` (`DataLayout.value_column` etc.). Do not fold column names back into `VariableIdentity` — long/tidy layouts need the split (value column is literally `value`, rows selected by `variable_column`/`variable_key`).
- Full rationale and known drawbacks: `src/linkml_microschemas_envar/schema/README.md` — read it before renaming top-level slots or restructuring `EnvironmentalExposureRecord`.

### Tier annotations vs `required:` — keep them aligned

- Every slot carries `annotations.tier` (`core` / `recommended` / `optional` / `conditionally_core`); the completeness checker (`src/linkml_microschemas_envar/checker.py`) reads tiers from the schema and BLOCKS on missing Core slots.
- Invariant: **`tier: core` implies `required: true`** on induced slots (`slot_usage` overrides count). Enforced by `tests/test_schema.py::test_core_tier_implies_required`; the converse is deliberately not asserted.
- If a Core slot cannot honestly be hard-required, do NOT soften it — re-tier to `conditionally_core` with the context encoded in the schema.
- Conditionally-core contexts are **single-sourced from the schema** (SPEC §7.7): either a LinkML class `rule` on the owning class (preconditions restricted to `equals_string` / `equals_string_in` / `pattern` / `value_presence` — the vocabulary the generator pipeline and checker support) or `required: true` inside a conditional block. When adding one, write the rule in the owning module's YAML — never add lambdas to the checker. Only exceptions: the two cross-class contexts in `RESIDUAL_CONTEXT_PREDICATES` and the not-machine-decidable `source_homogenisation_status`, which carry a `tier_context` annotation.
- Pinned by `test_conditionally_core_contexts_are_single_sourced` and `test_rule_precondition_values_are_permissible` (renaming an enum value cannot silently kill a rule).
- The §4 tier tables in SPEC.md re-state the tiers in prose — update them in the same change.

### Edit-vs-generated boundary

- **Edit:** `src/linkml_microschemas_envar/schema/*.yaml` only.
- **Never edit:** `project/` (from `just gen-project`), `src/linkml_microschemas_envar/datamodel/` except `__init__.py`, and `docs/elements/` (from `just gen-doc`).
- Generated but **git-tracked** (regenerate after schema/tier changes, never hand-edit): `docs/schema_overview.md` + `docs/overview/index.html` (`just render-schema-overview`) and `docs/datasets/index.html` (`just gen-datasets-ledger`).
- The canonical worked example is `examples/daymet_tmax_phoenix_2022_07_19.yaml`.

## Other context

- Codespell / typos ignore lists live in `pyproject.toml` — add new generated paths to both if you add generators.
- The published Pages site deliberately mixes mkdocs-material pages with standalone HTML copied verbatim from `docs/` (`docs/slides/*.html`, `docs/overview/index.html`, `docs/datasets/index.html`). The visual inconsistency is known and deliberate — do not try to "fix" them into the mkdocs theme.
- The hand-embedded completeness dashboard was retired (2026-07) in favour of the computed datasets ledger; it survives only as a design artefact at `specs/dashboard/index.html` next to `specs/SPEC_DASHBOARD.md`. Do not re-add it to the mkdocs nav or wire it to checker JSON — one completeness page only, so they cannot drift.
- The **standards index** (`docs/standards-index/`): `standards.yaml` is the hand-curated source of truth, validated against the standalone `standards_index.schema.yaml` (deliberately NOT imported into the umbrella). `docs/standards-index/index.md` is generated by `just standards-index` — regenerate after editing `standards.yaml`, never hand-edit. Distinct from `docs/related-approaches.md` (narrative deep-dives). The populating survey lives under `surveys/study-env-exposure-metadata-standards/` (rerun via its `DESIGN.md`; deep-research at concurrency <= 2 to avoid Perplexity rate limits).
