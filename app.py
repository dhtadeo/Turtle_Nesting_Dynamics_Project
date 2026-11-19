#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================================
ECO-INFORMATICS PLATFORM: SEA TURTLE NESTING & SURVIVAL ANALYTICS (TAMUL)
Author: Diego Hernández Tadeo
Entry Point: Streamlit UI & Multilingual Routing Orchestrator (EN default / ES)
================================================================================
"""

import streamlit as st
from src.config import (
    THRESHOLD_RAIN_LETHAL_SHAP,
    THRESHOLD_ATL_LETHAL_SHAP,
    THRESHOLD_CORRAL_DENSITY_SHAP,
    MIN_INCUBATION_HOURS,
    MAX_INCUBATION_HOURS,
)
from src.translations import get_texts
from src.data_loader import (
    load_processed_nests,
    load_era5_series,
    load_raw_master_logbook,
)
from src.thermodynamics import extract_nest_timeseries, get_archetypal_nests
from src.visualizations import plot_biological_trilogy, plot_macro_trends

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Tamul Eco-Informatics | Sea Turtle Survival Analytics",
    page_icon="🐢",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    # --------------------------------------------------------------------------
    # LANGUAGE SWITCHER (ENGLISH DEFAULT)
    # --------------------------------------------------------------------------
    st.sidebar.header("🎛️ Control Panel / Panel")
    lang_choice = st.sidebar.radio(
        "🌐 Language / Idioma",
        options=["English", "Español"],
        index=0,
        horizontal=True,
    )
    lang_code = "en" if lang_choice == "English" else "es"
    t = get_texts(lang_code)

    # --------------------------------------------------------------------------
    # HEADER
    # --------------------------------------------------------------------------
    st.title(t["app_title"])
    st.markdown(t["app_subtitle"])

    # --------------------------------------------------------------------------
    # DATA LOADING
    # --------------------------------------------------------------------------
    try:
        with st.spinner(t["spinner_nidos"]):
            df_nidos = load_processed_nests()
        with st.spinner(t["spinner_era5"]):
            df_era5 = load_era5_series()
        with st.spinner(t["spinner_maestro"]):
            df_maestro = load_raw_master_logbook()
    except Exception as e:
        st.error(f"{t['load_error']} {e}")
        st.stop()

    arquetipo_exitoso, arquetipo_lluvia, arquetipo_calor = get_archetypal_nests(df_nidos)

    # --------------------------------------------------------------------------
    # SIDEBAR FILTERS
    # --------------------------------------------------------------------------
    st.sidebar.markdown("---")
    modo_seleccion = st.sidebar.radio(
        t["explore_mode_label"],
        [t["mode_archetypes"], t["mode_free"]],
    )

    if modo_seleccion == t["mode_archetypes"]:
        caso = st.sidebar.selectbox(
            t["select_archetype"],
            [
                f"{t['arch_1']} ({arquetipo_exitoso['nido_uid']} - {int(arquetipo_exitoso['year'])})",
                f"{t['arch_2']} ({arquetipo_lluvia['nido_uid']} - {int(arquetipo_lluvia['year'])})",
                f"{t['arch_3']} ({arquetipo_calor['nido_uid']} - {int(arquetipo_calor['year'])})",
            ],
        )
        if caso.startswith("1."):
            nido_seleccionado = arquetipo_exitoso
        elif caso.startswith("2."):
            nido_seleccionado = arquetipo_lluvia
        else:
            nido_seleccionado = arquetipo_calor
    else:
        anios_disp = sorted(df_nidos["year"].unique())
        anio_sel = st.sidebar.selectbox(t["select_year"], anios_disp, index=1)

        df_filtrado_anio = df_nidos[df_nidos["year"] == anio_sel]
        especies_disp = sorted(df_filtrado_anio["especie_full"].dropna().unique())
        especie_sel = st.sidebar.selectbox(t["select_species"], especies_disp)

        df_filtrado_esp = df_filtrado_anio[
            df_filtrado_anio["especie_full"] == especie_sel
        ]

        filtro_estado = st.sidebar.selectbox(
            t["filter_status"],
            [t["status_all"], t["status_high"], t["status_low"]],
        )
        if filtro_estado == t["status_high"]:
            df_filtrado_esp = df_filtrado_esp[df_filtrado_esp["HSR"] >= 0.85]
        elif filtro_estado == t["status_low"]:
            df_filtrado_esp = df_filtrado_esp[df_filtrado_esp["HSR"] < 0.30]

        if df_filtrado_esp.empty:
            st.sidebar.warning(t["no_nests_warn"])
            df_filtrado_esp = df_filtrado_anio

        opciones_nidos = df_filtrado_esp["nido_uid"].tolist()
        uid_sel = st.sidebar.selectbox(
            f"{t['select_nest']} ({len(opciones_nidos)} {t['available']}):",
            opciones_nidos,
        )
        nido_seleccionado = df_filtrado_esp[
            df_filtrado_esp["nido_uid"] == uid_sel
        ].iloc[0]

    mostrar_comparativa = st.sidebar.checkbox(t["compare_ref"], value=True)

    st.sidebar.markdown("---")
    st.sidebar.caption(t["sidebar_arch"])

    # --------------------------------------------------------------------------
    # MAIN TABS
    # --------------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs([t["tab_1"], t["tab_2"], t["tab_3"]])

    # ==========================================================================
    # TAB 1: THERMODYNAMIC SIMULATOR & BIOLOGICAL TRILOGY
    # ==========================================================================
    with tab1:
        st.subheader(
            f"{t['dossier_header']} `{nido_seleccionado['nido_uid']}` "
            f"— *{nido_seleccionado['especie_full']}* ({t['season']} {int(nido_seleccionado['year'])})"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        hsr_pct = nido_seleccionado["HSR"] * 100.0
        lluvia_val = nido_seleccionado["precipitacion_total_mm"]
        atl_val = nido_seleccionado["ATL_33"]
        dens_val = nido_seleccionado["peak_corral_density"]
        dias_inc = nido_seleccionado["D_horas"] / 24.0

        col1.metric(
            t["kpi_hsr"],
            f"{hsr_pct:.1f}%",
            f"{int(nido_seleccionado['crias_vivas'])} / {int(nido_seleccionado['conteo_huevos'])} {t['hatchlings']}",
        )
        col2.metric(
            t["kpi_duration"],
            f"{dias_inc:.1f} {t['days']}",
            f"{nido_seleccionado['D_horas']:.0f} {t['total_hours']}",
        )
        col3.metric(
            t["kpi_rain"],
            f"{lluvia_val:.1f} mm",
            t["rain_risk"] if lluvia_val > THRESHOLD_RAIN_LETHAL_SHAP else t["rain_safe"],
            delta_color="inverse" if lluvia_val > THRESHOLD_RAIN_LETHAL_SHAP else "normal",
        )
        col4.metric(
            t["kpi_atl"],
            f"{atl_val:.1f} °C·h",
            t["atl_risk"] if atl_val > THRESHOLD_ATL_LETHAL_SHAP else t["atl_safe"],
            delta_color="inverse" if atl_val > THRESHOLD_ATL_LETHAL_SHAP else "normal",
        )
        col5.metric(
            t["kpi_density"],
            f"{dens_val:.0f} {t['nests']}",
            t["density_risk"] if dens_val > THRESHOLD_CORRAL_DENSITY_SHAP else t["density_safe"],
            delta_color="inverse" if dens_val > THRESHOLD_CORRAL_DENSITY_SHAP else "normal",
        )

        clima_sel, diario_sel = extract_nest_timeseries(
            nido_seleccionado, df_era5, df_nidos
        )
        clima_ref, diario_ref = extract_nest_timeseries(
            arquetipo_exitoso, df_era5, df_nidos
        )

        if clima_sel.empty:
            st.warning(t["no_era5_warn"])
        else:
            fig_trilogia = plot_biological_trilogy(
                nido_seleccionado,
                clima_sel,
                diario_sel,
                arquetipo_exitoso,
                clima_ref,
                diario_ref,
                t=t,
                show_ref=mostrar_comparativa,
            )
            st.pyplot(fig_trilogia)

            with st.expander(t["expander_title"]):
                st.markdown(t["expander_body"])

    # ==========================================================================
    # TAB 2: MACRO TRENDS & xAI THRESHOLDS
    # ==========================================================================
    with tab2:
        st.subheader(t["macro_header"])

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric(t["m_total_nests"], f"{len(df_nidos):,}")
        col_m2.metric(t["m_total_eggs"], f"{int(df_nidos['conteo_huevos'].sum()):,}")
        col_m3.metric(t["m_total_alive"], f"{int(df_nidos['crias_vivas'].sum()):,}")
        col_m4.metric(t["m_mean_hsr"], f"{df_nidos['HSR'].mean()*100:.1f}%")

        resumen_anual = (
            df_nidos.groupby("year")
            .agg(
                Total_Nidos=("nido_uid", "count"),
                Huevos_Totales=("conteo_huevos", "sum"),
                Crias_Vivas=("crias_vivas", "sum"),
                HSR_Promedio=("HSR", lambda x: round(x.mean() * 100, 2)),
                Temp_TSP_Media=("TSP_mean", lambda x: round(x.mean(), 2)),
                ATL_33_Promedio=("ATL_33", lambda x: round(x.mean(), 1)),
                Lluvia_Media_mm=("precipitacion_total_mm", lambda x: round(x.mean(), 1)),
                Pico_Densidad_Medio=("peak_corral_density", lambda x: round(x.mean(), 1)),
            )
            .reset_index()
        )

        resumen_display = resumen_anual.rename(
            columns={
                "year": t["col_year"],
                "Total_Nidos": t["col_nests"],
                "Huevos_Totales": t["col_eggs"],
                "Crias_Vivas": t["col_alive"],
                "HSR_Promedio": t["col_hsr"],
                "Temp_TSP_Media": t["col_tsp"],
                "ATL_33_Promedio": t["col_atl"],
                "Lluvia_Media_mm": t["col_rain"],
                "Pico_Densidad_Medio": t["col_dens"],
            }
        )

        st.markdown(t["macro_table_title"])
        st.dataframe(resumen_display, use_container_width=True, hide_index=True)

        fig_macro = plot_macro_trends(df_nidos, resumen_anual, t=t)
        st.pyplot(fig_macro)

    # ==========================================================================
    # TAB 3: DATA GOVERNANCE & ETL AUDIT
    # ==========================================================================
    with tab3:
        st.subheader(t["audit_header"])
        st.markdown(t["audit_intro"])

        nidos_anomalos = df_nidos[
            (df_nidos["D_horas"] < MIN_INCUBATION_HOURS)
            | (df_nidos["D_horas"] > MAX_INCUBATION_HOURS)
        ].copy()
        nidos_anomalos["Dias_Calculados"] = (nidos_anomalos["D_horas"] / 24.0).round(2)

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.info(f"{t['audit_anom_title']} `{len(nidos_anomalos)}` {t['audit_records']}")
            st.dataframe(
                nidos_anomalos[
                    [
                        "nido_uid",
                        "year",
                        "especie_full",
                        "fecha_siembra_calc",
                        "fecha_emergencia_calc",
                        "D_horas",
                        "Dias_Calculados",
                        "HSR",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

        with col_a2:
            if df_maestro is not None:
                nulos_emergencia = df_maestro[
                    df_maestro["fecha_emergencia_calc"].isna()
                ]
                st.warning(
                    f"{t['audit_null_title']} `{len(nulos_emergencia)}` {t['audit_records']}"
                )
                st.dataframe(
                    nulos_emergencia[
                        [
                            "id_nido",
                            "year",
                            "especie",
                            "fecha_recolecta",
                            "hora_siembra",
                            "fecha_emergencia",
                            "huevos_sembrados",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.success(t["audit_clean_ok"])

        st.markdown(t["audit_explorer_title"])
        st.dataframe(df_nidos.head(100), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
