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
                    'This umbrella schema imports the fourteen modules that '
                    'together define the\n'
                    'EnVar metadata layer:\n'
                    '\n'
                    '  - envar_common         shared enums and slots\n'
                    '  - envar_variable       variable identity (CF, UCUM, '
                    'target-vocab concept, ECTO, ENVO)\n'
                    '  - envar_layout         data layout (column bindings into '
                    'the companion data file)\n'
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
                 'envar_layout',
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


class TableOrientationEnum(str, Enum):
    """
    How variables map onto columns in the companion data file.
    """
    wide = "wide"
    """
    One column per variable; column name identifies the variable.
    """
    long = "long"
    """
    One shared value column; the variable is discriminated by a row value in a variable column (tidy format).
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
         'see_also': ['https://cfconventions.org/standard-names.html',
                      'https://ucum.org/'],
         'slot_usage': {'concept_status': {'name': 'concept_status', 'required': True},
                        'standard_name': {'name': 'standard_name', 'required': True},
                        'units_ucum': {'name': 'units_ucum', 'required': True},
                        'value_data_type': {'name': 'value_data_type',
                                            'required': True},
                        'variable_name': {'name': 'variable_name', 'required': True}},
         'title': 'Variable Identity'})

    variable_name: str = Field(default=..., title="Variable Name", description="""Short machine-readable name for the variable, usually the name the upstream tool uses for it (e.g. `tmax`, `tmmx`, `air.2m`). Identity only — not necessarily the column header in the companion data file; that binding lives in `DataLayout.value_column` (see envar_layout).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Data tools give each measurement a '
                                                  'short nickname, like `tmax` for '
                                                  'maximum temperature. This is that '
                                                  'nickname, written down exactly as '
                                                  'the tool spells it, so you can go '
                                                  'back to the source and find the '
                                                  'same measurement again.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the handle under which '
                                                    'the upstream product knows the '
                                                    'variable (Daymet `tmax` vs '
                                                    'gridMET `tmmx`). Without it the '
                                                    'record cannot be traced back to '
                                                    "the source product's variable, "
                                                    'and a rerun cannot request the '
                                                    'same quantity from the tool.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'Daymet daily maximum air temperature variable',
                       'value': 'tmax'}]} })
    variable_label: Optional[str] = Field(default=None, title="Variable Label", description="""Human-readable label, e.g. \"daily maximum air temperature at 2 m\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A friendly, spelled-out name for '
                                                  'the measurement — like "daily '
                                                  'maximum air temperature at 2 m" '
                                                  'instead of the cryptic code `tmax` '
                                                  '— so anyone reading the record '
                                                  'knows what it is without decoding '
                                                  'jargon.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Terse tool codes like `tmmx` are '
                                                    'easy to misread (maximum vs mean) '
                                                    'and force readers to consult '
                                                    'external tool documentation. A '
                                                    'plain-language label lets a human '
                                                    'verify at a glance that the '
                                                    'record describes the intended '
                                                    'quantity.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'value': 'daily maximum air temperature at 2 m'}]} })
    standard_name: str = Field(default=..., title="Standard Name", description="""The standard-name identifier for the physical quantity, as a CURIE so the schema privileges no single naming authority. Use a CF Convention Standard Name where one exists (`CF:air_temperature`, `CF:relative_humidity`); for health-relevant quantities CF does not define (e.g. Heat Index, WBGT), mint a term in the project registry (`ENVAR:heat_index`) or reuse an ontology term (`ECTO:...`). The prefix carries the authority; the slot name does not. Mandatory.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Different tools use different '
                                                  'nicknames for the same thing, so '
                                                  'scientific communities maintain '
                                                  'shared official names for physical '
                                                  'quantities (like '
                                                  '"air_temperature"). Tagging the '
                                                  'record with the official name lets '
                                                  'computers tell that two datasets '
                                                  'measure the same thing, no matter '
                                                  'what each dataset called it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the cross-agency '
                                                    'identifier that makes the '
                                                    'variable interoperable: without '
                                                    'it, `tmax` from one product and '
                                                    '`tmmx` from another cannot be '
                                                    'recognised by machines as the '
                                                    'same physical quantity, so '
                                                    'records cannot be pooled or '
                                                    'harmonised across studies.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'CF Standard Name for the Daymet daily Tmax '
                                      'scenario',
                       'value': 'CF:air_temperature'},
                      {'description': 'CF Standard Name for the ACAG PM2.5 scenario',
                       'value': 'CF:mass_concentration_of_pm2p5_ambient_aerosol_particles_in_air'}],
         'see_also': ['https://cfconventions.org/standard-names.html',
                      'https://obofoundry.org/ontology/ecto.html'],
         'slot_uri': 'dcterms:subject'} })
    cf_cell_methods: Optional[str] = Field(default=None, title="CF Cell Methods", description="""CF `cell_methods` string describing how the value summarises sub-period values, e.g. `time: maximum` for Tmax, `time: mean` for daily mean.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A "daily temperature" value could '
                                                  "be the day's highest reading, its "
                                                  'average, or its lowest — very '
                                                  'different numbers. This short '
                                                  'standard phrase (like "time: '
                                                  'maximum") records which one it is, '
                                                  'in the exact wording that '
                                                  'climate-data software already '
                                                  'understands.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A daily maximum and a daily mean '
                                                    'of the same quantity carry the '
                                                    'same standard name and units; '
                                                    'only the aggregation statement '
                                                    'tells them apart. Keeping the '
                                                    'verbatim CF string also enables '
                                                    'round-tripping against CF/NetCDF '
                                                    'source products and the '
                                                    'CF-consistency triple check over '
                                                    '`standard_name` + '
                                                    '`cf_cell_methods` + '
                                                    '`units_ucum`.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'comments': ['Deliberately CF-specific — do not generalise. The '
                      'vocabulary-neutral capture of aggregation semantics already '
                      'exists as the required '
                      '`TemporalReference.temporal_aggregation_method` enum '
                      '(envar_temporal), which maps 1:1 to the temporal part of '
                      '`cell_methods`; that enum is what machines should reason over. '
                      'This slot instead preserves the *verbatim* CF expression. '
                      '`cell_methods` is a structured mini-language (multi-axis forms '
                      'like `area: mean time: maximum`, `within`/`over` qualifiers, '
                      '`where` clauses) with no cross-vocabulary equivalent, so a '
                      '"generalised" slot would be either a free string of unspecified '
                      'syntax (losing machine-readability) or a newly minted EnVar '
                      'aggregation grammar with no tooling support. Keeping the '
                      'literal string also enables round-tripping against CF/NetCDF '
                      'source products and the CF-consistency triple check over '
                      '`standard_name` + `cf_cell_methods` + `units_ucum` (SPEC.md, '
                      'validation rule 5). Contrast `standard_name`, which *was* '
                      'generalised to a CURIE — that works because it is an '
                      'identifier, and prefixes provide a standard generalisation '
                      'mechanism; no such mechanism exists for expressions.'],
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'daily maximum (Tmax)', 'value': 'time: maximum'},
                      {'description': 'mean over the aggregation period (e.g. '
                                      'annual-mean PM2.5)',
                       'value': 'time: mean'}],
         'see_also': ['https://cfconventions.org/cf-conventions/cf-conventions.html#cell-methods']} })
    units_ucum: str = Field(default=..., title="Units (UCUM)", description="""The unit expressed in UCUM syntax, e.g. `Cel` for degrees Celsius, `K` for Kelvin, `ug/m3` for PM2.5 mass concentration.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'UCUM is a compact, machine-readable '
                                                  'spelling of the unit — `Cel` for '
                                                  'degrees Celsius, `ug/m3` for '
                                                  'micrograms per cubic metre — so '
                                                  'software can convert °C to °F or '
                                                  'check units automatically without '
                                                  'guessing what a human-written unit '
                                                  'string means.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A number without units is '
                                                    'uninterpretable — a value of 35 '
                                                    'could be °C or °F, a '
                                                    'factor-of-1.8 error in an '
                                                    'exposure analysis. UCUM is the '
                                                    'machine-readable form that '
                                                    "health-data layers (e.g. OMOP's "
                                                    'unit_concept_id) align to, so '
                                                    'omitting it also blocks automated '
                                                    'unit conversion and downstream '
                                                    'integration.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'degrees Celsius (Daymet Tmax)', 'value': 'Cel'},
                      {'description': 'micrograms per cubic metre (PM2.5 mass '
                                      'concentration)',
                       'value': 'ug/m3'}],
         'see_also': ['https://ucum.org/']} })
    units_display: Optional[str] = Field(default=None, title="Display Units", description="""Human-readable unit string for display purposes, e.g. `°C`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The pretty version of the unit for '
                                                  'people to read, like "°C". The '
                                                  'machine version (`Cel`) is stored '
                                                  'separately; this one exists purely '
                                                  'for showing on screen or in print.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Keeps human-facing output '
                                                    '(tables, plots, reports) readable '
                                                    'without every consumer having to '
                                                    'translate UCUM codes; omitting it '
                                                    'risks each tool rendering the '
                                                    'unit differently or mislabelling '
                                                    'axes.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'value': '°C'}]} })
    target_concept_vocabulary: Optional[str] = Field(default=None, title="Target Concept Vocabulary", description="""The downstream health-data vocabulary that `target_concept_id` and `concept_status` refer to, e.g. `omop` (OHDSI Standardised Vocabulary), `bdc` (BioData Catalyst). Names the vocabulary so the schema privileges no single health-data layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health databases each keep their '
                                                  'own catalogue of codes for the '
                                                  'things they record. This slot says '
                                                  "which catalogue the record's "
                                                  'health-data code (and its status) '
                                                  'comes from — for example the OMOP '
                                                  'catalogue used by many hospital '
                                                  'research databases.'},
                         'justification': {'tag': 'justification',
                                           'value': '`target_concept_id` and '
                                                    '`concept_status` are meaningless '
                                                    'without knowing which vocabulary '
                                                    'they refer to; naming it '
                                                    'explicitly keeps the record '
                                                    'portable across health-data '
                                                    'layers (OMOP, BDC, ...) instead '
                                                    'of silently assuming one.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'OHDSI Standardised Vocabulary (OMOP CDM)',
                       'value': 'omop'}],
         'see_also': ['https://athena.ohdsi.org/',
                      'https://biodatacatalyst.nhlbi.nih.gov/']} })
    target_concept_id: Optional[str] = Field(default=None, title="Target Concept Identifier", description="""Concept identifier for the variable in the vocabulary named by `target_concept_vocabulary` (e.g. an OHDSI concept_id). Nullable with reason for environmental variables that lack coverage today.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health databases store everything '
                                                  'under numeric codes from a shared '
                                                  'catalogue. This is that code for '
                                                  'the environmental measurement, when '
                                                  'one exists, so the exposure value '
                                                  'can sit alongside clinical data '
                                                  'under an identifier the database '
                                                  'already knows.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the hook that lets the '
                                                    'environmental value land in a '
                                                    'health database as a recognised '
                                                    'concept. Recording it — or its '
                                                    'documented absence — shows '
                                                    'whether the vocabulary binding '
                                                    'was attempted and against what, '
                                                    'instead of leaving the linkage '
                                                    'silent and unreproducible.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'illustrative OHDSI concept_id; in the canonical '
                                      'Tmax and PM2.5 scenarios this slot is null with '
                                      'a missing reason',
                       'value': '2005200123'}],
         'see_also': ['https://athena.ohdsi.org/']} })
    target_concept_id_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Concept ID Is Missing", description="""Reason `target_concept_id` is null. Distinguishes \"no concept yet exists in the target vocabulary\" from \"the pipeline did not resolve it\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When a code is missing, it matters '
                                                  'why. This slot records the reason — '
                                                  'for example that no such code has '
                                                  'been invented yet — so an empty '
                                                  'field is not mistaken for a '
                                                  'processing mistake.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a stated reason, a null '
                                                    '`target_concept_id` is ambiguous: '
                                                    'downstream users cannot tell a '
                                                    'genuine vocabulary gap from a '
                                                    'pipeline that simply failed to '
                                                    'look the concept up, and so '
                                                    'cannot decide whether to fix the '
                                                    'data or request a new concept.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    concept_status: ConceptStatusEnum = Field(default=..., title="Concept Status", description="""Status of this variable's coverage in the target health-data vocabulary (`existing` / `proposed` / `gap`). Makes the vocabulary gap explicit rather than silent. Required.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A simple status flag saying whether '
                                                  'the health-data catalogue already '
                                                  'has a code for this measurement, '
                                                  'has one in the works, or has '
                                                  'nothing yet. It turns a silent gap '
                                                  'into an explicit, reportable fact.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A downstream system must know '
                                                    'whether to expect a concept id. '
                                                    'The explicit '
                                                    'existing/proposed/gap status '
                                                    'makes vocabulary gaps visible and '
                                                    'countable rather than silently '
                                                    'null — which is what drives '
                                                    'vocabulary-extension requests for '
                                                    'environmental variables.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'no OMOP concept exists yet for daily Tmax',
                       'value': 'gap'}]} })
    concept_mappings: Optional[list[str]] = Field(default=None, title="Concept Cross-References", description="""Cross-references binding this variable to other vocabularies and ontologies, each as a CURIE. One generic list rather than a slot per standard, so adding a vocabulary is a new prefix, not a schema change. Examples: `ECTO:0000012` (Environmental Conditions, Treatments and Exposures Ontology — cross-Monarch / cross-CHORDS alignment), `ENVO:01000339` (Environment Ontology — material or process exposed to), `LOINC:...` / `SNOMED:...` (where the variable has clinical coverage). Note: the *primary* downstream health-data binding, with its `existing` / `proposed` / `gap` status, stays in the structured `target_concept_*` slots — this list is for additional, status-free cross-references.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Different scientific communities '
                                                  'keep different dictionaries of '
                                                  'concepts. This is a list of "also '
                                                  'known as" links pointing to the '
                                                  'matching entries in those '
                                                  'dictionaries, so people searching '
                                                  'any of them can still find this '
                                                  'measurement.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Cross-references to ontologies '
                                                    '(ECTO, ENVO) and clinical codes '
                                                    '(LOINC, SNOMED) let the variable '
                                                    'be found and aligned across '
                                                    'projects and communities; without '
                                                    'them, cross-study harmonisation '
                                                    'has to be redone by hand. '
                                                    'Enrichment only — not needed to '
                                                    'reproduce the value.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'exposure to temperature (ECTO) — one element of '
                                      'the cross-reference list for the Daymet daily '
                                      'Tmax scenario',
                       'value': 'ECTO:0000012'},
                      {'description': 'temperature of air (ENVO) — a second element of '
                                      'the same cross-reference list',
                       'value': 'ENVO:03000049'}],
         'see_also': ['https://obofoundry.org/ontology/ecto.html',
                      'https://obofoundry.org/ontology/envo.html',
                      'https://loinc.org/']} })
    value_data_type: DataTypeEnum = Field(default=..., title="Value Data Type", description="""The data type of the stored exposure value.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Says what kind of value to expect: '
                                                  'a decimal number that can take any '
                                                  'value (like a temperature), a '
                                                  'yes/no flag, or a category. '
                                                  'Software needs this to know how to '
                                                  'read and summarise the data '
                                                  'correctly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Tells consumers how to parse and '
                                                    'analyse the values — continuous '
                                                    'numbers, categories, and flags '
                                                    'need different statistics and '
                                                    'storage. Omitting it forces '
                                                    'guessing from the data, which '
                                                    'fails on ambiguous cases like 0/1 '
                                                    'columns (count, flag, or '
                                                    'category?).'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'value': 'continuous_numeric'}]} })
    value_range_plausible_min: Optional[float] = Field(default=None, title="Plausible Minimum Value", description="""Physical / domain lower bound for plausible values (e.g. -50 °C for ambient Tmax). Not a hard validation bound; sanity-check signal.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The lowest value that would still '
                                                  'make physical sense — for example '
                                                  '-50 °C for outdoor air temperature. '
                                                  'Anything below it is probably an '
                                                  'error; this is a warning signal, '
                                                  'not a hard rule.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Gives automated quality checks a '
                                                    'sanity band: without it, unit '
                                                    'mix-ups and corrupted values '
                                                    '(e.g. a Tmax of 350 from '
                                                    'unconverted Kelvin) pass silently '
                                                    'into downstream analyses.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'plausible lower bound for ambient Tmax in °C',
                       'value': '-50'}]} })
    value_range_plausible_max: Optional[float] = Field(default=None, title="Plausible Maximum Value", description="""Physical / domain upper bound for plausible values (e.g. 60 °C for ambient Tmax).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The highest value that would still '
                                                  'make physical sense — for example '
                                                  '60 °C for outdoor air temperature. '
                                                  'Anything above it likely signals a '
                                                  'unit mix-up or a data error worth '
                                                  'investigating.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Together with the plausible '
                                                    'minimum, this gives automated '
                                                    'quality checks a sanity band: '
                                                    'without it, unit mix-ups and '
                                                    'corrupted values slip silently '
                                                    'past validation into exposure '
                                                    'analyses.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['VariableIdentity'],
         'examples': [{'description': 'plausible upper bound for ambient Tmax in °C',
                       'value': '60'}]} })


class DataLayout(ConfiguredBaseModel):
    """
    How the companion data file (CSV / parquet) is laid out and how this record's values are located inside it. Separates the file-layout concern from variable identity: `VariableIdentity.variable_name` says what the variable is; `DataLayout` says which column (and, for long format, which rows) carry its values. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/layout',
         'slot_usage': {'table_orientation': {'name': 'table_orientation',
                                              'required': True},
                        'value_column': {'name': 'value_column', 'required': True}},
         'title': 'Data Layout'})

    table_orientation: TableOrientationEnum = Field(default=..., title="Table Orientation", description="""Whether the companion file is wide (one column per variable) or long (one `value` column, variables discriminated by row). Required.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Wide means one column per '
                                                  'measurement type (a `tmax` column, '
                                                  'a `vp` column, and so on); long '
                                                  'means one row per measurement, with '
                                                  'a shared `value` column and a label '
                                                  'column saying which measurement '
                                                  'each row is. Long is also known as '
                                                  '"tidy" format.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Every other column binding in '
                                                    'this class is read relative to '
                                                    'the orientation: in a wide file '
                                                    '`value_column` names a '
                                                    'variable-specific column, in a '
                                                    'long file it names a shared '
                                                    'column whose rows must be '
                                                    'filtered. Without this flag a '
                                                    'consumer cannot interpret the '
                                                    'bindings and so cannot reliably '
                                                    "locate this record's values in "
                                                    'the companion file.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['DataLayout'],
         'examples': [{'description': 'one column per variable, e.g. a `tmax` column '
                                      'in a Daymet extract',
                       'value': 'wide'},
                      {'description': 'tidy format with a shared `value` column, e.g. '
                                      'tract-level PM2.5',
                       'value': 'long'}],
         'see_also': ['https://doi.org/10.18637/jss.v059.i10']} })
    value_column: str = Field(default=..., title="Value Column", description="""Name of the column carrying this record's exposure values, e.g. `tmax` in a wide file or `value` in a long file. Required.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This is simply the name of the '
                                                  'spreadsheet column where the actual '
                                                  'numbers live — for example a column '
                                                  'headed `tmax` holding daily maximum '
                                                  'temperatures, or a generic column '
                                                  'headed `value` in a long table.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The record deliberately carries '
                                                    'no inline observation result — '
                                                    'the values live only in the '
                                                    'companion CSV/parquet file. '
                                                    'Without this column binding, a '
                                                    'validator or downstream pipeline '
                                                    'has no way to find the values the '
                                                    'sidecar describes, so the sidecar '
                                                    'is unverifiable and the data '
                                                    'unusable.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['DataLayout'],
         'examples': [{'description': "wide file — the variable's own column carries "
                                      'the values',
                       'value': 'tmax'},
                      {'description': 'long file — the shared value column',
                       'value': 'value'}]} })
    variable_column: Optional[str] = Field(default=None, title="Variable Column", description="""For long orientation: name of the column that discriminates variables (e.g. `variable`). Not applicable to wide files.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'In a long table there is a column — '
                                                  'often literally called `variable` — '
                                                  'that says what each row measures '
                                                  '(`tmax`, `vp`, ...). This slot '
                                                  'names that column. Wide files do '
                                                  'not have one, which is why this '
                                                  'only applies to long orientation.'},
                         'justification': {'tag': 'justification',
                                           'value': 'In a long file many variables '
                                                    'share one value column and are '
                                                    'told apart only by a '
                                                    'discriminator column. Without '
                                                    'naming that column, a consumer '
                                                    "cannot separate this record's "
                                                    'variable from every other '
                                                    'variable in the file, so the '
                                                    'value binding is ambiguous for '
                                                    'all long-format data.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DataLayout'],
         'examples': [{'value': 'variable'}],
         'see_also': ['https://doi.org/10.18637/jss.v059.i10']} })
    variable_key: Optional[str] = Field(default=None, title="Variable Key", description="""For long orientation: the value in `variable_column` that selects this record's rows (e.g. `tmax`). Often, but not necessarily, equal to `VariableIdentity.variable_name`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This is the label to filter on: '
                                                  'keep only the rows where the '
                                                  'variable column says, for example, '
                                                  '`tmax`, and you have exactly this '
                                                  "record's measurements. It usually "
                                                  "matches the variable's short name, "
                                                  'but does not have to.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Knowing which column '
                                                    'discriminates variables is not '
                                                    'enough — a consumer also needs '
                                                    'the label value that selects this '
                                                    "record's rows. Without the key, "
                                                    'every row of a long file is a '
                                                    "candidate and this record's "
                                                    'values cannot be filtered out of '
                                                    'the shared value column.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DataLayout'],
         'examples': [{'description': 'selects the PM2.5 rows in a long tract-level '
                                      'file',
                       'value': 'pm25_annual'}],
         'see_also': ['https://doi.org/10.18637/jss.v059.i10']} })
    subject_column: Optional[str] = Field(default=None, title="Subject Column", description="""Name of the column carrying the opaque subject / cohort identifier the record-level `subject` refers to (e.g. `subject_id`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This names the ID column that says '
                                                  'who (or where) each row belongs to '
                                                  '— a patient identifier like '
                                                  '`subject_id`, or a place identifier '
                                                  'like a census-tract code.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The whole point of an exposure '
                                                    'sidecar is to be joined back to a '
                                                    'health-data layer. Without '
                                                    'knowing which column carries the '
                                                    'subject or cohort identifier, the '
                                                    'values cannot be attached to the '
                                                    'people or places the record-level '
                                                    '`subject` refers to, and the '
                                                    'linkage step becomes guesswork.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DataLayout'],
         'examples': [{'description': 'patient-level extract', 'value': 'subject_id'},
                      {'description': 'census-tract-level extract',
                       'value': 'tract_id'}]} })
    time_column: Optional[str] = Field(default=None, title="Time Column", description="""Name of the column carrying the observation date / timestamp (e.g. `date`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This names the column that gives '
                                                  'each measurement its "when" — a '
                                                  '`date` column for daily data, or a '
                                                  '`year` column for annual '
                                                  'summaries.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without knowing which column '
                                                    'carries the date or timestamp, '
                                                    'each value cannot be placed in '
                                                    'time, so exposure values cannot '
                                                    'be aligned with clinical events — '
                                                    "which day's exposure goes with "
                                                    'which health record — and any lag '
                                                    'or window analysis is '
                                                    'impossible.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DataLayout'],
         'examples': [{'description': 'daily data', 'value': 'date'},
                      {'description': 'annual aggregate', 'value': 'year'}]} })
    value_uncertainty_column: Optional[str] = Field(default=None, title="Per-Value Uncertainty Column", description="""Name of the column carrying per-value uncertainty (e.g. `pm_se`, `tmax_stderr`). Its semantics (uncertainty type, units) live in the Uncertainty microschema. Null with reason for products whose per-value uncertainty exists upstream but is not surfaced.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some datasets include a "plus or '
                                                  'minus" column next to each value — '
                                                  'an estimate of how far off each '
                                                  'number might be. This slot names '
                                                  'that column so the uncertainty '
                                                  'travels with the data instead of '
                                                  'being lost.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Products like Daymet ship '
                                                    'per-value standard errors that '
                                                    'most pipelines silently drop. '
                                                    'Without this binding, downstream '
                                                    'analyses cannot find or propagate '
                                                    'the measurement error attached to '
                                                    'each value, and dropped '
                                                    'uncertainty is indistinguishable '
                                                    'from uncertainty that never '
                                                    'existed.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DataLayout'],
         'examples': [{'value': 'tmax_stderr'}]} })
    value_uncertainty_column_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Uncertainty Column Is Missing", description="""Reason `value_uncertainty_column` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When there is no uncertainty '
                                                  'column, this slot says why — for '
                                                  'example "the upstream product does '
                                                  'not provide one" versus "it exists '
                                                  'upstream but was not extracted".'},
                         'justification': {'tag': 'justification',
                                           'value': 'A bare null cannot be audited: it '
                                                    'could mean the source has no '
                                                    'per-value uncertainty, the '
                                                    'pipeline dropped it, or the '
                                                    'producer forgot to record it. '
                                                    'Stating the reason makes the '
                                                    'absence deliberate and lets '
                                                    'reviewers tell "unavailable" from '
                                                    '"lost", which matters for '
                                                    'reproducing the extraction.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DataLayout'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    quality_flag_column: Optional[str] = Field(default=None, title="Quality Flag Column", description="""Name of any per-value QA flag column. CF `ancillary_variables` analogue; the flag vocabulary lives in the Uncertainty microschema.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A quality flag column is like a '
                                                  'traffic light next to each number — '
                                                  'good, suspect, or bad — recorded by '
                                                  'the data producer. This slot names '
                                                  'that column; what the flag codes '
                                                  'mean is described in the '
                                                  'Uncertainty microschema.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without knowing where the '
                                                    'per-value QA flags live, '
                                                    'consumers cannot filter or '
                                                    'down-weight values the producer '
                                                    'already marked as suspect, so '
                                                    'known-bad measurements flow '
                                                    'silently into analyses.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DataLayout'],
         'examples': [{'description': 'per-value QA flag column accompanying a `tmax` '
                                      'value column',
                       'value': 'tmax_qc'}],
         'see_also': ['https://cfconventions.org/']} })
    quality_flag_column_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Quality Flag Column Is Missing", description="""Reason `quality_flag_column` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When there is no quality-flag '
                                                  'column, this slot says why it is '
                                                  'absent — for example because the '
                                                  'source dataset simply does not '
                                                  'publish quality flags.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a stated reason, a '
                                                    'missing QA-flag column is '
                                                    'ambiguous: the source may publish '
                                                    'no flags, or the pipeline may '
                                                    'have dropped them. The reason '
                                                    'turns a silent gap into a '
                                                    'documented decision that a '
                                                    'reviewer can check against the '
                                                    'upstream product.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DataLayout'],
         'examples': [{'value': 'not_provided_by_source'}]} })


