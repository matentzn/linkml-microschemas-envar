# Metadata standards for environmental-exposure data: study report

**SYNTHESIS STATUS: ALL PERPLEXITY AGENTS FAILED (quota exhausted, HTTP 401).**
All 6 sonar-deep-research calls returned `insufficient_quota` on both the initial run and the mandatory retry. No agent-produced text exists; this report is a knowledge-based synthesis by the study runner (Claude, training cutoff August 2025). Claims are sourced from training knowledge and carry canonical URLs where known; none has been verified by the `verify_refs.py` checker against live servers. Treat all references as [UNVERIFIED] until re-run with a funded API key.

To regenerate with real Perplexity deep research: top up the account at https://www.perplexity.ai/settings/api then run:
  PERPLEXITY_API_KEY=<key> bash ~/.claude/skills/study/scripts/run_agents.sh surveys/study-env-exposure-metadata-standards/deep-research

---

## 1. Executive summary

No single metadata standard dominates the environmental-exposure domain end-to-end. The landscape splits along two axes: (a) level of description (dataset vs. variable-type vs. observation-instance) and (b) domain origin (geospatial/earth-science, clinical/health, FAIR-packaging, or exposure-science-specific). The most widely deployed general standards are ISO 19115 for geospatial dataset discovery, the CF Conventions for variable-type and coordinate metadata in NetCDF files, DCAT for catalog interoperability, and W3C PROV-O for provenance chains. None alone carries enough provenance depth to reproduce a single exposure value at instance level. The closest to instance-level provenance are W3C SOSA/SSN (for sensor observations), ODM2 (for environmental observation databases), and W3C PROV-O in combination with RO-Crate. On the clinical side, the OMOP CDM Exposome Extension provides the most structured schema for linking gridded exposures to individuals, but provenance detail is schema-defined rather than enforced. Pipeline sidecars (DeGAUSS, gridMET, project-local YAML) fill the practical gap but are per-project and non-interoperable. The critical gap: no maintained, widely adopted standard simultaneously covers spatial derivation method, temporal aggregation, uncertainty quantification, health-linkage method, and per-value provenance for environmental-exposure data.

---

## 2. Standards inventory

### 2a. General standards IN scope

#### Geospatial / earth-science tier

**ISO 19115 / ISO 19115-1:2014 / ISO 19115-2 / ISO 19115-3:2016**
- Governing body: ISO TC 211
- Maturity: International Standard; Part 1 (2014) current; Part 2 covers imagery/gridded data
- Unit described: geographic dataset
- Primary purpose: discovery, documentation
- Provenance metadata: LI_Lineage element with process step list — rudimentary free-text; not a formal provenance model
- Domain: general-purpose geospatial
- Instance-level reproducibility: NO (dataset level only)
- Canonical URL: https://www.iso.org/standard/53798.html
- Notes: Mandatory basis for EU INSPIRE (Directive 2007/2/EC). ISO 19139 is the XML encoding. ISO 19115-2 covers gridded/imagery data directly relevant to gridded exposure products (gridMET, PRISM, Daymet, ERA5).

**ISO 19156 / OGC Observations and Measurements (O&M)**
- Governing body: OGC / ISO TC 211
- Maturity: ISO 19156:2011; O&M 3.0 in progress; OGC API-EDR (2022) is the REST binding
- Unit described: individual observation, feature of interest, observable property
- Primary purpose: define + compute + reproduce
- Provenance metadata: procedure (sensor/model), result quality, phenomenon time, result time — structural basis for instance-level provenance; depth varies by implementation
- Domain: general-purpose earth observations
- Instance-level reproducibility: PARTIAL
- Canonical URL: https://www.ogc.org/standard/om/ ; https://ogcapi.ogc.org/edr/

**OGC SOSA / SSN (Semantic Sensor Network Ontology)**
- Governing body: W3C / OGC
- Maturity: W3C Recommendation 2017; revision in progress 2024
- Unit described: observation, sensor, platform, sampling feature
- Primary purpose: define + reproduce + provenance
- Provenance metadata: sosa:usedProcedure, sosa:observedProperty, sosa:featureOfInterest — closest general standard to instance-level provenance for in-situ data; extension needed for modeled/gridded exposures
- Domain: general-purpose (sensors, IoT, earth observation)
- Instance-level reproducibility: YES for in-situ; PARTIAL for modeled exposures
- Canonical URL: https://www.w3.org/TR/vocab-ssn/

