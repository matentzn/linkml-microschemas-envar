from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "0.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'envar',
     'default_range': 'string',
     'description': 'LinkML microschemas for environmental exposure variables '
                    '(EnVar). Initial\n'
                    'scope: heat-related exposures (Tmax, WBGT, heat index, '
                    'heat-wave flags)\n'
                    'and the surrounding provenance metadata needed to load them '
                    'into OMOP\n'
                    'external_exposure with full reproducibility.\n'
                    '\n'
                    'This umbrella schema imports the thirteen modules that '
                    'together define the\n'
                    'EnVar metadata layer:\n'
                    '\n'
                    '  - envar_common         shared enums and slots\n'
                    '  - envar_variable       variable identity (CF, UCUM, '
                    'target-vocab concept, ECTO, ENVO)\n'
                    '  - envar_spatial        spatial reference, extraction\n'
                    '  - envar_temporal       temporal reference, day-boundary '
                    'convention\n'
                    '  - envar_source         upstream source dataset\n'
                    '  - envar_model          exposure model character\n'
                    '  - envar_uncertainty    uncertainty and quality\n'
                    '  - envar_linkage        gridded-to-patient linkage\n'
                    '  - envar_toolrun        tool run and W3C-PROV provenance '
                    'chain\n'
                    '  - envar_heat_metric    derived heat metrics (WBGT, HI, '
                    'UTCI, heat-wave)\n'
                    '  - envar_health_layer   health-data-layer linkage (OMOP, '
                    'BDC, …) and FAIR deposit\n'
                    '  - envar_record         the top EnvironmentalExposureRecord '
                    'composite\n'
                    '  - envar_examples       concrete record subclasses (Tmax, '
                    'Tmin, WBGT, EHD)',
     'id': 'https://w3id.org/linkml/microschemas/envar',
     'imports': ['linkml:types',
                 'envar_common',
                 'envar_variable',
                 'envar_spatial',
                 'envar_temporal',
                 'envar_source',
                 'envar_model',
                 'envar_uncertainty',
                 'envar_linkage',
                 'envar_toolrun',
                 'envar_heat_metric',
                 'envar_health_layer',
                 'envar_record',
                 'envar_examples'],
     'license': 'Apache-2.0',
     'name': 'linkml-microschemas-envar',
     'prefixes': {'envar': {'prefix_prefix': 'envar',
                            'prefix_reference': 'https://w3id.org/linkml/microschemas/envar/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'source_file': 'src/linkml_microschemas_envar/schema/linkml_microschemas_envar.yaml',
     'title': 'EnVar Microschemas — Umbrella Schema'} )

class MissingReasonEnum(str, Enum):
    """
    Controlled reasons that a slot value is missing. Distinguishes a slot the source genuinely does not produce (terminal) from one we could extract but did not (roadmap) from a bug in the chain.
    """
    not_provided_by_source = "not_provided_by_source"
    """
    Source product does not produce this information. Terminal.
    """
    available_but_not_extracted = "available_but_not_extracted"
    """
    Source produces this information but the current pipeline does not surface it. Roadmap item.
    """
    upstream_data_not_propagated = "upstream_data_not_propagated"
    """
    An upstream tool emitted this information but the current pipeline dropped it on the way through. Bug.
    """
    under_investigation = "under_investigation"
    """
    We are working on populating this slot.
    """
    not_applicable = "not_applicable"
    """
    This slot does not apply to this variable / record.
    """


class DataTypeEnum(str, Enum):
    """
    The data type of an exposure value.
    """
    continuous_numeric = "continuous_numeric"
    """
    Continuous numeric value (e.g. temperature in °C).
    """
    categorical = "categorical"
    """
    Categorical value (e.g. land-use class).
    """
    binary_flag = "binary_flag"
    """
    Binary flag (e.g. extreme-heat-day yes/no).
    """
    count = "count"
    """
    Integer count (e.g. consecutive heat days).
    """
    event_marker = "event_marker"
    """
    Date-stamped event (e.g. wildfire smoke plume).
    """


class PhiStatusEnum(str, Enum):
    """
    PHI content of the sidecar.
    """
    no_phi = "no_phi"
    """
    The sidecar carries no PHI.
    """
    aggregated_no_phi = "aggregated_no_phi"
    """
    The sidecar carries aggregated values with no PHI.
    """
    phi_present = "phi_present"
    """
    The sidecar carries PHI. Should never happen; sidecars are by design PHI-free.
    """


class ConceptStatusEnum(str, Enum):
    """
    Status of a variable's representation in the target health-data vocabulary named by `target_concept_vocabulary` (e.g. the OHDSI Standardised Vocabulary, the BioData Catalyst model). `existing` = a concept id is available now; `proposed` = a submission is in flight; `gap` = no concept exists and none is proposed.
    """
    existing = "existing"
    """
    A concept id is available in the target vocabulary.
    """
    proposed = "proposed"
    """
    A concept submission is in flight.
    """
    gap = "gap"
    """
    No concept exists yet and none is yet proposed.
    """


class ExtractionMethodEnum(str, Enum):
    """
    How a gridded value was extracted at a target location.
    """
    nearest_cell = "nearest_cell"
    """
    Take the value from the single nearest grid cell.
    """
    bilinear = "bilinear"
    """
    Bilinear interpolation of the four nearest cells.
    """
    inverse_distance_weighted_4_nearest_cells = "inverse_distance_weighted_4_nearest_cells"
    """
    Inverse-distance-weighted average of the 4 nearest cells. Default for DeGAUSS `daymet` and `narr`.
    """
    area_weighted_polygon_mean = "area_weighted_polygon_mean"
    """
    Area-weighted mean of cells overlapping a polygon.
    """
    population_weighted_mean = "population_weighted_mean"
    """
    Population-weighted mean over a target geography (e.g. tract).
    """
    point_station_lookup = "point_station_lookup"
    """
    Direct lookup at a point station observation.
    """


class TargetGeographyTypeEnum(str, Enum):
    """
    Geographic unit the exposure is attached to.
    """
    point_residence = "point_residence"
    """
    Attached to the patient's exact lat / lon.
    """
    census_block_group = "census_block_group"
    """
    US Census Block Group.
    """
    census_tract = "census_tract"
    """
    US Census Tract.
    """
    zcta = "zcta"
    """
    ZIP Code Tabulation Area.
    """
    county = "county"
    """
    US County (FIPS).
    """
    h3_hex = "h3_hex"
    """
    H3 hexagon at some resolution. Resolution captured separately.
    """
    public_water_system = "public_water_system"
    """
    Public water system service area polygon.
    """


class TemporalResolutionEnum(str, Enum):
    """
    Native temporal grain of the source product.
    """
    instantaneous = "instantaneous"
    """
    Instantaneous snapshot at a timestamp.
    """
    hourly = "hourly"
    """
    One value per hour.
    """
    number_3_hourly = "three_hourly"
    """
    One value per 3-hour window (NARR sub-daily).
    """
    daily = "daily"
    """
    One value per day.
    """
    monthly = "monthly"
    """
    One value per calendar month.
    """
    seasonal = "seasonal"
    """
    One value per season (3-month window).
    """
    annual = "annual"
    """
    One value per year.
    """


class TemporalAggregationMethodEnum(str, Enum):
    """
    How sub-period values were aggregated. CF `cell_methods` aligned.
    """
    mean = "mean"
    """
    Arithmetic mean over the window.
    """
    maximum = "maximum"
    """
    Maximum over the window. `time: maximum` in CF.
    """
    minimum = "minimum"
    """
    Minimum over the window. `time: minimum` in CF.
    """
    sum = "sum"
    """
    Sum over the window.
    """
    percentile = "percentile"
    """
    A percentile of the values in the window.
    """
    point_in_time = "point_in_time"
    """
    A point-in-time sample with no aggregation applied.
    """


class DayBoundaryConventionEnum(str, Enum):
    """
    Where the 24-hour day window starts. The single most-omitted slot in the environmental-health literature.
    """
    local_midnight = "local_midnight"
    """
    Day starts at local midnight at the target location. Daymet convention.
    """
    utc_midnight = "utc_midnight"
    """
    Day starts at 00:00 UTC. NARR / ERA5 sub-daily are computed against this.
    """
    number_24h_ending_1200_GMT = "ending_1200_gmt"
    """
    24-hour window ending 12:00 GMT, used by PRISM and historically common in US station-network products.
    """
    solar_noon_centered = "solar_noon_centered"
    """
    24-hour window centered on local solar noon.
    """
    observation_dependent = "observation_dependent"
    """
    Day boundary follows whatever the underlying observation network uses (e.g. weather-station local custom).
    """
    not_applicable = "not_applicable"
    """
    No day boundary applies — e.g. an annual or monthly aggregate where the sub-daily window is not a meaningful concept (SPEC §5).
    """


class CalendarEnum(str, Enum):
    """
    CF `calendar` values.
    """
    gregorian = "gregorian"
    """
    Standard mixed Julian / Gregorian calendar (default).
    """
    noleap = "noleap"
    """
    365-day calendar with no leap days. Common in climate-model output.
    """
    all_leap = "all_leap"
    """
    366-day calendar with all years leap.
    """
    number_360_day = "day_360"
    """
    12 months of 30 days each (CF `calendar` value `360_day`). Common in some climate-model outputs.
    """
    julian = "julian"
    """
    Proleptic Julian calendar.
    """
    proleptic_gregorian = "proleptic_gregorian"
    """
    Proleptic Gregorian calendar.
    """