class SpatialReference(ConfiguredBaseModel):
    """
    Spatial provenance of an environmental exposure value: the native grid / footprint of the source product, the CRS, the geographic extent, the extraction rule used to attach a value to a patient location, and the target geography type. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/spatial',
         'see_also': ['https://epsg.io/',
                      'https://en.wikipedia.org/wiki/Coordinate_reference_system'],
         'slot_usage': {'crs': {'name': 'crs', 'required': True},
                        'extraction_method': {'name': 'extraction_method',
                                              'required': True},
                        'target_geography_type': {'name': 'target_geography_type',
                                                  'required': True}},
         'title': 'Spatial Reference'})

    native_spatial_resolution_m: Optional[float] = Field(default=None, title="Native Spatial Resolution (m)", description="""Native spatial resolution of the source product in metres. Daymet = 1000, GridMET ≈ 4000, NARR ≈ 32000.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Gridded environmental data divides '
                                                  'the world into square tiles, like '
                                                  'pixels in a photo, and reports one '
                                                  'value per tile. This field says how '
                                                  'wide each tile is in metres — small '
                                                  'tiles give a sharp picture of local '
                                                  'conditions, big tiles give a blurry '
                                                  'average over a large area.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Exposure misclassification scales '
                                                    'directly with cell size: a value '
                                                    'from a 32 km NARR cell averages '
                                                    'over an entire metro area while a '
                                                    '1 km Daymet cell resolves a '
                                                    'neighbourhood. Without the '
                                                    'resolution, downstream users '
                                                    'cannot judge how precise a '
                                                    'per-patient exposure really is or '
                                                    "whether two studies' values are "
                                                    'comparable.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'Daymet V4 1 km grid', 'value': '1000'}],
         'see_also': ['https://daymet.ornl.gov/',
                      'https://www.climatologylab.org/gridmet.html',
                      'https://psl.noaa.gov/data/gridded/data.narr.html']} })
    native_spatial_resolution_descriptor: Optional[str] = Field(default=None, title="Native Resolution Descriptor", description="""Human-readable label for the native resolution, e.g. \"1 km regular grid\", \"H3 hex zoom 8\", \"census tract polygon\", \"point station\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A short plain-English phrase saying '
                                                  'what the map data actually looks '
                                                  'like — evenly spaced square tiles, '
                                                  'honeycomb-shaped cells, irregular '
                                                  'neighbourhood outlines, or '
                                                  'individual measuring stations '
                                                  'dotted around.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The numeric resolution alone '
                                                    'cannot distinguish a regular grid '
                                                    'from hex cells, polygons, or '
                                                    'point stations, and these layouts '
                                                    'imply different extraction and '
                                                    'error behaviour. Omitting the '
                                                    'label leaves the geometry of the '
                                                    'source data ambiguous even when '
                                                    'the cell size is known.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'Daymet V4 native grid',
                       'value': '1 km regular grid'}]} })
    crs: str = Field(default=..., title="Coordinate Reference System (CRS)", description="""Coordinate reference system as an EPSG identifier or PROJ string. Mandatory. E.g. `EPSG:4326` for Daymet, `EPSG:5072` for NARR Lambert Conformal Conic.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A coordinate reference system is '
                                                  'the agreed way of turning numbers '
                                                  'into places on the Earth — the same '
                                                  'pair of coordinates means different '
                                                  'spots under different systems. '
                                                  'Naming the system (usually as a '
                                                  'short EPSG code) tells software '
                                                  'exactly which convention the '
                                                  'numbers follow.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the CRS the grid cannot '
                                                    'be placed on the Earth correctly: '
                                                    'the same coordinate pair points '
                                                    'to different physical locations '
                                                    'under different reference '
                                                    'systems, so a mismatched or '
                                                    'missing CRS silently shifts every '
                                                    'location and attaches exposure '
                                                    'values to the wrong places.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'WGS 84, used by the Daymet and ACAG PM2.5 '
                                      'scenarios',
                       'value': 'EPSG:4326'}],
         'see_also': ['https://epsg.io/', 'https://proj.org/']} })
    spatial_extent_bbox: Optional[list[float]] = Field(default=None, title="Product Bounding Box", description="""Bounding box of the source *product* (not the extracted subset), as `[min_lon, min_lat, max_lon, max_lat]`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A bounding box is a rectangle drawn '
                                                  'on the map that just barely '
                                                  'contains all the data — four '
                                                  'numbers giving its western, '
                                                  'southern, eastern, and northern '
                                                  'edges. Anything outside that '
                                                  'rectangle was never covered by the '
                                                  'dataset in the first place.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The product footprint '
                                                    'distinguishes "no value here" '
                                                    '(the location lies outside the '
                                                    "product's coverage) from "
                                                    '"missing value" (the product '
                                                    'covers it but the value is '
                                                    'absent). Without it, '
                                                    'out-of-extent patients look like '
                                                    'data gaps and can be silently '
                                                    'misinterpreted.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'Daymet V4 product bounding box (CONUS + Hawaii '
                                      '+ Puerto Rico); one float per list element, '
                                      'ordered min_lon, min_lat, max_lon, max_lat',
                       'value': '[-131.104, 14.075, -52.95, 53.038]'}],
         'see_also': ['https://datatracker.ietf.org/doc/html/rfc7946#section-5']} })
    spatial_extent_descriptor: Optional[str] = Field(default=None, title="Product Extent Description", description="""Human-readable description of the product extent, e.g. \"CONUS + Hawaii + Puerto Rico\", \"global land surface 60°S-80°N\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A plain-English description of '
                                                  'where in the world the dataset has '
                                                  'data — for example "the continental '
                                                  'United States plus Hawaii and '
                                                  'Puerto Rico" — so you can tell at a '
                                                  'glance whether your study area is '
                                                  'covered.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The numeric bounding box is '
                                                    'precise but opaque; a '
                                                    'human-readable extent lets '
                                                    'reviewers and data users '
                                                    'sanity-check coverage at a glance '
                                                    '(e.g. spotting that Alaska is not '
                                                    'included) without decoding '
                                                    'coordinates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'Daymet V4 product extent',
                       'value': 'CONUS + Hawaii + Puerto Rico'}]} })
    extraction_method: ExtractionMethodEnum = Field(default=..., title="Extraction Method", description="""How a gridded value was extracted at the patient's coordinates. Default for DeGAUSS daymet / narr is `inverse_distance_weighted_4_nearest_cells`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': "A patient's home almost never sits "
                                                  'exactly at the centre of a data '
                                                  'tile, so a rule is needed to pick '
                                                  'or blend nearby tile values into '
                                                  'one number for that spot — take the '
                                                  'closest tile, average the four '
                                                  'nearest ones, and so on. This field '
                                                  'records which rule was used.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the single biggest lever '
                                                    'in turning a grid into a '
                                                    'per-person value: different '
                                                    'extraction methods yield '
                                                    'different exposure values at the '
                                                    'very same point. If the method is '
                                                    'unknown, exposure values are not '
                                                    'reproducible and cannot be '
                                                    'compared across studies or tool '
                                                    'runs.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'DeGAUSS default for point extraction (Daymet '
                                      'Tmax scenario)',
                       'value': 'inverse_distance_weighted_4_nearest_cells'},
                      {'description': 'polygon aggregation (ACAG PM2.5 tract scenario)',
                       'value': 'area_weighted_polygon_mean'}],
         'see_also': ['https://degauss.org/']} })
    extraction_buffer_m: Optional[float] = Field(default=None, title="Extraction Buffer Radius (m)", description="""Radius of any spatial buffer applied (e.g. greenspace at 500 / 1500 / 2500 m). Null when no buffer is applied.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some exposures are summarised over '
                                                  "a circle drawn around the patient's "
                                                  'home rather than at the exact '
                                                  'address — for example, how much '
                                                  'green space lies within walking '
                                                  'distance. This field gives the '
                                                  'radius of that circle in metres; a '
                                                  'bigger circle averages over more '
                                                  'surroundings.'},
                         'justification': {'tag': 'justification',
                                           'value': 'For buffer-based strategies the '
                                                    'radius is a hyperparameter that '
                                                    'changes the assigned exposure — '
                                                    'greenspace within 500 m and '
                                                    'within 2500 m of a home are '
                                                    'different quantities. Omitting it '
                                                    'makes buffer-derived values '
                                                    'unreproducible and incomparable '
                                                    'across analyses.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': '500 m greenspace buffer; null in the Daymet '
                                      'Tmax scenario (no buffer)',
                       'value': '500'}]} })
    extraction_buffer_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Buffer Radius Is Missing", description="""Reason `extraction_buffer_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the circle-radius field above '
                                                  'is left empty, this field says why '
                                                  '— most often because no circle was '
                                                  'drawn at all and the value was '
                                                  'taken straight at the address. It '
                                                  'turns a silent blank into an '
                                                  'explicit, trustworthy statement.'},
                         'justification': {'tag': 'justification',
                                           'value': 'An empty buffer field is '
                                                    'ambiguous: it could mean no '
                                                    'buffer was used or that the '
                                                    'radius was simply not recorded. '
                                                    'Stating the reason makes the '
                                                    'absence deliberate and checkable, '
                                                    'so validators and reviewers do '
                                                    'not flag a legitimate point '
                                                    'extraction as incomplete '
                                                    'metadata.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'no buffer is used for point extraction (Daymet '
                                      'Tmax scenario)',
                       'value': 'not_applicable'}]} })
    population_weighting_source: Optional[str] = Field(default=None, title="Population Weighting Source", description="""Census vintage used for population weighting (e.g. the Spangler et al. WBGT product is population-weighted from gridMET). Null when no weighting is applied.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some datasets average their tiles '
                                                  'by giving more weight to places '
                                                  'where more people live, so the '
                                                  'number reflects what a typical '
                                                  'resident experiences rather than a '
                                                  'plain average over land. This field '
                                                  'names the population map (and its '
                                                  'year) that was used for that '
                                                  'weighting.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Population-weighted values depend '
                                                    'on which population dataset and '
                                                    'census vintage supplied the '
                                                    'weights; the same grid weighted '
                                                    'by 2010 versus 2020 populations '
                                                    'gives different exposures. '
                                                    'Without the source, a weighted '
                                                    'value cannot be reproduced or '
                                                    'compared with other weighted '
                                                    'products.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'Gridded Population of the World v4, used in the '
                                      'ACAG PM2.5 scenario',
                       'value': 'GPW v4 (2020)'}],
         'see_also': ['https://www.census.gov/programs-surveys/geography/guidance/geo-areas.html',
                      'https://www.climatologylab.org/gridmet.html']} })
    population_weighting_source_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Population Weighting Is Missing", description="""Reason `population_weighting_source` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the population-weighting field '
                                                  'above is empty, this field explains '
                                                  'why — usually because the dataset '
                                                  'is a plain average with no '
                                                  'population weighting at all. It '
                                                  'makes the emptiness intentional '
                                                  'rather than an oversight.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A blank weighting source is '
                                                    'ambiguous between "no weighting '
                                                    'was applied" and "the source was '
                                                    'not recorded". Recording the '
                                                    'reason keeps unweighted products '
                                                    'from looking like incompletely '
                                                    'documented weighted ones and lets '
                                                    'automated checks pass '
                                                    'legitimately null records.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': 'no population weighting applied (Daymet Tmax '
                                      'scenario)',
                       'value': 'not_applicable'}]} })
    target_geography_type: TargetGeographyTypeEnum = Field(default=..., title="Target Geography Type", description="""Geographic unit the exposure value is attached to.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This says what kind of place the '
                                                  'value belongs to: one specific home '
                                                  'address, a neighbourhood-sized '
                                                  'census area, a ZIP-code area, a '
                                                  'whole county, and so on. The bigger '
                                                  'the unit, the more the number is a '
                                                  'shared average rather than a '
                                                  'personal measurement.'},
                         'justification': {'tag': 'justification',
                                           'value': 'An exposure pinned to an exact '
                                                    'residence and one averaged over a '
                                                    'whole county are fundamentally '
                                                    'different quantities with '
                                                    'different privacy and '
                                                    'misclassification profiles. '
                                                    'Without the target geography, '
                                                    'users cannot tell how localised '
                                                    'the value is or link it correctly '
                                                    'to health records held at a given '
                                                    'geographic level.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SpatialReference'],
         'examples': [{'description': "patient's exact residence coordinates (Daymet "
                                      'Tmax scenario)',
                       'value': 'point_residence'},
                      {'description': 'tract-level aggregate (ACAG PM2.5 scenario)',
                       'value': 'census_tract'}],
         'see_also': ['https://www.census.gov/programs-surveys/geography/guidance/geo-areas.html']} })


class TemporalReference(ConfiguredBaseModel):
    """
    Temporal provenance of an environmental exposure value: native temporal grain, aggregation rule, day-boundary convention, coverage of the source product, the extraction window the run actually pulled, and calendar. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/temporal',
         'see_also': ['https://cfconventions.org/',
                      'https://en.wikipedia.org/wiki/ISO_8601'],
         'slot_usage': {'day_boundary_convention': {'name': 'day_boundary_convention',
                                                    'required': True},
                        'temporal_aggregation_method': {'name': 'temporal_aggregation_method',
                                                        'required': True},
                        'temporal_resolution': {'name': 'temporal_resolution',
                                                'required': True}},
         'title': 'Temporal Reference'})

    temporal_resolution: TemporalResolutionEnum = Field(default=..., title="Temporal Resolution", description="""Native temporal grain of the values.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'How often does this dataset produce '
                                                  'a number — one per hour, one per '
                                                  'day, one per year? A daily '
                                                  'temperature and a yearly average '
                                                  'temperature are very different '
                                                  'things, so you need to know which '
                                                  'kind of value you are looking at '
                                                  'before comparing anything.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A daily value and an annual value '
                                                    'of the same variable are '
                                                    'different exposures with '
                                                    'different health associations; '
                                                    'without the native grain an '
                                                    'analyst cannot tell whether a '
                                                    'series supports an acute '
                                                    '(day-level) analysis or only a '
                                                    'chronic one, and silent '
                                                    'resampling between products goes '
                                                    'undetected.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Daymet Tmax — one value per day.',
                       'value': 'daily'},
                      {'description': 'ACAG satellite PM2.5 — one value per year.',
                       'value': 'annual'}],
         'see_also': ['https://cfconventions.org/cf-conventions/cf-conventions.html#time-coordinate']} })
    temporal_aggregation_method: TemporalAggregationMethodEnum = Field(default=..., title="Temporal Aggregation Method", description="""How the value summarises sub-period values. Maps 1:1 to CF cell_methods.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Within each time window there are '
                                                  'many raw measurements; this says '
                                                  'which single number was kept — the '
                                                  'highest, the average, the total. '
                                                  'The hottest moment of a day and the '
                                                  'average across the whole day can '
                                                  'differ by many degrees, so it '
                                                  'matters which one the value '
                                                  'represents.'},
                         'justification': {'tag': 'justification',
                                           'value': '"Daily maximum" and "daily mean" '
                                                    'temperature are different '
                                                    'exposures with different health '
                                                    'associations, and this is the '
                                                    'field that separates them. '
                                                    'Omitting it lets two studies '
                                                    'silently compare a maximum '
                                                    'against a mean and reach opposite '
                                                    'conclusions about the same heat '
                                                    'event.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Daily Tmax — `time: maximum` in CF.',
                       'value': 'maximum'},
                      {'description': 'Annual-mean PM2.5 — `time: mean` in CF.',
                       'value': 'mean'}],
         'see_also': ['https://cfconventions.org/cf-conventions/cf-conventions.html#cell-methods']} })
    temporal_aggregation_window_seconds: Optional[int] = Field(default=None, title="Aggregation Window (seconds)", description="""Redundant with `temporal_resolution` but explicit for machine use; e.g. 86400 for daily, 3600 for hourly.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The same "how long is one time '
                                                  'step" answer, but written as a '
                                                  'plain number of seconds — a day is '
                                                  '86,400 seconds. Computers can check '
                                                  'and compare numbers much more '
                                                  'reliably than words like "daily", '
                                                  'so the redundancy is deliberate.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A machine-checkable twin of '
                                                    '`temporal_resolution`: an '
                                                    'explicit numeric window (86400 '
                                                    'for daily) lets validators verify '
                                                    'the declared grain arithmetically '
                                                    'instead of interpreting an enum '
                                                    'label, catching a mislabelled '
                                                    'resolution before it corrupts a '
                                                    'temporal join.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Daily window (Daymet Tmax).', 'value': '86400'},
                      {'description': 'Annual window (satellite PM2.5).',
                       'value': '31536000'}]} })
    day_boundary_convention: DayBoundaryConventionEnum = Field(default=..., title="Day-Boundary Convention", description="""Where the 24-hour day window starts. **Mandatory.** Daymet = `local_midnight`; PRISM = `24h_ending_1200_GMT`; NARR / ERA5 sub-daily = `utc_midnight`. The single most-omitted slot in the literature and a known source of cross-study disagreement.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When does "Tuesday" start and end '
                                                  'for this dataset — midnight local '
                                                  'time, midnight in London, or '
                                                  'noon-to-noon? Different products '
                                                  'genuinely disagree, which changes '
                                                  'which hot afternoon lands on which '
                                                  'day.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The single most-omitted slot in '
                                                    'the environmental-health '
                                                    'literature and a known source of '
                                                    'cross-study disagreement: '
                                                    "Daymet's local-midnight day and "
                                                    "PRISM's 24h-ending-1200-GMT day "
                                                    'slice the same thermometer '
                                                    'readings differently, so the '
                                                    '"daily Tmax" for the same '
                                                    'calendar date can differ between '
                                                    'products and lagged analyses can '
                                                    'shift by a whole day. It is also '
                                                    'the exposure-side half of the '
                                                    'day-boundary cross-check against '
                                                    'the clinical-side '
                                                    '`clinical_date_assignment_convention`.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Daymet convention — day starts at local '
                                      'midnight.',
                       'value': 'local_midnight'},
                      {'description': 'Annual PM2.5 aggregate — no day boundary is '
                                      'meaningful.',
                       'value': 'not_applicable'}],
         'see_also': ['https://daymet.ornl.gov/',
                      'https://prism.oregonstate.edu/',
                      'https://psl.noaa.gov/data/gridded/data.narr.html']} })
    temporal_coverage_start: Optional[date] = Field(default=None, title="Temporal Coverage Start", description="""Start of the source product's full temporal coverage.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The earliest date the source '
                                                  'dataset has any data for at all. If '
                                                  'you ask for a date before this, the '
                                                  'answer is not "missing" — the '
                                                  'dataset simply never covered that '
                                                  'time.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes out-of-coverage '
                                                    'from missing: without the '
                                                    "product's coverage start, a gap "
                                                    'before 1980 in a Daymet-derived '
                                                    'series looks like missing data '
                                                    'rather than a request outside the '
                                                    "product's lifetime, and "
                                                    'imputation or exclusion decisions '
                                                    'go wrong.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Daymet V4 coverage starts in 1980.',
                       'value': '1980-01-01'}]} })
    temporal_coverage_end: Optional[date] = Field(default=None, title="Temporal Coverage End", description="""End of the source product's coverage. May be an \"ongoing\" sentinel for live products.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The latest date the source dataset '
                                                  'covers; some products are still '
                                                  'being extended. Asking for a date '
                                                  'after this returns nothing — not '
                                                  'because data is missing, but '
                                                  'because it does not exist yet.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes out-of-coverage '
                                                    'from missing at the recent end, '
                                                    'and — because live products keep '
                                                    'growing — pins down which vintage '
                                                    'of the product this run saw, so a '
                                                    'later re-run against a longer '
                                                    'series can be recognised as a '
                                                    'different extract.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'End of Daymet V4 coverage at extraction time.',
                       'value': '2024-12-31'}]} })
    extraction_window_start: Optional[date] = Field(default=None, title="Extraction Window Start", description="""Actual start date the run extracted.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Of everything the dataset covers, '
                                                  'this is the first date this '
                                                  'particular job actually downloaded '
                                                  '— like noting which pages of a big '
                                                  'book you photocopied.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Records the dates this run '
                                                    'actually pulled, as opposed to '
                                                    'what the product offers; without '
                                                    'it a reproducer cannot re-request '
                                                    'the same slice, and a lag '
                                                    'analysis cannot verify that the '
                                                    'pre-event days (e.g. the day '
                                                    'before the index date) were '
                                                    'actually in the extract.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Day before the Phoenix index date, for lag '
                                      'analysis.',
                       'value': '2022-07-18'}]} })
    extraction_window_end: Optional[date] = Field(default=None, title="Extraction Window End", description="""Actual end date the run extracted.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Of everything the dataset covers, '
                                                  'this is the last date this '
                                                  'particular job actually downloaded '
                                                  '— the end of the photocopied page '
                                                  'range.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The closing bracket of the slice '
                                                    'this run actually pulled; without '
                                                    'it a reproducer cannot re-request '
                                                    'the same window, and a lag '
                                                    'analysis cannot verify that the '
                                                    'post-event days it needs were '
                                                    'actually extracted rather than '
                                                    'silently truncated.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'Day after the Phoenix index date, for lag '
                                      'analysis.',
                       'value': '2022-07-20'}]} })
    calendar: Optional[CalendarEnum] = Field(default=None, title="Calendar (CF)", description="""CF calendar. `gregorian` is the default; only matters when a source uses a non-standard calendar (some climate model output does).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most data uses the ordinary '
                                                  'calendar, but some climate models '
                                                  'simplify — for example pretending '
                                                  'every year has exactly 365 days (no '
                                                  'leap days) or twelve 30-day months. '
                                                  'If you line those dates up against '
                                                  'a real calendar without converting, '
                                                  'they slowly drift out of sync.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Some climate-model output uses '
                                                    'non-standard calendars (365-day '
                                                    'noleap, 360-day); joining such a '
                                                    'series to real-world Gregorian '
                                                    'clinical dates without converting '
                                                    'shifts daily values progressively '
                                                    'through the year — a silent, '
                                                    'cumulative misalignment.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['TemporalReference'],
         'examples': [{'description': 'The default; used by Daymet and ACAG PM2.5 '
                                      'alike.',
                       'value': 'gregorian'}],
         'see_also': ['https://cfconventions.org/cf-conventions/cf-conventions.html#calendar']} })


class SourceDataset(ConfiguredBaseModel):
    """
    The upstream gridded / station product the exposure values originate from. Carries identity, DOI, version, coverage, producer, citation, license, native format, and homogenisation status. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/source',
         'see_also': ['https://www.doi.org/',
                      'https://spdx.org/licenses/',
                      'https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3'],
         'slot_usage': {'source_dataset_name': {'name': 'source_dataset_name',
                                                'required': True},
                        'source_dataset_version': {'name': 'source_dataset_version',
                                                   'required': True}},
         'title': 'Source Dataset'})

    source_dataset_name: str = Field(default=..., title="Source Dataset Name", description="""Full name of the source product, e.g. \"Daymet V4 Daily Surface Weather Data\", \"GridMET\", \"NARR\", \"ERA5-HEAT\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Weather and air-quality data come '
                                                  'from named products made by '
                                                  'different organisations, much like '
                                                  'maps come from different '
                                                  'map-makers. This is simply the full '
                                                  'official name of the product the '
                                                  'values were taken from.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the product name, "daily '
                                                    'maximum temperature" could come '
                                                    'from any of a dozen products '
                                                    'whose values disagree; the name '
                                                    'is the first anchor for '
                                                    'identifying which upstream data '
                                                    'actually produced the exposure '
                                                    'values.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'Daymet V4 Daily Surface Weather Data'}],
         'see_also': ['https://daymet.ornl.gov/',
                      'https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5']} })
    source_dataset_short_code: Optional[str] = Field(default=None, title="Source Dataset Short Code", description="""Short code keying into the EnVar source registry, e.g. `daymet_v4`, `gridmet`, `narr`, `era5_heat`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A short nickname for the dataset, '
                                                  'like a username, that computers can '
                                                  'match exactly — "Daymet V4 Daily '
                                                  'Surface Weather Data" becomes just '
                                                  '`daymet_v4`.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A stable machine-readable key '
                                                    'lets tools group and compare '
                                                    'records from the same product '
                                                    'without fuzzy-matching free-text '
                                                    'names, which vary in spelling and '
                                                    'capitalisation across studies.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'daymet_v4'}]} })
    source_dataset_doi: Optional[str] = Field(default=None, title="Source Dataset DOI", description="""DOI of the source dataset. Mandatory if a DOI exists. Daymet V4 = `10.3334/ORNLDAAC/2129`; ERA5 = `10.24381/cds.adbb2d47`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A DOI is a permanent ID for a '
                                                  'dataset or paper that keeps working '
                                                  'even when websites move. Looking it '
                                                  'up at doi.org always leads to the '
                                                  'current home of the data.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The DOI is the durable handle for '
                                                    'the source; access URLs rot, but '
                                                    'a DOI keeps resolving to the '
                                                    'dataset, so future readers can '
                                                    'always retrieve exactly what was '
                                                    'used and producers get citable '
                                                    'credit.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'Daymet V4 R1 DOI',
                       'value': '10.3334/ORNLDAAC/2129'}],
         'see_also': ['https://www.doi.org/', 'https://datacite.org/'],
         'slot_uri': 'dcterms:identifier'} })
    source_dataset_doi_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Source Dataset DOI Is Missing", description="""Reason `source_dataset_doi` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the DOI box is empty, this field '
                                                  'says why — for example, the '
                                                  'producer never issued one. That way '
                                                  'an empty field is a deliberate '
                                                  'statement, not an oversight.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "this product '
                                                    'genuinely has no DOI" from '
                                                    '"nobody filled the field in"; a '
                                                    'blank is a bug, while a '
                                                    'null-with-reason is information a '
                                                    'completeness checker can act on.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    source_dataset_version: str = Field(default=..., title="Source Dataset Version", description="""Source product version. E.g. \"V4 R1\" for Daymet; \"V5.GL.03\" vs \"V6.GL.02\" for ACAG PM products. Version differences materially change values.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Datasets get updated and '
                                                  're-released like software, and the '
                                                  'numbers can change between '
                                                  'releases. The version says exactly '
                                                  'which release the values came '
                                                  'from.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Version differences materially '
                                                    'change values (e.g. ACAG V5 vs V6 '
                                                    'PM2.5), so two studies "using '
                                                    'Daymet" may in fact use different '
                                                    'data; a value without a version '
                                                    'is not reproducible.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'Daymet V4 Release 1', 'value': 'V4 R1'},
                      {'description': 'ACAG global PM2.5 product version',
                       'value': 'V5.GL.04'}]} })
    source_dataset_temporal_coverage: Optional[str] = Field(default=None, title="Source Dataset Temporal Coverage", description="""Source product temporal coverage as an ISO 8601 interval string `<start>/<end>`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Simply the first and last dates the '
                                                  'dataset covers. If you ask for a '
                                                  'day outside that window, there was '
                                                  'never any data to find — which is '
                                                  'different from data that should '
                                                  'exist but is missing.'},
                         'justification': {'tag': 'justification',
                                           'value': "Knowing the product's full time "
                                                    'span distinguishes "date outside '
                                                    'the product\'s coverage" from '
                                                    '"value genuinely missing", '
                                                    'preventing coverage gaps from '
                                                    'being misread as data errors.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': '1980-01-01/2024-12-31'}],
         'see_also': ['https://en.wikipedia.org/wiki/ISO_8601']} })
    source_dataset_spatial_extent: Optional[str] = Field(default=None, title="Source Dataset Spatial Extent", description="""Human-readable spatial extent of the product, e.g. \"CONUS, Hawaii, Puerto Rico\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A plain-language note of which '
                                                  'regions the dataset covers, for '
                                                  'example the continental United '
                                                  'States plus Hawaii and Puerto Rico. '
                                                  'Places outside this area simply '
                                                  'have no data.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The product footprint '
                                                    'distinguishes "location outside '
                                                    'the product\'s extent" from '
                                                    '"missing value"; without it, a '
                                                    'subject in Alaska queried against '
                                                    'a CONUS-only product looks like a '
                                                    'data error rather than an '
                                                    'out-of-coverage case.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'CONUS, Hawaii, Puerto Rico'}]} })
    source_producer_institution: Optional[str] = Field(default=None, title="Producer Institution", description="""Producer institution, e.g. \"NASA ORNL DAAC\", \"University of Idaho\", \"NOAA NCEP\", \"ECMWF Copernicus\".""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The organisation that makes and '
                                                  'publishes the dataset — for example '
                                                  'a NASA data centre or a university '
                                                  'group. Knowing who made the data '
                                                  'tells you where to go with '
                                                  'questions.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Identifies who is accountable for '
                                                    'the product, supports correct '
                                                    'attribution, and helps '
                                                    'disambiguate similarly named '
                                                    'products maintained by different '
                                                    'institutions.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'NASA ORNL DAAC'}]} })
    source_citation_apa: Optional[str] = Field(default=None, title="Source Citation (APA)", description="""Full APA-style citation for the source dataset.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The ready-to-paste reference for '
                                                  'the dataset, formatted the way '
                                                  'academic papers list their sources, '
                                                  'so anyone reusing the data knows '
                                                  'exactly how to cite it.'},
                         'justification': {'tag': 'justification',
                                           'value': "The producer's requested citation "
                                                    'is what enables attribution and '
                                                    'retrieval; omitting it makes it '
                                                    'harder for readers to credit the '
                                                    'producers and to locate the exact '
                                                    'product in the literature.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'truncated form; the real citation lists all '
                                      'authors',
                       'value': 'Thornton, M.M., et al. (2022). Daymet: Daily Surface '
                                'Weather Data on a 1-km Grid for North America, '
                                'Version 4 R1. ORNL DAAC.'}]} })
    source_citation_bibtex: Optional[str] = Field(default=None, title="Source Citation (BibTeX)", description="""BibTeX entry for the source dataset, machine-parseable.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'BibTeX is a structured text format '
                                                  'that reference-manager software '
                                                  'understands. It carries the same '
                                                  'citation as the human-readable '
                                                  'text, but in a form computers can '
                                                  'read directly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A machine-parseable citation lets '
                                                    'reference managers and pipelines '
                                                    'ingest the attribution '
                                                    'automatically, avoiding '
                                                    'transcription errors when the '
                                                    'citation is copied by hand.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': '@misc{daymet_v4_r1, title={Daymet: Daily Surface '
                                'Weather Data on a 1-km Grid for North America, '
                                'Version 4 R1}, author={Thornton, M.M. and others}, '
                                'year={2022}, publisher={ORNL DAAC}, '
                                'doi={10.3334/ORNLDAAC/2129}}'}]} })
    source_citation_bibtex_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason BibTeX Citation Is Missing", description="""Reason `source_citation_bibtex` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the machine-readable citation is '
                                                  'empty, this field says why, so the '
                                                  'gap is a deliberate statement '
                                                  'rather than an oversight.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Records whether the BibTeX entry '
                                                    'is absent because the producer '
                                                    'never supplied one or because it '
                                                    'was not extracted, so an empty '
                                                    'field is auditable rather than '
                                                    'ambiguous.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    source_license_spdx: Optional[str] = Field(default=None, title="Source License (SPDX)", description="""SPDX identifier of the source license, e.g. `CC0-1.0`, `CC-BY-4.0`. Use `public-domain-us-gov` for US federal data with no formal SPDX equivalent.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'SPDX codes are standard short names '
                                                  'for licenses, like CC-BY-4.0, so '
                                                  'software can check reuse rules '
                                                  'automatically. The license says '
                                                  'what you are allowed to do with the '
                                                  'data.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the license, downstream '
                                                    'deposit and redistribution '
                                                    'legality is unknowable — you '
                                                    'cannot tell whether derived '
                                                    'exposure values may be shared, '
                                                    'deposited in a repository, or '
                                                    'must stay private.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'US federal data (e.g. Daymet V4)',
                       'value': 'public-domain-us-gov'},
                      {'description': 'e.g. ACAG PM2.5 V5.GL', 'value': 'CC-BY-4.0'}],
         'see_also': ['https://spdx.org/licenses/']} })
    source_access_url: Optional[str] = Field(default=None, title="Source Access URL", description="""Landing-page URL for the dataset (not a download link, which rots).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': "The dataset's home page on the web "
                                                  '— the front door where you can read '
                                                  'about the data and find the '
                                                  'download options — rather than a '
                                                  'direct file link that stops working '
                                                  'when files move.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A stable landing page is how '
                                                    'future users actually reach the '
                                                    'data; a raw download link rots '
                                                    'when files are reorganised, '
                                                    'leaving the record pointing '
                                                    'nowhere.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'https://daymet.ornl.gov/'}]} })
    source_native_format: Optional[SourceNativeFormatEnum] = Field(default=None, title="Source Native Format", description="""Format the source ships in.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Scientific data comes packaged in '
                                                  'different file types (NetCDF, '
                                                  'GeoTIFF, CSV, and others), a bit '
                                                  'like documents come as PDF or Word. '
                                                  'This records which package the '
                                                  'producer ships.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The shipping format determines '
                                                    'which tools can read the source '
                                                    'and what metadata survives; '
                                                    'knowing it lets others rebuild '
                                                    'the same extraction pipeline and '
                                                    'anticipate format-specific '
                                                    'quirks.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'value': 'netcdf4_cf'}]} })
    source_homogenisation_status: Optional[HomogenisationStatusEnum] = Field(default=None, title="Homogenisation Status", description="""For station-based products, whether values have been homogenised. Mandatory for station-based products; GHCN-D = `not_homogenised`, GHCN-M v4 = `homogenised`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Weather stations get moved, '
                                                  'replaced, or re-instrumented over '
                                                  'the decades, which creates '
                                                  'artificial jumps in their records. '
                                                  '"Homogenised" data has had those '
                                                  'jumps statistically corrected; "not '
                                                  'homogenised" data is raw, as '
                                                  'observed.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Using a non-homogenised station '
                                                    'product (e.g. GHCN-Daily) for '
                                                    'trend work without saying so is a '
                                                    'known trap: station moves and '
                                                    'instrument changes masquerade as '
                                                    'climate signal. Mandatory for '
                                                    'station-based products.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'e.g. GHCN-Daily station observations',
                       'value': 'not_homogenised'}],
         'see_also': ['https://en.wikipedia.org/wiki/Homogenization_(climate)']} })
    source_homogenisation_status_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Homogenisation Status Is Missing", description="""Reason `source_homogenisation_status` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the homogenisation field is '
                                                  'empty, this field says why — most '
                                                  'often because the data is a gridded '
                                                  'product rather than raw station '
                                                  'records, so the question does not '
                                                  'apply.'},
                         'justification': {'tag': 'justification',
                                           'value': 'For gridded products '
                                                    'homogenisation status is '
                                                    'genuinely not applicable; '
                                                    'recording that reason keeps the '
                                                    'conditionally-core check '
                                                    'auditable instead of leaving an '
                                                    'ambiguous blank.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'e.g. gridded (non-station) products',
                       'value': 'not_applicable'}]} })
    source_acdd_attributes: Optional[Any] = Field(default=None, title="ACDD Global Attributes", description="""Passthrough of ACDD (Attribute Convention for Data Discovery) global attributes from the source NetCDF header, as a native key/value object.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Many scientific data files carry a '
                                                  'built-in "title page" of '
                                                  'descriptive labels inside the file '
                                                  'itself (following the ACDD '
                                                  'convention). This field simply '
                                                  'copies those labels across so '
                                                  'nothing the producer wrote is '
                                                  'lost.'},
                         'justification': {'tag': 'justification',
                                           'value': "Carrying the source's own ACDD "
                                                    'header attributes forward '
                                                    'preserves producer-supplied '
                                                    'metadata verbatim, allowing later '
                                                    'cross-checks against what this '
                                                    'record claims without '
                                                    're-downloading the source.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'object': {'Conventions': 'CF-1.6, ACDD-1.3',
                                  'institution': 'ORNL DAAC',
                                  'title': 'Daymet Daily Surface Weather Data'}}],
         'see_also': ['https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3']} })
    source_acdd_attributes_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason ACDD Attributes Are Missing", description="""Reason `source_acdd_attributes` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the copied-over file labels are '
                                                  'absent, this field says why — often '
                                                  'because the source is not '
                                                  'distributed as a NetCDF file that '
                                                  'carries such labels.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes sources that ship '
                                                    'no ACDD headers (e.g. CSV station '
                                                    'data) from headers that simply '
                                                    'were not extracted, keeping the '
                                                    'empty field auditable.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['SourceDataset'],
         'examples': [{'description': 'e.g. source not distributed as NetCDF with ACDD '
                                      'headers',
                       'value': 'not_provided_by_source'}]} })


class ExposureModel(ConfiguredBaseModel):
    """
    The model class that produced the values (interpolation, reanalysis, ML, statistical blend, equation), its inputs, its methods-paper DOI, its cross-validation skill, known biases, and any bias correction. One per record; may be null for direct observation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/model',
         'see_also': ['https://en.wikipedia.org/wiki/Reanalysis_(meteorology)'],
         'slot_usage': {'exposure_model_type': {'name': 'exposure_model_type',
                                                'required': True}},
         'title': 'Exposure Model'})

    exposure_model_type: ExposureModelTypeEnum = Field(default=..., title="Exposure Model Type", description="""The class of model that produced the values. Daymet = `spatial_interpolation`; NARR / ERA5 = `reanalysis`; GridMET = `statistical_blend`; Brokamp PM = `single_machine_learning`; Di et al. PM = `ensemble_machine_learning`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most "exposure" numbers were never '
                                                  'measured at your door: a model '
                                                  'estimates them from weather '
                                                  'stations, satellites, or physics '
                                                  'equations. This field says which '
                                                  'kind of machinery produced the '
                                                  'number, so you know how much to '
                                                  'trust it and what could go wrong.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A measured value, an interpolated '
                                                    'value, and an ML-predicted value '
                                                    'have different error structures '
                                                    'and cannot be pooled naively; '
                                                    'this is the field that tells them '
                                                    'apart. Without it, users cannot '
                                                    'judge whether values are '
                                                    'measurements or predictions.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'Daymet V4 daily Tmax (station observations '
                                      'interpolated to a 1 km grid)',
                       'value': 'spatial_interpolation'},
                      {'description': 'ACAG V5.GL satellite-derived annual PM2.5',
                       'value': 'satellite_retrieval'}],
         'see_also': ['https://daymet.ornl.gov/',
                      'https://www.climatologylab.org/gridmet.html',
                      'https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5']} })
    exposure_model_inputs: Optional[list[str]] = Field(default=None, title="Exposure Model Inputs", description="""Inputs to the model. For GridMET: `[\"PRISM monthly normals\", \"NLDAS-2 sub-daily reanalysis\"]`. For derived heat metrics, the input variable list (held in `DerivedHeatMetric.equation_inputs` for typed cases).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A model is only as good as what you '
                                                  'feed it. This lists the raw '
                                                  'ingredients — station readings, '
                                                  'satellite images, other datasets — '
                                                  'that went into cooking up the final '
                                                  'numbers.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Needed to trace what the value '
                                                    'actually derives from. Without '
                                                    'the input list, a shared bias or '
                                                    'gap in an upstream dataset cannot '
                                                    'be traced through to the exposure '
                                                    'values it contaminated.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'sole element of the Daymet V4 input list',
                       'value': 'GHCN-Daily station observations'}],
         'see_also': ['https://prism.oregonstate.edu/']} })
    exposure_model_paper_doi: Optional[str] = Field(default=None, title="Methods Paper DOI", description="""DOI of the methods paper describing the model (Thornton et al. 2022 for Daymet; Abatzoglou 2013 for GridMET).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Scientists publish a paper '
                                                  'describing exactly how a model '
                                                  'works, and a DOI is a permanent web '
                                                  'address for that paper. Recording '
                                                  'it here means anyone can look up '
                                                  'the full recipe behind the numbers, '
                                                  'even years later.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The reproducibility anchor for '
                                                    'how the value was made. Without '
                                                    'it, anyone auditing or '
                                                    'reproducing the analysis must '
                                                    'guess which of several versions '
                                                    'of a method the values actually '
                                                    'came from.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'van Donkelaar et al. 2021 methods paper for '
                                      'ACAG PM2.5',
                       'value': '10.1021/acs.est.1c05309'}],
         'see_also': ['https://www.doi.org/']} })
    exposure_model_paper_doi_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Methods Paper DOI Is Missing", description="""Reason `exposure_model_paper_doi` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When a field is empty, it helps to '
                                                  'say why. This slot records whether '
                                                  'the paper genuinely does not exist, '
                                                  'was not shared by the producer, or '
                                                  'simply was not looked up.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "no methods paper '
                                                    'exists" from "nobody bothered to '
                                                    'record it". Without the reason, a '
                                                    'blank DOI silently hides whether '
                                                    'the model is undocumented or the '
                                                    'metadata is just incomplete.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    exposure_model_cross_validation_r2: Optional[float] = Field(default=None, title="Cross-Validation R²", description="""Model cross-validation R², where reported by the producer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Cross-validation R² is a 0-to-1 '
                                                  'score of how well the model '
                                                  'predicted values it had never seen '
                                                  'during training — closer to 1 is '
                                                  'better. A score of 0.90 means the '
                                                  'model captures most of the real '
                                                  'variation; a low score means treat '
                                                  'the numbers with caution.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The single most useful one-number '
                                                    'quality signal for a modeled '
                                                    'product. Omitting it leaves '
                                                    'downstream users with no '
                                                    'quantitative basis for weighing '
                                                    'one exposure product against '
                                                    'another or for propagating model '
                                                    'skill into their error budgets.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'reported for ACAG V5.GL satellite-derived PM2.5',
                       'value': '0.90'}],
         'see_also': ['https://en.wikipedia.org/wiki/Coefficient_of_determination']} })
    exposure_model_cross_validation_r2_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Cross-Validation R² Is Missing", description="""Reason `exposure_model_cross_validation_r2` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the quality score is blank, this '
                                                  'slot says why — for example, some '
                                                  'well-known products simply never '
                                                  'publish one. It turns an empty '
                                                  'field into an honest answer.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Separates "the producer never '
                                                    'published a skill score" from "we '
                                                    'forgot to record it". Without '
                                                    'this, a missing R² is ambiguous '
                                                    'and reviewers cannot tell an '
                                                    'undocumented model from sloppy '
                                                    'metadata.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'Daymet does not publish a cross-validation R²',
                       'value': 'not_provided_by_source'}]} })
    exposure_model_known_biases: Optional[list[str]] = Field(default=None, title="Known Model Biases", description="""Free-text flags of known issues, e.g. \"NLDAS-2 coastal Tmax bias up to -1.48 °C\", \"NARR cold bias at extremes\", \"Daymet warm bias in summer in some western US regions\". The field reviewers care about.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Every model has known blind spots — '
                                                  'places or conditions where it is '
                                                  'reliably a bit wrong, like running '
                                                  'warm in summer or cold at the '
                                                  'coast. This slot writes those '
                                                  'warnings down so the next person '
                                                  'does not rediscover them the hard '
                                                  'way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The field reviewers care about '
                                                    'most; it bites coastal and '
                                                    'sparse-station analyses in '
                                                    'particular. Omitting it lets a '
                                                    'documented systematic error (e.g. '
                                                    'a coastal cold bias) silently '
                                                    'propagate into health-effect '
                                                    'estimates that reviewers will '
                                                    'later reject.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'one known bias of Daymet V4 daily Tmax',
                       'value': 'warm-season warm bias documented in some western US '
                                'regions'},
                      {'description': 'another element of the same Daymet V4 bias list',
                       'value': 'interpolation degrades in sparse-station areas'}],
         'see_also': ['https://psl.noaa.gov/data/gridded/data.narr.html',
                      'https://daymet.ornl.gov/']} })
    exposure_model_ensemble_member_count: Optional[int] = Field(default=None, title="Ensemble Member Count", description="""For ensemble products, the number of members. Null with reason `not_provided_by_source` for single-realisation products.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some products run the same model '
                                                  'many times with slightly different '
                                                  'settings and combine the results — '
                                                  'each run is a "member". Knowing how '
                                                  'many members there were (say, 100) '
                                                  'tells you how much the spread '
                                                  'between runs can be trusted as a '
                                                  'measure of uncertainty.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Mandatory for ensemble products: '
                                                    'the member count determines how '
                                                    'the ensemble spread can be '
                                                    'interpreted as an uncertainty '
                                                    'estimate. Without it, per-value '
                                                    'spread statistics cannot be '
                                                    'reproduced or sanity-checked.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'e.g. an ensemble ML product with 100 members; '
                                      'single-realisation products such as Daymet '
                                      'leave this null',
                       'value': '100'}],
         'see_also': ['https://en.wikipedia.org/wiki/Ensemble_forecasting']} })
    exposure_model_ensemble_member_count_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Ensemble Member Count Is Missing", description="""Reason `exposure_model_ensemble_member_count` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Many products come from just one '
                                                  'model run, so "number of members" '
                                                  'genuinely does not apply. This slot '
                                                  'says so explicitly, instead of '
                                                  'leaving readers to wonder whether '
                                                  'information was lost.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Confirms explicitly that a '
                                                    'product is single-realisation '
                                                    'rather than an ensemble whose '
                                                    'member count was dropped. Without '
                                                    'it, a null count is ambiguous and '
                                                    'the conditionally-core rule for '
                                                    'ensemble products cannot be '
                                                    'audited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'single-realisation products (Daymet, ACAG) have '
                                      'no ensemble',
                       'value': 'not_applicable'}]} })
    bias_correction_applied: Optional[BiasCorrectionAppliedEnum] = Field(default=None, title="Bias Correction Applied", description="""Whether and how bias correction has been applied. Usually `none` for Tmax from reference products.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Sometimes model output is nudged '
                                                  'after the fact to better match real '
                                                  'observations — that nudging is '
                                                  '"bias correction". This slot '
                                                  'records whether the numbers were '
                                                  'adjusted that way and, if so, which '
                                                  'technique was used.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Pooling bias-corrected and raw '
                                                    'values silently mixes apples and '
                                                    'oranges. Without this flag, an '
                                                    'analyst cannot tell whether two '
                                                    'datasets differ because of the '
                                                    'environment or because one of '
                                                    'them was statistically adjusted.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'description': 'Daymet V4 daily Tmax is used uncorrected',
                       'value': 'none'}]} })
    bias_correction_applied_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Bias Correction Is Missing", description="""Reason `bias_correction_applied` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If nobody could say whether the '
                                                  'numbers were statistically '
                                                  'adjusted, this slot records why '
                                                  'that answer is missing — for '
                                                  'example, the data producer never '
                                                  'documented it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "the producer never '
                                                    'documented any correction" from '
                                                    'an unrecorded answer. Without it, '
                                                    'a blank bias-correction field '
                                                    'cannot be told apart from missing '
                                                    'metadata, weakening any audit of '
                                                    'how values were adjusted.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ExposureModel'],
         'examples': [{'value': 'not_provided_by_source'}]} })


