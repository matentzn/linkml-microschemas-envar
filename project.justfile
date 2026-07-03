## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Generate docs/schema_overview.md — the human-readable tour of the schema
gen-schema-overview:
    uv run python scripts/gen_schema_overview.py

# Render docs/schema_overview.md as a standalone HTML page (tmp/schema_overview.html)
render-schema-overview: gen-schema-overview
    uv run python scripts/render_schema_overview_html.py

# Score sidecar(s) against the schema tier annotations (completeness checker)
check +FILES:
    uv run python -m linkml_microschemas_envar.checker {{FILES}}

# Regenerate docs/datasets/index.html — the computed example-dataset ledger
gen-datasets-ledger:
    uv run python scripts/gen_datasets_ledger.py
