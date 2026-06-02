"""Data model package for linkml-microschemas-envar."""

from pathlib import Path
from .linkml_microschemas_envar import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "linkml_microschemas_envar.yaml"
