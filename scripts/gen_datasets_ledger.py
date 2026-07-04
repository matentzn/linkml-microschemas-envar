"""Generate docs/datasets/index.html — the computed example-dataset ledger.

Runs the completeness checker (linkml_microschemas_envar.checker) over every
example sidecar in the repository and renders a single self-contained HTML
page: one row per dataset with its tier meters, reproducibility-readiness and
BLOCKED stamp, and an expandable drawer holding (a) the per-module
present/missing analysis and (b) the sidecar YAML itself.

Unlike docs/dashboard/index.html (hand-embedded, illustrative scenarios),
every number on this page is computed from the schema's tier annotations at
generation time. Regenerate with `just gen-datasets-ledger`.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from linkml_microschemas_envar.checker import CompletenessChecker  # noqa: E402

OUT = REPO / "docs" / "datasets" / "index.html"

# (group label, glob or explicit paths, note shown under the group)
DATASET_GROUPS = [
    (
        "Worked example",
        ["examples/daymet_tmax_phoenix_2022_07_19.yaml"],
        "The canonical worked sidecar: Daymet TMAX over Phoenix, 2022-07-19.",
    ),
    (
        "TMAX completeness gradient",
        [
            "tests/data/valid/EnvironmentalExposureRecord-tmax_core.yaml",
            "tests/data/valid/EnvironmentalExposureRecord-tmax_recommended.yaml",
            "tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml",
        ],
        "The same record at three curation levels — watch the readiness climb.",
    ),
    (
        "PM2.5 completeness gradient",
        [
            "tests/data/valid/EnvironmentalExposureRecord-pm25_core.yaml",
            "tests/data/valid/EnvironmentalExposureRecord-pm25_recommended.yaml",
            "tests/data/valid/EnvironmentalExposureRecord-pm25_ideal.yaml",
        ],
        "The generalisation check: a different variable, the same gradient.",
    ),
    (
        "Heat Index scenario (derived metric with two upstream inputs)",
        [
            "examples/scenarios/heat_index/heat_index_input_a_tmax_daymet.yaml",
            "examples/scenarios/heat_index/heat_index_input_b_rh_era5.yaml",
            "examples/scenarios/heat_index/heat_index_derived.yaml",
        ],
        "A derived heat metric: the conditionally-core equation slots switch on.",
    ),
    (
        "Standard coverage — real pipeline runs, translated (TMAX)",
        [
            "examples/scenarios/standards/amadeus_gridmet_tmmx.yaml",
            "examples/scenarios/standards/degauss_daymet_tmax.yaml",
            "examples/scenarios/standards/omop_gaia_daymet_tmax.yaml",
        ],
        "Strict EnVar translations of real Amadeus, DeGAUSS and GAIA-OMOP runs "
        "(sidecars emitted 2026-06-25 by the three-way pipeline in the EnVar "
        "sibling repo): only what each pipeline actually emitted is mapped, so "
        "the meters show each standard's true coverage of the variables of "
        "interest — and where none of them reaches the Core floor alone.",
    ),
    (
        "Counter-examples (must fail)",
        [
            "tests/data/invalid/EnvironmentalExposureRecord-tmax_core_missing.yaml",
            "tests/data/invalid/EnvironmentalExposureRecord-pm25_core_missing.yaml",
        ],
        "Core fields deliberately dropped: the checker stamps them BLOCKED.",
    ),
]

TIER_ORDER = ["core", "recommended", "optional"]
TIER_LABEL = {"core": "Core", "recommended": "Recommended", "optional": "Optional"}


def meter(tier: str, got: int, of: int) -> str:
    pct = 0 if of == 0 else round(100 * got / of)
    return (
        f'<div class="meter" title="{TIER_LABEL[tier]}: {got}/{of}">'
        f'<span class="meter-label">{TIER_LABEL[tier]}</span>'
        f'<span class="meter-track"><span class="meter-fill {tier}" style="width:{pct}%"></span></span>'
        f'<span class="meter-count">{got}/{of}</span></div>'
    )


def dataset_row(index: int, path: Path, report) -> str:
    rel = path.relative_to(REPO)
    name = path.stem
    d = report.as_dict()
    scores = d["scores"]
    blocked = d["blocked"]
    valid = d["valid"]
    variable = ""
    try:
        import yaml

        instance = yaml.safe_load(path.read_text())
        variable = instance.get("variable_identity", {}).get("variable_name", "")
    except Exception:
        instance = {}

    badges = []
    if blocked:
        badges.append('<span class="badge blocked">BLOCKED</span>')
    if valid is False:
        badges.append('<span class="badge invalid">fails validation</span>')
    elif valid:
        badges.append('<span class="badge valid">validates</span>')

    meters = "".join(meter(t, *scores[t]) for t in TIER_ORDER)

    modules_rows = "".join(
        f"<tr><td><code>{html.escape(m['name'])}</code></td>"
        f'<td class="state-{m["state"]}">{m["state"]}</td>'
        f"<td>{m['present']}/{m['total']}</td>"
        f"<td class='missing-list'>{html.escape(', '.join(m['missing'])) or '—'}</td></tr>"
        for m in d["modules"]
    )

    missing_lists = "".join(
        f"<p><strong>{TIER_LABEL[t]} missing ({len(d['missing'][t])}):</strong> "
        f"{html.escape(', '.join(d['missing'][t])) or '<em>none</em>'}</p>"
        for t in TIER_ORDER
        if d["missing"][t]
    ) or "<p><em>Nothing missing in any tier.</em></p>"

    explained = ""
    if d["explained_null"]:
        explained = (
            "<p><strong>Explained nulls</strong> (absent, but documented with a "
            f"<code>*_missing_reason</code> — counted as present): "
            f"{html.escape(', '.join(d['explained_null']))}</p>"
        )

    blocking = ""
    if d["blocking"]:
        blocking = (
            '<p class="blocking-line"><strong>BLOCKING (Core missing):</strong> '
            f"{html.escape(', '.join(d['blocking']))}</p>"
        )

    validation = ""
    if valid is False:
        items = "".join(f"<li>{html.escape(m)}</li>" for m in d["validation_messages"])
        validation = f"<details class='validation'><summary>{len(d['validation_messages'])} validation problem(s)</summary><ul>{items}</ul></details>"

    yaml_text = html.escape(path.read_text())

    return f"""
