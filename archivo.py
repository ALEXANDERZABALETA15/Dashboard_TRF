#IMPORTACION DE LIBRERIAS PARA EL USO DEL DASHBOARD 
import streamlit as st
import pandas as pd
import plotly.express as px 
from PIL import Image

st.set_page_config(page_title = "Dashboard Dinamico", layout ="wide")

# ---------------- LOGO Y TÍTULO ----------------
logo = Image.open("assets/logo_claro.png")
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=250)
with col2:
    st.title("Dashboard Empresarial TRF")

# ---------------- CARGA DE DATOS ----------------
@st.cache_data
def cargar_datos():
    df = pd.read_excel("data/Reporte_trf_base_fija_incidentes.xlsx", engine='openpyxl', header=0)
    return df

df = cargar_datos()

# ---------------- KPI 1: SUMATORIA DE OT ----------------

cantidad_ot = df['ot'].dropna().shape[0]

# ---------------- KPI 2: CONTEO DE CUMPLIMIENTOS (valores igual a 1) ----------------
# Contamos cuántas veces cumple_general es igual a 1

cumplimiento = (df['cumple_general'] == 1).sum()

# ---------------- KPI 3: CONTEO DE REPORTES TOTAL ----------------

total_reportes = df['regional'].notna().sum()

# ---------------- MOSTRAR TARJETAS CON KPIs --------------
st.markdown("### 📊 Indicadores Generales")

col_1 , col_2, col_3 = st.columns(3)

with col_1:
    st.metric(label="✅Cantidad Total OT's", value=int(cantidad_ot))
with col_2:
    st.metric(label="⏰Total de cumplimientos generales", value=int(cumplimiento))
with col_3:
    st.metric(label="📌Total registros", value=int(total_reportes))
# ---------------- VISTA PREVIA DE DATOS ----------------
st.subheader("Vista previa de los datos")
st.dataframe(df) 


# ---------- BARRA LATERAL DE FILTROS ---------

st.sidebar.header("FILTROS")

ciudades = st.sidebar.multiselect(
    "Seleciona la ciudad:",
    placeholder="Elige una ciudad",
    options=df['ciudad'].unique(),
#     default=df['ciudad'].unique()
)

tipos_ot = st.sidebar.multiselect(
    "Selecciones el tipo de OT:",
    placeholder="Tipo de ot",
    options=df['tipo_ot'].unique(),
    # default=df['tipo_ot'].unique()
)

cumple_campo= st.sidebar.multiselect(
    "Selecciones Cumple Campo:",
    placeholder="Campo",
    options=df['cumple_campo'].unique(),
    # default=df['cumple_campo'].unique()
)

zone = st.sidebar.multiselect(
    "Seleciona Zone Owner:",
    placeholder="Zone Owner",
    options=df['zone_owner'].unique(),
    # default=df['zone_owner'].unique()
)

aliados = st.sidebar.multiselect(
    "Aliados:",
    placeholder="Aliados",
    options=df['aliado'].unique(),
    # default=df["aliado"].unique()
)





# ---------- APLICACIÓN DE FILTROS ----------
# Aplicamos filtros dinámicamente solo si se selecciona algo

df_filtrado = df.copy()

if ciudades:
    df_filtrado = df_filtrado[df_filtrado['ciudad'].isin(ciudades)]

if tipos_ot:
    df_filtrado = df_filtrado[df_filtrado['tipo_ot'].isin(tipos_ot)]

if cumple_campo:
    df_filtrado = df_filtrado[df_filtrado['cumple_campo'].isin(cumple_campo)]

if zone:
    df_filtrado = df_filtrado[df_filtrado['zone_owner'].isin(zone)]

if aliados:
    df_filtrado = df_filtrado[df_filtrado['aliado'].isin(aliados)]

# ---------- VISUALIZACIÓN DE LOS DATOS FILTRADOS ----------
st.subheader("Vista previa de los datos filtrados")
st.dataframe(df_filtrado)


# ---------------- ESPACIO PARA GRÁFICAS ----------------
st.subheader("Gráficas de Análisis")

# Aquí irán tus futuras visualizaciones 
st.write("Aquí se mostrarán las gráficas y análisis visuales.")

# ---------------- PIE DE PÁGINA ----------------
st.markdown("---")
st.caption("Desarrollado por Jhon Alexander Zabaleta - 2025")










































































