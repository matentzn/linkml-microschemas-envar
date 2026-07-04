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

## Role addendum: gaps and frontiers

Focus on what is missing or just-emerging. Identify: questions the
literature explicitly flags as unanswered; datasets or measurements
that researchers say they need but don't have; proposed standards or
tools still at the draft / prototype / RFC stage; recent (last 24
months) preprints that may presage a shift. Distinguish between
"genuinely open question" and "answered but not yet disseminated".
For each gap, cite the source(s) flagging it as a gap.

## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
**Provider:** perplexity
**Generated:** 2026-07-04T14:41:26.281586

1. https://www.sciencedirect.com/science/article/pii/S2666389921001707
2. https://www.go-fair.org/fair-principles/
3. https://ohdsi.github.io/CommonDataModel/cdm53.html
4. https://github.com/OHDSI/GIS
5. https://pmc.ncbi.nlm.nih.gov/articles/PMC4383187/
6. https://www.iso.org/standard/32574.html
7. https://stacspec.org
8. https://www.iso.org/standard/53798.html
9. https://www.iso.org/obp/ui/
10. https://www.w3.org/TR/prov-overview/
11. https://dwc.tdwg.org
12. https://www.sciencedirect.com/science/article/pii/S1364815216300093
13. https://www.tdwg.org/community/cd/mids/
14. https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0309210
15. https://github.com/stac-extensions/processing
16. https://ohdsi.github.io/CommonDataModel/cdm54.html
17. https://ohdsi.github.io/GIS/vocabulary.html
18. https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health
19. https://build.fhir.org/ig/HL7/personal-health-record-format-ig/StructureDefinition-Environmental-definitions.html
20. https://pubmed.ncbi.nlm.nih.gov/29126118/
21. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210
22. https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor
23. https://www.w3.org/TR/prov-overview/,
24. https://ohdsi.github.io/CommonDataModel/cdm54.html,
25. https://www.iso.org/standard/32574.html,
26. https://www.iso.org/standard/53798.html,
27. https://www.ogc.org/standard/geosparql/
28. https://cfconventions.org
29. https://wiki.esipfed.org/Attribute_Conventions_for_Data_Discovery
30. https://www.w3.org/TR/vocab-dcat-3/
31. https://schema.datacite.org/meta/kernel-4.5/
32. https://specs.frictionlessdata.io/data-package/
33. https://mlcommons.org/croissant
34. https://ddialliance.org/Specification/DDI-Lifecycle/3.3
35. https://www.researchobject.org/ro-crate/
36. https://schema.org
37. https://github.com/ESIPFed/science-on-schema.org
38. https://ohdsi.github.io/CommonDataModel/cdm53.html,
39. https://ohdsi.github.io/GIS/vocabulary.html,
40. https://www.hl7.org/fhir/
41. https://cgi.vocabs.ga.gov.au
42. https://gcmd.nasa.gov
43. https://www.bodc.ac.uk/data/codes_and_formats/vocabulary_search/
44. https://www2.usgs.gov/science/about/thesaurus.php
45. https://cor.esipfed.org
46. https://www.fao.org/agrovoc
47. https://bioportal.bioontology.org
48. https://sweetontology.net
49. https://ecoportal.lifewatch.eu,
50. https://agroportal.lirmm.fr
51. https://vocabs.lter-europe.net/EnvThes
52. https://rs.gbif.org/vocabulary/
53. https://environmentontology.org
54. https://www.scivocab.org/svo
55. https://marinemetadata.org
56. https://rruff.info
57. https://vocabs.ardc.edu.au
58. https://bartoc.org
59. https://www.iode.org
60. https://www.bco-dmo.org
61. http://www.qudt.org
62. https://www.mindat.org
63. https://researchdata.4tu.nl
64. https://www.marinespecies.org
65. https://www.geonames.org
66. https://www.getty.edu/research/tools/vocabularies/tgn
67. http://www.ontobee.org
68. http://www.obofoundry.org
69. https://www.fgdc.gov/standards/projects/FGDC-standards-projects/cmecs-folder/cmechs