class Uncertainty(ConfiguredBaseModel):
    """
    Uncertainty and quality character of a value series: per-value uncertainty type / units, model-aggregate uncertainty summary, quality flag vocabulary, missing-data handling, and data completeness. The uncertainty / QA-flag column bindings live in DataLayout (see envar_layout). One per record; slots may be null with reasons.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/uncertainty',
         'see_also': ['https://en.wikipedia.org/wiki/Uncertainty_quantification'],
         'title': 'Uncertainty and Quality'})

    per_value_uncertainty_type: Optional[UncertaintyTypeEnum] = Field(default=None, title="Per-Value Uncertainty Type", description="""Kind of per-value uncertainty captured in the column named by `DataLayout.value_uncertainty_column` (see envar_layout).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Every estimated value comes with a '
                                                  '"how sure are we" number, but there '
                                                  'are several different kinds. This '
                                                  'says which kind you are looking at '
                                                  '— for example a standard error (a ± '
                                                  'number saying how far off the '
                                                  'estimate could plausibly be) versus '
                                                  'a prediction interval (a range the '
                                                  'true value should fall inside, say '
                                                  '95 times out of 100).'},
                         'justification': {'tag': 'justification',
                                           'value': 'A "±" number means nothing until '
                                                    'you know what kind of number it '
                                                    'is: a standard error, a 95 % '
                                                    'prediction interval, and an '
                                                    'ensemble spread are not '
                                                    'interchangeable and cannot be '
                                                    'pooled or propagated the same '
                                                    'way. Without the type, downstream '
                                                    'code either mishandles the '
                                                    'uncertainty or drops it, so '
                                                    'exposure measurement error goes '
                                                    'unaccounted for and health-effect '
                                                    'estimates are biased, usually '
                                                    'toward the null.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Daymet daily Tmax reports a per-value standard '
                                      'error.',
                       'value': 'standard_error'},
                      {'description': 'ACAG satellite PM2.5 reports a per-value '
                                      'prediction interval.',
                       'value': 'prediction_interval'}],
         'see_also': ['https://en.wikipedia.org/wiki/Standard_error',
                      'https://en.wikipedia.org/wiki/Prediction_interval']} })
    per_value_uncertainty_type_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Uncertainty Type Is Missing", description="""Reason `per_value_uncertainty_type` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the uncertainty-type field is '
                                                  'left empty, this simply says why — '
                                                  'for instance the original dataset '
                                                  'never published one. It turns a '
                                                  'confusing blank into an explicit, '
                                                  'honest "not available, and here is '
                                                  'the reason".'},
                         'justification': {'tag': 'justification',
                                           'value': 'Records the difference between '
                                                    '"we know the source has no '
                                                    'per-value uncertainty" and '
                                                    '"someone forgot to fill this in". '
                                                    'Without the reason, a blank '
                                                    'uncertainty type is ambiguous and '
                                                    'a validator cannot tell an honest '
                                                    'gap from an oversight, so '
                                                    'quality-completeness reporting is '
                                                    'unreliable.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'The source product publishes no per-value '
                                      'uncertainty.',
                       'value': 'not_provided_by_source'}]} })
    per_value_uncertainty_units_ucum: Optional[str] = Field(default=None, title="Uncertainty Units (UCUM)", description="""Units of the per-value uncertainty in UCUM syntax. Usually the same as the value units.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This says what the uncertainty is '
                                                  'measured in — degrees Celsius, '
                                                  'micrograms per cubic metre, and so '
                                                  'on — written in a standard code '
                                                  '(UCUM) that computers read the same '
                                                  'way every time. Usually it matches '
                                                  'the units of the value itself.'},
                         'justification': {'tag': 'justification',
                                           'value': 'An uncertainty number is '
                                                    'meaningless without its units: a '
                                                    'per-value error of "2" is 2 °C or '
                                                    '2 K depending on this field, and '
                                                    'a mismatch between value units '
                                                    'and uncertainty units silently '
                                                    'corrupts any error propagation '
                                                    'into the health analysis.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Standard error of a daily Tmax value, in '
                                      'degrees Celsius.',
                       'value': 'Cel'}],
         'see_also': ['https://ucum.org/']} })
    per_value_uncertainty_units_ucum_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Uncertainty Units Are Missing", description="""Reason `per_value_uncertainty_units_ucum` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the uncertainty-units field is '
                                                  'blank, this explains why — often '
                                                  'because there is no uncertainty '
                                                  'column at all, so there is nothing '
                                                  'to put units on. It stops a reader '
                                                  'from wondering whether the units '
                                                  'were simply forgotten.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "there is no '
                                                    'uncertainty column, so units '
                                                    'genuinely do not apply" from an '
                                                    'accidental omission. Without the '
                                                    'reason a blank units field is '
                                                    'ambiguous and completeness checks '
                                                    'cannot tell a legitimate '
                                                    'not-applicable from a missing '
                                                    'entry.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'No per-value uncertainty column exists, so '
                                      'units do not apply.',
                       'value': 'not_applicable'}]} })
    model_aggregate_uncertainty: Optional[ModelAggregateUncertainty] = Field(default=None, title="Model Aggregate Uncertainty", description="""Summary statistics for the model as a whole — cross-validation metrics and where they are reported.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A report card for how well the '
                                                  'model predicts reality overall, '
                                                  'checked by holding some data back '
                                                  'and seeing how close its guesses '
                                                  'came — for example an R² near 1 '
                                                  'means the model tracks the true '
                                                  'values closely. It also records '
                                                  'where those scores were published.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Per-value uncertainty is often '
                                                    'absent, so the whole-model '
                                                    'cross-validation summary (R², '
                                                    'RMSE) is frequently the only '
                                                    'quantitative handle on how '
                                                    'accurate the product is. Without '
                                                    'it an analyst cannot judge '
                                                    'whether the exposure estimates '
                                                    'are precise enough for the health '
                                                    'question, and cannot compare the '
                                                    'reliability of two products.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Cross-validated R² for ACAG satellite PM2.5 and '
                                      'its reporting DOI.',
                       'object': {'cv_r2': 0.9,
                                  'reported_in': '10.1021/acs.est.1c05309'}}],
         'see_also': ['https://en.wikipedia.org/wiki/Cross-validation_(statistics)']} })
    model_aggregate_uncertainty_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Aggregate Uncertainty Is Missing", description="""Reason `model_aggregate_uncertainty` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the model-accuracy summary is '
                                                  'missing, this says why — usually '
                                                  'because the people who made the '
                                                  'dataset never reported those '
                                                  'scores. It makes the absence '
                                                  'deliberate and explainable rather '
                                                  'than a mystery blank.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Separates "the producer published '
                                                    'no cross-validation metrics" from '
                                                    'a forgotten entry. Without the '
                                                    'reason, a missing model-accuracy '
                                                    'summary looks like a data-entry '
                                                    'lapse, and reviewers cannot tell '
                                                    'whether the information was ever '
                                                    'available.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'The producer reports no whole-model '
                                      'cross-validation metrics.',
                       'value': 'not_provided_by_source'}]} })
    quality_flag_vocabulary: Optional[str] = Field(default=None, title="Quality Flag Vocabulary", description="""Reference to the QA flag vocabulary (e.g. an EPA AQS qualifier-code list) used by the column named in `DataLayout.quality_flag_column` (see envar_layout).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some datasets tag individual values '
                                                  'with short quality codes — think of '
                                                  'the little footnote letters next to '
                                                  'numbers in a table. This points to '
                                                  'the key that explains what each '
                                                  'code means, so you know which '
                                                  'readings to trust or set aside.'},
                         'justification': {'tag': 'justification',
                                           'value': 'QA flags (e.g. "estimated", '
                                                    '"below detection limit", '
                                                    '"instrument malfunction") are '
                                                    'only interpretable against the '
                                                    'code list that defines them; '
                                                    'without naming the vocabulary, a '
                                                    'flagged value cannot be correctly '
                                                    'filtered or trusted, so suspect '
                                                    'measurements may enter the '
                                                    'analysis unnoticed.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Flag vocabulary for monitor-derived series; '
                                      'gridded products often have none.',
                       'value': 'EPA AQS qualifier codes'}]} })
    quality_flag_vocabulary_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Quality Flag Vocabulary Is Missing", description="""Reason `quality_flag_vocabulary` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If there is no quality-code key '
                                                  'listed, this says why — often '
                                                  'because the dataset simply does not '
                                                  'use quality codes. It turns a blank '
                                                  'into a clear statement rather than '
                                                  'leaving the reader guessing.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "this product has '
                                                    'no QA flags at all" (common for '
                                                    'gridded data) from an omission. '
                                                    'Without the reason, an empty '
                                                    'vocabulary field is ambiguous and '
                                                    'a completeness check cannot tell '
                                                    'an inapplicable entry from a '
                                                    'missing one.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Daymet publishes no QA-flag column, so no '
                                      'vocabulary exists.',
                       'value': 'not_provided_by_source'}]} })
    missing_data_handling_method: Optional[MissingDataHandlingEnum] = Field(default=None, title="Missing Data Handling Method", description="""How the source handles missing values (e.g. how Daymet handles snow-covered pixels).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Real data has holes — a cloud '
                                                  'blocks a satellite, snow covers a '
                                                  'sensor. This says what the dataset '
                                                  'did about those holes: leave them '
                                                  'empty, guess from nearby days and '
                                                  'places, copy the last known value, '
                                                  'and so on. Filled-in numbers can '
                                                  'look just like real measurements, '
                                                  'so it matters to know which is '
                                                  'which.'},
                         'justification': {'tag': 'justification',
                                           'value': 'How gaps were filled is often '
                                                    'invisible downstream: an '
                                                    'interpolated value looks '
                                                    'identical to a measured one, so '
                                                    'without this field an analyst '
                                                    'overstates coverage and treats '
                                                    'imputed exposures as if they were '
                                                    'observed, biasing associations in '
                                                    'unknown directions. It is the '
                                                    'difference between apparent and '
                                                    'real completeness.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Daymet fills missing cells by spatiotemporal '
                                      'interpolation.',
                       'value': 'spatiotemporal_interpolation'}],
         'see_also': ['https://daymet.ornl.gov/']} })
    missing_data_handling_method_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Handling Method Is Missing", description="""Reason `missing_data_handling_method` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the gap-handling method is '
                                                  'left empty, this explains why — '
                                                  'often because the original dataset '
                                                  'never said how it dealt with '
                                                  'missing values. It makes the '
                                                  'unknown explicit instead of a '
                                                  'silent blank.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Separates "the producer never '
                                                    'documented how gaps were handled" '
                                                    'from an entry someone forgot. '
                                                    'Without the reason, a blank '
                                                    'handling method is ambiguous and '
                                                    'an analyst cannot judge whether '
                                                    'the gap-filling behaviour is '
                                                    'unknown or simply unrecorded '
                                                    'here.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'The producer does not document its missing-data '
                                      'handling.',
                       'value': 'not_provided_by_source'}]} })
    data_completeness_pct: Optional[float] = Field(default=None, title="Data Completeness Percentage", description="""Percent of (location, date) cells in the extracted window that have a non-missing value. 0-100.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Out of all the days and places you '
                                                  'asked about, this is the percentage '
                                                  'that actually have a value — 100 '
                                                  'means nothing is missing, 60 means '
                                                  'four in ten slots are blank. It is '
                                                  'a quick honesty check on how full '
                                                  'the dataset really is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A quantitative handle on how much '
                                                    'of the requested exposure window '
                                                    'is actually populated. A series '
                                                    'that is 60 % complete supports '
                                                    'very different inferences from '
                                                    'one that is 100 % complete; '
                                                    'without this number, sparse '
                                                    'coverage is hidden and averages '
                                                    'or exposure windows are computed '
                                                    'over gaps as if they were full, '
                                                    'biasing the health analysis.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Every (location, date) cell in the extracted '
                                      'window has a value.',
                       'value': '100'}]} })
    data_completeness_pct_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Data Completeness Is Missing", description="""Reason `data_completeness_pct` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the completeness percentage is '
                                                  'missing, this says why — for '
                                                  'example the number could be worked '
                                                  'out from the data but the software '
                                                  'has not been set up to calculate it '
                                                  'yet. It flags the blank as a known '
                                                  'to-do rather than an '
                                                  'impossibility.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "completeness is '
                                                    'genuinely uncomputable" from "it '
                                                    'could be derived but the pipeline '
                                                    'does not yet do so" — a '
                                                    'distinction that tells a data '
                                                    'steward whether the gap is a '
                                                    'limitation of the source or a '
                                                    'fixable pipeline shortfall.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['Uncertainty'],
         'examples': [{'description': 'Completeness could be computed from the output '
                                      'but the pipeline does not yet do so.',
                       'value': 'available_but_not_extracted'}]} })