<article class="dataset" id="ds-{index}">
  <header class="dataset-head" onclick="toggle({index})">
    <div class="head-main">
      <span class="disclosure" id="disc-{index}">▸</span>
      <span class="ds-name">{html.escape(name)}</span>
      {f'<span class="ds-var">{html.escape(str(variable))}</span>' if variable else ''}
      {''.join(badges)}
    </div>
    <div class="head-meters">{meters}</div>
    <div class="readiness{' readiness-blocked' if blocked else ''}">
      <span class="readiness-num">{d['readiness']:.0f}%</span>
      <span class="readiness-label">readiness</span>
    </div>
  </header>
  <div class="drawer" id="drawer-{index}" hidden>
    <div class="tabs">
      <button class="tab active" onclick="showtab({index},'analysis',this)">Analysis</button>
      <button class="tab" onclick="showtab({index},'source',this)">Sidecar YAML</button>
    </div>
    <div class="tabpane" id="pane-{index}-analysis">
      {blocking}
      {validation}
      <table class="modules">
        <thead><tr><th>Module</th><th>State</th><th>Present</th><th>Missing slots</th></tr></thead>
        <tbody>{modules_rows}</tbody>
      </table>
      {missing_lists}
      {explained}
      <p class="src-path">Source: <code>{rel}</code></p>
    </div>
    <div class="tabpane" id="pane-{index}-source" hidden>
      <pre class="yaml">{yaml_text}</pre>
    </div>
  </div>
</article>"""


CSS = """
:root {
  --paper:#faf6ee; --panel:#fffdf8; --ink:#26221a; --muted:#7a715f;
  --rule:#d9d0bd; --core:#c2452d; --recommended:#d98324; --optional:#3d7a68;
  --blocked:#a31f1f; --valid:#3d7a68;
}
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink);
  font:15px/1.55 Georgia,'Times New Roman',serif; }
.wrap { max-width:1080px; margin:0 auto; padding:2.2rem 1.2rem 4rem; }
h1 { font-size:1.9rem; margin:0 0 .3rem; letter-spacing:.01em; }
nav.crumbs { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.74rem;
  margin:0 0 1rem; }
nav.crumbs a { color:var(--core); text-decoration:none; font-weight:600; }
nav.crumbs a:hover { color:var(--recommended); }
nav.crumbs span { color:var(--rule); margin:0 .45rem; }
.subtitle { color:var(--muted); margin:0 0 1.6rem; max-width:64ch; }
.subtitle code { font-size:.85em; }
h2.group { font-size:1.12rem; border-bottom:2px solid var(--ink);
  padding-bottom:.25rem; margin:2.2rem 0 .2rem; }
p.group-note { color:var(--muted); margin:.2rem 0 .8rem; font-style:italic; }
.dataset { background:var(--panel); border:1px solid var(--rule);
  border-radius:6px; margin:.55rem 0; overflow:hidden; }
.dataset-head { display:flex; align-items:center; gap:1rem; padding:.6rem .9rem;
  cursor:pointer; flex-wrap:wrap; }
