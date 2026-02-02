import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURACIÓN ÚNICA DE LA PÁGINA ---
st.set_page_config(
    page_title="RCL Scout Group - Scouting 2026", 
    layout="wide",
    page_icon="⚽"
)

# --- 2. FUNCIONES DE CARGA (LOAD DATA) ---
@st.cache_data
def load_df():
    # Busca el archivo en la carpeta data o raíz
    for ruta in ["data/df.csv", "df.csv"]:
        if os.path.exists(ruta):
            return pd.read_csv(ruta)
    return None

def get_team_logos():
    return {
        "Benferri Cf": "logos/Benferri Cf.png",
        "Betis Florida": "logos/Betis Florida.png",
        "Cd El Campello": "logos/Cd El Campello.png",
        "Cd Montesinos": "logos/Cd Montesinos.png",
        "Catral Castrum Cf": "logos/Catral Castrum Cf.png",
        "Muro Cf": "logos/Muro Cf.png",
        "Santa Pola Cf": "logos/Santa Pola Cf.png",
        "Teulada Moraira": "logos/Teulada Moraira.png",
        "Atletico Algorfa": "logos/Atletico Algorfa.png",
        "Villena Cf": "logos/Villena Cf.png",
        "Cd Almoradi": "logos/Cd Almoradi.png",
        "Novelda Cf": "logos/Novelda Cf.png",
        "Cd Murada": "logos/Cd Murada.png",
        "Atletico Jonense": "logos/Atletico Jonense.png",
        "Callosa Deportiva": "logos/Callosa Deportiva.png",
        "Cd Contestano": "logos/Cd Contestano.png",
    }

# --- 3. INTERFAZ: SELECTOR DE EQUIPOS (CON KEY ÚNICA E ÍNDICE) ---
def team_selector(team_logos, cols=4):
    if "equipo_seleccionado" not in st.session_state:
        st.session_state.equipo_seleccionado = None

    st.markdown("### 🏟️ Selecciona un equipo")
    teams = list(team_logos.keys())
    columns = st.columns(cols)

    for i, team in enumerate(teams):
        col_idx = i % cols
        with columns[col_idx]:
            try:
                st.image(team_logos[team], use_container_width=True)
            except:
                st.caption(f"📍 {team}")
            
            # Key única con índice para evitar el error DuplicateElementKey
            if st.button(team, key=f"btn_{team}_{i}", use_container_width=True):
                st.session_state.equipo_seleccionado = team
                st.rerun()

    return st.session_state.equipo_seleccionado

# --- 4. EJECUCIÓN PRINCIPAL ---
st.title("⚽ RCL Scout Group: Inteligencia Grupo 4")
st.caption("Herramienta descriptiva de scouting. Datos temporada 25/26.")

df = load_df()
team_logos = get_team_logos()

if df is None:
    st.error("Error: No se encontró el archivo 'df.csv' en el repositorio.")
    st.stop()

# --- SIDEBAR: FILTROS ---
st.sidebar.header("⏱️ Filtros Globales")
min_minutos = st.sidebar.slider(
    "Minutos mínimos jugados", 
    0, int(df["Minutos"].max()), 300, 50
)
df_filtrado = df[df["Minutos"] >= min_minutos]

# --- SELECTOR DE EQUIPO ---
equipo = team_selector(team_logos)

if equipo:
    st.divider()
    st.markdown(f"## 🏟️ {equipo}")
    
    # Filtrado por equipo
    df_team = df_filtrado[df_filtrado["Equipo"] == equipo].copy()

    if df_team.empty:
        st.warning("No hay jugadores que cumplan el filtro de minutos en este equipo.")
    else:
        # --- TABLA GENERAL DEL EQUIPO (PULIDA) ---
        st.markdown("### 📋 Plantel del equipo")
        
        # Selección de columnas clave
        cols_mostrar = [
            "Jugador", "Posicion_Limpia", "Minutos", "Partidos_Jugados", 
            "Pct_Titularidad_Real", "Goles", "Goles_p90"
        ]
        
        df_display = df_team[cols_mostrar].copy()
        
        # Formateo de decimales y porcentajes para la vista general
        df_display["Pct_Titularidad_Real"] = df_display["Pct_Titularidad_Real"].map("{:.1f}%".format)
        df_display["Goles_p90"] = df_display["Goles_p90"].map("{:.2f}".format)
        
        st.dataframe(df_display.sort_values("Minutos", ascending=False), use_container_width=True)

        # Botón para exportar a Excel (CSV)
        csv = df_team.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Data del Equipo (CSV)",
            data=csv,
            file_name=f"RCL_Scout_{equipo}.csv",
            mime='text/csv',
        )

        # --- ANÁLISIS INDIVIDUAL ---
        st.divider()
        st.markdown("### 👤 Análisis individual")
        jugador_sel = st.selectbox("Selecciona un jugador para ver su radiografía:", df_team["Jugador"].unique())
        
        if jugador_sel:
            df_j = df_team[df_team["Jugador"] == jugador_sel].iloc[0]

            # Bloques de métricas en columnas
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🧠 Uso y confianza CT")
                st.table(pd.DataFrame({
                    "Métrica": ["Convocados", "PJ", "Titular", "% Titularidad Real", "Minutos por Conv."],
                    "Valor": [
                        int(df_j["Convocados"]), 
                        int(df_j["Partidos_Jugados"]), 
                        int(df_j["Partidos_Titular"]), 
                        f"{df_j['Pct_Titularidad_Real']:.1f}%", 
                        f"{df_j['Minutos_por_Convocatoria']:.1f}"
                    ]
                }))

                st.subheader("🟨 Disciplina y Riesgo")
                st.table(pd.DataFrame({
                    "Métrica": ["Amarillas", "Rojas", "Tarjetas Totales", "Tarjetas p90", "Disciplina"],
                    "Valor": [
                        int(df_j["Amarillas"]), 
                        int(df_j["Rojas"]), 
                        int(df_j["Tarjetas_Totales"]), 
                        f"{df_j['Tarjetas_p90']:.2f}", 
                        f"{df_j['Disciplina']:.2f}"
                    ]
                }))

            with c2:
                st.subheader("📊 Impacto en cancha")
                st.table(pd.DataFrame({
                    "Métrica": ["Minutos", "Partidos 90", "Goles", "Goles p90", "Impacto Ofensivo"],
                    "Valor": [
                        int(df_j["Minutos"]), 
                        f"{df_j['Partidos_90']:.2f}", 
                        int(df_j["Goles"]), 
                        f"{df_j['Goles_p90']:.2f}", 
                        f"{df_j['Impacto_Ofensivo']:.2f}"
                    ]
                }))

                st.subheader("⚖️ Peso en el equipo")
                st.table(pd.DataFrame({
                    "Métrica": ["Peso en Equipo", "Rank Peso (Equipo)", "Minutos Totales"],
                    "Valor": [
                        f"{df_j['Peso_Equipo']:.2f}", 
                        int(df_j["Rank_Peso_Equipo"]), 
                        int(df_j["Minutos"])
                    ]
                }))

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("Desarrollado por Diego para RCL Scout Group. Prohibida su reproducción sin autorización.")
