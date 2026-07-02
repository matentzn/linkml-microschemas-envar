#!/usr/bin/env python3
"""Generate ``docs/schema_overview.md`` — a human-first tour of the EnVar schema.

Unlike the generated element reference (``docs/elements/``), this page is written
for readers who do not care what a slot is called or how it is constrained, but
want to know *what kind of metadata is being captured*: human-readable names,
plain-language descriptions, and pointers to the standards each field leans on.

It renders one section per microschema module, driven entirely by the curated
``title`` / ``description`` / ``see_also`` metadata in the schema YAML files.

Run via ``just gen-schema-overview``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parents[1]
UMBRELLA = ROOT / "src" / "linkml_microschemas_envar" / "schema" / "linkml_microschemas_envar.yaml"
OUTPUT = ROOT / "docs" / "schema_overview.md"

# Page order, section emoji, and a one-line hook per module.
MODULES = [
    ("envar-record", "📦", "The composite record — one variable, one place, one time, one method, fully described."),
    ("envar-variable", "🏷️", "What was measured — the physical quantity, its units, and how it binds to community vocabularies."),
    ("envar-layout", "🗂️", "Where the values live — column bindings between the sidecar and the companion data file."),
    ("envar-spatial", "🗺️", "Where the value comes from — grid, projection, and how it was attached to a location."),
    ("envar-temporal", "🕒", "When the value applies — temporal grain, aggregation, day boundaries, and calendar."),
    ("envar-source", "🛰️", "Which upstream product the value came from — identity, version, DOI, and licence."),
    ("envar-model", "🧮", "How the value was produced — the model class, its inputs, and its known biases."),
    ("envar-uncertainty", "📊", "How much to trust the value — per-value and aggregate uncertainty and quality."),
    ("envar-linkage", "🔗", "How gridded values met patient locations — geocoding, lag alignment, and join rules."),
    ("envar-toolrun", "⚙️", "Exactly what ran — the tool invocation and the W3C-PROV provenance chain."),
    ("envar-heat-metric", "🌡️", "How derived heat metrics were computed — WBGT, Heat Index, UTCI, heat waves."),
    ("envar-health-layer", "🏥", "Where the values landed — the health-data-layer binding and the FAIR deposit."),
    ("envar-examples", "🧾", "Ready-made record types for common heat variables."),
    ("envar-common", "🧰", "Shared building blocks — record identity, PHI safety, and missing-value reasons."),
]

TIER_BADGES = {
    "core": "🟥 Core",
    "conditionally_core": "🟧 Core (conditional)",
    "recommended": "🟨 Recommended",
    "optional": "⬜ Optional",
}

TYPE_PHRASES = {
    "string": "text",
    "integer": "whole number",
    "float": "number",
    "double": "number",
    "decimal": "number",
    "boolean": "yes / no",
    "date": "date",
    "datetime": "date & time",
    "time": "time of day",
    "uriorcurie": "identifier (CURIE / URI)",
    "curie": "identifier (CURIE)",
    "uri": "URL",
}

# Human labels for see_also links, matched by substring (first hit wins).
LINK_LABELS = [
    ("cfconventions.org/standard-names", "CF Standard Names"),
    ("cfconventions.org/cf-conventions/cf-conventions.html#cell-methods", "CF cell_methods"),
    ("cfconventions.org/cf-conventions/cf-conventions.html#calendar", "CF calendar"),
    ("cfconventions.org", "CF Conventions"),
    ("ucum.org", "UCUM"),
    ("epsg.io", "EPSG Registry"),
    ("epsg.org", "EPSG Registry"),
    ("proj.org", "PROJ"),
    ("w3.org/TR/prov-primer", "W3C PROV Primer"),
    ("w3.org/TR/prov-o", "W3C PROV-O"),
    ("ohdsi.github.io/CommonDataModel", "OMOP CDM"),
    ("athena.ohdsi.org", "OHDSI Athena"),
    ("biodatacatalyst", "BioData Catalyst"),
    ("daymet", "Daymet"),
    ("climatologylab.org", "gridMET"),
    ("data.narr", "NARR"),
    ("psl.noaa.gov", "NARR"),
    ("ecmwf", "ERA5"),
    ("prism.oregonstate", "PRISM"),
    ("degauss", "DeGAUSS"),
    ("obofoundry.org/ontology/ecto", "ECTO"),
    ("obofoundry.org/ontology/envo", "ENVO"),
    ("loinc.org", "LOINC"),
    ("snomed", "SNOMED CT"),
    ("spdx.org", "SPDX Licence List"),
    ("doi.org/10.1038/s41597-022-01405-3", "Spangler et al. 2022"),
    ("doi.org", "DOI Foundation"),
    ("datacite.org", "DataCite"),
    ("esipfed.org", "ACDD"),
    ("h3geo.org", "H3"),
    ("github.com/ulid", "ULID"),
    ("go-fair.org", "FAIR Principles"),
    ("zenodo.org", "Zenodo"),
    ("census.gov", "US Census Geographies"),
    ("weather.gov/safety/heat-index", "NWS Heat Index"),
    ("utci.org", "UTCI"),
    ("linkml/linkml-microschema-profile", "LinkML Microschema Profile"),
    ("wikipedia.org/wiki/", None),  # label from the article name
]

warnings: list[str] = []


def warn(msg: str) -> None:
    warnings.append(msg)


def clean(text: str | None) -> str:
    """Collapse whitespace and escape table-breaking pipes."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip().replace("|", "\\|")