**CF Conventions (Climate and Forecast Metadata Conventions)**
- Governing body: UCAR / Unidata community; CF Metadata Conventions committee
- Maturity: de facto community standard; CF 1.11 (2023) current
- Unit described: variable type within a NetCDF file; coordinate metadata
- Primary purpose: define + compute (interoperability of earth science NetCDF files)
- Provenance metadata: history global attribute (free-text processing steps); cell_methods captures temporal/spatial aggregation; no formal provenance model
- Domain: earth science (atmospheric, oceanographic, climate)
- Instance-level reproducibility: NO (free-text history only)
- Canonical URL: https://cfconventions.org/
- Notes: Gridded exposure products (gridMET, Daymet, ERA5, PRISM) use CF. The CF standard names table is a vocabulary (OUT of scope); the conventions document IS a metadata standard.

**ACDD (Attribute Convention for Dataset Discovery) 1.3**
- Governing body: ESIP / UCAR; ESIP ACDD working group
- Maturity: community standard; ACDD 1.3 current
- Unit described: NetCDF file / dataset
- Primary purpose: discovery
- Provenance metadata: minimal (source, history attributes); supplements CF
- Domain: earth science
- Instance-level reproducibility: NO
- Canonical URL: https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3

**STAC (SpatioTemporal Asset Catalog)**
- Governing body: Community spec; stacspec.org working group
- Maturity: STAC 1.0.0 (2021); widely deployed
- Unit described: spatiotemporal asset (file/scene), collection, catalog
- Primary purpose: discovery, access
- Provenance metadata: processing extension can carry lineage; core spec does not require it; extension adoption inconsistent
- Domain: geospatial (originally remote sensing; expanding)
- Instance-level reproducibility: NO (core); PARTIAL with processing extension
- Canonical URL: https://stacspec.org/

**OGC API Records**
- Governing body: OGC
- Maturity: candidate standard 2023
- Unit described: metadata record (dataset)
- Primary purpose: discovery
- Provenance metadata: none
- Domain: geospatial catalogs
- Instance-level reproducibility: NO
- Canonical URL: https://ogcapi.ogc.org/records/

**WMO WIGOS Metadata Standard (WMO-No. 1160)**
- Governing body: World Meteorological Organization
- Maturity: WMO-No. 1160 (2021)
- Unit described: observing station / observing system
- Primary purpose: define (station identity, instrument specifications)
- Provenance metadata: instrument calibration records, station change history; relevant for in-situ observations underpinning exposure datasets
- Domain: meteorological and climatological observations
- Instance-level reproducibility: PARTIAL (for in-situ station data)
- Canonical URL: https://library.wmo.int/records/item/55063-guide-to-the-wmo-integrated-global-observing-system

**NASA/GCMD DIF (Directory Interchange Format)**
- Governing body: NASA EOSDIS / Global Change Master Directory
- Maturity: DIF 10.x; actively maintained
- Unit described: earth science dataset
- Primary purpose: discovery
- Provenance metadata: minimal (lineage free text, citation)
- Domain: earth science (NASA-centric but widely used)
- Instance-level reproducibility: NO
- Canonical URL: https://gcmd.nasa.gov/DocumentBuilder/defaultDif10/guide/

#### FAIR packaging / provenance tier

**W3C PROV-O (Provenance Ontology)**
- Governing body: W3C
- Maturity: W3C Recommendation 2013
- Unit described: entity, activity, agent — provenance graph elements
- Primary purpose: reproduce + cite
- Provenance metadata: models derivation, attribution, revision; foundational standard for provenance chains; can express instance-level reproducibility when implemented
- Domain: general-purpose
- Instance-level reproducibility: YES (by design)
- Canonical URL: https://www.w3.org/TR/prov-o/
- Notes: PROV-N is the human-readable notation; PROV-DM is the abstract data model. Requires application profiles to constrain for a specific domain.

