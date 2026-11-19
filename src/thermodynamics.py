#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vectorized thermodynamic simulation of sand soil layers (ERA5-Land stl2/stl3),
embryonic metabolic heating, and spatial corral density calculation.
"""

import numpy as np
import pandas as pd
from src.config import (
    THRESHOLD_TEMP_LETHAL,
    CORRAL_CORRECTION_YEAR,
    CORRAL_CORRECTION_FACTOR,
    WEIGHT_STL3_CHELONIA_MYDAS,
    WEIGHT_STL3_DEFAULT,
)


def extract_nest_timeseries(
    nest: pd.Series,
    df_climate: pd.DataFrame,
    df_all_nests: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reconstructs hourly nest temperature dynamics and daily corral nest density
    using vectorized NumPy broadcasting.
    """
    t_siembra = nest["fecha_siembra_calc"]
    t_emergencia = nest["fecha_emergencia_calc"]

    df_total = df_climate.loc[
        (df_climate.index >= t_siembra) & (df_climate.index <= t_emergencia)
    ].copy()
    if df_total.empty:
        return pd.DataFrame(), pd.DataFrame()

    df_total["horas_transcurridas"] = (
        df_total.index - t_siembra
    ).total_seconds() / 3600.0
    df_total["dias_incubacion"] = df_total["horas_transcurridas"] / 24.0

    d_total_horas = (t_emergencia - t_siembra).total_seconds() / 3600.0
    t1_fin = t_siembra + pd.Timedelta(hours=d_total_horas / 3.0)
    t2_fin = t_siembra + pd.Timedelta(hours=2.0 * d_total_horas / 3.0)

    # Species-weighted soil depth interpolation
    especie = nest.get("especie_full", "Chelonia mydas")
    peso_stl3 = (
        WEIGHT_STL3_CHELONIA_MYDAS
        if especie == "Chelonia mydas"
        else WEIGHT_STL3_DEFAULT
    )
    df_total["T_base"] = df_total["stl2_celsius"] + peso_stl3 * (
        df_total["stl3_celsius"] - df_total["stl2_celsius"]
    )

    # Embryonic metabolic heating with 5-day (120h) centered rolling smoothing
    conteo_huevos = nest.get("conteo_huevos", 100)
    factor_metabolico_t3 = np.clip(
        2.5 + ((conteo_huevos - 50.0) / 100.0) * 2.5, 2.5, 5.0
    )

    df_total["calor_crudo"] = 0.0
    df_total.loc[df_total.index < t1_fin, "calor_crudo"] = factor_metabolico_t3 * 0.05
    df_total.loc[
        (df_total.index >= t1_fin) & (df_total.index < t2_fin), "calor_crudo"
    ] = (factor_metabolico_t3 * 0.15)
    df_total.loc[df_total.index >= t2_fin, "calor_crudo"] = factor_metabolico_t3

    df_total["calor_metabolico"] = (
        df_total["calor_crudo"].rolling(window=120, min_periods=1, center=True).mean()
    )
    df_total["T_nest"] = df_total["T_base"] + df_total["calor_metabolico"]
    df_total["lluvia_acumulada"] = df_total["tp_mm"].cumsum()
    df_total["ATL_incremental"] = np.where(
        df_total["T_nest"] > THRESHOLD_TEMP_LETHAL,
        df_total["T_nest"] - THRESHOLD_TEMP_LETHAL,
        0.0,
    )
    df_total["ATL_acumulado"] = df_total["ATL_incremental"].cumsum()

    # Vectorized daily corral density calculation
    df_diario = df_total.resample("D").first().copy()
    fechas_val = df_diario.index.values[:, None]
    siembras_val = df_all_nests["fecha_siembra_calc"].values[None, :]
    emergencias_val = df_all_nests["fecha_emergencia_calc"].values[None, :]

    activas = (
        (siembras_val <= fechas_val) & (emergencias_val >= fechas_val)
    ).sum(axis=1).astype(float)

    if int(nest["year"]) == CORRAL_CORRECTION_YEAR:
        activas = activas / CORRAL_CORRECTION_FACTOR

    df_diario["densidad_activa"] = activas
    return df_total, df_diario


def get_archetypal_nests(df_nests: pd.DataFrame) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Selects the three real-world thesis archetypal nests from the dataset."""
    exitoso = df_nests[
        (df_nests["HSR"] > 0.95)
        & (df_nests["precipitacion_total_mm"] < 150)
        & (df_nests["ATL_33"] < 50)
    ].iloc[0]

    lluvia = df_nests[
        (df_nests["HSR"] < 0.1) & (df_nests["precipitacion_total_mm"] > 300)
    ].iloc[0]

    calor = df_nests[
        (df_nests["HSR"] < 0.1) & (df_nests["ATL_33"] > 600)
    ].iloc[0]

    return exitoso, lluvia, calor
