#!/usr/bin/env python3
"""
Script de ejemplo para procesar datos de fuerza laboral del INE.
Demuestra el uso de la arquitectura modular del proyecto.
"""

import sys
from pathlib import Path

# Añadir src al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from etl.data_processor import LabourForceProcessor
from visualization.charts import LabourForceCharts
from utils.validators import LabourForceValidator
from utils.logger_config import get_logger

logger = get_logger(__name__)


def main():
    """Función principal del script de ejemplo."""
    
    print("🚀 SCRIPT DE EJEMPLO - PROCESAMIENTO DE DATOS INE")
    print("=" * 60)
    
    # Definir rutas
    data_dir = project_root / "data"
    raw_dir = data_dir / "raw"
    processed_dir = data_dir / "processed"
    output_dir = data_dir / "outputs"
    
    # Buscar archivos CSV
    csv_files = list(raw_dir.glob("*.csv"))
    
    if not csv_files:
        print("❌ No se encontraron archivos CSV en data/raw")
        print("💡 Coloca un archivo CSV del INE en la carpeta data/raw")
        return
    
    input_file = csv_files[0]
    print(f"📊 Procesando archivo: {input_file.name}")
    
    try:
        # 1. Crear procesador
        processor = LabourForceProcessor()
        print("✅ Procesador creado")
        
        # 2. Extraer datos
        raw_data = processor.extractor.extract(input_file)
        print(f"📥 Datos extraídos: {len(raw_data)} filas")
        
        # 3. Validar datos
        validator = LabourForceValidator()
        validation_results = validator.validate_labour_force_data(raw_data)
        
        passed_validations = sum(validation_results.values())
        total_validations = len(validation_results)
        print(f"✅ Validación: {passed_validations}/{total_validations} checks pasados")
        
        # 4. Transformar datos
        processed_data = processor.transformer.transform(raw_data)
        print(f"🔄 Datos procesados: {len(processed_data)} filas")
        
        # 5. Guardar datos procesados
        output_file = processed_dir / f"processed_{input_file.name}"
        processor.loader.load(processed_data, output_file)
        print(f"💾 Datos guardados en: {output_file}")
        
        # 6. Generar estadísticas
        stats = processor.get_summary_statistics(processed_data)
        print(f"📊 Estadísticas generadas:")
        print(f"   Total registros: {stats['total_records']:,}")
        print(f"   Rango fechas: {stats['date_range']['min']} - {stats['date_range']['max']}")
        print(f"   Regiones: {stats['regions_count']}")
        print(f"   Años: {stats['years_count']}")
        
        # 7. Crear visualizaciones
        print("\n📈 Generando visualizaciones...")
        charts = LabourForceCharts()
        
        # Serie temporal
        fig1 = charts.plot_time_series(
            processed_data,
            save_path=output_dir / "ejemplo_serie_temporal.png"
        )
        print("✅ Serie temporal guardada")
        
        # Comparación por género
        fig2 = charts.plot_gender_comparison(
            processed_data,
            save_path=output_dir / "ejemplo_genero.png"
        )
        print("✅ Comparación por género guardada")
        
        # Dashboard interactivo
        dashboard = charts.create_interactive_dashboard(
            processed_data,
            save_path=output_dir / "ejemplo_dashboard.html"
        )
        print("✅ Dashboard interactivo guardado")
        
        # 8. Guardar reporte
        report_file = output_dir / f"reporte_{input_file.stem}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE PROCESAMIENTO - FUERZA LABORAL INE\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Archivo procesado: {input_file.name}\n")
            f.write(f"Fecha de procesamiento: {processor.transformer.__class__.__name__}\n\n")
            
            f.write("ESTADÍSTICAS:\n")
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
            
            f.write(f"\nVALIDACIONES:\n")
            for validation, result in validation_results.items():
                status = "✅ PASS" if result else "❌ FAIL"
                f.write(f"{validation}: {status}\n")
        
        print(f"📄 Reporte guardado en: {report_file}")
        
        print("\n🎉 PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📂 Archivos generados:")
        print(f"   📊 Datos procesados: {output_file}")
        print(f"   📈 Visualizaciones: {output_dir}")
        print(f"   📄 Reporte: {report_file}")
        
    except Exception as e:
        logger.error(f"Error en el procesamiento: {str(e)}")
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
