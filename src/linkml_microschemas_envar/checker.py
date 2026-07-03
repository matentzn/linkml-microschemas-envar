"""Metadata-completeness checker for EnVar sidecars.

Scores a microschema-conformant sidecar against the tier annotations carried
by the schema slots (``annotations.tier``: ``core`` / ``recommended`` /
``optional`` / ``conditionally_core``), so the checker can never disagree
with SPEC.md — the tiers are read from the schema, not re-declared here.

Scoring policy (mirrors SPEC.md §3 and specs/SPEC_DASHBOARD.md §4):

- The slot universe is every tier-annotated slot reachable from the target
  class by walking inlined class ranges, counted once per slot name.
- ``*_missing_reason`` slots are meta-slots: they never count toward the
  meters. Instead, a missing slot whose sibling ``<name>_missing_reason``
  is populated counts as an *explained null* — information, not absence
  (SPEC §3 "null with reason") — and is scored as present but reported
  separately.
- ``conditionally_core`` slots are optional in general and Core in their
  stated context. The context predicates are not yet encoded in the schema
  (SPEC §7.7), so this module carries them in ``CONTEXT_PREDICATES``;
  a conditionally-core slot with no predicate, or out of context, is scored
  as Optional. In context it is scored as Core, including BLOCKING.
- readiness = 100 · (0.5·core_frac + 0.4·recommended_frac + 0.1·optional_frac).
- Any missing Core (or in-context conditionally-core) slot lands in
  ``blocking`` and stamps the report BLOCKED.

Validation runs before scoring when the full ``linkml`` package is
available (it is a dev dependency; the installed package only requires
``linkml-runtime``); otherwise the report notes that validation was skipped.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml
from linkml_runtime import SchemaView

DEFAULT_SCHEMA = Path(__file__).parent / "schema" / "linkml_microschemas_envar.yaml"
DEFAULT_TARGET_CLASS = "EnvironmentalExposureRecord"

MISSING_REASON_SUFFIX = "_missing_reason"

CORE = "core"
RECOMMENDED = "recommended"
OPTIONAL = "optional"
CONDITIONALLY_CORE = "conditionally_core"

READINESS_WEIGHTS = {CORE: 0.5, RECOMMENDED: 0.4, OPTIONAL: 0.1}


def _block(instance: dict, name: str) -> dict:
    value = instance.get(name)
    return value if isinstance(value, dict) else {}


def _contains(value: Any, needle: str) -> bool:
    return needle in str(value or "")


# Context predicates for conditionally-core slots: slot name -> predicate over
# the whole record instance. True means "this record is in the slot's stated
# context", making the slot Core for this record. These encode the prose
# contexts of SPEC.md §4 until they exist as LinkML rules (SPEC §7.7).
CONTEXT_PREDICATES: dict[str, Callable[[dict], bool]] = {
    # envar_layout — long format needs the discriminator column + key
    "variable_column": lambda r: _block(r, "data_layout").get("table_orientation") == "long",
    "variable_key": lambda r: _block(r, "data_layout").get("table_orientation") == "long",
    # envar_heat_metric — a derived heat metric must document its equation
    "equation_variant": lambda r: bool(_block(r, "derived_heat_metric")),
    "equation_inputs": lambda r: bool(_block(r, "derived_heat_metric")),
    "input_role": lambda r: bool(_block(r, "derived_heat_metric")),
    "input_provenance_id": lambda r: bool(_block(r, "derived_heat_metric")),
    "equation_validity_range": lambda r: bool(_block(r, "derived_heat_metric")),
    "indoor_outdoor": lambda r: bool(_block(r, "derived_heat_metric")),
    # heat-wave flavoured metrics only
    "heat_wave_threshold_definition": lambda r: _contains(_block(r, "derived_heat_metric"), "heat_wave"),
    "heat_wave_min_consecutive_days": lambda r: _contains(_block(r, "derived_heat_metric"), "heat_wave"),
    # percentile-based thresholds must state their reference period
    "percentile_reference_period_start": lambda r: _contains(
        _block(r, "derived_heat_metric").get("heat_wave_threshold_definition"), "percentile"
    ),
    "percentile_reference_period_end": lambda r: _contains(
        _block(r, "derived_heat_metric").get("heat_wave_threshold_definition"), "percentile"
    ),
    # envar_model — ensemble models must state their member count
    "exposure_model_ensemble_member_count": lambda r: _contains(
        _block(r, "exposure_model").get("exposure_model_type"), "ensemble"
    ),
    # envar_linkage — buffer/station strategies need their parameters.
    # clinical_date_assignment_convention has no predicate: its stated context
    # ("when linking to clinical events") is not decidable from the sidecar
    # alone, so it scores as Optional until SPEC §7.7 encodes the rule.
    "linkage_buffer_radius_m": lambda r: _contains(_block(r, "linkage_method").get("linkage_strategy"), "buffer"),
    "linkage_buffer_aggregation_method": lambda r: (
        _contains(_block(r, "linkage_method").get("linkage_strategy"), "buffer")
        or _contains(_block(r, "linkage_method").get("linkage_strategy"), "area")
    ),
    "linkage_max_distance_to_station_m": lambda r: _contains(
        _block(r, "linkage_method").get("linkage_strategy"), "station"
    ),
    # envar_spatial — buffer extraction / population weighting parameters
    "extraction_buffer_m": lambda r: _contains(_block(r, "spatial_reference").get("extraction_method"), "buffer"),
    "population_weighting_source": lambda r: (
        _contains(_block(r, "spatial_reference").get("extraction_method"), "population_weighted")
        or _contains(_block(r, "linkage_method").get("linkage_strategy"), "population_weighted")
    ),
    # envar_source — source_homogenisation_status (station-derived products
    # only) carries no predicate: "is this station-derived" is not reliably
    # decidable from instance text, so it scores as Optional out of context.
}

# Modules that SPEC.md §2 marks as omissible when not applicable. When the
# block is absent from an instance, the whole subtree (and the record slot
# binding it) leaves the slot universe instead of counting as missing.
CONDITIONAL_MODULES = {"derived_heat_metric"}


@dataclass
class SlotStatus:
    """Completeness status of one schema slot for one instance."""

    name: str
    tier: str  # tier as annotated in the schema
    effective_tier: str  # tier after resolving conditionally_core context
    module: str  # top-level record slot the slot sits under ("" = record root)
    owner_class: str
    present: bool
    explained: bool  # absent, but <name>_missing_reason is populated
    in_context: bool | None  # None unless tier == conditionally_core

    @property
    def counts_as_present(self) -> bool:
        return self.present or self.explained


@dataclass
class ModuleStatus:
    name: str
    state: str  # full | partial | absent
    present: int
    total: int
    missing: list[str] = field(default_factory=list)


@dataclass
class CompletenessReport:
    file: str | None
    target_class: str
    valid: bool | None  # None = validation unavailable/skipped
    validation_messages: list[str]
    scores: dict[str, list[int]]  # tier -> [got, of]
    readiness: float
    blocking: list[str]
    missing: dict[str, list[str]]  # tier -> missing slot names
    explained_null: list[str]
    modules: list[ModuleStatus]
    slots: list[SlotStatus]

    @property
    def blocked(self) -> bool:
        return bool(self.blocking)

    def as_dict(self) -> dict:
        data = asdict(self)
        data["blocked"] = self.blocked
        return data


class CompletenessChecker:
    """Scores instances of ``target_class`` against the schema's tier annotations."""

    def __init__(
        self,
        schema_path: str | Path = DEFAULT_SCHEMA,
        target_class: str = DEFAULT_TARGET_CLASS,
    ):
        self.schemaview = SchemaView(str(schema_path))
        self.target_class = target_class
        self._validator = None
        self._validation_available: bool | None = None

    # -- schema side ---------------------------------------------------------

    def tier_of(self, slot) -> str | None:
        annotation = None
        if slot.annotations and "tier" in slot.annotations:
            annotation = slot.annotations["tier"]
        else:
            top = self.schemaview.get_slot(slot.name)
            if top is not None and top.annotations and "tier" in top.annotations:
                annotation = top.annotations["tier"]
        return getattr(annotation, "value", None)

    def slot_universe(self) -> list[tuple[str, str, str, str]]:
        """All tier-annotated slots reachable from the target class.

        Returns (slot_name, tier, module, owner_class) tuples, one per unique
        slot name (first path wins). ``module`` is the top-level record slot
        the slot is nested under ("" for record-root slots).
        """
        sv = self.schemaview
        seen: dict[str, tuple[str, str, str, str]] = {}

        def walk(class_name: str, module: str, stack: tuple[str, ...]) -> None:
            if class_name in stack:  # cycle guard
                return
            for slot in sv.class_induced_slots(class_name):
                tier = self.tier_of(slot)
                if tier and slot.name not in seen:
                    seen[slot.name] = (slot.name, tier, module, class_name)
                slot_range = slot.range
                if slot_range in sv.all_classes():
                    next_module = module if module else slot.name
                    walk(slot_range, next_module, stack + (class_name,))

        walk(self.target_class, "", ())
        return list(seen.values())

    # -- instance side -------------------------------------------------------

    @staticmethod
    def _has_value(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, (str, list, dict)) and len(value) == 0:
            return False
        return True

    def _collect_present(self, node: Any, found: dict[str, Any]) -> None:
        """Flatten the instance tree into slot_name -> value (first hit wins;
        for multivalued nested blocks a slot is present if any element has it)."""
        if isinstance(node, dict):
            for key, value in node.items():
                if self._has_value(value) and key not in found:
                    found[key] = value
                self._collect_present(value, found)
        elif isinstance(node, list):
            for item in node:
                self._collect_present(item, found)

    # -- validation ----------------------------------------------------------

    def validate(self, instance: dict) -> tuple[bool | None, list[str]]:
        try:
            from linkml.validator import Validator
            from linkml.validator.plugins import JsonschemaValidationPlugin
        except ImportError:
            return None, ["validation skipped: the 'linkml' package is not installed"]
        if self._validator is None:
            self._validator = Validator(
                self.schemaview.schema,
                validation_plugins=[JsonschemaValidationPlugin(closed=True)],
            )
        report = self._validator.validate(instance, self.target_class)
        messages = [r.message for r in report.results]
        return not messages, messages

    # -- scoring -------------------------------------------------------------

    def check(self, instance: dict, file: str | None = None) -> CompletenessReport:
        valid, validation_messages = self.validate(instance)

        found: dict[str, Any] = {}
        self._collect_present(instance, found)

        absent_conditional_modules = {
            module for module in CONDITIONAL_MODULES if not self._has_value(instance.get(module))
        }

        statuses: list[SlotStatus] = []
        for name, tier, module, owner in self.slot_universe():
            if name.endswith(MISSING_REASON_SUFFIX):
                continue  # meta-slot: consumed via `explained` below
            if module in absent_conditional_modules or name in absent_conditional_modules:
                continue  # omissible module not present: subtree not applicable
            in_context: bool | None = None
            effective_tier = tier
            if tier == CONDITIONALLY_CORE:
                predicate = CONTEXT_PREDICATES.get(name)
                in_context = bool(predicate(instance)) if predicate else False
                effective_tier = CORE if in_context else OPTIONAL
            present = name in found
            # Null-with-reason is information for Recommended/Optional slots,
            # but it does not rescue Core: a missing Core slot blocks even
            # when its absence is explained (SPEC §3).
            explained = (
                not present
                and effective_tier != CORE
                and f"{name}{MISSING_REASON_SUFFIX}" in found
            )
            statuses.append(
                SlotStatus(
                    name=name,
                    tier=tier,
                    effective_tier=effective_tier,
                    module=module,
                    owner_class=owner,
                    present=present,
                    explained=explained,
                    in_context=in_context,
                )
            )

        scores: dict[str, list[int]] = {CORE: [0, 0], RECOMMENDED: [0, 0], OPTIONAL: [0, 0]}
        missing: dict[str, list[str]] = {CORE: [], RECOMMENDED: [], OPTIONAL: []}
        blocking: list[str] = []
        explained_null: list[str] = []
        for status in statuses:
            got_of = scores[status.effective_tier]
            got_of[1] += 1
            if status.counts_as_present:
                got_of[0] += 1
            else:
                missing[status.effective_tier].append(status.name)
                if status.effective_tier == CORE:
                    blocking.append(status.name)
            if status.explained:
                explained_null.append(status.name)

        readiness = 100.0 * sum(
            weight * (scores[tier][0] / scores[tier][1])
            for tier, weight in READINESS_WEIGHTS.items()
            if scores[tier][1]
        )

        modules: dict[str, ModuleStatus] = {}
        for status in statuses:
            module_name = status.module or "(record root)"
            entry = modules.setdefault(module_name, ModuleStatus(module_name, "absent", 0, 0))
            entry.total += 1
            if status.counts_as_present:
                entry.present += 1
            else:
                entry.missing.append(status.name)
        for entry in modules.values():
            entry.state = (
                "full" if entry.present == entry.total else "absent" if entry.present == 0 else "partial"
            )

        return CompletenessReport(
            file=file,
            target_class=self.target_class,
            valid=valid,
            validation_messages=validation_messages,
            scores=scores,
            readiness=round(readiness, 1),
            blocking=sorted(blocking),
            missing={tier: sorted(names) for tier, names in missing.items()},
            explained_null=sorted(explained_null),
            modules=sorted(modules.values(), key=lambda m: m.name),
            slots=statuses,
        )

    def check_file(self, path: str | Path) -> CompletenessReport:
        with open(path) as handle:
            instance = yaml.safe_load(handle)
        if not isinstance(instance, dict):
            raise ValueError(f"{path}: expected a mapping at the document root")
        return self.check(instance, file=str(path))


