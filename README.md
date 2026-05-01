# NASA Exoplanet Habitability Analysis

A data science pipeline for identifying Earth-like exoplanet candidates from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/). The project applies a multi-stage filtering methodology across 38,973 planetary records to isolate candidates most likely to support liquid water and rocky surface conditions.

---

## Table of Contents

- [Overview](#overview)
- [Methodology](#methodology)
- [Filtering Criteria](#filtering-criteria)
- [Stellar Classification Analysis](#stellar-classification-analysis)
- [Key Finding](#key-finding)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Usage](#usage)
- [Data Source](#data-source)

---

## Overview

| Parameter             | Value                        |
|-----------------------|------------------------------|
| Source Dataset        | NASA Exoplanet Archive (PSCompPars) |
| Total Records         | 38,973 planetary entries     |
| Processing Pipeline   | 8 Jupyter Notebooks          |
| Primary Language      | Python 3.10+                 |
| Core Libraries        | Pandas, NumPy, Matplotlib    |
| Primary Candidate     | Kepler-452 b                 |

---

## Methodology

The analysis is structured as a sequential, multi-stage pipeline distributed across 8 Jupyter Notebooks. Each notebook handles a discrete phase of the workflow, from raw data ingestion through final candidate scoring.

| Notebook | Stage | Description |
|---|---|---|
| `01_data_ingestion.ipynb` | Ingestion | Load raw CSV from NASA archive; initial schema inspection |
| `02_data_cleaning.ipynb` | Cleaning | Handle nulls, enforce data types, drop duplicate UIDs |
| `03_rocky_filter.ipynb` | Filter I | Apply planetary radius constraint (≤ 2 R⊕) |
| `04_thermal_filter.ipynb` | Filter II | Apply equilibrium temperature bounds (273K – 373K) |
| `05_insolation_filter.ipynb` | Filter III | Apply stellar insolation flux bounds (0.5 – 1.5 S⊕) |
| `06_stellar_classification.ipynb` | Classification | Segment candidates by host star spectral type (F/G/K/M) |
| `07_habitability_scoring.ipynb` | Scoring | Rank candidates using a composite habitability index |
| `08_final_analysis.ipynb` | Reporting | Generate summary statistics and export final candidates |

---

## Filtering Criteria

Candidates are required to satisfy all three constraints simultaneously. Records with missing values in any of the three key columns (`pl_rade`, `pl_eqt`, `pl_insol`) are excluded from downstream stages.

### Filter I — Rocky Composition

Planets are constrained to the rocky/super-Earth regime by placing an upper bound on planetary radius.

```
pl_rade <= 2.0   # Planetary radius in Earth radii
```

> Planets above 2 R⊕ are statistically likely to retain thick hydrogen-helium envelopes, precluding rocky surface conditions.

---

### Filter II — Thermal Constraints (Equilibrium Temperature)

The equilibrium temperature window is aligned with the liquid water phase boundary at standard atmospheric pressure.

```
273 <= pl_eqt <= 373   # Equilibrium temperature in Kelvin
```

---

### Filter III — Insolation Flux

Stellar flux received at the planet's orbital distance is constrained to the conservative habitable zone boundaries.

```
0.5 <= pl_insol <= 1.5   # Insolation flux in units of Earth flux (S⊕)
```

---

## Stellar Classification Analysis

A dedicated sub-analysis (`06_stellar_classification.ipynb`) segments the filtered candidate pool by host star spectral type. Each stellar class has distinct luminosity profiles, requiring specific orbital distance (AU) windows to remain within the habitable zone.

| Spectral Type | Temp. Range (K) | HZ Distance Constraint (AU) | Notes |
|---|---|---|---|
| F-type | 6,000 – 7,500 | 1.5 – 2.5 AU | Higher UV flux; shorter main-sequence lifespan |
| G-type | 5,200 – 6,000 | 0.9 – 1.4 AU | Solar analog; primary reference class |
| K-type | 3,700 – 5,200 | 0.4 – 0.9 AU | Extended main-sequence; favorable stability |
| M-type | 2,400 – 3,700 | 0.1 – 0.4 AU | Tidal locking and flare activity are risk factors |

The `st_spectype` column is parsed with a regex pattern to extract the primary spectral class character, accommodating the heterogeneous formatting present in the archive.

---

## Key Finding

**Primary Candidate: Kepler-452 b**

After all three filtering stages and stellar classification, **Kepler-452 b** emerges as the highest-ranked candidate. It satisfies all quantitative criteria and orbits a G-type star (solar analog) in the conservative habitable zone.

| Property | Value |
|---|---|
| Host Star | Kepler-452 |
| Spectral Type | G2V (solar analog) |
| Orbital Period | 384.84 days |
| Planetary Radius | ~1.63 R⊕ |
| Equilibrium Temp. | ~265 K |
| Insolation Flux | ~1.10 S⊕ |
| Orbital Distance | ~1.046 AU |

> **Note:** Kepler-452 b has no confirmed mass measurement. The rocky composition classification is inferred from radius alone using empirical mass-radius relationships (Chen & Kipping 2017). Confirmation of surface conditions requires follow-up spectroscopic observation.

---

## Project Structure

```
nasa-exoplanet-habitability/
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_rocky_filter.ipynb
│   ├── 04_thermal_filter.ipynb
│   ├── 05_insolation_filter.ipynb
│   ├── 06_stellar_classification.ipynb
│   ├── 07_habitability_scoring.ipynb
│   └── 08_final_analysis.ipynb
│
├── data/
│   ├── raw/
│   │   └── PS_CompPars_raw.csv        # Original archive download
│   ├── interim/
│   │   ├── cleaned.csv
│   │   ├── rocky_filtered.csv
│   │   ├── thermal_filtered.csv
│   │   └── insolation_filtered.csv
│   └── final/
│       └── habitable_candidates.csv   # Final scored candidate list
│
├── final_discovery.py                 # CLI script; runs full pipeline end-to-end
├── requirements.txt
└── README.md
```

---

## Requirements

```
python >= 3.10
pandas >= 2.0
numpy >= 1.24
matplotlib >= 3.7
seaborn >= 0.12
jupyterlab >= 4.0
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

**Run interactively via JupyterLab:**

```bash
jupyter lab
```

Open notebooks in the `notebooks/` directory and execute them in sequential order (01 → 08).

**Run the full pipeline as a single script:**

```bash
python final_discovery.py --input data/raw/PS_CompPars_raw.csv --output data/final/
```

Optional flags:

```
--radius-max     float   Maximum planetary radius in Earth radii (default: 2.0)
--temp-min       int     Minimum equilibrium temperature in K (default: 273)
--temp-max       int     Maximum equilibrium temperature in K (default: 373)
--flux-min       float   Minimum insolation flux in S⊕ (default: 0.5)
--flux-max       float   Maximum insolation flux in S⊕ (default: 1.5)
--verbose                Print stage-by-stage row counts to stdout
```

---

## Data Source

Data sourced from the NASA Exoplanet Archive Planetary Systems Composite Parameters table (PSCompPars).

- **URL:** https://exoplanetarchive.ipac.caltech.edu/
- **Table:** `PSCompPars`
- **Access method:** Direct CSV download or TAP/API query
- **Last retrieved:** 2025-07

```python
# Programmatic download via astroquery (optional)
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

data = NasaExoplanetArchive.query_criteria(table="pscomppars", select="*")
```

---

## License

This project is released under the [MIT License](LICENSE). The underlying NASA Exoplanet Archive data is publicly available and subject to NASA's standard data usage policies.
