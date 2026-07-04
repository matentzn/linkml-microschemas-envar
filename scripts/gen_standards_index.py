"""Render docs/standards-index/index.md from the standards registry YAML.

Reads the hand-curated registry (docs/standards-index/standards.yaml), which
validates against docs/standards-index/standards_index.schema.yaml, and emits a
grouped, deterministic markdown index. Doc-generator sibling to
scripts/gen_datasets_ledger.py.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "docs" / "standards-index" / "standards.yaml"
OUT = REPO / "docs" / "standards-index" / "index.md"

_COLUMNS = [
    ("name", "Standard"),
    ("unit_of_description", "Unit"),
    ("primary_purpose", "Purpose"),
    ("layer", "Layer"),
    ("carries_derivation_metadata", "Derivation?"),
    ("relevance", "Relevance"),
    ("envar_relation", "EnVar relation"),
]


def _cell(entry: dict, key: str) -> str:
    val = entry.get(key, "")
    if key == "name" and entry.get("spec_url"):
        return f"[{val}]({entry['spec_url']})"
    return str(val or "").replace("|", "\\|")


def _table(entries: list[dict]) -> str:
    if not entries:
        return "_None yet._\n"
    header = "| " + " | ".join(h for _, h in _COLUMNS) + " |"
    sep = "| " + " | ".join("---" for _ in _COLUMNS) + " |"
    rows = ["| " + " | ".join(_cell(e, k) for k, _ in _COLUMNS) + " |" for e in entries]
    return "\n".join([header, sep, *rows]) + "\n"


def _reconciliation_section(entries: list[dict]) -> str:
    lines = ["| Standard | Status | Where |", "| --- | --- | --- |"]
    for e in entries:
        status = e.get("reconciliation", "")
        ref = str(e.get("reconciliation_ref", "")).replace("|", "\\|")
        lines.append(f"| {e.get('name','')} | {status} | {ref} |")
    return "\n".join(lines) + "\n"


def render_index(registry: dict) -> str:
    entries = registry.get("entries") or []
    triaged = registry.get("triaged") or []

    def by_class(cls: str) -> list[dict]:
        return sorted(
            (e for e in entries if e.get("standard_class") == cls),
            key=lambda e: e.get("id", ""),
        )

    parts: list[str] = []
    parts.append("# Standards index\n")
    parts.append(
        "A survey of approaches that record *metadata about environmental-exposure "
        "data* for reuse, reproducibility, and meta-analysis. Two classes are kept "
        "apart deliberately: **general standards** intended to be reusable across "
        "producers, and **pipeline sidecars** — structured but per-pipeline "
        "documentative formats. Generated from `standards.yaml`; do not edit by hand.\n"
    )
    parts.append("## General standards\n")
    parts.append(_table(by_class("general_standard")))
    parts.append("## Pipeline sidecars\n")
    parts.append(_table(by_class("pipeline_sidecar")))
    parts.append("## Reconciliation with the niehs inventory\n")
    parts.append(_reconciliation_section(entries))
    parts.append("## Triaged out\n")
    parts.append(
        "Candidates considered and ruled out of the first-class index, kept for "
        "auditability.\n"
    )
    for t in sorted(triaged, key=lambda t: t.get("id", "")):
        parts.append(
            f"- **{t.get('name','')}** ({t.get('kind','')}) — "
            f"{t.get('relevance','out_of_scope')}: {t.get('relevance_reason','')}"
        )
    return "\n".join(parts) + "\n"


def main() -> None:
    registry = yaml.safe_load(REGISTRY.read_text()) or {}
    OUT.write_text(render_index(registry))
    print(f"Wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
