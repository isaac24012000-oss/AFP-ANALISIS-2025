import sys
import traceback

try:
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from datetime import datetime
    import streamlit as st
    
    print("Todas las importaciones exitosas")
    
    # Ejecutar línea por línea del dashboard
    ruta = r"C:\Users\USUARIO\Desktop\REPORTE MENSUAL WORLDTEL\DASHBOARD ANALISIS\WORLDTEL ANALISIS\ANALISIS WORLDTEL.xlsx"
    df = pd.read_excel(ruta, sheet_name='CIERRE DE PAGOS', engine='openpyxl')
    print("Datos cargados correctamente")
    
    equipo_worldtel = [
        'Laura Villanueva Solayo',
        'Cherry Nathalia Matson Zambrano',
        'Sandra Maria Benavides Vela',
        'Carmen Dora Niño Ordinola',
        'Daniel Alejandro Barrios Pavon',
        'Juan Jose Felix Ventura',
        'Rosa Elena Villarreal Pelaez',
        'Carla del Rosario Castillo Alvarez',
        'Lesly Dayanne Zarate Roman'
    ]
    
    df['EQUIPO'] = df['ASESOR'].apply(lambda x: 'WORLDTEL' if x in equipo_worldtel else 'GI CORONADO')
    df = df[df['ASESOR'].notna() & (df['ASESOR'] != 'ESTUDIO')].copy()
    print("Equipos clasificados")
    
    # NUEVA SECCIÓN - Evolucion de pagos
    df_fecha_equipo = df.copy()
    df_fecha_equipo = df_fecha_equipo[df_fecha_equipo['FECHA_DE_PAGO'].notna()].copy()
    print(f"Registros con fecha: {len(df_fecha_equipo)}")
    
    df_fecha_equipo['FECHA'] = pd.to_datetime(df_fecha_equipo['FECHA_DE_PAGO']).dt.normalize()
    print("Fechas normalizadas")
    
    evolucion_pagos = df_fecha_equipo.groupby(['FECHA', 'EQUIPO']).agg({
        'MONTO': 'sum'
    }).reset_index()
    print("Groupby ejecutado correctamente")
    
    evolucion_pagos.columns = ['FECHA', 'EQUIPO', 'MONTO_DIARIO']
    evolucion_pagos = evolucion_pagos.sort_values('FECHA')
    print("Columnas renombradas y ordenadas")
    
    evolucion_pagos['MONTO_ACUMULADO'] = evolucion_pagos.groupby('EQUIPO')['MONTO_DIARIO'].cumsum()
    print("Acumulado calculado")
    
    print(f"\nUltimas 5 filas de evolucion_pagos:")
    print(evolucion_pagos.tail())
    
    print("\n¡TODO FUNCIONANDO CORRECTAMENTE!")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    traceback.print_exc()
    sys.exit(1)
