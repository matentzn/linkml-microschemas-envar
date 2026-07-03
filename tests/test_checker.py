"""Tests for the metadata-completeness checker.

The six gradient files are the contract: each tier-branded sidecar must score
the way its brand promises (core files Core-clean, readiness strictly climbing
core → recommended → ideal), and the counter-examples must come out BLOCKED
with exactly their deliberately-dropped Core fields.
"""

from pathlib import Path

import pytest
from linkml_microschemas_envar.checker import (
    CompletenessChecker,
    format_report,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
VALID_DIR = REPO_ROOT / "tests" / "data" / "valid"
INVALID_DIR = REPO_ROOT / "tests" / "data" / "invalid"


@pytest.fixture(scope="module")
def checker() -> CompletenessChecker:
    return CompletenessChecker()


def gradient(checker: CompletenessChecker, variable: str) -> dict:
    return {
        tier: checker.check_file(VALID_DIR / f"EnvironmentalExposureRecord-{variable}_{tier}.yaml")
        for tier in ("core", "recommended", "ideal")
    }


@pytest.mark.parametrize("variable", ["tmax", "pm25"])
def test_gradient_is_monotonic_and_core_clean(checker, variable):
    reports = gradient(checker, variable)
    for tier, report in reports.items():
        assert report.valid, f"{variable}_{tier} must validate"
        assert not report.blocking, f"{variable}_{tier} must not be BLOCKED: {report.blocking}"
        got, of = report.scores["core"]
        assert got == of, f"{variable}_{tier} must be Core-clean ({got}/{of})"
    assert (
        reports["core"].readiness < reports["recommended"].readiness < reports["ideal"].readiness
    ), f"{variable} readiness must climb core → recommended → ideal"


@pytest.mark.parametrize("variable", ["tmax", "pm25"])
def test_counter_examples_are_blocked(checker, variable):
    report = checker.check_file(
        INVALID_DIR / f"EnvironmentalExposureRecord-{variable}_core_missing.yaml"
    )
    assert report.valid is False, "counter-examples must fail validation"
    assert report.blocked
    # the deliberately-dropped required fields must surface as blocking
    assert "day_boundary_convention" in report.blocking


def test_conditionally_core_context_switches(checker):
    """A long-format layout makes variable_column/variable_key Core; wide does not."""
    base = {
        "data_layout": {"table_orientation": "wide", "value_column": "tmax"},
    }
    report = checker.check(base)
    assert "variable_column" not in report.blocking
    long_layout = {
        "data_layout": {"table_orientation": "long", "value_column": "value"},
    }
    report = checker.check(long_layout)
    assert "variable_column" in report.blocking
    assert "variable_key" in report.blocking


def test_missing_reason_explains_recommended_but_not_core(checker):
    instance = {
        # recommended slot absent + reason -> explained (counts as present)
        "variable_identity": {"target_concept_id_missing_reason": "not_provided_by_source"},
        # core slot absent + reason -> still blocking
        "temporal_reference": {"day_boundary_convention_missing_reason": "under_investigation"},
    }
    report = checker.check(instance)
    assert "target_concept_id" in report.explained_null
    assert "target_concept_id" not in report.missing["recommended"]
    assert "day_boundary_convention" in report.blocking


def test_heat_metric_module_only_counts_when_present(checker):
    without = checker.check({})
    assert "heat_metric_family" not in [s.name for s in without.slots]
    with_metric = checker.check({"derived_heat_metric": {"heat_metric_family": "heat_index"}})
    names = {s.name: s for s in with_metric.slots}
    assert "heat_metric_family" in names
    # equation slots switch to Core in the derived-metric context
    assert names["equation_variant"].effective_tier == "core"


def test_report_round_trips_to_dict_and_text(checker):
    report = checker.check_file(VALID_DIR / "EnvironmentalExposureRecord-tmax_ideal.yaml")
    data = report.as_dict()
    assert data["scores"]["core"][0] == data["scores"]["core"][1]
    assert data["blocked"] is False
    text = format_report(report)
    assert "Reproducibility-readiness" in text
