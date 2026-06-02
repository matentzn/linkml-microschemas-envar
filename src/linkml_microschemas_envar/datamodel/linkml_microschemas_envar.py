# Auto generated from linkml_microschemas_envar.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-06-01T17:49:06
# Schema: linkml-microschemas-envar
#
# id: https://w3id.org/linkml/microschemas/envar
# description: LinkML microschemas for environmental exposure variables (EnVar). Initial
#   scope: heat-related exposures (Tmax, WBGT, heat index, heat-wave flags)
#   and the surrounding provenance metadata needed to load them into OMOP
#   external_exposure with full reproducibility.
#
#   This umbrella schema imports the eleven modules that together define the
#   EnVar metadata layer:
#
#     - envar_common         shared enums and slots
#     - envar_variable       variable identity (CF, UCUM, OMOP, ECTO, ENVO)
#     - envar_spatial        spatial reference, extraction
#     - envar_temporal       temporal reference, day-boundary convention
#     - envar_source         upstream source dataset
#     - envar_model          exposure model character
#     - envar_uncertainty    uncertainty and quality
#     - envar_linkage        gridded-to-patient linkage
#     - envar_toolrun        tool run and W3C-PROV provenance chain
#     - envar_heat_metric    derived heat metrics (WBGT, HI, UTCI, heat-wave)
#     - envar_omop           OMOP linkage and FAIR deposit
#     - envar_record         the top EnvironmentalExposureRecord composite
#     - envar_examples       concrete record subclasses (Tmax, Tmin, WBGT, EHD)
# license: Apache-2.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Date, Datetime, Decimal, Float, Integer, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Decimal, URI, URIorCURIE, XSDDate, XSDDateTime

metamodel_version = "1.11.0"
version = "0.1.0"

