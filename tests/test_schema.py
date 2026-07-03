"""Smoke tests for the EnVar microschema set.

These are the tests behind `just _test-python` (which regenerates the Python
datamodel first via `gen-python`). They cover three things:

1. the umbrella schema loads and exposes the expected composite record,
2. the generated Python datamodel imports,
3. every sidecar under tests/data/valid validates and every counter-example
   under tests/data/invalid fails validation (linkml-run-examples does not
   currently pick up the counter-examples, so this is the enforcement point
   for the must-fail gradient).
"""

from pathlib import Path

import pytest
from linkml.validator import validate_file
from linkml_runtime import SchemaView

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = (
    REPO_ROOT / "src" / "linkml_microschemas_envar" / "schema" / "linkml_microschemas_envar.yaml"
)
VALID_DIR = REPO_ROOT / "tests" / "data" / "valid"
INVALID_DIR = REPO_ROOT / "tests" / "data" / "invalid"

TARGET_CLASS = "EnvironmentalExposureRecord"


def _example_files(directory: Path) -> list[Path]:
    return sorted(directory.glob(f"{TARGET_CLASS}-*.yaml"))


@pytest.fixture(scope="module")
def schema_view() -> SchemaView:
    return SchemaView(str(SCHEMA_PATH))


def test_schema_loads_and_has_record(schema_view: SchemaView) -> None:
    record = schema_view.get_class(TARGET_CLASS)
    assert record is not None
    slots = {s.name for s in schema_view.class_induced_slots(TARGET_CLASS)}
    # The readable anatomy names plus the required layout binding.
    for expected in (
        "subject",
        "variable_identity",
        "spatial_reference",
        "temporal_reference",
        "data_layout",
    ):
        assert expected in slots


def test_generated_datamodel_imports() -> None:
    from linkml_microschemas_envar.datamodel import linkml_microschemas_envar as dm

    assert hasattr(dm, TARGET_CLASS)


@pytest.mark.parametrize(
    "example", _example_files(VALID_DIR), ids=lambda p: p.stem
)
def test_valid_examples_validate(schema_view: SchemaView, example: Path) -> None:
    # Pass the SchemaView-loaded SchemaDefinition, not the path: the validator
    # resolves the umbrella's sibling imports relative to CWD when handed a
    # path string, so a raw path only works when run from the schema directory.
    report = validate_file(example, schema_view.schema, TARGET_CLASS)
    messages = [r.message for r in report.results]
    assert not messages, f"{example.name} should validate but got: {messages}"


@pytest.mark.parametrize(
    "counter_example", _example_files(INVALID_DIR), ids=lambda p: p.stem
)
def test_counter_examples_fail_validation(
    schema_view: SchemaView, counter_example: Path
) -> None:
    report = validate_file(counter_example, schema_view.schema, TARGET_CLASS)
    assert report.results, f"{counter_example.name} must FAIL validation but passed"


def test_counter_examples_exist() -> None:
    # Guard against the silent-empty-directory failure mode: if the
    # counter-examples are renamed away from the ClassName-*.yaml convention,
    # the parametrized test above would pass vacuously.
    assert _example_files(INVALID_DIR), f"no counter-examples found in {INVALID_DIR}"
    assert _example_files(VALID_DIR), f"no examples found in {VALID_DIR}"
