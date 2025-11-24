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

# ============================================
# TABLA HOY x HOY - GESTIONES
# ============================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📅 Tabla HOY x HOY - Gestiones</h2>', unsafe_allow_html=True)

def cargar_gestiones():
    import os
    posibles_rutas = [
        "ANALISIS WORLDTEL.xlsx",
        "./ANALISIS WORLDTEL.xlsx",
        os.path.join(os.getcwd(), "ANALISIS WORLDTEL.xlsx"),
        r"C:\Users\USUARIO\Desktop\REPORTE MENSUAL WORLDTEL\DASHBOARD ANALISIS\WORLDTEL ANALISIS\ANALISIS WORLDTEL.xlsx"
    ]
    
    for ruta in posibles_rutas:
        try:
            if os.path.exists(ruta) and os.path.isfile(ruta):
                try:
                    df = pd.read_excel(ruta, sheet_name='GESTIONES', engine='openpyxl')
                    return df
                except:
                    pass
        except:
            pass
    return None

df_gestiones = cargar_gestiones()

if df_gestiones is not None and not df_gestiones.empty:
    # Clasificar gestores por equipo
    df_gestiones['EQUIPO'] = df_gestiones['GESTOR'].apply(lambda x: 'WORLDTEL' if x in equipo_worldtel else 'GI CORONADO')
    
    # Limpiar datos
    df_gestiones_limpio = df_gestiones[
        (df_gestiones['FECHA_GESTION'].notna()) &
        (df_gestiones['FECHA_PROMESA'].notna()) &
        (df_gestiones['MONTO_PROMESA'].notna()) &
        (df_gestiones['MONTO_PROMESA'] > 0)
    ].copy()
    
    if not df_gestiones_limpio.empty:
        # Filtro por equipo
        col_filtro = st.columns(1)[0]
        with col_filtro:
            filtro_equipo = st.selectbox(
                "🔍 Filtrar por Equipo",
                options=['TODOS', 'WORLDTEL', 'GI CORONADO'],
                index=0,
                key='selectbox_hoy'
            )
        
        # Aplicar filtro
        if filtro_equipo != 'TODOS':
            df_filtrado = df_gestiones_limpio[df_gestiones_limpio['EQUIPO'] == filtro_equipo].copy()
        else:
            df_filtrado = df_gestiones_limpio.copy()
        
        # Convertir fechas a formato DD/MM/AA
        df_filtrado['FECHA_GESTION'] = pd.to_datetime(df_filtrado['FECHA_GESTION']).dt.strftime('%d/%m/%y')
        df_filtrado['FECHA_PROMESA'] = pd.to_datetime(df_filtrado['FECHA_PROMESA']).dt.strftime('%d/%m/%y')
        
        # Crear tabla cruzada (pivot table)
        tabla_cruzada = df_filtrado.pivot_table(
            index='FECHA_GESTION',
            columns='FECHA_PROMESA',
            values='MONTO_PROMESA',
            aggfunc='sum'
        )
        
        # Agregar totales
        tabla_cruzada['TOTAL'] = tabla_cruzada.sum(axis=1)
        totales_columnas = tabla_cruzada.sum(axis=0)
        totales_columnas.name = 'TOTAL'
        tabla_cruzada = pd.concat([tabla_cruzada, totales_columnas.to_frame().T])
        
        # Rellenar NaN con 0 y redondear a 2 decimales
        tabla_cruzada = tabla_cruzada.fillna(0).round(2)
        
        # Crear tabla HTML mejorada
        html_tabla_hoy = "<div style='overflow-x: auto; margin: 20px 0;'><table style='border-collapse: collapse; width: 100%; font-size: 0.9em;'>"
        
        # Encabezados
        html_tabla_hoy += "<tr style='background-color: #f0f0f0;'><th style='border: 1px solid #ddd; padding: 4px; text-align: center; font-weight: bold;'>HOY x HOY</th>"
        for col in tabla_cruzada.columns:
            html_tabla_hoy += f"<th style='border: 1px solid #ddd; padding: 4px; text-align: center; font-weight: bold;'>{col}</th>"
        html_tabla_hoy += "</tr>"
        
        # Datos
        for idx, row in tabla_cruzada.iterrows():
            if idx == 'TOTAL':
                # Fila de totales
                html_tabla_hoy += f"<tr style='background-color: #e8f4f8; font-weight: bold;'><td style='border: 1px solid #ddd; padding: 4px; text-align: center;'>{idx}</td>"
                for val in row:
                    html_tabla_hoy += f"<td style='border: 1px solid #ddd; padding: 4px; text-align: right;'>{val:,.2f}</td>"
                html_tabla_hoy += "</tr>"
            else:
                # Filas normales
                html_tabla_hoy += f"<tr><td style='border: 1px solid #ddd; padding: 4px; text-align: center; font-weight: bold;'>{idx}</td>"
                for val in row:
                    if val == 0:
                        html_tabla_hoy += f"<td style='border: 1px solid #ddd; padding: 4px; text-align: right; color: #ccc;'>-</td>"
                    else:
                        html_tabla_hoy += f"<td style='border: 1px solid #ddd; padding: 4px; text-align: right;'>{val:,.2f}</td>"
                html_tabla_hoy += "</tr>"
        
        html_tabla_hoy += "</table></div>"
        st.markdown(html_tabla_hoy, unsafe_allow_html=True)
    else:
        st.warning("No hay datos válidos en la hoja GESTIONES")
