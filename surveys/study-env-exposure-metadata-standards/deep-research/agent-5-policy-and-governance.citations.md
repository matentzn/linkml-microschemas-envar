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

## Role addendum: policy and governance

Approach as a policy analyst. Identify: applicable regulations,
standards bodies, funding agency requirements, data-sharing mandates,
privacy/ethics frameworks, and the institutions that enforce them.
For each, cite the actual regulatory text, standard document, or
agency guidance. Trace the lineage of major requirements (which
directive / law / agency memo introduced them). Where compliance
practice diverges from the letter of the rule, document that gap.
Cover jurisdictional variation (US/EU/UK at minimum) where relevant.

## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
**Provider:** perplexity
**Generated:** 2026-07-04T14:23:53.085107

1. https://www.iso.org/standard/53798.html
2. https://www.iso.org/obp/ui/
3. https://www.ogc.org/standards/om/
4. https://www.w3.org/TR/vocab-dcat-3/
5. https://schema.org/Dataset
6. https://github.com/esipfed/science-on-schema.org
7. https://stacspec.org
8. https://www.researchobject.org/ro-crate/specification
9. https://mlcommons.org/working-groups/data/croissant/
10. http://www.ihsn.org/documentation-standards
11. https://ohdsi.github.io/CommonDataModel/cdm53.html
12. https://github.com/OHDSI/GIS
13. https://build.fhir.org/ig/HL7/fhir-us-phpl/artifacts.html
14. https://cfconventions.org
15. https://degauss.org/using_degauss.html
16. https://dwc.tdwg.org
17. https://github.com/mlcommons/croissant
18. https://ddialliance.org/ddi-codebook_v2.5
19. https://scientificvariablesontology.org/documentation.html
20. https://vocabularyserver.com/asfa/
21. https://www.iso.org/standard/53798.html.[1
22. https://degauss.org/using_degauss.html.[15
23. https://www.w3.org/TR/vocab-dcat-3/.[4
24. https://cfconventions.org.[14
25. https://www.ogc.org/standards/om/.[3
26. https://www.w3.org/TR/prov-o/,
27. https://ohdsi.github.io/CommonDataModel/cdm53.html,
28. https://github.com/OHDSI/GIS,
29. https://build.fhir.org/ig/HL7/fhir-us-phpl/artifacts.html.[13
30. https://www.iso.org/obp/ui/,
31. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0002
32. https://www.ogc.org/standards/om,
33. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery
34. https://dwc.tdwg.org,
35. https://www.w3.org/TR/vocab-dcat-3/,
36. https://github.com/esipfed/science-on-schema.org.[6
37. https://www.researchobject.org/ro-crate/specification,
38. https://mlcommons.org/working-groups/data/croissant/.[9
39. http://www.ihsn.org/documentation-standards,
40. https://ddialliance.org/ddi-codebook_v2.5.[18
41. https://ohdsi.github.io/CommonDataModel/cdm53.html.[11
42. http://www.obofoundry.org/ontology/envo.html
43. https://www.researchobject.org/ro-crate/specification.[8
44. https://frictionlessdata.io/specs/data-package/;
45. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0002;
46. https://www.epa.gov;
47. https://www.ukri.org;
48. https://www.iso.org/standard/53798.html[1
49. https://www.iso.org/obp/ui/[2
50. https://www.ogc.org/standards/om[3
51. https://cfconventions.org[14
52. https://www.w3.org/TR/vocab-dcat-3/[4
53. https://schema.org/Dataset[5
54. https://github.com/esipfed/science-on-schema.org[6
55. https://stacspec.org[7
56. https://www.researchobject.org/ro-crate/specification[8
57. https://mlcommons.org/working-groups/data/croissant/[9
58. https://github.com/mlcommons/croissant[17
59. https://ddialliance.org/ddi-codebook_v2.5[18
60. http://www.ihsn.org/documentation-standards[10
61. https://ohdsi.github.io/CommonDataModel/cdm53.html[11
62. https://github.com/OHDSI/GIS[12
63. https://build.fhir.org/ig/HL7/fhir-us-phpl/artifacts.html[13
64. https://degauss.org/using_degauss.html[15
65. https://cgi.vocabs.org
66. https://gcmd.nasa.gov
67. https://gcmd.nasa.gov/KeywordSearch
68. https://github.com/ODM2/ODM2
69. https://vocabulary.nerc.ac.uk
70. https://www2.usgs.gov/science/about
71. https://cor.esipfed.org
72. http://aims.fao.org/agrovoc
73. https://bioportal.bioontology.org
74. https://sweetontology.net
75. http://agroportal.lirmm.fr
76. https://vocabs.svs.ch/envthes
77. https://rs.gbif.org
78. https://www.ogc.org/standards/geosparql
79. https://scientificvariablesontology.org/documentation.html;
80. http://rruff.info
81. https://vocabs.ands.org.au
82. https://public.wmo.int
83. http://www.qudt.org
84. https://vocabularyserver.com/asfa/,