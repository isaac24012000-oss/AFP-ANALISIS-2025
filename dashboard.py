import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(page_title="Analisis Comparativo Worldtel", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Estilos personalizados avanzados
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        .header-container {
            background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .header-title {
            text-align: center;
            color: #ffffff;
            font-size: 2.8em;
            font-weight: 900;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .subtitle {
            text-align: center;
            color: #e3f2fd;
            font-size: 1.3em;
            margin-bottom: 0;
            font-weight: 300;
        }
        
        .team-section {
            margin: 20px 0;
        }
        
        .team-header {
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            font-size: 1.4em;
            font-weight: bold;
            color: white;
        }
        
        .worldtel-header {
            background: linear-gradient(135deg, #1f77b4 0%, #0d47a1 100%);
            box-shadow: 0 4px 10px rgba(31, 119, 180, 0.3);
        }
        
        .gi-header {
            background: linear-gradient(135deg, #ff7f0e 0%, #e65100 100%);
            box-shadow: 0 4px 10px rgba(255, 127, 14, 0.3);
        }
        
        .metric-container {
            display: flex;
            gap: 15px;
            margin: 15px 0;
            flex-wrap: wrap;
        }
        
        .metric-card {
            flex: 1;
            min-width: 150px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #1f77b4;
            text-align: center;
        }
        
        .metric-card.gi {
            border-left-color: #ff7f0e;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
            font-weight: 500;
        }
        
        .metric-value {
            font-size: 1.6em;
            font-weight: bold;
            color: #1f77b4;
        }
        
        .metric-card.gi .metric-value {
            color: #ff7f0e;
        }
        
        .divider {
            border-top: 3px solid #e0e0e0;
            margin: 30px 0;
        }
        
        .section-title {
            font-size: 1.8em;
            font-weight: bold;
            color: #1f77b4;
            margin: 25px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #1f77b4;
        }
        
        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .cartera-row {
            background-color: #fff3cd !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal con diseño mejorado
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">📊 ANÁLISIS COMPARATIVO</h1>
        <p class="subtitle">WORLDTEL vs GI CORONADO - Cierre de Pagos</p>
    </div>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def cargar_datos():
    import os
    import glob
    
    # Obtener el directorio actual
    dir_actual = os.getcwd()
    
    # Buscar el archivo Excel en diferentes ubicaciones
    posibles_rutas = [
        "ANALISIS WORLDTEL.xlsx",
        "./ANALISIS WORLDTEL.xlsx",
        os.path.join(dir_actual, "ANALISIS WORLDTEL.xlsx"),
        r"C:\Users\USUARIO\Desktop\REPORTE MENSUAL WORLDTEL\DASHBOARD ANALISIS\WORLDTEL ANALISIS\ANALISIS WORLDTEL.xlsx"
    ]
    
    # También buscar recursivamente en el directorio actual
    try:
        archivos_xlsx = glob.glob("**/*.xlsx", recursive=True)
        for archivo in archivos_xlsx:
            # Excluir archivos temporales de Excel (~$)
            if "ANALISIS WORLDTEL" in archivo and not archivo.startswith("~$"):
                posibles_rutas.insert(0, archivo)
    except:
        pass
    
    ruta_archivo = None
    for ruta in posibles_rutas:
        try:
            # Excluir archivos temporales (que comienzan con ~$)
            if ruta.startswith("~$"):
                continue
            if os.path.exists(ruta) and os.path.isfile(ruta):
                ruta_archivo = ruta
                break
        except:
            continue
    
    if ruta_archivo is None:
        st.error("❌ No se encontró el archivo 'ANALISIS WORLDTEL.xlsx'")
        st.info(f"📁 Directorio actual: {dir_actual}")
        st.info("📍 Ubicaciones buscadas:")
        for ruta in posibles_rutas:
            st.info(f"  • {ruta}")
        st.warning("⚠️ Por favor, cierra el archivo Excel si está abierto y luego recarga la página")
        st.warning("📝 O coloca el archivo 'ANALISIS WORLDTEL.xlsx' en el mismo directorio que dashboard.py")
        st.stop()
    
    try:
        df = pd.read_excel(ruta_archivo, sheet_name='CIERRE DE PAGOS', engine='openpyxl')
        return df
    except PermissionError as e:
        st.error("❌ El archivo está siendo utilizado por otra aplicación (probablemente Excel)")
        st.warning("⚠️ Por favor, cierra el archivo Excel y luego recarga esta página")
        st.info(f"📄 Archivo: {ruta_archivo}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error al leer el archivo: {str(e)}")
        st.info(f"📄 Archivo encontrado en: {ruta_archivo}")
        st.stop()

df = cargar_datos()

# Definir los equipos
equipo_worldtel = [
    'Laura Villanueva Solayo',
    'Cherry Nathalia Matson Zambrano',
    'Sandra Maria Benavides Vela',
    'Carmen Dora Niño Ordinola',
    'Daniel Alejandro Barrios Pavon',
    'Juan Jose Felix Ventura',
    'Rosa Elena Villarreal Pelaez',
    'Carla del Rosario Castillo Alvarez'
]

# Clasificar asesores
df['EQUIPO'] = df['ASESOR'].apply(lambda x: 'WORLDTEL' if x in equipo_worldtel else 'GI CORONADO')

# Remover filas con ASESOR nulo o ESTUDIO
df = df[df['ASESOR'].notna() & (df['ASESOR'] != 'ESTUDIO')].copy()

# Crear tabla de asesores con todas sus carteras
df_asesores = df.groupby(['ASESOR', 'EQUIPO', 'CARTERA']).agg({
    'MONTO': 'sum',
    'RAZON_SOCIAL': 'nunique'
}).reset_index()

df_asesores.columns = ['ASESOR', 'EQUIPO', 'CARTERA', 'MONTO_TOTAL', 'NUM_RAZONES_SOCIALES']

# Para la tabla de equipos simplificada, agregar por asesor sin cartera
df_asesores_simple = df.groupby(['ASESOR', 'EQUIPO']).agg({
    'MONTO': 'sum',
    'RAZON_SOCIAL': 'nunique',
    'CARTERA': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
}).reset_index()

df_asesores_simple.columns = ['ASESOR', 'EQUIPO', 'MONTO_TOTAL', 'NUM_RAZONES_SOCIALES', 'CARTERA']

# Tablas por equipo
col1, col2 = st.columns(2)

def crear_tabla_jerarquica_equipo(df_equipo_completo):
    """Crea tabla jerárquica con Cartera como encabezado y asesores debajo, usando df_asesores con carteras"""
    tabla_jer = []
    
    # Obtener carteras únicas para este equipo
    carteras_eq = sorted(df_equipo_completo['CARTERA'].unique())
    
    for cartera in carteras_eq:
        df_cartera_eq = df_equipo_completo[df_equipo_completo['CARTERA'] == cartera]
        total_monto_cartera = df_cartera_eq['MONTO_TOTAL'].sum()
        total_clientes_cartera = df_cartera_eq['NUM_RAZONES_SOCIALES'].sum()
        
        # Fila de cartera
        tabla_jer.append({
            'Cartera / Asesor': f"◼ {cartera}",
            'Clientes': int(total_clientes_cartera),
            'Monto': f"S/ {total_monto_cartera:,.2f}",
            '_es_header': True
        })
        
        # Asesores bajo esta cartera (pueden repetirse si están en otras carteras)
        df_asesores_eq = df_cartera_eq.sort_values('MONTO_TOTAL', ascending=False)
        for idx, row in df_asesores_eq.iterrows():
            tabla_jer.append({
                'Cartera / Asesor': f"  {row['ASESOR']}",
                'Clientes': int(row['NUM_RAZONES_SOCIALES']),
                'Monto': f"S/ {row['MONTO_TOTAL']:,.2f}",
                '_es_header': False
            })
    
    return pd.DataFrame(tabla_jer)

def mostrar_tabla_html(df_tabla, columnas):
    """Convierte DataFrame a tabla HTML con estilos personalizados"""
    html_table = "<table style='width:100%; border-collapse: collapse;'>\n"
    html_table += "<tr style='background-color: #e8e8e8; font-weight: bold;'>"
    for col in columnas:
        if col == 'Monto' or col == 'Monto ($)':
            html_table += f"<th style='padding: 10px; border: 1px solid #ddd; text-align: right;'>{col}</th>"
        elif col == 'Clientes':
            html_table += f"<th style='padding: 10px; border: 1px solid #ddd; text-align: center;'>{col}</th>"
        else:
            html_table += f"<th style='padding: 10px; border: 1px solid #ddd; text-align: left;'>{col}</th>"
    html_table += "</tr>\n"
    
    for idx, row in df_tabla.iterrows():
        is_header = row.get('_es_header', False)
        if is_header:
            bg_color = "#fff3cd"
            font_weight = "bold"
        else:
            bg_color = "#ffffff"
            font_weight = "normal"
        
        html_table += f"<tr style='background-color: {bg_color}; font-weight: {font_weight};'>"
        for col in columnas:
            if col == 'Monto' or col == 'Monto ($)':
                html_table += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: right;'>{row[col]}</td>"
            elif col == 'Clientes':
                html_table += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{row[col]}</td>"
            else:
                html_table += f"<td style='padding: 8px; border: 1px solid #ddd;'>{row[col]}</td>"
        html_table += "</tr>\n"
    
    html_table += "</table>"
    return html_table

with col1:
    st.markdown('<div class="team-header worldtel-header">🟦 EQUIPO WORLDTEL</div>', unsafe_allow_html=True)
    df_worldtel_completo = df_asesores[df_asesores['EQUIPO'] == 'WORLDTEL']
    
    # Mostrar tabla jerárquica (con carteras)
    tabla_worldtel_jer = crear_tabla_jerarquica_equipo(df_worldtel_completo)
    html_tabla_worldtel = mostrar_tabla_html(tabla_worldtel_jer, ['Cartera / Asesor', 'Clientes', 'Monto'])
    st.markdown(html_tabla_worldtel, unsafe_allow_html=True)
    
    # Métricas Worldtel (desde df_asesores_simple para no duplicar)
    df_worldtel_simple = df_asesores_simple[df_asesores_simple['EQUIPO'] == 'WORLDTEL']
    monto_worldtel = df_worldtel_simple['MONTO_TOTAL'].sum()
    razones_worldtel = df_worldtel_simple['NUM_RAZONES_SOCIALES'].sum()
    asesores_worldtel = len(df_worldtel_simple)

with col2:
    st.markdown('<div class="team-header gi-header">🟧 EQUIPO GI CORONADO</div>', unsafe_allow_html=True)
    df_gi_completo = df_asesores[df_asesores['EQUIPO'] == 'GI CORONADO']
    
    # Mostrar tabla jerárquica (con carteras)
    tabla_gi_jer = crear_tabla_jerarquica_equipo(df_gi_completo)
    html_tabla_gi = mostrar_tabla_html(tabla_gi_jer, ['Cartera / Asesor', 'Clientes', 'Monto'])
    st.markdown(html_tabla_gi, unsafe_allow_html=True)
    
    # Métricas GI Coronado (desde df_asesores_simple para no duplicar)
    df_gi_simple = df_asesores_simple[df_asesores_simple['EQUIPO'] == 'GI CORONADO']
    monto_gi = df_gi_simple['MONTO_TOTAL'].sum()
    razones_gi = df_gi_simple['NUM_RAZONES_SOCIALES'].sum()
    asesores_gi = len(df_gi_simple)

# Métricas alineadas horizontalmente
st.markdown("### Resumen de Equipos")
col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)

with col_m1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monto Total WORLDTEL</div>
            <div class="metric-value">S/ {monto_worldtel:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Clientes WORLDTEL</div>
            <div class="metric-value">{razones_worldtel:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Asesores WORLDTEL</div>
            <div class="metric-value">{asesores_worldtel}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
        <div class="metric-card gi">
            <div class="metric-label">Monto Total GI</div>
            <div class="metric-value">S/ {monto_gi:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m5:
    st.markdown(f"""
        <div class="metric-card gi">
            <div class="metric-label">Clientes GI</div>
            <div class="metric-value">{razones_gi:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col_m6:
    st.markdown(f"""
        <div class="metric-card gi">
            <div class="metric-label">Asesores GI</div>
            <div class="metric-value">{asesores_gi}</div>
        </div>
    """, unsafe_allow_html=True)

# Línea separadora
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Gráficos comparativos
st.markdown('<h2 class="section-title">📈 Análisis Comparativo</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Gráfico de Monto por Equipo
    datos_equipo = df_asesores_simple.groupby('EQUIPO')['MONTO_TOTAL'].sum().reset_index()
    fig_monto = px.bar(datos_equipo, x='EQUIPO', y='MONTO_TOTAL', 
                       title='Monto Total por Equipo',
                       color='EQUIPO',
                       color_discrete_map={'WORLDTEL': '#1f77b4', 'GI CORONADO': '#ff7f0e'},
                       labels={'MONTO_TOTAL': 'Monto (S/)', 'EQUIPO': 'Equipo'})
    fig_monto.update_layout(showlegend=False, hovermode='x unified', height=450)
    fig_monto.update_traces(marker_line_width=2, marker_line_color='white')
    st.plotly_chart(fig_monto, use_container_width=True)

with col2:
    # Gráfico de Razones Sociales por Equipo
    datos_razones = df_asesores_simple.groupby('EQUIPO')['NUM_RAZONES_SOCIALES'].sum().reset_index()
    fig_razones = px.bar(datos_razones, x='EQUIPO', y='NUM_RAZONES_SOCIALES',
                        title='Total de Clientes por Equipo',
                        color='EQUIPO',
                        color_discrete_map={'WORLDTEL': '#1f77b4', 'GI CORONADO': '#ff7f0e'},
                        labels={'NUM_RAZONES_SOCIALES': 'Cantidad', 'EQUIPO': 'Equipo'})
    fig_razones.update_layout(showlegend=False, hovermode='x unified', height=450)
    fig_razones.update_traces(marker_line_width=2, marker_line_color='white')
    st.plotly_chart(fig_razones, use_container_width=True)

# Desempeño por Asesor
st.markdown('<h2 class="section-title">👥 Desempeño Individual por Asesor</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="team-header worldtel-header">🟦 WORLDTEL</div>', unsafe_allow_html=True)
    fig_worldtel = px.bar(df_worldtel_simple.sort_values('MONTO_TOTAL', ascending=True),
                          x='MONTO_TOTAL', y='ASESOR',
                          orientation='h',
                          title='Monto por Asesor',
                          color='MONTO_TOTAL',
                          color_continuous_scale='Blues',
                          labels={'MONTO_TOTAL': 'Monto (S/)', 'ASESOR': 'Asesor'})
    fig_worldtel.update_layout(height=400, showlegend=False, hovermode='closest')
    fig_worldtel.update_traces(marker_line_width=1.5, marker_line_color='white')
    st.plotly_chart(fig_worldtel, use_container_width=True)

with col2:
    st.markdown('<div class="team-header gi-header">🟧 GI CORONADO</div>', unsafe_allow_html=True)
    fig_gi = px.bar(df_gi_simple.sort_values('MONTO_TOTAL', ascending=True),
                    x='MONTO_TOTAL', y='ASESOR',
                    orientation='h',
                    title='Monto por Asesor',
                    color='MONTO_TOTAL',
                    color_continuous_scale='Oranges',
                    labels={'MONTO_TOTAL': 'Monto (S/)', 'ASESOR': 'Asesor'})
    fig_gi.update_layout(height=400, showlegend=False, hovermode='closest')
    fig_gi.update_traces(marker_line_width=1.5, marker_line_color='white')
    st.plotly_chart(fig_gi, use_container_width=True)

# Análisis por Cartera
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📋 Análisis por Cartera</h2>', unsafe_allow_html=True)

# Datos por cartera, asesor y equipo
df_cartera_detalle = df_asesores.copy()

# Agrupar por cartera para el gráfico
df_cartera_chart = df.groupby(['CARTERA', 'EQUIPO']).agg({
    'MONTO': 'sum',
    'RAZON_SOCIAL': 'nunique'
}).reset_index()
df_cartera_chart.columns = ['CARTERA', 'EQUIPO', 'MONTO', 'CLIENTES']

# Gráfico de cartera
fig_cartera = px.bar(df_cartera_chart, x='CARTERA', y='MONTO', color='EQUIPO',
                     title='Monto por Cartera y Equipo',
                     color_discrete_map={'WORLDTEL': '#1f77b4', 'GI CORONADO': '#ff7f0e'},
                     labels={'MONTO': 'Monto (S/)', 'CARTERA': 'Cartera'},
                     barmode='group')
fig_cartera.update_layout(height=450, hovermode='x unified')
fig_cartera.update_traces(marker_line_width=1.5, marker_line_color='white')
st.plotly_chart(fig_cartera, use_container_width=True)

# Tabla jerárquica por Cartera y Asesor
st.markdown("### Detalle por Cartera y Asesor")

# Crear tabla jerárquica usando df_asesores (que tiene carteras múltiples)
tabla_jerarquica = []

carteras_ordenadas = sorted(df_asesores['CARTERA'].unique())

for cartera in carteras_ordenadas:
    df_cartera_actual = df_asesores[df_asesores['CARTERA'] == cartera]
    
    # Totales por cartera
    total_monto_cartera = df_cartera_actual['MONTO_TOTAL'].sum()
    total_clientes_cartera = df_cartera_actual['NUM_RAZONES_SOCIALES'].sum()
    
    # Fila de la cartera (header)
    tabla_jerarquica.append({
        'Cartera / Asesor': f"◼ {cartera}",
        'Clientes': int(total_clientes_cartera),
        'Monto ($)': f"S/ {total_monto_cartera:,.2f}",
        '_es_header': True
    })
    
    # Asesores bajo esta cartera ordenados por monto
    df_asesores_cartera = df_cartera_actual.sort_values('MONTO_TOTAL', ascending=False)
    
    for idx, row in df_asesores_cartera.iterrows():
        tabla_jerarquica.append({
            'Cartera / Asesor': f"    {row['ASESOR']} ({row['EQUIPO']})",
            'Clientes': int(row['NUM_RAZONES_SOCIALES']),
            'Monto ($)': f"S/ {row['MONTO_TOTAL']:,.2f}",
            '_es_header': False
        })

# Convertir a DataFrame
tabla_jerarquica_df = pd.DataFrame(tabla_jerarquica)

# Crear tabla HTML con estilos personalizados
html_tabla_detalle = mostrar_tabla_html(tabla_jerarquica_df, ['Cartera / Asesor', 'Clientes', 'Monto ($)'])
st.markdown(html_tabla_detalle, unsafe_allow_html=True)

# Resumen General
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📊 Resumen General Comparativo</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monto WORLDTEL</div>
            <div class="metric-value">S/ {monto_worldtel:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card gi">
            <div class="metric-label">Monto GI CORONADO</div>
            <div class="metric-value">S/ {monto_gi:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    diferencia = monto_worldtel - monto_gi
    color = "#27ae60" if diferencia > 0 else "#e74c3c"
    st.markdown(f"""
        <div class="metric-card" style="border-left-color: {color};">
            <div class="metric-label">Diferencia WORLDTEL</div>
            <div class="metric-value" style="color: {color};">S/ {diferencia:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    porcentaje_worldtel = (monto_worldtel / (monto_worldtel + monto_gi)) * 100
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Participación WORLDTEL</div>
            <div class="metric-value">{porcentaje_worldtel:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)
