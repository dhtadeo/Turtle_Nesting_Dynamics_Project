#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration, file paths, and SHAP/biological thresholds for the Tamul Eco-Informatics platform.
"""

import os

# File names (kept untouched as requested)
FILE_PROCESSED_V8 = "nidos_procesados_ML_v8.csv"
FILE_PROCESSED_V7 = "nidos_procesados_ML_v7_FINAL.csv"
FILE_ERA5 = "SERIE_MAESTRA_TAMUL_2018_2025_LOCAL.csv"
FILE_MAESTRO = "anidaciones_tamul_2018_2024_maestro.csv"

# xAI / SHAP & Biological Thresholds
THRESHOLD_RAIN_OPTIMAL_MIN = 50.0     # mm
THRESHOLD_RAIN_OPTIMAL_MAX = 150.0    # mm
THRESHOLD_RAIN_LETHAL_SHAP = 300.0    # mm (Washout / Asphyxiation)
THRESHOLD_TEMP_LETHAL = 33.0          # °C (Embryonic thermal tolerance limit)
THRESHOLD_ATL_LETHAL_SHAP = 600.0     # °C·h (>33°C cumulative thermal load)
THRESHOLD_CORRAL_DENSITY_SHAP = 350.0 # Active simultaneous nests

# Biological duration audit bounds (hours)
MIN_INCUBATION_HOURS = 960.0          # 40 days
MAX_INCUBATION_HOURS = 1800.0         # 75 days

# Spatial correction factor for 2019 (3x corral expansion)
CORRAL_CORRECTION_YEAR = 2019
CORRAL_CORRECTION_FACTOR = 3.0

# Soil depth interpolation weights (ERA5-Land stl2 & stl3)
WEIGHT_STL3_CHELONIA_MYDAS = 0.91
WEIGHT_STL3_DEFAULT = 0.59


def resolve_data_path(filename: str, subfolder: str = "processed") -> str:
    """Resolves file paths across modular GitHub folders or root directory."""
    candidates = [
        os.path.join("data", subfolder, filename),
        os.path.join("data", "raw", filename),
        os.path.join("data", "processed", filename),
        os.path.join("datos", filename),
        filename,
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return os.path.join("data", subfolder, filename)