class HomogenisationStatusEnum(str, Enum):
    """
    For station-based products, the homogenisation status of values across the record period.
    """
    homogenised = "homogenised"
    """
    Values have been homogenised against breakpoints.
    """
    not_homogenised = "not_homogenised"
    """
    Values are as-observed, with no homogenisation applied.
    """
    partial = "partial"
    """
    Partial homogenisation has been applied.
    """


class SourceNativeFormatEnum(str, Enum):
    """
    Format the source ships in.
    """
    NetCDF_4SOLIDUSCF = "netcdf4_cf"
    """
    NetCDF version 4 with CF Conventions metadata.
    """
    HDF5 = "hdf5"
    """
    Hierarchical Data Format version 5.
    """
    GeoTIFF = "geotiff"
    """
    GeoTIFF raster format.
    """
    GRIB_1 = "grib1"
    """
    WMO GRIB-1 format.
    """
    GRIB_2 = "grib2"
    """
    WMO GRIB-2 format.
    """
    CSV_station_observations = "csv_station_observations"
    """
    CSV file of station observations.
    """
    Zarr = "zarr"
    """
    Zarr cloud-optimised array format.
    """
    Parquet = "parquet"
    """
    Apache Parquet tabular format.
    """


class ExposureModelTypeEnum(str, Enum):
    """
    The class of model that produced the values.
    """
    direct_measurement = "direct_measurement"
    """
    Direct instrument observation.
    """
    spatial_interpolation = "spatial_interpolation"
    """
    Station observations interpolated to a grid (Daymet).
    """
    reanalysis = "reanalysis"
    """
    Data-assimilation reanalysis (NARR, ERA5).
    """
    statistical_blend = "statistical_blend"
    """
    Blend of multiple sources (GridMET = PRISM + NLDAS-2).
    """
    chemical_transport_model = "chemical_transport_model"
    """
    Deterministic chemical transport model (CMAQ, GEOS-Chem).
    """
    ensemble_machine_learning = "ensemble_machine_learning"
    """
    Ensemble ML model (Di et al. PM2.5).
    """
    single_machine_learning = "single_machine_learning"
    """
    Single ML model (Brokamp PM2.5).
    """
    equation_derived = "equation_derived"
    """
    Derived analytically from other variables via an equation.
    """
    satellite_retrieval = "satellite_retrieval"
    """
    Satellite-based retrieval algorithm.
    """


class BiasCorrectionAppliedEnum(str, Enum):
    """
    Whether and how bias correction has been applied.
    """
    none = "none"
    """
    No bias correction applied.
    """
    quantile_mapping = "quantile_mapping"
    """
    Quantile-mapping bias correction.
    """
    linear_scaling = "linear_scaling"
    """
    Linear scaling bias correction.
    """
    delta_method = "delta_method"
    """
    Delta-method bias correction.
    """
    other = "other"
    """
    Some other bias-correction method has been applied.
    """


class UncertaintyTypeEnum(str, Enum):
    """
    Kind of per-value uncertainty.
    """
    standard_error = "standard_error"
    """
    Standard error of the value.
    """
    prediction_interval = "prediction_interval"
    """
    Prediction interval; the percentile (e.g. 95 %) is captured implicitly in the producer documentation.
    """
    ensemble_std_dev = "ensemble_std_dev"
    """
    Standard deviation across ensemble members.
    """
    monte_carlo_std_dev = "monte_carlo_std_dev"
    """
    Standard deviation from Monte Carlo sampling.
    """


class MissingDataHandlingEnum(str, Enum):
    """
    How the source handles missing values.
    """
    none = "none"
    """
    Values are passed through as missing.
    """
    spatiotemporal_interpolation = "spatiotemporal_interpolation"
    """
    Missing cells are filled by spatiotemporal interpolation.
    """
    forward_fill = "forward_fill"
    """
    Forward fill from the previous non-missing observation.
    """
    nearest_neighbour = "nearest_neighbour"
    """
    Fill from the nearest non-missing neighbour cell.
    """


class LinkageStrategyEnum(str, Enum):
    """
    How a gridded value is attached to a patient location.
    """
    point_extraction_at_residence = "point_extraction_at_residence"
    """
    Extract value at the patient's residence coordinates.
    """
    buffer_aggregation_around_residence = "buffer_aggregation_around_residence"
    """
    Aggregate values within a buffer around the patient's residence.
    """
    area_membership_residence_in_polygon = "area_membership_residence_in_polygon"
    """
    Membership of the patient's residence in a polygon (e.g. public water system service area).
    """
    nearest_station_with_max_distance = "nearest_station_with_max_distance"
    """
    Use the nearest observing station, with a maximum allowed distance.
    """
    population_weighted_area_to_residence = "population_weighted_area_to_residence"
    """
    Population-weighted aggregation over an area surrounding the patient's residence.
    """


class BufferAggregationEnum(str, Enum):
    """
    Aggregation within a buffer.
    """
    mean = "mean"
    """
    Arithmetic mean of values in the buffer.
    """
    max = "max"
    """
    Maximum value in the buffer.
    """
    median = "median"
    """
    Median of values in the buffer.
    """
    area_weighted_mean = "area_weighted_mean"
    """
    Area-weighted mean of values in the buffer.
    """


class GeocodingPrecisionEnum(str, Enum):
    """
    Geocoder precision category, mirroring DeGAUSS `geocoder.precision`.
    """
    range = "range"
    """
    Street-centerline point interpolated within an address-range segment. Highest precision typical for residential addresses.
    """
    street = "street"
    """
    Representative point on the matched street segment.
    """
    intersection = "intersection"
    """
    Geocoded crossing of two named streets.
    """
    zip = "zip"
    """
    Centroid of the matched 5-digit ZIP code.
    """
    city = "city"
    """
    City centroid; lowest precision.
    """
    unknown = "unknown"
    """
    Precision is unknown.
    """


class AddressPeriodAlignmentEnum(str, Enum):
    """
    How the patient's location-over-time (the spatial axis of trajectory resolution) was modelled.
    """
    single_static_address = "single_static_address"
    """
    A single address is used for the whole observation period.
    """
    address_history_from_emr = "address_history_from_emr"
    """
    An EMR-sourced address history is used.
    """
    known_travel_interval = "known_travel_interval"
    """
    A documented trip away from the residence is accounted for (e.g. a holiday), rather than assuming the residence for the whole period; assuming a static address would smear home-location exposure across days the patient was elsewhere.
    """
    synthetic_residence_period = "synthetic_residence_period"
    """
    A synthetic residence period was constructed for the patient.
    """


class ClinicalDateAssignmentEnum(str, Enum):
    """
    The clinical-side mirror of `DayBoundaryConventionEnum` (envar_temporal): which timezone / day-boundary rule was used to collapse the clinical timestamp to the date used in the join. Compared against the exposure-side `day_boundary_convention` by the day-boundary cross-check.
    """
    local_midnight = "local_midnight"
    """
    Clinical date assigned at local midnight at the patient location.
    """
    utc_midnight = "utc_midnight"
    """
    Clinical date assigned at 00:00 UTC.
    """
    source_system_local_time = "source_system_local_time"
    """
    Clinical date assigned in the source clinical system's local time, whose offset may not be documented.
    """
    date_only_no_time = "date_only_no_time"
    """
    The clinical record carried only a date (no time of day), so no boundary rule applies; the date is taken as-is.
    """
    unknown = "unknown"
    """
    The clinical-date-assignment convention is unknown.
    """


class PartialDayAttributionEnum(str, Enum):
    """
    How boundary / transition days of the patient's trajectory (trip start / end, travel days) are attributed when location changes within a day.
    """
    origin_location = "origin_location"
    """
    The transition day is attributed to the origin location.
    """
    destination_location = "destination_location"
    """
    The transition day is attributed to the destination location.
    """
    both_days_included = "both_days_included"
    """
    Both ends of the transition are counted (exposure attributed at both locations).
    """
    excluded = "excluded"
    """
    Transition days are excluded from exposure attribution.
    """
    not_applicable = "not_applicable"
    """
    No trajectory transitions occur (e.g. a single static address), so the rule does not apply.
    """


class LagAlignmentEnum(str, Enum):
    """
    Whether the values have been pre-aligned to a clinical event window in this ETL. Companion slot `lag_alignment_specifier` captures the concrete lag pattern (e.g. `lag_3_days`, `distributed_lag_0_21`). Relocated here from envar_temporal.
    """
    none = "none"
    """
    No lag alignment applied; values are at native dates.
    """
    lag_n_days = "lag_n_days"
    """
    A single-day lag of N days has been applied. Concrete N captured in `lag_alignment_specifier`.
    """
    distributed_lag = "distributed_lag"
    """
    A distributed lag over a range of days has been applied. Range captured in `lag_alignment_specifier` (e.g. `"0-21"`).
    """


class ProvenanceChainTerminusEnum(str, Enum):
    """
    The kind of root of a provenance chain.
    """
    raw_source_download = "raw_source_download"
    """
    Chain terminates at a raw download from the source producer.
    """
    synthetic_data = "synthetic_data"
    """
    Chain terminates at a synthetic / simulated dataset.
    """
    pre_existing_curated_dataset = "pre_existing_curated_dataset"
    """
    Chain terminates at a pre-existing curated dataset.
    """


