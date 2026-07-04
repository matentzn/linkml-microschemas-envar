# Standards index

A survey of approaches that record *metadata about environmental-exposure data* for reuse, reproducibility, and meta-analysis. Two classes are kept apart deliberately: **general standards** intended to be reusable across producers, and **pipeline sidecars** — structured but per-pipeline documentative formats. Generated from `standards.yaml`; do not edit by hand.

## General standards

| Standard | Unit | Purpose | Layer | Derivation? | Relevance | EnVar relation |
| --- | --- | --- | --- | --- | --- | --- |
| [ACDD](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) | dataset | find | discovery | absent | in_scope | Overlaps source_dataset (geospatial_resolution, temporal_resolution, creator, institution); complementary at dataset level. |
| [CDIF](https://codata.org/initiatives/making-data-work/cdif/) | dataset | find | discovery | absent | peripheral | Overlaps source_dataset at discovery and cross-domain linkage level; complementary — EnVar could serve as a domain profile within a CDIF-governed ecosystem. |
| [CF Conventions](https://cfconventions.org/) | variable_type | define | conceptual | partial | in_scope | Overlaps variable_identity and temporal_reference; complementary — CF standard_name is the primary slot in EnVar VariableIdentity.cf_standard_name. |
| [CODATA / GEO Essential Variables](https://codata.org/) | variable_type | define | conceptual | absent | peripheral | Overlaps variable_identity (what to measure); complementary — Essential Variables inform target_vocab_concept in EnVar VariableIdentity. |
| [Croissant](https://mlcommons.org/croissant/) | dataset | define | conceptual | partial | peripheral | Overlaps source_dataset and data_layout for ML training use of exposure datasets; complementary but ML-focused. |
| [DataCite Metadata Schema](https://schema.datacite.org/) | dataset | cite | discovery | partial | peripheral | Overlaps deposit_metadata and source_dataset citation; complementary — DataCite DOI is the persistent identifier for upstream products an EnVar sidecar documents. |
| [DCAT](https://www.w3.org/TR/vocab-dcat-3/) | dataset | find | discovery | absent | in_scope | Overlaps source_dataset discovery; complementary, operates at dataset layer not instance layer. |
| [DDI](https://ddialliance.org/) | variable_type | define | conceptual | partial | peripheral | Overlaps variable_identity at study/variable level; complementary — DDI variable metadata maps to EnVar VariableIdentity for survey-linked exposure assessments. |
| [Frictionless Data Package](https://specs.frictionlessdata.io/) | file | define | conceptual | absent | peripheral | Overlaps data_layout for CSV/tabular exposure outputs; complementary — could describe the companion data file that an EnVar sidecar annotates. |
| [NASA/GCMD DIF](https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/directory-interchange-format-standard) | dataset | find | discovery | partial | peripheral | Overlaps source_dataset for NASA-hosted exposure products; complementary — DIF records discovery metadata for datasets whose EnVar sidecar provides instance-level detail. |
| [GeoSPARQL](https://www.ogc.org/standard/geosparql/) | produced_value | define | conceptual | absent | peripheral | Overlaps spatial_reference for Linked Data encoding; complementary — GeoSPARQL geo:hasGeometry carries the geometry referenced by EnVar SpatialReference. |
| [HL7 FHIR](https://www.hl7.org/fhir/) | geocoded_row | define | linkage | partial | peripheral | Overlaps health_layer_linkage at the clinical record level; complementary — FHIR can receive exposure values from an EnVar-documented pipeline. |
| [ISO 19115](https://www.iso.org/standard/53798.html) | dataset | find | discovery | partial | in_scope | Overlaps source_dataset and spatial_reference; complementary at dataset layer, silent at instance/linkage levels. |
| [OGC Observations, Measurements, and Samples](https://www.ogc.org/standard/om/) | produced_value | define | instance | partial | in_scope | Overlaps variable_identity, spatial_reference, temporal_reference, and exposure_model; complementary — closest general standard to EnVar's instance-level observation model. |
| [ODM2](http://www.odm2.org/) | produced_value | reproduce_pool | instance | carried | in_scope | Overlaps variable_identity, exposure_model, uncertainty, and tool_run; most competitive standard with EnVar for in-situ data; EnVar extends scope to gridded/modeled exposures and health linkage. |
| [OGC API Records](https://ogcapi.ogc.org/records/) | dataset | find | discovery | absent | in_scope | Overlaps source_dataset discovery; complementary — OGC API Records surfaces datasets whose instance-level detail is captured in an EnVar sidecar. |
| [OMOP CDM](https://ohdsi.github.io/CommonDataModel/) | geocoded_row | reproduce_pool | linkage | partial | in_scope | Directly overlaps health_layer_linkage and deposit_metadata; EnVar health_layer_linkage.target_cdm targets OMOP; competing at schema level but complementary as output consumer. |
| [PROV-O](https://www.w3.org/TR/prov-o/) | produced_value | reproduce_pool | instance | carried | in_scope | Directly overlaps provenance_chain and tool_run; complementary — EnVar ProvenanceChain is a domain-constrained PROV-O profile. |
| [RO-Crate](https://www.researchobject.org/ro-crate/specification.html) | file | reproduce_pool | instance | carried | in_scope | Overlaps tool_run and provenance_chain; complementary — RO-Crate WorkflowRun profile is the closest existing standard to EnVar's reproducibility intent at file/package level. |
| [schema.org / science-on-schema.org](https://science-on-schema.org/) | dataset | find | discovery | absent | peripheral | Overlaps source_dataset discovery and variable_identity (variableMeasured); complementary — landing page markup linking to EnVar-documented datasets. |
| [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/) | produced_value | define | instance | partial | in_scope | Overlaps variable_identity, exposure_model, and provenance_chain; complementary — sosa:usedProcedure maps to EnVar exposure_model. |
| [STAC](https://stacspec.org/) | file | find | discovery | partial | in_scope | Overlaps source_dataset and spatial_reference; complementary — STAC items provide asset-level discovery linking to EnVar-documented datasets. |
| [WaterML 2.0](https://www.ogc.org/standard/waterml/) | produced_value | define | instance | partial | peripheral | Overlaps variable_identity and temporal_reference for water-quality exposures; complementary — WaterML serializes observations that an EnVar sidecar documents. |
| [WMO WIGOS Metadata Standard](https://library.wmo.int/records/item/55626-wigos-metadata-standard) | dataset | define | conceptual | partial | in_scope | Overlaps source_dataset and exposure_model (instrument inputs); complementary at station/instrument layer. |

## Pipeline sidecars

| Standard | Unit | Purpose | Layer | Derivation? | Relevance | EnVar relation |
| --- | --- | --- | --- | --- | --- | --- |
| [DeGAUSS](https://degauss.org/) | geocoded_row | reproduce_pool | linkage | carried | in_scope | Directly overlaps linkage_method and health_layer_linkage; DeGAUSS container invocation metadata is the primary reference implementation for EnVar LinkageMethod in pediatric cohort studies. |
| [gridMET / Daymet / PRISM sidecars](https://www.climatologylab.org/gridmet.html) | file | reproduce_pool | instance | partial | peripheral | The gap that EnVar source_dataset and tool_run are designed to replace; competing in intent, complementary until EnVar adoption grows. |

## Reconciliation with the niehs inventory

| Standard | Status | Where |
| --- | --- | --- |
| ISO 19115 | new |  |
| OGC Observations, Measurements, and Samples | new |  |
| SOSA/SSN | new |  |
| CF Conventions | new |  |
| ACDD | new |  |
| STAC | new |  |
| OGC API Records | new |  |
| WMO WIGOS Metadata Standard | new |  |
| PROV-O | new |  |
| RO-Crate | new |  |
| DCAT | already_catalogued | projects_inventory.md §1.1 (GAIA meta_dcat) |
| DataCite Metadata Schema | new |  |
| Frictionless Data Package | new |  |
| schema.org / science-on-schema.org | new |  |
| DDI | new |  |
| Croissant | new |  |
| CDIF | new |  |
| OMOP CDM | new |  |
| HL7 FHIR | new |  |
| ODM2 | new |  |
| WaterML 2.0 | new |  |
| CODATA / GEO Essential Variables | new |  |
| NASA/GCMD DIF | new |  |
| GeoSPARQL | new |  |
| DeGAUSS | new |  |
| gridMET / Daymet / PRISM sidecars | new |  |

## Triaged out

Candidates considered and ruled out of the first-class index, kept for auditability.

- **AGI Glossary of Geology** (vocabulary) — out_of_scope: Pure geological glossary; not a metadata format.
- **Agroportal** (project_or_platform) — out_of_scope: Agronomic ontology portal; not a metadata format.
- **AGROVOC** (vocabulary) — out_of_scope: SKOS thesaurus for agriculture and food; not a metadata format.
- **ANZSRC 2020** (other) — out_of_scope: Australian and New Zealand Standard Research Classification; research classification scheme, not an environmental-exposure metadata standard.
- **Aquatic Sciences and Fisheries Thesaurus** (vocabulary) — out_of_scope: Pure vocabulary for aquatic and fisheries domain.
- **Astronomical Environment Ontology** (vocabulary) — out_of_scope: Out of domain for terrestrial environmental-exposure data.
- **BARTOC** (project_or_platform) — out_of_scope: Registry of thesauri and ontologies; not a metadata standard.
- **BCO-DMO** (project_or_platform) — out_of_scope: Biological and Chemical Oceanography Data Management Office repository; platform, not a standard.
- **BioPortal** (project_or_platform) — out_of_scope: Biomedical ontology repository hosting SWEET, ENVO, and others; not a metadata format.
- **CAB Thesaurus** (vocabulary) — out_of_scope: CABI agriculture and environment thesaurus; pure vocabulary.
- **CGI Vocabularies Register** (vocabulary) — out_of_scope: Controlled vocabulary register for geoscience terms; not a metadata format.
- **Coastal and Marine Ecological Classification Standard** (other) — out_of_scope: Habitat classification scheme for coastal and marine environments; not a metadata format for environmental-exposure data.
- **Collections Descriptions** (other) — out_of_scope: TDWG biodiversity collection descriptions; out of scope for environmental-exposure metadata.
- **CSDMS Standard Names** (vocabulary) — out_of_scope: Variable naming convention for earth surface models; vocabulary-level, not a metadata format.
- **Darwin Core** (vocabulary) — out_of_scope: Biodiversity observations vocabulary; not designed for environmental-exposure metadata.
- **EcoPortal** (project_or_platform) — out_of_scope: Ecology ontology portal; not a metadata format.
- **ECSO Ecosystems Ontology** (vocabulary) — out_of_scope: OWL ontology for ecosystem descriptions; pure vocabulary.
- **EFG** (other) — out_of_scope: Extension for Geosciences (biodiversity natural history collections); out of domain.
- **Environment Ontology** (vocabulary) — peripheral: OBO ontology for environmental features and biomes; used for concept annotation in SOSA/SSN and EnVar VariableIdentity but is a vocabulary, not a metadata format.
- **Environmental Thesaurus** (vocabulary) — out_of_scope: SKOS thesaurus for environmental terms; pure vocabulary.
- **ESIP Community Ontology Repository** (project_or_platform) — out_of_scope: Vocabulary registry and hosting service; not a metadata format.
- **EU Vocabularies** (vocabulary) — out_of_scope: Controlled vocabularies for EU institutions; not environmental-exposure metadata standards.
- **4TU.ResearchData** (project_or_platform) — out_of_scope: Dutch research data repository; platform, not a metadata standard.
- **GBIF Vocabulary Service** (project_or_platform) — out_of_scope: Biodiversity vocabulary service; not a metadata format for environmental-exposure data.
- **GCMD Science Keywords** (vocabulary) — out_of_scope: Pure controlled vocabulary for tagging NASA Earth science datasets; not a metadata format.
- **Global Change Master Directory** (project_or_platform) — peripheral: NASA Earth science dataset catalog platform; relevant as the origin of the DIF metadata standard (covered in entries as gcmd-dif) but not itself a metadata standard.
- **GeoCore Ontology** (vocabulary) — out_of_scope: Core vocabulary for geospatial data concepts; not an adopted metadata format standard.
- **GeoNames** (vocabulary) — out_of_scope: Geographic names gazetteer; not an exposure-metadata standard.
- **Getty Thesaurus of Geographic Names** (vocabulary) — out_of_scope: Pure geographic names vocabulary.
- **IODE Ocean Data Portal parameter dictionary** (vocabulary) — out_of_scope: Vocabulary/parameter list for oceanographic data; not a metadata format standard.
- **Marine Metadata Interoperability Project** (project_or_platform) — out_of_scope: Community project for marine metadata vocabulary management; not itself a metadata standard.
- **MIDS** (other) — out_of_scope: Minimum Information about a Digital Specimen (TDWG); natural history specimen metadata; out of scope.
- **MINDAT** (other) — out_of_scope: Mineralogy and geology database; out of domain.
- **MMI Ontology Registry and Repository** (project_or_platform) — out_of_scope: Marine metadata vocabulary registry; not a metadata format.
- **NERC Vocabulary Server** (project_or_platform) — out_of_scope: BODC/NERC vocabulary management service; not a metadata format.
- **OBO Foundry** (project_or_platform) — out_of_scope: Ontology community framework and registry; not a metadata format.
- **Ontology Resources for Environmental Health Sciences** (other) — out_of_scope: Survey/article on ontology resources for environmental health; not a metadata standard.
- **Ontobee** (project_or_platform) — out_of_scope: Ontology browser and SPARQL endpoint; not a metadata standard.
- **Orbital Space Domain Knowledge Models** (other) — out_of_scope: Space domain ontologies and vocabularies; out of domain for terrestrial exposure data.
- **QUDT** (vocabulary) — peripheral: Quantities, Units, Dimensions, and Types ontology; used for unit annotation in exposure data alongside EnVar but is a vocabulary, not a metadata format.
- **Research Vocabularies Australia** (project_or_platform) — out_of_scope: National vocabulary service for Australian research; not a metadata format.
- **RRUFF** (other) — out_of_scope: Mineral Raman spectra database; out of domain for environmental-exposure data.
- **Semantic interoperability in environmental sciences survey** (other) — peripheral: Survey paper on semantic interoperability in environmental sciences; relevant background literature but not a metadata standard.
- **Scientific Variables Ontology** (vocabulary) — peripheral: Ontology for decomposing scientific variable names into components; relevant to variable identity in exposure research but is a vocabulary, not a metadata format.
- **SWEET** (vocabulary) — out_of_scope: OWL ontology for earth and environmental science concepts; pure vocabulary, not a metadata format.
- **TERN Controlled Vocabularies** (vocabulary) — peripheral: Australia's TERN SOSA/SSN-based controlled vocabularies for ecosystem observation; the underlying TERN data model is a SOSA/SSN profile (in-scope tier) but the standalone CV set is a vocabulary.
- **USGS Thesaurus** (vocabulary) — out_of_scope: Pure thesaurus for USGS subject terms; not a metadata format.
- **vocabularies repositories catalog** (other) — out_of_scope: Generic category label in source list, not a specific standard.
- **vocabulary resources** (other) — out_of_scope: Generic category label in source list, not a specific standard.
- **WorldBank Thesaurus** (vocabulary) — out_of_scope: Pure vocabulary for World Bank subject terms.
- **WoRMS** (other) — out_of_scope: World Register of Marine Species; taxonomy database, not an exposure-metadata standard.
