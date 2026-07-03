# config.public.mk

# This file is public in git. No sensitive info allowed.

###### schema definition variables, used by justfile

# Note:
# - just works fine with quoted variables of dot-env files like this one
LINKML_SCHEMA_NAME="linkml_microschemas_envar"
LINKML_SCHEMA_AUTHOR="Nico Matentzoglu <nicolas.matentzoglu@gmail.com>"
LINKML_SCHEMA_DESCRIPTION="LinkML microschemas for environmental exposure variables (EnVar). Initial scope: heat-related exposures (Tmax, WBGT, heat index, heat-wave flags) and the surrounding provenance metadata needed to load them into OMOP external_exposure with full reproducibility."
LINKML_SCHEMA_SOURCE_DIR="src/linkml_microschemas_envar/schema"

###### linkml generator variables, used by justfile

## gen-project configuration file
LINKML_GENERATORS_CONFIG_YAML=config.yaml

## pass args if gendoc ignores config.yaml (i.e. --no-mergeimports)
## --subfolder-type-separation keeps class pages (Uncertainty.md) and slot
## pages (uncertainty.md) in separate folders so they cannot collide on
## case-insensitive filesystems (macOS/Windows local previews)
## --template-directory points gen-doc at the customized slot page template
## (docs/templates-linkml/slot.md.jinja2), which surfaces the tier /
## justification / explanation annotations as proper sections
LINKML_GENERATORS_DOC_ARGS="--subfolder-type-separation --template-directory docs/templates-linkml"

## pass args to workaround genowl rdfs config bug (linkml#1453)
##   (i.e. --no-type-objects --no-metaclasses --metadata-profile=rdfs)
# LINKML_GENERATORS_OWL_ARGS="--no-type-objects --no-metaclasses --metadata-profile=rdfs"
LINKML_GENERATORS_OWL_ARGS=

## pass args to pydantic generator which isn't supported by gen-project
## https://github.com/linkml/linkml/issues/2537
LINKML_GENERATORS_PYDANTIC_ARGS=
