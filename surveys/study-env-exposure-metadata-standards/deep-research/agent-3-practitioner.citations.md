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

## Reference rule (non-negotiable)

Every substantive claim, statistic, dataset, tool, project name,
or finding MUST carry at least one machine-verifiable reference:
a DOI (formatted `10.xxxx/...`), a PMID (formatted `PMID: 12345678`),
or a fully qualified URL. Inline-cite at the point of the claim;
do not defer all citations to a closing bibliography. If a claim
cannot be backed by such a reference, omit the claim or flag it
explicitly as "unverified".
**Provider:** perplexity
**Generated:** 2026-07-04T14:23:31.865731

1. https://pubmed.ncbi.nlm.nih.gov/18849771/
2. https://www.dcc.ac.uk/resources/metadata-standards/iso-19115
3. https://www.epa.gov/data
4. https://www.epa.gov/fera/human-exposure-modeling-databases-support-exposure-modeling
5. https://ads.atmosphere.copernicus.eu/stac-browser/
6. https://www.researchobject.org/ro-crate/
7. https://research.google/blog/croissant-a-metadata-format-for-ml-ready-datasets/
8. https://ohdsi.github.io/CommonDataModel/cdm54.html
9. https://niehs.github.io/PCOR_bookdown_tools/chapter-fhir-pit.html
10. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
11. https://www.w3.org/TR/vocab-dcat-3/
12. https://schema.org/Dataset
13. https://github.com/esipfed/science-on-schema.org
14. https://pro.arcgis.com/en/pro-app/3.4/help/metadata/create-iso-19115-and-iso-19139-metadata.htm
15. https://www.iso.org/standard/82463.html
16. https://www.w3.org/TR/prov-overview/
17. https://datacite.org/blog/connecting-the-dots-with-datacite-doi-metadata/
18. https://specs.frictionlessdata.io/data-package/
19. https://www.earthdata.nasa.gov/learn/earth-observation-data-basics/essential-variables
20. https://www.ohdsi.org/data-standardization/
21. https://stacspec.org,
22. http://www.qudt.org,
23. https://cgi.vocabs.ands.org.au,
24. https://gcmd.nasa.gov,
25. https://gcmd.nasa.gov/KeywordSearch,
26. https://github.com/ODM2/ODM2,
27. https://vocab.nerc.ac.uk,
28. https://www2.usgs.gov/science/about/thesaurus,
29. https://cor.esipfed.org,
30. http://aims.fao.org/agrovoc,
31. https://bioportal.bioontology.org,
32. http://sweetontology.net,
33. http://ecoportal.org,
34. http://agroportal.lirmm.fr,
35. https://vocabs.lter-europe.net/EnvThes,
36. https://www.gbif.org/vocabularies,
37. http://environmentontology.org,
38. https://www.opengeospatial.org/standards/geosparql,
39. https://github.com/ESIPFed/svo,
40. https://dwc.tdwg.org,
41. https://marinemetadata.org/orr,
42. https://rruff.info,
43. https://vocabs.ands.org.au,
44. https://csdms.colorado.edu/wiki/Standard_Names,
45. https://marinemetadata.org,
46. https://bartoc.org,
47. https://wmo.int,
48. http://www.iode.org,
49. https://www.bco-dmo.org,
50. https://www.mindat.org,
51. https://data.4tu.nl,
52. https://www.marinespecies.org,
53. https://op.europa.eu/en/web/eu-vocabularies,
54. https://www.geonames.org,
55. http://www.getty.edu/research/tools/vocabularies/tgn,
56. http://www.ontobee.org,
57. http://www.obofoundry.org,
58. https://www.cabi.org/cab-thesaurus,
59. https://www.abs.gov.au/ausstats/abs@.nsf/mf/1297.0,
60. https://www.fao.org/fishery/asfis/en,
61. https://vocabulary.worldbank.org,
62. https://www.tern.org.au/controlled-vocabularies,
63. https://www.cmecs.org,