**RO-Crate (Research Object Crate)**
- Governing body: RDA Research Object Alliance; community spec
- Maturity: RO-Crate 1.2 (2024) current; WorkflowRun RO-Crate profile active
- Unit described: research output package (data + metadata + provenance)
- Primary purpose: reproduce + cite + pool
- Provenance metadata: schema.org + PROV-O; WorkflowRun profile captures computational workflow provenance including tool versions, parameters, inputs/outputs
- Domain: general research/FAIR
- Instance-level reproducibility: YES when WorkflowRun profile is used
- Canonical URL: https://www.researchobject.org/ro-crate/

**DataCite Metadata Schema**
- Governing body: DataCite consortium
- Maturity: DataCite Metadata Schema 4.5 (2023) current
- Unit described: citable resource (dataset, software)
- Primary purpose: cite + discover
- Provenance metadata: relatedIdentifier for lineage; fundingReference; no formal provenance model
- Domain: general research data citation
- Instance-level reproducibility: NO
- Canonical URL: https://schema.datacite.org/

**W3C DCAT (Data Catalog Vocabulary)**
- Governing body: W3C
- Maturity: DCAT 3 (2024) current; DCAT 2 (2020) widely deployed
- Unit described: dataset, distribution, data service, catalog
- Primary purpose: discovery + catalog interoperability
- Provenance metadata: PROV-O integration possible; dcat:qualifiedRelation for lineage; not required
- Domain: general open data
- Instance-level reproducibility: NO
- Canonical URL: https://www.w3.org/TR/vocab-dcat/
- Notes: DCAT-AP (EU) and GeoDCAT-AP (geospatial EU profile) are key profiles. Mandated for EU open data portals under Open Data Directive 2019/1024.

**Frictionless Data Package / Data Resource Specification**
- Governing body: Open Knowledge Foundation / Frictionless Data Initiative
- Maturity: Frictionless Standards 2.0 (2023)
- Unit described: tabular data file, dataset
- Primary purpose: define + reproduce (machine-readable schema)
- Provenance metadata: minimal; no formal provenance model
- Domain: general open data (strong for tabular/CSV data)
- Instance-level reproducibility: NO
- Canonical URL: https://specs.frictionlessdata.io/

**schema.org / science-on-schema.org**
- Governing body: schema.org (W3C community group); science-on-schema.org (ESIP/RDA)
- Maturity: schema.org evergreen; science-on-schema.org v1.3 (2022)
- Unit described: dataset, variable measured
- Primary purpose: discovery (Google Dataset Search)
- Provenance metadata: variableMeasured, measurementTechnique, isBasedOn; shallow provenance
- Domain: general research discovery
- Instance-level reproducibility: NO
- Canonical URL: https://science-on-schema.org/

**DDI (Data Documentation Initiative)**
- Governing body: DDI Alliance
- Maturity: DDI-Codebook 2.5; DDI-Lifecycle 3.3; DDI-CDI emerging
- Unit described: study, dataset, variable, question, code list
- Primary purpose: define + reproduce + find
- Provenance metadata: study-level data collection documentation; weak on computational derivation
- Domain: social science / survey data; expanding cross-domain
- Instance-level reproducibility: PARTIAL
- Canonical URL: https://ddialliance.org/

**Croissant (ML Dataset Format)**
- Governing body: MLCommons / Google / Hugging Face
- Maturity: v1.0 (2024)
- Unit described: ML dataset, field, record set
- Primary purpose: define + reproduce (ML training data)
- Provenance metadata: data sources, transformations; not formal PROV
- Domain: machine learning
- Instance-level reproducibility: PARTIAL
- Canonical URL: https://mlcommons.org/working-groups/data/croissant/

**CDIF (Cross-Domain Interoperability Framework)**
- Governing body: RDA / CODATA
- Maturity: draft/emerging (2022-2024); not yet an implemented standard
- Unit described: digital object
- Primary purpose: cross-domain interoperability
- Domain: general cross-domain
- Instance-level reproducibility: NO
- Canonical URL: https://www.rd-alliance.org/groups/cross-domain-interoperability-framework-cdif.html

#### Clinical / health tier

