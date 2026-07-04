# Related approaches

A recurring question about EnVar is *"isn't this the same as X?"* — where X is GAIA, DeGAUSS,
Amadeus, or the CODATA Essential Variables work. The honest answer is that each overlaps with
**part** of EnVar, but operates at a different **granularity** or for a different **purpose**.
This page draws the lines.

## What EnVar is, in one sentence

> An EnVar sidecar is an **instance-level provenance record** — one document per *(variable, run)* —
> that describes how a *specific* environmental value (or homogeneous value series) was produced,
> in enough detail that the result can be reproduced from raw data plus the sidecar alone, and
> that two values can be checked for whether they may legitimately be pooled.

The key word is **instance**. EnVar does not catalogue datasets, define which variables matter, or
geocode addresses. It records the methodological identity of a value that has already been produced.

Two axes separate it from everything below:

- **Unit of description** — what is *one record* about? A whole dataset, a variable *type*, a
  geocoded row, or one produced value?
- **Purpose** — *find* it, *define* it, *compute* it, or *reproduce/pool* it?

| Approach | Unit of description | Primary purpose | Carries derivation metadata? |
|---|---|---|---|
| **GAIA catalog files** | a dataset | discovery | no — dataset-level description |
| **DeGAUSS** | a geocoded row | compute the linkage | partially — tool-run + geocoding precision |
| **Amadeus** | a downloaded file | access + cite the source | minimal — acknowledgement + hashes |
| **CODATA Essential Variables** | a variable *type / concept* | commensurability + interoperability | at the *conceptual* layer, not the *instance* layer |
| **EnVar sidecar** | one produced value series *(variable, run)* | reproducibility + poolability | **yes — that is the whole point** |

---

## 1. GAIA catalog files

**What it is.** The GAIA toolchain (OHDSI GIS Working Group) is a catalogue + database for
place-based exposure datasets. Each dataset in `gaiaCatalog` carries **three metadata files**:

| File | Standard | Role |
|---|---|---|
| `meta_dcat_*.json` | DCAT | discovery record for catalogue search |
| `meta_etl_*.json` | custom | ETL instructions for ingest into gaiaDB |
| `meta_json-ld_*.json` | Schema.org JSON-LD | linked-data description of the dataset |

**Granularity.** Dataset-level. One GAIA card describes a whole product — e.g. *"PM2.5, CMAQ, US,
2000–2020, 12 km."* It is built to help you **find** a dataset, not to explain any single value
inside it.

**How it differs from EnVar.** A GAIA card describes the *crate*; an EnVar sidecar describes one
*item taken out of the crate and assigned to a person*. The fields EnVar exists to capture —
`extraction_method`, `day_boundary_convention`, `geocoding_precision_propagated`,
`container_image_digest` — are properties of the **extraction run**, not of the published dataset,
so they cannot live on a GAIA card. (You *can* read a dataset card down onto every value in it, but
only while the dataset is internally homogeneous and the values are untransformed — which stops
being true the moment a value is extracted, linked, or pooled into a destination table like OMOP
`external_exposure`.)

!!! note "Complementary, not competing"
    The two stack: use GAIA to discover the PM2.5 product, use EnVar to describe each value you
    extract from it. Because EnVar is authored in LinkML, it can **emit the Schema.org JSON-LD that
    GAIA consumes** — so EnVar's instance-level detail can flow up into the catalogue rather than
    sitting in a separate silo.

---

## 2. DeGAUSS

