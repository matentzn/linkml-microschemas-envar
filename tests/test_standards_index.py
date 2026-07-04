"""Tests for the standalone standards-index registry schema and renderer."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from linkml_runtime import SchemaView

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "docs" / "standards-index" / "standards_index.schema.yaml"
MINIMAL = REPO / "docs" / "standards-index" / "examples" / "minimal.yaml"


def test_schema_loads_expected_classes_and_enums():
    sv = SchemaView(str(SCHEMA))
    assert {"StandardsIndex", "StandardEntry", "TriageEntry"} <= set(sv.all_classes())
    rel = sv.get_enum("RelevanceEnum")
    assert set(rel.permissible_values) == {"in_scope", "peripheral", "out_of_scope"}
    cls = sv.get_enum("StandardClassEnum")
    assert set(cls.permissible_values) == {"general_standard", "pipeline_sidecar"}


def test_minimal_instance_validates():
    result = subprocess.run(
        ["uv", "run", "linkml-validate", "-s", str(SCHEMA),
         "-C", "StandardsIndex", str(MINIMAL)],
        cwd=str(REPO), capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "gen_standards_index", REPO / "scripts" / "gen_standards_index.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_render_index_groups_and_lists_entries():
    gen = _load_generator()
    registry = {
        "entries": [
            {"id": "dcat", "name": "DCAT", "standard_class": "general_standard",
             "relevance": "in_scope", "relevance_reason": "r1"},
            {"id": "degauss", "name": "DeGAUSS", "standard_class": "pipeline_sidecar",
             "relevance": "in_scope", "relevance_reason": "r2"},
        ],
        "triaged": [
            {"id": "geonames", "name": "GeoNames", "kind": "vocabulary",
             "relevance": "out_of_scope", "relevance_reason": "gazetteer"},
        ],
    }
    md = gen.render_index(registry)
    assert "## General standards" in md
    assert "## Pipeline sidecars" in md
    assert "## Triaged out" in md
    assert "DCAT" in md and "DeGAUSS" in md and "GeoNames" in md
    # DeGAUSS must appear under Pipeline sidecars, not General standards
    assert md.index("DeGAUSS") > md.index("## Pipeline sidecars")


TODO = REPO / "todo.md"


def _todo_candidates() -> set[str]:
    """Verbatim candidate names under the '## Environmental standards' heading."""
    lines = TODO.read_text().splitlines()
    out: set[str] = set()
    grabbing = False
    for line in lines:
        if line.strip().startswith("## Environmental standards"):
            grabbing = True
            continue
        if grabbing and line.startswith("## "):
            break
        if not grabbing:
            continue
        s = line.strip().strip('"').strip()
        if not s or s.startswith("(") or s.startswith("#"):
            continue
        out.add(s)
    return out


def _covered_candidates() -> set[str]:
    registry = yaml.safe_load((REPO / "docs" / "standards-index" / "standards.yaml").read_text()) or {}
    covered: set[str] = set()
    for bucket in ("entries", "triaged"):
        for e in registry.get(bucket) or []:
            covered.update(e.get("source_candidates") or [])
    return covered


def test_every_todo_candidate_has_a_verdict():
    if not TODO.exists():
        pytest.skip(
            "todo.md is a local-only scratch file (gitignored); "
            "the candidate-coverage gate only runs where it is present."
        )
    missing = _todo_candidates() - _covered_candidates()
    assert not missing, (
        "todo.md candidates with no verdict in standards.yaml "
        f"(add each to some entry/triaged source_candidates): {sorted(missing)}"
    )
