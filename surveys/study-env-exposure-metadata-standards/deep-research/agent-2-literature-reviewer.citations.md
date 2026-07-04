# Citations for Research Query

**Query:** This study surveys the complete landscape of **metadata standards and structured-metadata formats** used to describe **environmental-exposure data** — data quantifying human or population exposure to environmental factors (heat, air pollution, wildfire smoke, etc.), optionally linked to health outcomes — for the purposes of reuse, reproducibility, and meta-analysis.

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

## Role addendum: literature reviewer

Approach this as a careful synthesis of the peer-reviewed scholarly
record. Prioritize, in order: systematic reviews and meta-analyses;
original primary research in indexed journals; conference proceedings
from established venues; preprints (only when no peer-reviewed work
exists). Track-record matters more than novelty: if a finding is
repeated across multiple independent groups, say so. Where the
literature is thin, say that explicitly rather than backfilling with
grey sources. Default to neutral synthesis voice.

## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
**Provider:** perplexity
**Generated:** 2026-07-04T14:35:53.753013

1. https://pubmed.ncbi.nlm.nih.gov/18849771/
2. https://pmc.ncbi.nlm.nih.gov/articles/PMC13022413/
3. https://semiceu.github.io/DCAT-AP-reuse-guidelines/
4. https://schema.org/Dataset
5. https://github.com/esipfed/science-on-schema.org
6. https://stacspec.org
7. https://www.iso.org/standard/53798.html
8. https://www.iso.org/obp/ui/
9. https://rd-alliance.github.io/metadata-directory/standards/observations-and-measurements.html
10. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
11. https://schema.datacite.org
12. https://www.ohdsi.org/data-standardization/
13. https://www.ogc.org/standards/geosparql/
14. https://www.ohdsi.org/web/wiki/doku.php?id=projects%3Aworkgroups%3Agis
15. https://build.fhir.org/ig/HL7/fhir-us-phpl/artifacts.html
16. https://ddialliance.org
17. https://www.researchobject.org/ro-crate/specification/1.1/index.html
18. https://www.qudt.org/2.1/catalog/qudt-catalog.html
19. http://www.ukoln.ac.uk/metadata/rslp/schema/
20. https://pmc.ncbi.nlm.nih.gov/articles/PMC1257643/
21. http://www.opengeospatial.org/standards/om
22. https://www.w3.org/TR/vocab-dcat-3/
23. https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/document/dcat-ap-v21
24. https://doi.org/10.5438/0014
25. https://www.dublincore.org/specifications/dublin-core/dces/
26. https://schema.org/
27. https://doi.org/10.5281/zenodo.3665575
28. https://cfconventions.org/
29. https://specs.frictionlessdata.io/data-package/
30. https://mlcommons.org/en/croissant/
31. https://www.w3.org/TR/prov-o/
32. https://www.hl7.org/fhir/
33. https://www.hl7.org/fhir/observation.html
34. https://www.hl7.org/fhir/provenance.html
35. http://www.opengeospatial.org/standards/sensorml
36. https://semiceu.github.io/DCAT-AP/