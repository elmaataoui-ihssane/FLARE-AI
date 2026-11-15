# FLARE AI
### Agentic Research Assistant for Space Combustion Science

FLARE AI is an AI-powered research assistant designed to help researchers explore fire behavior and combustion in microgravity. It brings together scientific investigations, experimental datasets, and research publications through a multi-agent architecture.

The goal is to make space-combustion research easier to discover, explore, analyze, and understand, while keeping findings connected to their original sources.

## Key Features

- **Research Discovery:** Search NASA investigations and scientific publications.
- **Dataset Exploration:** Discover, load, and profile experimental datasets.
- **Scientific Analysis:** Explore experimental parameters, missing values, and dataset characteristics.
- **Multi-Agent Architecture:** Coordinate specialized research and data agents.
- **Evidence-Based Research:** Maintain references to datasets, investigations, and publications.

## Agent Architecture

FLARE AI is organized around specialized agents coordinated through a central workflow:

| Component | Responsibility |
|---|---|
| Orchestrator | Coordinates agents and research tasks |
| Research Agent | Searches NASA investigations and publications |
| Data Agent | Discovers, loads, and profiles datasets |
| Scientific Analysis Agent | Supports data exploration and analysis |
| Report Agent | Organizes findings into research reports |

## Datasets

The project currently works with three experimental datasets from **MicroFire Atlas**, a third-party curated resource.

| Dataset | Records | Download |
|---|---:|---|
| SAFFIRE | 20 | [CSV](https://microfire-atlas.vercel.app/downloads/saffire-runs.csv) |
| BASS-II | 56 | [CSV](https://microfire-atlas.vercel.app/downloads/bass2-tests.csv) |
| LUCI | 2 | [CSV](https://microfire-atlas.vercel.app/downloads/luci-runs.csv) |

Additional JSON resources include:

- `findings.json`
- `evidence-graph.json`
- `source-manifest.json`

The datasets contain experimental information about combustion, materials, environmental conditions, and experimental outcomes.

**Data note:** MicroFire Atlas is not an official NASA data repository. Its datasets are treated as third-party curated resources and should be checked against original scientific sources when necessary.

## NASA Resources

NASA resources are used to support investigation discovery and scientific research:

- [NASA Physical Sciences Informatics (PSI) Repository](https://psi.nasa.gov/physci/repo)
- [NASA PSI Investigations](https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/)
- [NASA Technical Reports Server (NTRS)](https://ntrs.nasa.gov/)
- [NASA NTRS API](https://ntrs.nasa.gov/api/citations/search)

Investigations explored include SAFFIRE, BASS-II, FLEX, and SAME.

## Technology

- **Python** – Core data processing and agent implementation
- **Pandas** – Dataset loading, cleaning, and profiling
- **Google Colab** – Data exploration and notebook development
- **NASA PSI and NTRS** – Scientific investigation and publication resources
- **MicroFire Atlas** – Third-party experimental datasets

## Data Processing and Validation

The data preparation workflow includes:

- Downloading and organizing source files.
- Standardizing column names.
- Removing exact duplicate rows.
- Profiling datasets and identifying missing values.
- Building dataset inventories and source registries.
- Running automated validation checks.

Missing values are preserved rather than automatically replaced with zero. Experimental units and conditions are not assumed to be interchangeable across datasets.


<img width="500" height="500" alt="logo-removebg-preview" src="https://github.com/user-attachments/assets/ab9a4efa-ccee-4e4c-b0cd-5216c83febd5" />


