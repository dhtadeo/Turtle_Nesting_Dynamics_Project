#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bilingual dictionary (English default / Spanish) for UI labels, metrics,
technical explanations, and Matplotlib visualizations.
"""

TRANSLATIONS = {
    "en": {
        "page_title": "Tamul Eco-Informatics | Sea Turtle Survival Analytics",
        "app_title": "🐢 Eco-Informatics Platform: Sea Turtle Nesting & Survival (Tamul)",
        "app_subtitle": (
            "**Feature Engineering Pipeline, ERA5-Land Thermodynamic Simulation & eXplainable AI (xAI)**  \n"
            "*Applied ecological conservation research project (2018–2024) | 70,128 hourly climate records & 4,681 modeled nests.*"
        ),
        "load_error": (
            "Could not load CSV files. Please ensure `nidos_procesados_ML_v8.csv` and "
            "`SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv` are placed in `data/processed/` and `data/raw/` "
            "(or in the root folder). Details: "
        ),
        "spinner_nidos": "Loading processed nesting dataset...",
        "spinner_era5": "Loading hourly ERA5-Land climate series (+70,000 records)...",
        "spinner_maestro": "Loading raw master logbook for data governance audit...",
        # Sidebar
        "sidebar_header": "🎛️ Eco-Informatics Control Panel",
        "lang_label": "🌐 Language / Idioma",
        "explore_mode_label": "Exploration Mode:",
        "mode_archetypes": "Thesis Archetypal Case Studies",
        "mode_free": "Free Explorer by Season & Species",
        "select_archetype": "Select a Biological Archetype:",
        "arch_1": "1. Optimal Successful Nest",
        "arch_2": "2. Cyclonic Washout Mortality",
        "arch_3": "3. Thermal Stress & Overcrowding Mortality",
        "select_year": "Season (Year):",
        "select_species": "Species:",
        "filter_status": "Filter by Hatching Outcome:",
        "status_all": "All nests",
        "status_high": "High Survival (HSR >= 85%)",
        "status_low": "Low Survival / Mortality (HSR < 30%)",
        "no_nests_warn": "No nests match this filter in the selected season. Showing all nests.",
        "select_nest": "Select Nest ID",
        "available": "available",
        "compare_ref": "Overlay Optimal Archetype baseline on charts",
        "sidebar_arch": (
            "**Data Architecture:**\n"
            "• **Climate:** ECMWF / ERA5-Land API\n"
            "• **Modeling:** Cox PH, Quasi-binomial Regression, XGBoost + SHAP\n"
            "• **Author:** Diego Hernández Tadeo"
        ),
        # Tabs
        "tab_1": "📊 1. Thermodynamic Simulator & Biological Trilogy",
        "tab_2": "📈 2. Macro Trends & xAI Thresholds (2018–2024)",
        "tab_3": "🛡️ 3. Data Governance & ETL Audit",
        # Tab 1
        "dossier_header": "Eco-Informatic Dossier for Nest",
        "season": "Season",
        "kpi_hsr": "Hatching Success Rate (HSR)",
        "hatchlings": "hatchlings",
        "kpi_duration": "Incubation Duration",
        "days": "days",
        "total_hours": "total hours",
        "kpi_rain": "Cumulative Precipitation",
        "rain_risk": "Washout Risk (>300 mm)",
        "rain_safe": "Safe Range (<300 mm)",
        "kpi_atl": "Lethal Thermal Load (ATL_33)",
        "atl_risk": "Lethal Stress (>600 °C·h)",
        "atl_safe": "Below Critical Threshold",
        "kpi_density": "Peak Corral Density",
        "nests": "nests",
        "density_risk": "Overcrowding (>350 nests)",
        "density_safe": "Optimal Capacity",
        "no_era5_warn": "No hourly ERA5 climate records found for this nest's date range.",
        "expander_title": "🔬 Technical Deep-Dive: Physics-Biology Feature Engineering",
        "expander_body": (
            "* **Compensating for Missing Physical Sensors:** Integrated **ECMWF ERA5-Land** reanalysis by interpolating shallow (`stl2_celsius`: 7–28 cm) and deep (`stl3_celsius`: 28–100 cm) soil layers with species-specific depth weights (`0.91` for *Chelonia mydas* due to deeper egg chambers, and `0.59` for *Caretta caretta* and *Eretmochelys imbricata*).\n"
            "* **Continuous Metabolic Heat Curve:** During the final third of incubation ($T_3$), embryonic metabolism raises internal nest temperature by $+2.5\\text{ °C}$ to $+5.0\\text{ °C}$ scaled by clutch size (`conteo_huevos`). A 120-hour centered rolling mean (`rolling(window=120)`) models a smooth biological transition without artificial step jumps.\n"
            "* **Accumulated Thermal Load (`ATL_33`):** Integrates degree-hours spent above the embryonic lethal thermal tolerance threshold ($33.0\\text{ °C}$)."
        ),
        # Charts Trilogy
        "chart_nest_prefix": "Nest",
        "chart_ref_prefix": "Successful Archetype",
        "chart_opt_rain": "Optimal Thermoregulation Zone (50–150 mm)",
        "chart_shap_rain": "SHAP Lethal Threshold (> 300 mm - Asphyxiation/Washout)",
        "chart_title_a": "A. Cyclonic Impact & Hydric Paradox (ERA5-Land)",
        "chart_xlabel_days": "Incubation Days",
        "chart_ylabel_rain": "Cumulative Precipitation (mm)",
        "chart_dens_ref": "Density",
        "chart_dens_sel": "Corral Density — Nest",
        "chart_shap_dens": "SHAP Critical Carrying Capacity (> 350 Nests)",
        "chart_title_b": "B. Corral Nest Density Evolution During Incubation",
        "chart_ylabel_dens": "Simultaneous Active Nests (Spatially Adjusted)",
        "chart_stl2": "Shallow Sand (ERA5 stl2: 7–28 cm)",
        "chart_stl3": "Deep Sand (ERA5 stl3: 28–100 cm)",
        "chart_tnest": "Total Nest Temperature (T_base + Metabolic Heat)",
        "chart_lethal_temp": "Lethal Thermal Threshold (33.0 °C)",
        "chart_lethal_fill": "Accumulating Lethal Thermal Damage (Degree-Hours > 33 °C)",
        "chart_title_c": "C. Anatomy of Thermal Stress: Layer-by-Layer Thermodynamic Breakdown",
        "chart_ylabel_temp": "Temperature (°C)",
        "diag_title": "Thermodynamic Diagnosis (Nest",
        "diag_atl": "• Accumulated Thermal Load (ATL_33): {atl:.1f} degree-hours > 33°C",
        "diag_tsp": "• Mean Sensitive Period Temp (TSP): {tsp:.2f} °C",
        "diag_tbase": "• Mean Abiotic Baseline Temp: {tbase:.2f} °C",
        "diag_hsr": "• Observed Survival (HSR): {hsr:.1f}% ({alive}/{total} hatchlings)",
        # Tab 2
        "macro_header": "Historical Nesting Trends & xAI Operational Rules (4,681 Nests)",
        "m_total_nests": "Total Modeled Nests",
        "m_total_eggs": "Total Eggs Incubated",
        "m_total_alive": "Live Hatchlings Released",
        "m_mean_hsr": "Mean Hatching Success (HSR)",
        "macro_table_title": "#### Seasonal Summary Statistics (with 3x Spatial Corral Correction applied to 2019)",
        "col_year": "Year",
        "col_nests": "Total Nests",
        "col_eggs": "Total Eggs",
        "col_alive": "Live Hatchlings",
        "col_hsr": "Mean HSR (%)",
        "col_tsp": "Mean TSP (°C)",
        "col_atl": "Mean ATL_33 (°C·h)",
        "col_rain": "Mean Rain (mm)",
        "col_dens": "Mean Peak Density",
        "heat_bins": ["0–50 (Optimal)", "50–200 (Mild)", "200–400 (Moderate)", "400–600 (High)", ">600 (SHAP Lethal)"],
        "macro_chart1_title": "Impact of Thermal Load (ATL_33) on Mean Survival Rate",
        "macro_chart1_ylabel": "Mean Hatching Success Rate - HSR (%)",
        "macro_chart2_title": "Historical Nesting Volume vs. Hatching Success (2018–2024)",
        "macro_chart2_ylabel1": "Number of Nests",
        "macro_chart2_ylabel2": "Mean HSR (%)",
        "macro_chart2_legend": "Incubated Nests",
        # Tab 3
        "audit_header": "🛡️ Data Governance, API Troubleshooting & Anomaly Detection",
        "audit_intro": (
            "In ecological data science, **blindly dropping outliers destroys critical biological evidence**. "
            "The master ETL pipeline (`ejecutar_pipeline_definitivo`) enforces three quality assurance layers:\n"
            "1. **ECMWF ERA5-Land Soil Layer Troubleshooting:** Conducted backward mathematical auditing of soil formulas to fix misassigned shallow (`stl2`) and deep (`stl3`) temperature variables, restoring realistic sand thermal inertia curves.\n"
            "2. **Spatial Business Rule Correction (2019 Season):** In 2019, a record **1,842 nests** were recorded and the physical corral area was tripled ($3\\times$). The pipeline scales `peak_corral_density` and `density_last_third` by `1/3.0` to prevent artificial overcrowding bias.\n"
            "3. **Biological Filter & Anomaly Segregation (`reporte_anomalias_biologos.csv`):** Nests with extreme incubation durations ($< 40\\text{ days}$ [$960\\text{ h}$] or $> 75\\text{ days}$ [$1,800\\text{ h}$]) are automatically flagged into a biologist audit report while being preserved in the dataset; only records lacking valid emergence timestamps are dropped."
        ),
        "audit_anom_title": "🔍 **Atypical Incubation Duration Nests Flagged (<40 or >75 days):**",
        "audit_null_title": "🧹 **Records Dropped Due to Missing/Invalid Emergence Date:**",
        "audit_records": "record(s)",
        "audit_clean_ok": "Processed dataset `nidos_procesados_ML_v8.csv` is 100% free of null values in critical timestamps.",
        "audit_explorer_title": "#### Processed Analytical Table Explorer (`nidos_procesados_ML_v8.csv` — Top 100 rows)"
    },
    "es": {
        "page_title": "Eco-Informática Tamul | Análisis de Supervivencia",
        "app_title": "🐢 Plataforma Eco-Informática: Supervivencia de Tortugas Marinas (Tamul)",
        "app_subtitle": (
            "**Pipeline de Ingeniería de Características, Simulación Termodinámica ERA5-Land e Inteligencia Artificial Explicativa (xAI)**  \n"
            "*Proyecto de investigación aplicada a la conservación ecológica (2018–2024) | 70,128 registros climáticos horarios y 4,681 nidos modelados.*"
        ),
        "load_error": (
            "No se pudieron cargar los archivos CSV. Asegúrate de colocar `nidos_procesados_ML_v8.csv` y "
            "`SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv` en `data/processed/` y `data/raw/` "
            "(o en la carpeta raíz). Detalle: "
        ),
        "spinner_nidos": "Cargando base de datos de anidación procesada...",
        "spinner_era5": "Cargando serie climática horaria ERA5-Land (+70,000 registros)...",
        "spinner_maestro": "Cargando bitácora maestra para auditoría de datos...",
        # Sidebar
        "sidebar_header": "🎛️ Panel de Control Eco-Informático",
        "lang_label": "🌐 Language / Idioma",
        "explore_mode_label": "Modo de Exploración:",
        "mode_archetypes": "Casos Arquetípicos de Estudio (Tesis)",
        "mode_free": "Explorador Libre por Temporada y Especie",
        "select_archetype": "Selecciona un Arquetipo Biológico:",
        "arch_1": "1. Nido Exitoso Óptimo",
        "arch_2": "2. Siniestrado por Impacto Ciclónico",
        "arch_3": "3. Siniestrado por Estrés Térmico y Densidad",
        "select_year": "Temporada (Año):",
        "select_species": "Especie:",
        "filter_status": "Filtrar por Resultado de Eclosión:",
        "status_all": "Todos los nidos",
        "status_high": "Alta Supervivencia (HSR >= 85%)",
        "status_low": "Baja Supervivencia / Siniestrados (HSR < 30%)",
        "no_nests_warn": "No hay nidos con ese criterio en esta temporada. Mostrando todos.",
        "select_nest": "Seleccionar Nido",
        "available": "disponibles",
        "compare_ref": "Comparar contra Arquetipo Exitoso en gráficas",
        "sidebar_arch": (
            "**Arquitectura de Datos:**\n"
            "• **Clima:** API ECMWF / ERA5-Land\n"
            "• **Modelado:** Cox PH, Regresión Cuasibinomial, XGBoost + SHAP\n"
            "• **Autor:** Diego Hernández Tadeo"
        ),
        # Tabs
        "tab_1": "📊 1. Simulador Termodinámico y Trilogía Biológica",
        "tab_2": "📈 2. Análisis Macro y Umbrales xAI (2018–2024)",
        "tab_3": "🛡️ 3. Auditoría y Gobernanza de Datos (Pipeline ETL)",
        # Tab 1
        "dossier_header": "Expediente Eco-Informático del Nido",
        "season": "Temporada",
        "kpi_hsr": "Tasa de Supervivencia (HSR)",
        "hatchlings": "crías",
        "kpi_duration": "Duración de Incubación",
        "days": "días",
        "total_hours": "horas totales",
        "kpi_rain": "Precipitación Acumulada",
        "rain_risk": "Riesgo Washout (>300 mm)",
        "rain_safe": "Rango Seguro (<300 mm)",
        "kpi_atl": "Carga Térmica Letal (ATL_33)",
        "atl_risk": "Estrés Letal (>600 °C·h)",
        "atl_safe": "Bajo Umbral Crítico",
        "kpi_density": "Pico Densidad en Corral",
        "nests": "nidos",
        "density_risk": "Sobrecarga (>350 nidos)",
        "density_safe": "Capacidad Óptima",
        "no_era5_warn": "No se encontraron registros horarios en ERA5 para el rango de fechas de este nido.",
        "expander_title": "🔬 Ver explicación técnica de la Fusión Física-Biológica (Ingeniería de Características)",
        "expander_body": (
            "* **Compensación de falta de sensores físicos:** Se integró la reanálisis climática de **ERA5-Land (ECMWF)** interpolando las capas de suelo superficial (`stl2_celsius`: 7–28 cm) y profunda (`stl3_celsius`: 28–100 cm) con pesos diferenciados por especie (`0.91` para *Chelonia mydas* por excavar cámaras más profundas, y `0.59` para *Caretta caretta* y *Eretmochelys imbricata*).\n"
            "* **Curva de Calor Metabólico Continuo:** Durante el último tercio de incubación ($T_3$), el metabolismo embrionario eleva la temperatura interna del nido entre $+2.5\\text{ °C}$ y $+5.0\\text{ °C}$ en función del tamaño de la nidada (`conteo_huevos`). Se aplicó una media móvil centrada de 120 horas (`rolling(window=120)`) para simular una transición biológica realista sin escalones artificiales.\n"
            "* **Carga Térmica Letal Acumulada (`ATL_33`):** Cuantifica la integral de grados-hora que el nido pasa por encima del límite biológico de tolerancia ($33.0\\text{ °C}$)."
        ),
        # Charts Trilogy
        "chart_nest_prefix": "Nido",
        "chart_ref_prefix": "Arquetipo Exitoso",
        "chart_opt_rain": "Zona Óptima de Termorregulación (50–150 mm)",
        "chart_shap_rain": "Umbral Letal SHAP (> 300 mm - Asfixia/Washout)",
        "chart_title_a": "A. Impacto Ciclónico y Paradoja Hídrica (ERA5-Land)",
        "chart_xlabel_days": "Días de Incubación",
        "chart_ylabel_rain": "Precipitación Acumulada (mm)",
        "chart_dens_ref": "Densidad",
        "chart_dens_sel": "Densidad Corral — Nido",
        "chart_shap_dens": "Capacidad de Carga Crítica SHAP (> 350 Nidos)",
        "chart_title_b": "B. Evolución de la Densidad del Corral durante la Incubación",
        "chart_ylabel_dens": "Nidos Activos Simultáneos (Ajustado)",
        "chart_stl2": "Arena Superficial (ERA5 stl2: 7–28 cm)",
        "chart_stl3": "Arena Profunda (ERA5 stl3: 28–100 cm)",
        "chart_tnest": "Temperatura Total del Nido (T_base + Calor Metabólico)",
        "chart_lethal_temp": "Umbral Térmico Letal (33.0 °C)",
        "chart_lethal_fill": "Acumulación de Daño Térmico Letal (Grados-Hora > 33 °C)",
        "chart_title_c": "C. Anatomía del Estrés Térmico: Desglose Termodinámico de Capas",
        "chart_ylabel_temp": "Temperatura (°C)",
        "diag_title": "Diagnóstico Termodinámico (Nido",
        "diag_atl": "• Carga Térmica Acumulada (ATL_33): {atl:.1f} grados-hora > 33°C",
        "diag_tsp": "• Temp. Media Periodo Sensible (TSP): {tsp:.2f} °C",
        "diag_tbase": "• Temp. Base Abiótica Media: {tbase:.2f} °C",
        "diag_hsr": "• Supervivencia Real (HSR): {hsr:.1f}% ({alive}/{total} crías)",
        # Tab 2
        "macro_header": "Tendencias Históricas de Anidación y Reglas Operativas xAI (4,681 Nidos)",
        "m_total_nests": "Total Nidos Procesados",
        "m_total_eggs": "Total Huevos Sembrados",
        "m_total_alive": "Total Crías Vivas Liberadas",
        "m_mean_hsr": "Tasa Media de Eclosión (HSR)",
        "macro_table_title": "#### Resumen Estadístico por Temporada (con Corrección Espacial 3x aplicada en 2019)",
        "col_year": "Año",
        "col_nests": "Total Nidos",
        "col_eggs": "Huevos Totales",
        "col_alive": "Crías Vivas",
        "col_hsr": "HSR Promedio (%)",
        "col_tsp": "Temp. TSP Media (°C)",
        "col_atl": "ATL_33 Promedio (°C·h)",
        "col_rain": "Lluvia Media (mm)",
        "col_dens": "Pico Densidad Medio",
        "heat_bins": ["0–50 (Óptimo)", "50–200 (Leve)", "200–400 (Moderado)", "400–600 (Alto)", ">600 (Letal SHAP)"],
        "macro_chart1_title": "Impacto de la Carga Térmica (ATL_33) en la Supervivencia Media",
        "macro_chart1_ylabel": "Tasa de Supervivencia Media - HSR (%)",
        "macro_chart2_title": "Volumen Histórico de Anidación vs. Éxito de Eclosión (2018–2024)",
        "macro_chart2_ylabel1": "Número de Nidos",
        "macro_chart2_ylabel2": "HSR Promedio (%)",
        "macro_chart2_legend": "Nidos Sembrados",
        # Tab 3
        "audit_header": "🛡️ Gobernanza de Datos, Troubleshooting de API y Detección de Anomalías",
        "audit_intro": (
            "En proyectos de ciencia de datos aplicada a biología, **eliminar registros atípicos a ciegas destruye evidencia ecológica valiosa**. "
            "El pipeline maestro (`ejecutar_pipeline_definitivo`) implementa tres capas de validación y aseguramiento de calidad:\n"
            "1. **Troubleshooting de Fórmulas y Capas de Suelo (ERA5-Land):** Auditoría matemática hacia atrás para corregir la asignación de las capas térmicas superficial (`stl2`) y profunda (`stl3`), garantizando que las curvas reflejen la inercia térmica real de la arena.\n"
            "2. **Corrección Espacial de Negocio (Temporada 2019):** En 2019 se registró una temporada récord de **1,842 nidos** y el área física del corral se triplicó ($3\\times$). El algoritmo divide las métricas `peak_corral_density` y `density_last_third` entre `3.0` para evitar sesgos de falso hacinamiento.\n"
            "3. **Filtro Biológico y Segregación de Anomalías (`reporte_anomalias_biologos.csv`):** Los nidos con duraciones biológicamente extremas ($< 40\\text{ días}$ [$960\\text{ h}$] o $> 75\\text{ días}$ [$1,800\\text{ h}$]) se separan automáticamente en un reporte de auditoría para los biólogos sin descartarse arbitrariamente, filtrando únicamente registros con fechas de emergencia nulas."
        ),
        "audit_anom_title": "🔍 **Nidos con Duración Atípica Detectados (<40 o >75 días):**",
        "audit_null_title": "🧹 **Registros Descartados por Fecha de Emergencia Inválida/Nula:**",
        "audit_records": "registro(s)",
        "audit_clean_ok": "El dataset procesado `nidos_procesados_ML_v8.csv` se encuentra 100% libre de valores nulos en fechas críticas.",
        "audit_explorer_title": "#### Explorador de la Tabla Analítica Procesada (`nidos_procesados_ML_v8.csv` — Primeras 100 filas)"
    }
}


def get_texts(lang_code: str) -> dict:
    """Returns the dictionary of UI strings for 'en' or 'es'."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])
