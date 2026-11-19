# 🐢 Tamul Sea Turtle Eco-Informatics: Nesting Dynamics & Survival Analytics

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1%2B-150458?style=flat&logo=pandas&logoColor=white)
![ERA5-Land](https://img.shields.io/badge/Climate%20Data-ECMWF%20ERA5--Land-0055A4?style=flat)
![xAI](https://img.shields.io/badge/Modeling-Cox%20PH%20%7C%20Quasi--Binomial%20%7C%20SHAP-2E8B57?style=flat)

An end-to-end **Data Engineering, Thermodynamic Simulation, and eXplainable AI (xAI)** platform designed to analyze sea turtle incubation dynamics and hatching survival in the Mexican Caribbean (**Riviera Maya**, 2018–2024).

Developed within the framework of an applied conservation initiative linked to **The Palace Company** and the **Universidad del Caribe** (*Data Engineering and Organizational Intelligence*), this project transforms seven years of fragmented field logbooks and **70,128 hourly ECMWF climate records** into a reproducible analytical pipeline and a bilingual (**English / Spanish**) interactive **Streamlit** dashboard.

---

## 📋 Table of Contents
- [🐢 Tamul Sea Turtle Eco-Informatics: Nesting Dynamics \& Survival Analytics](#-tamul-sea-turtle-eco-informatics-nesting-dynamics--survival-analytics)
  - [📋 Table of Contents](#-table-of-contents)
  - [🌍 Background \& Problem Statement](#-background--problem-statement)
  - [🗄️ Data Sources \& ETL Pipeline](#️-data-sources--etl-pipeline)
    - [1. Biological Nesting Records (`anidaciones_tamul_2018_2024_maestro.csv`)](#1-biological-nesting-records-anidaciones_tamul_2018_2024_maestrocsv)
    - [2. Retrospective Climate Enrichment (`SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv`)](#2-retrospective-climate-enrichment-serie_maestra_tamul_2018_2025_localcsv)
  - [⚙️ Feature Engineering \& Thermodynamic Simulation](#️-feature-engineering--thermodynamic-simulation)
  - [🛡️ Key Troubleshooting \& Data Governance](#️-key-troubleshooting--data-governance)
  - [📊 Statistical Modeling \& Key Findings (xAI / SHAP)](#-statistical-modeling--key-findings-xai--shap)
    - [Thesis Archetypal Case Studies (Real Historical Nests)](#thesis-archetypal-case-studies-real-historical-nests)
  - [💻 Interactive Streamlit Dashboard](#-interactive-streamlit-dashboard)
  - [📂 Project Architecture](#-project-architecture)
  - [🚀 Installation \& Usage](#-installation--usage)
    - [Prerequisites](#prerequisites)
    - [Local Setup](#local-setup)
  - [🔭 Future Recommendations](#-future-recommendations)
  - [👨‍💻 Author \& Context](#-author--context)

---

## 🌍 Background & Problem Statement

The Riviera Maya is one of Mexico's most critical nesting habitats for sea turtles, primarily **Green turtles (*Chelonia mydas*)**, **Loggerhead turtles (*Caretta caretta*)**, and **Hawksbill turtles (*Eretmochelys imbricata*)**. Increasing coastal development and climate variability pose severe threats to embryonic survival and incubation phenology.

Prior to this project, the conservation camp faced three major analytical bottlenecks:
* **Data Fragmentation:** Over six years of historical field monitoring records (2018–2024) were stored in isolated, season-specific Excel spreadsheets without unified naming conventions, data types, or longitudinal traceability.
* **Lack of Physical Environmental Sensors:** The incubation corral lacked in-situ sand temperature loggers (thermistors) and weather stations, making it impossible to directly measure how thermal stress or heavy rainfall impacted individual clutches.
* **Descriptive-Only Decision Making:** Without derived ecological proxies (e.g., cumulative heat exposure or corral overcrowding), field decisions relied solely on manual reviews rather than quantitative survival modeling.

---

## 🗄️ Data Sources & ETL Pipeline

Following an adapted **CRISP-DM** methodology, raw operational spreadsheets were transformed into a unified, modeling-ready analytical repository using Python and Pandas.

### 1. Biological Nesting Records (`anidaciones_tamul_2018_2024_maestro.csv`)
* **Ingestion & Standardization:** Multi-season Excel workbooks (2018–2024) were converted to CSV and programmatically consolidated into a master table (**4,682 records × 35 fields**), standardizing column headers, data types, and scientific species nomenclature (`Cc` → *Caretta caretta*, `Cm` → *Chelonia mydas*, `Ei` → *Eretmochelys imbricata*).
* **Timestamp Normalization:** Constructed exact sowing (`fecha_siembra_calc`) and emergence (`fecha_emergencia_calc`, standardized to 20:00:00 local emergence time) timestamps to compute exact incubation durations in hours (`D_horas`).
* **Schema Evolution Preservation:** GPS coordinates were only captured starting in the 2024 season. Rather than discarding spatial attributes, the column was preserved in the unified schema (with nulls for prior years) to maintain historical compatibility while enabling future geospatial analysis.
* **Final Processed Analytical Dataset (`nidos_procesados_ML_v8.csv`):** Contains **4,681 modeled nests** across 7 seasons:
  * *Chelonia mydas*: **4,560 nests** (97.4%)
  * *Caretta caretta*: **105 nests** (2.2%)
  * *Eretmochelys imbricata*: **16 nests** (0.3%)

### 2. Retrospective Climate Enrichment (`SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv`)
* **Source:** **Copernicus Climate Data Store (ECMWF)** — **ERA5** (single-level atmospheric) and **ERA5-Land** (hourly land-surface reanalysis) products.
* **Spatial & Temporal Alignment:** Queried for a representative coastal grid coordinate covering the Tamul nesting stretch from **January 1, 2018 to December 31, 2025**, yielding **70,128 hourly records × 17 variables**.
* **Extracted Variables:** Multi-layer soil temperatures (`stl1_celsius`, `stl2_celsius` [7–28 cm], `stl3_celsius` [28–100 cm]), 2m air temperature (`t2m_celsius`), dewpoint (`d2m_celsius`), hourly precipitation (`tp_mm`), surface solar radiation (`ssrd_wm2`), and wind/wave parameters—all synchronized to local time (`time_local`) for exact nest-level window slicing.

---

## ⚙️ Feature Engineering & Thermodynamic Simulation

To bridge the absence of physical sand sensors, the core pipeline (`ejecutar_pipeline_definitivo`) pairs every nest's exact incubation window with hourly ERA5-Land time series to engineer physical-biological proxies:

| Feature | Description & Engineering Logic |
| :--- | :--- |
| **`T_base` & `T_base_mean`** | **Abiotic Sand Baseline (°C):** Linearly interpolates shallow (`stl2_celsius`) and deep (`stl3_celsius`) soil temperatures using species-specific nest depth weights (`0.91` for deeper-nesting *Chelonia mydas*, `0.59` for *Caretta caretta* and *Eretmochelys imbricata*). |
| **`T_nest` (Metabolic Heat)** | **Simulated Internal Nest Temperature (°C):** Models embryonic metabolic heating across incubation thirds ($T_1: 5\%$, $T_2: 15\%$, $T_3: 100\%$ of a clutch-scaled factor between $+2.5\text{ °C}$ and $+5.0\text{ °C}$). Smoothed with a **120-hour (5-day) centered rolling mean** to reflect gradual physiological heat buildup. |
| **`TSP_mean`** | **Thermosensitive Period Mean Temp (°C):** Mean internal nest temperature during the middle third of incubation ($T_2$), critical for embryonic development and sex determination. |
| **`ATL_33`** | **Accumulated Thermal Load (°C·h):** Cumulative sum of degree-hours where `T_nest > 33.0 °C` (the embryonic thermal lethality threshold). |
| **`precipitacion_total_mm`** | **Cumulative Rainfall (mm):** Total ERA5-Land precipitation accumulated over the nest's exact incubation window. |
| **`peak_corral_density` & `density_last_third`** | **Population & Metabolic Crowding:** Scans overlapping incubation windows day-by-day across all nests to quantify maximum simultaneous active nests in the corral and crowding during the nest's final third ($T_3$). |
| **`HSR`** | **Hatching Success Rate:** Target biological outcome defined as `crias_vivas / total_crias` (dataset mean: **85.0%**, median: **90.0%**). |

---

## 🛡️ Key Troubleshooting & Data Governance

Real-world environmental data requires strict domain-aware governance rather than blind automated filtering:

1. **ECMWF API Soil Variable Audit (Root-Cause Troubleshooting):** During exploratory validation, initial sand temperature curves showed physically illogical thermal amplitudes for beach sediment. By tracing the ETL pipeline backward—auditing the Copernicus API parameter requests and reviewing the depth-layer interpolation equations—a misassigned soil layer variable was identified and corrected, restoring realistic sand thermal inertia profiles.
2. **2019 Spatial Business Rule Correction (3x Corral Expansion):** The 2019 season experienced a historic nesting surge (**1,842 nests**, representing 39.3% of the 7-year total). Field biologist feedback confirmed that the physical corral area was tripled ($3\times$) that season. To prevent artificial overcrowding bias in survival models, `peak_corral_density` and `density_last_third` for 2019 are scaled by `/ 3.0`.
3. **Non-Destructive Anomaly Segregation (`reporte_anomalias_biologos.csv`):** Instead of silently dropping extreme outliers, the pipeline flags nests with biologically atypical incubation durations (`< 40 days` [960 h] or `> 75 days` [1,800 h]) into an audit CSV for expert review while preserving them in the dataset (e.g., `nido_uid: 2024_3` at **75.5 days / 1,811.6 h**). Only records lacking a valid emergence date are dropped (**1 record removed**: `2018_0001`).

---

## 📊 Statistical Modeling & Key Findings (xAI / SHAP)

Across **4,681 modeled nests** (mean clutch size: **113.5 eggs**; mean corral peak density: **321 simultaneous nests**, max **418**), statistical and machine learning models validated the ecological mechanisms driving incubation timing and mortality:

* **Phenological Acceleration (Cox Proportional Hazards Model):**
  * Higher **`ATL_33`** and **`density_last_third`** exhibit Hazard Ratios **$> 1$** ($\log(\text{HR}) > 0$), confirming that elevated thermal load and metabolic crowding accelerate embryonic development and shorten incubation duration.
  * Higher **`precipitacion_total_mm`** exhibits a Hazard Ratio **$< 1$** ($\log(\text{HR}) < 0$), confirming a cooling/delaying effect on emergence timing.
* **Hatching Survival Collapse (Overdispersed Binomial / Quasi-Binomial & XGBoost + SHAP):**
  * Odds ratios and SHAP dependence analysis identified three critical non-linear risk thresholds:
    * **Hydric Paradox / Cyclonic Washout:** Moderate rain (**50–150 mm**) aids thermoregulation, whereas cumulative rainfall **$> 300\text{ mm}$** triggers catastrophic washout and asphyxiation mortality.
    * **Lethal Thermal Load:** Prolonged exposure above **$33.0\text{ °C}$** accumulating **$> 600\text{ °C·h}$** (`ATL_33`) causes sharp declines in hatching survival.
    * **Corral Carrying Capacity:** Exceeding **$> 350$ simultaneous active nests** increases localized metabolic heat stress and reduces survival probabilities.

### Thesis Archetypal Case Studies (Real Historical Nests)
| Archetype | Nest ID | Season | HSR (%) | Rainfall (mm) | `ATL_33` (°C·h) | Duration | Ecological Diagnosis |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Optimal Success** | `2018_21` | 2018 | **95.2%** | 111.4 mm | 0.7 | 58.7 d | Ideal rainfall (50–150 mm) & near-zero lethal heat |
| **2. Cyclonic Washout** | `2018_437` | 2018 | **0.0%** | **322.0 mm** | 0.0 | 55.7 d | Exceeded >300 mm SHAP rain threshold (asphyxiation) |
| **3. Thermal & Density Stress** | `2019_949` | 2019 | **0.0%** | 130.6 mm | **664.2** | 54.7 d | Severe >33 °C thermal load + peak corral overcrowding |

---

## 💻 Interactive Streamlit Dashboard

To translate complex survival analytics into an operational tool for biologists and stakeholders, the pipeline is deployed as a **modular, bilingual Streamlit application** (**English by default**, with live toggle to **Spanish**):

* **Tab 1 — Thermodynamic Simulator & Biological Trilogy:** Inspect any of the 4,681 nests (or jump directly to the 3 thesis archetypes). Displays live KPI risk cards against SHAP thresholds and renders a 3-panel Matplotlib diagnostic figure (**Cyclonic Rain**, **Daily Corral Density**, and **Layer-by-Layer Sand/Nest Thermal Anatomy**). Daily corral density calculations are **vectorized via NumPy broadcasting** for millisecond rendering.
* **Tab 2 — Macro Trends & xAI Thresholds (2018–2024):** Multi-year summary tables and aggregated charts visualizing survival collapse across `ATL_33` bins and historical nesting volumes.
* **Tab 3 — Data Governance & ETL Audit:** Interactive inspector for the biological duration anomaly filter, dropped null-timestamp records, and the processed analytical table.

---

## 📂 Project Architecture

```text
tamul-sea-turtle-ecoinformatics/
├── app.py                                           # Streamlit entry point & bilingual UI orchestrator
├── requirements.txt                                 # Python dependencies for local & Streamlit Cloud deployment
├── README.md                                        # Project documentation
├── data/
│   ├── raw/
│   │   ├── SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv  # 70,128 hourly ECMWF ERA5-Land climate records
│   │   └── anidaciones_tamul_2018_2024_maestro.csv  # Consolidated 2018-2024 camp nesting logbook (4,682 rows)
│   └── processed/
│       └── nidos_procesados_ML_v8.csv               # Feature-engineered dataset ready for modeling (4,681 rows)
├── notebooks/
│   └── Pipeline_Tamul_Analisis_Eco_Informatico_2.ipynb  # Original Colab ETL & mechanism visualization notebook
└── src/
    ├── __init__.py                                  # Package initializer
    ├── config.py                                    # File path resolver, SHAP thresholds & biological constants
    ├── translations.py                              # Complete EN / ES internationalization (i18n) dictionary
    ├── data_loader.py                               # Cached (@st.cache_data) CSV ingestion utilities
    ├── thermodynamics.py                            # Vectorized ERA5 soil interpolation & corral density engine
    └── visualizations.py                            # Bilingual Matplotlib builders (Trilogy & Macro charts)
```

---

## 🚀 Installation & Usage

### Prerequisites
* Python 3.10 or higher
* `pip` package manager

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/dhtadeo/Turtle_Nesting_Dynamics_Project.git
   cd Turtle_Nesting_Dynamics_Project
   ```

2. **Create a virtual environment (recommended) and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Place the datasets in their respective folders:**
   * `data/raw/SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv`
   * `data/raw/anidaciones_tamul_2018_2024_maestro.csv`
   * `data/processed/nidos_procesados_ML_v8.csv`

4. **Launch the interactive dashboard:**
   ```bash
   streamlit run app.py
   ```

---

## 🔭 Future Recommendations

Based on the findings delivered to the conservation camp biologists:
* **In-Situ Thermal Instrumentation:** Deploy physical temperature data loggers across distinct corral zones and depths to calibrate and validate ERA5-Land thermal transfer coefficients.
* **Standardized Multi-Season Capture & GPS Logging:** Enforce standardized data entry schemas and expand GPS recording (initiated in 2024) across all nesting zones to support fine-grained spatiotemporal risk mapping.
* **Proactive Corral Capacity Management:** Use the **350 simultaneous nests** carrying capacity threshold as an early-warning operational KPI to plan corral expansions ahead of high-volume seasons.

---

## 👨‍💻 Author & Context

**Diego Hernández Tadeo** — Data Engineering & Organizational Intelligence (*Universidad del Caribe*, Cancún, Mexico)  
*Capstone Research Project developed in collaboration with the conservation monitoring program The Palace Company.*