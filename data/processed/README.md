# Datos procesados

Esta carpeta contiene los datos que han sido procesados y limpiados por el pipeline ETL del proyecto.

## Estructura

- `labour_force_processed.csv` - Datos principales procesados de fuerza laboral
- `summary_statistics.json` - Resumen estadístico de los datos
- `validation_report.txt` - Reporte de validación de calidad de datos

## Uso

Los archivos en esta carpeta son generados automáticamente por:
- `src/etl/data_processor.py`
- `notebooks/01_eda_labour_force.ipynb`
- `scripts/example_processing.py`

No editar manualmente estos archivos.
