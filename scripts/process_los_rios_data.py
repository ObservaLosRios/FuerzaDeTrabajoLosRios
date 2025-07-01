#!/usr/bin/env python3
"""
Script principal para procesar datos de Los Ríos
Automatiza todo el pipeline de ETL y análisis

Autor: Bruno San Martín
Universidad Austral de Chile
"""

import sys
from pathlib import Path
import argparse
import logging
from datetime import datetime

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

# Importaciones del proyecto
from src.etl.data_extractor import LosRiosDataExtractor
from src.etl.data_transformer import LosRiosDataTransformer
from src.etl.data_loader import LosRiosDataLoader
from src.models.labour_analyzer import LabourAnalyzer
from src.models.demographics import DemographicsAnalyzer
from src.visualization.dashboard_builder import DashboardBuilder
from src.utils.logger import setup_project_logging, PerformanceLogger
from config import LosRiosConfig


def setup_logging():
    """Configura el sistema de logging."""
    setup_project_logging()
    return logging.getLogger('los_rios_analysis.main_script')


def parse_arguments():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Procesamiento completo de datos de fuerza de trabajo - Los Ríos'
    )
    
    parser.add_argument(
        '--input-file',
        type=str,
        help='Archivo CSV de entrada (opcional, usa configuración por defecto)'
    )
    
    parser.add_argument(
        '--output-format',
        type=str,
        choices=['csv', 'parquet', 'excel'],
        default='csv',
        help='Formato de archivo de salida (default: csv)'
    )
    
    parser.add_argument(
        '--skip-analysis',
        action='store_true',
        help='Solo procesar datos, sin ejecutar análisis'
    )
    
    parser.add_argument(
        '--skip-visualization',
        action='store_true',
        help='No generar visualizaciones'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Salida detallada'
    )
    
    return parser.parse_args()


def extract_data(extractor: LosRiosDataExtractor, input_file: str = None) -> tuple:
    """
    Extrae datos de Los Ríos.
    
    Returns:
        Tupla (datos_extraidos, es_exitoso)
    """
    try:
        if input_file:
            # Cargar archivo específico
            raw_data = extractor.load_custom_file(input_file)
        else:
            # Usar archivo por defecto
            raw_data = extractor.load_ine_data()
        
        los_rios_data = extractor.extract_los_rios_data()
        
        return los_rios_data, True
        
    except Exception as e:
        logging.error(f"Error en extracción de datos: {str(e)}")
        return None, False


def transform_data(transformer: LosRiosDataTransformer, data) -> tuple:
    """
    Transforma y limpia los datos.
    
    Returns:
        Tupla (datos_transformados, es_exitoso)
    """
    try:
        clean_data = transformer.transform(data)
        return clean_data, True
        
    except Exception as e:
        logging.error(f"Error en transformación de datos: {str(e)}")
        return None, False


def perform_analysis(data, skip_analysis: bool = False) -> dict:
    """
    Realiza análisis completo de los datos.
    
    Returns:
        Diccionario con todos los resultados
    """
    if skip_analysis:
        return {"analysis_skipped": True}
    
    try:
        results = {}
        
        # Análisis del mercado laboral
        labour_analyzer = LabourAnalyzer()
        results['labour_analysis'] = labour_analyzer.analyze_labour_market(data)
        
        # Análisis demográfico
        demographics_analyzer = DemographicsAnalyzer()
        results['demographic_analysis'] = demographics_analyzer.analyze_demographic_structure(data)
        
        return results
        
    except Exception as e:
        logging.error(f"Error en análisis: {str(e)}")
        return {"error": str(e)}


def create_visualizations(data, analysis_results, skip_viz: bool = False) -> list:
    """
    Crea visualizaciones y dashboards.
    
    Returns:
        Lista de archivos de visualización creados
    """
    if skip_viz:
        return []
    
    try:
        viz_files = []
        dashboard_builder = DashboardBuilder()
        loader = LosRiosDataLoader()
        
        # Dashboard comprensivo
        comprehensive_dashboard = dashboard_builder.create_comprehensive_dashboard(
            data, analysis_results.get('labour_analysis', {})
        )
        
        comp_file = loader.save_visualization(
            comprehensive_dashboard,
            "comprehensive_dashboard_automated",
            format_type="html"
        )
        viz_files.append(comp_file)
        
        # Dashboard de género
        gender_dashboard = dashboard_builder.create_gender_analysis_dashboard(data)
        gender_file = loader.save_visualization(
            gender_dashboard,
            "gender_dashboard_automated",
            format_type="html"
        )
        viz_files.append(gender_file)
        
        return viz_files
        
    except Exception as e:
        logging.error(f"Error creando visualizaciones: {str(e)}")
        return []


