# 📊 Dashboard Fuerza de Trabajo - Región de Los Ríos

<div align="center">

![Los Ríos Banner](https://img.shields.io/badge/Región-Los%20Ríos%20(XIV)-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-ff6692?style=for-the-badge&logo=plotly)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter)

[![Universidad Austral de Chile](https://img.shields.io/badge/UACh-Universidad%20Austral%20de%20Chile-blue)](https://www.uach.cl/)
[![INE Chile](https://img.shields.io/badge/Datos-INE%20Chile-red)](https://www.ine.cl/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🎯 Análisis Profesional de la Fuerza Laboral en Los Ríos con Visualizaciones Interactivas**

[📊 Ver Dashboards](#-dashboards-interactivos) • [🚀 Instalación](#-instalación-rápida) • [📈 Resultados](#-resultados-clave) • [👨‍💻 Autor](#-autor)

---

</div>

## 🌟 **Descripción del Proyecto**

**Dashboard Fuerza de Trabajo Los Ríos** es un análisis profesional e interactivo de la evolución del mercado laboral en la **Región de Los Ríos (XIV)** de Chile. Utilizando datos oficiales del **Instituto Nacional de Estadísticas (INE)**, este proyecto presenta visualizaciones de alto impacto con **estilo The Economist** y accesibilidad para daltonismo.

### ✨ **Características Principales**

- 📈 **Visualizaciones Interactivas**: Gráficos dinámicos con Plotly y estilo profesional
- 🎨 **Diseño The Economist**: Tipografía Georgia y paleta de colores elegante  
- ♿ **Accesibilidad Total**: Colores amigables para daltonismo (Paleta Wong)
- 📊 **Dashboard Integral**: 4 paneles con análisis multidimensional
- 🔍 **Análisis Temporal**: Evolución 2010-2024 con proyecciones 2025-2027
- 👥 **Análisis de Género**: Participación femenina y brecha salarial
- 📱 **Responsive Design**: Optimizado para diferentes dispositivos

## 🎯 **Región de Los Ríos - Contexto del Análisis**

<table>
<tr>
<td width="50%">

### 📍 **Información Regional**
- **🏛️ Capital**: Valdivia
- **👥 Población**: ~400,000 habitantes  
- **📊 Código INE**: CHL14
- **🌍 Ubicación**: Sur de Chile (XIV Región)
- **🏞️ Superficie**: 18,429 km²

</td>
<td width="50%">

### 💼 **Economía Principal**
- **🌲 Silvicultura**: Industria forestal y celulosa
- **🌾 Agricultura**: Producción agropecuaria
- **🎓 Educación**: Servicios universitarios (UACh)
- **🏞️ Turismo**: Turismo natural y cultural
- **⚙️ Manufactura**: Industria alimentaria

</td>
</tr>
</table>

### 📊 **Datos del Proyecto**

| **Aspecto** | **Detalle** |
|-------------|-------------|
| **📈 Registros Analizados** | 867 observaciones específicas de Los Ríos |
| **⏰ Período Temporal** | 2010-2024 (trimestres móviles) + proyecciones 2025-2027 |
| **👥 Segmentación** | Análisis por género (Hombres, Mujeres, Total) |
| **🏢 Fuente de Datos** | Instituto Nacional de Estadísticas (INE) - Chile |
| **📋 Indicador Principal** | Fuerza de trabajo (miles de personas) |
| **🔄 Actualización** | Datos hasta segundo trimestre 2024 |

---

## 📊 **Dashboards Interactivos**

### � **Dashboard 1: Evolución Temporal**

Análisis dinámico de la **evolución histórica** de la fuerza de trabajo (2010-2024) con:

- 📈 **Líneas de tendencia** por género con suavizado spline
- 📍 **Anotaciones clave**: COVID-19, crecimiento participación femenina  
- 🎨 **Estilo The Economist**: Tipografía Georgia, colores profesionales
- 🔍 **Interactividad completa**: Hover detallado y navegación temporal
- 📊 **Estadísticas integradas**: Correlaciones, proyecciones y métricas

### 🎯 **Dashboard 2: Panel Demográfico Integral**

Dashboard multidimensional con **4 visualizaciones integradas**:

| **Panel** | **Visualización** | **Insights** |
|-----------|-------------------|--------------|
| **🥧 Superior Izquierdo** | Distribución por Género (Dona) | Composición actual 2024 |
| **📈 Superior Derecho** | Evolución Participación Femenina | Tendencias de inclusión (+0.34 pp/año) |
| **📊 Inferior Izquierdo** | Comparación por Décadas | Análisis generacional (2020s = mejor década) |
| **⚖️ Inferior Derecho** | Brecha de Género Histórica | Evolución diferencias H-M (-23.5 miles) |

---

## 🚀 **Instalación Rápida**

### 📋 **Prerrequisitos**

- **🐍 Python**: 3.11 o superior
- **📦 pip**: Gestor de paquetes
- **🔧 Git**: Control de versiones

### ⚡ **Instalación en 3 Pasos**

```bash
# 1️⃣ Clonar el repositorio
git clone https://github.com/ObservaLosRios/FuerzaDeTrabajoLosRios.git
cd FuerzaDeTrabajoLosRios

# 2️⃣ Crear y activar entorno virtual  
python -m venv .venv
source .venv/bin/activate    # 🐧 Linux/Mac
# .venv\Scripts\activate     # 🪟 Windows

# 3️⃣ Instalar dependencias
pip install -r requirements.txt
```

### 🚀 **Ejecución Rápida**

```bash
# Ejecutar notebook principal
jupyter notebook notebooks/dashboard_fuerza_trabajo_los_rios.ipynb

# O usar el notebook simplificado
jupyter notebook notebooks/fuerza_trabajo_los_rios.ipynb
```

---

## � **Resultados Clave**

<div align="center">

### 🏆 **Métricas Principales 2024**

| **Indicador** | **Valor** | **Tendencia** |
|---------------|-----------|---------------|
| **👥 Fuerza Laboral Total** | **202.5 miles** | +1.80 miles/año |
| **👩‍💼 Participación Femenina** | **44.2%** | +0.34 pp/año |
| **⚖️ Brecha de Género** | **23.5 miles** | Tendencia decreciente |
| **📊 Correlación Temporal** | **0.622** | Crecimiento sostenido |

</div>

### 🎯 **Insights Estratégicos**

#### 📈 **Tendencias Positivas**
- ✅ **Crecimiento sostenido**: +1.80 miles personas/año desde 2010
- ✅ **Inclusión femenina**: Incremento constante desde 2020 (+0.34 pp/año)
- ✅ **Reducción brecha**: Diferencias de género en declive progresivo
- ✅ **Resilencia post-COVID**: Recuperación acelerada desde 2021

#### 🔮 **Proyecciones 2025-2027**
- **2025**: 200.4 miles personas
- **2026**: 202.2 miles personas  
- **2027**: 204.0 miles personas

#### 🏆 **Décadas de Crecimiento**
- **Mejor década para mujeres**: 2020s (77.7 miles promedio)
- **Mayor dinamismo**: Período post-2020 con políticas inclusivas
- **Estabilidad estructural**: Correlación temporal robusta (r=0.622)

---

## 🛠️ **Stack Tecnológico**

<div align="center">

### 📊 **Análisis de Datos**
![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)

### 📈 **Visualización**
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge)

### 🔧 **Desarrollo**
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

### � **Dependencias Principales**

```python
# Análisis de datos
pandas >= 2.2.0          # Manipulación de datos
numpy >= 1.26.3          # Cálculos numéricos
scipy >= 1.12.0          # Análisis estadístico

# Visualización interactiva  
plotly >= 5.18.0         # Gráficos interactivos
matplotlib >= 3.8.0     # Visualizaciones base

# Entorno de desarrollo
jupyter >= 1.0.0         # Notebooks interactivos
```

---

## 🎨 **Características de Diseño**

### 🎭 **Estilo The Economist**

- **📝 Tipografía**: Georgia serif (estándar editorial)
- **🎨 Paleta de colores**: Basada en The Economist style guide
- **📏 Layout**: Grid responsive con espaciado armónico
- **🔍 Interactividad**: Hover detallado y navegación intuitiva

### ♿ **Accesibilidad**

- **🌈 Paleta Wong**: Colores distinguibles para daltonismo
- **📊 Contraste alto**: Texto legible en todas las condiciones
- **📱 Responsive**: Funciona en móviles, tablets y desktop
- **⌨️ Navegación**: Compatible con lectores de pantalla

### 🎯 **Principios de Diseño**

```python
# Paleta de colores optimizada para daltonismo
economist_colors = {
    'Ambos sexos': '#0173B2',  # Azul robusto
    'Hombres': '#DE8F05',      # Naranja dorado  
    'Mujeres': '#CC78BC'       # Rosa púrpura
}

# Configuración tipográfica
font_config = {
    'family': 'Georgia, serif',
    'color': '#1e293b',
    'title_size': 22,
    'axis_size': 14
}
```

---

## 📁 **Estructura del Proyecto**
```
FuerzaDeTrabajoLosRios/
├── 📊 data/                           # Datos del proyecto
│   ├── raw/                          # Datos originales INE
│   │   └── ENE_FDT_01072025123700776.csv
│   ├── processed/                    # Datos limpios y procesados
│   │   └── los_rios_clean_data_*.csv
│   └── outputs/                      # Resultados y exportaciones
│       └── reports/
├── 📔 notebooks/                      # Análisis interactivos
│   ├── 01_analisis_completo_los_rios.ipynb   # Análisis completo
│   ├── dashboard_fuerza_trabajo_los_rios.ipynb # Dashboard principal
│   └── fuerza_trabajo_los_rios.ipynb         # Versión simplificada
├── 📝 src/                           # Código fuente modular
│   ├── etl/                          # Extract, Transform, Load
│   │   ├── data_extractor.py         # Extracción de datos
│   │   ├── data_transformer.py       # Transformaciones
│   │   └── data_loader.py            # Carga optimizada
│   ├── models/                       # Modelos de análisis
│   │   ├── demographics.py           # Análisis demográfico
│   │   ├── labour_analyzer.py        # Análisis laboral
│   │   └── statistics_engine.py      # Motor estadístico
│   ├── visualization/                # Gráficos y dashboards
│   │   ├── chart_factory.py          # Factory de gráficos
│   │   └── dashboard_builder.py      # Constructor dashboards
│   └── utils/                        # Utilidades
│       ├── helpers.py                # Funciones auxiliares
│       ├── logger.py                 # Sistema de logging
│       └── validators.py             # Validación datos
├── 🔧 scripts/                       # Scripts automatización
│   ├── generate_reports.py           # Generación reportes
│   └── process_los_rios_data.py      # Procesamiento datos
├── 🧪 tests/                         # Tests unitarios
│   ├── test_analyzers.py
│   └── test_data_extractor.py
├── 📚 docs/                          # Documentación
├── 📄 requirements.txt               # Dependencias Python
├── ⚙️ config.py                     # Configuración centralizada
├── 📋 LICENSE                        # Licencia MIT
└── 📖 README.md                      # Este archivo
```

---

## � **Guía de Uso**

### 🎯 **Opción 1: Dashboard Completo** *(Recomendado)*

```bash
# Notebook principal con todas las visualizaciones
jupyter notebook notebooks/dashboard_fuerza_trabajo_los_rios.ipynb
```

**Incluye:**
- ✅ Importaciones optimizadas
- ✅ Configuración de estilos profesionales  
- ✅ Evolución temporal interactiva
- ✅ Dashboard demográfico integral (4 paneles)
- ✅ Métricas y estadísticas clave
- ✅ Documentación completa

### 🎯 **Opción 2: Análisis Exploratorio**

```bash
# Análisis completo con EDA detallado
jupyter notebook notebooks/01_analisis_completo_los_rios.ipynb
```

**Incluye:**
- 🔍 Análisis exploratorio exhaustivo
- 📊 Estadísticas descriptivas
- 📈 Múltiples visualizaciones
- 🔄 Pipeline ETL completo
- 💾 Exportación de resultados

### 🎯 **Opción 3: Uso Programático**

```python
# Importar módulos del proyecto
from src.etl.data_extractor import LosRiosDataExtractor
from src.models.labour_analyzer import LabourAnalyzer
from src.visualization.chart_factory import ChartFactory

# Pipeline básico
extractor = LosRiosDataExtractor()
data = extractor.extract()

analyzer = LabourAnalyzer(data)
insights = analyzer.analyze_trends()

charts = ChartFactory()
fig = charts.create_evolution_chart(data)
fig.show()
```

---

## 📊 **Metodología de Análisis**

### 🔬 **Proceso ETL**

1. **📥 Extracción**
   - Datos oficiales INE Chile
   - Filtrado específico Los Ríos (CHL14)
   - Validación de integridad

2. **🔄 Transformación**  
   - Limpieza de valores nulos
   - Creación de variables derivadas
   - Agregaciones temporales

3. **📊 Carga**
   - Datos procesados en CSV
   - Estructura optimizada para análisis
   - Metadatos y documentación

### 📈 **Análisis Estadístico**

- **Regresión lineal**: Tendencias temporales y proyecciones
- **Análisis de correlación**: Relaciones entre variables
- **Estadística descriptiva**: Medidas centrales y dispersión
- **Análisis de outliers**: Detección valores atípicos
- **Análisis de brechas**: Diferencias de género

### 🎨 **Visualización**

- **Gráficos temporales**: Evolución histórica con líneas de tendencia
- **Dashboard interactivo**: 4 paneles con análisis multidimensional
- **Paleta accesible**: Colores optimizados para daltonismo
- **Estilo profesional**: Diseño basado en The Economist

---

## 🤝 **Contribución**

¡Las contribuciones son bienvenidas! Sigue estos pasos:

### 🔧 **Para Desarrolladores**

1. **🍴 Fork** el proyecto
2. **🌿 Crear rama** feature (`git checkout -b feature/nueva-funcionalidad`)
3. **📝 Escribir código** siguiendo estándares del proyecto
4. **🧪 Agregar tests** para nuevas funcionalidades
5. **💾 Commit** cambios (`git commit -m 'Add: nueva funcionalidad'`)
6. **🚀 Push** a la rama (`git push origin feature/nueva-funcionalidad`) 
7. **📬 Crear Pull Request**

### 📊 **Para Analistas**

- 📈 Nuevas visualizaciones o métricas
- 🔍 Análisis adicionales por sectores económicos
- 📅 Extensión a otras regiones de Chile
- 📋 Mejoras en documentación

### 🎨 **Para Diseñadores**

- 🎭 Nuevos estilos de visualización
- ♿ Mejoras en accesibilidad
- 📱 Optimizaciones responsive
- 🌈 Paletas de colores adicionales

---

## � **Soporte y Contacto**

### 🆘 **Reportar Problemas**

- 🐛 **Bugs**: [Issues en GitHub](https://github.com/ObservaLosRios/FuerzaDeTrabajoLosRios/issues)
- 💡 **Sugerencias**: [Discussions](https://github.com/ObservaLosRios/FuerzaDeTrabajoLosRios/discussions)
- 📧 **Email**: bruno.sanmartin@uach.cl

### ❓ **FAQ**

<details>
<summary><strong>¿Cómo actualizar los datos con nueva información del INE?</strong></summary>

1. Descargar nuevos datos INE
2. Colocar en `data/raw/`
3. Ejecutar `scripts/process_los_rios_data.py`
4. Re-ejecutar notebooks para actualizar visualizaciones

</details>

<details>
<summary><strong>¿Puedo adaptar este análisis para otra región?</strong></summary>

Sí, el código es modular. Modifica los filtros en `config.py` para cambiar la región objetivo.

</details>

<details>
<summary><strong>¿Cómo exportar las visualizaciones?</strong></summary>

Las visualizaciones Plotly se pueden exportar como PNG, PDF o HTML usando el menú de cada gráfico.

</details>

---

## 📄 **Licencia**

Este proyecto está licenciado bajo la **Licencia MIT** - ver el archivo [LICENSE](LICENSE) para detalles.

### 💼 **Uso Comercial**
- ✅ Uso comercial permitido
- ✅ Modificación permitida  
- ✅ Distribución permitida
- ✅ Uso privado permitido

### 📋 **Condiciones**
- 📝 Incluir licencia y copyright
- 📊 Citar fuente de datos (INE Chile)

---

## 👨‍💻 **Autor**

<div align="center">

### **Bruno San Martín Navarro**

🎓 **Universidad Austral de Chile (UACh)**  
📊 **Especialista en Análisis de Datos**  
🌲 **Investigador Mercado Laboral Los Ríos**

[![GitHub](https://img.shields.io/badge/GitHub-SanMaBruno-black?style=for-the-badge&logo=github)](https://github.com/SanMaBruno)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Bruno%20San%20Martín-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sanmabruno/)
[![Email](https://img.shields.io/badge/Email-bruno.sanmartin%40uach.cl-red?style=for-the-badge&logo=gmail)](mailto:bruno.sanmartin@uach.cl)

</div>

### 🏛️ **Afiliación Institucional**

- **🎓 Universidad Austral de Chile**: Apoyo institucional y recursos
- **📊 Observatorio Los Ríos**: Iniciativa de investigación regional
- **🏢 INE Chile**: Fuente oficial de datos estadísticos

---

## 🙏 **Agradecimientos**

### 📊 **Datos y Metodología**
- **Instituto Nacional de Estadísticas (INE) Chile** por proporcionar datos oficiales
- **Universidad Austral de Chile** por el apoyo institucional y recursos
- **Región de Los Ríos** por ser el objeto de estudio

### 🛠️ **Tecnología**
- **Plotly Team** por la librería de visualización interactiva
- **Pandas Development Team** por las herramientas de análisis de datos
- **Jupyter Project** por el entorno de desarrollo

### 🎨 **Diseño e Inspiración**
- **The Economist** por los estándares de diseño visual
- **Wong, B.** por la paleta de colores accesible para daltonismo
- **Tufte, E.** por los principios de visualización de datos

---

<div align="center">

### 🌟 **¡Si este proyecto te resulta útil, no olvides darle una ⭐!**

**🌲 Explorando el futuro laboral de Los Ríos con datos y visualización** 📊✨

---

*Última actualización: Julio 2025 | Versión: 2.0.0*

</div>
