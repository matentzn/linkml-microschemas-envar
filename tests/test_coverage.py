"""Tests for the standards-coverage annotation (`covered_by`).

Step 1 of specs/2026-07-03-standard-coverage-design.md is a TDD spike to
retire the serialization risk: prove that a nested `covered_by` annotation
survives the whole `just gen-project` generator pipeline AND that SchemaView
reads it back in the shape the coverage generator will consume. This module
starts with that read-back contract; the generator-clean half is asserted by
`just gen-project` / `just test`.
"""

from pathlib import Path

import pytest
from linkml_runtime import SchemaView

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = (
    REPO_ROOT / "src" / "linkml_microschemas_envar" / "schema" / "linkml_microschemas_envar.yaml"
)


@pytest.fixture(scope="module")
def schema_view() -> SchemaView:
    return SchemaView(str(SCHEMA_PATH))


def test_covered_by_reads_back_nested(schema_view: SchemaView) -> None:
    """SchemaView exposes the nested covered_by entry as structured data.

    The first entry is on `value_data_type`, which GAIA-OMOP verifiably
    supplies first-class (gaia_catalog meta_etl_*.json qudt:dataType
    numeric/float4). The coverage generator needs to read `extent`, `status`
    and `note` per standard id back out of the annotation.
    """
    slot = schema_view.get_slot("value_data_type")
    assert slot.annotations and "covered_by" in slot.annotations, (
        "value_data_type is missing its covered_by annotation"
    )
    # Nested-annotation form: covered_by -> {standard_id -> {field -> value}}.
    standards = slot.annotations["covered_by"].annotations
    assert "omop_gaia" in standards, f"expected an omop_gaia entry, got: {list(standards)}"
    entry = standards["omop_gaia"].annotations
    assert entry["extent"].value == "full"
    assert entry["status"].value == "verified"
    assert entry["note"].value