def slug(text: str) -> str:
    """Mirror python-markdown's toc slugify so intra-page anchors resolve."""
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s+", "-", text.strip())


def humanize(name: str) -> str:
    words = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name.replace("_", " "))
    return words.title()


def el_title(element) -> str:
    return element.title or humanize(element.name)


def link_label(url: str) -> str:
    for needle, label in LINK_LABELS:
        if needle in url:
            if label:
                return label
            return url.rstrip("/").rsplit("/", 1)[-1].replace("_", " ")
    host = urlparse(url).netloc or url
    return host.removeprefix("www.")


def see_also_links(element) -> str:
    urls = [str(u) for u in (element.see_also or []) if str(u).startswith("http")]
    return " · ".join(f"[{link_label(u)}]({u})" for u in urls)


def get_annotation(element, key: str) -> str | None:
    try:
        ann = element.annotations
        if ann and key in ann:
            return str(ann[key].value)
    except Exception:
        pass
    return None


def get_tier(element) -> str | None:
    return get_annotation(element, "tier")


class Overview:
    def __init__(self) -> None:
        self.sv = SchemaView(str(UMBRELLA))
        self.sv.all_classes()  # force the import closure so schema_map is complete
        by_name = {sd.name: sd for sd in self.sv.schema_map.values()}
        self.modules = []
        for name, emoji, hook in MODULES:
            sd = by_name.get(name)
            if sd is None:
                warn(f"module {name} not found in import closure — skipped")
                continue
            display = (sd.title or sd.name).split("—")[-1].strip()
            self.modules.append((sd, emoji, display, hook))

        # Anchors for everything that gets its own heading.
        self.module_anchor = {sd.name: "#" + slug(d) for sd, _, d, _ in self.modules}
        self.class_anchor: dict[str, str] = {}
        self.enum_anchor: dict[str, str] = {}
        for sd, _, display, _ in self.modules:
            rendered = self.rendered_classes(sd)
            for cname in rendered:
                cls = self.sv.get_class(cname)
                if len(rendered) == 1 or el_title(cls) == display:
                    # A lone class, or one that shares the module's name,
                    # renders inline under the module heading.
                    self.class_anchor[cname] = self.module_anchor[sd.name]
                else:
                    self.class_anchor[cname] = "#" + slug(el_title(cls))
            for ename in sd.enums:
                self.enum_anchor[ename] = "#" + slug(el_title(self.sv.get_enum(ename)))

    def rendered_classes(self, sd) -> list[str]:
        """Classes of a module worth showing (skip Any-typed passthroughs)."""
        out = []
        for cname, cls in sd.classes.items():
            if cls.class_uri and str(cls.class_uri) == "linkml:Any":
                continue
            out.append(cname)
        return out

    # ── range / row rendering ────────────────────────────────────────────

    def range_phrase(self, slot) -> str:
        rng = slot.range or "string"
        if rng in self.sv.all_enums():
            title = el_title(self.sv.get_enum(rng))
            anchor = self.enum_anchor.get(rng)
            phrase = f"[{title}]({anchor}) value" if anchor else f"{title} value"
        elif rng in self.sv.all_classes():
            title = el_title(self.sv.get_class(rng))
            anchor = self.class_anchor.get(rng)
            phrase = f"[{title}]({anchor}) block" if anchor else f"{title} block"
        else:
            phrase = TYPE_PHRASES.get(rng, rng)
        if slot.multivalued:
            phrase = f"list of {phrase}"
        return phrase

    def example_phrases(self, slot) -> str:
        """Render a slot's ``examples`` as `value` — description lines."""
        out = []
        for ex in slot.examples or []:
            val = clean(str(ex.value)) if ex.value is not None else ""
            phrase = f"`{val}`" if val else ""
            if ex.description:
                phrase = f"{phrase} — {clean(ex.description)}" if phrase else clean(ex.description)
            if phrase:
                out.append(phrase)
        return "<br>".join(out)

    def slot_row(self, slot) -> str:
        title = el_title(slot)
        if not slot.title:
            warn(f"slot {slot.name}: no title (using '{title}')")
        desc = clean(slot.description)
        if not desc:
            warn(f"slot {slot.name}: no description")
        explanation = clean(get_annotation(slot, "explanation"))
        if explanation:
            desc = f"{desc}<br>💡 *{explanation}*" if desc else f"💡 *{explanation}*"
        else:
            warn(f"slot {slot.name}: no explanation annotation")
        links = see_also_links(slot)
        if links:
            desc = f"{desc}<br>↗ {links}" if desc else f"↗ {links}"
        question = clean(get_annotation(slot, "open_question"))
        if question:
            callout = f"<br><br>❓ **Open question (draft — feedback welcome):** {question}"
            desc = f"{desc}{callout}" if desc else callout.lstrip("<br>")
        justification = clean(get_annotation(slot, "justification"))
        if not justification:
            warn(f"slot {slot.name}: no justification annotation")
            justification = "—"
        examples = self.example_phrases(slot) or "—"
        tier = get_tier(slot)
        badge = TIER_BADGES.get(tier, "") if tier else ""
        if slot.required:
            badge = f"{badge}<br>*(required)*" if badge else "*(required)*"
        if not badge:
            badge = "—"
        field = f"**{clean(title)}**<br><small>`{slot.name}` · {self.range_phrase(slot)}</small>"
        return f"| {field} | {desc} | {justification} | {examples} | {badge} |"

    def slot_table(self, slots) -> list[str]:
        lines = [
            "| Field | What it captures | Why it matters | Examples | Priority |",
            "|---|---|---|---|---|",
        ]
        lines += [self.slot_row(s) for s in slots]
        return lines

    def slot_groups(self, slots) -> list[tuple[str | None, list]]:
        """Partition slots by their ``slot_group``, preserving first-seen order.

        Returns ``[(group_slot_name_or_None, [slots...]), ...]``. Grouping
        slots are the schema-level mechanism for keeping big composite
        classes tidy: display-only ``is_grouping_slot`` slots referenced via
        ``slot_group`` (see envar_record.yaml).
        """
        order: list[str | None] = []
        buckets: dict[str | None, list] = {}
        for s in slots:
            g = s.slot_group or None
            if g not in buckets:
                order.append(g)
                buckets[g] = []
            buckets[g].append(s)
        return [(g, buckets[g]) for g in order]

    def grouped_slot_tables(self, cname: str, slots, level: int) -> list[str]:
        """One subtable per slot_group; falls back to a single table."""
        groups = self.slot_groups(slots)
        if all(g is None for g, _ in groups):
            return self.slot_table(slots) + [""]
        lines: list[str] = []
        hashes = "#" * level
        for gname, gslots in groups:
            if gname is None:
                warn(f"class {cname}: slots {[s.name for s in gslots]} have no slot_group")
                lines += [f"{hashes} Other fields", ""]
            else:
                gslot = self.sv.get_slot(gname)
                lines += [f"{hashes} {el_title(gslot)}", ""]
                if gslot.description:
                    lines += [f"*{clean_block(gslot.description)}*", ""]
            lines += self.slot_table(gslots)
            lines += [""]
        return lines

    # ── section rendering ────────────────────────────────────────────────

    def render_class(self, cname: str, heading: bool) -> list[str]:
        cls = self.sv.get_class(cname)
        lines: list[str] = []
        if heading:
            lines += [f"### {el_title(cls)}", ""]
        if cls.description:
            lines += [clean_block(cls.description), ""]
        else:
            warn(f"class {cname}: no description")
        links = see_also_links(cls)
        if links:
            lines += [f"**Standards & references:** {links}", ""]

        parent = cls.is_a
        if parent and parent in self.class_anchor:
            # Preset subclass (e.g. the worked record types): show what it pins
            # down rather than repeating the parent's full field table.
            ptitle = el_title(self.sv.get_class(parent))
            lines += [f"*A specialisation of [{ptitle}]({self.class_anchor[parent]}).*", ""]
            rows, extra_required = [], []
            for sname, usage in (cls.slot_usage or {}).items():
                pins = []
                if usage.equals_string:
                    pins.append(f"`{usage.equals_string}`")
                if usage.equals_number is not None:
                    pins.append(f"`{usage.equals_number}`")
                if usage.pattern:
                    pins.append(f"matches `{usage.pattern}`")
                stitle = el_title(self.sv.induced_slot(sname, cname))
                if pins:
                    rows.append(f"| **{clean(stitle)}** <small>`{sname}`</small> | {' · '.join(pins)} |")
                elif usage.required:
                    extra_required.append(f"**{clean(stitle)}**")
            if rows:
                lines += ["| Field | Fixed to |", "|---|---|", *rows, ""]
            if extra_required:
                lines += [f"*Additionally requires {', '.join(extra_required)} to be present.*", ""]
            return lines

        slots = self.sv.class_induced_slots(cname)
        if slots:
            lines += self.grouped_slot_tables(cname, slots, level=4 if heading else 3)
        return lines

    def render_enum(self, ename: str) -> list[str]:
        enum = self.sv.get_enum(ename)
        lines = [f"### {el_title(enum)}", ""]
        if enum.description:
            lines += [clean_block(enum.description), ""]
        links = see_also_links(enum)
        if links:
            lines += [f"**Standards & references:** {links}", ""]
        lines += ["| Value | Meaning |", "|---|---|"]
        for vname, pv in enum.permissible_values.items():
            vtitle = pv.title or vname.replace("_", " ")
            lines.append(f"| **{clean(vtitle)}** | {clean(pv.description)} |")
        lines.append("")
        return lines

    def render_module(self, sd, emoji: str, display: str, hook: str) -> list[str]:
        lines = [f"## {emoji} {display}", "", f"**{hook}**", ""]
        if sd.description:
            lines += [clean_block(sd.description), ""]
        links = see_also_links(sd)
        if links:
            lines += [f"**Standards & references:** {links}", ""]

        rendered = self.rendered_classes(sd)
        multi = len(rendered) > 1
        for cname in rendered:
            # No sub-heading for a class that shares the module's name — its
            # content flows directly under the module heading.
            same_name = el_title(self.sv.get_class(cname)) == display
            lines += self.render_class(cname, heading=multi and not same_name)
            if cname == "EnvironmentalExposureRecord":
                lines += self.record_diagram(cname)

        # Slots defined here but not attached to any rendered class
        # (the shared fields in envar_common, for instance). Grouping slots
        # are display-only scaffolding rendered as subtable headings above.
        in_classes = {s.name for c in rendered for s in self.sv.class_induced_slots(c)}
        orphans = [
            self.sv.get_slot(s)
            for s in sd.slots
            if s not in in_classes and not self.sv.get_slot(s).is_grouping_slot
        ]
        if orphans:
            if rendered:
                lines += ["### Shared fields", ""]
            lines += self.slot_table(orphans)
            lines += [""]

        for ename in sd.enums:
            lines += self.render_enum(ename)
        return lines

    def record_diagram(self, cname: str) -> list[str]:
        """A mermaid map of the record and its component blocks, one
        subgraph per slot_group (ungrouped blocks hang off the record)."""

        def block_label(rng: str) -> str:
            emoji = next((e for sd, e, _, _ in self.modules if rng in sd.classes), "")
            return f"{emoji} {el_title(self.sv.get_class(rng))}".strip()

        lines = ["```mermaid", "flowchart LR", '  R(["📦 Environmental Exposure Record"])']
        n_nodes = n_groups = 0
        for gname, gslots in self.slot_groups(self.sv.class_induced_slots(cname)):
            blocks = [
                s.range
                for s in gslots
                if s.range in self.sv.all_classes() and s.range in self.class_anchor
            ]
            if not blocks:
                continue
            if gname is None:
                for rng in blocks:
                    lines.append(f'  R --> C{n_nodes}["{block_label(rng)}"]')
                    n_nodes += 1
                continue
            lines.append(f'  subgraph G{n_groups}["{el_title(self.sv.get_slot(gname))}"]')
            for rng in blocks:
                lines.append(f'    C{n_nodes}["{block_label(rng)}"]')
                n_nodes += 1
            lines.append("  end")
            lines.append(f"  R --> G{n_groups}")
            n_groups += 1
        if not n_nodes:
            return []
        lines += ["```", ""]
        return lines

    # ── page assembly ────────────────────────────────────────────────────

    def render(self) -> str:
        lines = [
            "<!-- Auto-generated by scripts/gen_schema_overview.py — do not edit.",
            "     Regenerate with `just gen-schema-overview`. -->",
            "",
            "# What the EnVar schema captures",
            "",
            "Every environmental exposure value that reaches a health-data system has a",
            "story: *which* physical quantity it is, *where* and *when* it applies, which",
            "upstream product it came from, how it was modelled, linked to patients, and",
            "validated. The **EnVar microschemas** capture that story as a small, PHI-free",
            "metadata *sidecar* that travels with the data.",
            "",
            "This page is a plain-language tour of everything the schema records — one",
            "section per microschema, focused on *what is captured* rather than how the",
            "fields are named or constrained. For the technical element-by-element",
            "reference, see the [generated schema docs](elements/index.md).",
            "",
            '!!! info "How to read this page"',
            "    Each field row shows its human-readable name (with the technical field",
            "    name and value type in small print), then four columns:",
            "",
            "    - **What it captures** — the field's definition, a 💡 plain-terms",
            "      explainer where the definition assumes background knowledge, and",
            "      ↗ links to the standards it leans on",
            "    - **Why it matters** — the justification: what breaks or becomes",
            "      unverifiable when the field is omitted",
            "    - **Examples** — concrete values as they would appear in a sidecar",
            "    - **Priority** — the field's tier:",
            "",
            "    - 🟥 **Core** — must be present for the record to be minimally interpretable",
            "    - 🟧 **Core (conditional)** — required whenever the situation applies (e.g. a buffer was used)",
            "    - 🟨 **Recommended** — fill in when available",
            "    - ⬜ **Optional** — nice to have",
            "",
            "## At a glance",
            "",
            "| Section | What it tells you |",
            "|---|---|",
        ]
        for sd, emoji, display, hook in self.modules:
            anchor = self.module_anchor[sd.name]
            lines.append(f"| {emoji} [{display}]({anchor}) | {clean(hook)} |")
        lines.append("")

        for sd, emoji, display, hook in self.modules:
            lines += self.render_module(sd, emoji, display, hook)

        lines += [
            "---",
            "",
            "*Generated from the LinkML sources under*",
            "*`src/linkml_microschemas_envar/schema/` — regenerate with",
            "`just gen-schema-overview`.*",
            "",
        ]
        return "\n".join(lines)


def clean_block(text: str) -> str:
    """Whitespace-normalise a prose block (module/class description)."""
    return re.sub(r"[ \t]*\n[ \t]*", " ", str(text)).strip()


def main() -> int:
    overview = Overview()
    OUTPUT.write_text(overview.render(), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    if warnings:
        print(f"\n{len(warnings)} curation gap(s):", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