def save_results(data, analysis_results, output_format: str) -> dict:
    """
    Guarda todos los resultados procesados.
    
    Returns:
        Diccionario con información de archivos guardados
    """
    try:
        loader = LosRiosDataLoader()
        saved_files = {}
        
        # Guardar datos procesados
        data_file = loader.save_processed_data(
            data,
            filename="los_rios_automated_processing",
            format_type=output_format
        )
        saved_files['processed_data'] = data_file
        
        # Guardar resultados de análisis
        if not analysis_results.get('analysis_skipped'):
            if 'labour_analysis' in analysis_results:
                labour_file = loader.save_analysis_results(
                    analysis_results['labour_analysis'],
                    "labour_analysis_automated",
                    format_type="json"
                )
                saved_files['labour_analysis'] = labour_file
            
            if 'demographic_analysis' in analysis_results:
                demo_file = loader.save_analysis_results(
                    analysis_results['demographic_analysis'],
                    "demographic_analysis_automated",
                    format_type="json"
                )
                saved_files['demographic_analysis'] = demo_file
        
        return saved_files
        
    except Exception as e:
        logging.error(f"Error guardando resultados: {str(e)}")
        return {}


def print_summary(data, analysis_results, saved_files, viz_files, elapsed_time):
    """Imprime resumen del procesamiento."""
    print("\n" + "="*60)
    print("🌲 RESUMEN DE PROCESAMIENTO - LOS RÍOS")
    print("="*60)
    
    print(f"⏱️  Tiempo total de procesamiento: {elapsed_time:.2f} segundos")
    print(f"📊 Registros procesados: {len(data):,}")
    print(f"📅 Período de datos: {data['ano_trimestre'].min()} - {data['ano_trimestre'].max()}")
    
    print(f"\n💾 Archivos guardados:")
    for file_type, file_path in saved_files.items():
        print(f"   • {file_type}: {file_path.name}")
    
    if viz_files:
        print(f"\n📊 Visualizaciones creadas:")
        for viz_file in viz_files:
            print(f"   • {viz_file.name}")
    
    if not analysis_results.get('analysis_skipped'):
        # Mostrar hallazgos clave
        labour_analysis = analysis_results.get('labour_analysis', {})
        current_indicators = labour_analysis.get('current_indicators', {})
        
        if current_indicators and not current_indicators.get('error'):
            print(f"\n🔍 Indicadores clave:")
            print(f"   • Último período: {current_indicators.get('latest_period', 'N/A')}")
            print(f"   • Fuerza de trabajo: {current_indicators.get('total_labour_force_formatted', 'N/A')}")
            print(f"   • Participación masculina: {current_indicators.get('male_participation_pct', 0)}%")
            print(f"   • Participación femenina: {current_indicators.get('female_participation_pct', 0)}%")
    
    print(f"\n✅ Procesamiento completado exitosamente!")


def main():
    """Función principal del script."""
    # Configurar argumentos y logging
    args = parse_arguments()
    logger = setup_logging()
    
    # Configurar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Inicializar performance logger
    perf_logger = PerformanceLogger("main_processing")
    perf_logger.start()
    
    config = LosRiosConfig()
    
    logger.info("Iniciando procesamiento automático de datos de Los Ríos")
    logger.info(f"Configuración: {config.REGION_NAME} ({config.REGION_CODE})")
    
    try:
        # 1. Extracción de datos
        logger.info("Iniciando extracción de datos...")
        extractor = LosRiosDataExtractor()
        data, extract_success = extract_data(extractor, args.input_file)
        
        if not extract_success:
            logger.error("Fallo en extracción de datos")
            sys.exit(1)
        
        perf_logger.checkpoint("data_extraction")
        
        # 2. Transformación de datos
        logger.info("Iniciando transformación de datos...")
        transformer = LosRiosDataTransformer()
        clean_data, transform_success = transform_data(transformer, data)
        
        if not transform_success:
            logger.error("Fallo en transformación de datos")
            sys.exit(1)
        
        perf_logger.checkpoint("data_transformation")
        
        # 3. Análisis de datos
        logger.info("Iniciando análisis de datos...")
        analysis_results = perform_analysis(clean_data, args.skip_analysis)
        
        perf_logger.checkpoint("data_analysis")
        
        # 4. Crear visualizaciones
        logger.info("Creando visualizaciones...")
        viz_files = create_visualizations(
            clean_data, 
            analysis_results, 
            args.skip_visualization
        )
        
        perf_logger.checkpoint("visualizations")
        
        # 5. Guardar resultados
        logger.info("Guardando resultados...")
        saved_files = save_results(clean_data, analysis_results, args.output_format)
        
        # 6. Resumen final
        elapsed_time = perf_logger.end("Procesamiento completo finalizado")
        
        print_summary(clean_data, analysis_results, saved_files, viz_files, elapsed_time)
        
        logger.info("Procesamiento automático completado exitosamente")
        
    except Exception as e:
        logger.error(f"Error crítico en procesamiento: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
