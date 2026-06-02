"""linkml-microschemas-envar.

LinkML microschemas for environmental exposure variables (EnVar). Initial scope: heat-related exposures (Tmax, WBGT, heat index, heat-wave flags) and the surrounding provenance metadata needed to load them into OMOP external_exposure with full reproducibility.
"""

try:
    from linkml_microschemas_envar._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
