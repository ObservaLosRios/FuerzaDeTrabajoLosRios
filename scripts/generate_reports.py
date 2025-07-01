#!/usr/bin/env python3
"""
Generador de reportes automatizados para Los Ríos
Crea reportes en PDF y HTML con análisis completo

Autor: Bruno San Martín
Universidad Austral de Chile
"""

import sys
from pathlib import Path
import argparse
import json
from datetime import datetime
from typing import Dict, Any

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

# Importaciones del proyecto
from src.etl.data_loader import LosRiosDataLoader
from src.utils.logger import setup_project_logging
from config import LosRiosConfig
import logging


class ReportGenerator:
    """
    Generador de reportes automatizados.
    
    Clean Code: Single Responsibility - solo generación de reportes
    """
    
    def __init__(self):
        """Inicializa el generador de reportes."""
        self.config = LosRiosConfig()
        self.loader = LosRiosDataLoader()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def generate_html_report(self, data_file: Path, analysis_files: Dict[str, Path]) -> Path:
        """
        Genera reporte HTML completo.
        
        Args:
            data_file: Archivo con datos procesados
            analysis_files: Diccionario con archivos de análisis
            
        Returns:
            Path del reporte HTML generado
        """
        try:
            # Cargar datos
            data = self.loader.load_processed_data(data_file.name)
            
            # Cargar resultados de análisis
            analysis_results = {}
            for analysis_type, file_path in analysis_files.items():
                with open(file_path, 'r', encoding='utf-8') as f:
                    analysis_results[analysis_type] = json.load(f)
            
            # Generar HTML
            html_content = self._create_html_content(data, analysis_results)
            
            # Guardar reporte
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = self.config.REPORTS_PATH / f"reporte_los_rios_{timestamp}.html"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Reporte HTML generado: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"Error generando reporte HTML: {str(e)}")
            raise
    
    def _create_html_content(self, data, analysis_results: Dict[str, Any]) -> str:
        """Crea contenido HTML del reporte."""
        
        # Extraer información clave
        labour_analysis = analysis_results.get('labour_analysis', {})
        demo_analysis = analysis_results.get('demographic_analysis', {})
        
        current_indicators = labour_analysis.get('current_indicators', {})
        executive_summary = labour_analysis.get('executive_summary', {})
        
        html_template = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Fuerza de Trabajo - Los Ríos</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #2c5530;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c5530;
            margin: 0;
            font-size: 2.5em;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-top: 10px;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 8px;
            border-left: 4px solid #2c5530;
        }}
        .section h2 {{
            color: #2c5530;
            margin-top: 0;
            font-size: 1.8em;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-card h3 {{
            margin: 0 0 10px 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .metric-card .value {{
            font-size: 2em;
            font-weight: bold;
            margin: 0;
        }}
        .findings ul {{
            list-style-type: none;
            padding: 0;
        }}
        .findings li {{
            background-color: #e8f5e8;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #2c5530;
        }}
        .recommendations ul {{
            list-style-type: none;
            padding: 0;
        }}
        .recommendations li {{
            background-color: #fff3cd;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .data-table th, .data-table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .data-table th {{
            background-color: #2c5530;
            color: white;
        }}
        .data-table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌲 Reporte de Fuerza de Trabajo</h1>
            <div class="subtitle">Región de Los Ríos (XIV) - Chile</div>
            <div class="subtitle">Generado el {datetime.now().strftime('%d de %B de %Y')}</div>
        </div>

        <div class="section">
            <h2>📊 Resumen Ejecutivo</h2>
            <p><strong>Región analizada:</strong> {executive_summary.get('region', 'Los Ríos')}</p>
            <p><strong>Período de datos:</strong> {data['ano_trimestre'].min()} - {data['ano_trimestre'].max()}</p>
            <p><strong>Registros analizados:</strong> {len(data):,}</p>
        </div>

        <div class="section">
            <h2>📈 Indicadores Clave Actuales</h2>
            <div class="metrics">
                <div class="metric-card">
                    <h3>Fuerza de Trabajo Total</h3>
                    <div class="value">{current_indicators.get('total_labour_force_formatted', 'N/A')}</div>
                </div>
                <div class="metric-card">
                    <h3>Participación Masculina</h3>
                    <div class="value">{current_indicators.get('male_participation_pct', 0)}%</div>
                </div>
                <div class="metric-card">
                    <h3>Participación Femenina</h3>
                    <div class="value">{current_indicators.get('female_participation_pct', 0)}%</div>
                </div>
                <div class="metric-card">
                    <h3>Último Período</h3>
                    <div class="value">{current_indicators.get('latest_period', 'N/A')}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔍 Hallazgos Principales</h2>
            <div class="findings">
                <ul>
                    {self._format_findings_list(executive_summary.get('key_findings', []))}
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>💡 Recomendaciones</h2>
            <div class="recommendations">
                <ul>
                    {self._format_recommendations_list(executive_summary.get('recommendations', []))}
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>📊 Estadísticas Descriptivas</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Métrica</th>
                        <th>Fuerza de Trabajo</th>
                        <th>Hombres</th>
                        <th>Mujeres</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Promedio</strong></td>
                        <td>{data['fuerza_de_trabajo'].mean():,.0f}</td>
                        <td>{data['hombres'].mean():,.0f}</td>
                        <td>{data['mujeres'].mean():,.0f}</td>
                    </tr>
                    <tr>
                        <td><strong>Máximo</strong></td>
                        <td>{data['fuerza_de_trabajo'].max():,.0f}</td>
                        <td>{data['hombres'].max():,.0f}</td>
                        <td>{data['mujeres'].max():,.0f}</td>
                    </tr>
                    <tr>
                        <td><strong>Mínimo</strong></td>
                        <td>{data['fuerza_de_trabajo'].min():,.0f}</td>
                        <td>{data['hombres'].min():,.0f}</td>
                        <td>{data['mujeres'].min():,.0f}</td>
                    </tr>
                    <tr>
                        <td><strong>Desviación Estándar</strong></td>
                        <td>{data['fuerza_de_trabajo'].std():,.0f}</td>
                        <td>{data['hombres'].std():,.0f}</td>
                        <td>{data['mujeres'].std():,.0f}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>📈 Análisis de Tendencias</h2>
            {self._format_trends_analysis(labour_analysis.get('historical_trends', {}))}
        </div>

        <div class="footer">
            <p><strong>Autor:</strong> Bruno San Martín - Universidad Austral de Chile</p>
            <p><strong>Fuente de datos:</strong> Instituto Nacional de Estadísticas (INE) - Chile</p>
            <p><strong>Metodología:</strong> Clean Code + Data Science Best Practices</p>
            <p>Reporte generado automáticamente el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def _format_findings_list(self, findings: list) -> str:
        """Formatea lista de hallazgos para HTML."""
        if not findings:
            return "<li>No se encontraron hallazgos específicos.</li>"
        
        return "".join([f"<li>{finding}</li>" for finding in findings])
    
    def _format_recommendations_list(self, recommendations: list) -> str:
        """Formatea lista de recomendaciones para HTML."""
        if not recommendations:
            return "<li>No se generaron recomendaciones específicas.</li>"
        
        return "".join([f"<li>{rec}</li>" for rec in recommendations])
    
    def _format_trends_analysis(self, trends: Dict[str, Any]) -> str:
        """Formatea análisis de tendencias para HTML."""
        if not trends or trends.get('error'):
            return "<p>No se pudo realizar análisis de tendencias.</p>"
        
        total_trend = trends.get('total_labour_force', {})
        if not total_trend:
            return "<p>Datos de tendencias no disponibles.</p>"
        
        growth_rates = total_trend.get('growth_rates', {})
        
        html = f"""
        <div class="metrics">
            <div class="metric-card">
                <h3>Crecimiento Total</h3>
                <div class="value">{growth_rates.get('total_growth_pct', 0)}%</div>
            </div>
            <div class="metric-card">
                <h3>Crecimiento Anualizado</h3>
                <div class="value">{growth_rates.get('annual_growth_pct', 0)}%</div>
            </div>
            <div class="metric-card">
                <h3>Dirección de Tendencia</h3>
                <div class="value">{total_trend.get('trend_direction', 'N/A').title()}</div>
            </div>
            <div class="metric-card">
                <h3>Outliers Detectados</h3>
                <div class="value">{total_trend.get('outliers', 0)}</div>
            </div>
        </div>
        """
        
        return html


def parse_arguments():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Generador de reportes para análisis de Los Ríos'
    )
    
    parser.add_argument(
        '--data-file',
        type=str,
        required=True,
        help='Archivo con datos procesados'
    )
    
    parser.add_argument(
        '--labour-analysis',
        type=str,
        help='Archivo con resultados de análisis laboral (JSON)'
    )
    
    parser.add_argument(
        '--demographic-analysis',
        type=str,
        help='Archivo con resultados de análisis demográfico (JSON)'
    )
    
    parser.add_argument(
        '--output-format',
        type=str,
        choices=['html', 'pdf', 'both'],
        default='html',
        help='Formato de reporte de salida (default: html)'
    )
    
    return parser.parse_args()


def main():
    """Función principal del script."""
    # Configurar logging
    setup_project_logging()
    logger = logging.getLogger('los_rios_analysis.report_generator')
    
    # Parsear argumentos
    args = parse_arguments()
    
    logger.info("Iniciando generación de reportes")
    
    try:
        # Inicializar generador
        generator = ReportGenerator()
        
        # Preparar archivos de análisis
        analysis_files = {}
        
        if args.labour_analysis:
            analysis_files['labour_analysis'] = Path(args.labour_analysis)
        
        if args.demographic_analysis:
            analysis_files['demographic_analysis'] = Path(args.demographic_analysis)
        
        # Generar reportes según formato solicitado
        data_file = Path(args.data_file)
        
        if args.output_format in ['html', 'both']:
            html_report = generator.generate_html_report(data_file, analysis_files)
            print(f"✅ Reporte HTML generado: {html_report}")
        
        if args.output_format in ['pdf', 'both']:
            print("⚠️  Generación de PDF no implementada aún. Usar HTML por ahora.")
        
        logger.info("Generación de reportes completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error generando reportes: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