class ModelAggregateUncertainty(ConfiguredBaseModel):
    """
    Whole-model uncertainty summary — cross-validation metrics and the reference where they are reported. Inlined on `model_aggregate_uncertainty`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/uncertainty',
         'see_also': ['https://en.wikipedia.org/wiki/Root_mean_square_deviation',
                      'https://en.wikipedia.org/wiki/Coefficient_of_determination'],
         'title': 'Model Aggregate Uncertainty'})

    cv_r2: Optional[float] = Field(default=None, title="Cross-Validated R²", description="""Cross-validated R² for the model as a whole.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelAggregateUncertainty']} })
    cv_rmse: Optional[float] = Field(default=None, title="Cross-Validated RMSE", description="""Cross-validated RMSE for the model as a whole.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelAggregateUncertainty']} })
    reported_in: Optional[str] = Field(default=None, title="Reporting Reference", description="""DOI / citation where the aggregate uncertainty is reported.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ModelAggregateUncertainty']} })


class LinkageMethod(ConfiguredBaseModel):
    """
    How a gridded environmental value gets attached to a patient: the resolution of the patient's spatiotemporal trajectory down to the resolution the exposure data supports. Covers the linkage strategy and buffer parameters, the propagated geocoder precision and score, how patient location-over-time is modelled (the spatial axis), and the clinical-date-assignment convention, partial-day attribution, and lag alignment (the temporal axis). One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/linkage',
         'see_also': ['https://degauss.org/'],
         'slot_usage': {'linkage_strategy': {'name': 'linkage_strategy',
                                             'required': True}},
         'title': 'Linkage Method'})

    linkage_strategy: LinkageStrategyEnum = Field(default=..., title="Linkage Strategy", description="""How a gridded value is attached to a patient location.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Environmental data comes as a map '
                                                  'of values, but health data belongs '
                                                  'to people. This slot records the '
                                                  "rule used to pick a person's value "
                                                  'off that map — for example reading '
                                                  'the value exactly at their home, or '
                                                  'averaging the values in a circle '
                                                  'around it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The strategy determines which '
                                                    'grid cells or stations contribute '
                                                    "to a patient's value: point "
                                                    'extraction, buffer aggregation, '
                                                    'and population weighting can '
                                                    'assign materially different '
                                                    'exposures to the same address. '
                                                    'Without it the person-level value '
                                                    'cannot be reproduced or compared '
                                                    'across studies — this is the '
                                                    '"linkage descriptor" gap named by '
                                                    'the GECC/EIRENE forum.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'extract the grid-cell value at the geocoded '
                                      'residence (Daymet tmax scenario)',
                       'value': 'point_extraction_at_residence'},
                      {'description': 'population-weighted aggregation over the '
                                      'residence tract (ACAG PM2.5 scenario)',
                       'value': 'population_weighted_area_to_residence'}]} })
    linkage_buffer_radius_m: Optional[float] = Field(default=None, title="Buffer Radius (Metres)", description="""Buffer radius in metres for buffer-aggregation strategies.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When exposure is averaged over a '
                                                  "circle drawn around a person's "
                                                  'home, this is how wide that circle '
                                                  'is, in metres.'},
                         'justification': {'tag': 'justification',
                                           'value': 'For buffer strategies the radius '
                                                    'defines the exposure footprint: a '
                                                    '500 m and a 5 km buffer around '
                                                    'the same residence can average '
                                                    'over very different air or heat '
                                                    'conditions, so the assigned value '
                                                    'is not reproducible without it.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': '500 m buffer around the geocoded residence',
                       'value': '500'}]} })
    linkage_buffer_radius_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Buffer Radius Is Missing", description="""Reason `linkage_buffer_radius_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the circle-width field is '
                                                  'empty, this says why — for example '
                                                  'because no circle was used at all.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "no buffer applies '
                                                    'because the strategy is point '
                                                    'extraction" from "the radius was '
                                                    'simply not recorded" — without it '
                                                    'a null radius is ambiguous and '
                                                    'the linkage cannot be audited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'strategy is point extraction, so no buffer '
                                      'radius applies',
                       'value': 'not_applicable'}]} })
    linkage_buffer_aggregation_method: Optional[BufferAggregationEnum] = Field(default=None, title="Buffer Aggregation Method", description="""Aggregation method applied within the buffer (mean / max / median / area-weighted mean).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If several map values fall inside '
                                                  'the circle around a home, they must '
                                                  'be boiled down to one number. This '
                                                  'records how — for example by taking '
                                                  'the average, or the highest value.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Within the same buffer, mean, '
                                                    'max, and area-weighted mean yield '
                                                    'different exposure values; '
                                                    'omitting the method makes the '
                                                    'assigned value irreproducible and '
                                                    'cross-study comparisons unsafe.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'area-weighted mean over the aggregation area '
                                      '(ACAG PM2.5 scenario)',
                       'value': 'area_weighted_mean'}]} })
    linkage_buffer_aggregation_method_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Buffer Aggregation Is Missing", description="""Reason `linkage_buffer_aggregation_method` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the how-values-were-combined '
                                                  'field is empty, this says why.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Separates "not applicable — no '
                                                    'buffer aggregation was performed" '
                                                    'from an undocumented gap; without '
                                                    'the reason a null method leaves '
                                                    'the linkage unauditable.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'strategy is point extraction, so no buffer '
                                      'aggregation applies',
                       'value': 'not_applicable'}]} })
    linkage_max_distance_to_station_m: Optional[float] = Field(default=None, title="Maximum Distance to Station (Metres)", description="""Maximum distance to a station for nearest-station strategies; values beyond this distance get null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some methods take the reading from '
                                                  'the closest measuring station. This '
                                                  'is the farthest a station may be '
                                                  'from the home before the match is '
                                                  'considered too unreliable and no '
                                                  'value is assigned.'},
                         'justification': {'tag': 'justification',
                                           'value': 'For nearest-station strategies '
                                                    'this cutoff decides whether a '
                                                    'distant monitor still counts as '
                                                    '"nearby"; beyond it the '
                                                    'assignment is meaningless and '
                                                    'should be null. Without the '
                                                    'cutoff, values assigned from '
                                                    'stations tens of kilometres away '
                                                    'are indistinguishable from tight '
                                                    'matches, silently degrading '
                                                    'exposure quality.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'stations farther than 50 km from the residence '
                                      'yield null',
                       'value': '50000'}]} })
    linkage_max_distance_to_station_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Station Distance Is Missing", description="""Reason `linkage_max_distance_to_station_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the maximum-station-distance '
                                                  'field is empty, this says why.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "not applicable — '
                                                    'the data is gridded, not '
                                                    'station-based" from an '
                                                    'undocumented cutoff; a bare null '
                                                    'hides whether unlimited-distance '
                                                    'station matches were allowed.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'strategy is gridded extraction, not '
                                      'nearest-station',
                       'value': 'not_applicable'}]} })
    geocoding_precision_propagated: Optional[GeocodingPrecisionEnum] = Field(default=None, title="Propagated Geocoding Precision", description="""Quality category propagated from the upstream geocoder (DeGAUSS `precision` column).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Geocoding means turning a street '
                                                  'address into map coordinates, and '
                                                  'it does not always land on the '
                                                  'exact house — sometimes only on the '
                                                  'street, the ZIP area, or the city. '
                                                  'This records how exact the landing '
                                                  'was.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Geocoding precision determines '
                                                    'whether "residence" means the '
                                                    'actual house or a ZIP-code '
                                                    'centroid kilometres away — which '
                                                    'changes which grid cell the '
                                                    'patient falls in and therefore '
                                                    'their assigned exposure. '
                                                    'Propagating it lets analysts '
                                                    'filter or down-weight coarsely '
                                                    'located records.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'street-centerline point interpolated within an '
                                      'address-range segment',
                       'value': 'range'}],
         'see_also': ['https://degauss.org/']} })
    geocoding_score_propagated: Optional[float] = Field(default=None, title="Propagated Geocoding Score", description="""Geocoder score (0-1) propagated from the upstream geocoder so the exposure record knows the spatial precision of its anchor.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When software converts an address '
                                                  'into map coordinates it also rates '
                                                  'its own confidence, from 0 to 1. '
                                                  'This carries that rating along with '
                                                  'the exposure record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The score quantifies how '
                                                    'confident the geocoder was in its '
                                                    'address match; without it '
                                                    'downstream analysts cannot apply '
                                                    'quality cutoffs, and poorly '
                                                    'matched addresses contaminate the '
                                                    'exposure assignment invisibly.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'value': '0.95'}],
         'see_also': ['https://degauss.org/']} })
    geocoding_score_propagated_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Geocoding Score Is Missing", description="""Reason `geocoding_score_propagated` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the geocoder-confidence field '
                                                  'is empty, this says why.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Records whether the score was '
                                                    'never produced or was produced '
                                                    'but dropped by the pipeline — the '
                                                    'difference between an upstream '
                                                    'limitation and a fixable ETL '
                                                    'gap.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'the geocoder emitted a score but the pipeline '
                                      'dropped it',
                       'value': 'upstream_data_not_propagated'}]} })
    address_period_alignment: Optional[AddressPeriodAlignmentEnum] = Field(default=None, title="Address Period Alignment", description="""How the patient's location-over-time (the spatial axis of trajectory resolution) was modelled.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'People move house and travel, so '
                                                  '"where the patient was" changes '
                                                  'over time. This records whether the '
                                                  'study used one fixed address, a '
                                                  'full address history, or accounted '
                                                  'for known trips away from home.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Assuming a single static address '
                                                    'smears home-location exposure '
                                                    'across days the patient was '
                                                    'actually elsewhere; how '
                                                    'location-over-time was modelled '
                                                    'changes which days get which '
                                                    'values and can bias exposure '
                                                    'estimates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'an EMR-sourced address history covers the '
                                      'observation period',
                       'value': 'address_history_from_emr'}]} })
    clinical_date_assignment_convention: Optional[ClinicalDateAssignmentEnum] = Field(default=None, title="Clinical Date Assignment Convention", description="""The clinical-side mirror of `day_boundary_convention` (envar_temporal): which timezone / day-boundary rule collapsed the clinical timestamp to the date used in the join. A boundary mismatch between this and the exposure-side `day_boundary_convention` silently misattributes boundary-hour events to the wrong day, which is what makes the Core `day_boundary_convention` checkable at all. Metadata *about the join* — never the clinical timestamp itself; carries no PHI.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A hospital visit at 11 pm can count '
                                                  'as "today" or "tomorrow" depending '
                                                  'on which clock and cutoff you use. '
                                                  'This records the rule the clinical '
                                                  'data used to turn a timestamp into '
                                                  'a calendar date.'},
                         'justification': {'tag': 'justification',
                                           'value': 'If the clinical side collapsed '
                                                    'timestamps to dates with a '
                                                    'different day-boundary rule than '
                                                    'the exposure side, events near '
                                                    'midnight are silently joined to '
                                                    "the wrong day's exposure; "
                                                    'recording both rules is what '
                                                    'makes that mismatch detectable at '
                                                    'all.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'matches the exposure-side '
                                      'day_boundary_convention (Daymet tmax scenario)',
                       'value': 'local_midnight'},
                      {'description': 'clinical record carried only a date, so no '
                                      'boundary rule applies (ACAG PM2.5 scenario)',
                       'value': 'date_only_no_time'}]} })
    clinical_date_assignment_convention_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Date Convention Is Missing", description="""Reason `clinical_date_assignment_convention` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the clinical date-rule field '
                                                  'is empty, this says why.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes a convention that '
                                                    'is undocumented at the source '
                                                    'from one the pipeline has not yet '
                                                    'extracted — which determines '
                                                    'whether the day-boundary '
                                                    'cross-check can ever be '
                                                    'completed.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'the clinical system documents its convention '
                                      'but the pipeline does not yet surface it',
                       'value': 'available_but_not_extracted'}]} })
    partial_day_attribution_rule: Optional[PartialDayAttributionEnum] = Field(default=None, title="Partial-Day Attribution Rule", description="""How boundary / transition days of the patient's trajectory (trip start / end, travel days) are attributed when location changes within a day. The temporal partner to the `known_travel_interval` address alignment.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If someone leaves on a trip '
                                                  "mid-day, which place's environment "
                                                  '"counts" for that day? This records '
                                                  'the choice — the place they left, '
                                                  'the place they arrived, both, or '
                                                  'neither.'},
                         'justification': {'tag': 'justification',
                                           'value': 'On a transition day the patient '
                                                    'is in two places; whether that '
                                                    'day is credited to the origin, '
                                                    'the destination, both, or '
                                                    'excluded changes which exposure '
                                                    'value the day receives, and an '
                                                    'undocumented rule makes the '
                                                    'linkage irreproducible.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'no trajectory transitions occur in the '
                                      'observation period',
                       'value': 'not_applicable'}]} })
    partial_day_attribution_rule_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Attribution Rule Is Missing", description="""Reason `partial_day_attribution_rule` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the travel-day rule field is '
                                                  'empty, this says why.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Separates "not applicable — the '
                                                    'patient never changed location" '
                                                    'from an undocumented handling of '
                                                    'travel days; without it a null '
                                                    'rule cannot be audited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'the trajectory source does not document '
                                      'transition-day handling',
                       'value': 'not_provided_by_source'}]} })
    lag_alignment_applied: Optional[LagAlignmentEnum] = Field(default=None, title="Lag Alignment Applied", description="""Whether and how values were lag-aligned to a clinical event. Relocated from envar_temporal: lag alignment attaches a value to an event (a linkage concern), not an intrinsic temporal property. See `lag_alignment_specifier` for the concrete lag value(s).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health effects can trail exposure '
                                                  'by days — a heat wave today may '
                                                  'send someone to hospital next week '
                                                  '— so analyses sometimes pair a '
                                                  'clinical event with earlier '
                                                  'exposure values. This records '
                                                  'whether such a shift was already '
                                                  'built into the data.'},
                         'justification': {'tag': 'justification',
                                           'value': 'If values were already shifted '
                                                    'relative to the clinical event '
                                                    'and this is not recorded, an '
                                                    'analyst may apply the lag again — '
                                                    'double-lagging is a silent '
                                                    'analytic error that misdates '
                                                    'every exposure.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'values are at native dates; no lag alignment '
                                      'applied',
                       'value': 'none'}],
         'see_also': ['https://cran.r-project.org/package=dlnm']} })
    lag_alignment_specifier: Optional[str] = Field(default=None, title="Lag Alignment Specifier", description="""Free-form specifier paired with `lag_alignment_applied` to capture the concrete lag values (e.g. `\"3\"` for a 3-day lag, or `\"0-21\"` for a distributed lag from 0 to 21 days). Empty when `lag_alignment_applied` = `none`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This spells out exactly how many '
                                                  'days the exposure values were '
                                                  'shifted relative to the clinical '
                                                  'event — for example 3 days, or a '
                                                  'whole range like 0 to 21 days.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Knowing that a lag was applied is '
                                                    'useless without the concrete '
                                                    'value(s); a 3-day lag and a '
                                                    'distributed lag over 0-21 days '
                                                    'define entirely different '
                                                    'exposure windows and cannot be '
                                                    'reconstructed after the fact.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'distributed lag from 0 to 3 days before the '
                                      'clinical event (with lag_alignment_applied = '
                                      'distributed_lag)',
                       'value': '0-3'}]} })
    lag_alignment_applied_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Lag Alignment Is Missing", description="""Reason `lag_alignment_applied` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the lag field is empty, this '
                                                  'says why — for example because the '
                                                  'documentation is still being '
                                                  'written.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Records why the lag-alignment '
                                                    'status is unknown; without it '
                                                    'analysts cannot tell whether the '
                                                    'data is safely unlagged or the '
                                                    'documentation simply has not '
                                                    'caught up, leaving the '
                                                    'double-lagging risk open.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['LinkageMethod'],
         'examples': [{'description': 'lag-alignment documentation for this ETL is '
                                      'still being populated',
                       'value': 'under_investigation'}]} })


class ToolRun(ConfiguredBaseModel):
    """
    A single tool invocation that produced an output from one or more inputs: tool name and version, container image (where applicable), arguments, environment, run timestamp and duration, input / output hashes and row counts, and an optional log excerpt.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'class_uri': 'prov:Activity',
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/toolrun',
         'see_also': ['https://www.w3.org/TR/prov-o/'],
         'slot_usage': {'tool_name': {'name': 'tool_name', 'required': True},
                        'tool_version': {'name': 'tool_version', 'required': True}},
         'title': 'Tool Run'})

    tool_name: str = Field(default=..., title="Tool Name", description="""Tool name, e.g. `daymet`, `narr`, `pm`, `amadeus`, `geocoder`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This simply records which program '
                                                  'was used — like noting the make and '
                                                  'model of an appliance before '
                                                  'describing its settings. Everything '
                                                  'else about the run only makes sense '
                                                  'once you know what tool ran.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the tool name, a consumer '
                                                    'cannot tell which piece of '
                                                    'software produced the value, so '
                                                    'the run cannot be re-executed and '
                                                    "the tool's known behaviours and "
                                                    'biases cannot be looked up. It is '
                                                    'the entry point for every '
                                                    'reproducibility check on the '
                                                    'run.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['ToolRun'],
         'examples': [{'description': 'DeGAUSS Daymet extraction tool',
                       'value': 'daymet'}],
         'see_also': ['https://degauss.org/']} })
    tool_version: str = Field(default=..., title="Tool Version", description="""Semver tool version. Mandatory.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Software changes over time, and a '
                                                  'version number labels one specific '
                                                  'edition of it — like the edition of '
                                                  'a book. Recording it says exactly '
                                                  'which edition of the tool did the '
                                                  'work.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Two versions of the same tool can '
                                                    'produce different outputs from '
                                                    'identical inputs, so "we ran '
                                                    'daymet" without a version is not '
                                                    'reproducible. It is mandatory '
                                                    'because it is the cheapest and '
                                                    'most decisive reproducibility '
                                                    'anchor after the tool name.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '1.0.0'}],
         'see_also': ['https://semver.org/']} })
    tool_description: Optional[str] = Field(default=None, title="Tool Description", description="""One-line tool description (from the tool's `dht` env var or equivalent).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A short plain-language note on the '
                                                  'tool\'s job, for example "extracts '
                                                  'daily temperature for a list of '
                                                  'addresses". It saves the reader a '
                                                  'lookup elsewhere.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A one-line description lets a '
                                                    'reader understand what the tool '
                                                    'does without leaving the record '
                                                    'or resolving the tool name '
                                                    'against external documentation. '
                                                    'Omitting it costs readability, '
                                                    'not reproducibility.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': 'DeGAUSS Daymet extraction container'}],
         'see_also': ['https://degauss.org/']} })
    container_image_repository: Optional[str] = Field(default=None, title="Container Image Repository", description="""Container image repository, e.g. `ghcr.io/degauss-org/daymet`. Null for non-containerised tools.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Containers are self-contained '
                                                  'software bundles, and the '
                                                  'repository is the public shelf '
                                                  'address where a bundle is published '
                                                  '— effectively the download location '
                                                  'of the exact software package '
                                                  'used.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The repository says where the '
                                                    'packaged software lives, so '
                                                    'anyone can pull the same '
                                                    'container and re-run the step. '
                                                    'Without it the image digest has '
                                                    'nothing to be resolved against, '
                                                    'and re-execution requires '
                                                    'guessing where the tool came '
                                                    'from.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': 'ghcr.io/degauss-org/daymet'}],
         'see_also': ['https://degauss.org/']} })
    container_image_repository_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Image Repository Is Missing", description="""Reason `container_image_repository` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the repository field is '
                                                  'deliberately empty, this note says '
                                                  'why — for example, the tool simply '
                                                  'was not run inside a container. An '
                                                  'explained blank can be trusted; an '
                                                  'unexplained one is a question '
                                                  'mark.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A blank repository is ambiguous — '
                                                    'it could mean "the tool is not '
                                                    'containerised" or "we forgot to '
                                                    'record it". Stating the reason '
                                                    'turns a silent gap into checkable '
                                                    'information; a blank is a bug, a '
                                                    'null-with-reason is information.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'description': 'e.g. the tool is not containerised',
                       'value': 'not_applicable'}]} })
    container_image_digest: Optional[str] = Field(default=None, title="Container Image Digest", description="""SHA256 of the container image actually used (not just the tag). Reproducibility-critical.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A digest is an exact serial number '
                                                  'for the software bundle actually '
                                                  'used — stronger than a version '
                                                  'label, which can be reused for '
                                                  'different contents. If the bundle '
                                                  'changes at all, the serial number '
                                                  'changes.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Image tags are mutable, so "same '
                                                    'tag" does not mean same code; '
                                                    'only the digest pins the exact '
                                                    'bytes that ran. It is the '
                                                    'strongest reproducibility anchor '
                                                    'available for a containerised '
                                                    'run.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': 'sha256:a8b3c2d1e0f9...'}],
         'see_also': ['https://github.com/opencontainers/image-spec']} })
    container_image_digest_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Image Digest Is Missing", description="""Reason `container_image_digest` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This note explains why the software '
                                                  "bundle's exact serial number was "
                                                  'not recorded — often the runner '
                                                  'only kept the human-friendly '
                                                  'version label and never looked up '
                                                  'the precise identifier behind it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a stated reason, a '
                                                    'missing digest is '
                                                    'indistinguishable from a pipeline '
                                                    'bug; with one (e.g. the runner '
                                                    'never resolved the tag) the gap '
                                                    'is auditable and fixable rather '
                                                    'than silent.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'description': 'e.g. the runner did not resolve the tag to a '
                                      'digest',
                       'value': 'available_but_not_extracted'}]} })
    run_arguments: Optional[str] = Field(default=None, title="Run Arguments", description="""The exact argument map passed at invocation, serialised as a JSON string.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'These are the settings the program '
                                                  'was started with — like the knob '
                                                  'positions on a machine. Writing '
                                                  'them down means someone else can '
                                                  'set the knobs identically before '
                                                  'pressing start.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The same tool run with different '
                                                    'arguments produces different '
                                                    'outputs; without the exact '
                                                    'argument map, re-running the tool '
                                                    'reproduces the tool, not the '
                                                    'result. Recording it verbatim '
                                                    'removes all guesswork about '
                                                    'settings.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '{"variables": "tmax"}'}]} })
    run_timestamp_utc: Optional[datetime ] = Field(default=None, title="Run Timestamp (UTC)", description="""When the run started (UTC).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Simply when the program started, '
                                                  'expressed on a single worldwide '
                                                  'clock (UTC) so that times recorded '
                                                  'on different machines in different '
                                                  'time zones line up.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The timestamp orders runs within '
                                                    'the provenance chain and lets '
                                                    'auditors match the record against '
                                                    'external logs and the state of '
                                                    'upstream data sources at that '
                                                    'moment. Without it, "which run '
                                                    'produced this file" can become '
                                                    'undecidable.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '2026-05-23T14:18:42Z'}],
         'see_also': ['https://www.w3.org/TR/prov-o/']} })
    run_duration_seconds: Optional[float] = Field(default=None, title="Run Duration (Seconds)", description="""How long the run took, in seconds.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'How long the program ran, in '
                                                  'seconds. A wildly unusual run time '
                                                  'is often the first clue that '
                                                  'something went wrong even when the '
                                                  'tool reported success.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Duration is a cheap sanity signal '
                                                    '— a step that normally takes an '
                                                    'hour finishing in two seconds '
                                                    'hints at silent failure or '
                                                    'truncated input. Omitting it '
                                                    'loses a diagnostic, not '
                                                    'reproducibility.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '37'}]} })
    run_environment: Optional[Any] = Field(default=None, title="Run Environment", description="""Host OS, Docker / podman version, R / Python version, key library versions, as a native key/value object.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A snapshot of the computer setup '
                                                  'around the tool — operating system, '
                                                  'language versions, key libraries. '
                                                  'Like noting the oven and altitude '
                                                  'alongside a recipe, because the '
                                                  'surroundings can change the '
                                                  'outcome.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Library and runtime versions can '
                                                    'change numeric results even when '
                                                    'the tool version is fixed; '
                                                    'recording the environment '
                                                    'explains otherwise-mysterious '
                                                    'differences between re-runs. For '
                                                    'non-containerised tools it is the '
                                                    'only record of the software '
                                                    'stack.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'object': {'container_runtime': 'docker 24.0.7',
                                  'os': 'Ubuntu 22.04',
                                  'r_version': '4.3.1'}}]} })
    input_file_sha256: Optional[str] = Field(default=None, title="Input File SHA-256 Hash", description="""SHA256 of the input file (CSV / parquet).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A SHA-256 hash is a fingerprint of '
                                                  'a file — if even one byte changes, '
                                                  'the fingerprint changes completely. '
                                                  'Comparing fingerprints proves two '
                                                  'files are exactly the same without '
                                                  'inspecting their contents.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The input hash lets anyone verify '
                                                    'they are re-running on '
                                                    'byte-identical inputs; without '
                                                    'it, a "reproduction" may quietly '
                                                    'use different data, and '
                                                    'disagreements can no longer be '
                                                    'traced to inputs versus code.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '9f8e7d6c5b4a...'}],
         'see_also': ['https://doi.org/10.6028/NIST.FIPS.180-4']} })
    input_row_count: Optional[int] = Field(default=None, title="Input Row Count", description="""Number of rows in the input.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Just the number of lines of data '
                                                  'that went in. If you expected 3 '
                                                  'addresses and the count says 2, '
                                                  'something was lost before the tool '
                                                  'ever ran.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The row count is a coarse but '
                                                    'instant integrity check — a '
                                                    'truncated or partially delivered '
                                                    'input shows up immediately as the '
                                                    'wrong count. It also anchors the '
                                                    'input side of input/output '
                                                    'cardinality checks.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'description': 'one row per cohort address', 'value': '3'}]} })
    output_file_sha256: Optional[str] = Field(default=None, title="Output File SHA-256 Hash", description="""SHA256 of the output file (CSV / parquet).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A fingerprint of the result file — '
                                                  'change one byte and the fingerprint '
                                                  'changes. It ties this metadata '
                                                  'record to exactly one version of '
                                                  'the data it describes.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The output hash proves the '
                                                    'companion data file is the one '
                                                    'this metadata describes; without '
                                                    'it, a swapped or regenerated file '
                                                    'can silently detach the values '
                                                    'from their provenance.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '1c2d3e4f5a6b...'}],
         'see_also': ['https://doi.org/10.6028/NIST.FIPS.180-4']} })
    output_row_count: Optional[int] = Field(default=None, title="Output Row Count", description="""Number of rows in the output.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The number of lines of data '
                                                  'produced. Outputs often have a '
                                                  'predictable size, so a wrong count '
                                                  'is an early warning that rows went '
                                                  'missing along the way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The expected output cardinality '
                                                    '(e.g. 3 subjects × 153 days = 459 '
                                                    'rows) is checkable at a glance; a '
                                                    'mismatch flags dropped subjects '
                                                    'or dates before any analysis runs '
                                                    'on the data.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ToolRun'],
         'examples': [{'description': '3 subjects × 153 days', 'value': '459'}]} })
    run_log_excerpt: Optional[str] = Field(default=None, title="Run Log Excerpt", description="""Last ~50 lines of the run log, where useful for debugging or audit.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The last few lines the program '
                                                  'printed while running — its own '
                                                  'account of what it did and whether '
                                                  'anything looked wrong. Keeping a '
                                                  'snippet is like stapling the '
                                                  'receipt to the record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The log tail captures warnings '
                                                    'and error summaries that no '
                                                    'structured field carries; without '
                                                    'it, diagnosing a suspect run '
                                                    'means hunting for logs that may '
                                                    'no longer exist. Omission costs '
                                                    'auditability, not '
                                                    'reproducibility.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'value': '[2026-05-23 14:19:19] daymet 1.0.0 finished: wrote '
                                '459 rows to /output/tmax.csv (0 errors, 0 warnings)'}]} })
    run_log_excerpt_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Log Excerpt Is Missing", description="""Reason `run_log_excerpt` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A note explaining why no log '
                                                  'snippet is attached — often the '
                                                  'logs live on the machine that ran '
                                                  'the job and were simply never '
                                                  'copied into the record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Stating why the log excerpt is '
                                                    'absent (e.g. logs exist on the '
                                                    'runner but are not captured) '
                                                    'distinguishes a deliberate '
                                                    'omission from data loss and tells '
                                                    'auditors where to look. A blank '
                                                    'is a bug; a null-with-reason is '
                                                    'information.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ToolRun'],
         'examples': [{'description': 'e.g. logs exist on the runner but are not '
                                      'captured by the pipeline',
                       'value': 'available_but_not_extracted'}]} })


class ProvenanceChain(ConfiguredBaseModel):
    """
    The ordered list of all upstream `ToolRun`s whose outputs were inputs to this run, terminating in a typed root. Patterned after W3C PROV (`prov:wasDerivedFrom`, `prov:wasGeneratedBy`).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'class_uri': 'prov:Bundle',
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/toolrun',
         'see_also': ['https://www.w3.org/TR/prov-o/',
                      'https://www.w3.org/TR/prov-primer/'],
         'title': 'Provenance Chain'})

    provenance_chain_steps: Optional[list[ToolRun]] = Field(default=None, title="Provenance Chain Steps", description="""Ordered list of upstream `ToolRun`s, from oldest to most recent, whose outputs were inputs to this run.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A step-by-step history of every '
                                                  'program run that led to this data, '
                                                  "oldest first — like a parcel's "
                                                  'tracking history showing each '
                                                  'station it passed through on the '
                                                  'way to you.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A value like a daily temperature '
                                                    'is usually the end of several '
                                                    'runs (geocode, then extract); '
                                                    'without the ordered steps a '
                                                    'consumer can verify only the last '
                                                    'hop, and any upstream error is '
                                                    'invisible. The chain lets anyone '
                                                    'walk the full derivation back to '
                                                    'its root.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ProvenanceChain'],
         'examples': [{'description': 'a single upstream geocoding step preceding the '
                                      'daymet run',
                       'object': {'output_file_sha256': '5b6c7d8e9f0a...',
                                  'run_timestamp_utc': '2026-05-23T14:02:11Z',
                                  'tool_name': 'geocoder',
                                  'tool_version': '3.3.0'}}],
         'see_also': ['https://www.w3.org/TR/prov-o/']} })
    provenance_chain_terminus_type: Optional[ProvenanceChainTerminusEnum] = Field(default=None, title="Provenance Chain Terminus Type", description="""The kind of root of the chain.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This says what the very first link '
                                                  'of the history is — freshly '
                                                  'downloaded raw data, simulated '
                                                  'data, or an existing curated '
                                                  'dataset. Different starting points '
                                                  'deserve different levels of '
                                                  'scrutiny.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A chain that just stops is '
                                                    'unverifiable — stating whether it '
                                                    'ends at a raw source download, '
                                                    'synthetic data, or a pre-existing '
                                                    'curated dataset tells consumers '
                                                    'what kind of trust the root '
                                                    'deserves, and makes the '
                                                    'no-orphaned-steps validation rule '
                                                    'checkable.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['ProvenanceChain'],
         'examples': [{'value': 'raw_source_download'}]} })
    chain_compatibility_assertions: Optional[list[str]] = Field(default=None, title="Chain Compatibility Assertions", description="""Declarations that two chain steps are compatible (e.g. `daymet@1.0.0` expects `geocoder@>=3.0.0` output column schema). Optional but enables strict-mode validation.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'These are notes saying "step B was '
                                                  'built to accept what step A '
                                                  'produces" — like declaring that a '
                                                  'plug and a socket follow the same '
                                                  'standard, so a checker can catch '
                                                  'mismatched pairs automatically.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Version bumps in one chain step '
                                                    'can silently break the '
                                                    'assumptions of the next (e.g. a '
                                                    'changed output column schema); '
                                                    'explicit compatibility '
                                                    'declarations make such mismatches '
                                                    'machine-checkable in strict mode '
                                                    'instead of surfacing later as '
                                                    'wrong values.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['ProvenanceChain'],
         'examples': [{'object': 'daymet@1.0.0 expects geocoder@>=3.0.0 output column '
                                 'schema'}]} })


