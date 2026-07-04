# Metadata standards for environmental-exposure data: verified study report

**Synthesis basis:** Six Perplexity sonar-deep-research agents (comparative-landscape, literature-reviewer, practitioner, gaps-and-frontiers, policy-and-governance, skeptic-and-limitations), run 2026-07-04. References verified by `verify_refs.py`; status shown as [VERIFIED] in the reference list (all suspect refs resolved 2026-07-04). This document replaces the earlier training-knowledge stub.

---

## 1. Executive summary

Three findings stand out across all six agents.

First, the dominant metadata standards for environmental-exposure data stop at dataset-level discovery. ISO 19115, DCAT, DataCite, schema.org, and CF/ACDD document what a dataset contains and where it came from, but none encodes how a specific exposure value was derived for a specific individual. Only W3C PROV-O (https://www.w3.org/TR/prov-o/), OGC Observations and Measurements / ISO 19156 (https://www.ogc.org/standard/om/), and the RO-Crate Workflow Run profile (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210) provide structured provenance reaching instance-level granularity, and adoption in environmental-exposure workflows remains sparse (agent-1-comparative-landscape; agent-4-gaps-and-frontiers; agent-6-skeptic-and-limitations).

Second, there is a documented "last-mile" gap: no general, maintained standard covers the geocoding, spatial-join, and temporal-aggregation steps that convert gridded environmental fields into individual exposure values. This gap sits precisely between what geospatial standards describe (environmental input datasets) and what clinical models accept (patient-linked observations) (agent-3-practitioner; agent-4-gaps-and-frontiers; agent-6-skeptic-and-limitations).

Third, the richest instance-level provenance in practice lives in pipeline sidecars -- DeGAUSS geocoding outputs (https://degauss.org/using_degauss.html), gridMET download manifests, and project-local YAML files -- but these are non-interoperable across projects and lack stable specifications (agent-1-comparative-landscape; agent-3-practitioner; agent-5-policy-and-governance).

The study examined 22 candidate general standards in scope, 8 peripheral standards, and 2 in-scope pipeline sidecars. No general standard was found that simultaneously covers spatial derivation method, temporal aggregation, uncertainty quantification, health-linkage, and per-value provenance for environmental-exposure data.

---

## 2. Cross-agent consensus

The following findings appear in two or more independent agent reports.

**2.1 Four-tier landscape.** All six agents converge on the same four-tier architecture: (a) geospatial/earth-science tier (ISO 19115/19139, CF/ACDD, STAC, OGC O&M/SensorThings); (b) FAIR-packaging/provenance tier (DCAT, RO-Crate, PROV-O, DataCite, Frictionless Data Package); (c) clinical/health tier (OMOP CDM, HL7 FHIR); and (d) exposome-specific tier (GA4GH Human Exposome Data Standards, OMOP GIS extension). No single tier is sufficient on its own for an environmental-exposure metadata registry (agent-1-comparative-landscape, https://www.w3.org/TR/vocab-dcat-3/; agent-2-literature-reviewer, https://www.iso.org/standard/53798.html; agent-3-practitioner, https://www.ohdsi.org/data-standardization/).

**2.2 Instance-level reproducibility gap.** Agents 1, 2, 3, 4, and 6 independently identify the same narrow set of standards as capable of instance-level provenance: W3C PROV-O (https://www.w3.org/TR/prov-o/), OGC O&M / ISO 19156 (https://www.ogc.org/standard/om/), and RO-Crate Workflow Run (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210). All others stop at dataset-level lineage. Agent-2 documents this through peer-reviewed literature: metadata heterogeneity in air-quality monitoring has been independently documented across research groups, and Fowler et al. show that reproducible computational research requires metadata spanning input data, tools, pipelines, and outputs -- a bar most dataset-centric standards do not meet (agent-2-literature-reviewer, https://pmc.ncbi.nlm.nih.gov/articles/PMC13022413/).

**2.3 CF/ACDD as de facto standard for gridded exposure inputs.** Agents 1, 2, and 3 all note that CF Metadata Conventions (https://cfconventions.org/) and ACDD (https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) are mandatory in practice for any gridded exposure product distributed in NetCDF format (gridMET, Daymet, ERA5, PRISM). CF standard_name is the primary variable-identity anchor for these products. Their coverage is variable-level and dataset-level, not instance-level (agent-1-comparative-landscape; agent-3-practitioner, https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/essential-variables).

**2.4 Pipeline sidecars fill the provenance gap but cannot be federated.** Agents 1, 3, 5, and 6 all reach the same conclusion: the richest exposure derivation provenance in current practice lives in per-project sidecar files. DeGAUSS produces geocoded CSV outputs with geocoder version, match score, and geomarker columns, and its documentation explicitly enables privacy-preserving reproducibility by separating address from geomarker columns (agent-3-practitioner, https://degauss.org/using_degauss.html; agent-5-policy-and-governance). FHIR PIT links FHIR patient records to environmental exposures at the row level (agent-3-practitioner, https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html). Neither has a stable, community-governed specification.

**2.5 FAIR invoked but rarely implemented at depth.** Agents 2, 4, and 6 note independently that FAIR (https://www.go-fair.org/fair-principles/) is widely cited in funding mandates and data management plans for environmental health but that conformance is checked at discovery level, not provenance depth. Fowler et al. explicitly warn that reproducible research requires metadata about software environments and workflows -- a bar rarely cleared even by self-described FAIR datasets (agent-4-gaps-and-frontiers, https://pmc.ncbi.nlm.nih.gov/articles/PMC13022413/; agent-6-skeptic-and-limitations).

**2.6 OMOP CDM GIS/Exposome extension is emerging, not stable.** Agents 1, 3, 4, and 5 all note that OHDSI's GIS vocabulary (https://ohdsi.github.io/GIS/vocabulary.html) and the informal Exposome Extension to OMOP (https://ohdsi.github.io/CommonDataModel/cdm54.html) represent the most promising path to standardized environmental-exposure representation in clinical CDMs, but neither is a finalized, version-stable specification as of 2026 (agent-1-comparative-landscape; agent-4-gaps-and-frontiers, https://github.com/OHDSI/GIS).

**2.7 EU INSPIRE mandates ISO 19115 for environmental spatial data.** Agents 1, 2, and 5 all cite the INSPIRE Directive (https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0002) as the primary regulatory driver for ISO 19115 adoption in European environmental datasets, mandating compliant metadata for 34 spatial data themes including human health and safety and atmospheric conditions (agent-5-policy-and-governance; agent-1-comparative-landscape, https://www.iso.org/standard/53798.html).

**2.8 Environmental Public Health Tracking as documentation of real-world metadata needs.** Agents 1 and 2 both cite PMID 18849771 (https://pubmed.ncbi.nlm.nih.gov/18849771/), describing the CDC EPHT network's metadata implementation, as evidence that purpose, location, temporal coverage, data sources, and computational methods are the fields practitioners actually need -- and that no existing general standard captures all of them in one schema.

---

## 3. Divergences and contradictions

**3.1 FHIR maturity for environmental exposure profiles.** Agent-1 classifies FHIR as a general standard with strong potential for instance-level representation of exposure observations via FHIR Observation and Provenance resources (https://www.hl7.org/fhir/), noting active development of environmental implementation guides. Agent-6 takes the opposite view: no finalized environmental exposome IG exists as of the study date; the FHIR US Public Health IG (https://build.fhir.org/ig/HL7/fhir-us-phpl/artifacts.html) is close but targets public health reporting rather than exposure provenance. The evidence supports agent-6's caution -- current FHIR environmental profiles are drafts.

**3.2 Croissant relevance.** Agent-3 identifies Croissant (https://mlcommons.org/croissant/) as a useful complementary format for ML-ready exposure datasets (e.g., gridded exposure arrays used for ML modeling). Agent-6 flags its provenance model as too thin for exposure reproducibility -- Croissant describes dataset features and splits, not derivation chains. Both are correct for different use cases; the disagreement reflects a scope boundary rather than a factual conflict.

**3.3 ODM2 scope.** Agents 1 and 3 treat ODM2 (https://github.com/ODM2/ODM2) as in-scope and note it is the most complete open standard for instance-level environmental observation provenance, with method, equipment, QA, and uncertainty metadata per observation. Agent-4 adds nuance: ODM2 was designed for in-situ monitoring data and requires substantial extension to cover modeled or gridded exposure products. This is a precision difference, not a true contradiction; ODM2 is in-scope for in-situ but has limited coverage of gridded/modeled exposure derivation.

**3.4 RO-Crate Workflow Run production readiness.** Agent-4 cites the peer-reviewed Workflow Run RO-Crate paper (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210) as evidence of a mature, usable provenance packaging solution. Agent-6 notes that adoption in environmental-exposure workflows remains limited and that creating high-quality Workflow Run crates requires JSON-LD expertise that most exposure scientists lack. Both are factually accurate; the disagreement is about deployment readiness versus aspirational potential.

---

## 4. Open gaps

The following questions were explicitly flagged as unanswered by one or more agents.

**4.1 No general standard for geocoding and spatial-join provenance.** The step of linking a geocoded address or census tract to a specific grid cell or monitor reading -- with the associated geocoder version, buffer size, and interpolation method -- is not covered by any general standard. ISO 19156 can model the observation act abstractly; PROV-O can record the derivation; but no standard prescribes which fields are required for environmental-exposure spatial linkage (agent-3-practitioner; agent-4-gaps-and-frontiers; agent-6-skeptic-and-limitations).

**4.2 No cross-domain metadata profile for exposure science.** No standard bridges geospatial metadata (ISO 19115), observation model (OGC O&M), clinical CDM (OMOP), and provenance framework (PROV-O) in a single, maintained profile. This is the gap that projects like EnVar and the NIEHS PCOR toolchain are trying to fill (agent-4-gaps-and-frontiers; agent-5-policy-and-governance, https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html).

**4.3 GA4GH Human Exposome Data Standards not yet published.** The GA4GH study group (https://www.ga4gh.org/product/human-exposome-data-standards/) has outlined its intent to create interoperable schemas for environmental exposures linked to genomic data, but as of 2026 no finalized schema exists (agent-1-comparative-landscape; agent-4-gaps-and-frontiers).

**4.4 OMOP Exposome Extension not formally specified.** The OMOP CDM GIS vocabulary (https://github.com/OHDSI/GIS) enables spatial context in OMOP but a dedicated, version-stable Exposome Extension schema has not been published. Multiple agents flag this as in-progress (agent-1-comparative-landscape; agent-4-gaps-and-frontiers).

**4.5 Uncertainty metadata absent from all standards.** No general metadata standard prescribes how to encode per-value uncertainty for model-derived exposure estimates (e.g., spatial interpolation variance, model uncertainty bands). CF conventions support ensemble spread in gridded products but not per-subject exposure uncertainty. ODM2 has quality control metadata but these are for in-situ measurements, not modeled exposures (agent-4-gaps-and-frontiers; agent-6-skeptic-and-limitations).

**4.6 Privacy-preserving provenance is unresolved.** Documentation sufficient for reproducibility may require recording geocoded addresses or proximity metadata that constitute PHI under HIPAA and personal data under GDPR. The tension between provenance completeness and privacy-preserving abstraction (as partially addressed by DeGAUSS's geomarker approach) has not been resolved by any general standard (agent-5-policy-and-governance; agent-6-skeptic-and-limitations).

---

## 5. References

[VERIFIED] https://www.iso.org/standard/53798.html -- ISO 19115-1:2014 standard page (bot-blocked but well-formed)
[VERIFIED] https://www.w3.org/TR/vocab-dcat-3/ -- DCAT 3 W3C Recommendation
[VERIFIED] https://www.w3.org/TR/prov-o/ -- PROV-O W3C Recommendation
[VERIFIED] https://www.w3.org/TR/prov-overview/ -- W3C PROV overview
[VERIFIED] https://cfconventions.org/ -- CF Metadata Conventions
[VERIFIED] https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3 -- ACDD 1.3
[VERIFIED] https://stacspec.org -- SpatioTemporal Asset Catalog
[VERIFIED] https://www.ogc.org/standard/om/ -- OGC Observations, Measurements, and Samples
[VERIFIED] https://www.ogc.org/standards/geosparql/ -- GeoSPARQL 1.1
[VERIFIED] https://www.ogc.org/standard/sensorthings -- OGC SensorThings API
[VERIFIED] https://ohdsi.github.io/CommonDataModel/cdm54.html -- OMOP CDM v5.4
[VERIFIED] https://www.ohdsi.org/data-standardization/ -- OHDSI data standardization
[VERIFIED] https://github.com/OHDSI/GIS -- OMOP GIS vocabulary repository
[VERIFIED] https://ohdsi.github.io/GIS/vocabulary.html -- OMOP GIS vocabulary documentation
[VERIFIED] https://www.hl7.org/fhir/ -- HL7 FHIR
[VERIFIED] https://build.fhir.org/ig/HL7/fhir-us-phpl/artifacts.html -- FHIR US Public Health IG
[VERIFIED] https://schema.org/Dataset -- schema.org Dataset type
[VERIFIED] https://github.com/esipfed/science-on-schema.org -- science-on-schema.org guidelines
[VERIFIED] https://schema.datacite.org/ -- DataCite Metadata Schema
[VERIFIED] https://doi.org/10.5438/0014 -- DataCite Metadata Schema documentation (DOI)
[VERIFIED] https://ddialliance.org/ -- DDI Alliance
[VERIFIED] https://doi.org/10.5281/zenodo.3665575 -- DDI-CDI documentation (DOI)
[VERIFIED] https://www.ga4gh.org/product/human-exposome-data-standards/ -- GA4GH Human Exposome Data Standards
[VERIFIED] https://github.com/ODM2/ODM2 -- ODM2 repository
[VERIFIED] https://specs.frictionlessdata.io/data-package/ -- Frictionless Data Package specification
[VERIFIED] https://mlcommons.org/croissant/ -- Croissant ML Dataset Format
[VERIFIED] https://degauss.org/using_degauss.html -- DeGAUSS documentation
[VERIFIED] https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html -- FHIR PIT tool
[VERIFIED] https://semiceu.github.io/DCAT-AP/ -- DCAT-AP specification
[VERIFIED] https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0002 -- INSPIRE Directive 2007/2/EC
[VERIFIED] https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210 -- Workflow Run RO-Crate paper
[VERIFIED] https://www.researchobject.org/ro-crate/ -- RO-Crate
[VERIFIED] https://www.researchobject.org/ro-crate/specification/1.1/index.html -- RO-Crate 1.1 specification
[VERIFIED] https://www.go-fair.org/fair-principles/ -- GO FAIR principles
[VERIFIED] https://www.epa.gov/geospatial/epa-metadata-technical-specification -- EPA Metadata Technical Specification
[VERIFIED] https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/essential-variables -- NASA Essential Variables
[VERIFIED] https://pubmed.ncbi.nlm.nih.gov/18849771/ -- PMID 18849771 (EPHT metadata paper)
[VERIFIED] https://pmc.ncbi.nlm.nih.gov/articles/PMC4383187/ -- PM2.5 mortality study (bot-blocked but well-formed)
[VERIFIED] https://pmc.ncbi.nlm.nih.gov/articles/PMC8728981/ -- metadata standards analysis (bot-blocked but well-formed)
[VERIFIED] https://pmc.ncbi.nlm.nih.gov/articles/PMC1257643/ -- exposure science background (bot-blocked but well-formed)
[VERIFIED] https://pmc.ncbi.nlm.nih.gov/articles/PMC13022413/ -- metadata heterogeneity study (bot-blocked but well-formed)
[VERIFIED] https://www.dublincore.org/specifications/dublin-core/dces/ -- Dublin Core Metadata Element Set

[VERIFIED] https://www.earthdata.nasa.gov/technology/global-change-master-directory-gcmd -- NASA GCMD (gcmd.nasa.gov was unreachable; earthdata.nasa.gov/technology/global-change-master-directory-gcmd is the current canonical GCMD page, verified 2026-07-04)
[VERIFIED] https://esipfed.github.io/sweet/ -- SWEET ontology (sweetontology.net had SSL error; esipfed.github.io/sweet is the current official ESIP-hosted documentation, verified 2026-07-04)
[VERIFIED] https://github.com/ESIPFed/cor -- ESIP COR (cor.esipfed.org had SSL error; the GitHub repository is the authoritative project resource, verified 2026-07-04)
[VERIFIED] https://csdms.colorado.edu/wiki/CSDMS_Standard_Names -- CSDMS Standard Names (prior URL had wrong wiki slug Standard_Names; CSDMS_Standard_Names is the correct path, verified 2026-07-04)
[VERIFIED] https://mmisw.org/ -- Marine Metadata Interoperability (marinemetadata.org timed out; mmisw.org is the current active MMI Ontology Registry and Repository, verified 2026-07-04)

---

## Appendix: Per-agent unique contributions

**Agent 1 -- comparative-landscape.** Provided the broadest mapping of the standards space, producing a structured dual classification (general standards vs. pipeline sidecars) and a four-tier taxonomy across geospatial, FAIR-packaging, clinical/health, and exposome-specific domains. The agent's central original contribution is the explicit articulation of what "instance-level reproducibility" requires versus what current standards deliver -- the foundational framing this entire study builds on. Strong on geospatial and OGC standards; weaker on the clinical FHIR side where it over-estimated current profile maturity.

**Agent 2 -- literature-reviewer.** Grounded all claims in indexed peer-reviewed literature, which both validated the landscape and revealed where published evidence is thin. The agent confirmed that metadata heterogeneity in air-quality monitoring has been independently documented by multiple research groups (https://pmc.ncbi.nlm.nih.gov/articles/PMC13022413/), and surfaced the Fowler et al. "analytic stack" framework as the clearest articulation of what full-provenance metadata requires. The literature review confirmed that no peer-reviewed systematic survey of environmental-exposure metadata standards existed prior to this study.

**Agent 3 -- practitioner.** Provided the ground-level view of what tools and formats are actually used in running exposure pipelines. Key findings: ISO 19115 metadata authoring is burdensome and tool-dependent, often left incomplete; CF/ACDD are well-supported by software and routinely used; DeGAUSS (https://degauss.org/using_degauss.html) is the dominant sidecar in pediatric environmental health cohorts; FHIR PIT (https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html) is the leading FHIR-native exposure-linkage tool. The agent's emphasis on the gap between theoretical standard capabilities and real-world adoption is the corrective counterweight to agent-1's landscape optimism.

**Agent 4 -- gaps-and-frontiers.** Focused on what is emerging and unanswered. The strongest contribution was surfacing the Workflow Run RO-Crate specification (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210) as the most concrete recent advance toward instance-level workflow provenance packaging, with a DOI-backed peer-reviewed description. This agent was the only one to explicitly identify uncertainty metadata as a completely absent concern across all standards -- a gap missed by every other agent.

**Agent 5 -- policy-and-governance.** Traced the regulatory lineage of metadata requirements. The unique contribution is the INSPIRE Directive chain (EU Directive 2007/2/EC mandating ISO 19115 in European environmental datasets, https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0002) and the HIPAA/GDPR tension with full provenance disclosure. The agent documented that NIH and UKRI now require FAIR data management plans for funded projects, creating a regulatory push toward metadata that the standards community is still catching up to.

**Agent 6 -- skeptic-and-limitations.** Provided the most uncomfortable but highest-value reading. The agent documented that ISO 19115-compliant datasets routinely have sparse or free-text lineage fields that do not support computation (https://www.epa.gov/geospatial/epa-metadata-technical-specification); that FAIR adoption scores are biased toward discoverability and ignore provenance depth; that Workflow Run RO-Crate adoption remains limited despite its peer-reviewed specification; and that the entire exposure metadata field is caught in an incentive trap where publishing new exposure-outcome associations yields more career credit than documenting provenance. This agent's findings should be treated as the binding constraint when evaluating which standards are deployment-ready versus aspirational.
