# 🇨🇱 Análisis Avanzado de la Fuerza de Trabajo en Chile

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Data Source: INE](https://img.shields.io/badge/Data%20Source-INE%20Chile-red)](https://www.ine.cl/)

## 📊 Descripción del Proyecto

Análisis profesional y exhaustivo de la **Fuerza de Trabajo en Chile** utilizando datos oficiales del Instituto Nacional de Estadísticas (INE). Este proyecto implementa las mejores prácticas de Data Science, siguiendo principios de Clean Code y SOLID para garantizar código mantenible, escalable y reproducible.

## 🎯 Objetivos

- **Análisis Exploratorio Completo**: Examinar patrones, tendencias y anomalías en la fuerza laboral chilena
- **Visualizaciones Profesionales**: Crear dashboards ejecutivos y gráficos de calidad publication-ready
- **Insights Económicos**: Generar conclusiones actionables sobre el mercado laboral
- **Código de Calidad**: Implementar arquitectura limpia y documentación exhaustiva

## 🏗️ Arquitectura del Proyecto

```
ine-chile-labour-force-analysis/
├── 📁 data/
│   ├── raw/           # Datos crudos del INE
│   ├── processed/     # Datos procesados y limpios
│   └── outputs/       # Resultados y exportaciones
├── 📁 src/
│   ├── etl/          # Extract, Transform, Load
│   ├── models/       # Modelos estadísticos y ML
│   ├── utils/        # Utilidades y helpers
│   └── visualization/ # Gráficos y dashboards
├── 📁 notebooks/     # Jupyter notebooks de análisis
├── 📁 scripts/       # Scripts de automatización
├── 📁 tests/         # Tests unitarios e integración
├── 📁 docs/          # Documentación del proyecto
└── 📁 logs/          # Logs del sistema
```

## 🚀 Configuración del Entorno

### Prerrequisitos
- Python 3.8+
- Git
- Virtual Environment

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/SanMaBruno/ine-chile-labour-force-analysis.git
cd ine-chile-labour-force-analysis
```

2. **Crear y activar entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Instalar el proyecto en modo desarrollo**
```bash
pip install -e .
```

## 📈 Uso del Proyecto

### Análisis Exploratorio
```bash
jupyter notebook notebooks/01_eda_labour_force.ipynb
```

### Procesamiento de Datos
```python
from src.etl.data_processor import LabourForceProcessor

processor = LabourForceProcessor()
df_clean = processor.process_raw_data("data/raw/ENE_FDT_*.csv")
```

### Visualizaciones
```python
from src.visualization.charts import LabourForceCharts

charts = LabourForceCharts()
charts.plot_unemployment_trends()
charts.create_regional_dashboard()
```

## 📊 Datasets y Variables

### Fuente de Datos: INE Chile
- **Encuesta Nacional de Empleo (ENE)**
- **Fuerza de Trabajo por región y sexo**
- **Series temporales 2010-2025**

### Variables Principales
- `Fuerza de Trabajo`: Total de personas ocupadas y desocupadas
- `Tasa de Participación`: Proporción de la PET que forma parte de la fuerza de trabajo
- `Tasa de Ocupación`: Proporción de ocupados respecto a la PET
- `Tasa de Desocupación`: Proporción de desocupados respecto a la fuerza de trabajo

## 🔍 Análisis Implementados

### 1. Análisis Temporal
- Tendencias de participación laboral
- Estacionalidad en el empleo
- Impacto de eventos económicos

### 2. Análisis Regional
- Comparación entre regiones
- Mapas de calor de indicadores laborales
- Análisis de convergencia regional

### 3. Análisis por Género
- Brecha de género en participación laboral
- Evolución histórica de la participación femenina
- Análisis de sectores por género

### 4. Análisis Predictivo
- Modelos de forecasting
- Detección de anomalías
- Proyecciones de indicadores clave

## 🛠️ Tecnologías Utilizadas

### Core Data Science
- **pandas**: Manipulación y análisis de datos
- **numpy**: Computación científica
- **scipy**: Estadística avanzada

### Visualización
- **matplotlib**: Gráficos base
- **seaborn**: Visualizaciones estadísticas
- **plotly**: Dashboards interactivos

### Machine Learning
- **scikit-learn**: Modelos predictivos
- **statsmodels**: Análisis estadístico

### Calidad de Código
- **black**: Formateo de código
- **flake8**: Linting
- **pytest**: Testing
- **mypy**: Type checking

## 📋 Mejores Prácticas Implementadas

### Clean Code
- Nombres descriptivos y funciones pequeñas
- Principio DRY (Don't Repeat Yourself)
- Comentarios claros y documentación

### SOLID Principles
- **S**: Single Responsibility Principle
- **O**: Open/Closed Principle
- **L**: Liskov Substitution Principle
- **I**: Interface Segregation Principle
- **D**: Dependency Inversion Principle

### Data Science Best Practices
- Versionado de datos
- Reproducibilidad de experimentos
- Validación de datos
- Logging y monitoreo

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=src

# Tests específicos
pytest tests/test_etl/
```

## 📝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## 👨‍💻 Autor

**Bruno San Martin**
- GitHub: [@SanMaBruno](https://github.com/SanMaBruno)
- LinkedIn: [Bruno San Martin](https://www.linkedin.com/in/sanmabruno/)


## 📊 Roadmap

- [ ] Dashboard web interactivo
- [ ] API REST para consultas
- [ ] Integración con bases de datos
- [ ] Análisis de sentiment de noticias laborales
- [ ] Modelos de deep learning para forecasting

---

**¡Explora, analiza y contribuye al entendimiento del mercado laboral chileno!** 🚀📈