class DerivedHeatMetric(ConfiguredBaseModel):
    """
    Methodology slots specific to derived heat metrics (WBGT, Heat Index, UTCI, apparent temperature, heat-wave flag, etc.). Captures the decisions that the heat-epidemiology literature flags as critical sources of cross-study disagreement: which equation variant, which indoor / outdoor regime, which solar-radiation input, and -- for percentile-based metrics -- the reference period, scope, and seasonal window. One per record where applicable.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/heat_metric',
         'see_also': ['https://en.wikipedia.org/wiki/Wet-bulb_globe_temperature',
                      'https://www.weather.gov/safety/heat-index',
                      'http://www.utci.org/'],
         'slot_usage': {'heat_metric_family': {'name': 'heat_metric_family',
                                               'required': True},
                        'indoor_outdoor': {'name': 'indoor_outdoor', 'required': True}},
         'title': 'Derived Heat Metric'})

    heat_metric_family: HeatMetricFamilyEnum = Field(default=..., title="Heat Metric Family", description="""The family of heat metric this variable represents.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'There are many different "heat '
                                                  'numbers" — plain air temperature, '
                                                  'composite scores that also fold in '
                                                  'humidity, wind and sunshine, or a '
                                                  'simple yes/no heat-wave flag. This '
                                                  'field says which kind of heat '
                                                  'number the record is about.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Tmax, Heat Index, WBGT, and a '
                                                    'heat-wave flag are distinct '
                                                    'exposures with distinct health '
                                                    'associations; without the family, '
                                                    'values from different metrics are '
                                                    'indistinguishable and get pooled '
                                                    'as if they measured the same '
                                                    'thing.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'outdoor Wet Bulb Globe Temperature (Phoenix '
                                      '2022 heat-wave record)',
                       'value': 'wbgt_outdoor'}]} })
    equation_variant: Optional[EquationVariantEnum] = Field(default=None, title="Equation Variant", description="""For derived heat metrics, the equation variant used. Mandatory for WBGT, HI, and UTCI: a Liljegren WBGT and an ACSM WBGT for the same inputs can differ by 2-3 °C.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Well-known heat metrics have '
                                                  'several published formulas that '
                                                  'share one name but differ '
                                                  'mathematically — like recipes with '
                                                  'the same title from different '
                                                  'cookbooks. This records which exact '
                                                  'recipe was used to cook the '
                                                  'number.'},
                         'justification': {'tag': 'justification',
                                           'value': 'WBGT approximations diverge '
                                                    'materially from the reference '
                                                    'model — well beyond 2-3 °C in '
                                                    'hot-humid conditions — so two '
                                                    'studies using "WBGT" with '
                                                    'different variants are measuring '
                                                    'systematically different '
                                                    'quantities; pooling them without '
                                                    'this field mixes those quantities '
                                                    'silently.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'Liljegren et al. 2008 outdoor WBGT formulation',
                       'value': 'liljegren_2008'}],
         'see_also': ['https://en.wikipedia.org/wiki/Wet-bulb_globe_temperature']} })
    equation_variant_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Equation Variant Is Missing", description="""Reason `equation_variant` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "no equation '
                                                    'variant exists for this metric" '
                                                    'from "the variant was used but '
                                                    'never captured" — the first is '
                                                    'fine, the second means the record '
                                                    'is unusable for cross-study '
                                                    'comparison and someone should go '
                                                    'back to the producer.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    equation_inputs: Optional[list[EquationInput]] = Field(default=None, title="Equation Inputs", description="""Typed per-input references for a multi-input derived metric (Heat Index from T + RH; WBGT from T + RH + wind + radiation). Each entry names the input's role and points, by `provenance_id`, to the upstream sidecar carrying that input's full context — it is an index into the lineage, not an inline copy of it.
Option-B decomposition (see the `EquationInput` class): when the inputs originate from different products and diverge in resolution, day-boundary convention, or temporal aggregation, each input is a full upstream sidecar referenced here and listed as a step in `provenance_chain`, so the divergence stays explicit and checkable.
Conditionally-Core: optional for a single-input metric, mandatory the moment a metric has more than one input.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Composite heat metrics are cooked '
                                                  'from several ingredients — '
                                                  'temperature, humidity, wind, '
                                                  'sunshine. This is the ingredient '
                                                  'list, where each entry points to '
                                                  "that ingredient's own full "
                                                  'paperwork instead of hiding it '
                                                  'inside the final number.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Multi-input metrics can silently '
                                                    'absorb mismatched inputs — e.g. a '
                                                    'Heat Index built from a 1 km '
                                                    'local-midnight daily-max '
                                                    'temperature and a ~31 km UTC '
                                                    'daily-mean humidity. Without '
                                                    'per-input references that '
                                                    'divergence is invisible and no '
                                                    'checker can surface it.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'comments': ['Cross-input consistency check (completeness checker, not '
                      'structural LinkML validation): when more than one entry is '
                      'present, dereference each `input_provenance_id` and WARN if the '
                      "referenced inputs' day-boundary conventions, temporal "
                      'aggregation windows, or native spatial resolutions differ. A '
                      'divergence is allowed but must be recorded via the decomposed '
                      'sidecars rather than absorbed silently into the output value.'],
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'one entry of the list — the air-temperature '
                                      'input of a Liljegren WBGT; a wind-speed entry '
                                      'from a divergent product (e.g. ~31 km ERA5) '
                                      'would sit alongside it as a second element',
                       'object': {'input_provenance_id': '01HFA7K8R3M6XP-daymet-tmax',
                                  'input_role': 'air_temperature',
                                  'input_source_short_code': 'daymet_v4'}},
                      {'description': 'a second list entry from a divergent product '
                                      '(~31 km ERA5 vs 1 km Daymet), pointing at its '
                                      'own full upstream sidecar',
                       'object': {'input_provenance_id': '01HFA7K8R3M6XP-era5-wind',
                                  'input_role': 'wind_speed',
                                  'input_source_short_code': 'era5'}}]} })
    equation_validity_range: Optional[str] = Field(default=None, title="Equation Validity Range", description="""Validity-range conditions for the equation, serialised as a JSON string. For Heat Index: `{\"min_temperature_F\": 80, \"min_relative_humidity_pct\": 40}` — Rothfusz is undefined below 80 °F / 40 % RH.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Every formula only works within a '
                                                  'fence of weather conditions it was '
                                                  'designed for. This field writes the '
                                                  'fence down, so anyone can check '
                                                  'whether a value was computed inside '
                                                  'or outside it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The Rothfusz Heat Index is '
                                                    'undefined below ~80 °F / 40 % RH; '
                                                    'applied outside its range an '
                                                    'equation produces '
                                                    'plausible-looking nonsense. '
                                                    'Without the recorded range, no '
                                                    'downstream consumer can flag '
                                                    'values computed where the formula '
                                                    'does not hold.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'Liljegren 2008 clamps wind speed below 0.13 m/s',
                       'value': '{"min_wind_speed_m_s": 0.13}'}],
         'see_also': ['https://www.weather.gov/safety/heat-index']} })
    equation_validity_range_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Validity Range Is Missing", description="""Reason `equation_validity_range` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "this equation has '
                                                    'no published validity range" from '
                                                    '"the range exists but was not '
                                                    'captured" — the difference '
                                                    'decides whether out-of-range '
                                                    'screening is impossible or merely '
                                                    'deferred.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    indoor_outdoor: IndoorOutdoorEnum = Field(default=..., title="Indoor or Outdoor Regime", description="""Indoor / outdoor regime. Mandatory for WBGT (the indoor vs outdoor distinction changes the equation and the health interpretation).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Heat stress works differently '
                                                  'inside and outside — indoors there '
                                                  'is no direct sun and little wind — '
                                                  'so heat metrics come in indoor and '
                                                  'outdoor versions, and you need to '
                                                  'know which one you are looking at.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Indoor and outdoor WBGT use '
                                                    'different equations and carry '
                                                    'different health interpretations; '
                                                    'an indoor formula applied to '
                                                    'outdoor conditions (or a regime '
                                                    'left unstated) makes the value '
                                                    'invalid or uninterpretable for '
                                                    'the exposure being claimed.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'outdoor'}],
         'see_also': ['https://www.iso.org/standard/67188.html',
                      'https://en.wikipedia.org/wiki/Wet-bulb_globe_temperature']} })
    wind_speed_measurement_height_m: Optional[float] = Field(default=None, title="Wind Speed Measurement Height (Metres)", description="""For WBGT and UTCI inputs, the wind-speed measurement height in metres. The ISO 7243 standard is 2 m, but reanalysis products often supply 10 m -- the height affects the WBGT value.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Wind blows faster the higher above '
                                                  'the ground you measure it, so a '
                                                  '"wind speed" is only meaningful '
                                                  'together with the height it was '
                                                  'taken at — this field records that '
                                                  'height.'},
                         'justification': {'tag': 'justification',
                                           'value': 'ISO 7243 assumes wind measured at '
                                                    '2 m, but reanalysis products '
                                                    'usually supply 10 m wind; wind is '
                                                    'slower near the ground, so an '
                                                    'uncorrected 10 m input '
                                                    'systematically shifts the '
                                                    'resulting WBGT.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'ERA5 10 m wind used without height adjustment',
                       'value': '10'}],
         'see_also': ['https://www.iso.org/standard/67188.html']} })
    wind_speed_measurement_height_m_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Measurement Height Is Missing", description="""Reason `wind_speed_measurement_height_m` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "the producer never '
                                                    'recorded a measurement height" '
                                                    'from "it exists upstream but was '
                                                    'not extracted" — only the latter '
                                                    'is recoverable, and only the '
                                                    'former precludes a height '
                                                    'correction.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'available_but_not_extracted'}]} })
    solar_radiation_basis: Optional[SolarRadiationBasisEnum] = Field(default=None, title="Solar Radiation Basis", description="""For WBGT / UTCI inputs, the basis used for solar radiation.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'How much sunshine hits a person is '
                                                  'part of how hot they feel, and '
                                                  'datasets represent "sunshine" in '
                                                  'different ways — or not at all. '
                                                  'This says which representation fed '
                                                  'the calculation.'},
                         'justification': {'tag': 'justification',
                                           'value': 'WBGT and UTCI respond strongly to '
                                                    'solar load; whether the sun input '
                                                    'was a measured shortwave flux, a '
                                                    'modelled mean radiant '
                                                    'temperature, or absent '
                                                    '(triggering a fallback formula) '
                                                    'changes the value and whether two '
                                                    'records are comparable at all.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'surface_downwelling_shortwave_flux'}]} })
    solar_radiation_basis_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Radiation Basis Is Missing", description="""Reason `solar_radiation_basis` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "the source never '
                                                    'stated its radiation basis" from '
                                                    '"it was not extracted" — deciding '
                                                    'whether the ambiguity can be '
                                                    'resolved by going back to the '
                                                    'source or is permanent.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    heat_wave_threshold_definition: Optional[HeatWaveThresholdDefinitionEnum] = Field(default=None, title="Heat-Wave Threshold Definition", description="""For heat-wave flags, the definition of the threshold (absolute, percentile-local, percentile-climatological, NWS advisory, ETCCDI).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'There is no universal definition of '
                                                  'a heat wave. "Above 35 °C" and '
                                                  '"hotter than 95 % of days usually '
                                                  'are here" are both in use and flag '
                                                  'different days — this field records '
                                                  'which rulebook was applied.'},
                         'justification': {'tag': 'justification',
                                           'value': 'At least seven heat-wave '
                                                    'definitions are in active use and '
                                                    'none are convertible after the '
                                                    'fact; two definitions can '
                                                    'disagree on most flagged days, '
                                                    'which changes both the exposure '
                                                    'series and the resulting '
                                                    'mortality estimate.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': '95th percentile of the local Tmax distribution',
                       'value': 'percentile_local'}],
         'see_also': ['https://en.wikipedia.org/wiki/Heat_wave']} })
    heat_wave_threshold_definition_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Threshold Definition Is Missing", description="""Reason `heat_wave_threshold_definition` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "this record is not '
                                                    'a heat-wave flag, so no threshold '
                                                    'definition exists" from "a '
                                                    'definition was used but not '
                                                    'captured" — the first is benign, '
                                                    'the second makes the flag '
                                                    'unusable.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_applicable'}]} })
    heat_wave_threshold_specifier: Optional[str] = Field(default=None, title="Heat-Wave Threshold Specifier", description="""Free-form specifier paired with `heat_wave_threshold_definition` to capture the concrete threshold values (e.g. `\"35_Cel\"` for an absolute threshold, `\"95\"` for the 95th percentile).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The threshold definition is the '
                                                  'type of cutoff; this is the actual '
                                                  'number plugged into it — like '
                                                  'knowing a speed limit exists versus '
                                                  'knowing it is 50.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The definition names the rule but '
                                                    'not the number: two records both '
                                                    'marked "percentile_local" are '
                                                    'still incomparable unless the '
                                                    'concrete value (95th vs 90th '
                                                    'percentile, 35 vs 40 °C) is '
                                                    'recorded here.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'percentile, paired with '
                                      'heat_wave_threshold_definition = '
                                      'percentile_local',
                       'value': '95'},
                      {'description': 'absolute threshold, paired with '
                                      'heat_wave_threshold_definition = absolute',
                       'value': '35_Cel'}]} })
    heat_wave_min_consecutive_days: Optional[int] = Field(default=None, title="Heat-Wave Minimum Consecutive Days", description="""Minimum-consecutive-days rule for heat-wave flags (commonly 2 or 3). Changes which days are flagged.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A heat wave means it stays hot for '
                                                  'several days in a row — but how '
                                                  'many days count as "several" is a '
                                                  'choice (usually 2 or 3), and the '
                                                  'choice changes which days get '
                                                  'flagged.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A 2-day rule and a 3-day rule '
                                                    'flag different sets of days from '
                                                    'the same temperature series, '
                                                    'changing which person-days count '
                                                    'as heat-wave-exposed and '
                                                    'therefore the effect estimates '
                                                    'built on them.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': '3'}]} })
    heat_wave_min_consecutive_days_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Consecutive Days Is Missing", description="""Reason `heat_wave_min_consecutive_days` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "not a heat-wave '
                                                    'flag, so no consecutive-days rule '
                                                    'applies" from "a rule was applied '
                                                    'but not recorded" — only the '
                                                    'latter undermines reuse of the '
                                                    'flag.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_applicable'}]} })
    percentile_reference_period_start: Optional[date] = Field(default=None, title="Percentile Reference Period Start", description="""Start of the reference distribution used for percentile-based thresholds. Mandatory for percentile metrics: \"95th percentile\" over 2000-2019 gives a different threshold than 1980-2010, and this delta is real.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': '"Unusually hot" means hot compared '
                                                  'to some stretch of past years. '
                                                  'Which years you compare against '
                                                  'changes what counts as unusual — '
                                                  'this field records where that '
                                                  'stretch begins.'},
                         'justification': {'tag': 'justification',
                                           'value': 'In a warming climate a "95th '
                                                    'percentile" computed over '
                                                    '1971-2000 is a materially '
                                                    'different threshold than one over '
                                                    '2000-2019; leaving the baseline '
                                                    'unstated makes percentile-based '
                                                    'studies non-comparable and '
                                                    'non-reproducible.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'start of the 1991-2020 climate-normal baseline',
                       'value': '1991-01-01'}],
         'see_also': ['https://www.ncei.noaa.gov/products/land-based-station/us-climate-normals']} })
    percentile_reference_period_start_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Period Start Is Missing", description="""Reason `percentile_reference_period_start` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "not a '
                                                    'percentile-based metric, so no '
                                                    'baseline exists" from "a baseline '
                                                    'was used but not captured" — '
                                                    'without the reason, a consumer '
                                                    'cannot tell a benign blank from a '
                                                    'blocking one.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_applicable'}]} })
    percentile_reference_period_end: Optional[date] = Field(default=None, title="Percentile Reference Period End", description="""End of the reference distribution.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The other end of the stretch of '
                                                  'past years used as the comparison — '
                                                  'start and end together say exactly '
                                                  'which years define "normal".'},
                         'justification': {'tag': 'justification',
                                           'value': 'Together with the start date this '
                                                    'pins down the reference '
                                                    'distribution; an end date that '
                                                    'includes or excludes the most '
                                                    'recent warm years shifts the '
                                                    'percentile threshold, so an '
                                                    'open-ended baseline is not '
                                                    'reproducible.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': '2020-12-31'}]} })
    percentile_reference_period_end_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Period End Is Missing", description="""Reason `percentile_reference_period_end` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "no percentile '
                                                    'baseline applies to this metric" '
                                                    'from "the baseline end was used '
                                                    'but never recorded" — deciding '
                                                    'whether the threshold is merely '
                                                    'undocumented or genuinely '
                                                    'absent.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_applicable'}]} })
    percentile_reference_geographic_scope: Optional[str] = Field(default=None, title="Percentile Reference Geographic Scope", description="""Geographic scope over which the reference distribution was computed. One of `local_tract`, `local_county`, `local_climate_region`, `national`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': '"Unusually hot" can mean hot '
                                                  'compared to what is normal HERE, or '
                                                  'compared to the whole country. This '
                                                  "field says which area's history the "
                                                  'comparison was made against.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A 95th percentile computed over '
                                                    'one county and one computed over '
                                                    'the whole nation are very '
                                                    'different thresholds; the scope '
                                                    'is what encodes "hot for here", '
                                                    'and without it the threshold '
                                                    'cannot be reproduced or compared '
                                                    'across studies.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'description': 'reference distribution computed over Maricopa '
                                      'County',
                       'value': 'local_county'}]} })
    percentile_reference_geographic_scope_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Geographic Scope Is Missing", description="""Reason `percentile_reference_geographic_scope` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "the source never '
                                                    'stated its baseline geography" '
                                                    'from "it was not extracted" — '
                                                    'telling consumers whether the '
                                                    'ambiguity is recoverable from the '
                                                    'source or permanent.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    percentile_reference_seasonal_window: Optional[str] = Field(default=None, title="Percentile Reference Seasonal Window", description="""Seasonal window over which the reference was computed. One of `annual`, `warm_season_may_sep`, `calendar_month`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Whether "normal" includes the whole '
                                                  'year or only the summer months '
                                                  'changes what counts as unusually '
                                                  'hot — a day that is extreme against '
                                                  'summer-only history may be '
                                                  'unremarkable against the full '
                                                  'year.'},
                         'justification': {'tag': 'justification',
                                           'value': 'An annual reference distribution '
                                                    'includes winter days and drags '
                                                    'the 95th percentile far below a '
                                                    'warm-season-only percentile; two '
                                                    'thresholds that sound identical '
                                                    'diverge substantially when the '
                                                    'seasonal window is left '
                                                    'unstated.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'warm_season_may_sep'}]} })
    percentile_reference_seasonal_window_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Seasonal Window Is Missing", description="""Reason `percentile_reference_seasonal_window` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "the source never '
                                                    'stated its seasonal window" from '
                                                    '"it was not extracted" — so '
                                                    'consumers know whether asking the '
                                                    'producer could still recover it.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'not_provided_by_source'}]} })
    metric_temporal_aggregation_rule: Optional[str] = Field(default=None, title="Metric Temporal Aggregation Rule", description="""For heat-wave flags, how multi-day exposures are stamped on individual days (e.g. `first_day_of_event` / `each_day_of_event` / `last_day_of_event`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A heat wave spans several days but '
                                                  'health records are kept day by day; '
                                                  'this says which calendar days '
                                                  'actually get the "heat wave" label '
                                                  '— just the first day, every day, or '
                                                  'the last.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Stamping a five-day event only on '
                                                    'its first day versus on every day '
                                                    'changes which person-days count '
                                                    'as exposed, directly altering '
                                                    'effect estimates in daily '
                                                    'time-series and case-crossover '
                                                    'designs.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'each_day_of_event'}]} })
    metric_temporal_aggregation_rule_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Aggregation Rule Is Missing", description="""Reason `metric_temporal_aggregation_rule` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A blank field is ambiguous: it '
                                                  'could mean the thing does not '
                                                  'exist, or that nobody wrote it '
                                                  'down. This companion field says '
                                                  'which one it is.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "no multi-day '
                                                    'stamping rule applies to this '
                                                    'metric" from "a rule was applied '
                                                    'but never captured" — only the '
                                                    'latter makes the daily exposure '
                                                    'series ambiguous.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DerivedHeatMetric'],
         'examples': [{'value': 'available_but_not_extracted'}]} })


class EquationInput(ConfiguredBaseModel):
    """
    A single physical-state input to a derived heat metric, recorded as a typed reference into the provenance chain rather than an inline copy of the input's metadata. It names the input's role (a CF standard name) and points, via `input_provenance_id`, to the upstream sidecar that carries that input's full spatial / temporal / model context.
    This is the Option-B decomposition: when a multi-input metric (Heat Index from T + RH; WBGT from T + RH + wind + radiation) draws its inputs from different products that diverge in resolution, day-boundary convention, or temporal aggregation, each input remains its own full sidecar — listed here and as a step in `provenance_chain` — so the divergence stays explicit and machine-checkable instead of being silently absorbed into the single output value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/heat_metric',
         'see_also': ['https://cfconventions.org/'],
         'slot_usage': {'input_provenance_id': {'name': 'input_provenance_id',
                                                'required': True},
                        'input_role': {'name': 'input_role', 'required': True}},
         'title': 'Equation Input'})

    input_role: str = Field(default=..., title="Input Role", description="""The standard-name local token of this input's physical quantity (the same quantity the referenced sidecar carries in `standard_name`), e.g. `air_temperature`, `relative_humidity`, `wind_speed`, `surface_downwelling_shortwave_flux_in_air`.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This labels what each ingredient '
                                                  'actually is — temperature versus '
                                                  'humidity versus wind — using a '
                                                  'shared standard vocabulary so that '
                                                  'machines and people read the label '
                                                  'the same way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a named role, a consumer '
                                                    'cannot tell which physical '
                                                    'quantity each referenced input '
                                                    'supplied to the equation, so '
                                                    'inputs cannot be matched to '
                                                    'equation terms and cross-input '
                                                    'consistency checks cannot run.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EquationInput'],
         'examples': [{'value': 'air_temperature'}],
         'see_also': ['https://cfconventions.org/']} })
    input_provenance_id: str = Field(default=..., title="Input Provenance ID", description="""The `provenance_id` of the upstream sidecar that fully describes this input — its source dataset, spatial / temporal reference, and exposure model. Dereferencing it lets a consumer (or the completeness checker) compare inputs and surface any divergence in resolution, day-boundary convention, or temporal aggregation.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Think of it as a tracking number: '
                                                  'instead of copying all the details '
                                                  'of the ingredient into this record, '
                                                  'we store a pointer to the record '
                                                  'that already holds them, and anyone '
                                                  'can follow the pointer.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the only '
                                                    'machine-followable link from an '
                                                    'input back to its full spatial, '
                                                    'temporal, and model context; '
                                                    'without it, divergences between '
                                                    'inputs in resolution, '
                                                    'day-boundary convention, or '
                                                    'aggregation cannot be detected at '
                                                    'all.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EquationInput'],
         'examples': [{'description': 'provenance_id of the upstream Daymet Tmax '
                                      'sidecar',
                       'value': '01HFA7K8R3M6XP-daymet-tmax'}],
         'see_also': ['https://www.w3.org/TR/prov-o/']} })
    input_source_short_code: Optional[str] = Field(default=None, title="Input Source Short Code", description="""Human-readable short code of the input's source product (e.g. `daymet_v4`, `era5`), duplicated from the referenced sidecar for convenience when scanning the record. Not authoritative — `input_provenance_id` is.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A friendly nickname for the dataset '
                                                  'an ingredient came from (like '
                                                  '"daymet_v4"), written next to the '
                                                  'tracking number so people do not '
                                                  'have to look everything up just to '
                                                  'get oriented.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Lets a human scanning the record '
                                                    'see at a glance which product '
                                                    'each input came from without '
                                                    'dereferencing every provenance '
                                                    'id; because it is a '
                                                    'non-authoritative duplicate, '
                                                    'omitting it costs readability, '
                                                    'not machine-checkability.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EquationInput'],
         'examples': [{'value': 'daymet_v4'}]} })


class HealthLayerLinkage(ConfiguredBaseModel):
    """
    Hooks the sidecar uses to be findable from a downstream health-data layer (OMOP, BioData Catalyst, …). These are *not* clinical metadata — they are the hooks the exposure record needs so a health-side row can resolve back to its provenance. The target layer is named in `health_layer_target`, so no single model is privileged. One per record.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/health_layer',
         'see_also': ['https://ohdsi.github.io/CommonDataModel/',
                      'https://biodatacatalyst.nhlbi.nih.gov/'],
         'title': 'Health-Layer Linkage'})

    health_layer_target: Optional[HealthLayerTargetEnum] = Field(default=None, title="Target Health-Data Layer", description="""The downstream health-data layer this sidecar links into. Names the target so `health_layer_link_field` is interpreted against the right model.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health records are stored in '
                                                  'different standard formats — for '
                                                  'example OMOP, a widely used common '
                                                  'format for health records, so tools '
                                                  "written for one hospital's data "
                                                  "work on another's. This slot simply "
                                                  'says which of those formats this '
                                                  'exposure record is meant to plug '
                                                  'into.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without naming the target layer, '
                                                    '`health_layer_link_field` is '
                                                    'ambiguous — a consumer cannot '
                                                    'know which data model the link '
                                                    'field belongs to, so the exposure '
                                                    'record cannot be reliably '
                                                    'resolved from the health side. '
                                                    'Naming the target in a slot '
                                                    '(rather than baking it into slot '
                                                    'names) is also what keeps the '
                                                    'schema neutral across health data '
                                                    'models.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['HealthLayerLinkage'],
         'examples': [{'description': 'OMOP CDM via the OHDSI GIS `external_exposure` '
                                      'table extension',
                       'value': 'omop_external_exposure'}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/']} })
    health_layer_link_field: Optional[str] = Field(default=None, title="Health-Layer Link Field", description="""Name of the field in the target health-data layer that carries `provenance_id`. For OMOP this is `external_exposure.exposure_source_value` (the default); other layers name their own field.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Think of the exposure record and '
                                                  'the patient database as two '
                                                  'spreadsheets that need to be '
                                                  'matched up. This slot names the '
                                                  'column in the patient-side '
                                                  'spreadsheet that holds the matching '
                                                  'ID, so anyone can connect the two '
                                                  'tables without guessing.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the join key declaration: '
                                                    'it names the exact field in the '
                                                    'health-data layer that holds this '
                                                    "record's `provenance_id`. Without "
                                                    'it, exposure rows cannot be '
                                                    'joined back to patients in the '
                                                    'health data model, and a '
                                                    'health-side row cannot resolve to '
                                                    'its exposure provenance.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['HealthLayerLinkage'],
         'examples': [{'description': 'the OMOP `external_exposure` field that carries '
                                      '`provenance_id`',
                       'value': 'exposure_source_value'}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/']} })
    cohort_size_anchored: Optional[int] = Field(default=None, title="Anchored Cohort Size", description="""Number of distinct persons this exposure record was extracted for. Helps downstream estimate the volume of health-layer rows the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This is simply a head count: how '
                                                  'many different people this exposure '
                                                  'record covers. It lets whoever '
                                                  'receives the data check that '
                                                  'nothing went missing along the '
                                                  'way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Gives downstream consumers a '
                                                    'volume expectation: without it, a '
                                                    'health-layer loader cannot '
                                                    'sanity-check whether the number '
                                                    'of exposure rows it receives '
                                                    'matches the number of persons the '
                                                    'record was extracted for, so '
                                                    'silent truncation or duplication '
                                                    'goes unnoticed.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['HealthLayerLinkage'],
         'examples': [{'description': 'three cohort members in the worked Phoenix '
                                      'example',
                       'value': '3'}]} })
    cohort_size_anchored_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Cohort Size Is Missing", description="""Reason `cohort_size_anchored` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'When the head count is missing, '
                                                  'this slot says why — for example, '
                                                  'the tool could have counted but did '
                                                  'not, or counting simply does not '
                                                  'apply. An explained blank is far '
                                                  'more useful than a silent one.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Distinguishes "the cohort size is '
                                                    'genuinely unknown" from "the '
                                                    'pipeline just did not record it". '
                                                    'Without the reason, a null count '
                                                    'is uninterpretable and downstream '
                                                    'users cannot tell whether to '
                                                    'chase the number or accept its '
                                                    'absence.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['HealthLayerLinkage'],
         'examples': [{'description': 'the pipeline could count anchored persons but '
                                      'does not yet surface it',
                       'value': 'available_but_not_extracted'}]} })


