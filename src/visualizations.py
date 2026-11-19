#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bilingual Matplotlib visualization builders for the Biological Trilogy
and Macro Historical Trends.
"""

import pandas as pd
import matplotlib.pyplot as plt
from src.config import (
    THRESHOLD_RAIN_OPTIMAL_MIN,
    THRESHOLD_RAIN_OPTIMAL_MAX,
    THRESHOLD_RAIN_LETHAL_SHAP,
    THRESHOLD_TEMP_LETHAL,
    THRESHOLD_CORRAL_DENSITY_SHAP,
)


def plot_biological_trilogy(
    nido_sel: pd.Series,
    clima_sel: pd.DataFrame,
    diario_sel: pd.DataFrame,
    nido_ref: pd.Series,
    clima_ref: pd.DataFrame,
    diario_ref: pd.DataFrame,
    t: dict,
    show_ref: bool = True,
):
    """Generates the 3-panel Biological Trilogy chart in the selected language."""
    fig = plt.figure(figsize=(18, 11), dpi=130)
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.25], hspace=0.32, wspace=0.22)

    res_sel = (
        f"{t['chart_nest_prefix']} {nido_sel['nido_uid']} ({int(nido_sel['year'])}) "
        f"| HSR: {nido_sel['HSR']*100:.1f}%"
    )
    res_ref = (
        f"{t['chart_ref_prefix']} {nido_ref['nido_uid']} "
        f"| HSR: {nido_ref['HSR']*100:.1f}%"
    )

    # PANEL A: CYCLONIC IMPACT (CUMULATIVE RAINFALL)
    ax1 = fig.add_subplot(gs[0, 0])
    if show_ref and nido_sel["nido_uid"] != nido_ref["nido_uid"]:
        ax1.plot(
            diario_ref["dias_incubacion"],
            diario_ref["lluvia_acumulada"],
            color="#2980b9",
            linewidth=2.2,
            linestyle="--",
            alpha=0.8,
            label=res_ref,
        )
    ax1.plot(
        diario_sel["dias_incubacion"],
        diario_sel["lluvia_acumulada"],
        color="#8e44ad",
        linewidth=3,
        label=res_sel,
    )
    ax1.axhspan(
        THRESHOLD_RAIN_OPTIMAL_MIN,
        THRESHOLD_RAIN_OPTIMAL_MAX,
        color="#3498db",
        alpha=0.15,
        label=t["chart_opt_rain"],
    )
    ax1.axhline(
        THRESHOLD_RAIN_LETHAL_SHAP, color="#c0392b", linestyle="--", linewidth=2
    )
    ax1.text(
        1.5,
        THRESHOLD_RAIN_LETHAL_SHAP + 12,
        t["chart_shap_rain"],
        color="#c0392b",
        fontweight="bold",
        fontsize=9.5,
    )
    ax1.set_title(t["chart_title_a"], fontsize=12.5, fontweight="bold")
    ax1.set_xlabel(t["chart_xlabel_days"], fontweight="bold")
    ax1.set_ylabel(t["chart_ylabel_rain"], fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=8.5)

    # PANEL B: CORRAL DENSITY / OVERCROWDING
    ax2 = fig.add_subplot(gs[0, 1])
    if show_ref and nido_sel["nido_uid"] != nido_ref["nido_uid"]:
        ax2.plot(
            diario_ref["dias_incubacion"],
            diario_ref["densidad_activa"],
            color="#27ae60",
            linewidth=2.2,
            linestyle="--",
            alpha=0.8,
            label=f"{t['chart_dens_ref']} {nido_ref['nido_uid']} (Ref.)",
        )
    ax2.plot(
        diario_sel["dias_incubacion"],
        diario_sel["densidad_activa"],
        color="#d35400",
        linewidth=3,
        label=f"{t['chart_dens_sel']} {nido_sel['nido_uid']}",
    )
    ax2.axhline(
        THRESHOLD_CORRAL_DENSITY_SHAP, color="#c0392b", linestyle="--", linewidth=2
    )
    ax2.text(
        1.5,
        THRESHOLD_CORRAL_DENSITY_SHAP + 10,
        t["chart_shap_dens"],
        color="#c0392b",
        fontweight="bold",
        fontsize=9.5,
    )
    ax2.set_title(t["chart_title_b"], fontsize=12.5, fontweight="bold")
    ax2.set_xlabel(t["chart_xlabel_days"], fontweight="bold")
    ax2.set_ylabel(t["chart_ylabel_dens"], fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=8.5)

    # PANEL C: ANATOMY OF THERMAL STRESS
    ax3 = fig.add_subplot(gs[1, :])
    stl2_suave = clima_sel["stl2_celsius"].rolling(6, min_periods=1).mean()
    stl3_suave = clima_sel["stl3_celsius"].rolling(6, min_periods=1).mean()
    tnest_suave = clima_sel["T_nest"].rolling(6, min_periods=1).mean()

    ax3.plot(
        clima_sel["dias_incubacion"],
        stl2_suave,
        color="#3498db",
        linewidth=1.5,
        linestyle=":",
        label=t["chart_stl2"],
    )
    ax3.plot(
        clima_sel["dias_incubacion"],
        stl3_suave,
        color="#e67e22",
        linewidth=1.5,
        linestyle="-.",
        label=t["chart_stl3"],
    )
    ax3.plot(
        clima_sel["dias_incubacion"],
        tnest_suave,
        color="#c0392b",
        linewidth=2.8,
        label=t["chart_tnest"],
    )
    ax3.axhline(
        THRESHOLD_TEMP_LETHAL,
        color="black",
        linestyle="--",
        linewidth=2,
        label=t["chart_lethal_temp"],
    )
    ax3.fill_between(
        clima_sel["dias_incubacion"],
        tnest_suave,
        THRESHOLD_TEMP_LETHAL,
        where=(tnest_suave > THRESHOLD_TEMP_LETHAL),
        color="#e74c3c",
        alpha=0.45,
        label=t["chart_lethal_fill"],
    )

    atl_val = nido_sel["ATL_33"]
    dias_val = nido_sel["D_horas"] / 24.0
    ax3.set_title(
        f"{t['chart_title_c']} "
        f"({t['chart_nest_prefix']} {nido_sel['nido_uid']} | {nido_sel['especie_full']} "
        f"| ATL_33: {atl_val:.1f} °C·h | {dias_val:.1f} {t['days']})",
        fontsize=13,
        fontweight="bold",
    )
    ax3.set_xlabel(t["chart_xlabel_days"], fontsize=11.5, fontweight="bold")
    ax3.set_ylabel(t["chart_ylabel_temp"], fontsize=11.5, fontweight="bold")
    ax3.grid(True, linestyle=":", alpha=0.5)

    texto_biologia = "\n".join(
        [
            f"{t['diag_title']} {nido_sel['nido_uid']}):",
            t["diag_atl"].format(atl=atl_val),
            t["diag_tsp"].format(tsp=nido_sel["TSP_mean"]),
            t["diag_tbase"].format(tbase=nido_sel["T_base_mean"]),
            t["diag_hsr"].format(
                hsr=nido_sel["HSR"] * 100.0,
                alive=int(nido_sel["crias_vivas"]),
                total=int(nido_sel["conteo_huevos"]),
            ),
        ]
    )

    y_max = max(tnest_suave.max(), 34.5)
    ax3.set_ylim(bottom=min(stl2_suave.min() - 0.8, 25.0), top=y_max + 1.2)
    ax3.text(
        1.0,
        y_max - 0.1,
        texto_biologia,
        fontsize=9.8,
        verticalalignment="top",
        bbox=dict(
            facecolor="white",
            alpha=0.9,
            edgecolor="#c0392b",
            boxstyle="round,pad=0.5",
        ),
    )
    ax3.legend(loc="lower right", ncol=2, fontsize=9)

    plt.tight_layout()
    return fig


def plot_macro_trends(df_nidos: pd.DataFrame, resumen_anual: pd.DataFrame, t: dict):
    """Generates the 2-panel Macro Trends & SHAP Thermal Impact figure."""
    fig_macro, (ax_m1, ax_m2) = plt.subplots(1, 2, figsize=(16, 5.2), dpi=120)

    # Subpanel 1: Mean HSR across ATL_33 bins
    bins_calor = [-1, 50, 200, 400, 600, 2000]
    df_temp = df_nidos.copy()
    df_temp["rango_calor"] = pd.cut(
        df_temp["ATL_33"], bins=bins_calor, labels=t["heat_bins"]
    )
    calor_group = df_temp.groupby("rango_calor", observed=False)["HSR"].mean() * 100.0

    barras1 = ax_m1.bar(
        calor_group.index.astype(str),
        calor_group.values,
        color=["#27ae60", "#2ecc71", "#f39c12", "#e67e22", "#c0392b"],
    )
    ax_m1.set_title(t["macro_chart1_title"], fontweight="bold")
    ax_m1.set_ylabel(t["macro_chart1_ylabel"])
    ax_m1.set_ylim(0, 105)
    ax_m1.tick_params(axis="x", rotation=15)
    for b in barras1:
        ax_m1.text(
            b.get_x() + b.get_width() / 2.0,
            b.get_height() + 1.5,
            f"{b.get_height():.1f}%",
            ha="center",
            fontweight="bold",
        )

    # Subpanel 2: Historical nesting volume vs mean HSR
    ax_m2_twin = ax_m2.twinx()
    ax_m2.bar(
        resumen_anual["year"].astype(str),
        resumen_anual["Total_Nidos"],
        color="#3498db",
        alpha=0.65,
        label=t["macro_chart2_legend"],
    )
    ax_m2_twin.plot(
        resumen_anual["year"].astype(str),
        resumen_anual["HSR_Promedio"],
        color="#c0392b",
        marker="o",
        linewidth=2.5,
        label=t["macro_chart2_ylabel2"],
    )
    ax_m2.set_title(t["macro_chart2_title"], fontweight="bold")
    ax_m2.set_ylabel(t["macro_chart2_ylabel1"], color="#2980b9", fontweight="bold")
    ax_m2_twin.set_ylabel(t["macro_chart2_ylabel2"], color="#c0392b", fontweight="bold")
    ax_m2_twin.set_ylim(50, 100)

    plt.tight_layout()
    return fig_macro
