# Study design: Metadata standards for environmental-exposure data

## Original prompt (verbatim user input)

> Execute the `study` skill end-to-end for a standards survey, in the repo `/Users/matentzn/ws/projects/linkml-microschemas-envar`. Fixed slug: `study-env-exposure-metadata-standards`. N = 6 agents with roles: `comparative-landscape`, `literature-reviewer`, `practitioner`, `gaps-and-frontiers`, `policy-and-governance`, `skeptic-and-limitations`.

## Parameters

- Slug: `study-env-exposure-metadata-standards`
- N agents: 6
- Model: `perplexity / sonar-deep-research` (reasoning_effort=high)
- Estimated cost: ~$48–$90 USD

## Core research brief (shared across all agents)

This study surveys the complete landscape of **metadata standards and structured-metadata formats** used to describe **environmental-exposure data** — data quantifying human or population exposure to environmental factors (heat, air pollution, wildfire smoke, etc.), optionally linked to health outcomes — for the purposes of reuse, reproducibility, and meta-analysis.

Scope — IN: any standard, specification, schema, or structured format whose purpose is to record metadata ABOUT environmental-exposure datasets or values so they can be found, understood, reproduced, or pooled. Two classes to distinguish: (a) GENERAL STANDARDS intended to be reusable and interoperable across data producers (e.g. DCAT, ISO 19115/19139/19156, schema.org / science-on-schema.org, STAC, RO-Crate, Croissant, DDI, W3C PROV, DataCite, Frictionless Data Package, CDIF, CODATA Essential Variables, OMOP CDM external_exposure / GIS / Exposome extensions, FHIR environmental profiles, ACDD/CF metadata conventions); and (b) PIPELINE SIDECARS — structured but per-pipeline documentative formats never intended as general standards (e.g. DeGAUSS geocoding sidecars, Amadeus/gridMET download sidecars, project-local YAML metadata).

Scope — OUT (note only as context / vocabularies-used, NOT primary entries): pure controlled vocabularies / ontologies / thesauri (ENVO, SWEET, CF standard names, QUDT, AGROVOC, GCMD, SVO, GeoNames, Getty TGN, USGS Thesaurus, EnvThes, WoRMS, etc.) and projects / data-platforms themselves (CDC Environmental Public Health Tracking, exposome cohorts).

Questions the study must answer:
1. What metadata standards and structured formats exist for environmental-exposure data, across earth/climate science, geospatial/OGC, clinical/health, provenance/FAIR packaging, and exposure science?
2. For each: governing body and maturity; the unit it describes (dataset / variable-type / geocoded-row / produced-value / file); primary purpose (find / define / compute / reproduce-pool / cite); whether it carries derivation/provenance metadata; domain specificity (env-health-specific vs general-purpose); canonical spec URL.
3. Which are general standards vs pipeline sidecars?
4. Which carry enough provenance/derivation detail to support INSTANCE-LEVEL reproducibility of a produced exposure value, and which stop at dataset-level discovery?
5. For EACH candidate in the todo.md list below, is it a metadata standard in scope, peripheral, or out of scope, and why (one line each)?

todo.md candidate list to assess explicitly: CGI Vocabularies Register; Global Change Master Directory (GCMD); GCMD Science Keywords; ODM2; NERC Vocabulary Server (NVS); USGS Thesaurus; ESIP Community Ontology Repository (COR); AGROVOC; BioPortal; SWEET; EcoPortal; Agroportal; Environmental Thesaurus (EnvThes); GBIF Vocabulary Service; Environment Ontology (EnvO); GeoSPARQL; Scientific Variables Ontology (SVO); Climate Forecast Standard Name Table (CF); Darwin Core (DwC); MMI Ontology Registry and Repository; RRUFF; American Geological Institute Glossary of Geology; Research Vocabularies Australia; CSDMS Standard Names; Marine Metadata Interoperability Project; BARTOC; World Meteorological Office (WMO); IODE Ocean Data Portal parameter dictionary; BCO-DMO; Collections Descriptions; MIDS; EFG; QUDT; MINDAT; 4TU.ResearchData; WoRMS; EU Vocabularies; GeoNames; Getty Thesaurus of Geographic Names; ECSO (Ecosystems Ontology); GeoCore Ontology; Astronomical Environment Ontology; Ontobee; OBO Foundry; CAB Thesaurus; ANZSRC 2020; Aquatic Sciences and Fisheries Thesaurus; WorldBank Thesaurus; TERN Controlled Vocabularies; Coastal and Marine Ecological Classification Standard (CMECS); Darwin Core; ODM2.

Evidence: prefer official standard documents / standards-body pages (W3C/OGC/ISO/RDA/CODATA/OHDSI) and peer-reviewed or authoritative grey literature over blogs. Every standard named must carry a canonical URL or DOI. Audience: schema engineers building an environmental-exposure metadata registry who need to know what already exists and how each relates to instance-level exposure provenance. Global scope; emphasise currently-maintained standards but include foundational older ones (ISO 19115, DCAT) still in use.

## Reference rule (shared across all agents)

```
## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
```

## Per-agent prompts

### Agent 1 — comparative-landscape

**Role addendum:**