class DepositMetadata(ConfiguredBaseModel):
    """
    Deposit-time slots required when the sidecar travels alongside a published FAIR object (Zenodo / Dryad / C-HER / etc.). Most slots are pulled from other modules; this class names the required-for-deposit subset and adds a few deposit-specific slots.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/health_layer',
         'see_also': ['https://www.go-fair.org/fair-principles/',
                      'https://zenodo.org/'],
         'title': 'Deposit Metadata'})

    deposit_doi: Optional[str] = Field(default=None, title="Deposit DOI (Digital Object Identifier)", description="""DOI assigned by the deposit repository (e.g. Zenodo).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A DOI is a permanent ID for a '
                                                  'published dataset, like an ISBN for '
                                                  'a book. Whatever happens to the '
                                                  'hosting website, the DOI keeps '
                                                  'pointing to the dataset, so people '
                                                  'can always find and cite it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The DOI is the permanent, citable '
                                                    'identifier of the published '
                                                    'deposit — the F in FAIR. Without '
                                                    'it the record cannot be cited, '
                                                    'found in catalogues, or '
                                                    're-retrieved once the original '
                                                    'download link rots.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'description': 'illustrative Zenodo DOI from the worked Daymet '
                                      'Tmax example',
                       'value': '10.5281/zenodo.9999999'}],
         'see_also': ['https://www.doi.org/', 'https://zenodo.org/']} })
    deposit_doi_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Deposit DOI Is Missing", description="""Reason `deposit_doi` is null (e.g. pre-deposit).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If the permanent dataset ID is '
                                                  'missing, this slot explains why — '
                                                  'for instance the record is '
                                                  'circulating before publication and '
                                                  'the ID has not been issued yet.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Separates "this record was never '
                                                    'deposited" from "the DOI is '
                                                    'pending". Without it, a missing '
                                                    'DOI is ambiguous and a consumer '
                                                    'cannot tell whether a citable '
                                                    'identifier will ever exist for '
                                                    'this record.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'description': 'sidecar circulated pre-deposit; DOI pending',
                       'value': 'under_investigation'}]} })
    deposit_repository: Optional[DepositRepositoryEnum] = Field(default=None, title="Deposit Repository", description="""Repository hosting the deposit.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A deposit repository is a public '
                                                  'archive for research data — a place '
                                                  'like Zenodo where a dataset is '
                                                  'published with a permanent ID and '
                                                  'kept available long-term. This slot '
                                                  'records which archive was used.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Names where the deposited object '
                                                    'actually lives, which determines '
                                                    'access routes, retention '
                                                    'guarantees, and how the DOI '
                                                    'resolves. Without it, the '
                                                    "deposit's accessibility (the A in "
                                                    'FAIR) rests on the DOI alone and '
                                                    'cannot be assessed.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'value': 'zenodo'}],
         'see_also': ['https://zenodo.org/']} })
    deposit_repository_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Deposit Repository Is Missing", description="""Reason `deposit_repository` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If no archive is named, this slot '
                                                  'says why — most often because the '
                                                  'record was never meant to be '
                                                  'published as a standalone dataset '
                                                  'in the first place.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Makes an absent repository name '
                                                    'interpretable: most records are '
                                                    'never deposited, and this slot '
                                                    'records that this is deliberate '
                                                    'rather than an oversight, so '
                                                    'completeness checks do not raise '
                                                    'false alarms.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'description': 'the record is not published as a standalone '
                                      'FAIR deposit',
                       'value': 'not_applicable'}]} })
    deposit_license_spdx: Optional[str] = Field(default=None, title="Deposit License (SPDX Identifier)", description="""SPDX identifier of the license under which the *derived* exposure record (not the source) is published.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A license is the legal permission '
                                                  'slip attached to the data — for '
                                                  'example "you may reuse this if you '
                                                  'credit the authors". SPDX is just a '
                                                  'standard list of short codes for '
                                                  'licenses (like CC-BY-4.0), so '
                                                  'software can read the terms without '
                                                  'a lawyer.'},
                         'justification': {'tag': 'justification',
                                           'value': 'States, in a machine-readable '
                                                    'form, what a reuser is legally '
                                                    'allowed to do with the published '
                                                    'exposure record. Without it, '
                                                    'reuse of the deposit is legally '
                                                    'uncertain and cautious downstream '
                                                    'users must treat the data as '
                                                    'all-rights-reserved — the R in '
                                                    'FAIR fails.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'value': 'CC-BY-4.0'}],
         'see_also': ['https://spdx.org/licenses/']} })
    deposit_redistribution_constraints_inherited: Optional[list[str]] = Field(default=None, title="Inherited Redistribution Constraints", description="""Constraints from any input source that pass through to the deposit.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Datasets built from other datasets '
                                                  'can inherit rules from their '
                                                  'ingredients, the way a recipe using '
                                                  "someone's secret sauce may come "
                                                  'with strings attached. This slot '
                                                  'lists any such inherited rules so '
                                                  'nobody accidentally breaks them '
                                                  'when sharing the result.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A derived product can carry '
                                                    'restrictions from its inputs even '
                                                    'when its own license is '
                                                    'permissive; without recording '
                                                    'them, a deposit may violate an '
                                                    'upstream license — for example by '
                                                    'redistributing grids the source '
                                                    'forbids sharing. An explicit '
                                                    'empty list positively asserts '
                                                    'that nothing passes through.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'description': 'one inherited pass-through constraint (list '
                                      'element); an empty list is also valid and '
                                      'asserts that no constraints pass through',
                       'value': 'no redistribution of raw PRISM grids'}],
         'see_also': ['https://spdx.org/licenses/']} })
    recommended_citation: Optional[str] = Field(default=None, title="Recommended Citation", description="""One-line recommended citation derived from the slots above.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This is the one-line "how to credit '
                                                  'us" text, like the suggested '
                                                  'citation on the back of a report. '
                                                  'Anyone reusing the dataset can copy '
                                                  'it verbatim into their paper.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A ready-made citation lowers the '
                                                    'barrier to correct attribution: '
                                                    'without it, reusers assemble '
                                                    'citations by hand, producing '
                                                    'inconsistent references that '
                                                    'break citation tracking and '
                                                    'deprive the producers of credit '
                                                    'for the deposit.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'value': 'EnVar exposure record for cohort:phoenix_aki_2022 '
                                'daily Tmax (Daymet V4), 2026. Deposited at Zenodo, '
                                'doi:10.5281/zenodo.9999999.'}]} })
    dcat_distribution_url: Optional[str] = Field(default=None, title="Data-Catalog (DCAT) Distribution URL", description="""DCAT-compatible distribution URL for catalogue integration.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'DCAT is a standard way for data '
                                                  'catalogues — searchable indexes of '
                                                  'datasets, like a library catalogue '
                                                  '— to describe where a file can be '
                                                  'downloaded. This slot holds that '
                                                  'direct download address so '
                                                  'catalogue software can list and '
                                                  'fetch the data automatically.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This is the machine-actionable '
                                                    'download hook for data '
                                                    'catalogues: with it, the deposit '
                                                    'can be indexed and fetched by '
                                                    'DCAT-speaking catalogue software '
                                                    'without human mediation. Without '
                                                    'it, the record is findable by '
                                                    'humans (via the DOI) but '
                                                    'invisible to automated catalogue '
                                                    'harvesting.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'value': 'https://zenodo.org/record/9999999/files/tmax_phoenix.parquet'}],
         'see_also': ['https://www.w3.org/TR/vocab-dcat-3/']} })
    dcat_distribution_url_missing_reason: Optional[MissingReasonEnum] = Field(default=None, title="Reason Distribution URL Is Missing", description="""Reason `dcat_distribution_url` is null.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If there is no catalogue download '
                                                  'link, this slot explains why — '
                                                  'usually because the dataset was '
                                                  'never registered in a data '
                                                  'catalogue at all.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Records whether the absence of a '
                                                    'catalogue link is deliberate (the '
                                                    'record is simply not catalogued) '
                                                    'or a gap to be filled, so '
                                                    'automated FAIR-ness assessments '
                                                    'do not misreport an intentional '
                                                    'omission as missing metadata.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['DepositMetadata'],
         'examples': [{'description': 'the record is not registered in a DCAT '
                                      'catalogue',
                       'value': 'not_applicable'}]} })


class EnvironmentalExposureRecord(ConfiguredBaseModel):
    """
    A single environmental-exposure record sidecar: the complete metadata graph that travels alongside a value (or value series) emitted by an upstream tool. Composes variable identity, data layout, spatial / temporal reference, source dataset, exposure model, uncertainty, linkage, tool run, provenance chain, optional derived-heat-metric methodology, health-data-layer linkage hooks, and FAIR-deposit metadata.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'domain_of_use': {'tag': 'domain_of_use',
                                           'value': 'environmental_exposure'}},
         'from_schema': 'https://w3id.org/linkml/microschemas/envar/record',
         'instantiates': ['MicroschemaDefinition'],
         'see_also': ['https://github.com/linkml/linkml-microschema-profile'],
         'slot_usage': {'phi_status': {'name': 'phi_status',
                                       'slot_group': 'record_bookkeeping'},
                        'provenance_id': {'name': 'provenance_id',
                                          'slot_group': 'record_bookkeeping'},
                        'schema_version': {'name': 'schema_version',
                                           'slot_group': 'record_bookkeeping'},
                        'subject': {'annotations': {'open_question': {'tag': 'open_question',
                                                                      'value': '`subject` '
                                                                               'is the '
                                                                               'only '
                                                                               'field '
                                                                               'in '
                                                                               'this '
                                                                               'group '
                                                                               'that '
                                                                               'is not '
                                                                               'a '
                                                                               'per-value '
                                                                               'predicate: '
                                                                               'every '
                                                                               'other '
                                                                               'field '
                                                                               'explains '
                                                                               'an '
                                                                               'individual '
                                                                               'value, '
                                                                               'but a '
                                                                               'single '
                                                                               'scalar '
                                                                               'subject '
                                                                               'is '
                                                                               'dataset-scoped '
                                                                               'and '
                                                                               'cannot '
                                                                               'distribute '
                                                                               'over '
                                                                               'the '
                                                                               "sidecar's "
                                                                               'rows '
                                                                               '(per-row '
                                                                               'subject '
                                                                               'identity '
                                                                               'lives '
                                                                               'in '
                                                                               '`subject_column`). '
                                                                               'Under '
                                                                               'review '
                                                                               '— '
                                                                               'should '
                                                                               'it be '
                                                                               'dropped, '
                                                                               'or '
                                                                               'demoted '
                                                                               'to a '
                                                                               'dataset-level '
                                                                               'cohort '
                                                                               'handle? '
                                                                               'Feedback '
                                                                               'welcome.'},
                                                    'tier': {'tag': 'tier',
                                                             'value': 'core'}},
                                    'description': 'The patient or cohort the exposure '
                                                   'value is attached to. Carried as '
                                                   'an opaque identifier; PHI must not '
                                                   'appear here.',
                                    'name': 'subject',
                                    'range': 'string',
                                    'slot_group': 'exposure_description',
                                    'title': 'Subject (Patient or Cohort)'}},
         'title': 'Environmental Exposure Record',
         'tree_root': True})

    subject: str = Field(default=..., title="Subject (Patient or Cohort)", description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'open_question': {'tag': 'open_question',
                                           'value': '`subject` is the only field in '
                                                    'this group that is not a '
                                                    'per-value predicate: every other '
                                                    'field explains an individual '
                                                    'value, but a single scalar '
                                                    'subject is dataset-scoped and '
                                                    'cannot distribute over the '
                                                    "sidecar's rows (per-row subject "
                                                    'identity lives in '
                                                    '`subject_column`). Under review — '
                                                    'should it be dropped, or demoted '
                                                    'to a dataset-level cohort handle? '
                                                    'Feedback welcome.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition'],
         'slot_group': 'exposure_description'} })
    variable_identity: VariableIdentity = Field(default=..., title="Variable Identity", description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable). Readable rename of the profile's `observation_type` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['observation_type'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block pins down exactly what '
                                                  'was measured. Instead of relying on '
                                                  'a nickname like "tmax", it uses '
                                                  'shared vocabularies to say "daily '
                                                  'maximum air temperature, in degrees '
                                                  'Celsius", so any tool or researcher '
                                                  'reads it the same way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a standard variable '
                                                    'identity, "tmax" in one file and '
                                                    '"TMAX" in another cannot be '
                                                    'recognised as the same physical '
                                                    'quantity, and unit mix-ups '
                                                    '(Celsius vs Fahrenheit vs Kelvin) '
                                                    'go undetected — pooling and '
                                                    'cross-study comparison silently '
                                                    'break.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:observation_type'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cf_cell_methods': 'time: maximum',
                                  'standard_name': 'CF:air_temperature',
                                  'units_ucum': 'Cel',
                                  'variable_name': 'tmax'}}],
         'implements': ['msprofile:observation_type'],
         'see_also': ['https://cfconventions.org/', 'https://ucum.org/'],
         'slot_group': 'exposure_description'} })
    spatial_reference: SpatialReference = Field(default=..., title="Spatial Reference", description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial). Readable rename of the profile's `location` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['location'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block says where the number '
                                                  'applies and how it was pulled out '
                                                  'of a map. Environmental data '
                                                  'usually comes as a grid of cells '
                                                  'covering a region; this records how '
                                                  'big those cells are and how the '
                                                  'value for a specific place was '
                                                  'picked from them.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A value without its grid, '
                                                    'coordinate system, and extraction '
                                                    'method cannot be located or '
                                                    'compared: a 1 km neighbourhood '
                                                    'average and a ~31 km regional '
                                                    'average look identical as numbers '
                                                    'but describe very different '
                                                    'exposures, and the extraction '
                                                    'cannot be re-run without the '
                                                    'method.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:location'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'crs': 'EPSG:4326',
                                  'extraction_method': 'inverse_distance_weighted_4_nearest_cells',
                                  'native_spatial_resolution_m': 1000,
                                  'target_geography_type': 'point_residence'}}],
         'implements': ['msprofile:location'],
         'see_also': ['https://epsg.io/'],
         'slot_group': 'exposure_description'} })
    temporal_reference: TemporalReference = Field(default=..., title="Temporal Reference", description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal). Readable rename of the profile's `temporality` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['temporality'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block explains the time ruler '
                                                  'behind each value: how long a '
                                                  'period each number summarises (a '
                                                  'day, a month), how it was '
                                                  'summarised (maximum, mean), and — '
                                                  'surprisingly important — when a '
                                                  '"day" is considered to start and '
                                                  'end.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A "daily maximum" is ambiguous '
                                                    'without the day-boundary '
                                                    'convention: Daymet days end at '
                                                    'local midnight while PRISM days '
                                                    'end at 12:00 GMT, so the same '
                                                    'calendar date can cover different '
                                                    'physical hours — the most-omitted '
                                                    'detail in the heat literature and '
                                                    'a known source of cross-product '
                                                    'disagreement.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:temporality'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'calendar': 'gregorian',
                                  'day_boundary_convention': 'local_midnight',
                                  'temporal_aggregation_method': 'maximum',
                                  'temporal_resolution': 'daily'}}],
         'implements': ['msprofile:temporality'],
         'see_also': ['https://cfconventions.org/'],
         'slot_group': 'exposure_description'} })
    exposure_model: ExposureModel = Field(default=..., title="Exposure Model", description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Readable rename of the profile's `methodology` anatomy slot, narrowed to the model itself: other methodology-adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots.""", json_schema_extra = { "linkml_meta": {'aliases': ['methodology'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most exposure values are not direct '
                                                  'readings from an instrument at '
                                                  "someone's house — they are "
                                                  'estimates computed from weather '
                                                  'stations, satellites, or models. '
                                                  'This block says which estimation '
                                                  'method produced the numbers and '
                                                  'what went into it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The same quantity can be '
                                                    'estimated by station '
                                                    'interpolation, satellite '
                                                    'retrieval, or model reanalysis, '
                                                    'each with different inputs and '
                                                    'biases; without the model '
                                                    'description, values from '
                                                    'different products get pooled as '
                                                    'if equivalent and their '
                                                    'systematic differences stay '
                                                    'invisible.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:methodology'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'bias_correction_applied': 'none',
                                  'exposure_model_inputs': ['GHCN-Daily station '
                                                            'observations'],
                                  'exposure_model_paper_doi': '10.3334/ORNLDAAC/2129',
                                  'exposure_model_type': 'spatial_interpolation'}}],
         'implements': ['msprofile:methodology'],
         'slot_group': 'exposure_description'} })
    uncertainty: Optional[Uncertainty] = Field(default=None, title="Uncertainty", description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'No estimate is perfect. This block '
                                                  'says how far off the numbers might '
                                                  'be and what was done about gaps in '
                                                  'the data, so users know how much '
                                                  'confidence to place in each value.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Exposure values are model '
                                                    'estimates with error; without '
                                                    'recorded per-value or aggregate '
                                                    'uncertainty and missing-data '
                                                    'handling, downstream analyses '
                                                    'treat estimates as exact, and '
                                                    'exposure-measurement error '
                                                    'propagates invisibly into '
                                                    'health-effect estimates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'data_completeness_pct': 100,
                                  'missing_data_handling_method': 'spatiotemporal_interpolation',
                                  'per_value_uncertainty_type': 'standard_error',
                                  'per_value_uncertainty_units_ucum': 'Cel'}}],
         'slot_group': 'exposure_description'} })
    derived_heat_metric: Optional[DerivedHeatMetric] = Field(default=None, title="Derived Heat Metric", description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some heat measures are not read '
                                                  'from a thermometer but calculated '
                                                  'from several ingredients '
                                                  '(temperature, humidity, wind, '
                                                  'sunshine) using a chosen formula. '
                                                  'This block records which formula '
                                                  'and ingredients were used — it is '
                                                  'only needed when the variable is '
                                                  'one of these computed heat '
                                                  'metrics.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Heat metrics like WBGT or Heat '
                                                    'Index can be computed by several '
                                                    'non-equivalent equations from '
                                                    'different inputs, and heat-wave '
                                                    'flags depend on the threshold '
                                                    'definition; the heat-epidemiology '
                                                    'literature flags these choices as '
                                                    'the main sources of cross-study '
                                                    'disagreement, so omitting the '
                                                    'block for a heat metric makes the '
                                                    'record uncomparable.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'illustrative outdoor-WBGT methodology block — '
                                      'not part of the tmax scenario, where this slot '
                                      'is omitted',
                       'object': {'equation_variant': 'liljegren_2008',
                                  'heat_metric_family': 'wbgt_outdoor',
                                  'indoor_outdoor': 'outdoor',
                                  'solar_radiation_basis': 'surface_downwelling_shortwave_flux'}}],
         'slot_group': 'variable_specific_extensions'} })
    data_layout: DataLayout = Field(default=..., title="Data Layout", description="""Data-layout object binding this sidecar to the columns of the companion data file — see envar_layout. Required: without it a consumer cannot locate the values the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The actual numbers live in a '
                                                  'separate data table that travels '
                                                  'with this record. This block is the '
                                                  'map between the two: it names which '
                                                  'column holds the values, which '
                                                  'holds the person identifier, which '
                                                  'holds the date, and so on.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The sidecar describes values that '
                                                    'live in a companion CSV/parquet '
                                                    'file; without the column bindings '
                                                    'a consumer cannot tell which '
                                                    'column holds the values, '
                                                    'subjects, or dates, so the '
                                                    'metadata is unanchored and the '
                                                    'data unusable — hence the slot is '
                                                    'required.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'subject_column': 'subject_id',
                                  'table_orientation': 'wide',
                                  'time_column': 'date',
                                  'value_column': 'tmax'}}],
         'slot_group': 'dataset_and_provenance'} })
    source_dataset: SourceDataset = Field(default=..., title="Source Dataset", description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Exposure values are derived from a '
                                                  'published data product (for example '
                                                  'Daymet, a daily weather dataset). '
                                                  'This block names that product '
                                                  'precisely — including its version, '
                                                  'citation, and license — so anyone '
                                                  'can find it and check its '
                                                  'documentation.'},
                         'justification': {'tag': 'justification',
                                           'value': "Without the upstream product's "
                                                    'identity, version, DOI, and '
                                                    'license, the record cannot be '
                                                    'cited, its documented biases '
                                                    'cannot be looked up, and reuse '
                                                    'terms are unknown — and two '
                                                    'records built from different '
                                                    'product versions cannot be told '
                                                    'apart.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'source_dataset_doi': '10.3334/ORNLDAAC/2129',
                                  'source_dataset_name': 'Daymet V4 Daily Surface '
                                                         'Weather Data',
                                  'source_dataset_short_code': 'daymet_v4',
                                  'source_license_spdx': 'public-domain-us-gov'}}],
         'see_also': ['https://spdx.org/licenses/', 'https://www.doi.org/'],
         'slot_group': 'dataset_and_provenance'} })
    tool_run: ToolRun = Field(default=..., title="Tool Run", description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block is the receipt for the '
                                                  'software step that produced the '
                                                  'values: which program ran, which '
                                                  'exact version, with what settings, '
                                                  'and when. With it, someone else can '
                                                  're-run the same step and get the '
                                                  'same numbers.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the exact tool name, '
                                                    'version, container image, '
                                                    'parameters, and timestamp, the '
                                                    'record cannot be re-run: "we used '
                                                    'the daymet tool" is not '
                                                    'reproducible, but a pinned '
                                                    'container invocation is.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'container_image_repository': 'ghcr.io/degauss-org/daymet',
                                  'run_timestamp_utc': '2026-05-23T14:18:42Z',
                                  'tool_name': 'daymet',
                                  'tool_version': '1.0.0'}}],
         'slot_group': 'dataset_and_provenance'} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, title="Provenance Chain", description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Data usually passes through several '
                                                  'tools before the final value '
                                                  'appears — download, geocode, '
                                                  'extract. This block lists those '
                                                  'earlier steps in order, like a '
                                                  'chain of custody reaching back to '
                                                  'the original raw source.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The final tool run is rarely the '
                                                    'whole story — downloads, '
                                                    'geocoding, and intermediate '
                                                    'transforms precede it; without '
                                                    'the ordered chain back to the raw '
                                                    'source, end-to-end reproduction '
                                                    'and error tracing are impossible '
                                                    'even when the last step is '
                                                    'pinned.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'provenance_chain_steps': [{'run_timestamp_utc': '2026-05-23T14:02:11Z',
                                                              'tool_name': 'geocoder',
                                                              'tool_version': '3.3.0'}],
                                  'provenance_chain_terminus_type': 'raw_source_download'}}],
         'see_also': ['https://www.w3.org/TR/prov-o/'],
         'slot_group': 'dataset_and_provenance'} })
    linkage_method: LinkageMethod = Field(default=..., title="Linkage Method", description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Environmental data describes '
                                                  'places, but health research is '
                                                  'about people. This block records '
                                                  'how the value for a place was '
                                                  'attached to a particular person — '
                                                  'for example, by looking up the map '
                                                  'cell containing their home address '
                                                  '— since that step involves real '
                                                  'choices that affect the result.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Attaching a place-based value to '
                                                    'a person is a lossy, choice-laden '
                                                    'step (geocoding, point vs buffer '
                                                    'extraction, date alignment) — the '
                                                    '"linkage descriptor" gap the '
                                                    'GECC/EIRENE forum names as '
                                                    'central. Without it, two studies '
                                                    'using the same data product can '
                                                    'differ solely through '
                                                    'undocumented joins.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'address_period_alignment': 'address_history_from_emr',
                                  'clinical_date_assignment_convention': 'local_midnight',
                                  'lag_alignment_applied': 'none',
                                  'linkage_strategy': 'point_extraction_at_residence'}}],
         'slot_group': 'health_data_integration'} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, title="Health-Layer Linkage", description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health studies keep patient data in '
                                                  'large standard databases. This '
                                                  'block notes which of those systems '
                                                  'the exposure values were wired into '
                                                  'and through which field, so someone '
                                                  'browsing the health data can find '
                                                  'their way back to this record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Naming the downstream health-data '
                                                    'layer (OMOP, BDC, …) and the join '
                                                    'field makes the exposure record '
                                                    'findable from the clinical side; '
                                                    'without it the sidecar and the '
                                                    'health records it serves drift '
                                                    'apart, and the link must be '
                                                    'reconstructed by hand.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cohort_size_anchored': 3,
                                  'health_layer_link_field': 'exposure_source_value',
                                  'health_layer_target': 'omop_external_exposure'}}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/',
                      'https://biodatacatalyst.nhlbi.nih.gov/'],
         'slot_group': 'health_data_integration'} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, title="FAIR Deposit Metadata", description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If this record and its data are '
                                                  'published in a public archive (such '
                                                  'as Zenodo), this block holds the '
                                                  'publication details: the permanent '
                                                  'DOI link, where it lives, and the '
                                                  'license saying how others may use '
                                                  'it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'When the sidecar travels with a '
                                                    'published deposit, the DOI, '
                                                    'repository, and license are what '
                                                    'make the object findable, '
                                                    'citable, and legally reusable — '
                                                    'omitting them strands a public '
                                                    'artifact without citation or '
                                                    'reuse terms. Optional because '
                                                    'most records are never '
                                                    'deposited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'deposit_doi': '10.5281/zenodo.9999999',
                                  'deposit_license_spdx': 'CC-BY-4.0',
                                  'deposit_repository': 'zenodo'}}],
         'see_also': ['https://www.go-fair.org/fair-principles/'],
         'slot_group': 'health_data_integration'} })
    schema_version: str = Field(default=..., title="Schema Version", description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Schemas change over time, like '
                                                  'editions of a paper form. This is '
                                                  'the edition number stamped on the '
                                                  'document, so anyone reading it '
                                                  'knows exactly which version of the '
                                                  'form was filled in and can '
                                                  'interpret the fields accordingly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Downstream consumers must branch '
                                                    'on schema evolution: a parser '
                                                    'built for one version will '
                                                    'silently misread or wrongly '
                                                    'reject sidecars written against '
                                                    'another. Without this slot there '
                                                    'is no way to tell which iteration '
                                                    'of the schema a document '
                                                    'targets.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': '0.1'}],
         'see_also': ['https://semver.org/'],
         'slot_group': 'record_bookkeeping'} })
    provenance_id: str = Field(default=..., title="Record Identifier", description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A unique serial number for this '
                                                  'metadata document, like the '
                                                  'tracking number on a parcel. '
                                                  'Wherever the data value ends up, '
                                                  'that number lets you look up '
                                                  'exactly where it came from and how '
                                                  'it was made.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This identifier is what the '
                                                    "downstream health-data layer's "
                                                    'source-value field carries (for '
                                                    'OMOP, '
                                                    '`external_exposure.exposure_source_value`); '
                                                    'it is the only hook that links an '
                                                    'exposure value in the health '
                                                    'layer back to its full spatial, '
                                                    'temporal, and model provenance. '
                                                    'Omit it and the value becomes '
                                                    'untraceable — its metadata can '
                                                    'never be recovered.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'ULID-based sidecar identifier for the Daymet '
                                      'Tmax deposit',
                       'value': '01HFA7K8R3M6XP-daymet-deposit'}],
         'see_also': ['https://github.com/ulid/spec',
                      'https://ohdsi.github.io/CommonDataModel/'],
         'slot_group': 'record_bookkeeping'} })
    phi_status: PhiStatusEnum = Field(default=..., title="PHI Status", description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'PHI (protected health information) '
                                                  'means private medical details about '
                                                  'an identifiable person. This flag '
                                                  'is a written promise on the '
                                                  'document saying "no private patient '
                                                  'information inside", so it can be '
                                                  'passed around and published '
                                                  'safely.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Sidecars are designed to be '
                                                    'PHI-free, and this slot is the '
                                                    'explicit machine-readable '
                                                    'assertion of that. Without it, '
                                                    'every sharing, deposit, or export '
                                                    'step must treat the document as '
                                                    'potentially containing patient '
                                                    'data and re-review it manually '
                                                    'before it can leave a protected '
                                                    'environment.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': 'no_phi'}],
         'see_also': ['https://www.hhs.gov/hipaa/for-professionals/privacy/index.html'],
         'slot_group': 'record_bookkeeping'} })


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
    observation_type: str = Field(default=..., description="""Question being asked, measurement being taken, quality being observed""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })
    location: str = Field(default=..., description="""Spatial metadata specifying where the observation was made - geolocation, place name, site id, environment, or biome""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })
    temporality: str = Field(default=..., description="""Temporal metadata specifying when an observation was made. This can be relative or absolute - datetime, age of person, season, or geologic era""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })
    methodology: str = Field(default=..., description="""Information about how an observation was made - method, instrument, reagent kit, statistical modifier""", json_schema_extra = { "linkml_meta": {'domain_of': ['MicroschemaDefinition']} })
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
                    'postconditions': {'slot_conditions': {'variable_identity': {'any_of': [{'range': 'VariableIdentity'}],
                                                                                 'name': 'variable_identity'}}}}],
         'see_also': ['https://cfconventions.org/standard-names.html',
                      'https://ucum.org/'],
         'title': 'Daily Maximum Temperature Record'})

    subject: str = Field(default=..., title="Subject (Patient or Cohort)", description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'open_question': {'tag': 'open_question',
                                           'value': '`subject` is the only field in '
                                                    'this group that is not a '
                                                    'per-value predicate: every other '
                                                    'field explains an individual '
                                                    'value, but a single scalar '
                                                    'subject is dataset-scoped and '
                                                    'cannot distribute over the '
                                                    "sidecar's rows (per-row subject "
                                                    'identity lives in '
                                                    '`subject_column`). Under review — '
                                                    'should it be dropped, or demoted '
                                                    'to a dataset-level cohort handle? '
                                                    'Feedback welcome.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition'],
         'slot_group': 'exposure_description'} })
    variable_identity: VariableIdentity = Field(default=..., title="Variable Identity", description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable). Readable rename of the profile's `observation_type` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['observation_type'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block pins down exactly what '
                                                  'was measured. Instead of relying on '
                                                  'a nickname like "tmax", it uses '
                                                  'shared vocabularies to say "daily '
                                                  'maximum air temperature, in degrees '
                                                  'Celsius", so any tool or researcher '
                                                  'reads it the same way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a standard variable '
                                                    'identity, "tmax" in one file and '
                                                    '"TMAX" in another cannot be '
                                                    'recognised as the same physical '
                                                    'quantity, and unit mix-ups '
                                                    '(Celsius vs Fahrenheit vs Kelvin) '
                                                    'go undetected — pooling and '
                                                    'cross-study comparison silently '
                                                    'break.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:observation_type'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cf_cell_methods': 'time: maximum',
                                  'standard_name': 'CF:air_temperature',
                                  'units_ucum': 'Cel',
                                  'variable_name': 'tmax'}}],
         'implements': ['msprofile:observation_type'],
         'see_also': ['https://cfconventions.org/', 'https://ucum.org/'],
         'slot_group': 'exposure_description'} })
    spatial_reference: SpatialReference = Field(default=..., title="Spatial Reference", description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial). Readable rename of the profile's `location` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['location'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block says where the number '
                                                  'applies and how it was pulled out '
                                                  'of a map. Environmental data '
                                                  'usually comes as a grid of cells '
                                                  'covering a region; this records how '
                                                  'big those cells are and how the '
                                                  'value for a specific place was '
                                                  'picked from them.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A value without its grid, '
                                                    'coordinate system, and extraction '
                                                    'method cannot be located or '
                                                    'compared: a 1 km neighbourhood '
                                                    'average and a ~31 km regional '
                                                    'average look identical as numbers '
                                                    'but describe very different '
                                                    'exposures, and the extraction '
                                                    'cannot be re-run without the '
                                                    'method.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:location'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'crs': 'EPSG:4326',
                                  'extraction_method': 'inverse_distance_weighted_4_nearest_cells',
                                  'native_spatial_resolution_m': 1000,
                                  'target_geography_type': 'point_residence'}}],
         'implements': ['msprofile:location'],
         'see_also': ['https://epsg.io/'],
         'slot_group': 'exposure_description'} })
    temporal_reference: TemporalReference = Field(default=..., title="Temporal Reference", description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal). Readable rename of the profile's `temporality` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['temporality'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block explains the time ruler '
                                                  'behind each value: how long a '
                                                  'period each number summarises (a '
                                                  'day, a month), how it was '
                                                  'summarised (maximum, mean), and — '
                                                  'surprisingly important — when a '
                                                  '"day" is considered to start and '
                                                  'end.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A "daily maximum" is ambiguous '
                                                    'without the day-boundary '
                                                    'convention: Daymet days end at '
                                                    'local midnight while PRISM days '
                                                    'end at 12:00 GMT, so the same '
                                                    'calendar date can cover different '
                                                    'physical hours — the most-omitted '
                                                    'detail in the heat literature and '
                                                    'a known source of cross-product '
                                                    'disagreement.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:temporality'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'calendar': 'gregorian',
                                  'day_boundary_convention': 'local_midnight',
                                  'temporal_aggregation_method': 'maximum',
                                  'temporal_resolution': 'daily'}}],
         'implements': ['msprofile:temporality'],
         'see_also': ['https://cfconventions.org/'],
         'slot_group': 'exposure_description'} })
    exposure_model: ExposureModel = Field(default=..., title="Exposure Model", description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Readable rename of the profile's `methodology` anatomy slot, narrowed to the model itself: other methodology-adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots.""", json_schema_extra = { "linkml_meta": {'aliases': ['methodology'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most exposure values are not direct '
                                                  'readings from an instrument at '
                                                  "someone's house — they are "
                                                  'estimates computed from weather '
                                                  'stations, satellites, or models. '
                                                  'This block says which estimation '
                                                  'method produced the numbers and '
                                                  'what went into it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The same quantity can be '
                                                    'estimated by station '
                                                    'interpolation, satellite '
                                                    'retrieval, or model reanalysis, '
                                                    'each with different inputs and '
                                                    'biases; without the model '
                                                    'description, values from '
                                                    'different products get pooled as '
                                                    'if equivalent and their '
                                                    'systematic differences stay '
                                                    'invisible.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:methodology'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'bias_correction_applied': 'none',
                                  'exposure_model_inputs': ['GHCN-Daily station '
                                                            'observations'],
                                  'exposure_model_paper_doi': '10.3334/ORNLDAAC/2129',
                                  'exposure_model_type': 'spatial_interpolation'}}],
         'implements': ['msprofile:methodology'],
         'slot_group': 'exposure_description'} })
    uncertainty: Optional[Uncertainty] = Field(default=None, title="Uncertainty", description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'No estimate is perfect. This block '
                                                  'says how far off the numbers might '
                                                  'be and what was done about gaps in '
                                                  'the data, so users know how much '
                                                  'confidence to place in each value.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Exposure values are model '
                                                    'estimates with error; without '
                                                    'recorded per-value or aggregate '
                                                    'uncertainty and missing-data '
                                                    'handling, downstream analyses '
                                                    'treat estimates as exact, and '
                                                    'exposure-measurement error '
                                                    'propagates invisibly into '
                                                    'health-effect estimates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'data_completeness_pct': 100,
                                  'missing_data_handling_method': 'spatiotemporal_interpolation',
                                  'per_value_uncertainty_type': 'standard_error',
                                  'per_value_uncertainty_units_ucum': 'Cel'}}],
         'slot_group': 'exposure_description'} })
    derived_heat_metric: Optional[DerivedHeatMetric] = Field(default=None, title="Derived Heat Metric", description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some heat measures are not read '
                                                  'from a thermometer but calculated '
                                                  'from several ingredients '
                                                  '(temperature, humidity, wind, '
                                                  'sunshine) using a chosen formula. '
                                                  'This block records which formula '
                                                  'and ingredients were used — it is '
                                                  'only needed when the variable is '
                                                  'one of these computed heat '
                                                  'metrics.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Heat metrics like WBGT or Heat '
                                                    'Index can be computed by several '
                                                    'non-equivalent equations from '
                                                    'different inputs, and heat-wave '
                                                    'flags depend on the threshold '
                                                    'definition; the heat-epidemiology '
                                                    'literature flags these choices as '
                                                    'the main sources of cross-study '
                                                    'disagreement, so omitting the '
                                                    'block for a heat metric makes the '
                                                    'record uncomparable.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'illustrative outdoor-WBGT methodology block — '
                                      'not part of the tmax scenario, where this slot '
                                      'is omitted',
                       'object': {'equation_variant': 'liljegren_2008',
                                  'heat_metric_family': 'wbgt_outdoor',
                                  'indoor_outdoor': 'outdoor',
                                  'solar_radiation_basis': 'surface_downwelling_shortwave_flux'}}],
         'slot_group': 'variable_specific_extensions'} })
    data_layout: DataLayout = Field(default=..., title="Data Layout", description="""Data-layout object binding this sidecar to the columns of the companion data file — see envar_layout. Required: without it a consumer cannot locate the values the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The actual numbers live in a '
                                                  'separate data table that travels '
                                                  'with this record. This block is the '
                                                  'map between the two: it names which '
                                                  'column holds the values, which '
                                                  'holds the person identifier, which '
                                                  'holds the date, and so on.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The sidecar describes values that '
                                                    'live in a companion CSV/parquet '
                                                    'file; without the column bindings '
                                                    'a consumer cannot tell which '
                                                    'column holds the values, '
                                                    'subjects, or dates, so the '
                                                    'metadata is unanchored and the '
                                                    'data unusable — hence the slot is '
                                                    'required.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'subject_column': 'subject_id',
                                  'table_orientation': 'wide',
                                  'time_column': 'date',
                                  'value_column': 'tmax'}}],
         'slot_group': 'dataset_and_provenance'} })
    source_dataset: SourceDataset = Field(default=..., title="Source Dataset", description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Exposure values are derived from a '
                                                  'published data product (for example '
                                                  'Daymet, a daily weather dataset). '
                                                  'This block names that product '
                                                  'precisely — including its version, '
                                                  'citation, and license — so anyone '
                                                  'can find it and check its '
                                                  'documentation.'},
                         'justification': {'tag': 'justification',
                                           'value': "Without the upstream product's "
                                                    'identity, version, DOI, and '
                                                    'license, the record cannot be '
                                                    'cited, its documented biases '
                                                    'cannot be looked up, and reuse '
                                                    'terms are unknown — and two '
                                                    'records built from different '
                                                    'product versions cannot be told '
                                                    'apart.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'source_dataset_doi': '10.3334/ORNLDAAC/2129',
                                  'source_dataset_name': 'Daymet V4 Daily Surface '
                                                         'Weather Data',
                                  'source_dataset_short_code': 'daymet_v4',
                                  'source_license_spdx': 'public-domain-us-gov'}}],
         'see_also': ['https://spdx.org/licenses/', 'https://www.doi.org/'],
         'slot_group': 'dataset_and_provenance'} })
    tool_run: ToolRun = Field(default=..., title="Tool Run", description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block is the receipt for the '
                                                  'software step that produced the '
                                                  'values: which program ran, which '
                                                  'exact version, with what settings, '
                                                  'and when. With it, someone else can '
                                                  're-run the same step and get the '
                                                  'same numbers.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the exact tool name, '
                                                    'version, container image, '
                                                    'parameters, and timestamp, the '
                                                    'record cannot be re-run: "we used '
                                                    'the daymet tool" is not '
                                                    'reproducible, but a pinned '
                                                    'container invocation is.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'container_image_repository': 'ghcr.io/degauss-org/daymet',
                                  'run_timestamp_utc': '2026-05-23T14:18:42Z',
                                  'tool_name': 'daymet',
                                  'tool_version': '1.0.0'}}],
         'slot_group': 'dataset_and_provenance'} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, title="Provenance Chain", description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Data usually passes through several '
                                                  'tools before the final value '
                                                  'appears — download, geocode, '
                                                  'extract. This block lists those '
                                                  'earlier steps in order, like a '
                                                  'chain of custody reaching back to '
                                                  'the original raw source.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The final tool run is rarely the '
                                                    'whole story — downloads, '
                                                    'geocoding, and intermediate '
                                                    'transforms precede it; without '
                                                    'the ordered chain back to the raw '
                                                    'source, end-to-end reproduction '
                                                    'and error tracing are impossible '
                                                    'even when the last step is '
                                                    'pinned.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'provenance_chain_steps': [{'run_timestamp_utc': '2026-05-23T14:02:11Z',
                                                              'tool_name': 'geocoder',
                                                              'tool_version': '3.3.0'}],
                                  'provenance_chain_terminus_type': 'raw_source_download'}}],
         'see_also': ['https://www.w3.org/TR/prov-o/'],
         'slot_group': 'dataset_and_provenance'} })
    linkage_method: LinkageMethod = Field(default=..., title="Linkage Method", description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Environmental data describes '
                                                  'places, but health research is '
                                                  'about people. This block records '
                                                  'how the value for a place was '
                                                  'attached to a particular person — '
                                                  'for example, by looking up the map '
                                                  'cell containing their home address '
                                                  '— since that step involves real '
                                                  'choices that affect the result.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Attaching a place-based value to '
                                                    'a person is a lossy, choice-laden '
                                                    'step (geocoding, point vs buffer '
                                                    'extraction, date alignment) — the '
                                                    '"linkage descriptor" gap the '
                                                    'GECC/EIRENE forum names as '
                                                    'central. Without it, two studies '
                                                    'using the same data product can '
                                                    'differ solely through '
                                                    'undocumented joins.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'address_period_alignment': 'address_history_from_emr',
                                  'clinical_date_assignment_convention': 'local_midnight',
                                  'lag_alignment_applied': 'none',
                                  'linkage_strategy': 'point_extraction_at_residence'}}],
         'slot_group': 'health_data_integration'} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, title="Health-Layer Linkage", description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health studies keep patient data in '
                                                  'large standard databases. This '
                                                  'block notes which of those systems '
                                                  'the exposure values were wired into '
                                                  'and through which field, so someone '
                                                  'browsing the health data can find '
                                                  'their way back to this record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Naming the downstream health-data '
                                                    'layer (OMOP, BDC, …) and the join '
                                                    'field makes the exposure record '
                                                    'findable from the clinical side; '
                                                    'without it the sidecar and the '
                                                    'health records it serves drift '
                                                    'apart, and the link must be '
                                                    'reconstructed by hand.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cohort_size_anchored': 3,
                                  'health_layer_link_field': 'exposure_source_value',
                                  'health_layer_target': 'omop_external_exposure'}}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/',
                      'https://biodatacatalyst.nhlbi.nih.gov/'],
         'slot_group': 'health_data_integration'} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, title="FAIR Deposit Metadata", description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If this record and its data are '
                                                  'published in a public archive (such '
                                                  'as Zenodo), this block holds the '
                                                  'publication details: the permanent '
                                                  'DOI link, where it lives, and the '
                                                  'license saying how others may use '
                                                  'it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'When the sidecar travels with a '
                                                    'published deposit, the DOI, '
                                                    'repository, and license are what '
                                                    'make the object findable, '
                                                    'citable, and legally reusable — '
                                                    'omitting them strands a public '
                                                    'artifact without citation or '
                                                    'reuse terms. Optional because '
                                                    'most records are never '
                                                    'deposited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'deposit_doi': '10.5281/zenodo.9999999',
                                  'deposit_license_spdx': 'CC-BY-4.0',
                                  'deposit_repository': 'zenodo'}}],
         'see_also': ['https://www.go-fair.org/fair-principles/'],
         'slot_group': 'health_data_integration'} })
    schema_version: str = Field(default=..., title="Schema Version", description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Schemas change over time, like '
                                                  'editions of a paper form. This is '
                                                  'the edition number stamped on the '
                                                  'document, so anyone reading it '
                                                  'knows exactly which version of the '
                                                  'form was filled in and can '
                                                  'interpret the fields accordingly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Downstream consumers must branch '
                                                    'on schema evolution: a parser '
                                                    'built for one version will '
                                                    'silently misread or wrongly '
                                                    'reject sidecars written against '
                                                    'another. Without this slot there '
                                                    'is no way to tell which iteration '
                                                    'of the schema a document '
                                                    'targets.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': '0.1'}],
         'see_also': ['https://semver.org/'],
         'slot_group': 'record_bookkeeping'} })
    provenance_id: str = Field(default=..., title="Record Identifier", description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A unique serial number for this '
                                                  'metadata document, like the '
                                                  'tracking number on a parcel. '
                                                  'Wherever the data value ends up, '
                                                  'that number lets you look up '
                                                  'exactly where it came from and how '
                                                  'it was made.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This identifier is what the '
                                                    "downstream health-data layer's "
                                                    'source-value field carries (for '
                                                    'OMOP, '
                                                    '`external_exposure.exposure_source_value`); '
                                                    'it is the only hook that links an '
                                                    'exposure value in the health '
                                                    'layer back to its full spatial, '
                                                    'temporal, and model provenance. '
                                                    'Omit it and the value becomes '
                                                    'untraceable — its metadata can '
                                                    'never be recovered.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'ULID-based sidecar identifier for the Daymet '
                                      'Tmax deposit',
                       'value': '01HFA7K8R3M6XP-daymet-deposit'}],
         'see_also': ['https://github.com/ulid/spec',
                      'https://ohdsi.github.io/CommonDataModel/'],
         'slot_group': 'record_bookkeeping'} })
    phi_status: PhiStatusEnum = Field(default=..., title="PHI Status", description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'PHI (protected health information) '
                                                  'means private medical details about '
                                                  'an identifiable person. This flag '
                                                  'is a written promise on the '
                                                  'document saying "no private patient '
                                                  'information inside", so it can be '
                                                  'passed around and published '
                                                  'safely.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Sidecars are designed to be '
                                                    'PHI-free, and this slot is the '
                                                    'explicit machine-readable '
                                                    'assertion of that. Without it, '
                                                    'every sharing, deposit, or export '
                                                    'step must treat the document as '
                                                    'potentially containing patient '
                                                    'data and re-review it manually '
                                                    'before it can leave a protected '
                                                    'environment.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': 'no_phi'}],
         'see_also': ['https://www.hhs.gov/hipaa/for-professionals/privacy/index.html'],
         'slot_group': 'record_bookkeeping'} })


class DailyMinTemperatureRecord(EnvironmentalExposureRecord):
    """
    Canonical record for daily minimum 2 m air temperature (Tmin). Pins `standard_name = CF:air_temperature`, `cf_cell_methods = \"time: minimum\"`, `units_ucum = Cel`, `value_data_type = continuous_numeric`.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/linkml/microschemas/envar/examples',
         'see_also': ['https://cfconventions.org/standard-names.html',
                      'https://ucum.org/'],
         'title': 'Daily Minimum Temperature Record'})

    subject: str = Field(default=..., title="Subject (Patient or Cohort)", description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'open_question': {'tag': 'open_question',
                                           'value': '`subject` is the only field in '
                                                    'this group that is not a '
                                                    'per-value predicate: every other '
                                                    'field explains an individual '
                                                    'value, but a single scalar '
                                                    'subject is dataset-scoped and '
                                                    'cannot distribute over the '
                                                    "sidecar's rows (per-row subject "
                                                    'identity lives in '
                                                    '`subject_column`). Under review — '
                                                    'should it be dropped, or demoted '
                                                    'to a dataset-level cohort handle? '
                                                    'Feedback welcome.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition'],
         'slot_group': 'exposure_description'} })
    variable_identity: VariableIdentity = Field(default=..., title="Variable Identity", description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable). Readable rename of the profile's `observation_type` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['observation_type'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block pins down exactly what '
                                                  'was measured. Instead of relying on '
                                                  'a nickname like "tmax", it uses '
                                                  'shared vocabularies to say "daily '
                                                  'maximum air temperature, in degrees '
                                                  'Celsius", so any tool or researcher '
                                                  'reads it the same way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a standard variable '
                                                    'identity, "tmax" in one file and '
                                                    '"TMAX" in another cannot be '
                                                    'recognised as the same physical '
                                                    'quantity, and unit mix-ups '
                                                    '(Celsius vs Fahrenheit vs Kelvin) '
                                                    'go undetected — pooling and '
                                                    'cross-study comparison silently '
                                                    'break.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:observation_type'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cf_cell_methods': 'time: maximum',
                                  'standard_name': 'CF:air_temperature',
                                  'units_ucum': 'Cel',
                                  'variable_name': 'tmax'}}],
         'implements': ['msprofile:observation_type'],
         'see_also': ['https://cfconventions.org/', 'https://ucum.org/'],
         'slot_group': 'exposure_description'} })
    spatial_reference: SpatialReference = Field(default=..., title="Spatial Reference", description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial). Readable rename of the profile's `location` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['location'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block says where the number '
                                                  'applies and how it was pulled out '
                                                  'of a map. Environmental data '
                                                  'usually comes as a grid of cells '
                                                  'covering a region; this records how '
                                                  'big those cells are and how the '
                                                  'value for a specific place was '
                                                  'picked from them.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A value without its grid, '
                                                    'coordinate system, and extraction '
                                                    'method cannot be located or '
                                                    'compared: a 1 km neighbourhood '
                                                    'average and a ~31 km regional '
                                                    'average look identical as numbers '
                                                    'but describe very different '
                                                    'exposures, and the extraction '
                                                    'cannot be re-run without the '
                                                    'method.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:location'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'crs': 'EPSG:4326',
                                  'extraction_method': 'inverse_distance_weighted_4_nearest_cells',
                                  'native_spatial_resolution_m': 1000,
                                  'target_geography_type': 'point_residence'}}],
         'implements': ['msprofile:location'],
         'see_also': ['https://epsg.io/'],
         'slot_group': 'exposure_description'} })
    temporal_reference: TemporalReference = Field(default=..., title="Temporal Reference", description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal). Readable rename of the profile's `temporality` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['temporality'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block explains the time ruler '
                                                  'behind each value: how long a '
                                                  'period each number summarises (a '
                                                  'day, a month), how it was '
                                                  'summarised (maximum, mean), and — '
                                                  'surprisingly important — when a '
                                                  '"day" is considered to start and '
                                                  'end.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A "daily maximum" is ambiguous '
                                                    'without the day-boundary '
                                                    'convention: Daymet days end at '
                                                    'local midnight while PRISM days '
                                                    'end at 12:00 GMT, so the same '
                                                    'calendar date can cover different '
                                                    'physical hours — the most-omitted '
                                                    'detail in the heat literature and '
                                                    'a known source of cross-product '
                                                    'disagreement.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:temporality'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'calendar': 'gregorian',
                                  'day_boundary_convention': 'local_midnight',
                                  'temporal_aggregation_method': 'maximum',
                                  'temporal_resolution': 'daily'}}],
         'implements': ['msprofile:temporality'],
         'see_also': ['https://cfconventions.org/'],
         'slot_group': 'exposure_description'} })
    exposure_model: ExposureModel = Field(default=..., title="Exposure Model", description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Readable rename of the profile's `methodology` anatomy slot, narrowed to the model itself: other methodology-adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots.""", json_schema_extra = { "linkml_meta": {'aliases': ['methodology'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most exposure values are not direct '
                                                  'readings from an instrument at '
                                                  "someone's house — they are "
                                                  'estimates computed from weather '
                                                  'stations, satellites, or models. '
                                                  'This block says which estimation '
                                                  'method produced the numbers and '
                                                  'what went into it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The same quantity can be '
                                                    'estimated by station '
                                                    'interpolation, satellite '
                                                    'retrieval, or model reanalysis, '
                                                    'each with different inputs and '
                                                    'biases; without the model '
                                                    'description, values from '
                                                    'different products get pooled as '
                                                    'if equivalent and their '
                                                    'systematic differences stay '
                                                    'invisible.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:methodology'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'bias_correction_applied': 'none',
                                  'exposure_model_inputs': ['GHCN-Daily station '
                                                            'observations'],
                                  'exposure_model_paper_doi': '10.3334/ORNLDAAC/2129',
                                  'exposure_model_type': 'spatial_interpolation'}}],
         'implements': ['msprofile:methodology'],
         'slot_group': 'exposure_description'} })
    uncertainty: Optional[Uncertainty] = Field(default=None, title="Uncertainty", description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'No estimate is perfect. This block '
                                                  'says how far off the numbers might '
                                                  'be and what was done about gaps in '
                                                  'the data, so users know how much '
                                                  'confidence to place in each value.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Exposure values are model '
                                                    'estimates with error; without '
                                                    'recorded per-value or aggregate '
                                                    'uncertainty and missing-data '
                                                    'handling, downstream analyses '
                                                    'treat estimates as exact, and '
                                                    'exposure-measurement error '
                                                    'propagates invisibly into '
                                                    'health-effect estimates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'data_completeness_pct': 100,
                                  'missing_data_handling_method': 'spatiotemporal_interpolation',
                                  'per_value_uncertainty_type': 'standard_error',
                                  'per_value_uncertainty_units_ucum': 'Cel'}}],
         'slot_group': 'exposure_description'} })
    derived_heat_metric: Optional[DerivedHeatMetric] = Field(default=None, title="Derived Heat Metric", description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some heat measures are not read '
                                                  'from a thermometer but calculated '
                                                  'from several ingredients '
                                                  '(temperature, humidity, wind, '
                                                  'sunshine) using a chosen formula. '
                                                  'This block records which formula '
                                                  'and ingredients were used — it is '
                                                  'only needed when the variable is '
                                                  'one of these computed heat '
                                                  'metrics.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Heat metrics like WBGT or Heat '
                                                    'Index can be computed by several '
                                                    'non-equivalent equations from '
                                                    'different inputs, and heat-wave '
                                                    'flags depend on the threshold '
                                                    'definition; the heat-epidemiology '
                                                    'literature flags these choices as '
                                                    'the main sources of cross-study '
                                                    'disagreement, so omitting the '
                                                    'block for a heat metric makes the '
                                                    'record uncomparable.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'illustrative outdoor-WBGT methodology block — '
                                      'not part of the tmax scenario, where this slot '
                                      'is omitted',
                       'object': {'equation_variant': 'liljegren_2008',
                                  'heat_metric_family': 'wbgt_outdoor',
                                  'indoor_outdoor': 'outdoor',
                                  'solar_radiation_basis': 'surface_downwelling_shortwave_flux'}}],
         'slot_group': 'variable_specific_extensions'} })
    data_layout: DataLayout = Field(default=..., title="Data Layout", description="""Data-layout object binding this sidecar to the columns of the companion data file — see envar_layout. Required: without it a consumer cannot locate the values the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The actual numbers live in a '
                                                  'separate data table that travels '
                                                  'with this record. This block is the '
                                                  'map between the two: it names which '
                                                  'column holds the values, which '
                                                  'holds the person identifier, which '
                                                  'holds the date, and so on.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The sidecar describes values that '
                                                    'live in a companion CSV/parquet '
                                                    'file; without the column bindings '
                                                    'a consumer cannot tell which '
                                                    'column holds the values, '
                                                    'subjects, or dates, so the '
                                                    'metadata is unanchored and the '
                                                    'data unusable — hence the slot is '
                                                    'required.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'subject_column': 'subject_id',
                                  'table_orientation': 'wide',
                                  'time_column': 'date',
                                  'value_column': 'tmax'}}],
         'slot_group': 'dataset_and_provenance'} })
    source_dataset: SourceDataset = Field(default=..., title="Source Dataset", description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Exposure values are derived from a '
                                                  'published data product (for example '
                                                  'Daymet, a daily weather dataset). '
                                                  'This block names that product '
                                                  'precisely — including its version, '
                                                  'citation, and license — so anyone '
                                                  'can find it and check its '
                                                  'documentation.'},
                         'justification': {'tag': 'justification',
                                           'value': "Without the upstream product's "
                                                    'identity, version, DOI, and '
                                                    'license, the record cannot be '
                                                    'cited, its documented biases '
                                                    'cannot be looked up, and reuse '
                                                    'terms are unknown — and two '
                                                    'records built from different '
                                                    'product versions cannot be told '
                                                    'apart.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'source_dataset_doi': '10.3334/ORNLDAAC/2129',
                                  'source_dataset_name': 'Daymet V4 Daily Surface '
                                                         'Weather Data',
                                  'source_dataset_short_code': 'daymet_v4',
                                  'source_license_spdx': 'public-domain-us-gov'}}],
         'see_also': ['https://spdx.org/licenses/', 'https://www.doi.org/'],
         'slot_group': 'dataset_and_provenance'} })
    tool_run: ToolRun = Field(default=..., title="Tool Run", description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block is the receipt for the '
                                                  'software step that produced the '
                                                  'values: which program ran, which '
                                                  'exact version, with what settings, '
                                                  'and when. With it, someone else can '
                                                  're-run the same step and get the '
                                                  'same numbers.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the exact tool name, '
                                                    'version, container image, '
                                                    'parameters, and timestamp, the '
                                                    'record cannot be re-run: "we used '
                                                    'the daymet tool" is not '
                                                    'reproducible, but a pinned '
                                                    'container invocation is.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'container_image_repository': 'ghcr.io/degauss-org/daymet',
                                  'run_timestamp_utc': '2026-05-23T14:18:42Z',
                                  'tool_name': 'daymet',
                                  'tool_version': '1.0.0'}}],
         'slot_group': 'dataset_and_provenance'} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, title="Provenance Chain", description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Data usually passes through several '
                                                  'tools before the final value '
                                                  'appears — download, geocode, '
                                                  'extract. This block lists those '
                                                  'earlier steps in order, like a '
                                                  'chain of custody reaching back to '
                                                  'the original raw source.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The final tool run is rarely the '
                                                    'whole story — downloads, '
                                                    'geocoding, and intermediate '
                                                    'transforms precede it; without '
                                                    'the ordered chain back to the raw '
                                                    'source, end-to-end reproduction '
                                                    'and error tracing are impossible '
                                                    'even when the last step is '
                                                    'pinned.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'provenance_chain_steps': [{'run_timestamp_utc': '2026-05-23T14:02:11Z',
                                                              'tool_name': 'geocoder',
                                                              'tool_version': '3.3.0'}],
                                  'provenance_chain_terminus_type': 'raw_source_download'}}],
         'see_also': ['https://www.w3.org/TR/prov-o/'],
         'slot_group': 'dataset_and_provenance'} })
    linkage_method: LinkageMethod = Field(default=..., title="Linkage Method", description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Environmental data describes '
                                                  'places, but health research is '
                                                  'about people. This block records '
                                                  'how the value for a place was '
                                                  'attached to a particular person — '
                                                  'for example, by looking up the map '
                                                  'cell containing their home address '
                                                  '— since that step involves real '
                                                  'choices that affect the result.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Attaching a place-based value to '
                                                    'a person is a lossy, choice-laden '
                                                    'step (geocoding, point vs buffer '
                                                    'extraction, date alignment) — the '
                                                    '"linkage descriptor" gap the '
                                                    'GECC/EIRENE forum names as '
                                                    'central. Without it, two studies '
                                                    'using the same data product can '
                                                    'differ solely through '
                                                    'undocumented joins.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'address_period_alignment': 'address_history_from_emr',
                                  'clinical_date_assignment_convention': 'local_midnight',
                                  'lag_alignment_applied': 'none',
                                  'linkage_strategy': 'point_extraction_at_residence'}}],
         'slot_group': 'health_data_integration'} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, title="Health-Layer Linkage", description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health studies keep patient data in '
                                                  'large standard databases. This '
                                                  'block notes which of those systems '
                                                  'the exposure values were wired into '
                                                  'and through which field, so someone '
                                                  'browsing the health data can find '
                                                  'their way back to this record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Naming the downstream health-data '
                                                    'layer (OMOP, BDC, …) and the join '
                                                    'field makes the exposure record '
                                                    'findable from the clinical side; '
                                                    'without it the sidecar and the '
                                                    'health records it serves drift '
                                                    'apart, and the link must be '
                                                    'reconstructed by hand.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cohort_size_anchored': 3,
                                  'health_layer_link_field': 'exposure_source_value',
                                  'health_layer_target': 'omop_external_exposure'}}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/',
                      'https://biodatacatalyst.nhlbi.nih.gov/'],
         'slot_group': 'health_data_integration'} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, title="FAIR Deposit Metadata", description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If this record and its data are '
                                                  'published in a public archive (such '
                                                  'as Zenodo), this block holds the '
                                                  'publication details: the permanent '
                                                  'DOI link, where it lives, and the '
                                                  'license saying how others may use '
                                                  'it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'When the sidecar travels with a '
                                                    'published deposit, the DOI, '
                                                    'repository, and license are what '
                                                    'make the object findable, '
                                                    'citable, and legally reusable — '
                                                    'omitting them strands a public '
                                                    'artifact without citation or '
                                                    'reuse terms. Optional because '
                                                    'most records are never '
                                                    'deposited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'deposit_doi': '10.5281/zenodo.9999999',
                                  'deposit_license_spdx': 'CC-BY-4.0',
                                  'deposit_repository': 'zenodo'}}],
         'see_also': ['https://www.go-fair.org/fair-principles/'],
         'slot_group': 'health_data_integration'} })
    schema_version: str = Field(default=..., title="Schema Version", description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Schemas change over time, like '
                                                  'editions of a paper form. This is '
                                                  'the edition number stamped on the '
                                                  'document, so anyone reading it '
                                                  'knows exactly which version of the '
                                                  'form was filled in and can '
                                                  'interpret the fields accordingly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Downstream consumers must branch '
                                                    'on schema evolution: a parser '
                                                    'built for one version will '
                                                    'silently misread or wrongly '
                                                    'reject sidecars written against '
                                                    'another. Without this slot there '
                                                    'is no way to tell which iteration '
                                                    'of the schema a document '
                                                    'targets.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': '0.1'}],
         'see_also': ['https://semver.org/'],
         'slot_group': 'record_bookkeeping'} })
    provenance_id: str = Field(default=..., title="Record Identifier", description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A unique serial number for this '
                                                  'metadata document, like the '
                                                  'tracking number on a parcel. '
                                                  'Wherever the data value ends up, '
                                                  'that number lets you look up '
                                                  'exactly where it came from and how '
                                                  'it was made.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This identifier is what the '
                                                    "downstream health-data layer's "
                                                    'source-value field carries (for '
                                                    'OMOP, '
                                                    '`external_exposure.exposure_source_value`); '
                                                    'it is the only hook that links an '
                                                    'exposure value in the health '
                                                    'layer back to its full spatial, '
                                                    'temporal, and model provenance. '
                                                    'Omit it and the value becomes '
                                                    'untraceable — its metadata can '
                                                    'never be recovered.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'ULID-based sidecar identifier for the Daymet '
                                      'Tmax deposit',
                       'value': '01HFA7K8R3M6XP-daymet-deposit'}],
         'see_also': ['https://github.com/ulid/spec',
                      'https://ohdsi.github.io/CommonDataModel/'],
         'slot_group': 'record_bookkeeping'} })
    phi_status: PhiStatusEnum = Field(default=..., title="PHI Status", description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'PHI (protected health information) '
                                                  'means private medical details about '
                                                  'an identifiable person. This flag '
                                                  'is a written promise on the '
                                                  'document saying "no private patient '
                                                  'information inside", so it can be '
                                                  'passed around and published '
                                                  'safely.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Sidecars are designed to be '
                                                    'PHI-free, and this slot is the '
                                                    'explicit machine-readable '
                                                    'assertion of that. Without it, '
                                                    'every sharing, deposit, or export '
                                                    'step must treat the document as '
                                                    'potentially containing patient '
                                                    'data and re-review it manually '
                                                    'before it can leave a protected '
                                                    'environment.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': 'no_phi'}],
         'see_also': ['https://www.hhs.gov/hipaa/for-professionals/privacy/index.html'],
         'slot_group': 'record_bookkeeping'} })


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
         'see_also': ['https://en.wikipedia.org/wiki/Wet-bulb_globe_temperature',
                      'https://doi.org/10.1038/s41597-022-01405-3'],
         'slot_usage': {'derived_heat_metric': {'name': 'derived_heat_metric',
                                                'required': True}},
         'title': 'Outdoor WBGT Record'})

    subject: str = Field(default=..., title="Subject (Patient or Cohort)", description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'open_question': {'tag': 'open_question',
                                           'value': '`subject` is the only field in '
                                                    'this group that is not a '
                                                    'per-value predicate: every other '
                                                    'field explains an individual '
                                                    'value, but a single scalar '
                                                    'subject is dataset-scoped and '
                                                    'cannot distribute over the '
                                                    "sidecar's rows (per-row subject "
                                                    'identity lives in '
                                                    '`subject_column`). Under review — '
                                                    'should it be dropped, or demoted '
                                                    'to a dataset-level cohort handle? '
                                                    'Feedback welcome.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition'],
         'slot_group': 'exposure_description'} })
    variable_identity: VariableIdentity = Field(default=..., title="Variable Identity", description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable). Readable rename of the profile's `observation_type` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['observation_type'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block pins down exactly what '
                                                  'was measured. Instead of relying on '
                                                  'a nickname like "tmax", it uses '
                                                  'shared vocabularies to say "daily '
                                                  'maximum air temperature, in degrees '
                                                  'Celsius", so any tool or researcher '
                                                  'reads it the same way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a standard variable '
                                                    'identity, "tmax" in one file and '
                                                    '"TMAX" in another cannot be '
                                                    'recognised as the same physical '
                                                    'quantity, and unit mix-ups '
                                                    '(Celsius vs Fahrenheit vs Kelvin) '
                                                    'go undetected — pooling and '
                                                    'cross-study comparison silently '
                                                    'break.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:observation_type'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cf_cell_methods': 'time: maximum',
                                  'standard_name': 'CF:air_temperature',
                                  'units_ucum': 'Cel',
                                  'variable_name': 'tmax'}}],
         'implements': ['msprofile:observation_type'],
         'see_also': ['https://cfconventions.org/', 'https://ucum.org/'],
         'slot_group': 'exposure_description'} })
    spatial_reference: SpatialReference = Field(default=..., title="Spatial Reference", description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial). Readable rename of the profile's `location` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['location'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block says where the number '
                                                  'applies and how it was pulled out '
                                                  'of a map. Environmental data '
                                                  'usually comes as a grid of cells '
                                                  'covering a region; this records how '
                                                  'big those cells are and how the '
                                                  'value for a specific place was '
                                                  'picked from them.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A value without its grid, '
                                                    'coordinate system, and extraction '
                                                    'method cannot be located or '
                                                    'compared: a 1 km neighbourhood '
                                                    'average and a ~31 km regional '
                                                    'average look identical as numbers '
                                                    'but describe very different '
                                                    'exposures, and the extraction '
                                                    'cannot be re-run without the '
                                                    'method.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:location'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'crs': 'EPSG:4326',
                                  'extraction_method': 'inverse_distance_weighted_4_nearest_cells',
                                  'native_spatial_resolution_m': 1000,
                                  'target_geography_type': 'point_residence'}}],
         'implements': ['msprofile:location'],
         'see_also': ['https://epsg.io/'],
         'slot_group': 'exposure_description'} })
    temporal_reference: TemporalReference = Field(default=..., title="Temporal Reference", description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal). Readable rename of the profile's `temporality` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['temporality'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block explains the time ruler '
                                                  'behind each value: how long a '
                                                  'period each number summarises (a '
                                                  'day, a month), how it was '
                                                  'summarised (maximum, mean), and — '
                                                  'surprisingly important — when a '
                                                  '"day" is considered to start and '
                                                  'end.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A "daily maximum" is ambiguous '
                                                    'without the day-boundary '
                                                    'convention: Daymet days end at '
                                                    'local midnight while PRISM days '
                                                    'end at 12:00 GMT, so the same '
                                                    'calendar date can cover different '
                                                    'physical hours — the most-omitted '
                                                    'detail in the heat literature and '
                                                    'a known source of cross-product '
                                                    'disagreement.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:temporality'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'calendar': 'gregorian',
                                  'day_boundary_convention': 'local_midnight',
                                  'temporal_aggregation_method': 'maximum',
                                  'temporal_resolution': 'daily'}}],
         'implements': ['msprofile:temporality'],
         'see_also': ['https://cfconventions.org/'],
         'slot_group': 'exposure_description'} })
    exposure_model: ExposureModel = Field(default=..., title="Exposure Model", description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Readable rename of the profile's `methodology` anatomy slot, narrowed to the model itself: other methodology-adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots.""", json_schema_extra = { "linkml_meta": {'aliases': ['methodology'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most exposure values are not direct '
                                                  'readings from an instrument at '
                                                  "someone's house — they are "
                                                  'estimates computed from weather '
                                                  'stations, satellites, or models. '
                                                  'This block says which estimation '
                                                  'method produced the numbers and '
                                                  'what went into it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The same quantity can be '
                                                    'estimated by station '
                                                    'interpolation, satellite '
                                                    'retrieval, or model reanalysis, '
                                                    'each with different inputs and '
                                                    'biases; without the model '
                                                    'description, values from '
                                                    'different products get pooled as '
                                                    'if equivalent and their '
                                                    'systematic differences stay '
                                                    'invisible.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:methodology'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'bias_correction_applied': 'none',
                                  'exposure_model_inputs': ['GHCN-Daily station '
                                                            'observations'],
                                  'exposure_model_paper_doi': '10.3334/ORNLDAAC/2129',
                                  'exposure_model_type': 'spatial_interpolation'}}],
         'implements': ['msprofile:methodology'],
         'slot_group': 'exposure_description'} })
    uncertainty: Optional[Uncertainty] = Field(default=None, title="Uncertainty", description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'No estimate is perfect. This block '
                                                  'says how far off the numbers might '
                                                  'be and what was done about gaps in '
                                                  'the data, so users know how much '
                                                  'confidence to place in each value.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Exposure values are model '
                                                    'estimates with error; without '
                                                    'recorded per-value or aggregate '
                                                    'uncertainty and missing-data '
                                                    'handling, downstream analyses '
                                                    'treat estimates as exact, and '
                                                    'exposure-measurement error '
                                                    'propagates invisibly into '
                                                    'health-effect estimates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'data_completeness_pct': 100,
                                  'missing_data_handling_method': 'spatiotemporal_interpolation',
                                  'per_value_uncertainty_type': 'standard_error',
                                  'per_value_uncertainty_units_ucum': 'Cel'}}],
         'slot_group': 'exposure_description'} })
    derived_heat_metric: DerivedHeatMetric = Field(default=..., title="Derived Heat Metric", description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some heat measures are not read '
                                                  'from a thermometer but calculated '
                                                  'from several ingredients '
                                                  '(temperature, humidity, wind, '
                                                  'sunshine) using a chosen formula. '
                                                  'This block records which formula '
                                                  'and ingredients were used — it is '
                                                  'only needed when the variable is '
                                                  'one of these computed heat '
                                                  'metrics.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Heat metrics like WBGT or Heat '
                                                    'Index can be computed by several '
                                                    'non-equivalent equations from '
                                                    'different inputs, and heat-wave '
                                                    'flags depend on the threshold '
                                                    'definition; the heat-epidemiology '
                                                    'literature flags these choices as '
                                                    'the main sources of cross-study '
                                                    'disagreement, so omitting the '
                                                    'block for a heat metric makes the '
                                                    'record uncomparable.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'illustrative outdoor-WBGT methodology block — '
                                      'not part of the tmax scenario, where this slot '
                                      'is omitted',
                       'object': {'equation_variant': 'liljegren_2008',
                                  'heat_metric_family': 'wbgt_outdoor',
                                  'indoor_outdoor': 'outdoor',
                                  'solar_radiation_basis': 'surface_downwelling_shortwave_flux'}}],
         'slot_group': 'variable_specific_extensions'} })
    data_layout: DataLayout = Field(default=..., title="Data Layout", description="""Data-layout object binding this sidecar to the columns of the companion data file — see envar_layout. Required: without it a consumer cannot locate the values the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The actual numbers live in a '
                                                  'separate data table that travels '
                                                  'with this record. This block is the '
                                                  'map between the two: it names which '
                                                  'column holds the values, which '
                                                  'holds the person identifier, which '
                                                  'holds the date, and so on.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The sidecar describes values that '
                                                    'live in a companion CSV/parquet '
                                                    'file; without the column bindings '
                                                    'a consumer cannot tell which '
                                                    'column holds the values, '
                                                    'subjects, or dates, so the '
                                                    'metadata is unanchored and the '
                                                    'data unusable — hence the slot is '
                                                    'required.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'subject_column': 'subject_id',
                                  'table_orientation': 'wide',
                                  'time_column': 'date',
                                  'value_column': 'tmax'}}],
         'slot_group': 'dataset_and_provenance'} })
    source_dataset: SourceDataset = Field(default=..., title="Source Dataset", description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Exposure values are derived from a '
                                                  'published data product (for example '
                                                  'Daymet, a daily weather dataset). '
                                                  'This block names that product '
                                                  'precisely — including its version, '
                                                  'citation, and license — so anyone '
                                                  'can find it and check its '
                                                  'documentation.'},
                         'justification': {'tag': 'justification',
                                           'value': "Without the upstream product's "
                                                    'identity, version, DOI, and '
                                                    'license, the record cannot be '
                                                    'cited, its documented biases '
                                                    'cannot be looked up, and reuse '
                                                    'terms are unknown — and two '
                                                    'records built from different '
                                                    'product versions cannot be told '
                                                    'apart.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'source_dataset_doi': '10.3334/ORNLDAAC/2129',
                                  'source_dataset_name': 'Daymet V4 Daily Surface '
                                                         'Weather Data',
                                  'source_dataset_short_code': 'daymet_v4',
                                  'source_license_spdx': 'public-domain-us-gov'}}],
         'see_also': ['https://spdx.org/licenses/', 'https://www.doi.org/'],
         'slot_group': 'dataset_and_provenance'} })
    tool_run: ToolRun = Field(default=..., title="Tool Run", description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block is the receipt for the '
                                                  'software step that produced the '
                                                  'values: which program ran, which '
                                                  'exact version, with what settings, '
                                                  'and when. With it, someone else can '
                                                  're-run the same step and get the '
                                                  'same numbers.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the exact tool name, '
                                                    'version, container image, '
                                                    'parameters, and timestamp, the '
                                                    'record cannot be re-run: "we used '
                                                    'the daymet tool" is not '
                                                    'reproducible, but a pinned '
                                                    'container invocation is.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'container_image_repository': 'ghcr.io/degauss-org/daymet',
                                  'run_timestamp_utc': '2026-05-23T14:18:42Z',
                                  'tool_name': 'daymet',
                                  'tool_version': '1.0.0'}}],
         'slot_group': 'dataset_and_provenance'} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, title="Provenance Chain", description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Data usually passes through several '
                                                  'tools before the final value '
                                                  'appears — download, geocode, '
                                                  'extract. This block lists those '
                                                  'earlier steps in order, like a '
                                                  'chain of custody reaching back to '
                                                  'the original raw source.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The final tool run is rarely the '
                                                    'whole story — downloads, '
                                                    'geocoding, and intermediate '
                                                    'transforms precede it; without '
                                                    'the ordered chain back to the raw '
                                                    'source, end-to-end reproduction '
                                                    'and error tracing are impossible '
                                                    'even when the last step is '
                                                    'pinned.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'provenance_chain_steps': [{'run_timestamp_utc': '2026-05-23T14:02:11Z',
                                                              'tool_name': 'geocoder',
                                                              'tool_version': '3.3.0'}],
                                  'provenance_chain_terminus_type': 'raw_source_download'}}],
         'see_also': ['https://www.w3.org/TR/prov-o/'],
         'slot_group': 'dataset_and_provenance'} })
    linkage_method: LinkageMethod = Field(default=..., title="Linkage Method", description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Environmental data describes '
                                                  'places, but health research is '
                                                  'about people. This block records '
                                                  'how the value for a place was '
                                                  'attached to a particular person — '
                                                  'for example, by looking up the map '
                                                  'cell containing their home address '
                                                  '— since that step involves real '
                                                  'choices that affect the result.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Attaching a place-based value to '
                                                    'a person is a lossy, choice-laden '
                                                    'step (geocoding, point vs buffer '
                                                    'extraction, date alignment) — the '
                                                    '"linkage descriptor" gap the '
                                                    'GECC/EIRENE forum names as '
                                                    'central. Without it, two studies '
                                                    'using the same data product can '
                                                    'differ solely through '
                                                    'undocumented joins.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'address_period_alignment': 'address_history_from_emr',
                                  'clinical_date_assignment_convention': 'local_midnight',
                                  'lag_alignment_applied': 'none',
                                  'linkage_strategy': 'point_extraction_at_residence'}}],
         'slot_group': 'health_data_integration'} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, title="Health-Layer Linkage", description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health studies keep patient data in '
                                                  'large standard databases. This '
                                                  'block notes which of those systems '
                                                  'the exposure values were wired into '
                                                  'and through which field, so someone '
                                                  'browsing the health data can find '
                                                  'their way back to this record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Naming the downstream health-data '
                                                    'layer (OMOP, BDC, …) and the join '
                                                    'field makes the exposure record '
                                                    'findable from the clinical side; '
                                                    'without it the sidecar and the '
                                                    'health records it serves drift '
                                                    'apart, and the link must be '
                                                    'reconstructed by hand.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cohort_size_anchored': 3,
                                  'health_layer_link_field': 'exposure_source_value',
                                  'health_layer_target': 'omop_external_exposure'}}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/',
                      'https://biodatacatalyst.nhlbi.nih.gov/'],
         'slot_group': 'health_data_integration'} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, title="FAIR Deposit Metadata", description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If this record and its data are '
                                                  'published in a public archive (such '
                                                  'as Zenodo), this block holds the '
                                                  'publication details: the permanent '
                                                  'DOI link, where it lives, and the '
                                                  'license saying how others may use '
                                                  'it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'When the sidecar travels with a '
                                                    'published deposit, the DOI, '
                                                    'repository, and license are what '
                                                    'make the object findable, '
                                                    'citable, and legally reusable — '
                                                    'omitting them strands a public '
                                                    'artifact without citation or '
                                                    'reuse terms. Optional because '
                                                    'most records are never '
                                                    'deposited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'deposit_doi': '10.5281/zenodo.9999999',
                                  'deposit_license_spdx': 'CC-BY-4.0',
                                  'deposit_repository': 'zenodo'}}],
         'see_also': ['https://www.go-fair.org/fair-principles/'],
         'slot_group': 'health_data_integration'} })
    schema_version: str = Field(default=..., title="Schema Version", description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Schemas change over time, like '
                                                  'editions of a paper form. This is '
                                                  'the edition number stamped on the '
                                                  'document, so anyone reading it '
                                                  'knows exactly which version of the '
                                                  'form was filled in and can '
                                                  'interpret the fields accordingly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Downstream consumers must branch '
                                                    'on schema evolution: a parser '
                                                    'built for one version will '
                                                    'silently misread or wrongly '
                                                    'reject sidecars written against '
                                                    'another. Without this slot there '
                                                    'is no way to tell which iteration '
                                                    'of the schema a document '
                                                    'targets.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': '0.1'}],
         'see_also': ['https://semver.org/'],
         'slot_group': 'record_bookkeeping'} })
    provenance_id: str = Field(default=..., title="Record Identifier", description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A unique serial number for this '
                                                  'metadata document, like the '
                                                  'tracking number on a parcel. '
                                                  'Wherever the data value ends up, '
                                                  'that number lets you look up '
                                                  'exactly where it came from and how '
                                                  'it was made.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This identifier is what the '
                                                    "downstream health-data layer's "
                                                    'source-value field carries (for '
                                                    'OMOP, '
                                                    '`external_exposure.exposure_source_value`); '
                                                    'it is the only hook that links an '
                                                    'exposure value in the health '
                                                    'layer back to its full spatial, '
                                                    'temporal, and model provenance. '
                                                    'Omit it and the value becomes '
                                                    'untraceable — its metadata can '
                                                    'never be recovered.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'ULID-based sidecar identifier for the Daymet '
                                      'Tmax deposit',
                       'value': '01HFA7K8R3M6XP-daymet-deposit'}],
         'see_also': ['https://github.com/ulid/spec',
                      'https://ohdsi.github.io/CommonDataModel/'],
         'slot_group': 'record_bookkeeping'} })
    phi_status: PhiStatusEnum = Field(default=..., title="PHI Status", description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'PHI (protected health information) '
                                                  'means private medical details about '
                                                  'an identifiable person. This flag '
                                                  'is a written promise on the '
                                                  'document saying "no private patient '
                                                  'information inside", so it can be '
                                                  'passed around and published '
                                                  'safely.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Sidecars are designed to be '
                                                    'PHI-free, and this slot is the '
                                                    'explicit machine-readable '
                                                    'assertion of that. Without it, '
                                                    'every sharing, deposit, or export '
                                                    'step must treat the document as '
                                                    'potentially containing patient '
                                                    'data and re-review it manually '
                                                    'before it can leave a protected '
                                                    'environment.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': 'no_phi'}],
         'see_also': ['https://www.hhs.gov/hipaa/for-professionals/privacy/index.html'],
         'slot_group': 'record_bookkeeping'} })


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
                                                'required': True}},
         'title': 'Extreme-Heat-Day Flag Record'})

    subject: str = Field(default=..., title="Subject (Patient or Cohort)", description="""The patient or cohort the exposure value is attached to. Carried as an opaque identifier; PHI must not appear here.""", json_schema_extra = { "linkml_meta": {'annotations': {'open_question': {'tag': 'open_question',
                                           'value': '`subject` is the only field in '
                                                    'this group that is not a '
                                                    'per-value predicate: every other '
                                                    'field explains an individual '
                                                    'value, but a single scalar '
                                                    'subject is dataset-scoped and '
                                                    'cannot distribute over the '
                                                    "sidecar's rows (per-row subject "
                                                    'identity lives in '
                                                    '`subject_column`). Under review — '
                                                    'should it be dropped, or demoted '
                                                    'to a dataset-level cohort handle? '
                                                    'Feedback welcome.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord', 'MicroschemaDefinition'],
         'slot_group': 'exposure_description'} })
    variable_identity: VariableIdentity = Field(default=..., title="Variable Identity", description="""The variable identity object — what physical quantity is being captured. Bound to VariableIdentity (see envar_variable). Readable rename of the profile's `observation_type` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['observation_type'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block pins down exactly what '
                                                  'was measured. Instead of relying on '
                                                  'a nickname like "tmax", it uses '
                                                  'shared vocabularies to say "daily '
                                                  'maximum air temperature, in degrees '
                                                  'Celsius", so any tool or researcher '
                                                  'reads it the same way.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without a standard variable '
                                                    'identity, "tmax" in one file and '
                                                    '"TMAX" in another cannot be '
                                                    'recognised as the same physical '
                                                    'quantity, and unit mix-ups '
                                                    '(Celsius vs Fahrenheit vs Kelvin) '
                                                    'go undetected — pooling and '
                                                    'cross-study comparison silently '
                                                    'break.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:observation_type'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cf_cell_methods': 'time: maximum',
                                  'standard_name': 'CF:air_temperature',
                                  'units_ucum': 'Cel',
                                  'variable_name': 'tmax'}}],
         'implements': ['msprofile:observation_type'],
         'see_also': ['https://cfconventions.org/', 'https://ucum.org/'],
         'slot_group': 'exposure_description'} })
    spatial_reference: SpatialReference = Field(default=..., title="Spatial Reference", description="""Spatial reference object describing the native grid and extraction. Bound to SpatialReference (see envar_spatial). Readable rename of the profile's `location` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['location'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block says where the number '
                                                  'applies and how it was pulled out '
                                                  'of a map. Environmental data '
                                                  'usually comes as a grid of cells '
                                                  'covering a region; this records how '
                                                  'big those cells are and how the '
                                                  'value for a specific place was '
                                                  'picked from them.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A value without its grid, '
                                                    'coordinate system, and extraction '
                                                    'method cannot be located or '
                                                    'compared: a 1 km neighbourhood '
                                                    'average and a ~31 km regional '
                                                    'average look identical as numbers '
                                                    'but describe very different '
                                                    'exposures, and the extraction '
                                                    'cannot be re-run without the '
                                                    'method.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:location'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'crs': 'EPSG:4326',
                                  'extraction_method': 'inverse_distance_weighted_4_nearest_cells',
                                  'native_spatial_resolution_m': 1000,
                                  'target_geography_type': 'point_residence'}}],
         'implements': ['msprofile:location'],
         'see_also': ['https://epsg.io/'],
         'slot_group': 'exposure_description'} })
    temporal_reference: TemporalReference = Field(default=..., title="Temporal Reference", description="""Temporal reference object describing resolution, aggregation, and day-boundary convention. Bound to TemporalReference (see envar_temporal). Readable rename of the profile's `temporality` anatomy slot.""", json_schema_extra = { "linkml_meta": {'aliases': ['temporality'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block explains the time ruler '
                                                  'behind each value: how long a '
                                                  'period each number summarises (a '
                                                  'day, a month), how it was '
                                                  'summarised (maximum, mean), and — '
                                                  'surprisingly important — when a '
                                                  '"day" is considered to start and '
                                                  'end.'},
                         'justification': {'tag': 'justification',
                                           'value': 'A "daily maximum" is ambiguous '
                                                    'without the day-boundary '
                                                    'convention: Daymet days end at '
                                                    'local midnight while PRISM days '
                                                    'end at 12:00 GMT, so the same '
                                                    'calendar date can cover different '
                                                    'physical hours — the most-omitted '
                                                    'detail in the heat literature and '
                                                    'a known source of cross-product '
                                                    'disagreement.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:temporality'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'calendar': 'gregorian',
                                  'day_boundary_convention': 'local_midnight',
                                  'temporal_aggregation_method': 'maximum',
                                  'temporal_resolution': 'daily'}}],
         'implements': ['msprofile:temporality'],
         'see_also': ['https://cfconventions.org/'],
         'slot_group': 'exposure_description'} })
    exposure_model: ExposureModel = Field(default=..., title="Exposure Model", description="""The exposure-model object describing how values were produced. Bound to ExposureModel (see envar_model). Readable rename of the profile's `methodology` anatomy slot, narrowed to the model itself: other methodology-adjacent concerns (source dataset, tool run, provenance chain, derived heat metric) are surfaced as separate envar-extension slots.""", json_schema_extra = { "linkml_meta": {'aliases': ['methodology'],
         'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Most exposure values are not direct '
                                                  'readings from an instrument at '
                                                  "someone's house — they are "
                                                  'estimates computed from weather '
                                                  'stations, satellites, or models. '
                                                  'This block says which estimation '
                                                  'method produced the numbers and '
                                                  'what went into it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The same quantity can be '
                                                    'estimated by station '
                                                    'interpolation, satellite '
                                                    'retrieval, or model reanalysis, '
                                                    'each with different inputs and '
                                                    'biases; without the model '
                                                    'description, values from '
                                                    'different products get pooled as '
                                                    'if equivalent and their '
                                                    'systematic differences stay '
                                                    'invisible.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'exact_mappings': ['msprofile:methodology'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'bias_correction_applied': 'none',
                                  'exposure_model_inputs': ['GHCN-Daily station '
                                                            'observations'],
                                  'exposure_model_paper_doi': '10.3334/ORNLDAAC/2129',
                                  'exposure_model_type': 'spatial_interpolation'}}],
         'implements': ['msprofile:methodology'],
         'slot_group': 'exposure_description'} })
    uncertainty: Optional[Uncertainty] = Field(default=None, title="Uncertainty", description="""Uncertainty object — see envar_uncertainty.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'No estimate is perfect. This block '
                                                  'says how far off the numbers might '
                                                  'be and what was done about gaps in '
                                                  'the data, so users know how much '
                                                  'confidence to place in each value.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Exposure values are model '
                                                    'estimates with error; without '
                                                    'recorded per-value or aggregate '
                                                    'uncertainty and missing-data '
                                                    'handling, downstream analyses '
                                                    'treat estimates as exact, and '
                                                    'exposure-measurement error '
                                                    'propagates invisibly into '
                                                    'health-effect estimates.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'data_completeness_pct': 100,
                                  'missing_data_handling_method': 'spatiotemporal_interpolation',
                                  'per_value_uncertainty_type': 'standard_error',
                                  'per_value_uncertainty_units_ucum': 'Cel'}}],
         'slot_group': 'exposure_description'} })
    derived_heat_metric: DerivedHeatMetric = Field(default=..., title="Derived Heat Metric", description="""Heat-metric methodology, present when the variable is a derived heat metric — see envar_heat_metric. Omitted for non-heat variables.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Some heat measures are not read '
                                                  'from a thermometer but calculated '
                                                  'from several ingredients '
                                                  '(temperature, humidity, wind, '
                                                  'sunshine) using a chosen formula. '
                                                  'This block records which formula '
                                                  'and ingredients were used — it is '
                                                  'only needed when the variable is '
                                                  'one of these computed heat '
                                                  'metrics.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Heat metrics like WBGT or Heat '
                                                    'Index can be computed by several '
                                                    'non-equivalent equations from '
                                                    'different inputs, and heat-wave '
                                                    'flags depend on the threshold '
                                                    'definition; the heat-epidemiology '
                                                    'literature flags these choices as '
                                                    'the main sources of cross-study '
                                                    'disagreement, so omitting the '
                                                    'block for a heat metric makes the '
                                                    'record uncomparable.'},
                         'tier': {'tag': 'tier', 'value': 'conditionally_core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'illustrative outdoor-WBGT methodology block — '
                                      'not part of the tmax scenario, where this slot '
                                      'is omitted',
                       'object': {'equation_variant': 'liljegren_2008',
                                  'heat_metric_family': 'wbgt_outdoor',
                                  'indoor_outdoor': 'outdoor',
                                  'solar_radiation_basis': 'surface_downwelling_shortwave_flux'}}],
         'slot_group': 'variable_specific_extensions'} })
    data_layout: DataLayout = Field(default=..., title="Data Layout", description="""Data-layout object binding this sidecar to the columns of the companion data file — see envar_layout. Required: without it a consumer cannot locate the values the sidecar describes.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'The actual numbers live in a '
                                                  'separate data table that travels '
                                                  'with this record. This block is the '
                                                  'map between the two: it names which '
                                                  'column holds the values, which '
                                                  'holds the person identifier, which '
                                                  'holds the date, and so on.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The sidecar describes values that '
                                                    'live in a companion CSV/parquet '
                                                    'file; without the column bindings '
                                                    'a consumer cannot tell which '
                                                    'column holds the values, '
                                                    'subjects, or dates, so the '
                                                    'metadata is unanchored and the '
                                                    'data unusable — hence the slot is '
                                                    'required.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'subject_column': 'subject_id',
                                  'table_orientation': 'wide',
                                  'time_column': 'date',
                                  'value_column': 'tmax'}}],
         'slot_group': 'dataset_and_provenance'} })
    source_dataset: SourceDataset = Field(default=..., title="Source Dataset", description="""Source dataset object — see envar_source.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Exposure values are derived from a '
                                                  'published data product (for example '
                                                  'Daymet, a daily weather dataset). '
                                                  'This block names that product '
                                                  'precisely — including its version, '
                                                  'citation, and license — so anyone '
                                                  'can find it and check its '
                                                  'documentation.'},
                         'justification': {'tag': 'justification',
                                           'value': "Without the upstream product's "
                                                    'identity, version, DOI, and '
                                                    'license, the record cannot be '
                                                    'cited, its documented biases '
                                                    'cannot be looked up, and reuse '
                                                    'terms are unknown — and two '
                                                    'records built from different '
                                                    'product versions cannot be told '
                                                    'apart.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'source_dataset_doi': '10.3334/ORNLDAAC/2129',
                                  'source_dataset_name': 'Daymet V4 Daily Surface '
                                                         'Weather Data',
                                  'source_dataset_short_code': 'daymet_v4',
                                  'source_license_spdx': 'public-domain-us-gov'}}],
         'see_also': ['https://spdx.org/licenses/', 'https://www.doi.org/'],
         'slot_group': 'dataset_and_provenance'} })
    tool_run: ToolRun = Field(default=..., title="Tool Run", description="""The current ToolRun — see envar_toolrun.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'This block is the receipt for the '
                                                  'software step that produced the '
                                                  'values: which program ran, which '
                                                  'exact version, with what settings, '
                                                  'and when. With it, someone else can '
                                                  're-run the same step and get the '
                                                  'same numbers.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Without the exact tool name, '
                                                    'version, container image, '
                                                    'parameters, and timestamp, the '
                                                    'record cannot be re-run: "we used '
                                                    'the daymet tool" is not '
                                                    'reproducible, but a pinned '
                                                    'container invocation is.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'container_image_repository': 'ghcr.io/degauss-org/daymet',
                                  'run_timestamp_utc': '2026-05-23T14:18:42Z',
                                  'tool_name': 'daymet',
                                  'tool_version': '1.0.0'}}],
         'slot_group': 'dataset_and_provenance'} })
    provenance_chain: Optional[ProvenanceChain] = Field(default=None, title="Provenance Chain", description="""Ordered W3C-PROV-style chain of upstream tool runs — see envar_toolrun. Recommended (not required): a record is reproducible in principle without the full chain, but real reproduction needs it.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Data usually passes through several '
                                                  'tools before the final value '
                                                  'appears — download, geocode, '
                                                  'extract. This block lists those '
                                                  'earlier steps in order, like a '
                                                  'chain of custody reaching back to '
                                                  'the original raw source.'},
                         'justification': {'tag': 'justification',
                                           'value': 'The final tool run is rarely the '
                                                    'whole story — downloads, '
                                                    'geocoding, and intermediate '
                                                    'transforms precede it; without '
                                                    'the ordered chain back to the raw '
                                                    'source, end-to-end reproduction '
                                                    'and error tracing are impossible '
                                                    'even when the last step is '
                                                    'pinned.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'provenance_chain_steps': [{'run_timestamp_utc': '2026-05-23T14:02:11Z',
                                                              'tool_name': 'geocoder',
                                                              'tool_version': '3.3.0'}],
                                  'provenance_chain_terminus_type': 'raw_source_download'}}],
         'see_also': ['https://www.w3.org/TR/prov-o/'],
         'slot_group': 'dataset_and_provenance'} })
    linkage_method: LinkageMethod = Field(default=..., title="Linkage Method", description="""Linkage-method object — see envar_linkage.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Environmental data describes '
                                                  'places, but health research is '
                                                  'about people. This block records '
                                                  'how the value for a place was '
                                                  'attached to a particular person — '
                                                  'for example, by looking up the map '
                                                  'cell containing their home address '
                                                  '— since that step involves real '
                                                  'choices that affect the result.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Attaching a place-based value to '
                                                    'a person is a lossy, choice-laden '
                                                    'step (geocoding, point vs buffer '
                                                    'extraction, date alignment) — the '
                                                    '"linkage descriptor" gap the '
                                                    'GECC/EIRENE forum names as '
                                                    'central. Without it, two studies '
                                                    'using the same data product can '
                                                    'differ solely through '
                                                    'undocumented joins.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'address_period_alignment': 'address_history_from_emr',
                                  'clinical_date_assignment_convention': 'local_midnight',
                                  'lag_alignment_applied': 'none',
                                  'linkage_strategy': 'point_extraction_at_residence'}}],
         'slot_group': 'health_data_integration'} })
    health_layer_linkage: Optional[HealthLayerLinkage] = Field(default=None, title="Health-Layer Linkage", description="""Downstream health-data-layer linkage hooks (OMOP, BDC, …) — see envar_health_layer. Optional: its members are Recommended/Optional, and the Core PHI assertion lives at the record root (`phi_status`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Health studies keep patient data in '
                                                  'large standard databases. This '
                                                  'block notes which of those systems '
                                                  'the exposure values were wired into '
                                                  'and through which field, so someone '
                                                  'browsing the health data can find '
                                                  'their way back to this record.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Naming the downstream health-data '
                                                    'layer (OMOP, BDC, …) and the join '
                                                    'field makes the exposure record '
                                                    'findable from the clinical side; '
                                                    'without it the sidecar and the '
                                                    'health records it serves drift '
                                                    'apart, and the link must be '
                                                    'reconstructed by hand.'},
                         'tier': {'tag': 'tier', 'value': 'recommended'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'cohort_size_anchored': 3,
                                  'health_layer_link_field': 'exposure_source_value',
                                  'health_layer_target': 'omop_external_exposure'}}],
         'see_also': ['https://ohdsi.github.io/CommonDataModel/',
                      'https://biodatacatalyst.nhlbi.nih.gov/'],
         'slot_group': 'health_data_integration'} })
    deposit_metadata: Optional[DepositMetadata] = Field(default=None, title="FAIR Deposit Metadata", description="""FAIR-deposit metadata, present when the sidecar is intended to travel with a published deposit — see envar_health_layer.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'If this record and its data are '
                                                  'published in a public archive (such '
                                                  'as Zenodo), this block holds the '
                                                  'publication details: the permanent '
                                                  'DOI link, where it lives, and the '
                                                  'license saying how others may use '
                                                  'it.'},
                         'justification': {'tag': 'justification',
                                           'value': 'When the sidecar travels with a '
                                                    'published deposit, the DOI, '
                                                    'repository, and license are what '
                                                    'make the object findable, '
                                                    'citable, and legally reusable — '
                                                    'omitting them strands a public '
                                                    'artifact without citation or '
                                                    'reuse terms. Optional because '
                                                    'most records are never '
                                                    'deposited.'},
                         'tier': {'tag': 'tier', 'value': 'optional'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'abridged — see '
                                      'tests/data/valid/EnvironmentalExposureRecord-tmax_ideal.yaml '
                                      'for a full instance',
                       'object': {'deposit_doi': '10.5281/zenodo.9999999',
                                  'deposit_license_spdx': 'CC-BY-4.0',
                                  'deposit_repository': 'zenodo'}}],
         'see_also': ['https://www.go-fair.org/fair-principles/'],
         'slot_group': 'health_data_integration'} })
    schema_version: str = Field(default=..., title="Schema Version", description="""The version of the EnVar micro-schema this document conforms to. Required on every sidecar so downstream consumers can branch on schema evolution.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'Schemas change over time, like '
                                                  'editions of a paper form. This is '
                                                  'the edition number stamped on the '
                                                  'document, so anyone reading it '
                                                  'knows exactly which version of the '
                                                  'form was filled in and can '
                                                  'interpret the fields accordingly.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Downstream consumers must branch '
                                                    'on schema evolution: a parser '
                                                    'built for one version will '
                                                    'silently misread or wrongly '
                                                    'reject sidecars written against '
                                                    'another. Without this slot there '
                                                    'is no way to tell which iteration '
                                                    'of the schema a document '
                                                    'targets.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': '0.1'}],
         'see_also': ['https://semver.org/'],
         'slot_group': 'record_bookkeeping'} })
    provenance_id: str = Field(default=..., title="Record Identifier", description="""Stable identifier for this sidecar / record (ULID recommended). This is the value the downstream health-data layer's source-value field carries to link a row back to its provenance (for OMOP, that field is `external_exposure.exposure_source_value`).""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'A unique serial number for this '
                                                  'metadata document, like the '
                                                  'tracking number on a parcel. '
                                                  'Wherever the data value ends up, '
                                                  'that number lets you look up '
                                                  'exactly where it came from and how '
                                                  'it was made.'},
                         'justification': {'tag': 'justification',
                                           'value': 'This identifier is what the '
                                                    "downstream health-data layer's "
                                                    'source-value field carries (for '
                                                    'OMOP, '
                                                    '`external_exposure.exposure_source_value`); '
                                                    'it is the only hook that links an '
                                                    'exposure value in the health '
                                                    'layer back to its full spatial, '
                                                    'temporal, and model provenance. '
                                                    'Omit it and the value becomes '
                                                    'untraceable — its metadata can '
                                                    'never be recovered.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'description': 'ULID-based sidecar identifier for the Daymet '
                                      'Tmax deposit',
                       'value': '01HFA7K8R3M6XP-daymet-deposit'}],
         'see_also': ['https://github.com/ulid/spec',
                      'https://ohdsi.github.io/CommonDataModel/'],
         'slot_group': 'record_bookkeeping'} })
    phi_status: PhiStatusEnum = Field(default=..., title="PHI Status", description="""Whether the sidecar carries any Protected Health Information. A record-level safety assertion; by design, sidecars are PHI-free.""", json_schema_extra = { "linkml_meta": {'annotations': {'explanation': {'tag': 'explanation',
                                         'value': 'PHI (protected health information) '
                                                  'means private medical details about '
                                                  'an identifiable person. This flag '
                                                  'is a written promise on the '
                                                  'document saying "no private patient '
                                                  'information inside", so it can be '
                                                  'passed around and published '
                                                  'safely.'},
                         'justification': {'tag': 'justification',
                                           'value': 'Sidecars are designed to be '
                                                    'PHI-free, and this slot is the '
                                                    'explicit machine-readable '
                                                    'assertion of that. Without it, '
                                                    'every sharing, deposit, or export '
                                                    'step must treat the document as '
                                                    'potentially containing patient '
                                                    'data and re-review it manually '
                                                    'before it can leave a protected '
                                                    'environment.'},
                         'tier': {'tag': 'tier', 'value': 'core'}},
         'domain_of': ['EnvironmentalExposureRecord'],
         'examples': [{'value': 'no_phi'}],
         'see_also': ['https://www.hhs.gov/hipaa/for-professionals/privacy/index.html'],
         'slot_group': 'record_bookkeeping'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
VariableIdentity.model_rebuild()
DataLayout.model_rebuild()
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
