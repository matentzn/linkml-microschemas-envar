<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# linkml-microschemas-envar

> **Status: very early prototype — for illustration only.** Schemas, examples,
> and design decisions are exploratory and will change. Nothing here is stable
> or production-ready.

LinkML microschemas for environmental exposure variables (EnVar). Initial scope: heat-related exposures (Tmax, WBGT, heat index, heat-wave flags) and the surrounding provenance metadata needed to load them into OMOP external_exposure with full reproducibility.

## Documentation Website

[https://monarch-initiative.github.io/linkml-microschemas-envar](https://monarch-initiative.github.io/linkml-microschemas-envar)

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files (edit these)
  * [linkml_microschemas_envar](src/linkml_microschemas_envar)
    * [schema/](src/linkml_microschemas_envar/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/linkml_microschemas_envar/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/).
To list all pre-defined commands, run `just` or `just --list`.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).