# Namespaces
CF = CurieNamespace('CF', 'http://vocab.nerc.ac.uk/standard_name/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
ENVAR = CurieNamespace('envar', 'https://w3id.org/linkml/microschemas/envar/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = ENVAR


# Types

# Class references



@dataclass(repr=False)
class VariableIdentity(YAMLRoot):
    """
    The identity and semantics of an environmental exposure variable — what physical quantity is being captured, in
    what units, and how it binds to community vocabularies. One per record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["VariableIdentity"]
    class_class_curie: ClassVar[str] = "envar:VariableIdentity"
    class_name: ClassVar[str] = "VariableIdentity"
    class_model_uri: ClassVar[URIRef] = ENVAR.VariableIdentity

    variable_name: str = None
    cf_standard_name: str = None
    units_ucum: str = None
    omop_concept_status: Union[str, "OmopConceptStatusEnum"] = None
    value_data_type: Union[str, "DataTypeEnum"] = None
    variable_label: Optional[str] = None
    cf_cell_methods: Optional[str] = None
    units_display: Optional[str] = None
    omop_concept_id: Optional[int] = None
    omop_concept_id_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    ecto_iri: Optional[Union[str, URIorCURIE]] = None
    ecto_iri_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    envo_iri: Optional[Union[str, URIorCURIE]] = None
    loinc_code: Optional[str] = None
    loinc_code_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    snomed_code: Optional[str] = None
    snomed_code_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    value_range_plausible_min: Optional[float] = None
    value_range_plausible_max: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.variable_name):
            self.MissingRequiredField("variable_name")
        if not isinstance(self.variable_name, str):
            self.variable_name = str(self.variable_name)

        if self._is_empty(self.cf_standard_name):
            self.MissingRequiredField("cf_standard_name")
        if not isinstance(self.cf_standard_name, str):
            self.cf_standard_name = str(self.cf_standard_name)

        if self._is_empty(self.units_ucum):
            self.MissingRequiredField("units_ucum")
        if not isinstance(self.units_ucum, str):
            self.units_ucum = str(self.units_ucum)

        if self._is_empty(self.omop_concept_status):
            self.MissingRequiredField("omop_concept_status")
        if not isinstance(self.omop_concept_status, OmopConceptStatusEnum):
            self.omop_concept_status = OmopConceptStatusEnum(self.omop_concept_status)

        if self._is_empty(self.value_data_type):
            self.MissingRequiredField("value_data_type")
        if not isinstance(self.value_data_type, DataTypeEnum):
            self.value_data_type = DataTypeEnum(self.value_data_type)

        if self.variable_label is not None and not isinstance(self.variable_label, str):
            self.variable_label = str(self.variable_label)

        if self.cf_cell_methods is not None and not isinstance(self.cf_cell_methods, str):
            self.cf_cell_methods = str(self.cf_cell_methods)

        if self.units_display is not None and not isinstance(self.units_display, str):
            self.units_display = str(self.units_display)

        if self.omop_concept_id is not None and not isinstance(self.omop_concept_id, int):
            self.omop_concept_id = int(self.omop_concept_id)

        if self.omop_concept_id_missing_reason is not None and not isinstance(self.omop_concept_id_missing_reason, MissingReasonEnum):
            self.omop_concept_id_missing_reason = MissingReasonEnum(self.omop_concept_id_missing_reason)

        if self.ecto_iri is not None and not isinstance(self.ecto_iri, URIorCURIE):
            self.ecto_iri = URIorCURIE(self.ecto_iri)

        if self.ecto_iri_missing_reason is not None and not isinstance(self.ecto_iri_missing_reason, MissingReasonEnum):
            self.ecto_iri_missing_reason = MissingReasonEnum(self.ecto_iri_missing_reason)

        if self.envo_iri is not None and not isinstance(self.envo_iri, URIorCURIE):
            self.envo_iri = URIorCURIE(self.envo_iri)

        if self.loinc_code is not None and not isinstance(self.loinc_code, str):
            self.loinc_code = str(self.loinc_code)

        if self.loinc_code_missing_reason is not None and not isinstance(self.loinc_code_missing_reason, MissingReasonEnum):
            self.loinc_code_missing_reason = MissingReasonEnum(self.loinc_code_missing_reason)

        if self.snomed_code is not None and not isinstance(self.snomed_code, str):
            self.snomed_code = str(self.snomed_code)

        if self.snomed_code_missing_reason is not None and not isinstance(self.snomed_code_missing_reason, MissingReasonEnum):
            self.snomed_code_missing_reason = MissingReasonEnum(self.snomed_code_missing_reason)

        if self.value_range_plausible_min is not None and not isinstance(self.value_range_plausible_min, float):
            self.value_range_plausible_min = float(self.value_range_plausible_min)

        if self.value_range_plausible_max is not None and not isinstance(self.value_range_plausible_max, float):
            self.value_range_plausible_max = float(self.value_range_plausible_max)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SpatialReference(YAMLRoot):
    """
    Spatial provenance of an environmental exposure value: the native grid / footprint of the source product, the CRS,
    the geographic extent, the extraction rule used to attach a value to a patient location, and the target geography
    type. One per record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["SpatialReference"]
    class_class_curie: ClassVar[str] = "envar:SpatialReference"
    class_name: ClassVar[str] = "SpatialReference"
    class_model_uri: ClassVar[URIRef] = ENVAR.SpatialReference

    crs: str = None
    extraction_method: Union[str, "ExtractionMethodEnum"] = None
    target_geography_type: Union[str, "TargetGeographyTypeEnum"] = None
    native_spatial_resolution_m: Optional[float] = None
    native_spatial_resolution_descriptor: Optional[str] = None
    spatial_extent_bbox: Optional[Union[float, list[float]]] = empty_list()
    spatial_extent_descriptor: Optional[str] = None
    extraction_buffer_m: Optional[float] = None
    extraction_buffer_m_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    population_weighting_source: Optional[str] = None
    population_weighting_source_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.crs):
            self.MissingRequiredField("crs")
        if not isinstance(self.crs, str):
            self.crs = str(self.crs)

        if self._is_empty(self.extraction_method):
            self.MissingRequiredField("extraction_method")
        if not isinstance(self.extraction_method, ExtractionMethodEnum):
            self.extraction_method = ExtractionMethodEnum(self.extraction_method)

        if self._is_empty(self.target_geography_type):
            self.MissingRequiredField("target_geography_type")
        if not isinstance(self.target_geography_type, TargetGeographyTypeEnum):
            self.target_geography_type = TargetGeographyTypeEnum(self.target_geography_type)

        if self.native_spatial_resolution_m is not None and not isinstance(self.native_spatial_resolution_m, float):
            self.native_spatial_resolution_m = float(self.native_spatial_resolution_m)

        if self.native_spatial_resolution_descriptor is not None and not isinstance(self.native_spatial_resolution_descriptor, str):
            self.native_spatial_resolution_descriptor = str(self.native_spatial_resolution_descriptor)

        if not isinstance(self.spatial_extent_bbox, list):
            self.spatial_extent_bbox = [self.spatial_extent_bbox] if self.spatial_extent_bbox is not None else []
        self.spatial_extent_bbox = [v if isinstance(v, float) else float(v) for v in self.spatial_extent_bbox]

        if self.spatial_extent_descriptor is not None and not isinstance(self.spatial_extent_descriptor, str):
            self.spatial_extent_descriptor = str(self.spatial_extent_descriptor)

        if self.extraction_buffer_m is not None and not isinstance(self.extraction_buffer_m, float):
            self.extraction_buffer_m = float(self.extraction_buffer_m)

        if self.extraction_buffer_m_missing_reason is not None and not isinstance(self.extraction_buffer_m_missing_reason, MissingReasonEnum):
            self.extraction_buffer_m_missing_reason = MissingReasonEnum(self.extraction_buffer_m_missing_reason)

        if self.population_weighting_source is not None and not isinstance(self.population_weighting_source, str):
            self.population_weighting_source = str(self.population_weighting_source)

        if self.population_weighting_source_missing_reason is not None and not isinstance(self.population_weighting_source_missing_reason, MissingReasonEnum):
            self.population_weighting_source_missing_reason = MissingReasonEnum(self.population_weighting_source_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TemporalReference(YAMLRoot):
    """
    Temporal provenance of an environmental exposure value: native temporal grain, aggregation rule, day-boundary
    convention, coverage of the source product, the extraction window the run actually pulled, calendar, and lag
    alignment to a clinical event. One per record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["TemporalReference"]
    class_class_curie: ClassVar[str] = "envar:TemporalReference"
    class_name: ClassVar[str] = "TemporalReference"
    class_model_uri: ClassVar[URIRef] = ENVAR.TemporalReference

    temporal_resolution: Union[str, "TemporalResolutionEnum"] = None
    temporal_aggregation_method: Union[str, "TemporalAggregationMethodEnum"] = None
    day_boundary_convention: Union[str, "DayBoundaryConventionEnum"] = None
    temporal_aggregation_window_seconds: Optional[int] = None
    temporal_coverage_start: Optional[Union[str, XSDDate]] = None
    temporal_coverage_end: Optional[Union[str, XSDDate]] = None
    extraction_window_start: Optional[Union[str, XSDDate]] = None
    extraction_window_end: Optional[Union[str, XSDDate]] = None
    calendar: Optional[Union[str, "CalendarEnum"]] = None
    lag_alignment_applied: Optional[Union[str, "LagAlignmentEnum"]] = None
    lag_alignment_specifier: Optional[str] = None
    lag_alignment_applied_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.temporal_resolution):
            self.MissingRequiredField("temporal_resolution")
        if not isinstance(self.temporal_resolution, TemporalResolutionEnum):
            self.temporal_resolution = TemporalResolutionEnum(self.temporal_resolution)

        if self._is_empty(self.temporal_aggregation_method):
            self.MissingRequiredField("temporal_aggregation_method")
        if not isinstance(self.temporal_aggregation_method, TemporalAggregationMethodEnum):
            self.temporal_aggregation_method = TemporalAggregationMethodEnum(self.temporal_aggregation_method)

        if self._is_empty(self.day_boundary_convention):
            self.MissingRequiredField("day_boundary_convention")
        if not isinstance(self.day_boundary_convention, DayBoundaryConventionEnum):
            self.day_boundary_convention = DayBoundaryConventionEnum(self.day_boundary_convention)

        if self.temporal_aggregation_window_seconds is not None and not isinstance(self.temporal_aggregation_window_seconds, int):
            self.temporal_aggregation_window_seconds = int(self.temporal_aggregation_window_seconds)

        if self.temporal_coverage_start is not None and not isinstance(self.temporal_coverage_start, XSDDate):
            self.temporal_coverage_start = XSDDate(self.temporal_coverage_start)

        if self.temporal_coverage_end is not None and not isinstance(self.temporal_coverage_end, XSDDate):
            self.temporal_coverage_end = XSDDate(self.temporal_coverage_end)

        if self.extraction_window_start is not None and not isinstance(self.extraction_window_start, XSDDate):
            self.extraction_window_start = XSDDate(self.extraction_window_start)

        if self.extraction_window_end is not None and not isinstance(self.extraction_window_end, XSDDate):
            self.extraction_window_end = XSDDate(self.extraction_window_end)

        if self.calendar is not None and not isinstance(self.calendar, CalendarEnum):
            self.calendar = CalendarEnum(self.calendar)

        if self.lag_alignment_applied is not None and not isinstance(self.lag_alignment_applied, LagAlignmentEnum):
            self.lag_alignment_applied = LagAlignmentEnum(self.lag_alignment_applied)

        if self.lag_alignment_specifier is not None and not isinstance(self.lag_alignment_specifier, str):
            self.lag_alignment_specifier = str(self.lag_alignment_specifier)

        if self.lag_alignment_applied_missing_reason is not None and not isinstance(self.lag_alignment_applied_missing_reason, MissingReasonEnum):
            self.lag_alignment_applied_missing_reason = MissingReasonEnum(self.lag_alignment_applied_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SourceDataset(YAMLRoot):
    """
    The upstream gridded / station product the exposure values originate from. Carries identity, DOI, version,
    coverage, producer, citation, license, native format, and homogenisation status. One per record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["SourceDataset"]
    class_class_curie: ClassVar[str] = "envar:SourceDataset"
    class_name: ClassVar[str] = "SourceDataset"
    class_model_uri: ClassVar[URIRef] = ENVAR.SourceDataset

    source_dataset_name: str = None
    source_dataset_short_code: str = None
    source_dataset_version: str = None
    source_producer_institution: str = None
    source_license_spdx: str = None
    source_native_format: Union[str, "SourceNativeFormatEnum"] = None
    source_dataset_doi: Optional[str] = None
    source_dataset_doi_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    source_dataset_temporal_coverage: Optional[str] = None
    source_dataset_spatial_extent: Optional[str] = None
    source_citation_apa: Optional[str] = None
    source_citation_bibtex: Optional[str] = None
    source_citation_bibtex_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    source_access_url: Optional[Union[str, URI]] = None
    source_homogenisation_status: Optional[Union[str, "HomogenisationStatusEnum"]] = None
    source_homogenisation_status_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    source_acdd_attributes: Optional[str] = None
    source_acdd_attributes_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.source_dataset_name):
            self.MissingRequiredField("source_dataset_name")
        if not isinstance(self.source_dataset_name, str):
            self.source_dataset_name = str(self.source_dataset_name)

        if self._is_empty(self.source_dataset_short_code):
            self.MissingRequiredField("source_dataset_short_code")
        if not isinstance(self.source_dataset_short_code, str):
            self.source_dataset_short_code = str(self.source_dataset_short_code)

        if self._is_empty(self.source_dataset_version):
            self.MissingRequiredField("source_dataset_version")
        if not isinstance(self.source_dataset_version, str):
            self.source_dataset_version = str(self.source_dataset_version)

        if self._is_empty(self.source_producer_institution):
            self.MissingRequiredField("source_producer_institution")
        if not isinstance(self.source_producer_institution, str):
            self.source_producer_institution = str(self.source_producer_institution)

        if self._is_empty(self.source_license_spdx):
            self.MissingRequiredField("source_license_spdx")
        if not isinstance(self.source_license_spdx, str):
            self.source_license_spdx = str(self.source_license_spdx)

        if self._is_empty(self.source_native_format):
            self.MissingRequiredField("source_native_format")
        if not isinstance(self.source_native_format, SourceNativeFormatEnum):
            self.source_native_format = SourceNativeFormatEnum(self.source_native_format)

        if self.source_dataset_doi is not None and not isinstance(self.source_dataset_doi, str):
            self.source_dataset_doi = str(self.source_dataset_doi)

        if self.source_dataset_doi_missing_reason is not None and not isinstance(self.source_dataset_doi_missing_reason, MissingReasonEnum):
            self.source_dataset_doi_missing_reason = MissingReasonEnum(self.source_dataset_doi_missing_reason)

        if self.source_dataset_temporal_coverage is not None and not isinstance(self.source_dataset_temporal_coverage, str):
            self.source_dataset_temporal_coverage = str(self.source_dataset_temporal_coverage)

        if self.source_dataset_spatial_extent is not None and not isinstance(self.source_dataset_spatial_extent, str):
            self.source_dataset_spatial_extent = str(self.source_dataset_spatial_extent)

        if self.source_citation_apa is not None and not isinstance(self.source_citation_apa, str):
            self.source_citation_apa = str(self.source_citation_apa)

        if self.source_citation_bibtex is not None and not isinstance(self.source_citation_bibtex, str):
            self.source_citation_bibtex = str(self.source_citation_bibtex)

        if self.source_citation_bibtex_missing_reason is not None and not isinstance(self.source_citation_bibtex_missing_reason, MissingReasonEnum):
            self.source_citation_bibtex_missing_reason = MissingReasonEnum(self.source_citation_bibtex_missing_reason)

        if self.source_access_url is not None and not isinstance(self.source_access_url, URI):
            self.source_access_url = URI(self.source_access_url)

        if self.source_homogenisation_status is not None and not isinstance(self.source_homogenisation_status, HomogenisationStatusEnum):
            self.source_homogenisation_status = HomogenisationStatusEnum(self.source_homogenisation_status)

        if self.source_homogenisation_status_missing_reason is not None and not isinstance(self.source_homogenisation_status_missing_reason, MissingReasonEnum):
            self.source_homogenisation_status_missing_reason = MissingReasonEnum(self.source_homogenisation_status_missing_reason)

        if self.source_acdd_attributes is not None and not isinstance(self.source_acdd_attributes, str):
            self.source_acdd_attributes = str(self.source_acdd_attributes)

        if self.source_acdd_attributes_missing_reason is not None and not isinstance(self.source_acdd_attributes_missing_reason, MissingReasonEnum):
            self.source_acdd_attributes_missing_reason = MissingReasonEnum(self.source_acdd_attributes_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExposureModel(YAMLRoot):
    """
    The model class that produced the values (interpolation, reanalysis, ML, statistical blend, equation), its inputs,
    its methods-paper DOI, its cross-validation skill, known biases, and any bias correction. One per record; may be
    null for direct observation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["ExposureModel"]
    class_class_curie: ClassVar[str] = "envar:ExposureModel"
    class_name: ClassVar[str] = "ExposureModel"
    class_model_uri: ClassVar[URIRef] = ENVAR.ExposureModel

    exposure_model_type: Union[str, "ExposureModelTypeEnum"] = None
    exposure_model_inputs: Optional[Union[str, list[str]]] = empty_list()
    exposure_model_paper_doi: Optional[str] = None
    exposure_model_paper_doi_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    exposure_model_cross_validation_r2: Optional[float] = None
    exposure_model_cross_validation_r2_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    exposure_model_known_biases: Optional[Union[str, list[str]]] = empty_list()
    exposure_model_uncertainty_field: Optional[str] = None
    exposure_model_uncertainty_field_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    exposure_model_ensemble_member_count: Optional[int] = None
    exposure_model_ensemble_member_count_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    bias_correction_applied: Optional[Union[str, "BiasCorrectionAppliedEnum"]] = None
    bias_correction_applied_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.exposure_model_type):
            self.MissingRequiredField("exposure_model_type")
        if not isinstance(self.exposure_model_type, ExposureModelTypeEnum):
            self.exposure_model_type = ExposureModelTypeEnum(self.exposure_model_type)

        if not isinstance(self.exposure_model_inputs, list):
            self.exposure_model_inputs = [self.exposure_model_inputs] if self.exposure_model_inputs is not None else []
        self.exposure_model_inputs = [v if isinstance(v, str) else str(v) for v in self.exposure_model_inputs]

        if self.exposure_model_paper_doi is not None and not isinstance(self.exposure_model_paper_doi, str):
            self.exposure_model_paper_doi = str(self.exposure_model_paper_doi)

        if self.exposure_model_paper_doi_missing_reason is not None and not isinstance(self.exposure_model_paper_doi_missing_reason, MissingReasonEnum):
            self.exposure_model_paper_doi_missing_reason = MissingReasonEnum(self.exposure_model_paper_doi_missing_reason)

        if self.exposure_model_cross_validation_r2 is not None and not isinstance(self.exposure_model_cross_validation_r2, float):
            self.exposure_model_cross_validation_r2 = float(self.exposure_model_cross_validation_r2)

        if self.exposure_model_cross_validation_r2_missing_reason is not None and not isinstance(self.exposure_model_cross_validation_r2_missing_reason, MissingReasonEnum):
            self.exposure_model_cross_validation_r2_missing_reason = MissingReasonEnum(self.exposure_model_cross_validation_r2_missing_reason)

        if not isinstance(self.exposure_model_known_biases, list):
            self.exposure_model_known_biases = [self.exposure_model_known_biases] if self.exposure_model_known_biases is not None else []
        self.exposure_model_known_biases = [v if isinstance(v, str) else str(v) for v in self.exposure_model_known_biases]

        if self.exposure_model_uncertainty_field is not None and not isinstance(self.exposure_model_uncertainty_field, str):
            self.exposure_model_uncertainty_field = str(self.exposure_model_uncertainty_field)

        if self.exposure_model_uncertainty_field_missing_reason is not None and not isinstance(self.exposure_model_uncertainty_field_missing_reason, MissingReasonEnum):
            self.exposure_model_uncertainty_field_missing_reason = MissingReasonEnum(self.exposure_model_uncertainty_field_missing_reason)

        if self.exposure_model_ensemble_member_count is not None and not isinstance(self.exposure_model_ensemble_member_count, int):
            self.exposure_model_ensemble_member_count = int(self.exposure_model_ensemble_member_count)

        if self.exposure_model_ensemble_member_count_missing_reason is not None and not isinstance(self.exposure_model_ensemble_member_count_missing_reason, MissingReasonEnum):
            self.exposure_model_ensemble_member_count_missing_reason = MissingReasonEnum(self.exposure_model_ensemble_member_count_missing_reason)

        if self.bias_correction_applied is not None and not isinstance(self.bias_correction_applied, BiasCorrectionAppliedEnum):
            self.bias_correction_applied = BiasCorrectionAppliedEnum(self.bias_correction_applied)

        if self.bias_correction_applied_missing_reason is not None and not isinstance(self.bias_correction_applied_missing_reason, MissingReasonEnum):
            self.bias_correction_applied_missing_reason = MissingReasonEnum(self.bias_correction_applied_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Uncertainty(YAMLRoot):
    """
    Uncertainty and quality character of a value series: per-value uncertainty column, uncertainty type / units,
    model-aggregate uncertainty summary, quality flag pointers, missing-data handling, and data completeness. One per
    record; slots may be null with reasons.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["Uncertainty"]
    class_class_curie: ClassVar[str] = "envar:Uncertainty"
    class_name: ClassVar[str] = "Uncertainty"
    class_model_uri: ClassVar[URIRef] = ENVAR.Uncertainty

    per_value_uncertainty_field_name: Optional[str] = None
    per_value_uncertainty_field_name_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    per_value_uncertainty_type: Optional[Union[str, "UncertaintyTypeEnum"]] = None
    per_value_uncertainty_type_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    per_value_uncertainty_units_ucum: Optional[str] = None
    per_value_uncertainty_units_ucum_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    model_aggregate_uncertainty: Optional[str] = None
    model_aggregate_uncertainty_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    quality_flag_field_name: Optional[str] = None
    quality_flag_field_name_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    quality_flag_vocabulary: Optional[str] = None
    quality_flag_vocabulary_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    missing_data_handling_method: Optional[Union[str, "MissingDataHandlingEnum"]] = None
    missing_data_handling_method_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    data_completeness_pct: Optional[float] = None
    data_completeness_pct_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.per_value_uncertainty_field_name is not None and not isinstance(self.per_value_uncertainty_field_name, str):
            self.per_value_uncertainty_field_name = str(self.per_value_uncertainty_field_name)

        if self.per_value_uncertainty_field_name_missing_reason is not None and not isinstance(self.per_value_uncertainty_field_name_missing_reason, MissingReasonEnum):
            self.per_value_uncertainty_field_name_missing_reason = MissingReasonEnum(self.per_value_uncertainty_field_name_missing_reason)

        if self.per_value_uncertainty_type is not None and not isinstance(self.per_value_uncertainty_type, UncertaintyTypeEnum):
            self.per_value_uncertainty_type = UncertaintyTypeEnum(self.per_value_uncertainty_type)

        if self.per_value_uncertainty_type_missing_reason is not None and not isinstance(self.per_value_uncertainty_type_missing_reason, MissingReasonEnum):
            self.per_value_uncertainty_type_missing_reason = MissingReasonEnum(self.per_value_uncertainty_type_missing_reason)

        if self.per_value_uncertainty_units_ucum is not None and not isinstance(self.per_value_uncertainty_units_ucum, str):
            self.per_value_uncertainty_units_ucum = str(self.per_value_uncertainty_units_ucum)

        if self.per_value_uncertainty_units_ucum_missing_reason is not None and not isinstance(self.per_value_uncertainty_units_ucum_missing_reason, MissingReasonEnum):
            self.per_value_uncertainty_units_ucum_missing_reason = MissingReasonEnum(self.per_value_uncertainty_units_ucum_missing_reason)

        if self.model_aggregate_uncertainty is not None and not isinstance(self.model_aggregate_uncertainty, str):
            self.model_aggregate_uncertainty = str(self.model_aggregate_uncertainty)

        if self.model_aggregate_uncertainty_missing_reason is not None and not isinstance(self.model_aggregate_uncertainty_missing_reason, MissingReasonEnum):
            self.model_aggregate_uncertainty_missing_reason = MissingReasonEnum(self.model_aggregate_uncertainty_missing_reason)

        if self.quality_flag_field_name is not None and not isinstance(self.quality_flag_field_name, str):
            self.quality_flag_field_name = str(self.quality_flag_field_name)

        if self.quality_flag_field_name_missing_reason is not None and not isinstance(self.quality_flag_field_name_missing_reason, MissingReasonEnum):
            self.quality_flag_field_name_missing_reason = MissingReasonEnum(self.quality_flag_field_name_missing_reason)

        if self.quality_flag_vocabulary is not None and not isinstance(self.quality_flag_vocabulary, str):
            self.quality_flag_vocabulary = str(self.quality_flag_vocabulary)

        if self.quality_flag_vocabulary_missing_reason is not None and not isinstance(self.quality_flag_vocabulary_missing_reason, MissingReasonEnum):
            self.quality_flag_vocabulary_missing_reason = MissingReasonEnum(self.quality_flag_vocabulary_missing_reason)

        if self.missing_data_handling_method is not None and not isinstance(self.missing_data_handling_method, MissingDataHandlingEnum):
            self.missing_data_handling_method = MissingDataHandlingEnum(self.missing_data_handling_method)

        if self.missing_data_handling_method_missing_reason is not None and not isinstance(self.missing_data_handling_method_missing_reason, MissingReasonEnum):
            self.missing_data_handling_method_missing_reason = MissingReasonEnum(self.missing_data_handling_method_missing_reason)

        if self.data_completeness_pct is not None and not isinstance(self.data_completeness_pct, float):
            self.data_completeness_pct = float(self.data_completeness_pct)

        if self.data_completeness_pct_missing_reason is not None and not isinstance(self.data_completeness_pct_missing_reason, MissingReasonEnum):
            self.data_completeness_pct_missing_reason = MissingReasonEnum(self.data_completeness_pct_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LinkageMethod(YAMLRoot):
    """
    How a gridded environmental value gets attached to a patient location: the linkage strategy, any buffer
    parameters, the propagated geocoder precision and score, and how patient address-over-time is modelled. One per
    record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["LinkageMethod"]
    class_class_curie: ClassVar[str] = "envar:LinkageMethod"
    class_name: ClassVar[str] = "LinkageMethod"
    class_model_uri: ClassVar[URIRef] = ENVAR.LinkageMethod

    linkage_strategy: Union[str, "LinkageStrategyEnum"] = None
    geocoding_precision_propagated: Union[str, "GeocodingPrecisionEnum"] = None
    address_period_alignment: Union[str, "AddressPeriodAlignmentEnum"] = None
    linkage_buffer_radius_m: Optional[float] = None
    linkage_buffer_radius_m_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    linkage_buffer_aggregation_method: Optional[Union[str, "BufferAggregationEnum"]] = None
    linkage_buffer_aggregation_method_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    linkage_max_distance_to_station_m: Optional[float] = None
    linkage_max_distance_to_station_m_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    geocoding_score_propagated: Optional[float] = None
    geocoding_score_propagated_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.linkage_strategy):
            self.MissingRequiredField("linkage_strategy")
        if not isinstance(self.linkage_strategy, LinkageStrategyEnum):
            self.linkage_strategy = LinkageStrategyEnum(self.linkage_strategy)

        if self._is_empty(self.geocoding_precision_propagated):
            self.MissingRequiredField("geocoding_precision_propagated")
        if not isinstance(self.geocoding_precision_propagated, GeocodingPrecisionEnum):
            self.geocoding_precision_propagated = GeocodingPrecisionEnum(self.geocoding_precision_propagated)

        if self._is_empty(self.address_period_alignment):
            self.MissingRequiredField("address_period_alignment")
        if not isinstance(self.address_period_alignment, AddressPeriodAlignmentEnum):
            self.address_period_alignment = AddressPeriodAlignmentEnum(self.address_period_alignment)

        if self.linkage_buffer_radius_m is not None and not isinstance(self.linkage_buffer_radius_m, float):
            self.linkage_buffer_radius_m = float(self.linkage_buffer_radius_m)

        if self.linkage_buffer_radius_m_missing_reason is not None and not isinstance(self.linkage_buffer_radius_m_missing_reason, MissingReasonEnum):
            self.linkage_buffer_radius_m_missing_reason = MissingReasonEnum(self.linkage_buffer_radius_m_missing_reason)

        if self.linkage_buffer_aggregation_method is not None and not isinstance(self.linkage_buffer_aggregation_method, BufferAggregationEnum):
            self.linkage_buffer_aggregation_method = BufferAggregationEnum(self.linkage_buffer_aggregation_method)

        if self.linkage_buffer_aggregation_method_missing_reason is not None and not isinstance(self.linkage_buffer_aggregation_method_missing_reason, MissingReasonEnum):
            self.linkage_buffer_aggregation_method_missing_reason = MissingReasonEnum(self.linkage_buffer_aggregation_method_missing_reason)

        if self.linkage_max_distance_to_station_m is not None and not isinstance(self.linkage_max_distance_to_station_m, float):
            self.linkage_max_distance_to_station_m = float(self.linkage_max_distance_to_station_m)

        if self.linkage_max_distance_to_station_m_missing_reason is not None and not isinstance(self.linkage_max_distance_to_station_m_missing_reason, MissingReasonEnum):
            self.linkage_max_distance_to_station_m_missing_reason = MissingReasonEnum(self.linkage_max_distance_to_station_m_missing_reason)

        if self.geocoding_score_propagated is not None and not isinstance(self.geocoding_score_propagated, float):
            self.geocoding_score_propagated = float(self.geocoding_score_propagated)

        if self.geocoding_score_propagated_missing_reason is not None and not isinstance(self.geocoding_score_propagated_missing_reason, MissingReasonEnum):
            self.geocoding_score_propagated_missing_reason = MissingReasonEnum(self.geocoding_score_propagated_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ToolRun(YAMLRoot):
    """
    A single tool invocation that produced an output from one or more inputs: tool name and version, container image
    (where applicable), arguments, environment, run timestamp and duration, input / output hashes and row counts, and
    an optional log excerpt.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "ToolRun"
    class_model_uri: ClassVar[URIRef] = ENVAR.ToolRun

    tool_name: str = None
    tool_version: str = None
    run_timestamp_utc: Union[str, XSDDateTime] = None
    tool_description: Optional[str] = None
    container_image_repository: Optional[str] = None
    container_image_repository_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    container_image_digest: Optional[str] = None
    container_image_digest_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    run_arguments: Optional[str] = None
    run_duration_seconds: Optional[float] = None
    run_environment: Optional[str] = None
    input_file_sha256: Optional[str] = None
    input_row_count: Optional[int] = None
    output_file_sha256: Optional[str] = None
    output_row_count: Optional[int] = None
    run_log_excerpt: Optional[str] = None
    run_log_excerpt_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.tool_name):
            self.MissingRequiredField("tool_name")
        if not isinstance(self.tool_name, str):
            self.tool_name = str(self.tool_name)

        if self._is_empty(self.tool_version):
            self.MissingRequiredField("tool_version")
        if not isinstance(self.tool_version, str):
            self.tool_version = str(self.tool_version)

        if self._is_empty(self.run_timestamp_utc):
            self.MissingRequiredField("run_timestamp_utc")
        if not isinstance(self.run_timestamp_utc, XSDDateTime):
            self.run_timestamp_utc = XSDDateTime(self.run_timestamp_utc)

        if self.tool_description is not None and not isinstance(self.tool_description, str):
            self.tool_description = str(self.tool_description)

        if self.container_image_repository is not None and not isinstance(self.container_image_repository, str):
            self.container_image_repository = str(self.container_image_repository)

        if self.container_image_repository_missing_reason is not None and not isinstance(self.container_image_repository_missing_reason, MissingReasonEnum):
            self.container_image_repository_missing_reason = MissingReasonEnum(self.container_image_repository_missing_reason)

        if self.container_image_digest is not None and not isinstance(self.container_image_digest, str):
            self.container_image_digest = str(self.container_image_digest)

        if self.container_image_digest_missing_reason is not None and not isinstance(self.container_image_digest_missing_reason, MissingReasonEnum):
            self.container_image_digest_missing_reason = MissingReasonEnum(self.container_image_digest_missing_reason)

        if self.run_arguments is not None and not isinstance(self.run_arguments, str):
            self.run_arguments = str(self.run_arguments)

        if self.run_duration_seconds is not None and not isinstance(self.run_duration_seconds, float):
            self.run_duration_seconds = float(self.run_duration_seconds)

        if self.run_environment is not None and not isinstance(self.run_environment, str):
            self.run_environment = str(self.run_environment)

        if self.input_file_sha256 is not None and not isinstance(self.input_file_sha256, str):
            self.input_file_sha256 = str(self.input_file_sha256)

        if self.input_row_count is not None and not isinstance(self.input_row_count, int):
            self.input_row_count = int(self.input_row_count)

        if self.output_file_sha256 is not None and not isinstance(self.output_file_sha256, str):
            self.output_file_sha256 = str(self.output_file_sha256)

        if self.output_row_count is not None and not isinstance(self.output_row_count, int):
            self.output_row_count = int(self.output_row_count)

        if self.run_log_excerpt is not None and not isinstance(self.run_log_excerpt, str):
            self.run_log_excerpt = str(self.run_log_excerpt)

        if self.run_log_excerpt_missing_reason is not None and not isinstance(self.run_log_excerpt_missing_reason, MissingReasonEnum):
            self.run_log_excerpt_missing_reason = MissingReasonEnum(self.run_log_excerpt_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProvenanceChain(YAMLRoot):
    """
    The ordered list of all upstream `ToolRun`s whose outputs were inputs to this run, terminating in a typed root.
    Patterned after W3C PROV (`prov:wasDerivedFrom`, `prov:wasGeneratedBy`).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Bundle"]
    class_class_curie: ClassVar[str] = "prov:Bundle"
    class_name: ClassVar[str] = "ProvenanceChain"
    class_model_uri: ClassVar[URIRef] = ENVAR.ProvenanceChain

    provenance_chain_steps: Union[Union[dict, ToolRun], list[Union[dict, ToolRun]]] = None
    provenance_chain_terminus_type: Union[str, "ProvenanceChainTerminusEnum"] = None
    chain_compatibility_assertions: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.provenance_chain_steps):
            self.MissingRequiredField("provenance_chain_steps")
        self._normalize_inlined_as_list(slot_name="provenance_chain_steps", slot_type=ToolRun, key_name="tool_name", keyed=False)

        if self._is_empty(self.provenance_chain_terminus_type):
            self.MissingRequiredField("provenance_chain_terminus_type")
        if not isinstance(self.provenance_chain_terminus_type, ProvenanceChainTerminusEnum):
            self.provenance_chain_terminus_type = ProvenanceChainTerminusEnum(self.provenance_chain_terminus_type)

        if not isinstance(self.chain_compatibility_assertions, list):
            self.chain_compatibility_assertions = [self.chain_compatibility_assertions] if self.chain_compatibility_assertions is not None else []
        self.chain_compatibility_assertions = [v if isinstance(v, str) else str(v) for v in self.chain_compatibility_assertions]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DerivedHeatMetric(YAMLRoot):
    """
    Methodology slots specific to derived heat metrics (WBGT, Heat Index, UTCI, apparent temperature, heat-wave flag,
    etc.). Captures the decisions that the heat-epidemiology literature flags as critical sources of cross-study
    disagreement: which equation variant, which indoor / outdoor regime, which solar-radiation input, and -- for
    percentile-based metrics -- the reference period, scope, and seasonal window. One per record where applicable.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["DerivedHeatMetric"]
    class_class_curie: ClassVar[str] = "envar:DerivedHeatMetric"
    class_name: ClassVar[str] = "DerivedHeatMetric"
    class_model_uri: ClassVar[URIRef] = ENVAR.DerivedHeatMetric

    heat_metric_family: Union[str, "HeatMetricFamilyEnum"] = None
    indoor_outdoor: Union[str, "IndoorOutdoorEnum"] = None
    equation_variant: Optional[Union[str, "EquationVariantEnum"]] = None
    equation_variant_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    equation_inputs: Optional[Union[str, list[str]]] = empty_list()
    equation_validity_range: Optional[str] = None
    equation_validity_range_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    wind_speed_measurement_height_m: Optional[float] = None
    wind_speed_measurement_height_m_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    solar_radiation_basis: Optional[Union[str, "SolarRadiationBasisEnum"]] = None
    solar_radiation_basis_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    heat_wave_threshold_definition: Optional[Union[str, "HeatWaveThresholdDefinitionEnum"]] = None
    heat_wave_threshold_definition_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    heat_wave_threshold_specifier: Optional[str] = None
    heat_wave_min_consecutive_days: Optional[int] = None
    heat_wave_min_consecutive_days_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    percentile_reference_period_start: Optional[Union[str, XSDDate]] = None
    percentile_reference_period_start_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    percentile_reference_period_end: Optional[Union[str, XSDDate]] = None
    percentile_reference_period_end_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    percentile_reference_geographic_scope: Optional[str] = None
    percentile_reference_geographic_scope_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    percentile_reference_seasonal_window: Optional[str] = None
    percentile_reference_seasonal_window_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    metric_temporal_aggregation_rule: Optional[str] = None
    metric_temporal_aggregation_rule_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.heat_metric_family):
            self.MissingRequiredField("heat_metric_family")
        if not isinstance(self.heat_metric_family, HeatMetricFamilyEnum):
            self.heat_metric_family = HeatMetricFamilyEnum(self.heat_metric_family)

        if self._is_empty(self.indoor_outdoor):
            self.MissingRequiredField("indoor_outdoor")
        if not isinstance(self.indoor_outdoor, IndoorOutdoorEnum):
            self.indoor_outdoor = IndoorOutdoorEnum(self.indoor_outdoor)

        if self.equation_variant is not None and not isinstance(self.equation_variant, EquationVariantEnum):
            self.equation_variant = EquationVariantEnum(self.equation_variant)

        if self.equation_variant_missing_reason is not None and not isinstance(self.equation_variant_missing_reason, MissingReasonEnum):
            self.equation_variant_missing_reason = MissingReasonEnum(self.equation_variant_missing_reason)

        if not isinstance(self.equation_inputs, list):
            self.equation_inputs = [self.equation_inputs] if self.equation_inputs is not None else []
        self.equation_inputs = [v if isinstance(v, str) else str(v) for v in self.equation_inputs]

        if self.equation_validity_range is not None and not isinstance(self.equation_validity_range, str):
            self.equation_validity_range = str(self.equation_validity_range)

        if self.equation_validity_range_missing_reason is not None and not isinstance(self.equation_validity_range_missing_reason, MissingReasonEnum):
            self.equation_validity_range_missing_reason = MissingReasonEnum(self.equation_validity_range_missing_reason)

        if self.wind_speed_measurement_height_m is not None and not isinstance(self.wind_speed_measurement_height_m, float):
            self.wind_speed_measurement_height_m = float(self.wind_speed_measurement_height_m)

        if self.wind_speed_measurement_height_m_missing_reason is not None and not isinstance(self.wind_speed_measurement_height_m_missing_reason, MissingReasonEnum):
            self.wind_speed_measurement_height_m_missing_reason = MissingReasonEnum(self.wind_speed_measurement_height_m_missing_reason)

        if self.solar_radiation_basis is not None and not isinstance(self.solar_radiation_basis, SolarRadiationBasisEnum):
            self.solar_radiation_basis = SolarRadiationBasisEnum(self.solar_radiation_basis)

        if self.solar_radiation_basis_missing_reason is not None and not isinstance(self.solar_radiation_basis_missing_reason, MissingReasonEnum):
            self.solar_radiation_basis_missing_reason = MissingReasonEnum(self.solar_radiation_basis_missing_reason)

        if self.heat_wave_threshold_definition is not None and not isinstance(self.heat_wave_threshold_definition, HeatWaveThresholdDefinitionEnum):
            self.heat_wave_threshold_definition = HeatWaveThresholdDefinitionEnum(self.heat_wave_threshold_definition)

        if self.heat_wave_threshold_definition_missing_reason is not None and not isinstance(self.heat_wave_threshold_definition_missing_reason, MissingReasonEnum):
            self.heat_wave_threshold_definition_missing_reason = MissingReasonEnum(self.heat_wave_threshold_definition_missing_reason)

        if self.heat_wave_threshold_specifier is not None and not isinstance(self.heat_wave_threshold_specifier, str):
            self.heat_wave_threshold_specifier = str(self.heat_wave_threshold_specifier)

        if self.heat_wave_min_consecutive_days is not None and not isinstance(self.heat_wave_min_consecutive_days, int):
            self.heat_wave_min_consecutive_days = int(self.heat_wave_min_consecutive_days)

        if self.heat_wave_min_consecutive_days_missing_reason is not None and not isinstance(self.heat_wave_min_consecutive_days_missing_reason, MissingReasonEnum):
            self.heat_wave_min_consecutive_days_missing_reason = MissingReasonEnum(self.heat_wave_min_consecutive_days_missing_reason)

        if self.percentile_reference_period_start is not None and not isinstance(self.percentile_reference_period_start, XSDDate):
            self.percentile_reference_period_start = XSDDate(self.percentile_reference_period_start)

        if self.percentile_reference_period_start_missing_reason is not None and not isinstance(self.percentile_reference_period_start_missing_reason, MissingReasonEnum):
            self.percentile_reference_period_start_missing_reason = MissingReasonEnum(self.percentile_reference_period_start_missing_reason)

        if self.percentile_reference_period_end is not None and not isinstance(self.percentile_reference_period_end, XSDDate):
            self.percentile_reference_period_end = XSDDate(self.percentile_reference_period_end)

        if self.percentile_reference_period_end_missing_reason is not None and not isinstance(self.percentile_reference_period_end_missing_reason, MissingReasonEnum):
            self.percentile_reference_period_end_missing_reason = MissingReasonEnum(self.percentile_reference_period_end_missing_reason)

        if self.percentile_reference_geographic_scope is not None and not isinstance(self.percentile_reference_geographic_scope, str):
            self.percentile_reference_geographic_scope = str(self.percentile_reference_geographic_scope)

        if self.percentile_reference_geographic_scope_missing_reason is not None and not isinstance(self.percentile_reference_geographic_scope_missing_reason, MissingReasonEnum):
            self.percentile_reference_geographic_scope_missing_reason = MissingReasonEnum(self.percentile_reference_geographic_scope_missing_reason)

        if self.percentile_reference_seasonal_window is not None and not isinstance(self.percentile_reference_seasonal_window, str):
            self.percentile_reference_seasonal_window = str(self.percentile_reference_seasonal_window)

        if self.percentile_reference_seasonal_window_missing_reason is not None and not isinstance(self.percentile_reference_seasonal_window_missing_reason, MissingReasonEnum):
            self.percentile_reference_seasonal_window_missing_reason = MissingReasonEnum(self.percentile_reference_seasonal_window_missing_reason)

        if self.metric_temporal_aggregation_rule is not None and not isinstance(self.metric_temporal_aggregation_rule, str):
            self.metric_temporal_aggregation_rule = str(self.metric_temporal_aggregation_rule)

        if self.metric_temporal_aggregation_rule_missing_reason is not None and not isinstance(self.metric_temporal_aggregation_rule_missing_reason, MissingReasonEnum):
            self.metric_temporal_aggregation_rule_missing_reason = MissingReasonEnum(self.metric_temporal_aggregation_rule_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OmopLinkage(YAMLRoot):
    """
    Hooks the sidecar uses to interface with OMOP (or BDC, or another) health-data layer. These are *not* clinical
    metadata — they are the hooks the exposure record needs to be findable from the health side. One per record.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["OmopLinkage"]
    class_class_curie: ClassVar[str] = "envar:OmopLinkage"
    class_name: ClassVar[str] = "OmopLinkage"
    class_model_uri: ClassVar[URIRef] = ENVAR.OmopLinkage

    omop_external_exposure_link_field: str = None
    phi_status: Union[str, "PhiStatusEnum"] = None
    bdc_link_field: Optional[str] = None
    bdc_link_field_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    cohort_size_anchored: Optional[int] = None
    cohort_size_anchored_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.omop_external_exposure_link_field):
            self.MissingRequiredField("omop_external_exposure_link_field")
        if not isinstance(self.omop_external_exposure_link_field, str):
            self.omop_external_exposure_link_field = str(self.omop_external_exposure_link_field)

        if self._is_empty(self.phi_status):
            self.MissingRequiredField("phi_status")
        if not isinstance(self.phi_status, PhiStatusEnum):
            self.phi_status = PhiStatusEnum(self.phi_status)

        if self.bdc_link_field is not None and not isinstance(self.bdc_link_field, str):
            self.bdc_link_field = str(self.bdc_link_field)

        if self.bdc_link_field_missing_reason is not None and not isinstance(self.bdc_link_field_missing_reason, MissingReasonEnum):
            self.bdc_link_field_missing_reason = MissingReasonEnum(self.bdc_link_field_missing_reason)

        if self.cohort_size_anchored is not None and not isinstance(self.cohort_size_anchored, int):
            self.cohort_size_anchored = int(self.cohort_size_anchored)

        if self.cohort_size_anchored_missing_reason is not None and not isinstance(self.cohort_size_anchored_missing_reason, MissingReasonEnum):
            self.cohort_size_anchored_missing_reason = MissingReasonEnum(self.cohort_size_anchored_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DepositMetadata(YAMLRoot):
    """
    Deposit-time slots required when the sidecar travels alongside a published FAIR object (Zenodo / Dryad / C-HER /
    etc.). Most slots are pulled from other modules; this class names the required-for-deposit subset and adds a few
    deposit-specific slots.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["DepositMetadata"]
    class_class_curie: ClassVar[str] = "envar:DepositMetadata"
    class_name: ClassVar[str] = "DepositMetadata"
    class_model_uri: ClassVar[URIRef] = ENVAR.DepositMetadata

    deposit_doi: Optional[str] = None
    deposit_doi_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    deposit_repository: Optional[Union[str, "DepositRepositoryEnum"]] = None
    deposit_repository_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None
    deposit_license_spdx: Optional[str] = None
    deposit_redistribution_constraints_inherited: Optional[Union[str, list[str]]] = empty_list()
    recommended_citation: Optional[str] = None
    dcat_distribution_url: Optional[Union[str, URI]] = None
    dcat_distribution_url_missing_reason: Optional[Union[str, "MissingReasonEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.deposit_doi is not None and not isinstance(self.deposit_doi, str):
            self.deposit_doi = str(self.deposit_doi)

        if self.deposit_doi_missing_reason is not None and not isinstance(self.deposit_doi_missing_reason, MissingReasonEnum):
            self.deposit_doi_missing_reason = MissingReasonEnum(self.deposit_doi_missing_reason)

        if self.deposit_repository is not None and not isinstance(self.deposit_repository, DepositRepositoryEnum):
            self.deposit_repository = DepositRepositoryEnum(self.deposit_repository)

        if self.deposit_repository_missing_reason is not None and not isinstance(self.deposit_repository_missing_reason, MissingReasonEnum):
            self.deposit_repository_missing_reason = MissingReasonEnum(self.deposit_repository_missing_reason)

        if self.deposit_license_spdx is not None and not isinstance(self.deposit_license_spdx, str):
            self.deposit_license_spdx = str(self.deposit_license_spdx)

        if not isinstance(self.deposit_redistribution_constraints_inherited, list):
            self.deposit_redistribution_constraints_inherited = [self.deposit_redistribution_constraints_inherited] if self.deposit_redistribution_constraints_inherited is not None else []
        self.deposit_redistribution_constraints_inherited = [v if isinstance(v, str) else str(v) for v in self.deposit_redistribution_constraints_inherited]

        if self.recommended_citation is not None and not isinstance(self.recommended_citation, str):
            self.recommended_citation = str(self.recommended_citation)

        if self.dcat_distribution_url is not None and not isinstance(self.dcat_distribution_url, URI):
            self.dcat_distribution_url = URI(self.dcat_distribution_url)

        if self.dcat_distribution_url_missing_reason is not None and not isinstance(self.dcat_distribution_url_missing_reason, MissingReasonEnum):
            self.dcat_distribution_url_missing_reason = MissingReasonEnum(self.dcat_distribution_url_missing_reason)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnvironmentalExposureRecord(YAMLRoot):
    """
    A single environmental-exposure record sidecar: the complete metadata graph that travels alongside a value (or
    value series) emitted by an upstream tool. Composes variable identity, spatial / temporal reference, source
    dataset, exposure model, uncertainty, linkage, tool run, provenance chain, optional derived-heat-metric
    methodology, OMOP linkage hooks, and FAIR-deposit metadata.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["EnvironmentalExposureRecord"]
    class_class_curie: ClassVar[str] = "envar:EnvironmentalExposureRecord"
    class_name: ClassVar[str] = "EnvironmentalExposureRecord"
    class_model_uri: ClassVar[URIRef] = ENVAR.EnvironmentalExposureRecord

    subject: str = None
    observation_type: Union[dict, VariableIdentity] = None
    location: Union[dict, SpatialReference] = None
    temporality: Union[dict, TemporalReference] = None
    methodology: Union[dict, ExposureModel] = None
    observation_result: Union[dict, "ValueMicroschemaDefinition"] = None
    schema_version: str = None
    provenance_id: str = None
    source_dataset: Union[dict, SourceDataset] = None
    linkage_method: Union[dict, LinkageMethod] = None
    tool_run: Union[dict, ToolRun] = None
    provenance_chain: Union[dict, ProvenanceChain] = None
    omop_linkage: Union[dict, OmopLinkage] = None
    uncertainty: Optional[Union[dict, Uncertainty]] = None
    derived_heat_metric: Optional[Union[dict, DerivedHeatMetric]] = None
    deposit_metadata: Optional[Union[dict, DepositMetadata]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, str):
            self.subject = str(self.subject)

        if self._is_empty(self.observation_type):
            self.MissingRequiredField("observation_type")
        if not isinstance(self.observation_type, VariableIdentity):
            self.observation_type = VariableIdentity(**as_dict(self.observation_type))

        if self._is_empty(self.location):
            self.MissingRequiredField("location")
        if not isinstance(self.location, SpatialReference):
            self.location = SpatialReference(**as_dict(self.location))

        if self._is_empty(self.temporality):
            self.MissingRequiredField("temporality")
        if not isinstance(self.temporality, TemporalReference):
            self.temporality = TemporalReference(**as_dict(self.temporality))

        if self._is_empty(self.methodology):
            self.MissingRequiredField("methodology")
        if not isinstance(self.methodology, ExposureModel):
            self.methodology = ExposureModel(**as_dict(self.methodology))

        if self._is_empty(self.observation_result):
            self.MissingRequiredField("observation_result")
        if not isinstance(self.observation_result, ValueMicroschemaDefinition):
            self.observation_result = ValueMicroschemaDefinition()

        if self._is_empty(self.schema_version):
            self.MissingRequiredField("schema_version")
        if not isinstance(self.schema_version, str):
            self.schema_version = str(self.schema_version)

        if self._is_empty(self.provenance_id):
            self.MissingRequiredField("provenance_id")
        if not isinstance(self.provenance_id, str):
            self.provenance_id = str(self.provenance_id)

        if self._is_empty(self.source_dataset):
            self.MissingRequiredField("source_dataset")
        if not isinstance(self.source_dataset, SourceDataset):
            self.source_dataset = SourceDataset(**as_dict(self.source_dataset))

        if self._is_empty(self.linkage_method):
            self.MissingRequiredField("linkage_method")
        if not isinstance(self.linkage_method, LinkageMethod):
            self.linkage_method = LinkageMethod(**as_dict(self.linkage_method))

        if self._is_empty(self.tool_run):
            self.MissingRequiredField("tool_run")
        if not isinstance(self.tool_run, ToolRun):
            self.tool_run = ToolRun(**as_dict(self.tool_run))

        if self._is_empty(self.provenance_chain):
            self.MissingRequiredField("provenance_chain")
        if not isinstance(self.provenance_chain, ProvenanceChain):
            self.provenance_chain = ProvenanceChain(**as_dict(self.provenance_chain))

        if self._is_empty(self.omop_linkage):
            self.MissingRequiredField("omop_linkage")
        if not isinstance(self.omop_linkage, OmopLinkage):
            self.omop_linkage = OmopLinkage(**as_dict(self.omop_linkage))

        if self.uncertainty is not None and not isinstance(self.uncertainty, Uncertainty):
            self.uncertainty = Uncertainty(**as_dict(self.uncertainty))

        if self.derived_heat_metric is not None and not isinstance(self.derived_heat_metric, DerivedHeatMetric):
            self.derived_heat_metric = DerivedHeatMetric(**as_dict(self.derived_heat_metric))

        if self.deposit_metadata is not None and not isinstance(self.deposit_metadata, DepositMetadata):
            self.deposit_metadata = DepositMetadata(**as_dict(self.deposit_metadata))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DailyMaxTemperatureRecord(EnvironmentalExposureRecord):
    """
    Canonical record for daily maximum 2 m air temperature (Tmax). Pins `cf_standard_name = air_temperature`,
    `cf_cell_methods = "time: maximum"`, `units_ucum = Cel`, `value_data_type = continuous_numeric`.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["DailyMaxTemperatureRecord"]
    class_class_curie: ClassVar[str] = "envar:DailyMaxTemperatureRecord"
    class_name: ClassVar[str] = "DailyMaxTemperatureRecord"
    class_model_uri: ClassVar[URIRef] = ENVAR.DailyMaxTemperatureRecord

    subject: str = None
    observation_type: Union[dict, VariableIdentity] = None
    location: Union[dict, SpatialReference] = None
    temporality: Union[dict, TemporalReference] = None
    methodology: Union[dict, ExposureModel] = None
    observation_result: Union[dict, "ValueMicroschemaDefinition"] = None
    schema_version: str = None
    provenance_id: str = None
    source_dataset: Union[dict, SourceDataset] = None
    linkage_method: Union[dict, LinkageMethod] = None
    tool_run: Union[dict, ToolRun] = None
    provenance_chain: Union[dict, ProvenanceChain] = None
    omop_linkage: Union[dict, OmopLinkage] = None

@dataclass(repr=False)
class DailyMinTemperatureRecord(EnvironmentalExposureRecord):
    """
    Canonical record for daily minimum 2 m air temperature (Tmin). Pins `cf_standard_name = air_temperature`,
    `cf_cell_methods = "time: minimum"`, `units_ucum = Cel`, `value_data_type = continuous_numeric`.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["DailyMinTemperatureRecord"]
    class_class_curie: ClassVar[str] = "envar:DailyMinTemperatureRecord"
    class_name: ClassVar[str] = "DailyMinTemperatureRecord"
    class_model_uri: ClassVar[URIRef] = ENVAR.DailyMinTemperatureRecord

    subject: str = None
    observation_type: Union[dict, VariableIdentity] = None
    location: Union[dict, SpatialReference] = None
    temporality: Union[dict, TemporalReference] = None
    methodology: Union[dict, ExposureModel] = None
    observation_result: Union[dict, "ValueMicroschemaDefinition"] = None
    schema_version: str = None
    provenance_id: str = None
    source_dataset: Union[dict, SourceDataset] = None
    linkage_method: Union[dict, LinkageMethod] = None
    tool_run: Union[dict, ToolRun] = None
    provenance_chain: Union[dict, ProvenanceChain] = None
    omop_linkage: Union[dict, OmopLinkage] = None

@dataclass(repr=False)
class WetBulbGlobeTemperatureOutdoorRecord(EnvironmentalExposureRecord):
    """
    Canonical record for outdoor WBGT under the Liljegren 2008 formulation. Pins `heat_metric_family = wbgt_outdoor`,
    `equation_variant = liljegren_2008`, `indoor_outdoor = outdoor`, `units_ucum = Cel`, `value_data_type =
    continuous_numeric`.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["WetBulbGlobeTemperatureOutdoorRecord"]
    class_class_curie: ClassVar[str] = "envar:WetBulbGlobeTemperatureOutdoorRecord"
    class_name: ClassVar[str] = "WetBulbGlobeTemperatureOutdoorRecord"
    class_model_uri: ClassVar[URIRef] = ENVAR.WetBulbGlobeTemperatureOutdoorRecord

    subject: str = None
    observation_type: Union[dict, VariableIdentity] = None
    location: Union[dict, SpatialReference] = None
    temporality: Union[dict, TemporalReference] = None
    methodology: Union[dict, ExposureModel] = None
    observation_result: Union[dict, "ValueMicroschemaDefinition"] = None
    schema_version: str = None
    provenance_id: str = None
    source_dataset: Union[dict, SourceDataset] = None
    linkage_method: Union[dict, LinkageMethod] = None
    tool_run: Union[dict, ToolRun] = None
    provenance_chain: Union[dict, ProvenanceChain] = None
    omop_linkage: Union[dict, OmopLinkage] = None
    derived_heat_metric: Union[dict, DerivedHeatMetric] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.derived_heat_metric):
            self.MissingRequiredField("derived_heat_metric")
        if not isinstance(self.derived_heat_metric, DerivedHeatMetric):
            self.derived_heat_metric = DerivedHeatMetric(**as_dict(self.derived_heat_metric))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExtremeHeatDayFlagRecord(EnvironmentalExposureRecord):
    """
    Canonical record for a daily binary extreme-heat-day flag, defined against a local 95th-percentile Tmax baseline.
    Pins `heat_metric_family = heat_wave_flag`, `value_data_type = binary_flag`, and requires the
    percentile-reference-period slots in DerivedHeatMetric to be populated.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ENVAR["ExtremeHeatDayFlagRecord"]
    class_class_curie: ClassVar[str] = "envar:ExtremeHeatDayFlagRecord"
    class_name: ClassVar[str] = "ExtremeHeatDayFlagRecord"
    class_model_uri: ClassVar[URIRef] = ENVAR.ExtremeHeatDayFlagRecord

    subject: str = None
    observation_type: Union[dict, VariableIdentity] = None
    location: Union[dict, SpatialReference] = None
    temporality: Union[dict, TemporalReference] = None
    methodology: Union[dict, ExposureModel] = None
    observation_result: Union[dict, "ValueMicroschemaDefinition"] = None
    schema_version: str = None
    provenance_id: str = None
    source_dataset: Union[dict, SourceDataset] = None
    linkage_method: Union[dict, LinkageMethod] = None
    tool_run: Union[dict, ToolRun] = None
    provenance_chain: Union[dict, ProvenanceChain] = None
    omop_linkage: Union[dict, OmopLinkage] = None
    derived_heat_metric: Union[dict, DerivedHeatMetric] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.derived_heat_metric):
            self.MissingRequiredField("derived_heat_metric")
        if not isinstance(self.derived_heat_metric, DerivedHeatMetric):
            self.derived_heat_metric = DerivedHeatMetric(**as_dict(self.derived_heat_metric))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MicroschemaDefinition(YAMLRoot):
    """
    A metaclass for classes that conform to the Microschema profile. Classes that instantiate this are designed for
    inline composition.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["linkml-microschema-profile/MicroschemaDefinition"]
    class_class_curie: ClassVar[str] = "linkml:linkml-microschema-profile/MicroschemaDefinition"
    class_name: ClassVar[str] = "MicroschemaDefinition"
    class_model_uri: ClassVar[URIRef] = ENVAR.MicroschemaDefinition

    subject: str = None
    observation_type: str = None
    location: str = None
    temporality: str = None
    methodology: str = None
    observation_result: Union[dict, "ValueMicroschemaDefinition"] = None
    profile_version: Optional[str] = None
    domain_of_use: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, str):
            self.subject = str(self.subject)

        if self._is_empty(self.observation_type):
            self.MissingRequiredField("observation_type")
        if not isinstance(self.observation_type, str):
            self.observation_type = str(self.observation_type)

        if self._is_empty(self.location):
            self.MissingRequiredField("location")
        if not isinstance(self.location, str):
            self.location = str(self.location)

        if self._is_empty(self.temporality):
            self.MissingRequiredField("temporality")
        if not isinstance(self.temporality, str):
            self.temporality = str(self.temporality)

        if self._is_empty(self.methodology):
            self.MissingRequiredField("methodology")
        if not isinstance(self.methodology, str):
            self.methodology = str(self.methodology)

        if self._is_empty(self.observation_result):
            self.MissingRequiredField("observation_result")
        if not isinstance(self.observation_result, ValueMicroschemaDefinition):
            self.observation_result = ValueMicroschemaDefinition()

        if self.profile_version is not None and not isinstance(self.profile_version, str):
            self.profile_version = str(self.profile_version)

        if not isinstance(self.domain_of_use, list):
            self.domain_of_use = [self.domain_of_use] if self.domain_of_use is not None else []
        self.domain_of_use = [v if isinstance(v, str) else str(v) for v in self.domain_of_use]

        super().__post_init__(**kwargs)


class ValueMicroschemaDefinition(YAMLRoot):
    """
    A microschema representing a typed value with optional unit/system. Examples: Quantity, Timepoint, CodedValue,
    Range. This is the range for observation result
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["linkml-microschema-profile/ValueMicroschemaDefinition"]
    class_class_curie: ClassVar[str] = "linkml:linkml-microschema-profile/ValueMicroschemaDefinition"
    class_name: ClassVar[str] = "ValueMicroschemaDefinition"
    class_model_uri: ClassVar[URIRef] = ENVAR.ValueMicroschemaDefinition


@dataclass(repr=False)
class Quantity(YAMLRoot):
    """
    A numerical value with unit
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["linkml-microschema-profile/Quantity"]
    class_class_curie: ClassVar[str] = "linkml:linkml-microschema-profile/Quantity"
    class_name: ClassVar[str] = "Quantity"
    class_model_uri: ClassVar[URIRef] = ENVAR.Quantity

    quantity_value: Decimal = None
    quantity_unit: Union[str, URIorCURIE] = None
    comparator: Optional[Union[str, "ComparatorEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.quantity_value):
            self.MissingRequiredField("quantity_value")
        if not isinstance(self.quantity_value, Decimal):
            self.quantity_value = Decimal(self.quantity_value)

        if self._is_empty(self.quantity_unit):
            self.MissingRequiredField("quantity_unit")
        if not isinstance(self.quantity_unit, URIorCURIE):
            self.quantity_unit = URIorCURIE(self.quantity_unit)

        if self.comparator is not None and not isinstance(self.comparator, ComparatorEnum):
            self.comparator = ComparatorEnum(self.comparator)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Timepoint(YAMLRoot):
    """
    A point in time, potentially relative
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["linkml-microschema-profile/Timepoint"]
    class_class_curie: ClassVar[str] = "linkml:linkml-microschema-profile/Timepoint"
    class_name: ClassVar[str] = "Timepoint"
    class_model_uri: ClassVar[URIRef] = ENVAR.Timepoint

    datetime: Optional[Union[str, XSDDateTime]] = None
    relative_to_event: Optional[Union[str, URIorCURIE]] = None
    offset: Optional[Union[dict, Quantity]] = None
    subject_age: Optional[Union[dict, Quantity]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.datetime is not None and not isinstance(self.datetime, XSDDateTime):
            self.datetime = XSDDateTime(self.datetime)

        if self.relative_to_event is not None and not isinstance(self.relative_to_event, URIorCURIE):
            self.relative_to_event = URIorCURIE(self.relative_to_event)

        if self.offset is not None and not isinstance(self.offset, Quantity):
            self.offset = Quantity(**as_dict(self.offset))

        if self.subject_age is not None and not isinstance(self.subject_age, Quantity):
            self.subject_age = Quantity(**as_dict(self.subject_age))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TimeInterval(YAMLRoot):
    """
    A period between two timepoints
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["linkml-microschema-profile/TimeInterval"]
    class_class_curie: ClassVar[str] = "linkml:linkml-microschema-profile/TimeInterval"
    class_name: ClassVar[str] = "TimeInterval"
    class_model_uri: ClassVar[URIRef] = ENVAR.TimeInterval

    interval_start: Optional[Union[dict, Timepoint]] = None
    interval_end: Optional[Union[dict, Timepoint]] = None
    duration: Optional[Union[dict, Quantity]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.interval_start is not None and not isinstance(self.interval_start, Timepoint):
            self.interval_start = Timepoint(**as_dict(self.interval_start))

        if self.interval_end is not None and not isinstance(self.interval_end, Timepoint):
            self.interval_end = Timepoint(**as_dict(self.interval_end))

        if self.duration is not None and not isinstance(self.duration, Quantity):
            self.duration = Quantity(**as_dict(self.duration))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CodedValue(YAMLRoot):
    """
    A value from a controlled vocabulary
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LINKML["linkml-microschema-profile/CodedValue"]
    class_class_curie: ClassVar[str] = "linkml:linkml-microschema-profile/CodedValue"
    class_name: ClassVar[str] = "CodedValue"
    class_model_uri: ClassVar[URIRef] = ENVAR.CodedValue

    code: Union[str, URIorCURIE] = None
    code_label: Optional[str] = None
    code_system: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.code):
            self.MissingRequiredField("code")
        if not isinstance(self.code, URIorCURIE):
            self.code = URIorCURIE(self.code)

        if self.code_label is not None and not isinstance(self.code_label, str):
            self.code_label = str(self.code_label)

        if self.code_system is not None and not isinstance(self.code_system, URIorCURIE):
            self.code_system = URIorCURIE(self.code_system)

        super().__post_init__(**kwargs)


# Enumerations
class MissingReasonEnum(EnumDefinitionImpl):
    """
    Controlled reasons that a slot value is missing. Distinguishes a slot the source genuinely does not produce
    (terminal) from one we could extract but did not (roadmap) from a bug in the chain.
    """
    not_provided_by_source = PermissibleValue(
        text="not_provided_by_source",
        description="Source product does not produce this information. Terminal.")
    available_but_not_extracted = PermissibleValue(
        text="available_but_not_extracted",
        description="Source produces this information but the current pipeline does not surface it. Roadmap item.")
    upstream_data_not_propagated = PermissibleValue(
        text="upstream_data_not_propagated",
        description="""An upstream tool emitted this information but the current pipeline dropped it on the way through. Bug.""")
    under_investigation = PermissibleValue(
        text="under_investigation",
        description="We are working on populating this slot.")
    not_applicable = PermissibleValue(
        text="not_applicable",
        description="This slot does not apply to this variable / record.")

    _defn = EnumDefinition(
        name="MissingReasonEnum",
        description="""Controlled reasons that a slot value is missing. Distinguishes a slot the source genuinely does not produce (terminal) from one we could extract but did not (roadmap) from a bug in the chain.""",
    )

class DataTypeEnum(EnumDefinitionImpl):
    """
    The data type of an exposure value.
    """
    continuous_numeric = PermissibleValue(
        text="continuous_numeric",
        description="Continuous numeric value (e.g. temperature in °C).")
    categorical = PermissibleValue(
        text="categorical",
        description="Categorical value (e.g. land-use class).")
    binary_flag = PermissibleValue(
        text="binary_flag",
        description="Binary flag (e.g. extreme-heat-day yes/no).")
    count = PermissibleValue(
        text="count",
        description="Integer count (e.g. consecutive heat days).")
    event_marker = PermissibleValue(
        text="event_marker",
        description="Date-stamped event (e.g. wildfire smoke plume).")

    _defn = EnumDefinition(
        name="DataTypeEnum",
        description="The data type of an exposure value.",
    )

class OmopConceptStatusEnum(EnumDefinitionImpl):
    """
    Status of a variable's representation in the OHDSI Standardised Vocabulary. `existing` = a concept_id is available
    now; `proposed` = submission in flight; `gap` = no concept exists and none is proposed.
    """
    existing = PermissibleValue(
        text="existing",
        description="A concept_id is available in the standard OHDSI vocabulary.")
    proposed = PermissibleValue(
        text="proposed",
        description="A concept submission is in flight.")
    gap = PermissibleValue(
        text="gap",
        description="No concept exists yet and none is yet proposed.")

    _defn = EnumDefinition(
        name="OmopConceptStatusEnum",
        description="""Status of a variable's representation in the OHDSI Standardised Vocabulary. `existing` = a concept_id is available now; `proposed` = submission in flight; `gap` = no concept exists and none is proposed.""",
    )

class ExtractionMethodEnum(EnumDefinitionImpl):
    """
    How a gridded value was extracted at a target location.
    """
    nearest_cell = PermissibleValue(
        text="nearest_cell",
        description="Take the value from the single nearest grid cell.")
    bilinear = PermissibleValue(
        text="bilinear",
        description="Bilinear interpolation of the four nearest cells.")
    inverse_distance_weighted_4_nearest_cells = PermissibleValue(
        text="inverse_distance_weighted_4_nearest_cells",
        description="""Inverse-distance-weighted average of the 4 nearest cells. Default for DeGAUSS `daymet` and `narr`.""")
    area_weighted_polygon_mean = PermissibleValue(
        text="area_weighted_polygon_mean",
        description="Area-weighted mean of cells overlapping a polygon.")
    population_weighted_mean = PermissibleValue(
        text="population_weighted_mean",
        description="Population-weighted mean over a target geography (e.g. tract).")
    point_station_lookup = PermissibleValue(
        text="point_station_lookup",
        description="Direct lookup at a point station observation.")

    _defn = EnumDefinition(
        name="ExtractionMethodEnum",
        description="How a gridded value was extracted at a target location.",
    )

class TargetGeographyTypeEnum(EnumDefinitionImpl):
    """
    Geographic unit the exposure is attached to.
    """
    point_residence = PermissibleValue(
        text="point_residence",
        description="Attached to the patient's exact lat / lon.")
    census_block_group = PermissibleValue(
        text="census_block_group",
        description="US Census Block Group.")
    census_tract = PermissibleValue(
        text="census_tract",
        description="US Census Tract.")
    zcta = PermissibleValue(
        text="zcta",
        description="ZIP Code Tabulation Area.")
    county = PermissibleValue(
        text="county",
        description="US County (FIPS).")
    h3_hex = PermissibleValue(
        text="h3_hex",
        description="H3 hexagon at some resolution. Resolution captured separately.")
    public_water_system = PermissibleValue(
        text="public_water_system",
        description="Public water system service area polygon.")

    _defn = EnumDefinition(
        name="TargetGeographyTypeEnum",
        description="Geographic unit the exposure is attached to.",
    )

class TemporalResolutionEnum(EnumDefinitionImpl):
    """
    Native temporal grain of the source product.
    """
    instantaneous = PermissibleValue(
        text="instantaneous",
        description="Instantaneous snapshot at a timestamp.")
    hourly = PermissibleValue(
        text="hourly",
        description="One value per hour.")
    daily = PermissibleValue(
        text="daily",
        description="One value per day.")
    monthly = PermissibleValue(
        text="monthly",
        description="One value per calendar month.")
    seasonal = PermissibleValue(
        text="seasonal",
        description="One value per season (3-month window).")
    annual = PermissibleValue(
        text="annual",
        description="One value per year.")

    _defn = EnumDefinition(
        name="TemporalResolutionEnum",
        description="Native temporal grain of the source product.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "3_hourly",
            PermissibleValue(
                text="3_hourly",
                description="One value per 3-hour window (NARR sub-daily)."))

class TemporalAggregationMethodEnum(EnumDefinitionImpl):
    """
    How sub-period values were aggregated. CF `cell_methods` aligned.
    """
    mean = PermissibleValue(
        text="mean",
        description="Arithmetic mean over the window.")
    maximum = PermissibleValue(
        text="maximum",
        description="Maximum over the window. `time: maximum` in CF.")
    minimum = PermissibleValue(
        text="minimum",
        description="Minimum over the window. `time: minimum` in CF.")
    sum = PermissibleValue(
        text="sum",
        description="Sum over the window.")
    percentile = PermissibleValue(
        text="percentile",
        description="A percentile of the values in the window.")
    point_in_time = PermissibleValue(
        text="point_in_time",
        description="A point-in-time sample with no aggregation applied.")

    _defn = EnumDefinition(
        name="TemporalAggregationMethodEnum",
        description="How sub-period values were aggregated. CF `cell_methods` aligned.",
    )

class DayBoundaryConventionEnum(EnumDefinitionImpl):
    """
    Where the 24-hour day window starts. The single most-omitted slot in the environmental-health literature.
    """
    local_midnight = PermissibleValue(
        text="local_midnight",
        description="Day starts at local midnight at the target location. Daymet convention.")
    utc_midnight = PermissibleValue(
        text="utc_midnight",
        description="Day starts at 00:00 UTC. NARR / ERA5 sub-daily are computed against this.")
    solar_noon_centered = PermissibleValue(
        text="solar_noon_centered",
        description="24-hour window centered on local solar noon.")
    observation_dependent = PermissibleValue(
        text="observation_dependent",
        description="""Day boundary follows whatever the underlying observation network uses (e.g. weather-station local custom).""")

    _defn = EnumDefinition(
        name="DayBoundaryConventionEnum",
        description="""Where the 24-hour day window starts. The single most-omitted slot in the environmental-health literature.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "24h_ending_1200_GMT",
            PermissibleValue(
                text="24h_ending_1200_GMT",
                description="""24-hour window ending 12:00 GMT, used by PRISM and historically common in US station-network products."""))

class CalendarEnum(EnumDefinitionImpl):
    """
    CF `calendar` values.
    """
    gregorian = PermissibleValue(
        text="gregorian",
        description="Standard mixed Julian / Gregorian calendar (default).")
    noleap = PermissibleValue(
        text="noleap",
        description="365-day calendar with no leap days. Common in climate-model output.")
    all_leap = PermissibleValue(
        text="all_leap",
        description="366-day calendar with all years leap.")
    julian = PermissibleValue(
        text="julian",
        description="Proleptic Julian calendar.")
    proleptic_gregorian = PermissibleValue(
        text="proleptic_gregorian",
        description="Proleptic Gregorian calendar.")

    _defn = EnumDefinition(
        name="CalendarEnum",
        description="CF `calendar` values.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "360_day",
            PermissibleValue(
                text="360_day",
                description="12 months of 30 days each. Common in some climate-model outputs."))

class LagAlignmentEnum(EnumDefinitionImpl):
    """
    Whether the values have been pre-aligned to a clinical event window in this ETL. Companion slot
    `lag_alignment_specifier` captures the concrete lag pattern (e.g. `lag_3_days`, `distributed_lag_0_21`).
    """
    none = PermissibleValue(
        text="none",
        description="No lag alignment applied; values are at native dates.")
    lag_n_days = PermissibleValue(
        text="lag_n_days",
        description="A single-day lag of N days has been applied. Concrete N captured in `lag_alignment_specifier`.")
    distributed_lag = PermissibleValue(
        text="distributed_lag",
        description="""A distributed lag over a range of days has been applied. Range captured in `lag_alignment_specifier` (e.g. `\"0-21\"`).""")

    _defn = EnumDefinition(
        name="LagAlignmentEnum",
        description="""Whether the values have been pre-aligned to a clinical event window in this ETL. Companion slot `lag_alignment_specifier` captures the concrete lag pattern (e.g. `lag_3_days`, `distributed_lag_0_21`).""",
    )

class HomogenisationStatusEnum(EnumDefinitionImpl):
    """
    For station-based products, the homogenisation status of values across the record period.
    """
    homogenised = PermissibleValue(
        text="homogenised",
        description="Values have been homogenised against breakpoints.")
    not_homogenised = PermissibleValue(
        text="not_homogenised",
        description="Values are as-observed, with no homogenisation applied.")
    partial = PermissibleValue(
        text="partial",
        description="Partial homogenisation has been applied.")

    _defn = EnumDefinition(
        name="HomogenisationStatusEnum",
        description="For station-based products, the homogenisation status of values across the record period.",
    )

class SourceNativeFormatEnum(EnumDefinitionImpl):
    """
    Format the source ships in.
    """
    HDF5 = PermissibleValue(
        text="HDF5",
        description="Hierarchical Data Format version 5.")
    GeoTIFF = PermissibleValue(
        text="GeoTIFF",
        description="GeoTIFF raster format.")
    CSV_station_observations = PermissibleValue(
        text="CSV_station_observations",
        description="CSV file of station observations.")
    Zarr = PermissibleValue(
        text="Zarr",
        description="Zarr cloud-optimised array format.")
    Parquet = PermissibleValue(
        text="Parquet",
        description="Apache Parquet tabular format.")

    _defn = EnumDefinition(
        name="SourceNativeFormatEnum",
        description="Format the source ships in.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "NetCDF-4_CF",
            PermissibleValue(
                text="NetCDF-4_CF",
                description="NetCDF version 4 with CF Conventions metadata."))
        setattr(cls, "GRIB-1",
            PermissibleValue(
                text="GRIB-1",
                description="WMO GRIB-1 format."))
        setattr(cls, "GRIB-2",
            PermissibleValue(
                text="GRIB-2",
                description="WMO GRIB-2 format."))

class ExposureModelTypeEnum(EnumDefinitionImpl):
    """
    The class of model that produced the values.
    """
    direct_measurement = PermissibleValue(
        text="direct_measurement",
        description="Direct instrument observation.")
    spatial_interpolation = PermissibleValue(
        text="spatial_interpolation",
        description="Station observations interpolated to a grid (Daymet).")
    reanalysis = PermissibleValue(
        text="reanalysis",
        description="Data-assimilation reanalysis (NARR, ERA5).")
    statistical_blend = PermissibleValue(
        text="statistical_blend",
        description="Blend of multiple sources (GridMET = PRISM + NLDAS-2).")
    chemical_transport_model = PermissibleValue(
        text="chemical_transport_model",
        description="Deterministic chemical transport model (CMAQ, GEOS-Chem).")
    ensemble_machine_learning = PermissibleValue(
        text="ensemble_machine_learning",
        description="Ensemble ML model (Di et al. PM2.5).")
    single_machine_learning = PermissibleValue(
        text="single_machine_learning",
        description="Single ML model (Brokamp PM2.5).")
    equation_derived = PermissibleValue(
        text="equation_derived",
        description="Derived analytically from other variables via an equation.")
    satellite_retrieval = PermissibleValue(
        text="satellite_retrieval",
        description="Satellite-based retrieval algorithm.")

    _defn = EnumDefinition(
        name="ExposureModelTypeEnum",
        description="The class of model that produced the values.",
    )

class BiasCorrectionAppliedEnum(EnumDefinitionImpl):
    """
    Whether and how bias correction has been applied.
    """
    none = PermissibleValue(
        text="none",
        description="No bias correction applied.")
    quantile_mapping = PermissibleValue(
        text="quantile_mapping",
        description="Quantile-mapping bias correction.")
    linear_scaling = PermissibleValue(
        text="linear_scaling",
        description="Linear scaling bias correction.")
    delta_method = PermissibleValue(
        text="delta_method",
        description="Delta-method bias correction.")
    other = PermissibleValue(
        text="other",
        description="Some other bias-correction method has been applied.")

    _defn = EnumDefinition(
        name="BiasCorrectionAppliedEnum",
        description="Whether and how bias correction has been applied.",
    )

class UncertaintyTypeEnum(EnumDefinitionImpl):
    """
    Kind of per-value uncertainty.
    """
    standard_error = PermissibleValue(
        text="standard_error",
        description="Standard error of the value.")
    prediction_interval = PermissibleValue(
        text="prediction_interval",
        description="""Prediction interval; the percentile (e.g. 95 %) is captured implicitly in the producer documentation.""")
    ensemble_std_dev = PermissibleValue(
        text="ensemble_std_dev",
        description="Standard deviation across ensemble members.")
    monte_carlo_std_dev = PermissibleValue(
        text="monte_carlo_std_dev",
        description="Standard deviation from Monte Carlo sampling.")

    _defn = EnumDefinition(
        name="UncertaintyTypeEnum",
        description="Kind of per-value uncertainty.",
    )

class MissingDataHandlingEnum(EnumDefinitionImpl):
    """
    How the source handles missing values.
    """
    none = PermissibleValue(
        text="none",
        description="Values are passed through as missing.")
    spatiotemporal_interpolation = PermissibleValue(
        text="spatiotemporal_interpolation",
        description="Missing cells are filled by spatiotemporal interpolation.")
    forward_fill = PermissibleValue(
        text="forward_fill",
        description="Forward fill from the previous non-missing observation.")
    nearest_neighbour = PermissibleValue(
        text="nearest_neighbour",
        description="Fill from the nearest non-missing neighbour cell.")

    _defn = EnumDefinition(
        name="MissingDataHandlingEnum",
        description="How the source handles missing values.",
    )

class LinkageStrategyEnum(EnumDefinitionImpl):
    """
    How a gridded value is attached to a patient location.
    """
    point_extraction_at_residence = PermissibleValue(
        text="point_extraction_at_residence",
        description="Extract value at the patient's residence coordinates.")
    buffer_aggregation_around_residence = PermissibleValue(
        text="buffer_aggregation_around_residence",
        description="Aggregate values within a buffer around the patient's residence.")
    area_membership_residence_in_polygon = PermissibleValue(
        text="area_membership_residence_in_polygon",
        description="Membership of the patient's residence in a polygon (e.g. public water system service area).")
    nearest_station_with_max_distance = PermissibleValue(
        text="nearest_station_with_max_distance",
        description="Use the nearest observing station, with a maximum allowed distance.")
    population_weighted_area_to_residence = PermissibleValue(
        text="population_weighted_area_to_residence",
        description="Population-weighted aggregation over an area surrounding the patient's residence.")

    _defn = EnumDefinition(
        name="LinkageStrategyEnum",
        description="How a gridded value is attached to a patient location.",
    )

class BufferAggregationEnum(EnumDefinitionImpl):
    """
    Aggregation within a buffer.
    """
    mean = PermissibleValue(
        text="mean",
        description="Arithmetic mean of values in the buffer.")
    max = PermissibleValue(
        text="max",
        description="Maximum value in the buffer.")
    median = PermissibleValue(
        text="median",
        description="Median of values in the buffer.")
    area_weighted_mean = PermissibleValue(
        text="area_weighted_mean",
        description="Area-weighted mean of values in the buffer.")

    _defn = EnumDefinition(
        name="BufferAggregationEnum",
        description="Aggregation within a buffer.",
    )

class GeocodingPrecisionEnum(EnumDefinitionImpl):
    """
    Geocoder precision category, mirroring DeGAUSS `geocoder.precision`.
    """
    range = PermissibleValue(
        text="range",
        description="""Street-centerline point interpolated within an address-range segment. Highest precision typical for residential addresses.""")
    street = PermissibleValue(
        text="street",
        description="Representative point on the matched street segment.")
    intersection = PermissibleValue(
        text="intersection",
        description="Geocoded crossing of two named streets.")
    zip = PermissibleValue(
        text="zip",
        description="Centroid of the matched 5-digit ZIP code.")
    city = PermissibleValue(
        text="city",
        description="City centroid; lowest precision.")
    unknown = PermissibleValue(
        text="unknown",
        description="Precision is unknown.")

    _defn = EnumDefinition(
        name="GeocodingPrecisionEnum",
        description="Geocoder precision category, mirroring DeGAUSS `geocoder.precision`.",
    )

class AddressPeriodAlignmentEnum(EnumDefinitionImpl):
    """
    How the patient's address-over-time was modelled.
    """
    single_static_address = PermissibleValue(
        text="single_static_address",
        description="A single address is used for the whole observation period.")
    address_history_from_emr = PermissibleValue(
        text="address_history_from_emr",
        description="An EMR-sourced address history is used.")
    synthetic_residence_period = PermissibleValue(
        text="synthetic_residence_period",
        description="A synthetic residence period was constructed for the patient.")

    _defn = EnumDefinition(
        name="AddressPeriodAlignmentEnum",
        description="How the patient's address-over-time was modelled.",
    )

class ProvenanceChainTerminusEnum(EnumDefinitionImpl):
    """
    The kind of root of a provenance chain.
    """
    raw_source_download = PermissibleValue(
        text="raw_source_download",
        description="Chain terminates at a raw download from the source producer.")
    synthetic_data = PermissibleValue(
        text="synthetic_data",
        description="Chain terminates at a synthetic / simulated dataset.")
    pre_existing_curated_dataset = PermissibleValue(
        text="pre_existing_curated_dataset",
        description="Chain terminates at a pre-existing curated dataset.")

    _defn = EnumDefinition(
        name="ProvenanceChainTerminusEnum",
        description="The kind of root of a provenance chain.",
    )

class HeatMetricFamilyEnum(EnumDefinitionImpl):
    """
    Family of heat metric.
    """
    tmax = PermissibleValue(
        text="tmax",
        description="Daily maximum air temperature.")
    tmin = PermissibleValue(
        text="tmin",
        description="Daily minimum air temperature.")
    tmean = PermissibleValue(
        text="tmean",
        description="Daily mean air temperature.")
    heat_index = PermissibleValue(
        text="heat_index",
        description="Heat Index (NWS Rothfusz / Steadman).")
    wbgt_outdoor = PermissibleValue(
        text="wbgt_outdoor",
        description="Wet Bulb Globe Temperature, outdoor variant.")
    wbgt_indoor = PermissibleValue(
        text="wbgt_indoor",
        description="Wet Bulb Globe Temperature, indoor variant.")
    utci = PermissibleValue(
        text="utci",
        description="Universal Thermal Climate Index.")
    apparent_temperature = PermissibleValue(
        text="apparent_temperature",
        description="Apparent temperature (Steadman family).")
    humidex = PermissibleValue(
        text="humidex",
        description="Humidex (Masterton-Richardson).")
    heat_wave_flag = PermissibleValue(
        text="heat_wave_flag",
        description="Binary heat-wave flag.")
    consecutive_extreme_heat_days = PermissibleValue(
        text="consecutive_extreme_heat_days",
        description="Count of consecutive extreme-heat days.")
    cooling_degree_days = PermissibleValue(
        text="cooling_degree_days",
        description="Cooling degree-days.")

    _defn = EnumDefinition(
        name="HeatMetricFamilyEnum",
        description="Family of heat metric.",
    )

class EquationVariantEnum(EnumDefinitionImpl):
    """
    Equation variant for a derived heat metric. The applicable subset depends on the `heat_metric_family`.
    """
    liljegren_2008 = PermissibleValue(
        text="liljegren_2008",
        description="WBGT — Liljegren et al. 2008 outdoor formulation.")
    acsm_simplified = PermissibleValue(
        text="acsm_simplified",
        description="WBGT — American College of Sports Medicine simplified.")
    bernard_simplified = PermissibleValue(
        text="bernard_simplified",
        description="WBGT — Bernard simplified.")
    rothfusz_1990_nws = PermissibleValue(
        text="rothfusz_1990_nws",
        description="Heat Index — Rothfusz / NWS 1990 polynomial.")
    steadman_1979 = PermissibleValue(
        text="steadman_1979",
        description="Heat Index / apparent temperature — Steadman 1979.")
    brode_2012_polynomial = PermissibleValue(
        text="brode_2012_polynomial",
        description="UTCI — Bröde et al. 2012 polynomial approximation.")

    _defn = EnumDefinition(
        name="EquationVariantEnum",
        description="""Equation variant for a derived heat metric. The applicable subset depends on the `heat_metric_family`.""",
    )

class IndoorOutdoorEnum(EnumDefinitionImpl):
    """
    Indoor / outdoor regime for derived heat metrics.
    """
    outdoor = PermissibleValue(
        text="outdoor",
        description="Outdoor (default for all reanalysis / satellite / interpolation products).")
    indoor_modeled = PermissibleValue(
        text="indoor_modeled",
        description="Indoor regime, modelled.")
    indoor_measured = PermissibleValue(
        text="indoor_measured",
        description="Indoor regime, measured by an indoor instrument.")
    mixed_unspecified = PermissibleValue(
        text="mixed_unspecified",
        description="Mixed indoor / outdoor, regime unspecified.")

    _defn = EnumDefinition(
        name="IndoorOutdoorEnum",
        description="Indoor / outdoor regime for derived heat metrics.",
    )

class SolarRadiationBasisEnum(EnumDefinitionImpl):
    """
    Basis used for the solar-radiation input to a heat metric.
    """
    surface_downwelling_shortwave_flux = PermissibleValue(
        text="surface_downwelling_shortwave_flux",
        description="Surface downwelling shortwave flux density.")
    mean_radiant_temperature_modeled = PermissibleValue(
        text="mean_radiant_temperature_modeled",
        description="Modelled mean radiant temperature.")
    not_available = PermissibleValue(
        text="not_available",
        description="Solar radiation input not available; metric falls back.")

    _defn = EnumDefinition(
        name="SolarRadiationBasisEnum",
        description="Basis used for the solar-radiation input to a heat metric.",
    )

class HeatWaveThresholdDefinitionEnum(EnumDefinitionImpl):
    """
    How the heat-wave threshold is defined. Companion slot `heat_wave_threshold_specifier` captures the concrete value.
    """
    absolute = PermissibleValue(
        text="absolute",
        description="Absolute threshold value (e.g. 35 °C). Concrete value in `heat_wave_threshold_specifier`.")
    percentile_local = PermissibleValue(
        text="percentile_local",
        description="""Local-distribution percentile (e.g. 95th percentile of local Tmax history). Percentile in `heat_wave_threshold_specifier`.""")
    percentile_climatological = PermissibleValue(
        text="percentile_climatological",
        description="Climatological-baseline percentile.")
    nws_heat_advisory_criteria = PermissibleValue(
        text="nws_heat_advisory_criteria",
        description="National Weather Service Heat Advisory criteria.")
    etccdi_warm_spell_duration_index = PermissibleValue(
        text="etccdi_warm_spell_duration_index",
        description="ETCCDI Warm Spell Duration Index.")

    _defn = EnumDefinition(
        name="HeatWaveThresholdDefinitionEnum",
        description="""How the heat-wave threshold is defined. Companion slot `heat_wave_threshold_specifier` captures the concrete value.""",
    )

class PhiStatusEnum(EnumDefinitionImpl):
    """
    PHI content of the sidecar.
    """
    no_phi = PermissibleValue(
        text="no_phi",
        description="The sidecar carries no PHI.")
    aggregated_no_phi = PermissibleValue(
        text="aggregated_no_phi",
        description="The sidecar carries aggregated values with no PHI.")
    phi_present = PermissibleValue(
        text="phi_present",
        description="The sidecar carries PHI. Should never happen; sidecars are by design PHI-free.")

    _defn = EnumDefinition(
        name="PhiStatusEnum",
        description="PHI content of the sidecar.",
    )

class DepositRepositoryEnum(EnumDefinitionImpl):
    """
    Repository hosting a FAIR deposit.
    """
    zenodo = PermissibleValue(
        text="zenodo",
        description="Zenodo.")
    dryad = PermissibleValue(
        text="dryad",
        description="Dryad.")
    figshare = PermissibleValue(
        text="figshare",
        description="Figshare.")
    osf = PermissibleValue(
        text="osf",
        description="Open Science Framework.")

    _defn = EnumDefinition(
        name="DepositRepositoryEnum",
        description="Repository hosting a FAIR deposit.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "c-her",
            PermissibleValue(
                text="c-her",
                description="ORNL C-HER (Centralized Health and Exposomic Resource)."))

class ComparatorEnum(EnumDefinitionImpl):
    """
    Comparator for quantity values
    """
    lt = PermissibleValue(
        text="lt",
        description="Less than")
    le = PermissibleValue(
        text="le",
        description="Less than or equal to")
    ge = PermissibleValue(
        text="ge",
        description="Greater than or equal to")
    gt = PermissibleValue(
        text="gt",
        description="Greater than")

    _defn = EnumDefinition(
        name="ComparatorEnum",
        description="Comparator for quantity values",
    )

# Slots
class slots:
    pass

slots.schema_version = Slot(uri=ENVAR.schema_version, name="schema_version", curie=ENVAR.curie('schema_version'),
                   model_uri=ENVAR.schema_version, domain=None, range=str)

slots.provenance_id = Slot(uri=ENVAR.provenance_id, name="provenance_id", curie=ENVAR.curie('provenance_id'),
                   model_uri=ENVAR.provenance_id, domain=None, range=str)

slots.missing_reason = Slot(uri=ENVAR.missing_reason, name="missing_reason", curie=ENVAR.curie('missing_reason'),
                   model_uri=ENVAR.missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.variable_name = Slot(uri=ENVAR.variable_name, name="variable_name", curie=ENVAR.curie('variable_name'),
                   model_uri=ENVAR.variable_name, domain=None, range=Optional[str])

slots.variable_label = Slot(uri=ENVAR.variable_label, name="variable_label", curie=ENVAR.curie('variable_label'),
                   model_uri=ENVAR.variable_label, domain=None, range=Optional[str])

slots.cf_standard_name = Slot(uri=DCTERMS.subject, name="cf_standard_name", curie=DCTERMS.curie('subject'),
                   model_uri=ENVAR.cf_standard_name, domain=None, range=Optional[str])

slots.cf_cell_methods = Slot(uri=ENVAR.cf_cell_methods, name="cf_cell_methods", curie=ENVAR.curie('cf_cell_methods'),
                   model_uri=ENVAR.cf_cell_methods, domain=None, range=Optional[str])

slots.units_ucum = Slot(uri=ENVAR.units_ucum, name="units_ucum", curie=ENVAR.curie('units_ucum'),
                   model_uri=ENVAR.units_ucum, domain=None, range=Optional[str])

slots.units_display = Slot(uri=ENVAR.units_display, name="units_display", curie=ENVAR.curie('units_display'),
                   model_uri=ENVAR.units_display, domain=None, range=Optional[str])

slots.omop_concept_id = Slot(uri=ENVAR.omop_concept_id, name="omop_concept_id", curie=ENVAR.curie('omop_concept_id'),
                   model_uri=ENVAR.omop_concept_id, domain=None, range=Optional[int])

slots.omop_concept_id_missing_reason = Slot(uri=ENVAR.omop_concept_id_missing_reason, name="omop_concept_id_missing_reason", curie=ENVAR.curie('omop_concept_id_missing_reason'),
                   model_uri=ENVAR.omop_concept_id_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.omop_concept_status = Slot(uri=ENVAR.omop_concept_status, name="omop_concept_status", curie=ENVAR.curie('omop_concept_status'),
                   model_uri=ENVAR.omop_concept_status, domain=None, range=Optional[Union[str, "OmopConceptStatusEnum"]])

slots.ecto_iri = Slot(uri=ENVAR.ecto_iri, name="ecto_iri", curie=ENVAR.curie('ecto_iri'),
                   model_uri=ENVAR.ecto_iri, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.ecto_iri_missing_reason = Slot(uri=ENVAR.ecto_iri_missing_reason, name="ecto_iri_missing_reason", curie=ENVAR.curie('ecto_iri_missing_reason'),
                   model_uri=ENVAR.ecto_iri_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.envo_iri = Slot(uri=ENVAR.envo_iri, name="envo_iri", curie=ENVAR.curie('envo_iri'),
                   model_uri=ENVAR.envo_iri, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.loinc_code = Slot(uri=ENVAR.loinc_code, name="loinc_code", curie=ENVAR.curie('loinc_code'),
                   model_uri=ENVAR.loinc_code, domain=None, range=Optional[str])

slots.loinc_code_missing_reason = Slot(uri=ENVAR.loinc_code_missing_reason, name="loinc_code_missing_reason", curie=ENVAR.curie('loinc_code_missing_reason'),
                   model_uri=ENVAR.loinc_code_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.snomed_code = Slot(uri=ENVAR.snomed_code, name="snomed_code", curie=ENVAR.curie('snomed_code'),
                   model_uri=ENVAR.snomed_code, domain=None, range=Optional[str])

slots.snomed_code_missing_reason = Slot(uri=ENVAR.snomed_code_missing_reason, name="snomed_code_missing_reason", curie=ENVAR.curie('snomed_code_missing_reason'),
                   model_uri=ENVAR.snomed_code_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.value_data_type = Slot(uri=ENVAR.value_data_type, name="value_data_type", curie=ENVAR.curie('value_data_type'),
                   model_uri=ENVAR.value_data_type, domain=None, range=Optional[Union[str, "DataTypeEnum"]])

slots.value_range_plausible_min = Slot(uri=ENVAR.value_range_plausible_min, name="value_range_plausible_min", curie=ENVAR.curie('value_range_plausible_min'),
                   model_uri=ENVAR.value_range_plausible_min, domain=None, range=Optional[float])

slots.value_range_plausible_max = Slot(uri=ENVAR.value_range_plausible_max, name="value_range_plausible_max", curie=ENVAR.curie('value_range_plausible_max'),
                   model_uri=ENVAR.value_range_plausible_max, domain=None, range=Optional[float])

slots.native_spatial_resolution_m = Slot(uri=ENVAR.native_spatial_resolution_m, name="native_spatial_resolution_m", curie=ENVAR.curie('native_spatial_resolution_m'),
                   model_uri=ENVAR.native_spatial_resolution_m, domain=None, range=Optional[float])

slots.native_spatial_resolution_descriptor = Slot(uri=ENVAR.native_spatial_resolution_descriptor, name="native_spatial_resolution_descriptor", curie=ENVAR.curie('native_spatial_resolution_descriptor'),
                   model_uri=ENVAR.native_spatial_resolution_descriptor, domain=None, range=Optional[str])

slots.crs = Slot(uri=ENVAR.crs, name="crs", curie=ENVAR.curie('crs'),
                   model_uri=ENVAR.crs, domain=None, range=Optional[str])

slots.spatial_extent_bbox = Slot(uri=ENVAR.spatial_extent_bbox, name="spatial_extent_bbox", curie=ENVAR.curie('spatial_extent_bbox'),
                   model_uri=ENVAR.spatial_extent_bbox, domain=None, range=Optional[Union[float, list[float]]])

slots.spatial_extent_descriptor = Slot(uri=ENVAR.spatial_extent_descriptor, name="spatial_extent_descriptor", curie=ENVAR.curie('spatial_extent_descriptor'),
                   model_uri=ENVAR.spatial_extent_descriptor, domain=None, range=Optional[str])

slots.extraction_method = Slot(uri=ENVAR.extraction_method, name="extraction_method", curie=ENVAR.curie('extraction_method'),
                   model_uri=ENVAR.extraction_method, domain=None, range=Optional[Union[str, "ExtractionMethodEnum"]])

slots.extraction_buffer_m = Slot(uri=ENVAR.extraction_buffer_m, name="extraction_buffer_m", curie=ENVAR.curie('extraction_buffer_m'),
                   model_uri=ENVAR.extraction_buffer_m, domain=None, range=Optional[float])

slots.extraction_buffer_m_missing_reason = Slot(uri=ENVAR.extraction_buffer_m_missing_reason, name="extraction_buffer_m_missing_reason", curie=ENVAR.curie('extraction_buffer_m_missing_reason'),
                   model_uri=ENVAR.extraction_buffer_m_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.population_weighting_source = Slot(uri=ENVAR.population_weighting_source, name="population_weighting_source", curie=ENVAR.curie('population_weighting_source'),
                   model_uri=ENVAR.population_weighting_source, domain=None, range=Optional[str])

slots.population_weighting_source_missing_reason = Slot(uri=ENVAR.population_weighting_source_missing_reason, name="population_weighting_source_missing_reason", curie=ENVAR.curie('population_weighting_source_missing_reason'),
                   model_uri=ENVAR.population_weighting_source_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.target_geography_type = Slot(uri=ENVAR.target_geography_type, name="target_geography_type", curie=ENVAR.curie('target_geography_type'),
                   model_uri=ENVAR.target_geography_type, domain=None, range=Optional[Union[str, "TargetGeographyTypeEnum"]])

slots.temporal_resolution = Slot(uri=ENVAR.temporal_resolution, name="temporal_resolution", curie=ENVAR.curie('temporal_resolution'),
                   model_uri=ENVAR.temporal_resolution, domain=None, range=Optional[Union[str, "TemporalResolutionEnum"]])

slots.temporal_aggregation_method = Slot(uri=ENVAR.temporal_aggregation_method, name="temporal_aggregation_method", curie=ENVAR.curie('temporal_aggregation_method'),
                   model_uri=ENVAR.temporal_aggregation_method, domain=None, range=Optional[Union[str, "TemporalAggregationMethodEnum"]])

slots.temporal_aggregation_window_seconds = Slot(uri=ENVAR.temporal_aggregation_window_seconds, name="temporal_aggregation_window_seconds", curie=ENVAR.curie('temporal_aggregation_window_seconds'),
                   model_uri=ENVAR.temporal_aggregation_window_seconds, domain=None, range=Optional[int])

slots.day_boundary_convention = Slot(uri=ENVAR.day_boundary_convention, name="day_boundary_convention", curie=ENVAR.curie('day_boundary_convention'),
                   model_uri=ENVAR.day_boundary_convention, domain=None, range=Optional[Union[str, "DayBoundaryConventionEnum"]])

slots.temporal_coverage_start = Slot(uri=ENVAR.temporal_coverage_start, name="temporal_coverage_start", curie=ENVAR.curie('temporal_coverage_start'),
                   model_uri=ENVAR.temporal_coverage_start, domain=None, range=Optional[Union[str, XSDDate]])

slots.temporal_coverage_end = Slot(uri=ENVAR.temporal_coverage_end, name="temporal_coverage_end", curie=ENVAR.curie('temporal_coverage_end'),
                   model_uri=ENVAR.temporal_coverage_end, domain=None, range=Optional[Union[str, XSDDate]])

slots.extraction_window_start = Slot(uri=ENVAR.extraction_window_start, name="extraction_window_start", curie=ENVAR.curie('extraction_window_start'),
                   model_uri=ENVAR.extraction_window_start, domain=None, range=Optional[Union[str, XSDDate]])

slots.extraction_window_end = Slot(uri=ENVAR.extraction_window_end, name="extraction_window_end", curie=ENVAR.curie('extraction_window_end'),
                   model_uri=ENVAR.extraction_window_end, domain=None, range=Optional[Union[str, XSDDate]])

slots.calendar = Slot(uri=ENVAR.calendar, name="calendar", curie=ENVAR.curie('calendar'),
                   model_uri=ENVAR.calendar, domain=None, range=Optional[Union[str, "CalendarEnum"]])

slots.lag_alignment_applied = Slot(uri=ENVAR.lag_alignment_applied, name="lag_alignment_applied", curie=ENVAR.curie('lag_alignment_applied'),
                   model_uri=ENVAR.lag_alignment_applied, domain=None, range=Optional[Union[str, "LagAlignmentEnum"]])

slots.lag_alignment_specifier = Slot(uri=ENVAR.lag_alignment_specifier, name="lag_alignment_specifier", curie=ENVAR.curie('lag_alignment_specifier'),
                   model_uri=ENVAR.lag_alignment_specifier, domain=None, range=Optional[str])

slots.lag_alignment_applied_missing_reason = Slot(uri=ENVAR.lag_alignment_applied_missing_reason, name="lag_alignment_applied_missing_reason", curie=ENVAR.curie('lag_alignment_applied_missing_reason'),
                   model_uri=ENVAR.lag_alignment_applied_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.source_dataset_name = Slot(uri=ENVAR.source_dataset_name, name="source_dataset_name", curie=ENVAR.curie('source_dataset_name'),
                   model_uri=ENVAR.source_dataset_name, domain=None, range=Optional[str])

slots.source_dataset_short_code = Slot(uri=ENVAR.source_dataset_short_code, name="source_dataset_short_code", curie=ENVAR.curie('source_dataset_short_code'),
                   model_uri=ENVAR.source_dataset_short_code, domain=None, range=Optional[str])

slots.source_dataset_doi = Slot(uri=DCTERMS.identifier, name="source_dataset_doi", curie=DCTERMS.curie('identifier'),
                   model_uri=ENVAR.source_dataset_doi, domain=None, range=Optional[str])

slots.source_dataset_doi_missing_reason = Slot(uri=ENVAR.source_dataset_doi_missing_reason, name="source_dataset_doi_missing_reason", curie=ENVAR.curie('source_dataset_doi_missing_reason'),
                   model_uri=ENVAR.source_dataset_doi_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.source_dataset_version = Slot(uri=ENVAR.source_dataset_version, name="source_dataset_version", curie=ENVAR.curie('source_dataset_version'),
                   model_uri=ENVAR.source_dataset_version, domain=None, range=Optional[str])

slots.source_dataset_temporal_coverage = Slot(uri=ENVAR.source_dataset_temporal_coverage, name="source_dataset_temporal_coverage", curie=ENVAR.curie('source_dataset_temporal_coverage'),
                   model_uri=ENVAR.source_dataset_temporal_coverage, domain=None, range=Optional[str])

slots.source_dataset_spatial_extent = Slot(uri=ENVAR.source_dataset_spatial_extent, name="source_dataset_spatial_extent", curie=ENVAR.curie('source_dataset_spatial_extent'),
                   model_uri=ENVAR.source_dataset_spatial_extent, domain=None, range=Optional[str])

slots.source_producer_institution = Slot(uri=ENVAR.source_producer_institution, name="source_producer_institution", curie=ENVAR.curie('source_producer_institution'),
                   model_uri=ENVAR.source_producer_institution, domain=None, range=Optional[str])

slots.source_citation_apa = Slot(uri=ENVAR.source_citation_apa, name="source_citation_apa", curie=ENVAR.curie('source_citation_apa'),
                   model_uri=ENVAR.source_citation_apa, domain=None, range=Optional[str])

slots.source_citation_bibtex = Slot(uri=ENVAR.source_citation_bibtex, name="source_citation_bibtex", curie=ENVAR.curie('source_citation_bibtex'),
                   model_uri=ENVAR.source_citation_bibtex, domain=None, range=Optional[str])

slots.source_citation_bibtex_missing_reason = Slot(uri=ENVAR.source_citation_bibtex_missing_reason, name="source_citation_bibtex_missing_reason", curie=ENVAR.curie('source_citation_bibtex_missing_reason'),
                   model_uri=ENVAR.source_citation_bibtex_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.source_license_spdx = Slot(uri=ENVAR.source_license_spdx, name="source_license_spdx", curie=ENVAR.curie('source_license_spdx'),
                   model_uri=ENVAR.source_license_spdx, domain=None, range=Optional[str])

slots.source_access_url = Slot(uri=ENVAR.source_access_url, name="source_access_url", curie=ENVAR.curie('source_access_url'),
                   model_uri=ENVAR.source_access_url, domain=None, range=Optional[Union[str, URI]])

slots.source_native_format = Slot(uri=ENVAR.source_native_format, name="source_native_format", curie=ENVAR.curie('source_native_format'),
                   model_uri=ENVAR.source_native_format, domain=None, range=Optional[Union[str, "SourceNativeFormatEnum"]])

slots.source_homogenisation_status = Slot(uri=ENVAR.source_homogenisation_status, name="source_homogenisation_status", curie=ENVAR.curie('source_homogenisation_status'),
                   model_uri=ENVAR.source_homogenisation_status, domain=None, range=Optional[Union[str, "HomogenisationStatusEnum"]])

slots.source_homogenisation_status_missing_reason = Slot(uri=ENVAR.source_homogenisation_status_missing_reason, name="source_homogenisation_status_missing_reason", curie=ENVAR.curie('source_homogenisation_status_missing_reason'),
                   model_uri=ENVAR.source_homogenisation_status_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.source_acdd_attributes = Slot(uri=ENVAR.source_acdd_attributes, name="source_acdd_attributes", curie=ENVAR.curie('source_acdd_attributes'),
                   model_uri=ENVAR.source_acdd_attributes, domain=None, range=Optional[str])

slots.source_acdd_attributes_missing_reason = Slot(uri=ENVAR.source_acdd_attributes_missing_reason, name="source_acdd_attributes_missing_reason", curie=ENVAR.curie('source_acdd_attributes_missing_reason'),
                   model_uri=ENVAR.source_acdd_attributes_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.exposure_model_type = Slot(uri=ENVAR.exposure_model_type, name="exposure_model_type", curie=ENVAR.curie('exposure_model_type'),
                   model_uri=ENVAR.exposure_model_type, domain=None, range=Optional[Union[str, "ExposureModelTypeEnum"]])

slots.exposure_model_inputs = Slot(uri=ENVAR.exposure_model_inputs, name="exposure_model_inputs", curie=ENVAR.curie('exposure_model_inputs'),
                   model_uri=ENVAR.exposure_model_inputs, domain=None, range=Optional[Union[str, list[str]]])

slots.exposure_model_paper_doi = Slot(uri=ENVAR.exposure_model_paper_doi, name="exposure_model_paper_doi", curie=ENVAR.curie('exposure_model_paper_doi'),
                   model_uri=ENVAR.exposure_model_paper_doi, domain=None, range=Optional[str])

slots.exposure_model_paper_doi_missing_reason = Slot(uri=ENVAR.exposure_model_paper_doi_missing_reason, name="exposure_model_paper_doi_missing_reason", curie=ENVAR.curie('exposure_model_paper_doi_missing_reason'),
                   model_uri=ENVAR.exposure_model_paper_doi_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.exposure_model_cross_validation_r2 = Slot(uri=ENVAR.exposure_model_cross_validation_r2, name="exposure_model_cross_validation_r2", curie=ENVAR.curie('exposure_model_cross_validation_r2'),
                   model_uri=ENVAR.exposure_model_cross_validation_r2, domain=None, range=Optional[float])

slots.exposure_model_cross_validation_r2_missing_reason = Slot(uri=ENVAR.exposure_model_cross_validation_r2_missing_reason, name="exposure_model_cross_validation_r2_missing_reason", curie=ENVAR.curie('exposure_model_cross_validation_r2_missing_reason'),
                   model_uri=ENVAR.exposure_model_cross_validation_r2_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.exposure_model_known_biases = Slot(uri=ENVAR.exposure_model_known_biases, name="exposure_model_known_biases", curie=ENVAR.curie('exposure_model_known_biases'),
                   model_uri=ENVAR.exposure_model_known_biases, domain=None, range=Optional[Union[str, list[str]]])

slots.exposure_model_uncertainty_field = Slot(uri=ENVAR.exposure_model_uncertainty_field, name="exposure_model_uncertainty_field", curie=ENVAR.curie('exposure_model_uncertainty_field'),
                   model_uri=ENVAR.exposure_model_uncertainty_field, domain=None, range=Optional[str])

slots.exposure_model_uncertainty_field_missing_reason = Slot(uri=ENVAR.exposure_model_uncertainty_field_missing_reason, name="exposure_model_uncertainty_field_missing_reason", curie=ENVAR.curie('exposure_model_uncertainty_field_missing_reason'),
                   model_uri=ENVAR.exposure_model_uncertainty_field_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.exposure_model_ensemble_member_count = Slot(uri=ENVAR.exposure_model_ensemble_member_count, name="exposure_model_ensemble_member_count", curie=ENVAR.curie('exposure_model_ensemble_member_count'),
                   model_uri=ENVAR.exposure_model_ensemble_member_count, domain=None, range=Optional[int])

slots.exposure_model_ensemble_member_count_missing_reason = Slot(uri=ENVAR.exposure_model_ensemble_member_count_missing_reason, name="exposure_model_ensemble_member_count_missing_reason", curie=ENVAR.curie('exposure_model_ensemble_member_count_missing_reason'),
                   model_uri=ENVAR.exposure_model_ensemble_member_count_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.bias_correction_applied = Slot(uri=ENVAR.bias_correction_applied, name="bias_correction_applied", curie=ENVAR.curie('bias_correction_applied'),
                   model_uri=ENVAR.bias_correction_applied, domain=None, range=Optional[Union[str, "BiasCorrectionAppliedEnum"]])

slots.bias_correction_applied_missing_reason = Slot(uri=ENVAR.bias_correction_applied_missing_reason, name="bias_correction_applied_missing_reason", curie=ENVAR.curie('bias_correction_applied_missing_reason'),
                   model_uri=ENVAR.bias_correction_applied_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.per_value_uncertainty_field_name = Slot(uri=ENVAR.per_value_uncertainty_field_name, name="per_value_uncertainty_field_name", curie=ENVAR.curie('per_value_uncertainty_field_name'),
                   model_uri=ENVAR.per_value_uncertainty_field_name, domain=None, range=Optional[str])

slots.per_value_uncertainty_field_name_missing_reason = Slot(uri=ENVAR.per_value_uncertainty_field_name_missing_reason, name="per_value_uncertainty_field_name_missing_reason", curie=ENVAR.curie('per_value_uncertainty_field_name_missing_reason'),
                   model_uri=ENVAR.per_value_uncertainty_field_name_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.per_value_uncertainty_type = Slot(uri=ENVAR.per_value_uncertainty_type, name="per_value_uncertainty_type", curie=ENVAR.curie('per_value_uncertainty_type'),
                   model_uri=ENVAR.per_value_uncertainty_type, domain=None, range=Optional[Union[str, "UncertaintyTypeEnum"]])

slots.per_value_uncertainty_type_missing_reason = Slot(uri=ENVAR.per_value_uncertainty_type_missing_reason, name="per_value_uncertainty_type_missing_reason", curie=ENVAR.curie('per_value_uncertainty_type_missing_reason'),
                   model_uri=ENVAR.per_value_uncertainty_type_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.per_value_uncertainty_units_ucum = Slot(uri=ENVAR.per_value_uncertainty_units_ucum, name="per_value_uncertainty_units_ucum", curie=ENVAR.curie('per_value_uncertainty_units_ucum'),
                   model_uri=ENVAR.per_value_uncertainty_units_ucum, domain=None, range=Optional[str])

slots.per_value_uncertainty_units_ucum_missing_reason = Slot(uri=ENVAR.per_value_uncertainty_units_ucum_missing_reason, name="per_value_uncertainty_units_ucum_missing_reason", curie=ENVAR.curie('per_value_uncertainty_units_ucum_missing_reason'),
                   model_uri=ENVAR.per_value_uncertainty_units_ucum_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.model_aggregate_uncertainty = Slot(uri=ENVAR.model_aggregate_uncertainty, name="model_aggregate_uncertainty", curie=ENVAR.curie('model_aggregate_uncertainty'),
                   model_uri=ENVAR.model_aggregate_uncertainty, domain=None, range=Optional[str])

slots.model_aggregate_uncertainty_missing_reason = Slot(uri=ENVAR.model_aggregate_uncertainty_missing_reason, name="model_aggregate_uncertainty_missing_reason", curie=ENVAR.curie('model_aggregate_uncertainty_missing_reason'),
                   model_uri=ENVAR.model_aggregate_uncertainty_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.quality_flag_field_name = Slot(uri=ENVAR.quality_flag_field_name, name="quality_flag_field_name", curie=ENVAR.curie('quality_flag_field_name'),
                   model_uri=ENVAR.quality_flag_field_name, domain=None, range=Optional[str])

slots.quality_flag_field_name_missing_reason = Slot(uri=ENVAR.quality_flag_field_name_missing_reason, name="quality_flag_field_name_missing_reason", curie=ENVAR.curie('quality_flag_field_name_missing_reason'),
                   model_uri=ENVAR.quality_flag_field_name_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.quality_flag_vocabulary = Slot(uri=ENVAR.quality_flag_vocabulary, name="quality_flag_vocabulary", curie=ENVAR.curie('quality_flag_vocabulary'),
                   model_uri=ENVAR.quality_flag_vocabulary, domain=None, range=Optional[str])

slots.quality_flag_vocabulary_missing_reason = Slot(uri=ENVAR.quality_flag_vocabulary_missing_reason, name="quality_flag_vocabulary_missing_reason", curie=ENVAR.curie('quality_flag_vocabulary_missing_reason'),
                   model_uri=ENVAR.quality_flag_vocabulary_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.missing_data_handling_method = Slot(uri=ENVAR.missing_data_handling_method, name="missing_data_handling_method", curie=ENVAR.curie('missing_data_handling_method'),
                   model_uri=ENVAR.missing_data_handling_method, domain=None, range=Optional[Union[str, "MissingDataHandlingEnum"]])

slots.missing_data_handling_method_missing_reason = Slot(uri=ENVAR.missing_data_handling_method_missing_reason, name="missing_data_handling_method_missing_reason", curie=ENVAR.curie('missing_data_handling_method_missing_reason'),
                   model_uri=ENVAR.missing_data_handling_method_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.data_completeness_pct = Slot(uri=ENVAR.data_completeness_pct, name="data_completeness_pct", curie=ENVAR.curie('data_completeness_pct'),
                   model_uri=ENVAR.data_completeness_pct, domain=None, range=Optional[float])

slots.data_completeness_pct_missing_reason = Slot(uri=ENVAR.data_completeness_pct_missing_reason, name="data_completeness_pct_missing_reason", curie=ENVAR.curie('data_completeness_pct_missing_reason'),
                   model_uri=ENVAR.data_completeness_pct_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.linkage_strategy = Slot(uri=ENVAR.linkage_strategy, name="linkage_strategy", curie=ENVAR.curie('linkage_strategy'),
                   model_uri=ENVAR.linkage_strategy, domain=None, range=Optional[Union[str, "LinkageStrategyEnum"]])

slots.linkage_buffer_radius_m = Slot(uri=ENVAR.linkage_buffer_radius_m, name="linkage_buffer_radius_m", curie=ENVAR.curie('linkage_buffer_radius_m'),
                   model_uri=ENVAR.linkage_buffer_radius_m, domain=None, range=Optional[float])

slots.linkage_buffer_radius_m_missing_reason = Slot(uri=ENVAR.linkage_buffer_radius_m_missing_reason, name="linkage_buffer_radius_m_missing_reason", curie=ENVAR.curie('linkage_buffer_radius_m_missing_reason'),
                   model_uri=ENVAR.linkage_buffer_radius_m_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.linkage_buffer_aggregation_method = Slot(uri=ENVAR.linkage_buffer_aggregation_method, name="linkage_buffer_aggregation_method", curie=ENVAR.curie('linkage_buffer_aggregation_method'),
                   model_uri=ENVAR.linkage_buffer_aggregation_method, domain=None, range=Optional[Union[str, "BufferAggregationEnum"]])

slots.linkage_buffer_aggregation_method_missing_reason = Slot(uri=ENVAR.linkage_buffer_aggregation_method_missing_reason, name="linkage_buffer_aggregation_method_missing_reason", curie=ENVAR.curie('linkage_buffer_aggregation_method_missing_reason'),
                   model_uri=ENVAR.linkage_buffer_aggregation_method_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.linkage_max_distance_to_station_m = Slot(uri=ENVAR.linkage_max_distance_to_station_m, name="linkage_max_distance_to_station_m", curie=ENVAR.curie('linkage_max_distance_to_station_m'),
                   model_uri=ENVAR.linkage_max_distance_to_station_m, domain=None, range=Optional[float])

slots.linkage_max_distance_to_station_m_missing_reason = Slot(uri=ENVAR.linkage_max_distance_to_station_m_missing_reason, name="linkage_max_distance_to_station_m_missing_reason", curie=ENVAR.curie('linkage_max_distance_to_station_m_missing_reason'),
                   model_uri=ENVAR.linkage_max_distance_to_station_m_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.geocoding_precision_propagated = Slot(uri=ENVAR.geocoding_precision_propagated, name="geocoding_precision_propagated", curie=ENVAR.curie('geocoding_precision_propagated'),
                   model_uri=ENVAR.geocoding_precision_propagated, domain=None, range=Optional[Union[str, "GeocodingPrecisionEnum"]])

slots.geocoding_score_propagated = Slot(uri=ENVAR.geocoding_score_propagated, name="geocoding_score_propagated", curie=ENVAR.curie('geocoding_score_propagated'),
                   model_uri=ENVAR.geocoding_score_propagated, domain=None, range=Optional[float])

slots.geocoding_score_propagated_missing_reason = Slot(uri=ENVAR.geocoding_score_propagated_missing_reason, name="geocoding_score_propagated_missing_reason", curie=ENVAR.curie('geocoding_score_propagated_missing_reason'),
                   model_uri=ENVAR.geocoding_score_propagated_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.address_period_alignment = Slot(uri=ENVAR.address_period_alignment, name="address_period_alignment", curie=ENVAR.curie('address_period_alignment'),
                   model_uri=ENVAR.address_period_alignment, domain=None, range=Optional[Union[str, "AddressPeriodAlignmentEnum"]])

slots.tool_name = Slot(uri=ENVAR.tool_name, name="tool_name", curie=ENVAR.curie('tool_name'),
                   model_uri=ENVAR.tool_name, domain=None, range=Optional[str])

slots.tool_version = Slot(uri=ENVAR.tool_version, name="tool_version", curie=ENVAR.curie('tool_version'),
                   model_uri=ENVAR.tool_version, domain=None, range=Optional[str])

slots.tool_description = Slot(uri=ENVAR.tool_description, name="tool_description", curie=ENVAR.curie('tool_description'),
                   model_uri=ENVAR.tool_description, domain=None, range=Optional[str])

slots.container_image_repository = Slot(uri=ENVAR.container_image_repository, name="container_image_repository", curie=ENVAR.curie('container_image_repository'),
                   model_uri=ENVAR.container_image_repository, domain=None, range=Optional[str])

slots.container_image_repository_missing_reason = Slot(uri=ENVAR.container_image_repository_missing_reason, name="container_image_repository_missing_reason", curie=ENVAR.curie('container_image_repository_missing_reason'),
                   model_uri=ENVAR.container_image_repository_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.container_image_digest = Slot(uri=ENVAR.container_image_digest, name="container_image_digest", curie=ENVAR.curie('container_image_digest'),
                   model_uri=ENVAR.container_image_digest, domain=None, range=Optional[str])

slots.container_image_digest_missing_reason = Slot(uri=ENVAR.container_image_digest_missing_reason, name="container_image_digest_missing_reason", curie=ENVAR.curie('container_image_digest_missing_reason'),
                   model_uri=ENVAR.container_image_digest_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.run_arguments = Slot(uri=ENVAR.run_arguments, name="run_arguments", curie=ENVAR.curie('run_arguments'),
                   model_uri=ENVAR.run_arguments, domain=None, range=Optional[str])

slots.run_timestamp_utc = Slot(uri=ENVAR.run_timestamp_utc, name="run_timestamp_utc", curie=ENVAR.curie('run_timestamp_utc'),
                   model_uri=ENVAR.run_timestamp_utc, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.run_duration_seconds = Slot(uri=ENVAR.run_duration_seconds, name="run_duration_seconds", curie=ENVAR.curie('run_duration_seconds'),
                   model_uri=ENVAR.run_duration_seconds, domain=None, range=Optional[float])

slots.run_environment = Slot(uri=ENVAR.run_environment, name="run_environment", curie=ENVAR.curie('run_environment'),
                   model_uri=ENVAR.run_environment, domain=None, range=Optional[str])

slots.input_file_sha256 = Slot(uri=ENVAR.input_file_sha256, name="input_file_sha256", curie=ENVAR.curie('input_file_sha256'),
                   model_uri=ENVAR.input_file_sha256, domain=None, range=Optional[str])

slots.input_row_count = Slot(uri=ENVAR.input_row_count, name="input_row_count", curie=ENVAR.curie('input_row_count'),
                   model_uri=ENVAR.input_row_count, domain=None, range=Optional[int])

slots.output_file_sha256 = Slot(uri=ENVAR.output_file_sha256, name="output_file_sha256", curie=ENVAR.curie('output_file_sha256'),
                   model_uri=ENVAR.output_file_sha256, domain=None, range=Optional[str])

slots.output_row_count = Slot(uri=ENVAR.output_row_count, name="output_row_count", curie=ENVAR.curie('output_row_count'),
                   model_uri=ENVAR.output_row_count, domain=None, range=Optional[int])

slots.run_log_excerpt = Slot(uri=ENVAR.run_log_excerpt, name="run_log_excerpt", curie=ENVAR.curie('run_log_excerpt'),
                   model_uri=ENVAR.run_log_excerpt, domain=None, range=Optional[str])

slots.run_log_excerpt_missing_reason = Slot(uri=ENVAR.run_log_excerpt_missing_reason, name="run_log_excerpt_missing_reason", curie=ENVAR.curie('run_log_excerpt_missing_reason'),
                   model_uri=ENVAR.run_log_excerpt_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.provenance_chain_steps = Slot(uri=ENVAR.provenance_chain_steps, name="provenance_chain_steps", curie=ENVAR.curie('provenance_chain_steps'),
                   model_uri=ENVAR.provenance_chain_steps, domain=None, range=Optional[Union[Union[dict, ToolRun], list[Union[dict, ToolRun]]]])

slots.provenance_chain_terminus_type = Slot(uri=ENVAR.provenance_chain_terminus_type, name="provenance_chain_terminus_type", curie=ENVAR.curie('provenance_chain_terminus_type'),
                   model_uri=ENVAR.provenance_chain_terminus_type, domain=None, range=Optional[Union[str, "ProvenanceChainTerminusEnum"]])

slots.chain_compatibility_assertions = Slot(uri=ENVAR.chain_compatibility_assertions, name="chain_compatibility_assertions", curie=ENVAR.curie('chain_compatibility_assertions'),
                   model_uri=ENVAR.chain_compatibility_assertions, domain=None, range=Optional[Union[str, list[str]]])

slots.heat_metric_family = Slot(uri=ENVAR.heat_metric_family, name="heat_metric_family", curie=ENVAR.curie('heat_metric_family'),
                   model_uri=ENVAR.heat_metric_family, domain=None, range=Optional[Union[str, "HeatMetricFamilyEnum"]])

slots.equation_variant = Slot(uri=ENVAR.equation_variant, name="equation_variant", curie=ENVAR.curie('equation_variant'),
                   model_uri=ENVAR.equation_variant, domain=None, range=Optional[Union[str, "EquationVariantEnum"]])

slots.equation_variant_missing_reason = Slot(uri=ENVAR.equation_variant_missing_reason, name="equation_variant_missing_reason", curie=ENVAR.curie('equation_variant_missing_reason'),
                   model_uri=ENVAR.equation_variant_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.equation_inputs = Slot(uri=ENVAR.equation_inputs, name="equation_inputs", curie=ENVAR.curie('equation_inputs'),
                   model_uri=ENVAR.equation_inputs, domain=None, range=Optional[Union[str, list[str]]])

slots.equation_validity_range = Slot(uri=ENVAR.equation_validity_range, name="equation_validity_range", curie=ENVAR.curie('equation_validity_range'),
                   model_uri=ENVAR.equation_validity_range, domain=None, range=Optional[str])

slots.equation_validity_range_missing_reason = Slot(uri=ENVAR.equation_validity_range_missing_reason, name="equation_validity_range_missing_reason", curie=ENVAR.curie('equation_validity_range_missing_reason'),
                   model_uri=ENVAR.equation_validity_range_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.indoor_outdoor = Slot(uri=ENVAR.indoor_outdoor, name="indoor_outdoor", curie=ENVAR.curie('indoor_outdoor'),
                   model_uri=ENVAR.indoor_outdoor, domain=None, range=Optional[Union[str, "IndoorOutdoorEnum"]])

slots.wind_speed_measurement_height_m = Slot(uri=ENVAR.wind_speed_measurement_height_m, name="wind_speed_measurement_height_m", curie=ENVAR.curie('wind_speed_measurement_height_m'),
                   model_uri=ENVAR.wind_speed_measurement_height_m, domain=None, range=Optional[float])

slots.wind_speed_measurement_height_m_missing_reason = Slot(uri=ENVAR.wind_speed_measurement_height_m_missing_reason, name="wind_speed_measurement_height_m_missing_reason", curie=ENVAR.curie('wind_speed_measurement_height_m_missing_reason'),
                   model_uri=ENVAR.wind_speed_measurement_height_m_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.solar_radiation_basis = Slot(uri=ENVAR.solar_radiation_basis, name="solar_radiation_basis", curie=ENVAR.curie('solar_radiation_basis'),
                   model_uri=ENVAR.solar_radiation_basis, domain=None, range=Optional[Union[str, "SolarRadiationBasisEnum"]])

slots.solar_radiation_basis_missing_reason = Slot(uri=ENVAR.solar_radiation_basis_missing_reason, name="solar_radiation_basis_missing_reason", curie=ENVAR.curie('solar_radiation_basis_missing_reason'),
                   model_uri=ENVAR.solar_radiation_basis_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.heat_wave_threshold_definition = Slot(uri=ENVAR.heat_wave_threshold_definition, name="heat_wave_threshold_definition", curie=ENVAR.curie('heat_wave_threshold_definition'),
                   model_uri=ENVAR.heat_wave_threshold_definition, domain=None, range=Optional[Union[str, "HeatWaveThresholdDefinitionEnum"]])

slots.heat_wave_threshold_definition_missing_reason = Slot(uri=ENVAR.heat_wave_threshold_definition_missing_reason, name="heat_wave_threshold_definition_missing_reason", curie=ENVAR.curie('heat_wave_threshold_definition_missing_reason'),
                   model_uri=ENVAR.heat_wave_threshold_definition_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.heat_wave_threshold_specifier = Slot(uri=ENVAR.heat_wave_threshold_specifier, name="heat_wave_threshold_specifier", curie=ENVAR.curie('heat_wave_threshold_specifier'),
                   model_uri=ENVAR.heat_wave_threshold_specifier, domain=None, range=Optional[str])

slots.heat_wave_min_consecutive_days = Slot(uri=ENVAR.heat_wave_min_consecutive_days, name="heat_wave_min_consecutive_days", curie=ENVAR.curie('heat_wave_min_consecutive_days'),
                   model_uri=ENVAR.heat_wave_min_consecutive_days, domain=None, range=Optional[int])

slots.heat_wave_min_consecutive_days_missing_reason = Slot(uri=ENVAR.heat_wave_min_consecutive_days_missing_reason, name="heat_wave_min_consecutive_days_missing_reason", curie=ENVAR.curie('heat_wave_min_consecutive_days_missing_reason'),
                   model_uri=ENVAR.heat_wave_min_consecutive_days_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.percentile_reference_period_start = Slot(uri=ENVAR.percentile_reference_period_start, name="percentile_reference_period_start", curie=ENVAR.curie('percentile_reference_period_start'),
                   model_uri=ENVAR.percentile_reference_period_start, domain=None, range=Optional[Union[str, XSDDate]])

slots.percentile_reference_period_start_missing_reason = Slot(uri=ENVAR.percentile_reference_period_start_missing_reason, name="percentile_reference_period_start_missing_reason", curie=ENVAR.curie('percentile_reference_period_start_missing_reason'),
                   model_uri=ENVAR.percentile_reference_period_start_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.percentile_reference_period_end = Slot(uri=ENVAR.percentile_reference_period_end, name="percentile_reference_period_end", curie=ENVAR.curie('percentile_reference_period_end'),
                   model_uri=ENVAR.percentile_reference_period_end, domain=None, range=Optional[Union[str, XSDDate]])

slots.percentile_reference_period_end_missing_reason = Slot(uri=ENVAR.percentile_reference_period_end_missing_reason, name="percentile_reference_period_end_missing_reason", curie=ENVAR.curie('percentile_reference_period_end_missing_reason'),
                   model_uri=ENVAR.percentile_reference_period_end_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.percentile_reference_geographic_scope = Slot(uri=ENVAR.percentile_reference_geographic_scope, name="percentile_reference_geographic_scope", curie=ENVAR.curie('percentile_reference_geographic_scope'),
                   model_uri=ENVAR.percentile_reference_geographic_scope, domain=None, range=Optional[str])

slots.percentile_reference_geographic_scope_missing_reason = Slot(uri=ENVAR.percentile_reference_geographic_scope_missing_reason, name="percentile_reference_geographic_scope_missing_reason", curie=ENVAR.curie('percentile_reference_geographic_scope_missing_reason'),
                   model_uri=ENVAR.percentile_reference_geographic_scope_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.percentile_reference_seasonal_window = Slot(uri=ENVAR.percentile_reference_seasonal_window, name="percentile_reference_seasonal_window", curie=ENVAR.curie('percentile_reference_seasonal_window'),
                   model_uri=ENVAR.percentile_reference_seasonal_window, domain=None, range=Optional[str])

slots.percentile_reference_seasonal_window_missing_reason = Slot(uri=ENVAR.percentile_reference_seasonal_window_missing_reason, name="percentile_reference_seasonal_window_missing_reason", curie=ENVAR.curie('percentile_reference_seasonal_window_missing_reason'),
                   model_uri=ENVAR.percentile_reference_seasonal_window_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.metric_temporal_aggregation_rule = Slot(uri=ENVAR.metric_temporal_aggregation_rule, name="metric_temporal_aggregation_rule", curie=ENVAR.curie('metric_temporal_aggregation_rule'),
                   model_uri=ENVAR.metric_temporal_aggregation_rule, domain=None, range=Optional[str])

slots.metric_temporal_aggregation_rule_missing_reason = Slot(uri=ENVAR.metric_temporal_aggregation_rule_missing_reason, name="metric_temporal_aggregation_rule_missing_reason", curie=ENVAR.curie('metric_temporal_aggregation_rule_missing_reason'),
                   model_uri=ENVAR.metric_temporal_aggregation_rule_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.omop_external_exposure_link_field = Slot(uri=ENVAR.omop_external_exposure_link_field, name="omop_external_exposure_link_field", curie=ENVAR.curie('omop_external_exposure_link_field'),
                   model_uri=ENVAR.omop_external_exposure_link_field, domain=None, range=Optional[str])

slots.bdc_link_field = Slot(uri=ENVAR.bdc_link_field, name="bdc_link_field", curie=ENVAR.curie('bdc_link_field'),
                   model_uri=ENVAR.bdc_link_field, domain=None, range=Optional[str])

slots.bdc_link_field_missing_reason = Slot(uri=ENVAR.bdc_link_field_missing_reason, name="bdc_link_field_missing_reason", curie=ENVAR.curie('bdc_link_field_missing_reason'),
                   model_uri=ENVAR.bdc_link_field_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.cohort_size_anchored = Slot(uri=ENVAR.cohort_size_anchored, name="cohort_size_anchored", curie=ENVAR.curie('cohort_size_anchored'),
                   model_uri=ENVAR.cohort_size_anchored, domain=None, range=Optional[int])

slots.cohort_size_anchored_missing_reason = Slot(uri=ENVAR.cohort_size_anchored_missing_reason, name="cohort_size_anchored_missing_reason", curie=ENVAR.curie('cohort_size_anchored_missing_reason'),
                   model_uri=ENVAR.cohort_size_anchored_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.phi_status = Slot(uri=ENVAR.phi_status, name="phi_status", curie=ENVAR.curie('phi_status'),
                   model_uri=ENVAR.phi_status, domain=None, range=Optional[Union[str, "PhiStatusEnum"]])

slots.deposit_doi = Slot(uri=ENVAR.deposit_doi, name="deposit_doi", curie=ENVAR.curie('deposit_doi'),
                   model_uri=ENVAR.deposit_doi, domain=None, range=Optional[str])

slots.deposit_doi_missing_reason = Slot(uri=ENVAR.deposit_doi_missing_reason, name="deposit_doi_missing_reason", curie=ENVAR.curie('deposit_doi_missing_reason'),
                   model_uri=ENVAR.deposit_doi_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.deposit_repository = Slot(uri=ENVAR.deposit_repository, name="deposit_repository", curie=ENVAR.curie('deposit_repository'),
                   model_uri=ENVAR.deposit_repository, domain=None, range=Optional[Union[str, "DepositRepositoryEnum"]])

slots.deposit_repository_missing_reason = Slot(uri=ENVAR.deposit_repository_missing_reason, name="deposit_repository_missing_reason", curie=ENVAR.curie('deposit_repository_missing_reason'),
                   model_uri=ENVAR.deposit_repository_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.deposit_license_spdx = Slot(uri=ENVAR.deposit_license_spdx, name="deposit_license_spdx", curie=ENVAR.curie('deposit_license_spdx'),
                   model_uri=ENVAR.deposit_license_spdx, domain=None, range=Optional[str])

slots.deposit_redistribution_constraints_inherited = Slot(uri=ENVAR.deposit_redistribution_constraints_inherited, name="deposit_redistribution_constraints_inherited", curie=ENVAR.curie('deposit_redistribution_constraints_inherited'),
                   model_uri=ENVAR.deposit_redistribution_constraints_inherited, domain=None, range=Optional[Union[str, list[str]]])

slots.recommended_citation = Slot(uri=ENVAR.recommended_citation, name="recommended_citation", curie=ENVAR.curie('recommended_citation'),
                   model_uri=ENVAR.recommended_citation, domain=None, range=Optional[str])

slots.dcat_distribution_url = Slot(uri=ENVAR.dcat_distribution_url, name="dcat_distribution_url", curie=ENVAR.curie('dcat_distribution_url'),
                   model_uri=ENVAR.dcat_distribution_url, domain=None, range=Optional[Union[str, URI]])

slots.dcat_distribution_url_missing_reason = Slot(uri=ENVAR.dcat_distribution_url_missing_reason, name="dcat_distribution_url_missing_reason", curie=ENVAR.curie('dcat_distribution_url_missing_reason'),
                   model_uri=ENVAR.dcat_distribution_url_missing_reason, domain=None, range=Optional[Union[str, "MissingReasonEnum"]])

slots.source_dataset = Slot(uri=ENVAR.source_dataset, name="source_dataset", curie=ENVAR.curie('source_dataset'),
                   model_uri=ENVAR.source_dataset, domain=None, range=Union[dict, SourceDataset])

slots.uncertainty = Slot(uri=ENVAR.uncertainty, name="uncertainty", curie=ENVAR.curie('uncertainty'),
                   model_uri=ENVAR.uncertainty, domain=None, range=Optional[Union[dict, Uncertainty]])

slots.linkage_method = Slot(uri=ENVAR.linkage_method, name="linkage_method", curie=ENVAR.curie('linkage_method'),
                   model_uri=ENVAR.linkage_method, domain=None, range=Union[dict, LinkageMethod])

slots.tool_run = Slot(uri=ENVAR.tool_run, name="tool_run", curie=ENVAR.curie('tool_run'),
                   model_uri=ENVAR.tool_run, domain=None, range=Union[dict, ToolRun])

slots.provenance_chain = Slot(uri=ENVAR.provenance_chain, name="provenance_chain", curie=ENVAR.curie('provenance_chain'),
                   model_uri=ENVAR.provenance_chain, domain=None, range=Union[dict, ProvenanceChain])

slots.derived_heat_metric = Slot(uri=ENVAR.derived_heat_metric, name="derived_heat_metric", curie=ENVAR.curie('derived_heat_metric'),
                   model_uri=ENVAR.derived_heat_metric, domain=None, range=Optional[Union[dict, DerivedHeatMetric]])

slots.omop_linkage = Slot(uri=ENVAR.omop_linkage, name="omop_linkage", curie=ENVAR.curie('omop_linkage'),
                   model_uri=ENVAR.omop_linkage, domain=None, range=Union[dict, OmopLinkage])

slots.deposit_metadata = Slot(uri=ENVAR.deposit_metadata, name="deposit_metadata", curie=ENVAR.curie('deposit_metadata'),
                   model_uri=ENVAR.deposit_metadata, domain=None, range=Optional[Union[dict, DepositMetadata]])

slots.profile_version = Slot(uri=LINKML['linkml-microschema-profile/profile_version'], name="profile_version", curie=LINKML.curie('linkml-microschema-profile/profile_version'),
                   model_uri=ENVAR.profile_version, domain=None, range=Optional[str])

slots.domain_of_use = Slot(uri=LINKML['linkml-microschema-profile/domain_of_use'], name="domain_of_use", curie=LINKML.curie('linkml-microschema-profile/domain_of_use'),
                   model_uri=ENVAR.domain_of_use, domain=None, range=Optional[Union[str, list[str]]])

slots.subject = Slot(uri=LINKML['linkml-microschema-profile/subject'], name="subject", curie=LINKML.curie('linkml-microschema-profile/subject'),
                   model_uri=ENVAR.subject, domain=None, range=str)

slots.observation_type = Slot(uri=LINKML['linkml-microschema-profile/observation_type'], name="observation_type", curie=LINKML.curie('linkml-microschema-profile/observation_type'),
                   model_uri=ENVAR.observation_type, domain=None, range=str)

slots.location = Slot(uri=LINKML['linkml-microschema-profile/location'], name="location", curie=LINKML.curie('linkml-microschema-profile/location'),
                   model_uri=ENVAR.location, domain=None, range=str)

slots.temporality = Slot(uri=LINKML['linkml-microschema-profile/temporality'], name="temporality", curie=LINKML.curie('linkml-microschema-profile/temporality'),
                   model_uri=ENVAR.temporality, domain=None, range=str)

slots.methodology = Slot(uri=LINKML['linkml-microschema-profile/methodology'], name="methodology", curie=LINKML.curie('linkml-microschema-profile/methodology'),
                   model_uri=ENVAR.methodology, domain=None, range=str)

slots.observation_result = Slot(uri=LINKML['linkml-microschema-profile/observation_result'], name="observation_result", curie=LINKML.curie('linkml-microschema-profile/observation_result'),
                   model_uri=ENVAR.observation_result, domain=None, range=Union[dict, ValueMicroschemaDefinition])

slots.quantity_value = Slot(uri=LINKML['linkml-microschema-profile/quantity_value'], name="quantity_value", curie=LINKML.curie('linkml-microschema-profile/quantity_value'),
                   model_uri=ENVAR.quantity_value, domain=None, range=Decimal)

slots.quantity_unit = Slot(uri=SCHEMA.unitCode, name="quantity_unit", curie=SCHEMA.curie('unitCode'),
                   model_uri=ENVAR.quantity_unit, domain=None, range=Union[str, URIorCURIE])

slots.comparator = Slot(uri=LINKML['linkml-microschema-profile/comparator'], name="comparator", curie=LINKML.curie('linkml-microschema-profile/comparator'),
                   model_uri=ENVAR.comparator, domain=None, range=Optional[Union[str, "ComparatorEnum"]])

slots.datetime = Slot(uri=LINKML['linkml-microschema-profile/datetime'], name="datetime", curie=LINKML.curie('linkml-microschema-profile/datetime'),
                   model_uri=ENVAR.datetime, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.relative_to_event = Slot(uri=LINKML['linkml-microschema-profile/relative_to_event'], name="relative_to_event", curie=LINKML.curie('linkml-microschema-profile/relative_to_event'),
                   model_uri=ENVAR.relative_to_event, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.offset = Slot(uri=LINKML['linkml-microschema-profile/offset'], name="offset", curie=LINKML.curie('linkml-microschema-profile/offset'),
                   model_uri=ENVAR.offset, domain=None, range=Optional[Union[dict, Quantity]])

slots.subject_age = Slot(uri=LINKML['linkml-microschema-profile/subject_age'], name="subject_age", curie=LINKML.curie('linkml-microschema-profile/subject_age'),
                   model_uri=ENVAR.subject_age, domain=None, range=Optional[Union[dict, Quantity]])

slots.interval_start = Slot(uri=LINKML['linkml-microschema-profile/interval_start'], name="interval_start", curie=LINKML.curie('linkml-microschema-profile/interval_start'),
                   model_uri=ENVAR.interval_start, domain=None, range=Optional[Union[dict, Timepoint]])

slots.interval_end = Slot(uri=LINKML['linkml-microschema-profile/interval_end'], name="interval_end", curie=LINKML.curie('linkml-microschema-profile/interval_end'),
                   model_uri=ENVAR.interval_end, domain=None, range=Optional[Union[dict, Timepoint]])

slots.duration = Slot(uri=LINKML['linkml-microschema-profile/duration'], name="duration", curie=LINKML.curie('linkml-microschema-profile/duration'),
                   model_uri=ENVAR.duration, domain=None, range=Optional[Union[dict, Quantity]])

slots.code = Slot(uri=LINKML['linkml-microschema-profile/code'], name="code", curie=LINKML.curie('linkml-microschema-profile/code'),
                   model_uri=ENVAR.code, domain=None, range=Union[str, URIorCURIE])

slots.code_label = Slot(uri=LINKML['linkml-microschema-profile/code_label'], name="code_label", curie=LINKML.curie('linkml-microschema-profile/code_label'),
                   model_uri=ENVAR.code_label, domain=None, range=Optional[str])

slots.code_system = Slot(uri=LINKML['linkml-microschema-profile/code_system'], name="code_system", curie=LINKML.curie('linkml-microschema-profile/code_system'),
                   model_uri=ENVAR.code_system, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.VariableIdentity_variable_name = Slot(uri=ENVAR.variable_name, name="VariableIdentity_variable_name", curie=ENVAR.curie('variable_name'),
                   model_uri=ENVAR.VariableIdentity_variable_name, domain=VariableIdentity, range=str)

slots.VariableIdentity_cf_standard_name = Slot(uri=DCTERMS.subject, name="VariableIdentity_cf_standard_name", curie=DCTERMS.curie('subject'),
                   model_uri=ENVAR.VariableIdentity_cf_standard_name, domain=VariableIdentity, range=str)

slots.VariableIdentity_units_ucum = Slot(uri=ENVAR.units_ucum, name="VariableIdentity_units_ucum", curie=ENVAR.curie('units_ucum'),
                   model_uri=ENVAR.VariableIdentity_units_ucum, domain=VariableIdentity, range=str)

slots.VariableIdentity_omop_concept_status = Slot(uri=ENVAR.omop_concept_status, name="VariableIdentity_omop_concept_status", curie=ENVAR.curie('omop_concept_status'),
                   model_uri=ENVAR.VariableIdentity_omop_concept_status, domain=VariableIdentity, range=Union[str, "OmopConceptStatusEnum"])

slots.VariableIdentity_value_data_type = Slot(uri=ENVAR.value_data_type, name="VariableIdentity_value_data_type", curie=ENVAR.curie('value_data_type'),
                   model_uri=ENVAR.VariableIdentity_value_data_type, domain=VariableIdentity, range=Union[str, "DataTypeEnum"])

slots.SpatialReference_crs = Slot(uri=ENVAR.crs, name="SpatialReference_crs", curie=ENVAR.curie('crs'),
                   model_uri=ENVAR.SpatialReference_crs, domain=SpatialReference, range=str)

slots.SpatialReference_extraction_method = Slot(uri=ENVAR.extraction_method, name="SpatialReference_extraction_method", curie=ENVAR.curie('extraction_method'),
                   model_uri=ENVAR.SpatialReference_extraction_method, domain=SpatialReference, range=Union[str, "ExtractionMethodEnum"])

slots.SpatialReference_target_geography_type = Slot(uri=ENVAR.target_geography_type, name="SpatialReference_target_geography_type", curie=ENVAR.curie('target_geography_type'),
                   model_uri=ENVAR.SpatialReference_target_geography_type, domain=SpatialReference, range=Union[str, "TargetGeographyTypeEnum"])

slots.TemporalReference_temporal_resolution = Slot(uri=ENVAR.temporal_resolution, name="TemporalReference_temporal_resolution", curie=ENVAR.curie('temporal_resolution'),
                   model_uri=ENVAR.TemporalReference_temporal_resolution, domain=TemporalReference, range=Union[str, "TemporalResolutionEnum"])

slots.TemporalReference_temporal_aggregation_method = Slot(uri=ENVAR.temporal_aggregation_method, name="TemporalReference_temporal_aggregation_method", curie=ENVAR.curie('temporal_aggregation_method'),
                   model_uri=ENVAR.TemporalReference_temporal_aggregation_method, domain=TemporalReference, range=Union[str, "TemporalAggregationMethodEnum"])

slots.TemporalReference_day_boundary_convention = Slot(uri=ENVAR.day_boundary_convention, name="TemporalReference_day_boundary_convention", curie=ENVAR.curie('day_boundary_convention'),
                   model_uri=ENVAR.TemporalReference_day_boundary_convention, domain=TemporalReference, range=Union[str, "DayBoundaryConventionEnum"])

slots.SourceDataset_source_dataset_name = Slot(uri=ENVAR.source_dataset_name, name="SourceDataset_source_dataset_name", curie=ENVAR.curie('source_dataset_name'),
                   model_uri=ENVAR.SourceDataset_source_dataset_name, domain=SourceDataset, range=str)

slots.SourceDataset_source_dataset_short_code = Slot(uri=ENVAR.source_dataset_short_code, name="SourceDataset_source_dataset_short_code", curie=ENVAR.curie('source_dataset_short_code'),
                   model_uri=ENVAR.SourceDataset_source_dataset_short_code, domain=SourceDataset, range=str)

slots.SourceDataset_source_dataset_version = Slot(uri=ENVAR.source_dataset_version, name="SourceDataset_source_dataset_version", curie=ENVAR.curie('source_dataset_version'),
                   model_uri=ENVAR.SourceDataset_source_dataset_version, domain=SourceDataset, range=str)

slots.SourceDataset_source_producer_institution = Slot(uri=ENVAR.source_producer_institution, name="SourceDataset_source_producer_institution", curie=ENVAR.curie('source_producer_institution'),
                   model_uri=ENVAR.SourceDataset_source_producer_institution, domain=SourceDataset, range=str)

slots.SourceDataset_source_license_spdx = Slot(uri=ENVAR.source_license_spdx, name="SourceDataset_source_license_spdx", curie=ENVAR.curie('source_license_spdx'),
                   model_uri=ENVAR.SourceDataset_source_license_spdx, domain=SourceDataset, range=str)

slots.SourceDataset_source_native_format = Slot(uri=ENVAR.source_native_format, name="SourceDataset_source_native_format", curie=ENVAR.curie('source_native_format'),
                   model_uri=ENVAR.SourceDataset_source_native_format, domain=SourceDataset, range=Union[str, "SourceNativeFormatEnum"])

slots.ExposureModel_exposure_model_type = Slot(uri=ENVAR.exposure_model_type, name="ExposureModel_exposure_model_type", curie=ENVAR.curie('exposure_model_type'),
                   model_uri=ENVAR.ExposureModel_exposure_model_type, domain=ExposureModel, range=Union[str, "ExposureModelTypeEnum"])

slots.LinkageMethod_linkage_strategy = Slot(uri=ENVAR.linkage_strategy, name="LinkageMethod_linkage_strategy", curie=ENVAR.curie('linkage_strategy'),
                   model_uri=ENVAR.LinkageMethod_linkage_strategy, domain=LinkageMethod, range=Union[str, "LinkageStrategyEnum"])

slots.LinkageMethod_geocoding_precision_propagated = Slot(uri=ENVAR.geocoding_precision_propagated, name="LinkageMethod_geocoding_precision_propagated", curie=ENVAR.curie('geocoding_precision_propagated'),
                   model_uri=ENVAR.LinkageMethod_geocoding_precision_propagated, domain=LinkageMethod, range=Union[str, "GeocodingPrecisionEnum"])

slots.LinkageMethod_address_period_alignment = Slot(uri=ENVAR.address_period_alignment, name="LinkageMethod_address_period_alignment", curie=ENVAR.curie('address_period_alignment'),
                   model_uri=ENVAR.LinkageMethod_address_period_alignment, domain=LinkageMethod, range=Union[str, "AddressPeriodAlignmentEnum"])

slots.ToolRun_tool_name = Slot(uri=ENVAR.tool_name, name="ToolRun_tool_name", curie=ENVAR.curie('tool_name'),
                   model_uri=ENVAR.ToolRun_tool_name, domain=ToolRun, range=str)

slots.ToolRun_tool_version = Slot(uri=ENVAR.tool_version, name="ToolRun_tool_version", curie=ENVAR.curie('tool_version'),
                   model_uri=ENVAR.ToolRun_tool_version, domain=ToolRun, range=str)

slots.ToolRun_run_timestamp_utc = Slot(uri=ENVAR.run_timestamp_utc, name="ToolRun_run_timestamp_utc", curie=ENVAR.curie('run_timestamp_utc'),
                   model_uri=ENVAR.ToolRun_run_timestamp_utc, domain=ToolRun, range=Union[str, XSDDateTime])

slots.ProvenanceChain_provenance_chain_steps = Slot(uri=ENVAR.provenance_chain_steps, name="ProvenanceChain_provenance_chain_steps", curie=ENVAR.curie('provenance_chain_steps'),
                   model_uri=ENVAR.ProvenanceChain_provenance_chain_steps, domain=ProvenanceChain, range=Union[Union[dict, ToolRun], list[Union[dict, ToolRun]]])

slots.ProvenanceChain_provenance_chain_terminus_type = Slot(uri=ENVAR.provenance_chain_terminus_type, name="ProvenanceChain_provenance_chain_terminus_type", curie=ENVAR.curie('provenance_chain_terminus_type'),
                   model_uri=ENVAR.ProvenanceChain_provenance_chain_terminus_type, domain=ProvenanceChain, range=Union[str, "ProvenanceChainTerminusEnum"])

slots.DerivedHeatMetric_heat_metric_family = Slot(uri=ENVAR.heat_metric_family, name="DerivedHeatMetric_heat_metric_family", curie=ENVAR.curie('heat_metric_family'),
                   model_uri=ENVAR.DerivedHeatMetric_heat_metric_family, domain=DerivedHeatMetric, range=Union[str, "HeatMetricFamilyEnum"])

slots.DerivedHeatMetric_indoor_outdoor = Slot(uri=ENVAR.indoor_outdoor, name="DerivedHeatMetric_indoor_outdoor", curie=ENVAR.curie('indoor_outdoor'),
                   model_uri=ENVAR.DerivedHeatMetric_indoor_outdoor, domain=DerivedHeatMetric, range=Union[str, "IndoorOutdoorEnum"])

slots.OmopLinkage_omop_external_exposure_link_field = Slot(uri=ENVAR.omop_external_exposure_link_field, name="OmopLinkage_omop_external_exposure_link_field", curie=ENVAR.curie('omop_external_exposure_link_field'),
                   model_uri=ENVAR.OmopLinkage_omop_external_exposure_link_field, domain=OmopLinkage, range=str)

slots.OmopLinkage_phi_status = Slot(uri=ENVAR.phi_status, name="OmopLinkage_phi_status", curie=ENVAR.curie('phi_status'),
                   model_uri=ENVAR.OmopLinkage_phi_status, domain=OmopLinkage, range=Union[str, "PhiStatusEnum"])

slots.EnvironmentalExposureRecord_subject = Slot(uri=LINKML['linkml-microschema-profile/subject'], name="EnvironmentalExposureRecord_subject", curie=LINKML.curie('linkml-microschema-profile/subject'),
                   model_uri=ENVAR.EnvironmentalExposureRecord_subject, domain=EnvironmentalExposureRecord, range=str)

slots.EnvironmentalExposureRecord_observation_type = Slot(uri=LINKML['linkml-microschema-profile/observation_type'], name="EnvironmentalExposureRecord_observation_type", curie=LINKML.curie('linkml-microschema-profile/observation_type'),
                   model_uri=ENVAR.EnvironmentalExposureRecord_observation_type, domain=EnvironmentalExposureRecord, range=Union[dict, VariableIdentity])

slots.EnvironmentalExposureRecord_location = Slot(uri=LINKML['linkml-microschema-profile/location'], name="EnvironmentalExposureRecord_location", curie=LINKML.curie('linkml-microschema-profile/location'),
                   model_uri=ENVAR.EnvironmentalExposureRecord_location, domain=EnvironmentalExposureRecord, range=Union[dict, SpatialReference])

slots.EnvironmentalExposureRecord_temporality = Slot(uri=LINKML['linkml-microschema-profile/temporality'], name="EnvironmentalExposureRecord_temporality", curie=LINKML.curie('linkml-microschema-profile/temporality'),
                   model_uri=ENVAR.EnvironmentalExposureRecord_temporality, domain=EnvironmentalExposureRecord, range=Union[dict, TemporalReference])

slots.EnvironmentalExposureRecord_methodology = Slot(uri=LINKML['linkml-microschema-profile/methodology'], name="EnvironmentalExposureRecord_methodology", curie=LINKML.curie('linkml-microschema-profile/methodology'),
                   model_uri=ENVAR.EnvironmentalExposureRecord_methodology, domain=EnvironmentalExposureRecord, range=Union[dict, ExposureModel])

slots.EnvironmentalExposureRecord_observation_result = Slot(uri=LINKML['linkml-microschema-profile/observation_result'], name="EnvironmentalExposureRecord_observation_result", curie=LINKML.curie('linkml-microschema-profile/observation_result'),
                   model_uri=ENVAR.EnvironmentalExposureRecord_observation_result, domain=EnvironmentalExposureRecord, range=Union[dict, "ValueMicroschemaDefinition"])

slots.WetBulbGlobeTemperatureOutdoorRecord_derived_heat_metric = Slot(uri=ENVAR.derived_heat_metric, name="WetBulbGlobeTemperatureOutdoorRecord_derived_heat_metric", curie=ENVAR.curie('derived_heat_metric'),
                   model_uri=ENVAR.WetBulbGlobeTemperatureOutdoorRecord_derived_heat_metric, domain=WetBulbGlobeTemperatureOutdoorRecord, range=Union[dict, DerivedHeatMetric])

slots.ExtremeHeatDayFlagRecord_derived_heat_metric = Slot(uri=ENVAR.derived_heat_metric, name="ExtremeHeatDayFlagRecord_derived_heat_metric", curie=ENVAR.curie('derived_heat_metric'),
                   model_uri=ENVAR.ExtremeHeatDayFlagRecord_derived_heat_metric, domain=ExtremeHeatDayFlagRecord, range=Union[dict, DerivedHeatMetric])