**What it is.** DeGAUSS (Brokamp / Cincinnati Children's) is a privacy-preserving **geocoding and
geomarker pipeline**, distributed as versioned Docker containers that run *inside* the institution,
so no PHI leaves the site. It geocodes a patient address and appends geomarker columns (including
the extracted environmental value) to the data, recording the geocoding **precision** and **match
score** and the exact container image used.

**Granularity.** Per geocoded row. DeGAUSS's metadata is about *this linkage event* — how well the
address resolved and which tool version produced the value.

**How it differs from EnVar.** DeGAUSS is a **producer**; EnVar is a **description of what a producer
did**. The two are not alternatives — the EnVar "ideal" TMAX scenario *is* a DeGAUSS → Daymet run.
DeGAUSS is strong exactly where it acts (geocoding precision/score, reproducible container
provenance) and silent on the rest of the derivation:

| Axis | DeGAUSS records | EnVar adds |
|---|---|---|
| Linkage | precision, match score, container image | normalises into `LinkageMethod` + `geocoding_*` slots |
| Source product | (implicit in the container) | version, DOI, license, homogenisation status |
| Model | — | model class, known biases, cross-validation R² |
| Temporal semantics | — | `day_boundary_convention`, aggregation, calendar |
| Uncertainty | — | per-value + aggregate uncertainty |
| Requirement level | — | Core / Recommended / Optional tiers + completeness score |

In short, DeGAUSS guarantees *reproducible computation*; EnVar guarantees that the **choices that
computation made are written down in a standard, scoreable form**.

---

## 3. Amadeus

**What it is.** Amadeus (NIEHS, Messier group) is an **R package for accessing and processing**
large environmental datasets — GridMET, NARR, MERRA-2, MODIS, EPA AQS, and ~20 more sources. When it
downloads data it can attach an **acknowledgement string** and **file hashes** (`acknowledgement = TRUE,
hash = TRUE`).

**Granularity.** Per downloaded file. Amadeus's metadata answers *"where did these bytes come from
and how do I cite them."*

**How it differs from EnVar.** Amadeus is the **data-access layer**; its emitted metadata is a
free-text acknowledgement plus integrity hashes. That is genuinely useful — and genuinely thin: it
does not record the product *version*, the day-boundary convention, the extraction rule, or the model
class. The EnVar "minimum" TMAX scenario *is* an Amadeus → GridMET output, and it is the deliberate
**"before" picture**: a real sidecar that scores poorly because the Core fields are absent
(recorded as `null` with a missing-reason, not silently dropped).

!!! example "Same value, two representations"
    Amadeus today emits: `acknowledgement: "Data provided by the University of Idaho; GridMET via
    Amadeus."` + `input_file_sha256` + `output_file_sha256`.
    EnVar wraps that and demands the rest: `source_dataset_version`, `day_boundary_convention`,
    `extraction_method`, `exposure_model_type`, … — and reports what is still missing.

EnVar does not replace Amadeus; it **standardises and extends what an Amadeus run should emit** so
its output can land in OMOP reproducibly.

---

## 4. CODATA Essential Variables (and CDIF)

**What it is.** "Essential Variables" (EVs) come from the Earth-observation community: a curated,
community-agreed minimal set of variables *necessary and sufficient* to monitor a system —
Essential **Climate** Variables (GCOS), Essential **Ocean** Variables (GOOS), Essential
**Biodiversity** Variables (GEO BON); clinical CDEs play the same role in health. CODATA (Simon
Hodson) generalised these into a **family of EV frameworks** and observed that the interesting part
is not the variable *lists* but the **data-description semantics underneath them** — the machinery
that governs whether two measurements of "the same" variable may legitimately be combined.

That machinery is the **Cross-Domain Interoperability Framework (CDIF / CDIF4EOSC)**, which aligns
existing standards rather than inventing one. The piece that matters for EnVar is the **DDI-CDI
three-layer variable cascade**:

| Cascade layer | Means | Example |
|---|---|---|
| `ConceptualVariable` | *what is measured and why* (the claim) | "near-surface air temperature, as a heat stressor" |
| `RepresentedVariable` | value domain + units | `air_temperature`, °C |
| `InstanceVariable` | *this column, this file, this run* | the `tmax` value, extracted from Daymet V4 R1 |

EVs (and I-ADOPT, the vocabulary that decomposes a property into `object + property + matrix + …`)
live at the **conceptual / represented** layers. They tell you that surface temperature is an
essential variable, define it canonically, and let two communities agree they mean the same thing.

**How it differs from EnVar.** EnVar lives at the **`InstanceVariable`** layer. It is the detail an
EV definition deliberately does *not* carry: the version, the day-boundary, the extraction rule, the
container digest of one produced value. As Greenfield's CODATA data story puts it, EnVar and the EV
machinery are *"the same move at opposite ends of the same cascade"*:

| | Essential Variables / CDIF | EnVar sidecar |
|---|---|---|
| Entry layer | conceptual ("what is the claim?") | instance ("how was this number made?") |
| Direction | top-down (hypothesis → evidence) | bottom-up (bytes → methodological identity) |
| Question answered | "do we mean the same variable?" | "may I pool *these two values*?" |
| Packaging | DDI-CDI / Croissant `cr:Field` | LinkML micro-schema sidecar |

The shared thesis is **commensurability**. `43.91 °C` (Daymet) and `42.65 °C` (GridMET) for the
same patient-day is a commensurability failure wearing the costume of two equal numbers — and that
is precisely the "may I combine them?" question EV frameworks ask, answered at the layer where the
methodological differences actually live.

!!! note "Posture: speak the vocabulary, don't adopt the toolchain"
    EnVar is **not** a competitor to CDIF — it is the missing instance-layer detail that makes a
    CDIF/Croissant document safe to pool. A CDIF document can assert *"`temp_c` is air temperature"*;
    it cannot today assert *"and it was extracted by inverse-distance-weighting four cells, on a
    local-midnight day boundary, from Daymet V4 R1."* That second sentence is EnVar. The cheap,
    high-leverage alignment is to **expose an I-ADOPT projection of each EnVar variable** and to
    **label which cascade layer each sidecar field sits on** (CF/UCUM → `RepresentedVariable`;
    provenance → `InstanceVariable`) — without taking on the full EU/EOSC standards stack.

---

## Summary

| | Describes | Answers | Layer |
|---|---|---|---|
| **GAIA** | a dataset | "where do I find it?" | catalogue |
| **DeGAUSS** | a geocoded row | "how do I compute the linkage reproducibly?" | tool run |
| **Amadeus** | a downloaded file | "where did the bytes come from?" | data access |
| **Essential Variables / CDIF** | a variable concept | "do we mean the same thing?" | conceptual |
| **EnVar** | one produced value series | "how was this made — can I reproduce and pool it?" | **instance** |

None of these is redundant with EnVar, and EnVar does not replace any of them. EnVar fills the
**instance/provenance layer** that the others leave underspecified — and, because it is authored in
LinkML, it can export into the formats the others already consume (Schema.org JSON-LD for GAIA, the
DDI-CDI/Croissant vocabulary for CDIF).

This page and the coverage matrix ask what each standard is missing that EnVar has. The
[reverse gap survey](reverse-gap-survey.md) asks the opposite — which fields these systems
natively record that EnVar has no slot for — with a verdict (add / absorb / out of scope) per field.

### References

- GAIA: <https://github.com/OHDSI/gaiaCatalog>
- DeGAUSS: <https://degauss.org/> · Brokamp et al. 2018, *JAMIA*, doi:10.1093/jamia/ocx128
- Amadeus: Manware et al. 2025, *Environmental Modelling & Software* 186:106352
- CDIF (CODATA): <https://codata.org/release-of-the-cross-domain-interoperability-framework-cdif-version-1-1/>
- I-ADOPT: <https://i-adopt.github.io/> · DDI-CDI: <https://docs.ddialliance.org/DDI-CDI/1.0/> · Croissant: <https://github.com/mlcommons/croissant>