**OMOP CDM (Common Data Model) including Exposome Extension**
- Governing body: OHDSI consortium
- Maturity: OMOP CDM v5.4 (current); Exposome Extension actively developed (2023-)
- Unit described: patient-level observation row (EXPOSURE_OCCURRENCE, GIS extension tables)
- Primary purpose: reproduce + pool (observational health research)
- Provenance metadata: exposure_source_value, linkage method in Exposome Extension; schema supports provenance but completeness is implementation-defined, not enforced
- Domain: clinical / health outcomes research
- Instance-level reproducibility: PARTIAL (schema supports it; compliance not mandated)
- Canonical URL: https://ohdsi.github.io/CommonDataModel/

**HL7 FHIR — Environmental / Exposome Profiles**
- Governing body: HL7 International
- Maturity: FHIR R5 (2023); environmental exposome Implementation Guides at draft/ballot maturity (2024)
- Unit described: Observation resource (individual measurement/exposure)
- Primary purpose: clinical interoperability
- Provenance metadata: FHIR Provenance resource; Observation.derivedFrom; implementation-dependent
- Domain: clinical health data exchange
- Instance-level reproducibility: PARTIAL
- Canonical URL: https://www.hl7.org/fhir/

#### Observation database / exposure-science tier

**ODM2 (Observations Data Model 2)**
- Governing body: CUAHSI / community (Horsburgh et al.)
- Maturity: published 2016 (DOI: 10.1016/j.envsoft.2016.01.010); actively maintained; serialized via WaterML 2.0 (OGC)
- Unit described: individual observation (result), method, variable, site, instrument
- Primary purpose: define + compute + reproduce
- Provenance metadata: method record, equipment record, calibration record, data quality code, annotation — the most structured schema for instance-level reproducibility among environmental observation standards
- Domain: environmental/hydrological/earth science observations
- Instance-level reproducibility: YES (designed for this)
- Canonical URL: http://www.odm2.org/
- Notes: Database schema, not a file format standard; designed for in-situ data; extension required for gridded/modeled exposures.

**WaterML 2.0**
- Governing body: OGC
- Maturity: OGC Standard 12-031r2 (2012)
- Unit described: hydrological/environmental time series observation
- Primary purpose: define + reproduce
- Provenance metadata: procedure, quality; links to ODM2 concepts
- Domain: water / environmental data
- Instance-level reproducibility: PARTIAL
- Canonical URL: https://www.ogc.org/standard/waterml/

**CODATA Essential Variables / GEO Essential Variables**
- Governing body: CODATA; Group on Earth Observations (GEO)
- Maturity: concept framework; individual EV sets vary
- Unit described: variable type (what to measure, at what aggregation level)
- Primary purpose: define (harmonize what gets measured globally)
- Provenance metadata: none (EVs define what, not how)
- Domain: cross-domain earth/climate/biodiversity
- Instance-level reproducibility: NO
- Canonical URL: https://codata.org/ ; https://www.earthobservations.org/

---

### 2b. Pipeline sidecars IN scope

**DeGAUSS geocoding sidecar**
- Developer: Cincinnati Children's Hospital GRAPPH lab (Brokamp et al.)
- Format: project-local YAML + CSV per DeGAUSS container invocation
- Unit described: geocoded patient address rows + Docker container invocation metadata
- Provenance metadata: Docker image hash, version, date — sufficient for exact reproduction if image is preserved
- Not a general standard; de-facto pattern for pediatric environmental health geocoding pipelines
- Canonical URL: https://degauss.org/

**gridMET / Daymet / PRISM download sidecars**
- Format: project-local scripts + README + parameter files; varies by pipeline
- Unit described: dataset version, geographic extent, date range, variable queried
- Provenance metadata: partial — records download query but not model internals
- Not a standard

---

## 3. Key tensions

**Tension 1: dataset-level vs. instance-level scope.**
ISO 19115, DCAT, and schema.org address dataset-level metadata (one record per dataset). For environmental epidemiology pooling and meta-analysis, what is needed is metadata at the individual exposure estimate level: what model, what resolution, what linkage radius produced THIS person's exposure on THIS date. No general standard fully covers this without extension. ODM2 and SOSA/SSN come closest.

