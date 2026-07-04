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

## Role addendum: comparative landscape

Map the space. Produce a structured comparison of the main contenders
(competing methods, datasets, standards, projects, vendors). For each:
who maintains it, scope, license/access model, adoption indicators
(citations, GitHub stars, listed users, regulatory uptake), and the
distinguishing axis along which it differs from the others. Aim for a
comparative table where one is feasible. Where two entities are often
confused, clarify the actual difference with citations. Avoid ranking;
your job is to map, not judge.

## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
**Provider:** perplexity
**Generated:** 2026-07-04T14:36:00.802458

1. https://pubmed.ncbi.nlm.nih.gov/18849771/
2. https://pmc.ncbi.nlm.nih.gov/articles/PMC8728981/
3. https://www.dcc.ac.uk/resources/metadata-standards/iso-19115
4. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
5. https://stacspec.org
6. https://schema.org/Dataset
7. https://www.earthcube.org/science-on-schema
8. https://www.researchobject.org/ro-crate/
9. https://mlcommons.org/working-groups/data/croissant/
10. https://specs.frictionlessdata.io/data-package/
11. https://www.w3.org/TR/prov-overview/
12. https://www.w3.org/TR/vocab-dcat-3/
13. https://www.ogc.org/standards/om/
14. https://doc.esri.com/en/arcgis-pro/latest/help/metadata/create-iso-19115-and-iso-19139-metadata.html
15. https://www.sciencedirect.com/science/article/pii/S1364815224003025
16. https://ohdsi.github.io/CommonDataModel/cdm53.html
17. https://pmc.ncbi.nlm.nih.gov/articles/PMC4383187/
18. https://gcos.wmo.int/site/global-climate-observing-system-gcos/essential-climate-variables/about-essential-climate-variables
19. https://unstats.un.org/iswghs/documents/ISWGHS-metadata-20221123.pdf
20. https://www.ga4gh.org/product/human-exposome-data-standards/
21. https://pubmed.ncbi.nlm.nih.gov/18849771/[1
22. https://pmc.ncbi.nlm.nih.gov/articles/PMC4383187/[17
23. https://gcos.wmo.int/site/global-climate-observing-system-gcos/essential-climate-variables/about-essential-climate-variables[18
24. https://pmc.ncbi.nlm.nih.gov/articles/PMC8728981/[2
25. https://www.dcc.ac.uk/resources/metadata-standards/iso-19115[3
26. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3[4
27. https://stacspec.org[5
28. https://schema.org/Dataset[6
29. https://www.earthcube.org/science-on-schema[7
30. https://www.researchobject.org/ro-crate/[8
31. https://mlcommons.org/working-groups/data/croissant/[9
32. https://specs.frictionlessdata.io/data-package/[10
33. https://www.w3.org/TR/prov-overview/[11
34. https://www.w3.org/TR/vocab-dcat-3/[12
35. https://www.ogc.org/standards/om/[13
36. https://doc.esri.com/en/arcgis-pro/latest/help/metadata/create-iso-19115-and-iso-19139-metadata.html[14
37. https://www.sciencedirect.com/science/article/pii/S1364815224003025[15
38. https://ohdsi.github.io/CommonDataModel/cdm53.html[16
39. https://unstats.un.org/iswghs/documents/ISWGHS-metadata-20221123.pdf[19
40. https://www.ga4gh.org/product/human-exposome-data-standards/[20
41. https://www.iso.org/standard/53798.html,
42. https://schema.org/Dataset,
43. https://stacspec.org,
44. https://specs.frictionlessdata.io/data-package/,
45. https://schema.datacite.org/[unverified
46. https://schema.datacite.org
47. https://www.sciencedirect.com/science/article/pii/S1364815224003025,
48. http://cfconventions.org,
49. https://ohdsi.github.io/CommonDataModel/cdm53.html,
50. https://hl7.org/fhir/[unverified
51. https://hl7.org/fhir
52. https://www.ga4gh.org/product/human-exposome-data-standards/,
53. https://www.w3.org/TR/prov-overview/,
54. https://www.researchobject.org/ro-crate/,
55. https://mlcommons.org/working-groups/data/croissant/,
56. http://cfconventions.org
57. https://www.ogc.org/standard/sensorthings
58. https://schema.datacite.org/
59. https://ddialliance.org/
60. https://hl7.org/fhir/
61. http://www.cgi-iugs.org/
62. https://gcmd.nasa.gov,
63. https://gcmd.nasa.gov/KeywordSearch/,
64. https://github.com/ODM2/ODM2,
65. https://vocab.nerc.ac.uk,
66. https://www.usgs.gov/thesaurus,
67. https://cor.esipfed.org,
68. https://agrovoc.fao.org,
69. https://bioportal.bioontology.org,
70. https://sweetontology.net,
71. http://agroportal.lirmm.fr,
72. https://vocabs.acdh.oeaw.ac.at/envthes,
73. https://www.gbif.org/vocabularies,
74. http://environmentontology.org,
75. https://www.ogc.org/standards/geosparql,
76. https://www.scienceontology.org,
77. https://cfconventions.org/standard-names.html,
78. https://dwc.tdwg.org,
79. https://mmisw.org,
80. https://rruff.info,
81. https://pubs.geoscienceworld.org,
82. https://vocabs.ardc.edu.au,
83. https://csdms.colorado.edu/wiki/Standard_Names,
84. https://marinemetadata.org,
85. https://bartoc.org,
86. https://public.wmo.int,
87. https://www.iode.org,
88. https://www.bco-dmo.org,
89. http://www.qudt.org,
90. https://www.mindat.org,
91. https://data.4tu.nl,
92. https://www.marinespecies.org,
93. https://op.europa.eu/en/web/eu-vocabularies,
94. https://www.geonames.org,
95. https://www.getty.edu/research/tools/vocabularies/tgn,
96. http://www.ontobee.org,
97. http://www.obofoundry.org,
98. https://www.cabi.org/cabthesaurus,
99. https://www.abs.gov.au/ausstats/anzsrc-2020,
100. https://agris.fao.org,
101. https://vocabulary.worldbank.org,
102. https://vocabs.tern.org.au,
103. https://www.fgdc.gov/standards/projects/CMECS,
104. CF conventions and ACDD
105. GA4GH