```
## Role addendum: comparative landscape

Map the space. Produce a structured comparison of the main contenders
(competing methods, datasets, standards, projects, vendors). For each:
who maintains it, scope, license/access model, adoption indicators
(citations, GitHub stars, listed users, regulatory uptake), and the
distinguishing axis along which it differs from the others. Aim for a
comparative table where one is feasible. Where two entities are often
confused, clarify the actual difference with citations. Avoid ranking;
your job is to map, not judge.
```

**Full composed prompt sent to Perplexity** (core + addendum + reference rule):

```
[See: deep-research/agent-1-comparative-landscape.prompt.md]
```

### Agent 2 — literature-reviewer

**Role addendum:**

```
## Role addendum: literature reviewer

Approach this as a careful synthesis of the peer-reviewed scholarly
record. Prioritize, in order: systematic reviews and meta-analyses;
original primary research in indexed journals; conference proceedings
from established venues; preprints (only when no peer-reviewed work
exists). Track-record matters more than novelty: if a finding is
repeated across multiple independent groups, say so. Where the
literature is thin, say that explicitly rather than backfilling with
grey sources. Default to neutral synthesis voice.
```

**Full composed prompt sent to Perplexity** (core + addendum + reference rule):

```
[See: deep-research/agent-2-literature-reviewer.prompt.md]
```

### Agent 3 — practitioner

**Role addendum:**

```
## Role addendum: practitioner / applied user

Take the perspective of a working practitioner who must actually use
these methods, datasets, tools, or standards in a real setting (a
clinic, a public-health agency, a data pipeline, a regulatory filing).
Emphasize: implementation cost, deployment friction, documentation
quality, real-world performance vs. benchmark performance, vendor
lock-in, and what the field's practitioners actually complain about
in conference talks, GitHub issues, and Slack/listserv discussions.
Cite practitioner-authored case studies, tool-comparison reports,
operational post-mortems where available.
```

**Full composed prompt sent to Perplexity** (core + addendum + reference rule):

```
[See: deep-research/agent-3-practitioner.prompt.md]
```

### Agent 4 — gaps-and-frontiers

**Role addendum:**

```
## Role addendum: gaps and frontiers

Focus on what is missing or just-emerging. Identify: questions the
literature explicitly flags as unanswered; datasets or measurements
that researchers say they need but don't have; proposed standards or
tools still at the draft / prototype / RFC stage; recent (last 24
months) preprints that may presage a shift. Distinguish between
"genuinely open question" and "answered but not yet disseminated".
For each gap, cite the source(s) flagging it as a gap.
```

**Full composed prompt sent to Perplexity** (core + addendum + reference rule):

```
[See: deep-research/agent-4-gaps-and-frontiers.prompt.md]
```

### Agent 5 — policy-and-governance

**Role addendum:**

```
## Role addendum: policy and governance

Approach as a policy analyst. Identify: applicable regulations,
standards bodies, funding agency requirements, data-sharing mandates,
privacy/ethics frameworks, and the institutions that enforce them.
For each, cite the actual regulatory text, standard document, or
agency guidance. Trace the lineage of major requirements (which
directive / law / agency memo introduced them). Where compliance
practice diverges from the letter of the rule, document that gap.
Cover jurisdictional variation (US/EU/UK at minimum) where relevant.
```

**Full composed prompt sent to Perplexity** (core + addendum + reference rule):

```
[See: deep-research/agent-5-policy-and-governance.prompt.md]
```

### Agent 6 — skeptic-and-limitations

**Role addendum:**

```
## Role addendum: skeptic and limitations

Adopt the stance of an informed skeptic. For each major claim, dataset,
tool, or standard discussed: identify the strongest documented
criticism, replication failure, methodological objection, or known
limitation. Where consensus exists, find the dissenting evidence and
attribute it. Where consensus is presumed but not actually established,
say so. Surface conflicts of interest, funding biases, and known
reproducibility issues. Your output should be uncomfortable reading
for advocates of the field — but every objection must carry a citation.
```

**Full composed prompt sent to Perplexity** (core + addendum + reference rule):

```
[See: deep-research/agent-6-skeptic-and-limitations.prompt.md]
```

## Outputs

- `deep-research/agent-1-comparative-landscape.md` — agent 1 report
- `deep-research/agent-1-comparative-landscape.citations.md` — citations
- `deep-research/agent-2-literature-reviewer.md` — agent 2 report
- `deep-research/agent-2-literature-reviewer.citations.md` — citations
- `deep-research/agent-3-practitioner.md` — agent 3 report
- `deep-research/agent-3-practitioner.citations.md` — citations
- `deep-research/agent-4-gaps-and-frontiers.md` — agent 4 report
- `deep-research/agent-4-gaps-and-frontiers.citations.md` — citations
- `deep-research/agent-5-policy-and-governance.md` — agent 5 report
- `deep-research/agent-5-policy-and-governance.citations.md` — citations
- `deep-research/agent-6-skeptic-and-limitations.md` — agent 6 report
- `deep-research/agent-6-skeptic-and-limitations.citations.md` — citations
- `deep-research/verification-report.md` — main-agent ref check
- `REPORT.md` — consolidated synthesis