**Tension 2: CF Conventions — format or standard.**
The CF standard names table is a vocabulary (OUT of scope as a primary entry); the CF conventions document specifying coordinate metadata, cell_methods, and history attributes IS a metadata standard. The field routinely conflates the two; this survey treats the conventions document as IN.

**Tension 3: OMOP CDM placement.**
OMOP CDM is primarily a data model for patient-level data, not a metadata standard about a dataset. However, the Exposome Extension tables function as a structured sidecar schema documenting exposure linkage metadata within a CDM record. Placement is genuinely ambiguous; this survey treats it as IN with a domain-specific note.

**Tension 4: ODM2 scope limitation.**
ODM2 is the most powerful standard for in-situ observational data provenance but was not designed for gridded/modeled exposure data. Extending ODM2 to cover modeled exposures requires significant profiling.

---

## 4. Open gaps

1. **No instance-level provenance standard for modeled gridded exposures.** PROV-O can model it in principle but there is no community profile or agreed serialization for "this gridded PM2.5 value at census tract X on date Y was derived from model Z at resolution R using linkage method L."

2. **Health-linkage metadata absent from all geospatial standards.** ISO 19115, STAC, CF, DCAT carry no fields documenting the spatial linkage method (area-weighted areal interpolation, centroid snap, buffer overlap) used to assign a gridded value to a health record.

3. **Uncertainty quantification metadata lacking.** No mainstream standard has a standardized schema for per-value uncertainty intervals on derived exposure estimates. W3C SOSA has sosa:resultQuality but without a controlled type system for exposure uncertainty.

4. **FHIR environmental profiles immature.** HL7 FHIR exposure/exposome IGs are active work-in-progress (as of 2024); not yet stable enough to build registries against.

5. **STAC processing extension under-specified.** The STAC processing extension exists but is not part of the core specification, and adoption is inconsistent.

6. **No common profile linking OMOP CDM exposure tables to PROV-O or RO-Crate.** Each OHDSI network site handles exposure provenance differently; no community consensus profile exists.

7. **No standard bridges the earth-science to clinical gap.** A researcher can use ISO 19115 or CF on the geospatial side and OMOP CDM on the clinical side, but no standard traces a computed exposure estimate from its gridded source through the linkage step to the patient row.

---

## 5. todo.md candidate verdicts

Every candidate from the core brief is assessed. IN = metadata standard in scope; PERIPHERAL = partly relevant; OUT = pure vocabulary/ontology/repository/platform.

