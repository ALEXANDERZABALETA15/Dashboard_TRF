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
st.subheader("Datos filtrados")
st.dataframe(df_filtrado)


# ---------------- ESPACIO PARA GRÁFICAS ----------------
st.subheader("Gráficas de Análisis")

#1. Gráfico de barras por cantidad de OTs por ciudad
#¿Qué muestra? Número total de reportes (OTs) por cada ciudad.

# fig = px.bar(df_filtrado, x='ciudad', title='Cantidad de reportes por ciudad')
# st.plotly_chart(fig)

#PRUEBASSSSSS

# 1. Gráfico de barras por cantidad de OTs por ciudad
# ¿Qué muestra? Número total de reportes (OTs) por cada ciudad.

# Contamos OTs por ciudad
conteo_ciudades = df_filtrado['ciudad'].value_counts().reset_index()
conteo_ciudades.columns = ['ciudad', 'cantidad']

# Gráfico
fig = px.bar(
    conteo_ciudades,
    x='ciudad',
    y='cantidad',
    title='Cantidad de reportes por ciudad',
    text='cantidad',                # Muestra valores encima de cada barra
    color_discrete_sequence=['#1f77b4']  # Un solo color (azul por defecto, lo puedes cambiar)
)

# Ajustes de diseño
fig.update_traces(
    texttemplate='<b>%{text}</b>',   # Texto en negrita
    textposition='outside'           # Colocar los valores encima de la barra
)

fig.update_layout(
    uniformtext_minsize=12,
    uniformtext_mode='hide',
    yaxis_title="Cantidad de reportes",
    xaxis_title="Ciudad",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)





#2. Gráfico de torta (Pie Chart) – Distribución por aliados
#¿Qué muestra? Porcentaje de participación de cada aliado.

figura = px.pie(df_filtrado, names='aliado', title='Distribución por aliado')
st.plotly_chart(figura)

#3. Gráfico de barras por cumplimiento en campo (cumple_campo)
#¿Qué muestra? Cuántos reportes cumplieron o no cumplieron.


# Paso 1: Contar valores y resetear el índice
cumple_data = df_filtrado['cumple_campo'].value_counts().reset_index()

# Paso 2: Renombrar las columnas
cumple_data.columns = ['cumple_campo', 'cantidad']

# Paso 3: Crear el gráfico con un solo color
grafico_barras = px.bar(
    cumple_data,
    x='cumple_campo',
    y='cantidad',
    labels={'cumple_campo': 'Cumple en Campo', 'cantidad': 'Cantidad'},
    title='Cumplimiento en Campo',
    color_discrete_sequence=['#1f77b4']  # un solo color
)

# Paso 4: Personalizar las trazas
grafico_barras.update_traces(
    text=cumple_data['cantidad'],      # Mostrar los valores
    textposition='outside',            # Posición encima de las barras
    textfont=dict(size=14, color='black', family="Arial Black")  # Negrita usando Arial Black
)

# Paso 5: Mejorar la estética general
grafico_barras.update_layout(
    title=dict(x=0.5, xanchor='center', font=dict(size=22, family="Arial", color="black")),
    xaxis=dict(title='', showgrid=False),
    yaxis=dict(title='Cantidad', showgrid=True, gridcolor="lightgrey"),
    plot_bgcolor='white',
    bargap=0.3
)

# Mostrar en Streamlit
st.plotly_chart(grafico_barras, use_container_width=True)




#4. Gráfico de barras por tipo de OT
#¿Qué muestra? Distribución de los tipos de orden de trabajo.

# Paso 1: Contar tipos de OT y resetear el índice
tipo_ot_data = df_filtrado['tipo_ot'].value_counts().reset_index()

# Paso 2: Renombrar las columnas
tipo_ot_data.columns = ['tipo_ot', 'cantidad']

# Paso 3: Calcular porcentaje
tipo_ot_data['porcentaje'] = (tipo_ot_data['cantidad'] / tipo_ot_data['cantidad'].sum()) * 100

# Paso 4: Crear gráfico con Plotly
grafico_tipo_ot = px.bar(
    tipo_ot_data,
    x='tipo_ot',
    y='cantidad',
    text=tipo_ot_data['porcentaje'].apply(lambda x: f"{x:.1f}%"),
    labels={'tipo_ot': 'Tipo de OT', 'cantidad': 'Cantidad'},
    title='Distribución de Tipos de OT',
    color='tipo_ot'  # Colores diferentes por tipo de OT
)

# Ajustar diseño
grafico_tipo_ot.update_traces(textposition='outside')  # Muestra porcentajes encima de cada barra
grafico_tipo_ot.update_layout(
    xaxis_title="Tipo de OT",
    yaxis_title="Cantidad",
    uniformtext_minsize=10,
    uniformtext_mode='hide',
    bargap=0.3
)

# Mostrar en dashboard
st.plotly_chart(grafico_tipo_ot)


#6. Gráfico de barras horizontales por zone_owner
#¿Qué muestra? Cantidad de reportes por dueño de zona.

# Paso 1: Contar cuántas veces aparece cada zone_owner
zone_data = df_filtrado['zone_owner'].value_counts().reset_index()

# Paso 2: Renombrar las columnas correctamente
zone_data.columns = ['zone_owner', 'cantidad']

# Paso 3: Crear el gráfico horizontal con etiquetas
grafico_barras_horizontales = px.bar(
    zone_data,
    x='cantidad',
    y='zone_owner',
    orientation='h',  # Horizontal
    labels={'zone_owner': 'Zone Owner', 'cantidad': 'Cantidad'},
    title='Reportes por Zone Owner',
    text='cantidad'  # Mostrar la cantidad sobre cada barra
)

# Paso 4: Personalizar el texto para que se vea más claro
grafico_barras_horizontales.update_traces(
    textposition='outside',  # Muestra el número fuera de la barra
    textfont=dict(size=12, color="black", family="Arial", weight="bold")  # Negrita y tamaño
)

# Paso 5: Mostrar el gráfico
st.plotly_chart(grafico_barras_horizontales)

# ---------------- PIE DE PÁGINA ----------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; font-size:14px; color:gray;">
        📊 Desarrollado por <b>Jhon Alexander Zabaleta</b> - 2025 <br>
        <a href="https://www.linkedin.com/in/jhon-alexander-zabaleta-dev/" target="_blank">LinkedIn</a> | 
        <a href="https://github.com/ALEXANDERZABALETA15" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)











































































