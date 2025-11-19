# Dashboard Análisis Comparativo WORLDTEL vs GI CORONADO

## 📊 Descripción

Dashboard interactivo desarrollado con Streamlit para visualizar y analizar el cierre de pagos comparativo entre dos equipos: **WORLDTEL** y **GI CORONADO**.

El dashboard presenta:
- Análisis jerárquico por cartera y asesor
- Comparativa de montos y clientes
- Gráficos interactivos con Plotly
- Desglose detallado por cartera

## 🚀 Características

- **Tablas Jerárquicas**: Visualización de carteras con asesores asociados
- **Métricas Comparativas**: Montos totales, clientes y asesores por equipo
- **Gráficos Interactivos**: Análisis por cartera y desempeño individual
- **Tabla HOY x HOY**: Análisis cruzado de fechas de gestión vs fechas de promesa
- **Filtrado por Equipo**: Botones para filtrar entre WORLDTEL, GI CORONADO o TODOS
- **Formato en Moneda Local**: Todos los montos expresados en Soles Peruanos (S/)
- **Interfaz Responsive**: Diseño adaptado para diferentes tamaños de pantalla

## 📋 Requisitos

- Python 3.8 o superior
- Ver `requirements.txt` para las dependencias específicas

## 💻 Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/isaac24012000-oss/ANALISIS-COMPARATIVO.git
cd ANALISIS-COMPARATIVO
```

2. **Crear un entorno virtual**
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

### Ejecución Local
```bash
streamlit run dashboard.py
```

El dashboard se abrirá en tu navegador (por defecto en `http://localhost:8501`)

### Despliegue en Streamlit Cloud

1. **Sube tu repositorio a GitHub** incluyendo:
   - `dashboard.py`
   - `requirements.txt` o `requirements-light.txt`
   - `ANALISIS WORLDTEL.xlsx` (el archivo de datos)
   - `README.md`
   - `.gitignore`