class HeatMetricFamilyEnum(str, Enum):
    """
    Family of heat metric.
    """
    tmax = "tmax"
    """
    Daily maximum air temperature.
    """
    tmin = "tmin"
    """
    Daily minimum air temperature.
    """
    tmean = "tmean"
    """
    Daily mean air temperature.
    """
    heat_index = "heat_index"
    """
    Heat Index (NWS Rothfusz / Steadman).
    """
    wbgt_outdoor = "wbgt_outdoor"
    """
    Wet Bulb Globe Temperature, outdoor variant.
    """
    wbgt_indoor = "wbgt_indoor"
    """
    Wet Bulb Globe Temperature, indoor variant.
    """
    utci = "utci"
    """
    Universal Thermal Climate Index.
    """
    apparent_temperature = "apparent_temperature"
    """
    Apparent temperature (Steadman family).
    """
    humidex = "humidex"
    """
    Humidex (Masterton-Richardson).
    """
    heat_wave_flag = "heat_wave_flag"
    """
    Binary heat-wave flag.
    """
    consecutive_extreme_heat_days = "consecutive_extreme_heat_days"
    """
    Count of consecutive extreme-heat days.
    """
    cooling_degree_days = "cooling_degree_days"
    """
    Cooling degree-days.
    """


class EquationVariantEnum(str, Enum):
    """
    Equation variant for a derived heat metric. The applicable subset depends on the `heat_metric_family`.
    """
    liljegren_2008 = "liljegren_2008"
    """
    WBGT — Liljegren et al. 2008 outdoor formulation.
    """
    acsm_simplified = "acsm_simplified"
    """
    WBGT — American College of Sports Medicine simplified.
    """
    bernard_simplified = "bernard_simplified"
    """
    WBGT — Bernard simplified.
    """
    rothfusz_1990_nws = "rothfusz_1990_nws"
    """
    Heat Index — Rothfusz / NWS 1990 polynomial.
    """
    steadman_1979 = "steadman_1979"
    """
    Heat Index / apparent temperature — Steadman 1979.
    """
    brode_2012_polynomial = "brode_2012_polynomial"
    """
    UTCI — Bröde et al. 2012 polynomial approximation.
    """


class IndoorOutdoorEnum(str, Enum):
    """
    Indoor / outdoor regime for derived heat metrics.
    """
    outdoor = "outdoor"
    """
    Outdoor (default for all reanalysis / satellite / interpolation products).
    """
    indoor_modeled = "indoor_modeled"
    """
    Indoor regime, modelled.
    """
    indoor_measured = "indoor_measured"
    """
    Indoor regime, measured by an indoor instrument.
    """
    mixed_unspecified = "mixed_unspecified"
    """
    Mixed indoor / outdoor, regime unspecified.
    """


class SolarRadiationBasisEnum(str, Enum):
    """
    Basis used for the solar-radiation input to a heat metric.
    """
    surface_downwelling_shortwave_flux = "surface_downwelling_shortwave_flux"
    """
    Surface downwelling shortwave flux density.
    """
    mean_radiant_temperature_modeled = "mean_radiant_temperature_modeled"
    """
    Modelled mean radiant temperature.
    """
    not_available = "not_available"
    """
    Solar radiation input not available; metric falls back.
    """


class HeatWaveThresholdDefinitionEnum(str, Enum):
    """
    How the heat-wave threshold is defined. Companion slot `heat_wave_threshold_specifier` captures the concrete value.
    """
    absolute = "absolute"
    """
    Absolute threshold value (e.g. 35 °C). Concrete value in `heat_wave_threshold_specifier`.
    """
    percentile_local = "percentile_local"
    """
    Local-distribution percentile (e.g. 95th percentile of local Tmax history). Percentile in `heat_wave_threshold_specifier`.
    """
    percentile_climatological = "percentile_climatological"
    """
    Climatological-baseline percentile.
    """
    nws_heat_advisory_criteria = "nws_heat_advisory_criteria"
    """
    National Weather Service Heat Advisory criteria.
    """
    etccdi_warm_spell_duration_index = "etccdi_warm_spell_duration_index"
    """
    ETCCDI Warm Spell Duration Index.
    """


class HealthLayerTargetEnum(str, Enum):
    """
    The downstream health-data layer a sidecar links into. Open by design; extend as new targets are supported.
    """
    omop_external_exposure = "omop_external_exposure"
    """
    OMOP CDM, via the OHDSI GIS `external_exposure` table extension.
    """
    bdc = "bdc"
    """
    BioData Catalyst (BDC) harmonised model.
    """
    other = "other"
    """
    Another health-data layer named out of band.
    """


class DepositRepositoryEnum(str, Enum):
    """
    Repository hosting a FAIR deposit.
    """
    zenodo = "zenodo"
    """
    Zenodo.
    """
    dryad = "dryad"
    """
    Dryad.
    """
    figshare = "figshare"
    """
    Figshare.
    """
    C_HER = "c_her"
    """
    ORNL C-HER (Centralized Health and Exposomic Resource).
    """
    osf = "osf"
    """
    Open Science Framework.
    """


class ComparatorEnum(str, Enum):
    """
    Comparator for quantity values
    """
    lt = "lt"
    """
    Less than
    """
    le = "le"
    """
    Less than or equal to
    """
    ge = "ge"
    """
    Greater than or equal to
    """
    gt = "gt"
    """
    Greater than
    """



