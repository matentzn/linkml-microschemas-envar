# Citations for Research Query

**Query:** This study surveys the complete landscape of **metadata standards and structured-metadata formats** used to describe **environmental-exposure data** — data quantifying human or population exposure to environmental factors (heat, air pollution, wildfire smoke, etc.), optionally linked to health outcomes — for the purposes of reuse, reproducibility, and meta-analysis.

Scope — IN: any standard, specification, schema, or structured format whose purpose is to record metadata ABOUT environmental-exposure datasets or values so they can be found, understood, reproduced, or pooled. Two classes to distinguish: (a) GENERAL STANDARDS intended to be reusable and interoperable across data producers (e.g. DCAT, ISO 19115/19139/19156, schema.org / science-on-schema.org, STAC, RO-Crate, Croissant, DDI, W3C PROV, DataCite, Frictionless Data Package, CDIF, CODATA Essential Variables, OMOP CDM external_exposure / GIS / Exposome extensions, FHIR environmental profiles, ACDD/CF metadata conventions); and (b) PIPELINE SIDECARS — structured but per-pipeline documentative formats never intended as general standards (e.g. DeGAUSS geocoding sidecars, Amadeus/gridMET download sidecars, project-local YAML metadata).

Scope — OUT (note only as context / vocabularies-used, NOT primary entries): pure controlled vocabularies / ontologies / thesauri (ENVO, SWEET, CF standard names, QUDT, AGROVOC, GCMD, SVO, GeoNames, Getty TGN, USGS Thesaurus, EnvThes, WoRMS, etc.) and projects / data-platforms themselves (CDC Environmental Public Health Tracking, exposome cohorts).

Questions the study must answer:
1. What metadata standards and structured formats exist for environmental-exposure data, across earth/climate science, geospatial/OGC, clinical/health, provenance/FAIR packaging, and exposure science?
2. For each: governing body and maturity; the unit it describes (dataset / variable-type / geocoded-row / produced-value / cite); primary purpose (find / define / compute / reproduce-pool / cite); whether it carries derivation/provenance metadata; domain specificity (env-health-specific vs general-purpose); canonical spec URL.
3. Which are general standards vs pipeline sidecars?
4. Which carry enough provenance/derivation detail to support INSTANCE-LEVEL reproducibility of a produced exposure value, and which stop at dataset-level discovery?
5. For EACH candidate in the todo.md list below, is it a metadata standard in scope, peripheral, or out of scope, and why (one line each)?

todo.md candidate list to assess explicitly: CGI Vocabularies Register; Global Change Master Directory (GCMD); GCMD Science Keywords; ODM2; NERC Vocabulary Server (NVS); USGS Thesaurus; ESIP Community Ontology Repository (COR); AGROVOC; BioPortal; SWEET; EcoPortal; Agroportal; Environmental Thesaurus (EnvThes); GBIF Vocabulary Service; Environment Ontology (EnvO); GeoSPARQL; Scientific Variables Ontology (SVO); Climate Forecast Standard Name Table (CF); Darwin Core (DwC); MMI Ontology Registry and Repository; RRUFF; American Geological Institute Glossary of Geology; Research Vocabularies Australia; CSDMS Standard Names; Marine Metadata Interoperability Project; BARTOC; World Meteorological Office (WMO); IODE Ocean Data Portal parameter dictionary; BCO-DMO; Collections Descriptions; MIDS; EFG; QUDT; MINDAT; 4TU.ResearchData; WoRMS; EU Vocabularies; GeoNames; Getty Thesaurus of Geographic Names; ECSO (Ecosystems Ontology); GeoCore Ontology; Astronomical Environment Ontology; Ontobee; OBO Foundry; CAB Thesaurus; ANZSRC 2020; Aquatic Sciences and Fisheries Thesaurus; WorldBank Thesaurus; TERN Controlled Vocabularies; Coastal and Marine Ecological Classification Standard (CMECS); Darwin Core; ODM2.

Evidence: prefer official standard documents / standards-body pages (W3C/OGC/ISO/RDA/CODATA/OHDSI) and peer-reviewed or authoritative grey literature over blogs. Every standard named must carry a canonical URL or DOI. Audience: schema engineers building an environmental-exposure metadata registry who need to know what already exists and how each relates to instance-level exposure provenance. Global scope; emphasise currently-maintained standards but include foundational older ones (ISO 19115, DCAT) still in use.

## Role addendum: skeptic and limitations

Adopt the stance of an informed skeptic. For each major claim, dataset,
tool, or standard discussed: identify the strongest documented
criticism, replication failure, methodological objection, or known
limitation. Where consensus exists, find the dissenting evidence and
attribute it. Where consensus is presumed but not actually established,
say so. Surface conflicts of interest, funding biases, and known
reproducibility issues. Your output should be uncomfortable reading
for advocates of the field — but every objection must carry a citation.

## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
**Provider:** perplexity
**Generated:** 2026-07-04T14:41:06.975411

1. https://www.sciencedirect.com/science/article/pii/S2666389921001707
2. https://www.epa.gov/geospatial/epa-metadata-technical-specification
3. https://www.iso.org/standard/32574.html
4. https://www.w3.org/TR/vocab-dcat-3/
5. https://schema.org/Dataset
6. https://www.esipfed.org/esip-endorses-guidance-for-science-on-schema-org-metadata/
7. https://stacspec.org
8. https://www.researchobject.org/ro-crate/about_ro_crate
9. https://schema.datacite.org/meta/kernel-4.0/doc/DataCite-MetadataKernel_v4.0.pdf
10. https://www.sciencedirect.com/science/article/pii/S0198971517300558
11. https://www.iso.org/standard/53798.html
12. https://doc.esri.com/en/arcgis-pro/latest/help/metadata/create-iso-19115-and-iso-19139-metadata.html
13. https://www.ogc.org/standards/om/
14. https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/climate-forecast-metadata-conventions
15. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
16. https://specs.frictionlessdata.io/data-package/
17. https://github.com/mlcommons/croissant
18. https://ohdsi.github.io/GIS/vocabulary.html
19. https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html
20. https://degauss.org/using_degauss.html
21. https://www.iso.org/standard/53798.html.[11
22. https://www.iso.org/standard/32574.html.[3
23. https://www.ogc.org/standards/om/.[13
24. https://cfconventions.org,
25. https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/climate-forecast-metadata-conventions.[14
26. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3.[15
27. https://stacspec.org.[7
28. https://www.w3.org/TR/vocab-dcat-3/.[4
29. https://schema.org/Dataset.[5
30. https://www.esipfed.org/esip-endorses-guidance-for-science-on-schema.org-metadata.[6
31. https://schema.datacite.org/meta/kernel-4.0/doc/DataCite-MetadataKernel_v4.0.pdf.[9
32. https://specs.frictionlessdata.io/data-package/.[16
33. https://www.researchobject.org/ro-crate/about_ro_crate.[8
34. https://github.com/mlcommons/croissant.[17
35. https://ohdsi.github.io/GIS/vocabulary.html.[18
36. https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html.[19
37. https://www.hl7.org/fhir,
38. https://www.w3.org/TR/prov-overview/,
39. https://www.sciencedirect.com/science/article/pii/S0198971517300558.[10
40. https://degauss.org/using_degauss.html.[20
41. https://www.iso.org/standard/53798.html[11
42. https://www.iso.org/standard/32574.html[3
43. https://www.ogc.org/standards/om/[13
44. https://cfconventions.org;
45. https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/climate-forecast-metadata-conventions[14
46. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3[15
47. https://www.w3.org/TR/vocab-dcat-3/[4
48. https://schema.org/Dataset[5
49. https://www.esipfed.org/esip-endorses-guidance-for-science-on-schema.org-metadata[6
50. https://schema.datacite.org/meta/kernel-4.0/doc/DataCite-MetadataKernel_v4.0.pdf[9
51. https://stacspec.org[7
52. https://specs.frictionlessdata.io/data-package/[16
53. https://www.researchobject.org/ro-crate/about_ro_crate[8
54. https://github.com/mlcommons/croissant[17
55. https://ohdsi.github.io/GIS/vocabulary.html[18
56. https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html[19
57. https://degauss.org/using_degauss.html[20
58. http://external.cgi-iugs.org/cgi-list-vocabularies
59. https://gcmd.nasa.gov
60. https://earthdata.nasa.gov/esds/gcmd-keywords
61. https://github.com/ODM2/ODM2
62. http://vocab.nerc.ac.uk
63. https://www.usgs.gov/products/thesaurus
64. https://cor.esipfed.org
65. http://www.fao.org/agrovoc
66. https://bioportal.bioontology.org
67. https://sweetontology.net
68. http://agroportal.lirmm.fr
69. https://vocabs.acdh.oeaw.ac.at/envthes
70. https://www.gbif.org/vocabularies
71. http://environmentontology.org
72. https://www.ogc.org/standards/geosparql
73. http://www.geoscienceontology.org/svo
74. https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html[14
75. http://rs.tdwg.org/dwc
76. http://marinemetadata.org
77. http://rruff.info
78. https://vocabs.ands.org.au
79. https://bartoc.org
80. https://public.wmo.int
81. https://www.bco-dmo.org
82. http://www.qudt.org
83. https://www.mindat.org
84. https://data.4tu.nl
85. http://www.marinespecies.org
86. https://op.europa.eu/en/web/eu-vocabularies
87. https://www.geonames.org
88. http://www.getty.edu/research/tools/vocabularies/tgn
89. http://www.ontobee.org
90. http://www.obofoundry.org
91. https://www.worldbank.org
92. https://www.cmecs.org