else:
    st.info("No se encontró la hoja GESTIONES o está vacía")

# ============================================
# ANÁLISIS DE EFECTIVIDAD Y CONVERSIÓN
# ============================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📈 Análisis de Efectividad y Conversión</h2>', unsafe_allow_html=True)

# Calcular totales de cada equipo
monto_worldtel_recaudado = df[df['EQUIPO'] == 'WORLDTEL']['MONTO'].sum()
monto_gi_recaudado = df[df['EQUIPO'] == 'GI CORONADO']['MONTO'].sum()

# Calcular promesas por equipo desde HOY x HOY
if df_gestiones is not None and not df_gestiones.empty:
    df_gestiones['EQUIPO'] = df_gestiones['GESTOR'].apply(lambda x: 'WORLDTEL' if x in equipo_worldtel else 'GI CORONADO')
    
    df_gestiones_limpio = df_gestiones[
        (df_gestiones['FECHA_GESTION'].notna()) &
        (df_gestiones['FECHA_PROMESA'].notna()) &
        (df_gestiones['MONTO_PROMESA'].notna()) &
        (df_gestiones['MONTO_PROMESA'] > 0)
    ].copy()
    
    monto_promesas_worldtel = df_gestiones_limpio[df_gestiones_limpio['EQUIPO'] == 'WORLDTEL']['MONTO_PROMESA'].sum()
    monto_promesas_gi = df_gestiones_limpio[df_gestiones_limpio['EQUIPO'] == 'GI CORONADO']['MONTO_PROMESA'].sum()
    
    # Filtro para la sección de análisis
    col_filtro_analisis = st.columns(1)[0]
    with col_filtro_analisis:
        filtro_analisis = st.selectbox(
            "🔍 Selecciona Equipo para Análisis",
            options=['TODOS', 'WORLDTEL', 'GI CORONADO'],
            index=0,
            key='selectbox_analisis'
        )
    
    # Crear tarjetas de análisis
    if filtro_analisis == 'WORLDTEL' or filtro_analisis == 'TODOS':
        st.markdown("### 🟦 WORLDTEL")
        
        col1, col2, col3, col4 = st.columns(4)
        
        monto_recaudado = monto_worldtel_recaudado
        monto_promesas = monto_promesas_worldtel
        monto_total_proyectado = monto_recaudado + monto_promesas
        
        # Calcular % de conversión
        if monto_total_proyectado > 0:
            porcentaje_conversion = (monto_recaudado / monto_total_proyectado) * 100
        else:
            porcentaje_conversion = 0
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💰 Recaudado</div>
                    <div class="metric-value">S/ {monto_recaudado:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📋 En Promesas</div>
                    <div class="metric-value">S/ {monto_promesas:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Total Proyectado</div>
                    <div class="metric-value">S/ {monto_total_proyectado:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            color_conversion = "#27ae60" if porcentaje_conversion > 50 else "#e74c3c"
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: {color_conversion};">
                    <div class="metric-label">📊 % Conversión</div>
                    <div class="metric-value" style="color: {color_conversion};">{porcentaje_conversion:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
    
    if filtro_analisis == 'GI CORONADO' or filtro_analisis == 'TODOS':
        st.markdown("### 🟠 GI CORONADO")
        
        col1, col2, col3, col4 = st.columns(4)
        
        monto_recaudado = monto_gi_recaudado
        monto_promesas = monto_promesas_gi
        monto_total_proyectado = monto_recaudado + monto_promesas
        
        # Calcular % de conversión
        if monto_total_proyectado > 0:
            porcentaje_conversion = (monto_recaudado / monto_total_proyectado) * 100
        else:
            porcentaje_conversion = 0
        
        with col1:
            st.markdown(f"""
                <div class="metric-card gi">
                    <div class="metric-label">💰 Recaudado</div>
                    <div class="metric-value">S/ {monto_recaudado:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card gi">
                    <div class="metric-label">📋 En Promesas</div>
                    <div class="metric-value">S/ {monto_promesas:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card gi">
                    <div class="metric-label">🎯 Total Proyectado</div>
                    <div class="metric-value">S/ {monto_total_proyectado:,.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            color_conversion = "#27ae60" if porcentaje_conversion > 50 else "#e74c3c"
            st.markdown(f"""
                <div class="metric-card gi" style="border-left-color: {color_conversion};">
                    <div class="metric-label">📊 % Conversión</div>
                    <div class="metric-value" style="color: {color_conversion};">{porcentaje_conversion:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("No se pueden calcular métricas sin datos de GESTIONES")

# ============================================
# SECCIÓN TIMMING - GASTOS
# ============================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">⏱️ ANÁLISIS DE TIMMING - GASTOS</h2>', unsafe_allow_html=True)

def cargar_timming():
    import os
    
    # Obtener el directorio donde está el dashboard
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar el archivo TIMMING en el mismo directorio
    ruta_timming = os.path.join(dir_actual, 'TIMMING WORLDTEL SET - OCT 2025.xlsx')
    
    if not os.path.exists(ruta_timming):
        st.error(f"❌ No se encontró el archivo TIMMING")
        st.info(f"📁 Buscando en: {ruta_timming}")
        return None
    
    try:
        # Leer la hoja TIMMING NOVIEMBRE sin headers
        df_timming = pd.read_excel(ruta_timming, sheet_name='TIMMING NOVIEMBRE', engine='openpyxl', header=None)
        return df_timming
    except PermissionError:
        st.error("❌ El archivo está siendo utilizado por otra aplicación")
        st.warning("⚠️ Por favor, cierra el archivo Excel y luego recarga la página")
        return None
    except Exception as e:
        st.error(f"Error al cargar timming: {str(e)}")
        return None

def parsear_timming_data(df_timming):
    """Parsea las 4 tablas del archivo timming"""
    tablas = {}
    
    try:
        # GASTOS GENERAL (columnas 1-5, filas 2-23)
        datos_gg = df_timming.iloc[2:23, 1:6].copy()
        datos_gg.columns = ['Día hábil', 'Fecha', 'Timing', 'Meta día', 'Acumulado']
        datos_gg = datos_gg[pd.to_numeric(datos_gg['Día hábil'], errors='coerce').notna()].copy()
        datos_gg = datos_gg.reset_index(drop=True)
        tablas['GASTOS_GENERAL'] = datos_gg
    except:
        tablas['GASTOS_GENERAL'] = None
    
    try:
        # GASTOS ASESOR (columnas 7-11, filas 2-23)
        datos_ga = df_timming.iloc[2:23, 7:12].copy()
        datos_ga.columns = ['Día hábil', 'Fecha', 'Timing', 'Meta día', 'Acumulado']
        datos_ga = datos_ga[pd.to_numeric(datos_ga['Día hábil'], errors='coerce').notna()].copy()
        datos_ga = datos_ga.reset_index(drop=True)
        tablas['GASTOS_ASESOR'] = datos_ga
    except:
        tablas['GASTOS_ASESOR'] = None
    
    try:
        # PLANILLAS GENERAL (columnas 1-5, filas 28-49)
        datos_pg = df_timming.iloc[28:49, 1:6].copy()
        datos_pg.columns = ['Día hábil', 'Fecha', 'Timing', 'Meta día', 'Acumulado']
        datos_pg = datos_pg[pd.to_numeric(datos_pg['Día hábil'], errors='coerce').notna()].copy()
        datos_pg = datos_pg.reset_index(drop=True)
        tablas['PLANILLAS_GENERAL'] = datos_pg
    except:
        tablas['PLANILLAS_GENERAL'] = None
    
    try:
        # PLANILLAS ASESOR (columnas 7-11, filas 28-49)
        datos_pa = df_timming.iloc[28:49, 7:12].copy()
        datos_pa.columns = ['Día hábil', 'Fecha', 'Timing', 'Meta día', 'Acumulado']
        datos_pa = datos_pa[pd.to_numeric(datos_pa['Día hábil'], errors='coerce').notna()].copy()
        datos_pa = datos_pa.reset_index(drop=True)
        tablas['PLANILLAS_ASESOR'] = datos_pa
    except:
        tablas['PLANILLAS_ASESOR'] = None
    
    return tablas

def mostrar_tabla_timming(datos, titulo, monto_recaudado_worldtel=None, es_asesor=False, nombre_asesor=None, df_cierre=None):
    """Muestra tabla de timming con análisis del día actual
    
    Args:
        datos: DataFrame con datos de timming
        titulo: Título de la tabla
        monto_recaudado_worldtel: Monto recaudado total (por defecto)
        es_asesor: True si es una tabla de asesor
        nombre_asesor: Nombre del asesor específico
        df_cierre: DataFrame de CIERRE DE PAGOS para buscar recaudado por asesor
    """
    if datos is None or datos.empty:
        st.warning(f"No hay datos para {titulo}")
        return
    
    try:
        from datetime import datetime
        
        # Limpiar y convertir datos
        datos = datos.copy()
        
        # Convertir columnas numéricas
        datos['Día hábil'] = pd.to_numeric(datos['Día hábil'], errors='coerce')
        datos['Timing'] = pd.to_numeric(datos['Timing'], errors='coerce')
        datos['Meta día'] = pd.to_numeric(datos['Meta día'], errors='coerce')
        datos['Acumulado'] = pd.to_numeric(datos['Acumulado'], errors='coerce')
        
        # Convertir fechas
        datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')
        
        # Obtener el día actual (fecha del sistema)
        from datetime import date
        hoy = datetime.combine(date.today(), datetime.min.time())
        
        # Buscar la fila del día actual basado en la fecha
        fila_hoy = None
        acumulado_hoy = 0
        meta_acumulada_hoy = 0
        
        for idx, row in datos.iterrows():
            fecha = row['Fecha']
            if pd.notna(fecha):
                if fecha.date() <= hoy.date():
                    acumulado_hoy = row['Acumulado'] if pd.notna(row['Acumulado']) else 0
                    meta_acumulada_hoy = row['Meta día'] if pd.notna(row['Meta día']) else 0
                    fila_hoy = idx
        
        # Calcular el recaudado específico si es por asesor
        monto_recaudado_actual = monto_recaudado_worldtel
        if es_asesor and nombre_asesor and df_cierre is not None:
            # Buscar el recaudado del asesor específico desde CIERRE DE PAGOS
            monto_asesor = df_cierre[df_cierre['ASESOR'] == nombre_asesor]['MONTO'].sum()
            monto_recaudado_actual = monto_asesor if monto_asesor > 0 else monto_recaudado_worldtel
        
        # Mostrar métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Acumulado Hoy (Timming) - Visual mejorado
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                    <div style='font-size: 0.85em; color: rgba(255,255,255,0.8); margin-bottom: 5px;'>📍 Acumulado Hoy (Timming)</div>
                    <div style='font-size: 1.8em; font-weight: bold; color: #ffffff;'>S/ {acumulado_hoy:,.2f}</div>
                    <div style='font-size: 0.75em; color: rgba(255,255,255,0.6); margin-top: 5px;'>Meta esperada al 21/11</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if monto_recaudado_actual is not None:
                # Recaudado Real - Visual mejorado
                etiqueta_recaudado = "Recaudado Real (Asesor)" if es_asesor else "Recaudado Real"
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <div style='font-size: 0.85em; color: rgba(255,255,255,0.8); margin-bottom: 5px;'>💰 {etiqueta_recaudado}</div>
                        <div style='font-size: 1.8em; font-weight: bold; color: #ffffff;'>S/ {monto_recaudado_actual:,.2f}</div>
                        <div style='font-size: 0.75em; color: rgba(255,255,255,0.6); margin-top: 5px;'>{'Dinero generado por asesor' if es_asesor else 'Dinero en caja WORLDTEL'}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                        <div style='font-size: 0.85em; color: rgba(255,255,255,0.8); margin-bottom: 5px;'>💰 Recaudado Real</div>
                        <div style='font-size: 1.8em; font-weight: bold; color: #ffffff;'>S/ 0.00</div>
                        <div style='font-size: 0.75em; color: rgba(255,255,255,0.6); margin-top: 5px;'>Sin datos disponibles</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col3:
            # Diferencia: Timming - Recaudado con visual mejorado
            if monto_recaudado_actual is not None:
                diferencia = acumulado_hoy - monto_recaudado_actual
                if diferencia > 0:
                    color_emoji = "🔴"  # Rojo: te falta dinero
                    estado = "FALTA"
                    color_bg = "#ffebee"
                    color_text = "#c62828"
                elif diferencia < 0:
                    color_emoji = "🟢"  # Verde: te sobra dinero
                    estado = "SOBRA"
                    color_bg = "#e8f5e9"
                    color_text = "#2e7d32"
                    diferencia = abs(diferencia)
                else:
                    color_emoji = "🟡"  # Amarillo: estás al día
                    estado = "AL DÍA"
                    color_bg = "#fff3e0"
                    color_text = "#f57c00"
                
                # HTML personalizado para Diferencia
                st.markdown(f"""
                    <div style='background-color: {color_bg}; padding: 15px; border-radius: 10px; border-left: 4px solid {color_text};'>
                        <div style='font-size: 0.85em; color: #666; margin-bottom: 5px;'>💰 Diferencia ({estado})</div>
                        <div style='font-size: 1.8em; font-weight: bold; color: {color_text};'>S/ {diferencia:,.2f}</div>
                        <div style='font-size: 0.75em; color: #999; margin-top: 5px;'>{color_emoji} {estado}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("💰 Diferencia", "Sin datos")
        
        with col4:
            if acumulado_hoy > 0 and monto_recaudado_actual is not None:
                # % de Avance: (Dinero Recaudado / Timming Esperado) * 100
                porcentaje_avance = (monto_recaudado_actual / acumulado_hoy) * 100
                color_emoji = "🟢" if porcentaje_avance >= 100 else "🟡" if porcentaje_avance >= 80 else "🔴"
                
                # HTML personalizado para Avance
                color_barra = "#4caf50" if porcentaje_avance >= 100 else "#ff9800" if porcentaje_avance >= 80 else "#f44336"
                st.markdown(f"""
                    <div style='background-color: #f5f5f5; padding: 15px; border-radius: 10px; border-left: 4px solid {color_barra};'>
                        <div style='font-size: 0.85em; color: #666; margin-bottom: 8px;'>{color_emoji} Avance vs Timming</div>
                        <div style='font-size: 1.8em; font-weight: bold; color: {color_barra};'>{porcentaje_avance:.1f}%</div>
                        <div style='background-color: #e0e0e0; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden;'>
                            <div style='background-color: {color_barra}; height: 100%; width: {min(porcentaje_avance, 100)}%; transition: width 0.3s;'></div>
                        </div>
                        <div style='font-size: 0.7em; color: #999; margin-top: 5px; text-align: right;'>{min(int(porcentaje_avance), 100)}% completado</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.metric("Avance vs Timming", "Sin datos")
        
        # Crear tabla visual
        st.markdown(f"### Detalle de {titulo}")
        
        # Preparar datos para tabla
        tabla_visual = datos[['Día hábil', 'Fecha', 'Timing', 'Meta día', 'Acumulado']].copy()
        tabla_visual['Día hábil'] = tabla_visual['Día hábil'].astype(int)
        tabla_visual['Fecha'] = tabla_visual['Fecha'].dt.strftime('%d-%b-%Y')
        tabla_visual['Timing'] = tabla_visual['Timing'].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else "-")
        tabla_visual['Meta día'] = tabla_visual['Meta día'].apply(lambda x: f"S/ {x:,.2f}" if pd.notna(x) else "-")
        tabla_visual['Acumulado'] = tabla_visual['Acumulado'].apply(lambda x: f"S/ {x:,.2f}" if pd.notna(x) else "-")
        
        # Mostrar tabla con alternancia de colores para el día actual
        html_tabla = "<table style='width:100%; border-collapse: collapse; font-size: 0.85em;'>"
        html_tabla += "<tr style='background-color: #e8e8e8; font-weight: bold;'>"
        for col in tabla_visual.columns:
            html_tabla += f"<th style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{col}</th>"
        html_tabla += "</tr>"
        
        for idx, row in tabla_visual.iterrows():
            if idx == fila_hoy:
                bg_color = "#fffacd"
                font_weight = "bold"
            else:
                bg_color = "#ffffff"
                font_weight = "normal"
            
            html_tabla += f"<tr style='background-color: {bg_color}; font-weight: {font_weight};'>"
            for col in tabla_visual.columns:
                html_tabla += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{row[col]}</td>"
            html_tabla += "</tr>"
        
        html_tabla += "</table>"
        st.markdown(html_tabla, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error al mostrar tabla: {str(e)}")

# Cargar y procesar datos de timming
df_timming_raw = cargar_timming()

if df_timming_raw is not None:
    # Extraer las 4 tablas
    tablas_timming = parsear_timming_data(df_timming_raw)
    
    # Crear tabs para las 2 tablas de gastos
    tab1, tab2 = st.tabs([
        "📊 Gastos General",
        "👥 Gastos por Asesor"
    ])
    
    # Mostrar cada tabla en su tab
    with tab1:
        st.markdown("#### 📊 TIMMING GENERAL GASTOS ADMINISTRATIVOS")
        mostrar_tabla_timming(tablas_timming.get('GASTOS_GENERAL'), "Gastos General", monto_worldtel_recaudado)
    
    with tab2:
        st.markdown("#### 👥 TIMMING ASESOR GASTOS")
        
        # Selector de asesor para esta pestaña
        asesores_worldtel = equipo_worldtel
        asesor_seleccionado = st.selectbox(
            "Selecciona un Asesor",
            options=asesores_worldtel,
            key="asesor_gastos"
        )
        
        # Obtener recaudado del asesor seleccionado
        monto_asesor = df[df['ASESOR'] == asesor_seleccionado]['MONTO'].sum()
        
        mostrar_tabla_timming(
            tablas_timming.get('GASTOS_ASESOR'), 
            "Gastos por Asesor",
            monto_recaudado_worldtel=monto_asesor,
            es_asesor=True,
            nombre_asesor=asesor_seleccionado,
            df_cierre=df
        )
    
else:
    st.warning("⚠️ No se pudo cargar el archivo de TIMMING. Verifica que el archivo existe en la ruta correcta.")