class VariableIdentity(ConfiguredBaseModel):
    """
    The identity and semantics of an environmental exposure variable — what physical quantity is being captured, in what units, and how it binds to community vocabularies. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/variable',
         'slot_usage': {'concept_status': {'name': 'concept_status', 'required': True},
                        'standard_name': {'name': 'standard_name', 'required': True},
                        'units_ucum': {'name': 'units_ucum', 'required': True},
                        'value_data_type': {'name': 'value_data_type',
                                            'required': True},
                        'variable_name': {'name': 'variable_name', 'required': True}}})

    variable_name: str = Field(default=..., description="""The literal column name produced by the upstream tool (e.g. `tmax`, `tmmx`, `air.2m`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity']} })
    variable_label: Optional[str] = Field(default=None, description="""Human-readable label, e.g. \"daily maximum air temperature at 2 m\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity']} })
    standard_name: str = Field(default=..., description="""The standard-name identifier for the physical quantity, as a CURIE so the schema privileges no single naming authority. Use a CF Convention Standard Name where one exists (`CF:air_temperature`, `CF:relative_humidity`); for health-relevant quantities CF does not define (e.g. Heat Index, WBGT), mint a term in the project registry (`ENVAR:heat_index`) or reuse an ontology term (`ECTO:...`). The prefix carries the authority; the slot name does not. Mandatory.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity'],
         'slot_uri': 'dcterms:subject'} })
    cf_cell_methods: Optional[str] = Field(default=None, description="""CF `cell_methods` string describing how the value summarises sub-period values, e.g. `time: maximum` for Tmax, `time: mean` for daily mean.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity']} })
    units_ucum: str = Field(default=..., description="""The unit expressed in UCUM syntax, e.g. `Cel` for degrees Celsius, `K` for Kelvin, `ug/m3` for PM2.5 mass concentration.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity']} })
    units_display: Optional[str] = Field(default=None, description="""Human-readable unit string for display purposes, e.g. `°C`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['VariableIdentity']} })
    target_concept_vocabulary: Optional[str] = Field(default=None, description="""The downstream health-data vocabulary that `target_concept_id` and `concept_status` refer to, e.g. `omop` (OHDSI Standardised Vocabulary), `bdc` (BioData Catalyst). Names the vocabulary so the schema privileges no single health-data layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity']} })
    target_concept_id: Optional[str] = Field(default=None, description="""Concept identifier for the variable in the vocabulary named by `target_concept_vocabulary` (e.g. an OHDSI concept_id). Nullable with reason for environmental variables that lack coverage today.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity']} })
    target_concept_id_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `target_concept_id` is null. Distinguishes \"no concept yet exists in the target vocabulary\" from \"the pipeline did not resolve it\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['VariableIdentity']} })
    concept_status: ConceptStatusEnum = Field(default=..., description="""Status of this variable's coverage in the target health-data vocabulary (`existing` / `proposed` / `gap`). Makes the vocabulary gap explicit rather than silent. Required.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity']} })
    concept_mappings: Optional[list[str]] = Field(default=None, description="""Cross-references binding this variable to other vocabularies and ontologies, each as a CURIE. One generic list rather than a slot per standard, so adding a vocabulary is a new prefix, not a schema change. Examples: `ECTO:0000012` (Environmental Conditions, Treatments and Exposures Ontology — cross-Monarch / cross-CHORDS alignment), `ENVO:01000339` (Environment Ontology — material or process exposed to), `LOINC:...` / `SNOMED:...` (where the variable has clinical coverage). Note: the *primary* downstream health-data binding, with its `existing` / `proposed` / `gap` status, stays in the structured `target_concept_*` slots — this list is for additional, status-free cross-references.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['VariableIdentity']} })
    value_data_type: DataTypeEnum = Field(default=..., description="""The data type of the stored exposure value.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity']} })
    value_range_plausible_min: Optional[float] = Field(default=None, description="""Physical / domain lower bound for plausible values (e.g. -50 °C for ambient Tmax). Not a hard validation bound; sanity-check signal.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity']} })
    value_range_plausible_max: Optional[float] = Field(default=None, description="""Physical / domain upper bound for plausible values (e.g. 60 °C for ambient Tmax).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity']} })


class SpatialReference(ConfiguredBaseModel):
    """
    Spatial provenance of an environmental exposure value: the native grid / footprint of the source product, the CRS, the geographic extent, the extraction rule used to attach a value to a patient location, and the target geography type. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/spatial',
         'slot_usage': {'crs': {'name': 'crs', 'required': True},
                        'extraction_method': {'name': 'extraction_method',
                                              'required': True},
                        'target_geography_type': {'name': 'target_geography_type',
                                                  'required': True}}})

    native_spatial_resolution_m: Optional[float] = Field(default=None, description="""Native spatial resolution of the source product in metres. Daymet = 1000, GridMET ≈ 4000, NARR ≈ 32000.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference']} })
    native_spatial_resolution_descriptor: Optional[str] = Field(default=None, description="""Human-readable label for the native resolution, e.g. \"1 km regular grid\", \"H3 hex zoom 8\", \"census tract polygon\", \"point station\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SpatialReference']} })
    crs: str = Field(default=..., description="""Coordinate reference system as an EPSG identifier or PROJ string. Mandatory. E.g. `EPSG:4326` for Daymet, `EPSG:5072` for NARR Lambert Conformal Conic.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference']} })
    spatial_extent_bbox: Optional[list[float]] = Field(default=None, description="""Bounding box of the source *product* (not the extracted subset), as `[min_lon, min_lat, max_lon, max_lat]`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SpatialReference']} })
    spatial_extent_descriptor: Optional[str] = Field(default=None, description="""Human-readable description of the product extent, e.g. \"CONUS + Hawaii + Puerto Rico\", \"global land surface 60°S-80°N\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SpatialReference']} })
    extraction_method: ExtractionMethodEnum = Field(default=..., description="""How a gridded value was extracted at the patient's coordinates. Default for DeGAUSS daymet / narr is `inverse_distance_weighted_4_nearest_cells`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference']} })
    extraction_buffer_m: Optional[float] = Field(default=None, description="""Radius of any spatial buffer applied (e.g. greenspace at 500 / 1500 / 2500 m). Null when no buffer is applied.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['SpatialReference']} })
    extraction_buffer_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `extraction_buffer_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SpatialReference']} })
    population_weighting_source: Optional[str] = Field(default=None, description="""Census vintage used for population weighting (e.g. the Spangler et al. WBGT product is population-weighted from gridMET). Null when no weighting is applied.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['SpatialReference']} })
    population_weighting_source_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `population_weighting_source` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SpatialReference']} })
    target_geography_type: TargetGeographyTypeEnum = Field(default=..., description="""Geographic unit the exposure value is attached to.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference']} })


class TemporalReference(ConfiguredBaseModel):
    """
    Temporal provenance of an environmental exposure value: native temporal grain, aggregation rule, day-boundary convention, coverage of the source product, the extraction window the run actually pulled, and calendar. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/temporal',
         'slot_usage': {'day_boundary_convention': {'name': 'day_boundary_convention',
                                                    'required': True},
                        'temporal_aggregation_method': {'name': 'temporal_aggregation_method',
                                                        'required': True},
                        'temporal_resolution': {'name': 'temporal_resolution',
                                                'required': True}}})

    temporal_resolution: TemporalResolutionEnum = Field(default=..., description="""Native temporal grain of the values.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['TemporalReference']} })
    temporal_aggregation_method: TemporalAggregationMethodEnum = Field(default=..., description="""How the value summarises sub-period values. Maps 1:1 to CF cell_methods.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['TemporalReference']} })
    temporal_aggregation_window_seconds: Optional[int] = Field(default=None, description="""Redundant with `temporal_resolution` but explicit for machine use; e.g. 86400 for daily, 3600 for hourly.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference']} })
    day_boundary_convention: DayBoundaryConventionEnum = Field(default=..., description="""Where the 24-hour day window starts. **Mandatory.** Daymet = `local_midnight`; PRISM = `24h_ending_1200_GMT`; NARR / ERA5 sub-daily = `utc_midnight`. The single most-omitted slot in the literature and a known source of cross-study disagreement.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['TemporalReference']} })
    temporal_coverage_start: Optional[date] = Field(default=None, description="""Start of the source product's full temporal coverage.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference']} })
    temporal_coverage_end: Optional[date] = Field(default=None, description="""End of the source product's coverage. May be an \"ongoing\" sentinel for live products.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference']} })
    extraction_window_start: Optional[date] = Field(default=None, description="""Actual start date the run extracted.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference']} })
    extraction_window_end: Optional[date] = Field(default=None, description="""Actual end date the run extracted.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference']} })
    calendar: Optional[CalendarEnum] = Field(default=None, description="""CF calendar. `gregorian` is the default; only matters when a source uses a non-standard calendar (some climate model output does).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference']} })


class SourceDataset(ConfiguredBaseModel):
    """
    The upstream gridded / station product the exposure values originate from. Carries identity, DOI, version, coverage, producer, citation, license, native format, and homogenisation status. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/source',
         'slot_usage': {'source_dataset_name': {'name': 'source_dataset_name',
                                                'required': True},
                        'source_dataset_version': {'name': 'source_dataset_version',
                                                   'required': True}}})

    source_dataset_name: str = Field(default=..., description="""Full name of the source product, e.g. \"Daymet V4 Daily Surface Weather Data\", \"GridMET\", \"NARR\", \"ERA5-HEAT\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SourceDataset']} })
    source_dataset_short_code: Optional[str] = Field(default=None, description="""Short code keying into the EnVar source registry, e.g. `daymet_v4`, `gridmet`, `narr`, `era5_heat`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_dataset_doi: Optional[str] = Field(default=None, description="""DOI of the source dataset. Mandatory if a DOI exists. Daymet V4 = `10.3334/ORNLDAAC/2129`; ERA5 = `10.24381/cds.adbb2d47`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'slot_uri': 'dcterms:identifier'} })
    source_dataset_doi_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `source_dataset_doi` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset']} })
    source_dataset_version: str = Field(default=..., description="""Source product version. E.g. \"V4 R1\" for Daymet; \"V5.GL.03\" vs \"V6.GL.02\" for ACAG PM products. Version differences materially change values.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SourceDataset']} })
    source_dataset_temporal_coverage: Optional[str] = Field(default=None, description="""Source product temporal coverage as an ISO 8601 interval string `<start>/<end>`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_dataset_spatial_extent: Optional[str] = Field(default=None, description="""Human-readable spatial extent of the product, e.g. \"CONUS, Hawaii, Puerto Rico\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_producer_institution: Optional[str] = Field(default=None, description="""Producer institution, e.g. \"NASA ORNL DAAC\", \"University of Idaho\", \"NOAA NCEP\", \"ECMWF Copernicus\".""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_citation_apa: Optional[str] = Field(default=None, description="""Full APA-style citation for the source dataset.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_citation_bibtex: Optional[str] = Field(default=None, description="""BibTeX entry for the source dataset, machine-parseable.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset']} })
    source_citation_bibtex_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `source_citation_bibtex` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset']} })
    source_license_spdx: Optional[str] = Field(default=None, description="""SPDX identifier of the source license, e.g. `CC0-1.0`, `CC-BY-4.0`. Use `public-domain-us-gov` for US federal data with no formal SPDX equivalent.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_access_url: Optional[str] = Field(default=None, description="""Landing-page URL for the dataset (not a download link, which rots).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_native_format: Optional[SourceNativeFormatEnum] = Field(default=None, description="""Format the source ships in.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset']} })
    source_homogenisation_status: Optional[HomogenisationStatusEnum] = Field(default=None, description="""For station-based products, whether values have been homogenised. Mandatory for station-based products; GHCN-D = `not_homogenised`, GHCN-M v4 = `homogenised`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['SourceDataset']} })
    source_homogenisation_status_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `source_homogenisation_status` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset']} })
    source_acdd_attributes: Optional[Any] = Field(default=None, description="""Passthrough of ACDD (Attribute Convention for Data Discovery) global attributes from the source NetCDF header, as a native key/value object.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset']} })
    source_acdd_attributes_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `source_acdd_attributes` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset']} })


class ExposureModel(ConfiguredBaseModel):
    """
    The model class that produced the values (interpolation, reanalysis, ML, statistical blend, equation), its inputs, its methods-paper DOI, its cross-validation skill, known biases, and any bias correction. One per record; may be null for direct observation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/model',
         'slot_usage': {'exposure_model_type': {'name': 'exposure_model_type',
                                                'required': True}}})

    exposure_model_type: ExposureModelTypeEnum = Field(default=..., description="""The class of model that produced the values. Daymet = `spatial_interpolation`; NARR / ERA5 = `reanalysis`; GridMET = `statistical_blend`; Brokamp PM = `single_machine_learning`; Di et al. PM = `ensemble_machine_learning`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_inputs: Optional[list[str]] = Field(default=None, description="""Inputs to the model. For GridMET: `[\"PRISM monthly normals\", \"NLDAS-2 sub-daily reanalysis\"]`. For derived heat metrics, the input variable list (held in `DerivedHeatMetric.equation_inputs` for typed cases).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_paper_doi: Optional[str] = Field(default=None, description="""DOI of the methods paper describing the model (Thornton et al. 2022 for Daymet; Abatzoglou 2013 for GridMET).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_paper_doi_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `exposure_model_paper_doi` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_cross_validation_r2: Optional[float] = Field(default=None, description="""Model cross-validation R², where reported by the producer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_cross_validation_r2_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `exposure_model_cross_validation_r2` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_known_biases: Optional[list[str]] = Field(default=None, description="""Free-text flags of known issues, e.g. \"NLDAS-2 coastal Tmax bias up to -1.48 °C\", \"NARR cold bias at extremes\", \"Daymet warm bias in summer in some western US regions\". The field reviewers care about.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_uncertainty_field: Optional[str] = Field(default=None, description="""Name of any per-value uncertainty column emitted alongside the value (e.g. `pm_se` for DeGAUSS `pm`). Null with reason for products whose per-cell SE exists upstream but is not surfaced.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_uncertainty_field_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `exposure_model_uncertainty_field` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_ensemble_member_count: Optional[int] = Field(default=None, description="""For ensemble products, the number of members. Null with reason `not_provided_by_source` for single-realisation products.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['ExposureModel']} })
    exposure_model_ensemble_member_count_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `exposure_model_ensemble_member_count` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel']} })
    bias_correction_applied: Optional[BiasCorrectionAppliedEnum] = Field(default=None, description="""Whether and how bias correction has been applied. Usually `none` for Tmax from reference products.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel']} })
    bias_correction_applied_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `bias_correction_applied` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel']} })


class Uncertainty(ConfiguredBaseModel):
    """
    Uncertainty and quality character of a value series: per-value uncertainty column, uncertainty type / units, model-aggregate uncertainty summary, quality flag pointers, missing-data handling, and data completeness. One per record; slots may be null with reasons.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/uncertainty'})

    per_value_uncertainty_field_name: Optional[str] = Field(default=None, description="""Name of the column carrying per-value uncertainty (e.g. `pm_se`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty']} })
    per_value_uncertainty_field_name_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `per_value_uncertainty_field_name` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    per_value_uncertainty_type: Optional[UncertaintyTypeEnum] = Field(default=None, description="""Kind of per-value uncertainty captured in the column.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty']} })
    per_value_uncertainty_type_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `per_value_uncertainty_type` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    per_value_uncertainty_units_ucum: Optional[str] = Field(default=None, description="""Units of the per-value uncertainty in UCUM syntax. Usually the same as the value units.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty']} })
    per_value_uncertainty_units_ucum_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `per_value_uncertainty_units_ucum` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    model_aggregate_uncertainty: Optional[ModelAggregateUncertainty] = Field(default=None, description="""Summary statistics for the model as a whole — cross-validation metrics and where they are reported.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty']} })
    model_aggregate_uncertainty_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `model_aggregate_uncertainty` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    quality_flag_field_name: Optional[str] = Field(default=None, description="""Name of any per-value QA flag column. CF `ancillary_variables` analogue.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    quality_flag_field_name_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `quality_flag_field_name` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    quality_flag_vocabulary: Optional[str] = Field(default=None, description="""Reference to the QA flag vocabulary (e.g. an EPA AQS qualifier-code list).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    quality_flag_vocabulary_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `quality_flag_vocabulary` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    missing_data_handling_method: Optional[MissingDataHandlingEnum] = Field(default=None, description="""How the source handles missing values (e.g. how Daymet handles snow-covered pixels).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty']} })
    missing_data_handling_method_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `missing_data_handling_method` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })
    data_completeness_pct: Optional[float] = Field(default=None, description="""Percent of (location, date) cells in the extracted window that have a non-missing value. 0-100.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty']} })
    data_completeness_pct_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `data_completeness_pct` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty']} })


class ModelAggregateUncertainty(ConfiguredBaseModel):
    """
    Whole-model uncertainty summary — cross-validation metrics and the reference where they are reported. Inlined on `model_aggregate_uncertainty`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/uncertainty'})

    cv_r2: Optional[float] = Field(default=None, description="""Cross-validated R² for the model as a whole.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelAggregateUncertainty']} })
    cv_rmse: Optional[float] = Field(default=None, description="""Cross-validated RMSE for the model as a whole.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelAggregateUncertainty']} })
    reported_in: Optional[str] = Field(default=None, description="""DOI / citation where the aggregate uncertainty is reported.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelAggregateUncertainty']} })


class LinkageMethod(ConfiguredBaseModel):
    """
    How a gridded environmental value gets attached to a patient: the resolution of the patient's spatiotemporal trajectory down to the resolution the exposure data supports. Covers the linkage strategy and buffer parameters, the propagated geocoder precision and score, how patient location-over-time is modelled (the spatial axis), and the clinical-date-assignment convention, partial-day attribution, and lag alignment (the temporal axis). One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/linkage',
         'slot_usage': {'linkage_strategy': {'name': 'linkage_strategy',
                                             'required': True}}})

    linkage_strategy: LinkageStrategyEnum = Field(default=..., description="""How a gridded value is attached to a patient location.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['LinkageMethod']} })
    linkage_buffer_radius_m: Optional[float] = Field(default=None, description="""Buffer radius in metres for buffer-aggregation strategies.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod']} })
    linkage_buffer_radius_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `linkage_buffer_radius_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    linkage_buffer_aggregation_method: Optional[BufferAggregationEnum] = Field(default=None, description="""Aggregation method applied within the buffer (mean / max / median / area-weighted mean).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod']} })
    linkage_buffer_aggregation_method_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `linkage_buffer_aggregation_method` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    linkage_max_distance_to_station_m: Optional[float] = Field(default=None, description="""Maximum distance to a station for nearest-station strategies; values beyond this distance get null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod']} })
    linkage_max_distance_to_station_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `linkage_max_distance_to_station_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    geocoding_precision_propagated: Optional[GeocodingPrecisionEnum] = Field(default=None, description="""Quality category propagated from the upstream geocoder (DeGAUSS `precision` column).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod']} })
    geocoding_score_propagated: Optional[float] = Field(default=None, description="""Geocoder score (0-1) propagated from the upstream geocoder so the exposure record knows the spatial precision of its anchor.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod']} })
    geocoding_score_propagated_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `geocoding_score_propagated` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    address_period_alignment: Optional[AddressPeriodAlignmentEnum] = Field(default=None, description="""How the patient's location-over-time (the spatial axis of trajectory resolution) was modelled.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod']} })
    clinical_date_assignment_convention: Optional[ClinicalDateAssignmentEnum] = Field(default=None, description="""The clinical-side mirror of `day_boundary_convention` (envar_temporal): which timezone / day-boundary rule collapsed the clinical timestamp to the date used in the join. A boundary mismatch between this and the exposure-side `day_boundary_convention` silently misattributes boundary-hour events to the wrong day, which is what makes the Core `day_boundary_convention` checkable at all. Metadata *about the join* — never the clinical timestamp itself; carries no PHI.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod']} })
    clinical_date_assignment_convention_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `clinical_date_assignment_convention` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    partial_day_attribution_rule: Optional[PartialDayAttributionEnum] = Field(default=None, description="""How boundary / transition days of the patient's trajectory (trip start / end, travel days) are attributed when location changes within a day. The temporal partner to the `known_travel_interval` address alignment.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod']} })
    partial_day_attribution_rule_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `partial_day_attribution_rule` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    lag_alignment_applied: Optional[LagAlignmentEnum] = Field(default=None, description="""Whether and how values were lag-aligned to a clinical event. Relocated from envar_temporal: lag alignment attaches a value to an event (a linkage concern), not an intrinsic temporal property. See `lag_alignment_specifier` for the concrete lag value(s).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod']} })
    lag_alignment_specifier: Optional[str] = Field(default=None, description="""Free-form specifier paired with `lag_alignment_applied` to capture the concrete lag values (e.g. `\"3\"` for a 3-day lag, or `\"0-21\"` for a distributed lag from 0 to 21 days). Empty when `lag_alignment_applied` = `none`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })
    lag_alignment_applied_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `lag_alignment_applied` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod']} })


class ToolRun(ConfiguredBaseModel):
    """
    A single tool invocation that produced an output from one or more inputs: tool name and version, container image (where applicable), arguments, environment, run timestamp and duration, input / output hashes and row counts, and an optional log excerpt.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'class_uri': 'prov:Activity',
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/toolrun',
         'slot_usage': {'tool_name': {'name': 'tool_name', 'required': True},
                        'tool_version': {'name': 'tool_version', 'required': True}}})

    tool_name: str = Field(default=..., description="""Tool name, e.g. `daymet`, `narr`, `pm`, `amadeus`, `geocoder`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['ToolRun']} })
    tool_version: str = Field(default=..., description="""Semver tool version. Mandatory.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['ToolRun']} })
    tool_description: Optional[str] = Field(default=None, description="""One-line tool description (from the tool's `dht` env var or equivalent).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })
    container_image_repository: Optional[str] = Field(default=None, description="""Container image repository, e.g. `ghcr.io/degauss-org/daymet`. Null for non-containerised tools.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    container_image_repository_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `container_image_repository` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })
    container_image_digest: Optional[str] = Field(default=None, description="""SHA256 of the container image actually used (not just the tag). Reproducibility-critical.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    container_image_digest_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `container_image_digest` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })
    run_arguments: Optional[str] = Field(default=None, description="""The exact argument map passed at invocation, serialised as a JSON string.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    run_timestamp_utc: Optional[datetime ] = Field(default=None, description="""When the run started (UTC).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    run_duration_seconds: Optional[float] = Field(default=None, description="""How long the run took, in seconds.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })
    run_environment: Optional[Any] = Field(default=None, description="""Host OS, Docker / podman version, R / Python version, key library versions, as a native key/value object.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })
    input_file_sha256: Optional[str] = Field(default=None, description="""SHA256 of the input file (CSV / parquet).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    input_row_count: Optional[int] = Field(default=None, description="""Number of rows in the input.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    output_file_sha256: Optional[str] = Field(default=None, description="""SHA256 of the output file (CSV / parquet).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    output_row_count: Optional[int] = Field(default=None, description="""Number of rows in the output.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun']} })
    run_log_excerpt: Optional[str] = Field(default=None, description="""Last ~50 lines of the run log, where useful for debugging or audit.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })
    run_log_excerpt_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `run_log_excerpt` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun']} })


class ProvenanceChain(ConfiguredBaseModel):
    """
    The ordered list of all upstream `ToolRun`s whose outputs were inputs to this run, terminating in a typed root. Patterned after W3C PROV (`prov:wasDerivedFrom`, `prov:wasGeneratedBy`).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'class_uri': 'prov:Bundle',
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/toolrun'})

    provenance_chain_steps: Optional[list[ToolRun]] = Field(default=None, description="""Ordered list of upstream `ToolRun`s, from oldest to most recent, whose outputs were inputs to this run.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ProvenanceChain']} })
    provenance_chain_terminus_type: Optional[ProvenanceChainTerminusEnum] = Field(default=None, description="""The kind of root of the chain.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ProvenanceChain']} })
    chain_compatibility_assertions: Optional[list[str]] = Field(default=None, description="""Declarations that two chain steps are compatible (e.g. `daymet@1.0.0` expects `geocoder@>=3.0.0` output column schema). Optional but enables strict-mode validation.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ProvenanceChain']} })


class DerivedHeatMetric(ConfiguredBaseModel):
    """
    Methodology slots specific to derived heat metrics (WBGT, Heat Index, UTCI, apparent temperature, heat-wave flag, etc.). Captures the decisions that the heat-epidemiology literature flags as critical sources of cross-study disagreement: which equation variant, which indoor / outdoor regime, which solar-radiation input, and -- for percentile-based metrics -- the reference period, scope, and seasonal window. One per record where applicable.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/heat_metric',
         'slot_usage': {'heat_metric_family': {'name': 'heat_metric_family',
                                               'required': True},
                        'indoor_outdoor': {'name': 'indoor_outdoor', 'required': True}}})

    heat_metric_family: HeatMetricFamilyEnum = Field(default=..., description="""The family of heat metric this variable represents.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['DerivedHeatMetric']} })
    equation_variant: Optional[EquationVariantEnum] = Field(default=None, description="""For derived heat metrics, the equation variant used. Mandatory for WBGT, HI, and UTCI: a Liljegren WBGT and an ACSM WBGT for the same inputs can differ by 2-3 °C.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    equation_variant_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `equation_variant` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    equation_inputs: Optional[list[EquationInput]] = Field(default=None, description="""Typed per-input references for a multi-input derived metric (Heat Index from T + RH; WBGT from T + RH + wind + radiation). Each entry names the input's role and points, by `provenance_id`, to the upstream sidecar carrying that input's full context — it is an index into the lineage, not an inline copy of it.
Option-B decomposition (see the `EquationInput` class): when the inputs originate from different products and diverge in resolution, day-boundary convention, or temporal aggregation, each input is a full upstream sidecar referenced here and listed as a step in `provenance_chain`, so the divergence stays explicit and checkable.
Conditionally-Core: optional for a single-input metric, mandatory the moment a metric has more than one input.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'comments': ['Cross-input consistency check (completeness checker, not '
                      'structural LinkML validation): when more than one entry is '
                      'present, dereference each `input_provenance_id` and WARN if the '
                      "referenced inputs' day-boundary conventions, temporal "
                      'aggregation windows, or native spatial resolutions differ. A '
                      'divergence is allowed but must be recorded via the decomposed '
                      'sidecars rather than absorbed silently into the output value.'],
         'domain_of': ['DerivedHeatMetric']} })
    equation_validity_range: Optional[str] = Field(default=None, description="""Validity-range conditions for the equation, serialised as a JSON string. For Heat Index: `{\"min_temperature_F\": 80, \"min_relative_humidity_pct\": 40}` — Rothfusz is undefined below 80 °F / 40 % RH.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    equation_validity_range_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `equation_validity_range` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    indoor_outdoor: IndoorOutdoorEnum = Field(default=..., description="""Indoor / outdoor regime. Mandatory for WBGT (the indoor vs outdoor distinction changes the equation and the health interpretation).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    wind_speed_measurement_height_m: Optional[float] = Field(default=None, description="""For WBGT and UTCI inputs, the wind-speed measurement height in metres. The ISO 7243 standard is 2 m, but reanalysis products often supply 10 m -- the height affects the WBGT value.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric']} })
    wind_speed_measurement_height_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `wind_speed_measurement_height_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    solar_radiation_basis: Optional[SolarRadiationBasisEnum] = Field(default=None, description="""For WBGT / UTCI inputs, the basis used for solar radiation.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric']} })
    solar_radiation_basis_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `solar_radiation_basis` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    heat_wave_threshold_definition: Optional[HeatWaveThresholdDefinitionEnum] = Field(default=None, description="""For heat-wave flags, the definition of the threshold (absolute, percentile-local, percentile-climatological, NWS advisory, ETCCDI).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    heat_wave_threshold_definition_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `heat_wave_threshold_definition` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    heat_wave_threshold_specifier: Optional[str] = Field(default=None, description="""Free-form specifier paired with `heat_wave_threshold_definition` to capture the concrete threshold values (e.g. `\"35_Cel\"` for an absolute threshold, `\"95\"` for the 95th percentile).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    heat_wave_min_consecutive_days: Optional[int] = Field(default=None, description="""Minimum-consecutive-days rule for heat-wave flags (commonly 2 or 3). Changes which days are flagged.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    heat_wave_min_consecutive_days_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `heat_wave_min_consecutive_days` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_period_start: Optional[date] = Field(default=None, description="""Start of the reference distribution used for percentile-based thresholds. Mandatory for percentile metrics: \"95th percentile\" over 2000-2019 gives a different threshold than 1980-2010, and this delta is real.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_period_start_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `percentile_reference_period_start` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_period_end: Optional[date] = Field(default=None, description="""End of the reference distribution.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_period_end_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `percentile_reference_period_end` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_geographic_scope: Optional[str] = Field(default=None, description="""Geographic scope over which the reference distribution was computed. One of `local_tract`, `local_county`, `local_climate_region`, `national`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_geographic_scope_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `percentile_reference_geographic_scope` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_seasonal_window: Optional[str] = Field(default=None, description="""Seasonal window over which the reference was computed. One of `annual`, `warm_season_may_sep`, `calendar_month`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric']} })
    percentile_reference_seasonal_window_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `percentile_reference_seasonal_window` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })
    metric_temporal_aggregation_rule: Optional[str] = Field(default=None, description="""For heat-wave flags, how multi-day exposures are stamped on individual days (e.g. `first_day_of_event` / `each_day_of_event` / `last_day_of_event`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric']} })
    metric_temporal_aggregation_rule_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `metric_temporal_aggregation_rule` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric']} })


class EquationInput(ConfiguredBaseModel):
    """
    A single physical-state input to a derived heat metric, recorded as a typed reference into the provenance chain rather than an inline copy of the input's metadata. It names the input's role (a CF standard name) and points, via `input_provenance_id`, to the upstream sidecar that carries that input's full spatial / temporal / model context.
    This is the Option-B decomposition: when a multi-input metric (Heat Index from T + RH; WBGT from T + RH + wind + radiation) draws its inputs from different products that diverge in resolution, day-boundary convention, or temporal aggregation, each input remains its own full sidecar — listed here and as a step in `provenance_chain` — so the divergence stays explicit and machine-checkable instead of being silently absorbed into the single output value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/heat_metric',
         'slot_usage': {'input_provenance_id': {'name': 'input_provenance_id',
                                                'required': True},
                        'input_role': {'name': 'input_role', 'required': True}}})

    input_role: str = Field(default=..., description="""The standard-name local token of this input's physical quantity (the same quantity the referenced sidecar carries in `standard_name`), e.g. `air_temperature`, `relative_humidity`, `wind_speed`, `surface_downwelling_shortwave_flux_in_air`.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EquationInput']} })
    input_provenance_id: str = Field(default=..., description="""The `provenance_id` of the upstream sidecar that fully describes this input — its source dataset, spatial / temporal reference, and exposure model. Dereferencing it lets a consumer (or the completeness checker) compare inputs and surface any divergence in resolution, day-boundary convention, or temporal aggregation.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EquationInput']} })
    input_source_short_code: Optional[str] = Field(default=None, description="""Human-readable short code of the input's source product (e.g. `daymet_v4`, `era5`), duplicated from the referenced sidecar for convenience when scanning the record. Not authoritative — `input_provenance_id` is.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EquationInput']} })


class HealthLayerLinkage(ConfiguredBaseModel):
    """
    Hooks the sidecar uses to be findable from a downstream health-data layer (OMOP, BioData Catalyst, …). These are *not* clinical metadata — they are the hooks the exposure record needs so a health-side row can resolve back to its provenance. The target layer is named in `health_layer_target`, so no single model is privileged. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/health_layer'})

    health_layer_target: Optional[HealthLayerTargetEnum] = Field(default=None, description="""The downstream health-data layer this sidecar links into. Names the target so `health_layer_link_field` is interpreted against the right model.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['HealthLayerLinkage']} })
    health_layer_link_field: Optional[str] = Field(default=None, description="""Name of the field in the target health-data layer that carries `provenance_id`. For OMOP this is `external_exposure.exposure_source_value` (the default); other layers name their own field.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['HealthLayerLinkage']} })
    cohort_size_anchored: Optional[int] = Field(default=None, description="""Number of distinct persons this exposure record was extracted for. Helps downstream estimate the volume of health-layer rows the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['HealthLayerLinkage']} })
    cohort_size_anchored_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `cohort_size_anchored` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['HealthLayerLinkage']} })


class DepositMetadata(ConfiguredBaseModel):
    """
    Deposit-time slots required when the sidecar travels alongside a published FAIR object (Zenodo / Dryad / C-HER / etc.). Most slots are pulled from other modules; this class names the required-for-deposit subset and adds a few deposit-specific slots.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/health_layer'})

    deposit_doi: Optional[str] = Field(default=None, description="""DOI assigned by the deposit repository (e.g. Zenodo).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    deposit_doi_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `deposit_doi` is null (e.g. pre-deposit).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    deposit_repository: Optional[DepositRepositoryEnum] = Field(default=None, description="""Repository hosting the deposit.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    deposit_repository_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `deposit_repository` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    deposit_license_spdx: Optional[str] = Field(default=None, description="""SPDX identifier of the license under which the *derived* exposure record (not the source) is published.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    deposit_redistribution_constraints_inherited: Optional[list[str]] = Field(default=None, description="""Constraints from any input source that pass through to the deposit.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    recommended_citation: Optional[str] = Field(default=None, description="""One-line recommended citation derived from the slots above.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    dcat_distribution_url: Optional[str] = Field(default=None, description="""DCAT-compatible distribution URL for catalogue integration.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })
    dcat_distribution_url_missing_reason: Optional[MissingReasonEnum] = Field(default=None, description="""Reason `dcat_distribution_url` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata']} })


class EnvironmentalExposureRecord(ConfiguredBaseModel):
    """
    A single environmental-exposure record sidecar: the complete metadata graph that travels alongside a value (or value series) emitted by an upstream tool. Composes variable identity, spatial / temporal reference, source dataset, exposure model, uncertainty, linkage, tool run, provenance chain, optional derived-heat-metric methodology, health-data-layer linkage hooks, and FAIR-deposit metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/record',
         'instantiates': ['MicroschemaDefinition'],
         'slot_usage': {'location': {'aliases': ['spatial_reference'],
                                     'annotations': {'tier': {'tag': 'tier',
                                                              'value': 'core'}},
                                     'description': 'Spatial reference object '
                                                    'describing the native grid and '
                                                    'extraction. Bound to '
                                                    'SpatialReference (see '
                                                    'envar_spatial).',
                                     'inlined': True,
                                     'name': 'location',
                                     'range': 'SpatialReference'},
                        'methodology': {'aliases': ['exposure_model'],
                                        'annotations': {'tier': {'tag': 'tier',
                                                                 'value': 'core'}},
                                        'description': 'The exposure-model object '
                                                       'describing how values were '
                                                       'produced. Bound to '
                                                       'ExposureModel (see '
                                                       'envar_model). Other '
                                                       'methodology- adjacent concerns '
                                                       '(source dataset, tool run, '
                                                       'provenance chain, derived heat '
                                                       'metric) are surfaced as '
                                                       'separate envar-extension '
                                                       "slots; the profile's single "
                                                       '`methodology` slot is narrowed '
                                                       'to the model itself.',
                                        'inlined': True,
                                        'name': 'methodology',
                                        'range': 'ExposureModel'},
                        'observation_type': {'aliases': ['variable_identity'],
                                             'annotations': {'tier': {'tag': 'tier',
                                                                      'value': 'core'}},
                                             'description': 'The variable identity '
                                                            'object — what physical '
                                                            'quantity is being '
                                                            'captured. Bound to '
                                                            'VariableIdentity (see '
                                                            'envar_variable).',
                                             'inlined': True,
                                             'name': 'observation_type',
                                             'range': 'VariableIdentity'},
                        'subject': {'annotations': {'tier': {'tag': 'tier',
                                                             'value': 'core'}},
                                    'description': 'The patient or cohort the exposure '
                                                   'value is attached to. Carried as '
                                                   'an opaque identifier; PHI must not '
                                                   'appear here.',
                                    'name': 'subject',
                                    'range': 'string'},
                        'temporality': {'aliases': ['temporal_reference'],
                                        'annotations': {'tier': {'tag': 'tier',
                                                                 'value': 'core'}},
                                        'description': 'Temporal reference object '
                                                       'describing resolution, '
                                                       'aggregation, and day-boundary '
                                                       'convention. Bound to '
                                                       'TemporalReference (see '
                                                       'envar_temporal).',
                                        'inlined': True,
                                        'name': 'temporality',
                                        'range': 'TemporalReference'}},
         'tree_root': True})

    subject: str = Field(default=..., description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_type: VariableIdentity = Field(default=..., description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable).""", json_schema_extra = { "linkml_meta": {'aliases': ['variable_identity'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    location: SpatialReference = Field(default=..., description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial).""", json_schema_extra = { "linkml_meta": {'aliases': ['spatial_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    temporality: TemporalReference = Field(default=..., description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal).""", json_schema_extra = { "linkml_meta": {'aliases': ['temporal_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    methodology: ExposureModel = Field(default=..., description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Other methodology- adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots; the profile's single `methodology` slot is narrowed to the model itself.""", json_schema_extra = { "linkml_meta": {'aliases': ['exposure_model'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    schema_version: str = Field(default=..., description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_id: str = Field(default=..., description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    phi_status: PhiStatusEnum = Field(default=..., description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    source_dataset: SourceDataset = Field(default=..., description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    uncertainty: Optional[Uncertainty] = Field(default=None, description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    linkage_method: LinkageMethod = Field(default=..., description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    tool_run: ToolRun = Field(default=..., description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    derived_heat_metric: Optional[DerivedHeatMetric] = Field(default=None, description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord']} })


class MicroschemaDefinition(ConfiguredBaseModel):
    """
    A metaclass for classes that conform to the Microschema profile. Classes that instantiate this are designed for inline composition.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'must_be_inlined': {'tag': 'must_be_inlined', 'value': True},
                         'must_not_have_id_slot': {'tag': 'must_not_have_id_slot',
                                                   'value': True}},
         'comments': ['Classes instantiating this SHOULD NOT have identifier slots',
                      'Classes instantiating this SHOULD be used with inlined=true',
                      'Classes instantiating this MAY compose other microschemas via '
                      'attributes'],
         'from_schema': 'https://w3id.org/linkml/linkml-microschema-profile'})

    profile_version: Optional[str] = Field(default=None, description="""Version of microschema profile this conforms to""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })
    domain_of_use: Optional[list[str]] = Field(default=None, description="""Domains where this microschema is applicable""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })
    subject: str = Field(default=..., description="""Entity being measured, observed, or interviewed - person, animal, specimen, or environmental material""", json_schema_extra = { "linkml_meta": {'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_type: str = Field(default=..., description="""Question being asked, measurement being taken, quality being observed""", json_schema_extra = { "linkml_meta": {'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    location: str = Field(default=..., description="""Spatial metadata specifying where the observation was made - geolocation, place name, site id, environment, or biome""", json_schema_extra = { "linkml_meta": {'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    temporality: str = Field(default=..., description="""Temporal metadata specifying when an observation was made. This can be relative or absolute - datetime, age of person, season, or geologic era""", json_schema_extra = { "linkml_meta": {'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    methodology: str = Field(default=..., description="""Information about how an observation was made - method, instrument, reagent kit, statistical modifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_result: ValueMicroschemaDefinition = Field(default=..., description="""The outcome of the observation type - answer, value, result, determination""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })


class ValueMicroschemaDefinition(ConfiguredBaseModel):
    """
    A microschema representing a typed value with optional unit/system. Examples: Quantity, Timepoint, CodedValue, Range. This is the range for observation result
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'must_be_inlined': {'tag': 'must_be_inlined', 'value': True},
                         'must_not_have_id_slot': {'tag': 'must_not_have_id_slot',
                                                   'value': True}},
         'comments': ['Classes instantiating this SHOULD NOT have identifier slots',
                      'Classes instantiating this SHOULD be used with inlined=true',
                      'Classes instantiating this MAY compose other microschemas via '
                      'attributes'],
         'from_schema': 'https://w3id.org/linkml/linkml-microschema-profile'})

    pass


class Quantity(ConfiguredBaseModel):
    """
    A numerical value with unit
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-microschema-profile',
         'instantiates': ['ValueMicroschemaDefinition']})

    quantity_value: Decimal = Field(default=..., description="""The numeric value""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity']} })
    quantity_unit: str = Field(default=..., description="""Unit (UCUM, UO, QUDT, etc.)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity'], 'slot_uri': 'schema:unitCode'} })
    comparator: Optional[ComparatorEnum] = Field(default=None, description="""Comparison operator (less than, greater than, etc.) or exact if null""", json_schema_extra = { "linkml_meta": {'domain_of': ['Quantity']} })


class Timepoint(ConfiguredBaseModel):
    """
    A point in time, potentially relative
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-microschema-profile',
         'instantiates': ['ValueMicroschemaDefinition']})

    datetime: Optional[datetime ] = Field(default=None, description="""Absolute timestamp""", json_schema_extra = { "linkml_meta": {'domain_of': ['Timepoint']} })
    relative_to_event: Optional[str] = Field(default=None, description="""Event this is relative to""", json_schema_extra = { "linkml_meta": {'domain_of': ['Timepoint']} })
    offset: Optional[Quantity] = Field(default=None, description="""Offset from event (e.g., \"+3 days\")""", json_schema_extra = { "linkml_meta": {'domain_of': ['Timepoint']} })
    subject_age: Optional[Quantity] = Field(default=None, description="""Age of the subject at this timepoint (e.g., age when the event occurred)""", json_schema_extra = { "linkml_meta": {'domain_of': ['Timepoint']} })


class TimeInterval(ConfiguredBaseModel):
    """
    A period between two timepoints
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-microschema-profile',
         'instantiates': ['ValueMicroschemaDefinition']})

    interval_start: Optional[Timepoint] = Field(default=None, description="""Start of the interval""", json_schema_extra = { "linkml_meta": {'domain_of': ['TimeInterval']} })
    interval_end: Optional[Timepoint] = Field(default=None, description="""End of the interval""", json_schema_extra = { "linkml_meta": {'domain_of': ['TimeInterval']} })
    duration: Optional[Quantity] = Field(default=None, description="""Duration as alternative to start/end""", json_schema_extra = { "linkml_meta": {'domain_of': ['TimeInterval']} })


class CodedValue(ConfiguredBaseModel):
    """
    A value from a controlled vocabulary
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/linkml-microschema-profile',
         'instantiates': ['ValueMicroschemaDefinition']})

    code: str = Field(default=..., description="""The code value as a CURIE""", json_schema_extra = { "linkml_meta": {'domain_of': ['CodedValue']} })
    code_label: Optional[str] = Field(default=None, description="""Human-readable label for the code""", json_schema_extra = { "linkml_meta": {'domain_of': ['CodedValue']} })
    code_system: Optional[str] = Field(default=None, description="""The code system URI""", json_schema_extra = { "linkml_meta": {'domain_of': ['CodedValue']} })


class DailyMaxTemperatureRecord(EnvironmentalExposureRecord):
    """
    Canonical record for daily maximum 2 m air temperature (Tmax). Pins `standard_name = CF:air_temperature`, `cf_cell_methods = \"time: maximum\"`, `units_ucum = Cel`, `value_data_type = continuous_numeric`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/examples',
         'rules': [{'description': 'The variable identity for a '
                                   'DailyMaxTemperatureRecord must use the CF triple '
                                   '(air_temperature, time: maximum, Cel) and a '
                                   'continuous_numeric value_data_type. Enforce by '
                                   'pinning the inner slots when authoring an '
                                   'instance. (Placeholder rule; nested-object pinning '
                                   'is not yet expressed — see schema README "Design '
                                   'decisions".)',
                    'postconditions': {'slot_conditions': {'observation_type': {'any_of': [{'range': 'VariableIdentity'}],
                                                                                'name': 'observation_type'}}}}]})

    subject: str = Field(default=..., description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_type: VariableIdentity = Field(default=..., description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable).""", json_schema_extra = { "linkml_meta": {'aliases': ['variable_identity'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    location: SpatialReference = Field(default=..., description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial).""", json_schema_extra = { "linkml_meta": {'aliases': ['spatial_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    temporality: TemporalReference = Field(default=..., description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal).""", json_schema_extra = { "linkml_meta": {'aliases': ['temporal_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    methodology: ExposureModel = Field(default=..., description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Other methodology- adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots; the profile's single `methodology` slot is narrowed to the model itself.""", json_schema_extra = { "linkml_meta": {'aliases': ['exposure_model'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    schema_version: str = Field(default=..., description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_id: str = Field(default=..., description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    phi_status: PhiStatusEnum = Field(default=..., description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    source_dataset: SourceDataset = Field(default=..., description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    uncertainty: Optional[Uncertainty] = Field(default=None, description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    linkage_method: LinkageMethod = Field(default=..., description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    tool_run: ToolRun = Field(default=..., description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    derived_heat_metric: Optional[DerivedHeatMetric] = Field(default=None, description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord']} })


class DailyMinTemperatureRecord(EnvironmentalExposureRecord):
    """
    Canonical record for daily minimum 2 m air temperature (Tmin). Pins `standard_name = CF:air_temperature`, `cf_cell_methods = \"time: minimum\"`, `units_ucum = Cel`, `value_data_type = continuous_numeric`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/examples'})

    subject: str = Field(default=..., description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_type: VariableIdentity = Field(default=..., description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable).""", json_schema_extra = { "linkml_meta": {'aliases': ['variable_identity'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    location: SpatialReference = Field(default=..., description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial).""", json_schema_extra = { "linkml_meta": {'aliases': ['spatial_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    temporality: TemporalReference = Field(default=..., description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal).""", json_schema_extra = { "linkml_meta": {'aliases': ['temporal_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    methodology: ExposureModel = Field(default=..., description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Other methodology- adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots; the profile's single `methodology` slot is narrowed to the model itself.""", json_schema_extra = { "linkml_meta": {'aliases': ['exposure_model'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    schema_version: str = Field(default=..., description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_id: str = Field(default=..., description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    phi_status: PhiStatusEnum = Field(default=..., description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    source_dataset: SourceDataset = Field(default=..., description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    uncertainty: Optional[Uncertainty] = Field(default=None, description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    linkage_method: LinkageMethod = Field(default=..., description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    tool_run: ToolRun = Field(default=..., description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    derived_heat_metric: Optional[DerivedHeatMetric] = Field(default=None, description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord']} })


class WetBulbGlobeTemperatureOutdoorRecord(EnvironmentalExposureRecord):
    """
    Canonical record for outdoor WBGT under the Liljegren 2008 formulation. Pins `heat_metric_family = wbgt_outdoor`, `equation_variant = liljegren_2008`, `indoor_outdoor = outdoor`, `units_ucum = Cel`, `value_data_type = continuous_numeric`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/examples',
         'rules': [{'description': 'The DerivedHeatMetric inner object must pin '
                                   'heat_metric_family = wbgt_outdoor, '
                                   'equation_variant = liljegren_2008, and '
                                   'indoor_outdoor = outdoor.',
                    'postconditions': {'slot_conditions': {'derived_heat_metric': {'any_of': [{'range': 'DerivedHeatMetric'}],
                                                                                   'name': 'derived_heat_metric'}}}}],
         'slot_usage': {'derived_heat_metric': {'name': 'derived_heat_metric',
                                                'required': True}}})

    subject: str = Field(default=..., description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_type: VariableIdentity = Field(default=..., description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable).""", json_schema_extra = { "linkml_meta": {'aliases': ['variable_identity'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    location: SpatialReference = Field(default=..., description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial).""", json_schema_extra = { "linkml_meta": {'aliases': ['spatial_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    temporality: TemporalReference = Field(default=..., description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal).""", json_schema_extra = { "linkml_meta": {'aliases': ['temporal_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    methodology: ExposureModel = Field(default=..., description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Other methodology- adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots; the profile's single `methodology` slot is narrowed to the model itself.""", json_schema_extra = { "linkml_meta": {'aliases': ['exposure_model'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    schema_version: str = Field(default=..., description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_id: str = Field(default=..., description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    phi_status: PhiStatusEnum = Field(default=..., description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    source_dataset: SourceDataset = Field(default=..., description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    uncertainty: Optional[Uncertainty] = Field(default=None, description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    linkage_method: LinkageMethod = Field(default=..., description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    tool_run: ToolRun = Field(default=..., description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    derived_heat_metric: DerivedHeatMetric = Field(default=..., description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord']} })


class ExtremeHeatDayFlagRecord(EnvironmentalExposureRecord):
    """
    Canonical record for a daily binary extreme-heat-day flag, defined against a local 95th-percentile Tmax baseline. Pins `heat_metric_family = heat_wave_flag`, `value_data_type = binary_flag`, and requires the percentile-reference-period slots in DerivedHeatMetric to be populated.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/examples',
         'rules': [{'description': 'The DerivedHeatMetric inner object must pin '
                                   'heat_metric_family = heat_wave_flag, '
                                   'heat_wave_threshold_definition = percentile_local, '
                                   'and supply percentile_reference_period_start / '
                                   '_end and percentile_reference_geographic_scope.',
                    'postconditions': {'slot_conditions': {'derived_heat_metric': {'any_of': [{'range': 'DerivedHeatMetric'}],
                                                                                   'name': 'derived_heat_metric'}}}}],
         'slot_usage': {'derived_heat_metric': {'name': 'derived_heat_metric',
                                                'required': True}}})

    subject: str = Field(default=..., description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    observation_type: VariableIdentity = Field(default=..., description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable).""", json_schema_extra = { "linkml_meta": {'aliases': ['variable_identity'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    location: SpatialReference = Field(default=..., description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial).""", json_schema_extra = { "linkml_meta": {'aliases': ['spatial_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    temporality: TemporalReference = Field(default=..., description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal).""", json_schema_extra = { "linkml_meta": {'aliases': ['temporal_reference'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    methodology: ExposureModel = Field(default=..., description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Other methodology- adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots; the profile's single `methodology` slot is narrowed to the model itself.""", json_schema_extra = { "linkml_meta": {'aliases': ['exposure_model'],
         'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition']} })
    schema_version: str = Field(default=..., description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_id: str = Field(default=..., description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    phi_status: PhiStatusEnum = Field(default=..., description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    source_dataset: SourceDataset = Field(default=..., description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    uncertainty: Optional[Uncertainty] = Field(default=None, description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    linkage_method: LinkageMethod = Field(default=..., description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    tool_run: ToolRun = Field(default=..., description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    derived_heat_metric: DerivedHeatMetric = Field(default=..., description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord']} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
VariableIdentity.model_rebuild()
SpatialReference.model_rebuild()
TemporalReference.model_rebuild()
SourceDataset.model_rebuild()
ExposureModel.model_rebuild()
Uncertainty.model_rebuild()
ModelAggregateUncertainty.model_rebuild()
LinkageMethod.model_rebuild()
ToolRun.model_rebuild()
ProvenanceChain.model_rebuild()
DerivedHeatMetric.model_rebuild()
EquationInput.model_rebuild()
HealthLayerLinkage.model_rebuild()
DepositMetadata.model_rebuild()
EnvironmentalExposureRecord.model_rebuild()
MicroschemaDefinition.model_rebuild()
ValueMicroschemaDefinition.model_rebuild()
Quantity.model_rebuild()
Timepoint.model_rebuild()
TimeInterval.model_rebuild()
CodedValue.model_rebuild()
DailyMaxTemperatureRecord.model_rebuild()
DailyMinTemperatureRecord.model_rebuild()
WetBulbGlobeTemperatureOutdoorRecord.model_rebuild()
ExtremeHeatDayFlagRecord.model_rebuild()
