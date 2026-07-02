#!/usr/bin/env python3
"""Render ``docs/schema_overview.md`` as a standalone HTML page.

Writes ``docs/overview/index.html``, which mkdocs deploys verbatim (like
``docs/dashboard/index.html``) and the site nav links as "Schema overview".
The page keeps its own full-width layout because the overview's five-column
field tables do not fit mkdocs-material's content column. Typeset as a
scientific field monograph — warm paper ground, ink-dark serif prose, a
heat-vermilion accent, dense sans tables, and a sticky chapter rail.
Mermaid diagrams render client-side (CDN); fonts come from Google Fonts,
so the page wants a network connection on first open.

Run via ``just render-schema-overview`` (also wired into ``just site`` /
``just testdoc``).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "schema_overview.md"
OUTPUT = ROOT / "docs" / "overview" / "index.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — EnVar Microschemas</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,600;9..144,700&family=Source+Serif+4:opsz,ital,wght@8..60,0,400;8..60,0,600;8..60,1,400&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{
  --paper: #f7f1e6;
  --paper-deep: #efe6d4;
  --card: #fbf7ee;
  --ink: #241c12;
  --ink-soft: #5c5243;
  --hairline: #d8cbb2;
  --rule: #a08e6f;
  --vermilion: #b23a12;
  --vermilion-deep: #8c2c0c;
  --teal: #1f6a5c;
  --serif: "Source Serif 4", Georgia, serif;
  --sans: "Source Sans 3", "Helvetica Neue", sans-serif;
  --display: "Fraunces", Georgia, serif;
  --mono: "JetBrains Mono", ui-monospace, monospace;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; scroll-padding-top: 2rem; }}
body {{
  margin: 0;
  background:
    radial-gradient(1200px 500px at 85% -100px, rgba(178, 58, 18, 0.06), transparent 60%),
    linear-gradient(var(--paper), var(--paper));
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.0rem;
  line-height: 1.62;
  -webkit-font-smoothing: antialiased;
}}
/* faint laid-paper grain */
body::before {{
  content: "";
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: repeating-linear-gradient(0deg, rgba(36,28,18,0.022) 0 1px, transparent 1px 3px);
}}

.frame {{
  position: relative; z-index: 1;
  /* Internal-review page: use the whole screen, however wide. */
  max-width: 2160px; margin: 0 auto;
  display: grid; grid-template-columns: 250px minmax(0, 1fr);
  gap: 3.2rem; padding: 0 2.2rem 6rem;
}}

/* ── masthead ─────────────────────────────────────────────── */
header.masthead {{
  grid-column: 1 / -1;
  padding: 3.4rem 0 2rem;
  border-bottom: 3px double var(--rule);
  animation: rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) both;
}}
.kicker {{
  font-family: var(--sans); font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.22em; text-transform: uppercase; color: var(--vermilion);
}}
nav.crumbs {{
  font-family: var(--sans); font-size: 0.78rem; margin-top: 0.8rem;
}}
nav.crumbs a {{
  color: var(--teal); text-decoration: none; font-weight: 600;
}}
nav.crumbs a:hover {{ color: var(--vermilion-deep); }}
nav.crumbs span {{ color: var(--hairline); margin: 0 0.5rem; }}
header.masthead h1 {{
  font-family: var(--display); font-weight: 600;
  font-size: clamp(2.1rem, 4.6vw, 3.4rem);
  line-height: 1.06; letter-spacing: -0.01em;
  margin: 0.45rem 0 0.7rem; max-width: 22ch;
}}
.colophon {{
  font-family: var(--sans); font-size: 0.8rem; color: var(--ink-soft);
}}
.colophon code {{ font-size: 0.75rem; }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} }}

/* ── chapter rail ─────────────────────────────────────────── */
nav.rail {{
  position: sticky; top: 1.6rem; align-self: start;
  max-height: calc(100vh - 3rem); overflow-y: auto;
  padding: 1.1rem 0 1.1rem 0.1rem;
  font-family: var(--sans);
  animation: rise 0.7s 0.12s cubic-bezier(0.2, 0.7, 0.2, 1) both;
}}
nav.rail .rail-title {{
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.2em;
  text-transform: uppercase; color: var(--ink-soft); margin-bottom: 0.7rem;
}}
nav.rail a {{
  display: block; padding: 0.28rem 0.6rem;
  font-size: 0.82rem; color: var(--ink-soft); text-decoration: none;
  border-left: 2px solid var(--hairline);
  transition: color 0.15s, border-color 0.15s, background 0.15s;
}}
nav.rail a:hover {{ color: var(--vermilion-deep); }}
nav.rail a.active {{
  color: var(--vermilion-deep); font-weight: 600;
  border-left-color: var(--vermilion); background: rgba(178, 58, 18, 0.05);
}}

/* ── article ──────────────────────────────────────────────── */
article {{ min-width: 0; animation: rise 0.7s 0.2s cubic-bezier(0.2, 0.7, 0.2, 1) both; }}
article > h1 {{ display: none; }} /* masthead carries the title */
article h2 {{
  font-family: var(--display); font-weight: 600; font-size: 1.72rem;
  line-height: 1.15; margin: 3.4rem 0 0.9rem; padding-top: 1.6rem;
  border-top: 1px solid var(--rule);
}}
article h3 {{
  font-family: var(--display); font-weight: 500; font-size: 1.22rem;
  margin: 2.2rem 0 0.6rem; color: var(--vermilion-deep);
}}
article h4 {{
  font-family: var(--sans); font-weight: 700; font-size: 0.85rem;
  letter-spacing: 0.14em; text-transform: uppercase; margin: 1.8rem 0 0.5rem;
}}
article p {{ margin: 0.7rem 0; max-width: 76ch; }}
article a {{ color: var(--teal); text-decoration-color: rgba(31, 106, 92, 0.4); text-underline-offset: 2px; }}
article a:hover {{ color: var(--vermilion-deep); }}
.headerlink {{ opacity: 0; margin-left: 0.35rem; font-size: 0.8em; text-decoration: none; }}
h2:hover .headerlink, h3:hover .headerlink, h4:hover .headerlink {{ opacity: 0.55; }}
article hr {{ border: 0; border-top: 3px double var(--rule); margin: 3rem 0 1.5rem; }}
article em {{ color: var(--ink-soft); }}
code {{
  font-family: var(--mono); font-size: 0.82em;
  background: rgba(160, 142, 111, 0.16); border-radius: 3px; padding: 0.08em 0.32em;
}}

/* ── tables: Tufte-ish rules, sans density ────────────────── */
table {{
  width: 100%; border-collapse: collapse; margin: 1rem 0 1.6rem;
  font-family: var(--sans); font-size: 0.86rem; line-height: 1.45;
  background: var(--card); box-shadow: 0 1px 0 var(--hairline), 0 -1px 0 var(--hairline);
}}
thead th {{
  text-align: left; font-size: 0.7rem; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-soft);
  padding: 0.55rem 0.8rem; border-bottom: 2px solid var(--ink);
}}
tbody td {{
  padding: 0.6rem 0.8rem; border-bottom: 1px solid var(--hairline);
  vertical-align: top;
}}
tbody tr:hover {{ background: rgba(178, 58, 18, 0.035); }}
td:first-child {{ min-width: 15ch; }}
td small {{ display: block; margin-top: 0.15rem; color: var(--ink-soft); font-size: 0.78rem; }}
/* Field tables (tagged by JS): fixed column rhythm, nowrap tier badges. */
table.fields td:last-child {{ white-space: nowrap; font-size: 0.8rem; }}
table.fields[data-cols="5"] th:nth-child(1) {{ width: 15%; }}
table.fields[data-cols="5"] th:nth-child(2) {{ width: 35%; }}
table.fields[data-cols="5"] th:nth-child(3) {{ width: 26%; }}
table.fields[data-cols="5"] th:nth-child(4) {{ width: 15%; }}
table.fields[data-cols="5"] th:nth-child(5) {{ width: 9%; }}
table.fields[data-cols="5"] td:nth-child(3) {{ color: #4a3f30; }}
table.fields[data-cols="5"] td:nth-child(4) {{ font-size: 0.8rem; }}

/* ── admonition (from `!!! info`) ─────────────────────────── */
.admonition {{
  background: var(--card); border: 1px solid var(--hairline);
  border-left: 4px solid var(--vermilion);
  padding: 0.9rem 1.2rem; margin: 1.6rem 0; max-width: 76ch;
  box-shadow: 3px 3px 0 rgba(36, 28, 18, 0.06);
}}
.admonition-title {{
  font-family: var(--sans); font-weight: 700; font-size: 0.74rem;
  letter-spacing: 0.16em; text-transform: uppercase; color: var(--vermilion-deep);
  margin: 0 0 0.4rem;
}}

/* ── mermaid ──────────────────────────────────────────────── */
.mermaid {{
  background: var(--card); border: 1px solid var(--hairline);
  padding: 1.2rem; margin: 1.4rem 0; overflow-x: auto;
}}
/* The rendered label font MUST match the font mermaid measures with
   (themeVariables.fontFamily below): the page's serif otherwise bleeds
   into the SVG labels, whose wider metrics crop the last glyph. */
.mermaid svg, .mermaid .nodeLabel, .mermaid .cluster-label {{
  font-family: "Source Sans 3", sans-serif !important;
}}

@media (max-width: 940px) {{
  .frame {{ grid-template-columns: 1fr; gap: 0; padding: 0 1.2rem 4rem; }}
  nav.rail {{ position: static; max-height: none; border-bottom: 1px solid var(--hairline); margin-bottom: 1rem; }}
}}
@media print {{
  nav.rail {{ display: none; }}
  .frame {{ grid-template-columns: 1fr; }}
  body::before {{ display: none; }}
}}
</style>
</head>
<body>
<div class="frame">
  <header class="masthead">
    <div class="kicker">EnVar Microschemas · Schema Overview</div>
    <h1>{title}</h1>
    <nav class="crumbs" aria-label="Site">
      <a href="../">← Docs home</a><span>·</span><a href="../elements/">Element reference</a><span>·</span><a href="../dashboard/">Completeness ledger</a>
    </nav>
    <div class="colophon">Rendered from <code>docs/schema_overview.md</code> as part of <code>just site</code> — regenerate with <code>just render-schema-overview</code>.</div>
  </header>
  <nav class="rail" aria-label="Sections">
    <div class="rail-title">Contents</div>
    {rail}
  </nav>
  <article>
    {body}
  </article>
</div>
<script type="module">
  // Lift fenced mermaid blocks out of <pre><code> and render them.
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  document.querySelectorAll("pre > code.language-mermaid").forEach((code) => {{
    const holder = document.createElement("div");
    holder.className = "mermaid";
    holder.textContent = code.textContent;
    code.closest("pre").replaceWith(holder);
  }});
  mermaid.initialize({{
    startOnLoad: false,
    theme: "base",
    themeVariables: {{
      background: "#fbf7ee",
      primaryColor: "#efe6d4",
      primaryTextColor: "#241c12",
      primaryBorderColor: "#a08e6f",
      lineColor: "#5c5243",
      clusterBkg: "#f3ecdd",
      clusterBorder: "#d8cbb2",
      fontFamily: "Source Sans 3, sans-serif",
      fontSize: "14px",
    }},
  }});
  // Render only once the webfonts have loaded: mermaid measures node
  // widths at render time, and if Source Sans 3 swaps in afterwards the
  // slightly wider metrics crop the last glyph in each box.
  await document.fonts.load('14px "Source Sans 3"');
  await document.fonts.ready;
  mermaid.run({{ querySelector: ".mermaid" }});

  // Tag field tables so CSS can give them a fixed column rhythm without
  // disturbing enum / at-a-glance tables.
  document.querySelectorAll("article table").forEach((t) => {{
    const heads = t.querySelectorAll("thead th");
    if (heads[0]?.textContent.trim() === "Field") {{
      t.classList.add("fields");
      t.dataset.cols = String(heads.length);
    }}
  }});

  // Chapter-rail scroll spy.
  const links = new Map(
    [...document.querySelectorAll("nav.rail a")].map((a) => [a.hash.slice(1), a])
  );
  const spy = new IntersectionObserver(
    (entries) => {{
      for (const e of entries) {{
        if (e.isIntersecting) {{
          links.forEach((a) => a.classList.remove("active"));
          links.get(e.target.id)?.classList.add("active");
        }}
      }}
    }},
    {{ rootMargin: "0px 0px -75% 0px" }}
  );
  links.forEach((_, id) => {{
    const el = document.getElementById(id);
    if (el) spy.observe(el);
  }});
</script>
</body>
</html>
"""


