# linkml-microschemas-envar

LinkML microschemas for environmental exposure variables (EnVar): a PHI-free metadata **sidecar** that travels with each exposure value series and carries the provenance needed to reproduce it — from the producing tool (Amadeus, DeGAUSS, …) into a health-data layer (OMOP `external_exposure`, BioData Catalyst, …). Worked scope: heat-related exposures (Tmax, WBGT, heat index, heat-wave flags), with PM2.5 as the generalisation check.

- [Schema overview](overview/index.html) — a plain-language, full-width tour of everything the schema captures (start here)
- [Architecture](architecture.md) — how the microschema modules compose (assumes LinkML fluency)
- [Related approaches](related-approaches.md) — how EnVar differs from GAIA, DeGAUSS, Amadeus, and CODATA Essential Variables
- [Example datasets](datasets/index.html) — every worked sidecar scored by the completeness checker, core → recommended → ideal
- Auto-generated [schema documentation](elements/index.md)
