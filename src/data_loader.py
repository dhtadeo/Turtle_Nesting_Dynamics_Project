#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cached data loading utilities for processed nesting datasets, ERA5-Land climate
time series, and raw camp logbooks.
"""

import os
import pandas as pd
import streamlit as st
from src.config import (
    FILE_PROCESSED_V8,
    FILE_PROCESSED_V7,
    FILE_ERA5,
    FILE_MAESTRO,
    resolve_data_path,
)


@st.cache_data(show_spinner=False)
def load_processed_nests() -> pd.DataFrame:
    """Loads the cleaned and feature-engineered nesting dataset."""
    path = resolve_data_path(FILE_PROCESSED_V8, "processed")
    if not os.path.exists(path):
        path = resolve_data_path(FILE_PROCESSED_V7, "processed")

    df = pd.read_csv(path)
    df["fecha_siembra_calc"] = pd.to_datetime(df["fecha_siembra_calc"])
    df["fecha_emergencia_calc"] = pd.to_datetime(df["fecha_emergencia_calc"])

    if "ATC_33" in df.columns and "ATL_33" not in df.columns:
        df["ATL_33"] = df["ATC_33"]
    return df


@st.cache_data(show_spinner=False)
def load_era5_series() -> pd.DataFrame:
    """Loads the 2018-2025 hourly ERA5-Land climate series indexed by local time."""
    path = resolve_data_path(FILE_ERA5, "raw")
    df = pd.read_csv(path)
    df["time_local"] = pd.to_datetime(df["time_local"])
    df.set_index("time_local", inplace=True)
    return df


@st.cache_data(show_spinner=False)
def load_raw_master_logbook():
    """Loads the raw nesting master CSV to audit dropped records dynamically."""
    path = resolve_data_path(FILE_MAESTRO, "raw")
    if not os.path.exists(path):
        return None

    df = pd.read_csv(path)
    df["fecha_siembra_calc"] = pd.to_datetime(
        df["fecha_recolecta"].astype(str) + " " + df["hora_siembra"].astype(str),
        errors="coerce",
    )
    df["fecha_emergencia_calc"] = pd.to_datetime(
        df["fecha_emergencia"].astype(str) + " 20:00:00",
        errors="coerce",
    )
    df["D_horas_bruto"] = (
        df["fecha_emergencia_calc"] - df["fecha_siembra_calc"]
    ).dt.total_seconds() / 3600.0
    return df
