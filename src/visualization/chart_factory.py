"""
Factory para creación de gráficos del análisis de Los Ríos
Clean Code: Factory Pattern para creación de visualizaciones
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any, Optional, Union
import logging

from ...config import LosRiosConfig, VisualizationConfig
from ..utils.logger import setup_logger
from ..utils.helpers import HelperFunctions


class ChartFactory:
    """
    Factory para crear diferentes tipos de gráficos.
    
    Clean Code: Factory Pattern - centraliza creación de visualizaciones
    """
    
    def __init__(self, config: Optional[LosRiosConfig] = None):
        """Inicializa la factory de gráficos."""
        self.config = config or LosRiosConfig()
        self.viz_config = VisualizationConfig()
        self.logger = setup_logger(self.__class__.__name__)
        self.helpers = HelperFunctions()
        
        # Configurar estilo
        self._setup_plotting_style()
    
    def _setup_plotting_style(self) -> None:
        """Configura el estilo de los gráficos."""
        # Matplotlib/Seaborn
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
        
        # Configuración general
        plt.rcParams.update({
            'figure.figsize': (12, 8),
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 11
        })
    
    def create_time_series_chart(
        self, 
        data: pd.DataFrame, 
        y_column: str,
        title: str = None,
        chart_type: str = "plotly"
    ) -> Union[plt.Figure, go.Figure]:
        """
        Crea gráfico de serie temporal.
        
        Args:
            data: DataFrame con datos temporales
            y_column: Columna para el eje Y
            title: Título del gráfico
            chart_type: Tipo de gráfico ("plotly" o "matplotlib")
            
        Returns:
            Figura del gráfico
        """
        try:
            if chart_type == "plotly":
                return self._create_plotly_time_series(data, y_column, title)
            else:
                return self._create_matplotlib_time_series(data, y_column, title)
                
        except Exception as e:
            self.logger.error(f"Error creando gráfico de serie temporal: {str(e)}")
            raise
    
    def create_gender_comparison_chart(
        self, 
        data: pd.DataFrame,
        chart_type: str = "plotly"
    ) -> Union[plt.Figure, go.Figure]:
        """Crea gráfico de comparación por género."""
        try:
            if not all(col in data.columns for col in ['hombres', 'mujeres', 'ano_trimestre']):
                raise ValueError("Columnas requeridas no encontradas")
            
            if chart_type == "plotly":
                return self._create_plotly_gender_comparison(data)
            else:
                return self._create_matplotlib_gender_comparison(data)
                
        except Exception as e:
            self.logger.error(f"Error creando gráfico de género: {str(e)}")
            raise
    
    def create_distribution_chart(
        self, 
        data: pd.Series,
        chart_type: str = "plotly",
        bins: int = 30
    ) -> Union[plt.Figure, go.Figure]:
        """Crea gráfico de distribución."""
        try:
            if chart_type == "plotly":
                return self._create_plotly_distribution(data, bins)
            else:
                return self._create_matplotlib_distribution(data, bins)
                
        except Exception as e:
            self.logger.error(f"Error creando gráfico de distribución: {str(e)}")
            raise
    
    def create_correlation_heatmap(
        self, 
        correlation_matrix: pd.DataFrame,
        chart_type: str = "plotly"
    ) -> Union[plt.Figure, go.Figure]:
        """Crea mapa de calor de correlaciones."""
        try:
            if chart_type == "plotly":
                return self._create_plotly_heatmap(correlation_matrix)
            else:
                return self._create_matplotlib_heatmap(correlation_matrix)
                
        except Exception as e:
            self.logger.error(f"Error creando mapa de calor: {str(e)}")
            raise
    
    def create_trend_analysis_chart(
        self, 
        data: pd.DataFrame,
        y_column: str,
        chart_type: str = "plotly"
    ) -> Union[plt.Figure, go.Figure]:
        """Crea gráfico de análisis de tendencia."""
        try:
            if chart_type == "plotly":
                return self._create_plotly_trend_analysis(data, y_column)
            else:
                return self._create_matplotlib_trend_analysis(data, y_column)
                
        except Exception as e:
            self.logger.error(f"Error creando análisis de tendencia: {str(e)}")
            raise
    
    def _create_plotly_time_series(
        self, 
        data: pd.DataFrame, 
        y_column: str, 
        title: str = None
    ) -> go.Figure:
        """Crea serie temporal con Plotly."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['ano_trimestre'],
            y=data[y_column],
            mode='lines+markers',
            name=y_column.replace('_', ' ').title(),
            line=dict(color=self.viz_config.PRIMARY_COLOR, width=3),
            marker=dict(size=8)
        ))
        
        # Añadir línea de tendencia
        if len(data) > 2:
            import numpy as np
            x_numeric = np.arange(len(data))
            z = np.polyfit(x_numeric, data[y_column], 1)
            trend_line = np.poly1d(z)(x_numeric)
            
            fig.add_trace(go.Scatter(
                x=data['ano_trimestre'],
                y=trend_line,
                mode='lines',
                name='Tendencia',
                line=dict(color='red', width=2, dash='dash'),
                opacity=0.7
            ))
        
        fig.update_layout(
            title=title or f'Evolución de {y_column.replace("_", " ").title()} - Los Ríos',
            xaxis_title='Período',
            yaxis_title=y_column.replace('_', ' ').title(),
            template='plotly_white',
            height=600,
            font=dict(size=12)
        )
        
        return fig
    
    def _create_plotly_gender_comparison(self, data: pd.DataFrame) -> go.Figure:
        """Crea comparación por género con Plotly."""
        fig = go.Figure()
        
        # Línea para hombres
        fig.add_trace(go.Scatter(
            x=data['ano_trimestre'],
            y=data['hombres'],
            mode='lines+markers',
            name='Hombres',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        # Línea para mujeres
        fig.add_trace(go.Scatter(
            x=data['ano_trimestre'],
            y=data['mujeres'],
            mode='lines+markers',
            name='Mujeres',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        # Área sombreada entre las líneas
        fig.add_trace(go.Scatter(
            x=data['ano_trimestre'].tolist() + data['ano_trimestre'].tolist()[::-1],
            y=data['hombres'].tolist() + data['mujeres'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(128,128,128,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Brecha de género',
            showlegend=False
        ))
        
        fig.update_layout(
            title='Participación Laboral por Género - Los Ríos',
            xaxis_title='Período',
            yaxis_title='Número de Personas',
            template='plotly_white',
            height=600,
            font=dict(size=12)
        )
        
        return fig
    
    def _create_plotly_distribution(self, data: pd.Series, bins: int) -> go.Figure:
        """Crea distribución con Plotly."""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=data,
            nbinsx=bins,
            name='Distribución',
            marker_color=self.viz_config.PRIMARY_COLOR,
            opacity=0.7
        ))
        
        # Añadir línea de media
        mean_value = data.mean()
        fig.add_vline(
            x=mean_value,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Media: {mean_value:.0f}"
        )
        
        fig.update_layout(
            title=f'Distribución de {data.name or "Valores"}',
            xaxis_title='Valor',
            yaxis_title='Frecuencia',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def _create_plotly_heatmap(self, correlation_matrix: pd.DataFrame) -> go.Figure:
        """Crea mapa de calor con Plotly."""
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.round(3).values,
            texttemplate="%{text}",
            textfont={"size": 10},
            colorbar=dict(title="Correlación")
        ))
        
        fig.update_layout(
            title='Matriz de Correlaciones',
            template='plotly_white',
            height=600,
            width=600
        )
        
        return fig
    
    def _create_plotly_trend_analysis(self, data: pd.DataFrame, y_column: str) -> go.Figure:
        """Crea análisis de tendencia con Plotly."""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=['Serie Original', 'Cambios Porcentuales'],
            vertical_spacing=0.1
        )
        
        # Serie original
        fig.add_trace(
            go.Scatter(
                x=data['ano_trimestre'],
                y=data[y_column],
                mode='lines+markers',
                name='Original',
                line=dict(color=self.viz_config.PRIMARY_COLOR, width=2)
            ),
            row=1, col=1
        )
        
        # Cambios porcentuales
        pct_changes = data[y_column].pct_change() * 100
        colors = ['green' if x > 0 else 'red' for x in pct_changes]
        
        fig.add_trace(
            go.Bar(
                x=data['ano_trimestre'],
                y=pct_changes,
                name='Cambio %',
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f'Análisis de Tendencia - {y_column.replace("_", " ").title()}',
            template='plotly_white',
            height=800,
            showlegend=False
        )
        
        return fig
    
    def _create_matplotlib_time_series(
        self, 
        data: pd.DataFrame, 
        y_column: str, 
        title: str = None
    ) -> plt.Figure:
        """Crea serie temporal con Matplotlib."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(data['ano_trimestre'], data[y_column], 
                marker='o', linewidth=2, markersize=6)
        
        ax.set_title(title or f'Evolución de {y_column.replace("_", " ").title()} - Los Ríos')
        ax.set_xlabel('Período')
        ax.set_ylabel(y_column.replace('_', ' ').title())
        ax.grid(True, alpha=0.3)
        
        # Rotar etiquetas del eje x
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def _create_matplotlib_gender_comparison(self, data: pd.DataFrame) -> plt.Figure:
        """Crea comparación por género con Matplotlib."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(data['ano_trimestre'], data['hombres'], 
                marker='o', linewidth=2, label='Hombres', color='blue')
        ax.plot(data['ano_trimestre'], data['mujeres'], 
                marker='s', linewidth=2, label='Mujeres', color='red')
        
        ax.fill_between(data['ano_trimestre'], data['hombres'], data['mujeres'], 
                       alpha=0.3, color='gray')
        
        ax.set_title('Participación Laboral por Género - Los Ríos')
        ax.set_xlabel('Período')
        ax.set_ylabel('Número de Personas')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def _create_matplotlib_distribution(self, data: pd.Series, bins: int) -> plt.Figure:
        """Crea distribución con Matplotlib."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.hist(data, bins=bins, alpha=0.7, color=self.viz_config.PRIMARY_COLOR, edgecolor='black')
        ax.axvline(data.mean(), color='red', linestyle='--', 
                  label=f'Media: {data.mean():.0f}')
        
        ax.set_title(f'Distribución de {data.name or "Valores"}')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        return fig
    
    def _create_matplotlib_heatmap(self, correlation_matrix: pd.DataFrame) -> plt.Figure:
        """Crea mapa de calor con Matplotlib."""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap='RdBu_r', 
                   center=0,
                   square=True,
                   ax=ax)
        
        ax.set_title('Matriz de Correlaciones')
        plt.tight_layout()
        
        return fig
    
    def _create_matplotlib_trend_analysis(self, data: pd.DataFrame, y_column: str) -> plt.Figure:
        """Crea análisis de tendencia con Matplotlib."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Serie original
        ax1.plot(data['ano_trimestre'], data[y_column], 
                marker='o', linewidth=2)
        ax1.set_title('Serie Original')
        ax1.set_ylabel(y_column.replace('_', ' ').title())
        ax1.grid(True, alpha=0.3)
        
        # Cambios porcentuales
        pct_changes = data[y_column].pct_change() * 100
        colors = ['green' if x > 0 else 'red' for x in pct_changes]
        ax2.bar(data['ano_trimestre'], pct_changes, color=colors, alpha=0.7)
        ax2.set_title('Cambios Porcentuales')
        ax2.set_xlabel('Período')
        ax2.set_ylabel('Cambio %')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