# -- reporting ----------------------------------------------------------------

TIER_LABELS = {CORE: "Core", RECOMMENDED: "Recommended", OPTIONAL: "Optional"}


def format_report(report: CompletenessReport) -> str:
    lines: list[str] = []
    if report.file:
        lines.append(f"# {report.file}")
    if report.valid is False:
        lines.append(f"INVALID against {report.target_class} ({len(report.validation_messages)} problem(s))")
    elif report.valid is None and report.validation_messages:
        lines.append(report.validation_messages[0])
    for tier in (CORE, RECOMMENDED, OPTIONAL):
        got, of = report.scores[tier]
        marker = "✓" if got == of else ("✗" if tier == CORE else "⚠")
        line = f"{TIER_LABELS[tier]:<12} {got}/{of}   {marker}"
        if report.missing[tier]:
            line += "   missing: " + ", ".join(report.missing[tier])
        lines.append(line)
    if report.explained_null:
        lines.append("Explained nulls (counted as documented): " + ", ".join(report.explained_null))
    lines.append(f"Reproducibility-readiness: {report.readiness:.0f}%")
    if report.blocking:
        lines.append("BLOCKING (Core missing): " + ", ".join(report.blocking))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="envar-check",
        description="Score a sidecar's metadata completeness against the EnVar tier annotations.",
    )
    parser.add_argument("sidecars", nargs="+", help="sidecar YAML file(s) to score")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="schema YAML (default: packaged umbrella)")
    parser.add_argument("--target-class", default=DEFAULT_TARGET_CLASS)
    parser.add_argument("--json", action="store_true", help="emit one JSON report per file instead of text")
    args = parser.parse_args(argv)

    checker = CompletenessChecker(schema_path=args.schema, target_class=args.target_class)
    any_blocked = False
    outputs = []
    for sidecar in args.sidecars:
        report = checker.check_file(sidecar)
        any_blocked = any_blocked or report.blocked
        outputs.append(report.as_dict() if args.json else format_report(report))
    if args.json:
        print(json.dumps(outputs if len(outputs) > 1 else outputs[0], indent=2))
    else:
        print("\n\n".join(outputs))
    return 1 if any_blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
