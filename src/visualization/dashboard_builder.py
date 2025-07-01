"""
Constructor de dashboards para el análisis de Los Ríos
Clean Code: Builder Pattern para crear dashboards complejos
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import Dict, List, Any, Optional
import logging

from ...config import LosRiosConfig, VisualizationConfig
from ..utils.logger import setup_logger
from .chart_factory import ChartFactory


class DashboardBuilder:
    """
    Constructor de dashboards interactivos.
    
    Clean Code: Builder Pattern - construye dashboards paso a paso
    """
    
    def __init__(self, config: Optional[LosRiosConfig] = None):
        """Inicializa el constructor de dashboards."""
        self.config = config or LosRiosConfig()
        self.viz_config = VisualizationConfig()
        self.logger = setup_logger(self.__class__.__name__)
        self.chart_factory = ChartFactory(config)
        
    def create_comprehensive_dashboard(
        self, 
        data: pd.DataFrame,
        analysis_results: Dict[str, Any]
    ) -> go.Figure:
        """
        Crea dashboard completo del análisis.
        
        Args:
            data: DataFrame con datos de Los Ríos
            analysis_results: Resultados del análisis
            
        Returns:
            Dashboard interactivo de Plotly
        """
        try:
            # Crear subplots
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=[
                    'Evolución de la Fuerza de Trabajo',
                    'Distribución por Género',
                    'Tendencias por Género',
                    'Cambios Porcentuales',
                    'Indicadores Clave',
                    'Proyecciones'
                ],
                specs=[
                    [{"secondary_y": False}, {"secondary_y": False}],
                    [{"secondary_y": False}, {"secondary_y": False}],
                    [{"type": "indicator"}, {"secondary_y": False}]
                ],
                vertical_spacing=0.08,
                horizontal_spacing=0.08
            )
            
            # 1. Evolución de la fuerza de trabajo
            self._add_labour_force_evolution(fig, data, row=1, col=1)
            
            # 2. Distribución por género (pie chart)
            self._add_gender_distribution(fig, data, row=1, col=2)
            
            # 3. Tendencias por género
            self._add_gender_trends(fig, data, row=2, col=1)
            
            # 4. Cambios porcentuales
            self._add_percentage_changes(fig, data, row=2, col=2)
            
            # 5. Indicadores clave
            self._add_key_indicators(fig, analysis_results, row=3, col=1)
            
            # 6. Proyecciones
            self._add_forecasts(fig, data, analysis_results, row=3, col=2)
            
            # Configurar layout
            fig.update_layout(
                title={
                    'text': f'Dashboard de Análisis de Fuerza de Trabajo - {self.config.REGION_NAME}',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                template='plotly_white',
                height=1200,
                showlegend=True,
                font=dict(size=11)
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creando dashboard: {str(e)}")
            raise
    
    def create_gender_analysis_dashboard(self, data: pd.DataFrame) -> go.Figure:
        """Crea dashboard específico para análisis de género."""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    'Evolución Comparativa por Género',
                    'Participación Relativa (%)',
                    'Brecha de Género',
                    'Crecimiento Anual por Género'
                ],
                vertical_spacing=0.12
            )
            
            # Evolución comparativa
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=data['hombres'],
                    mode='lines+markers',
                    name='Hombres',
                    line=dict(color='blue', width=3)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=data['mujeres'],
                    mode='lines+markers',
                    name='Mujeres',
                    line=dict(color='red', width=3)
                ),
                row=1, col=1
            )
            
            # Participación relativa
            male_pct = (data['hombres'] / data['fuerza_de_trabajo']) * 100
            female_pct = (data['mujeres'] / data['fuerza_de_trabajo']) * 100
            
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=male_pct,
                    mode='lines',
                    name='% Hombres',
                    line=dict(color='blue', width=2)
                ),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=female_pct,
                    mode='lines',
                    name='% Mujeres',
                    line=dict(color='red', width=2)
                ),
                row=1, col=2
            )
            
            # Brecha de género
            gender_gap = abs(data['hombres'] - data['mujeres'])
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=gender_gap,
                    mode='lines+markers',
                    name='Brecha Absoluta',
                    line=dict(color='purple', width=2),
                    fill='tonexty'
                ),
                row=2, col=1
            )
            
            # Crecimiento anual
            male_growth = data['hombres'].pct_change() * 100
            female_growth = data['mujeres'].pct_change() * 100
            
            fig.add_trace(
                go.Bar(
                    x=data['ano_trimestre'],
                    y=male_growth,
                    name='Crecimiento Hombres (%)',
                    marker_color='lightblue',
                    opacity=0.7
                ),
                row=2, col=2
            )
            
            fig.add_trace(
                go.Bar(
                    x=data['ano_trimestre'],
                    y=female_growth,
                    name='Crecimiento Mujeres (%)',
                    marker_color='lightcoral',
                    opacity=0.7
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title='Análisis de Género - Fuerza de Trabajo Los Ríos',
                template='plotly_white',
                height=800,
                showlegend=True
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creando dashboard de género: {str(e)}")
            raise
    
    def create_trend_analysis_dashboard(self, data: pd.DataFrame) -> go.Figure:
        """Crea dashboard de análisis de tendencias."""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    'Serie Temporal Original',
                    'Tendencia y Componentes',
                    'Análisis de Volatilidad',
                    'Detección de Outliers'
                ]
            )
            
            # Serie original con tendencia
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=data['fuerza_de_trabajo'],
                    mode='lines+markers',
                    name='Datos Originales',
                    line=dict(color=self.viz_config.PRIMARY_COLOR, width=2)
                ),
                row=1, col=1
            )
            
            # Línea de tendencia
            import numpy as np
            x_numeric = np.arange(len(data))
            z = np.polyfit(x_numeric, data['fuerza_de_trabajo'], 1)
            trend_line = np.poly1d(z)(x_numeric)
            
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=trend_line,
                    mode='lines',
                    name='Tendencia Lineal',
                    line=dict(color='red', width=2, dash='dash')
                ),
                row=1, col=1
            )
            
            # Media móvil
            rolling_mean = data['fuerza_de_trabajo'].rolling(window=4).mean()
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=rolling_mean,
                    mode='lines',
                    name='Media Móvil (4 períodos)',
                    line=dict(color='green', width=2)
                ),
                row=1, col=2
            )
            
            # Desviación estándar móvil
            rolling_std = data['fuerza_de_trabajo'].rolling(window=4).std()
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'],
                    y=rolling_std,
                    mode='lines',
                    name='Volatilidad (4 períodos)',
                    line=dict(color='orange', width=2)
                ),
                row=2, col=1
            )
            
            # Detección de outliers
            from ..utils.helpers import HelperFunctions
            helpers = HelperFunctions()
            outliers = helpers.detect_outliers(data['fuerza_de_trabajo'])
            
            fig.add_trace(
                go.Scatter(
                    x=data['ano_trimestre'][~outliers],
                    y=data['fuerza_de_trabajo'][~outliers],
                    mode='markers',
                    name='Valores Normales',
                    marker=dict(color='blue', size=6)
                ),
                row=2, col=2
            )
            
            if outliers.any():
                fig.add_trace(
                    go.Scatter(
                        x=data['ano_trimestre'][outliers],
                        y=data['fuerza_de_trabajo'][outliers],
                        mode='markers',
                        name='Outliers',
                        marker=dict(color='red', size=10, symbol='x')
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                title='Análisis de Tendencias - Fuerza de Trabajo Los Ríos',
                template='plotly_white',
                height=800
            )
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creando dashboard de tendencias: {str(e)}")
            raise
    
    def _add_labour_force_evolution(self, fig: go.Figure, data: pd.DataFrame, row: int, col: int):
        """Añade evolución de fuerza de trabajo al dashboard."""
        fig.add_trace(
            go.Scatter(
                x=data['ano_trimestre'],
                y=data['fuerza_de_trabajo'],
                mode='lines+markers',
                name='Fuerza de Trabajo',
                line=dict(color=self.viz_config.PRIMARY_COLOR, width=3),
                marker=dict(size=6)
            ),
            row=row, col=col
        )
    
    def _add_gender_distribution(self, fig: go.Figure, data: pd.DataFrame, row: int, col: int):
        """Añade distribución por género."""
        latest_data = data.iloc[-1]
        
        fig.add_trace(
            go.Pie(
                labels=['Hombres', 'Mujeres'],
                values=[latest_data['hombres'], latest_data['mujeres']],
                hole=0.3,
                marker_colors=['lightblue', 'lightcoral']
            ),
            row=row, col=col
        )
    
    def _add_gender_trends(self, fig: go.Figure, data: pd.DataFrame, row: int, col: int):
        """Añade tendencias por género."""
        fig.add_trace(
            go.Scatter(
                x=data['ano_trimestre'],
                y=data['hombres'],
                mode='lines',
                name='Hombres',
                line=dict(color='blue', width=2)
            ),
            row=row, col=col
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['ano_trimestre'],
                y=data['mujeres'],
                mode='lines',
                name='Mujeres',
                line=dict(color='red', width=2)
            ),
            row=row, col=col
        )
    
    def _add_percentage_changes(self, fig: go.Figure, data: pd.DataFrame, row: int, col: int):
        """Añade cambios porcentuales."""
        pct_changes = data['fuerza_de_trabajo'].pct_change() * 100
        colors = ['green' if x > 0 else 'red' for x in pct_changes]
        
        fig.add_trace(
            go.Bar(
                x=data['ano_trimestre'],
                y=pct_changes,
                name='Cambio %',
                marker_color=colors,
                opacity=0.7
            ),
            row=row, col=col
        )
    
    def _add_key_indicators(self, fig: go.Figure, analysis_results: Dict[str, Any], row: int, col: int):
        """Añade indicadores clave."""
        current = analysis_results.get('current_indicators', {})
        
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=current.get('total_labour_force', 0),
                title={"text": "Fuerza de Trabajo Total"},
                number={'suffix': " personas", 'font': {'size': 20}},
                domain={'row': row-1, 'column': col-1}
            ),
            row=row, col=col
        )
    
    def _add_forecasts(self, fig: go.Figure, data: pd.DataFrame, analysis_results: Dict[str, Any], row: int, col: int):
        """Añade proyecciones."""
        # Serie histórica
        fig.add_trace(
            go.Scatter(
                x=data['ano_trimestre'],
                y=data['fuerza_de_trabajo'],
                mode='lines',
                name='Histórico',
                line=dict(color='blue', width=2)
            ),
            row=row, col=col
        )
        
        # Proyección simple
        forecasts = analysis_results.get('forecasts', {})
        if forecasts and not forecasts.get('error'):
            projections = forecasts.get('projections', {})
            if projections:
                # Crear períodos futuros (simplificado)
                next_periods = ['2025-Q1', '2025-Q2']  # Ejemplo
                projected_values = [
                    projections.get('next_quarter', 0),
                    projections.get('quarter_after', 0)
                ]
                
                fig.add_trace(
                    go.Scatter(
                        x=next_periods,
                        y=projected_values,
                        mode='lines+markers',
                        name='Proyección',
                        line=dict(color='red', width=2, dash='dash'),
                        marker=dict(size=8, symbol='diamond')
                    ),
                    row=row, col=col
                )
