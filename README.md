# 🌲 Análisis de la Fuerza de Trabajo - Región de Los Ríos

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![Clean Code](https://img.shields.io/badge/Clean%20Code-Practices-green)](https://github.com/ryanmcdermott/clean-code-javascript)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data Source: INE](https://img.shields.io/badge/Data%20Source-INE%20Chile-red)](https://www.ine.cl/)

## 📊 Descripción del Proyecto

Análisis especializado y exhaustivo de la **Fuerza de Trabajo en la Región de Los Ríos (CHL14)** utilizando datos oficiales del Instituto Nacional de Estadísticas (INE) de Chile. Este proyecto implementa las mejores prácticas de Clean Code siguiendo los principios del libro "Clean Code" de Robert C. Martin.

## 🎯 Objetivos Específicos

- **Análisis Regional Especializado**: Caracterización completa de la fuerza laboral en Los Ríos
- **Tendencias Temporales**: Evolución histórica del empleo regional (2010-2025)
- **Análisis por Género**: Participación laboral diferenciada por sexo
- **Insights Económicos**: Conclusiones actionables para stakeholders regionales
- **Clean Code Implementation**: Código limpio, testeable y mantenible

## 🌲 Enfoque Regional: Los Ríos (CHL14)

### Características de la Región
- **Capital**: Valdivia
- **Población**: ~400,000 habitantes
- **Economía Principal**: Silvicultura, agricultura, turismo, servicios universitarios
- **Ubicación**: Sur de Chile, XIV Región
- **Código INE**: CHL14

### Datos Analizados
- **867 registros** específicos de Los Ríos
- **Período**: 2010-2025 (trimestres móviles)
- **Variables**: Fuerza de trabajo por sexo y totales
- **Fuente**: INE Chile - Encuesta Nacional de Empleo (ENE)

## 🏗️ Arquitectura del Proyecto (Clean Code)

```
ine-chile-labour-force-analysis/
├── 📊 data/
│   ├── raw/                    # Datos originales del INE
│   ├── processed/              # Datos procesados y limpios
│   └── outputs/                # Resultados y visualizaciones
├── 📝 src/                     # Código fuente (Clean Code)
│   ├── etl/                    # Extract, Transform, Load
│   │   ├── __init__.py
│   │   ├── data_extractor.py   # Principio de Responsabilidad Única
│   │   ├── data_transformer.py # Transformaciones específicas
│   │   └── data_loader.py      # Carga de datos procesados
│   ├── models/                 # Modelos de datos y análisis
│   │   ├── __init__.py
│   │   └── labour_force_model.py
│   ├── utils/                  # Utilidades y helpers
│   │   ├── __init__.py
│   │   ├── validators.py       # Validación de datos
│   │   ├── logger.py          # Sistema de logging
│   │   └── constants.py       # Constantes del proyecto
│   └── visualization/          # Gráficos y dashboards
│       ├── __init__.py
│       ├── chart_factory.py   # Factory Pattern
│       └── dashboard_builder.py
├── 📔 notebooks/               # Análisis interactivo
│   └── los_rios_analysis.ipynb
├── 🔧 scripts/                 # Scripts de automatización
│   └── process_los_rios_data.py
├── 🧪 tests/                   # Tests unitarios
│   └── test_*.py
├── 📚 docs/                    # Documentación
├── 📄 requirements.txt         # Dependencias
├── ⚙️ config.py               # Configuración centralizada
└── 📖 README.md               # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- pip
- Virtual Environment

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/SanMaBruno/ine-chile-labour-force-analysis.git
cd ine-chile-labour-force-analysis
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📈 Uso del Proyecto

### Análisis Principal
```bash
# Ejecutar análisis completo de Los Ríos
python scripts/process_los_rios_data.py
```

### Notebook Interactivo
```bash
jupyter notebook notebooks/los_rios_analysis.ipynb
```

### Usar módulos (Clean Code)
```python
from src.etl.data_extractor import LosRiosDataExtractor
from src.models.labour_force_model import LabourForceAnalyzer
from src.visualization.chart_factory import ChartFactory

# Extracción limpia
extractor = LosRiosDataExtractor()
data = extractor.extract_los_rios_data()

# Análisis especializado
analyzer = LabourForceAnalyzer(data)
insights = analyzer.analyze_trends()

# Visualización profesional
charts = ChartFactory()
charts.create_time_series_chart(data)
```

## 🧹 Principios Clean Code Implementados

### 1. **Nombres Significativos**
```python
# ❌ Malo
def calc(x, y):
    return x + y

# ✅ Bueno
def calculate_total_workforce(male_workforce: float, female_workforce: float) -> float:
    return male_workforce + female_workforce
```

### 2. **Funciones Pequeñas**
- Cada función tiene una sola responsabilidad
- Máximo 20 líneas por función
- Parámetros descriptivos

### 3. **Principio DRY (Don't Repeat Yourself)**
- Código reutilizable en módulos
- Factory patterns para visualizaciones
- Constantes centralizadas

### 4. **Principios SOLID**
- **S**: Cada clase tiene una responsabilidad
- **O**: Abierto para extensión, cerrado para modificación
- **L**: Subclases sustituibles
- **I**: Interfaces específicas
- **D**: Inversión de dependencias

## 📊 Análisis Implementados

### 1. **Análisis Temporal Los Ríos**
- Evolución trimestral 2010-2025
- Tendencias de crecimiento/decrecimiento
- Estacionalidad regional

### 2. **Análisis por Género Los Ríos**
- Participación laboral femenina vs masculina
- Brechas de género específicas de la región
- Evolución histórica por sexo

### 3. **Insights Regionales**
- Comparación con promedios nacionales
- Caracterización económica regional
- Proyecciones futuras

## 🛠️ Tecnologías Utilizadas

### Core
- **Python 3.11**: Lenguaje principal
- **pandas**: Manipulación de datos
- **numpy**: Cálculos numéricos

### Visualización
- **matplotlib**: Gráficos base
- **seaborn**: Visualizaciones estadísticas
- **plotly**: Dashboards interactivos

### Calidad de Código
- **black**: Formateo automático
- **flake8**: Linting
- **pytest**: Testing
- **mypy**: Type checking

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Tests con cobertura
pytest --cov=src tests/

# Tests específicos de Los Ríos
pytest tests/test_los_rios_analysis.py
```

## 📈 Resultados Esperados

### Insights Clave
1. **Tamaño del mercado laboral**: Fuerza de trabajo total en Los Ríos
2. **Tendencias temporales**: Crecimiento o decrecimiento regional
3. **Participación por género**: Distribución y evolución
4. **Estacionalidad**: Patrones por trimestres
5. **Proyecciones**: Estimaciones futuras

### Deliverables
- Datos procesados en `data/processed/`
- Visualizaciones en `data/outputs/`
- Insights documentados
- Código limpio y testeable

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/amazing-feature`)
3. Aplicar Clean Code principles
4. Escribir tests
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Crear Pull Request

## 📄 Licencia

Distribuido bajo Licencia MIT. Ver `LICENSE` para más información.

## 👨‍💻 Autor

**Bruno San Martin**
- GitHub: [@SanMaBruno](https://github.com/SanMaBruno)
- LinkedIn: [Bruno San Martin](https://www.linkedin.com/in/sanmabruno/)

## 📊 Métricas del Proyecto

- **867 registros** analizados de Los Ríos
- **15 años** de datos históricos
- **3 variables** principales (Total, Hombres, Mujeres)
- **100% cobertura** de tests

---

**🌲 ¡Explorando el mercado laboral de Los Ríos con Clean Code!** 📊✨