.dataset-head:hover { background:#f5efe2; }
.head-main { display:flex; align-items:center; gap:.55rem; flex:1 1 22rem; min-width:0; }
.disclosure { color:var(--muted); width:1em; flex:none; }
.ds-name { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.86rem;
  overflow-wrap:anywhere; }
.ds-var { background:#efe7d4; border-radius:3px; padding:0 .45em;
  font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.78rem; }
.badge { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.7rem;
  border-radius:3px; padding:.1em .5em; letter-spacing:.05em; flex:none; }
.badge.blocked { background:var(--blocked); color:#fff; }
.badge.invalid { background:#f3d9d9; color:var(--blocked); }
.badge.valid { background:#e2ede8; color:var(--valid); }
.head-meters { display:flex; flex-direction:column; gap:2px; flex:0 0 17rem; }
.meter { display:flex; align-items:center; gap:.45rem;
  font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.68rem; }
.meter-label { width:6.4em; color:var(--muted); text-align:right; }
.meter-track { flex:1; height:7px; background:#eee5d2; border-radius:4px; overflow:hidden; }
.meter-fill { display:block; height:100%; border-radius:4px; }
.meter-fill.core { background:var(--core); }
.meter-fill.recommended { background:var(--recommended); }
.meter-fill.optional { background:var(--optional); }
.meter-count { width:3.4em; color:var(--muted); }
.readiness { text-align:right; flex:0 0 5.6rem; }
.readiness-num { font-size:1.45rem; font-weight:700; display:block; line-height:1.1; }
.readiness-label { color:var(--muted); font-size:.7rem; letter-spacing:.08em;
  text-transform:uppercase; }
.readiness-blocked .readiness-num { color:var(--blocked); text-decoration:line-through; }
.drawer { border-top:1px solid var(--rule); padding: .8rem .9rem 1rem; }
.tabs { display:flex; gap:.4rem; margin-bottom:.7rem; }
.tab { font:inherit; font-size:.8rem; border:1px solid var(--rule);
  background:transparent; border-radius:4px; padding:.2em .8em; cursor:pointer; }
.tab.active { background:var(--ink); color:var(--paper); border-color:var(--ink); }
table.modules { border-collapse:collapse; width:100%; font-size:.82rem; margin:.4rem 0 .9rem; }
table.modules th, table.modules td { border:1px solid var(--rule);
  padding:.28em .55em; text-align:left; vertical-align:top; }
table.modules th { background:#f1ead9; font-size:.72rem; letter-spacing:.05em;
  text-transform:uppercase; }
td.state-full { color:var(--valid); font-weight:700; }
td.state-partial { color:var(--recommended); font-weight:700; }
td.state-absent { color:var(--blocked); font-weight:700; }
td.missing-list { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.72rem;
  color:var(--muted); }
.blocking-line { color:var(--blocked); }
details.validation { margin:.4rem 0; font-size:.85rem; }
pre.yaml { background:#292520; color:#efe8d8; padding:1rem; border-radius:6px;
  font-size:.74rem; line-height:1.45; overflow:auto; max-height:34rem; }
.src-path { color:var(--muted); font-size:.8rem; }
footer { margin-top:2.5rem; color:var(--muted); font-size:.8rem;
  border-top:1px solid var(--rule); padding-top:.8rem; }
"""

JS = """
function toggle(i) {
  const d = document.getElementById('drawer-' + i);
  const disc = document.getElementById('disc-' + i);
  d.hidden = !d.hidden;
  disc.textContent = d.hidden ? '\\u25b8' : '\\u25be';
}
function showtab(i, which, btn) {
  document.getElementById('pane-' + i + '-analysis').hidden = which !== 'analysis';
  document.getElementById('pane-' + i + '-source').hidden = which !== 'source';
  btn.parentElement.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
}
"""


def main() -> int:
    checker = CompletenessChecker()
    sections = []
    index = 0
    summary = {"datasets": 0, "blocked": 0}
    for group, paths, note in DATASET_GROUPS:
        rows = []
        for rel in paths:
            path = REPO / rel
            if not path.exists():
                print(f"WARNING: skipping missing dataset {rel}", file=sys.stderr)
                continue
            report = checker.check_file(path)
            summary["datasets"] += 1
            summary["blocked"] += int(report.blocked)
            rows.append(dataset_row(index, path, report))
            index += 1
        sections.append(
            f'<h2 class="group">{html.escape(group)}</h2>'
            f'<p class="group-note">{html.escape(note)}</p>' + "".join(rows)
        )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EnVar example datasets — computed completeness</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Example datasets</h1>
<nav class="crumbs" aria-label="Site">
<a href="../">&larr; Docs home</a><span>&middot;</span><a href="../overview/">Schema overview</a><span>&middot;</span><a href="../elements/">Element reference</a><span>&middot;</span><a href="../dashboard/">Completeness ledger</a>
</nav>
<p class="subtitle">Every sidecar shipped with this repository, scored live by the
metadata-completeness checker against the schema's <code>tier</code> annotations
(<code>core</code> / <code>recommended</code> / <code>optional</code> /
<code>conditionally_core</code>). Click a row to see what is present, what is
missing, and the sidecar itself. Readiness =
100&nbsp;·&nbsp;(0.5·core + 0.4·recommended + 0.1·optional). A missing Core slot
stamps the record <strong>BLOCKED</strong>. Regenerated by
<code>just gen-datasets-ledger</code>; {summary['datasets']} datasets,
{summary['blocked']} blocked.</p>
{''.join(sections)}
<footer>Generated from the schema tier annotations by
<code>scripts/gen_datasets_ledger.py</code> — numbers are computed, not curated.
The <a href="../dashboard/index.html">completeness ledger</a> shows the
hand-authored illustrative scenarios this page replaces with live data.</footer>
</div>
<script>{JS}</script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    print(f"wrote {OUT.relative_to(REPO)} ({summary['datasets']} datasets, {summary['blocked']} blocked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