| Candidate | Verdict | Rationale |
|---|---|---|
| CGI Vocabularies Register | OUT | Controlled vocabulary register for geoscience terms; not a metadata format |
| Global Change Master Directory (GCMD) | PERIPHERAL | NASA earth science dataset catalog (platform); the DIF schema produced by GCMD IS a metadata standard (IN, listed above as NASA/GCMD DIF) |
| GCMD Science Keywords | OUT | Pure controlled vocabulary for tagging datasets |
| ODM2 | IN | Database schema with rich instance-level observation provenance; DOI: 10.1016/j.envsoft.2016.01.010 |
| NERC Vocabulary Server (NVS) | OUT | Vocabulary management service (BODC/NERC); not a metadata standard |
| USGS Thesaurus | OUT | Pure thesaurus |
| ESIP Community Ontology Repository (COR) | OUT | Vocabulary registry; not a metadata standard |
| AGROVOC | OUT | SKOS thesaurus for agriculture; pure vocabulary |
| BioPortal | OUT | Biomedical ontology repository; not a metadata standard |
| SWEET | OUT | OWL ontology; not a metadata standard |
| EcoPortal | OUT | Ecology ontology portal; not a metadata standard |
| Agroportal | OUT | Agronomic ontology portal; not a metadata standard |
| Environmental Thesaurus (EnvThes) | OUT | SKOS thesaurus; pure vocabulary |
| GBIF Vocabulary Service | OUT | Biodiversity vocabulary service; not a metadata standard |
| Environment Ontology (EnvO) | OUT | OBO ontology for environmental features; pure vocabulary |
| GeoSPARQL | PERIPHERAL | OGC standard for geospatial RDF features; primarily a query language and feature representation model, not a metadata format; used alongside metadata standards |
| Scientific Variables Ontology (SVO) | OUT | Ontology for variable decomposition; pure vocabulary |
| Climate Forecast Standard Name Table (CF) | PERIPHERAL | The name table itself is a vocabulary (OUT); the CF Conventions document as a whole IS a metadata standard (IN, listed above) |
| Darwin Core (DwC) | OUT | Biodiversity observations standard; not designed for environmental-exposure metadata |
| MMI Ontology Registry and Repository | OUT | Marine metadata vocabulary registry; not a metadata standard |
| RRUFF | OUT | Mineral Raman spectra database; out of domain |
| American Geological Institute Glossary of Geology | OUT | Pure glossary |
| Research Vocabularies Australia | OUT | National vocabulary service; not a metadata standard |
| CSDMS Standard Names | OUT | Variable naming convention for earth surface models; vocabulary-level, not a metadata format |
| Marine Metadata Interoperability Project | OUT | Community project; not itself a standard |
| BARTOC | OUT | Registry of thesauri and ontologies; not a metadata standard |
| World Meteorological Organization (WMO) | PERIPHERAL | WMO produces metadata standards; the WIGOS Metadata Standard (WMO-No. 1160) IS in scope and listed above as IN; WMO as an organization is not itself a standard |
| IODE Ocean Data Portal parameter dictionary | OUT | Vocabulary/parameter list for oceanographic data; not a metadata standard |
| BCO-DMO | OUT | Biological and Chemical Oceanography Data Management Office repository; platform, not a standard |
| Collections Descriptions | OUT | TDWG collections descriptions; biodiversity collections metadata; out of scope |
| MIDS | OUT | Minimum Information about a Digital Specimen (TDWG); natural history specimen metadata; out of scope |
| EFG (Extension for Geosciences) | OUT | Biodiversity natural history collection extension; out of domain |
| QUDT | OUT | Quantities, Units, Dimensions and Types ontology; pure vocabulary |
| MINDAT | OUT | Mineralogy database; out of domain |
| 4TU.ResearchData | OUT | Dutch research data repository; platform, not a standard |
| WoRMS | OUT | World Register of Marine Species; taxonomy database, not a metadata standard |
| EU Vocabularies | OUT | Controlled vocabularies for EU institutions; not environmental-exposure metadata standards |
| GeoNames | OUT | Geographic names gazetteer; pure reference vocabulary |
| Getty Thesaurus of Geographic Names | OUT | Pure vocabulary |
| ECSO (Ecosystems Ontology) | OUT | OWL ontology for ecosystem descriptions; pure vocabulary |
| GeoCore Ontology | OUT | Core vocabulary for geospatial data; vocabulary, not an adopted metadata format standard |
| Astronomical Environment Ontology | OUT | Out of domain for terrestrial environmental-exposure data |
| Ontobee | OUT | Ontology browser/repository; not a metadata standard |
| OBO Foundry | OUT | Ontology community framework/repository; not a metadata standard |
| CAB Thesaurus | OUT | CABI agriculture/environment thesaurus; pure vocabulary |
| ANZSRC 2020 | OUT | Australian and New Zealand Standard Research Classification; classification scheme, not environmental-exposure metadata |
| Aquatic Sciences and Fisheries Thesaurus | OUT | Pure vocabulary |
| WorldBank Thesaurus | OUT | Pure vocabulary |
| TERN Controlled Vocabularies | PERIPHERAL | TERN (Australia) controlled vocabularies; the TERN data model (SOSA/SSN-based profile) is peripheral; the standalone controlled vocabularies are OUT |
| Coastal and Marine Ecological Classification Standard (CMECS) | OUT | Habitat classification scheme; not a metadata format for environmental-exposure data |
| Darwin Core (duplicate) | OUT | Same as above |
| ODM2 (duplicate) | IN | Same as above |

---

## 6. References [UNVERIFIED]

All references are from training knowledge. Perplexity calls failed; none has been verified against live servers.