2. **Accede a [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Crea una nueva app**:
   - Conecta tu repositorio de GitHub
   - Selecciona la rama `main`
   - Especifica el archivo principal: `dashboard.py`
   - En configuración avanzada, asegúrate de usar `requirements-light.txt` si tienes problemas

4. **Importante**: El archivo `ANALISIS WORLDTEL.xlsx` DEBE estar en la raíz del repositorio para que Streamlit Cloud lo encuentre

## 📁 Estructura del Proyecto

```
.
├── dashboard.py              # Archivo principal de la aplicación
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
├── .gitignore               # Archivos a ignorar en git
└── ANALISIS WORLDTEL.xlsx   # Datos fuente (no incluido en git)
```

## 📊 Fuente de Datos

El dashboard lee datos del archivo Excel:
```
ANALISIS WORLDTEL.xlsx
```

Ubicación esperada: `./ANALISIS WORLDTEL.xlsx`

**Nota**: Este archivo no se incluye en el repositorio por razones de confidencialidad.

### Hojas del Libro Excel

El archivo contiene dos hojas principales:

#### 1. **CIERRE DE PAGOS**
Contiene el análisis comparativo entre WORLDTEL y GI CORONADO:
- **Cartera**: Nombre de la cartera (hierárquica)
- **Asesor**: Nombre del asesor
- **EQUIPO**: WORLDTEL o GI CORONADO
- **MONTO**: Monto en Soles Peruanos (S/)
- **CLIENTES**: Cantidad de clientes
- **PROMESA**: Estado de promesa de pago

Visualización: Tabla jerárquica con gráficos comparativos.

#### 2. **GESTIONES**
Contiene el registro detallado de gestiones de cobro:
- **FECHA_GESTION**: Fecha en la que se realizó la gestión
- **FECHA_PROMESA**: Fecha de la promesa de pago
- **MONTO_PROMESA**: Monto de la promesa en S/
- **EQUIPO**: WORLDTEL o GI CORONADO

Visualización: **Tabla HOY x HOY** (Tabla Cruzada)
- **Filas**: Fechas de gestión (DD/MM/AA)
- **Columnas**: Fechas de promesa (DD/MM/AA)
- **Valores**: Montos prometidos
- **Filtros**: Botones para seleccionar equipo

## 🎨 Personalización

### Tabla HOY x HOY
La tabla HOY x HOY muestra un análisis cruzado de fechas:
- **Filas (HOY 1)**: Fecha en que se realizó la gestión de cobro
- **Columnas (HOY 2)**: Fecha en que el cliente prometió pagar
- **Celdas**: Monto total prometido para esa combinación de fechas

**Cómo usar**:
1. Selecciona el equipo usando los botones (WORLDTEL, GI CORONADO o TODOS)
2. La tabla se actualiza automáticamente
3. Observa el patrón de gestiones vs promesas
4. La fila "TOTAL" muestra el monto por fecha de promesa
5. La columna "TOTAL" muestra el monto por fecha de gestión

### Cambiar equipos
Edita la lista `equipo_worldtel` en `dashboard.py`:
```python
equipo_worldtel = [
    'Nombre Asesor 1',
    'Nombre Asesor 2',
    # ... más asesores
]
```

### Cambiar ruta del archivo de datos
Modifica la variable `ruta_archivo` en la función `cargar_datos()`:
```python
ruta_archivo = r"ruta/a/tu/archivo.xlsx"
```

## 📝 Cambios Recientes

### v2.0.0
- ✨ Nueva visualización: Tabla HOY x HOY (análisis cruzado de fechas)
- 📋 Lectura de segunda hoja "GESTIONES" del Excel
- 🔘 Filtrado por equipo con botones interactivos
- 📅 Formato de fecha estandarizado (DD/MM/AA)
- ✅ Interfaz optimizada y compactada

### v1.0.0
- Estructura jerárquica por carteras
- Tablas con colores destacados para carteras
- Todas las columnas reordenadas para mejor visualización
- Moneda en Soles Peruanos (S/)
- Gráficos comparativos mejorados

## 📦 Versiones de Dependencias

### Requisitos Recomendados (`requirements.txt`)
```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.0.0
openpyxl>=3.9.0
```

### Requisitos Ligeros (`requirements-light.txt`)
Para usar si tienes problemas de instalación en Streamlit Cloud:
```
streamlit>=1.0.0
pandas>=1.0.0
plotly>=5.0.0
openpyxl>=3.0.0
```

**Para actualizar paquetes**:
```bash
pip install --upgrade -r requirements.txt
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 📧 Contacto

Para preguntas o sugerencias, contacta al equipo de desarrollo.

## 🔧 Troubleshooting

### Error: "FileNotFoundError: ANALISIS WORLDTEL.xlsx"
Este error ocurre cuando el archivo Excel no está en la ubicación correcta.

**Solución**:
1. Asegúrate de que el archivo `ANALISIS WORLDTEL.xlsx` está en la **raíz del repositorio** (mismo nivel que `dashboard.py`)
2. Si estás en Streamlit Cloud, sube el archivo a GitHub
3. Si estás localmente, copia el archivo al directorio del proyecto
4. La aplicación busca el archivo automáticamente en varias ubicaciones

### Error: "Error installing requirements"
Si obtiene este error al desplegar en Streamlit Cloud:

**Opción 1**: Usar el archivo `requirements-light.txt` en lugar de `requirements.txt`
- En Streamlit Cloud, ve a "Manage App" > "Advanced settings"
- Cambia el archivo de requisitos a `requirements-light.txt`

**Opción 2**: Actualizar `requirements.txt` a versiones más flexibles
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Opción 3**: Instalar dependencias sin versiones específicas
```bash
pip install streamlit pandas plotly openpyxl
```

### Error: "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### El dashboard es lento
- Intenta borrar el cache de Streamlit: `streamlit cache clear`
- Reduce el tamaño del archivo de datos

### En Streamlit Cloud
Si despliegas en Streamlit Cloud y encuentras problemas:
1. Verifica que el archivo `requirements-light.txt` está en la raíz del repo
2. Asegúrate de que el archivo Excel está incluido en el repositorio
3. En "Manage App", verifica que no hay errores de Python en los logs
4. Intenta hacer "Reboot app" si persisten los errores

## 📚 Documentación Adicional

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