def _rewrite_internal_links(body: str) -> str:
    """Point relative ``*.md`` links at their deployed mkdocs URLs.

    The overview source lives at the docs root but deploys under
    ``overview/``, and mkdocs turns ``foo.md`` into ``foo/`` (directory
    URLs) — so ``elements/index.md`` must become ``../elements/``.
    """

    def repl(match: re.Match[str]) -> str:
        path = match.group(1)
        if path.endswith("index.md"):
            target = path[: -len("index.md")]
        else:
            target = path[: -len(".md")] + "/"
        return f'href="../{target}"'

    return re.sub(r'href="(?!(?:[a-z]+:|#|/))([^"]+\.md)"', repl, body)


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    # Drop the "auto-generated" HTML comment header.
    text = re.sub(r"\A<!--.*?-->\s*", "", text, flags=re.DOTALL)

    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "admonition", "toc"],
        extension_configs={"toc": {"permalink": "¶"}},
    )
    body = _rewrite_internal_links(md.convert(text))

    title = "What the EnVar schema captures"
    rail_links: list[str] = []
    for token in md.toc_tokens:
        if token["level"] == 1 and token["name"]:
            title = token["name"]
        for child in token["children"] if token["level"] == 1 else [token]:
            if child["level"] == 2:
                rail_links.append(f'<a href="#{child["id"]}">{child["name"]}</a>')
    rail = "\n    ".join(rail_links)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(TEMPLATE.format(title=title, rail=rail, body=body), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