- ISO 19115-1:2014. https://www.iso.org/standard/53798.html [UNVERIFIED]
- ISO 19156:2011. https://www.ogc.org/standard/om/ [UNVERIFIED]
- OGC API-EDR. https://ogcapi.ogc.org/edr/ [UNVERIFIED]
- W3C SOSA/SSN Recommendation. https://www.w3.org/TR/vocab-ssn/ [UNVERIFIED]
- CF Conventions v1.11. https://cfconventions.org/ [UNVERIFIED]
- ESIP ACDD 1.3. https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3 [UNVERIFIED]
- STAC Specification 1.0.0. https://stacspec.org/ [UNVERIFIED]
- OGC API Records. https://ogcapi.ogc.org/records/ [UNVERIFIED]
- WMO WIGOS Metadata Standard (WMO-No. 1160). https://library.wmo.int/records/item/55063-guide-to-the-wmo-integrated-global-observing-system [UNVERIFIED]
- NASA/GCMD DIF 10. https://gcmd.nasa.gov/DocumentBuilder/defaultDif10/guide/ [UNVERIFIED]
- W3C PROV-O. https://www.w3.org/TR/prov-o/ [UNVERIFIED]
- RO-Crate 1.2. https://www.researchobject.org/ro-crate/ [UNVERIFIED]
- DataCite Metadata Schema 4.5. https://schema.datacite.org/ [UNVERIFIED]
- W3C DCAT 3. https://www.w3.org/TR/vocab-dcat/ [UNVERIFIED]
- Frictionless Standards 2.0. https://specs.frictionlessdata.io/ [UNVERIFIED]
- science-on-schema.org v1.3. https://science-on-schema.org/ [UNVERIFIED]
- DDI Alliance. https://ddialliance.org/ [UNVERIFIED]
- Croissant v1.0. https://mlcommons.org/working-groups/data/croissant/ [UNVERIFIED]
- CDIF. https://www.rd-alliance.org/groups/cross-domain-interoperability-framework-cdif.html [UNVERIFIED]
- OMOP CDM v5.4. https://ohdsi.github.io/CommonDataModel/ [UNVERIFIED]
- HL7 FHIR R5. https://www.hl7.org/fhir/ [UNVERIFIED]
- Horsburgh et al. 2016. ODM2. Environmental Modelling and Software. DOI: 10.1016/j.envsoft.2016.01.010 [UNVERIFIED]
- WaterML 2.0. OGC Standard 12-031r2. https://www.ogc.org/standard/waterml/ [UNVERIFIED]
- DeGAUSS. https://degauss.org/ [UNVERIFIED]
- CODATA Essential Variables. https://codata.org/ [UNVERIFIED]
- GEO Essential Variables. https://www.earthobservations.org/ [UNVERIFIED]
- EU Open Data Directive 2019/1024. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019L1024 [UNVERIFIED]
- EU INSPIRE Directive 2007/2/EC. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32007L0002 [UNVERIFIED]

---

## 7. Appendix: planned per-agent contributions (all failed — API quota exhausted)

**Agent 1 — comparative-landscape:** Structured comparison table of all standards with adoption indicators (citation counts, GitHub stars, regulatory uptake), maintenance status, distinguishing axes, and cross-referencing confusions (e.g., CF conventions vs. CF standard names; GCMD vs. DIF).

**Agent 2 — literature-reviewer:** Synthesis of peer-reviewed literature on metadata standardization in environmental epidemiology and exposure science, including systematic reviews of data harmonization challenges in multi-cohort environmental health studies.

**Agent 3 — practitioner:** Implementation friction, documentation quality, and real-world deployment experience for each standard, drawn from practitioner case studies, GitHub issue trackers, and listserv discussions (ESIP, RDA, OHDSI forums).

**Agent 4 — gaps-and-frontiers:** Identification of proposed-but-not-yet-adopted standards, recent preprints signaling emerging approaches, and specific researcher-stated unmet metadata needs in exposure science.

**Agent 5 — policy-and-governance:** Regulatory mandates (INSPIRE Directive, NIH DMS Policy 2023, EU Open Data Directive 2019/1024, UK FAIR Data requirements, EPA data-sharing rules) driving standard adoption, jurisdictional variation, and compliance gaps.

**Agent 6 — skeptic-and-limitations:** Critical assessment of over-stated adoption claims, known implementation failures, and standards that exist on paper but are rarely correctly implemented (e.g., ISO 19115 lineage fields routinely left empty; CF history attributes in free text rather than structured form).
