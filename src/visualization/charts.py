"""
Professional charts and visualizations for Labour Force analysis.
Following Clean Code and SOLID principles.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import warnings

from ..utils.logger_config import get_logger

logger = get_logger(__name__)

# Set style
plt.style.use('seaborn-v0_8')
warnings.filterwarnings('ignore')


class BaseChartMaker:
    """Base class for chart creation following SOLID principles."""
    
    def __init__(self, style: str = "seaborn-v0_8", figsize: Tuple[int, int] = (12, 8)):
        self.style = style
        self.figsize = figsize
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff7f0e',
            'info': '#17a2b8',
            'male': '#3498db',
            'female': '#e74c3c',
            'total': '#2c3e50'
        }
        
        # Set default style
        plt.style.use(self.style)
        sns.set_palette("husl")
    
    def save_figure(
        self,
        fig,
        filename: Union[str, Path],
        dpi: int = 300,
        bbox_inches: str = 'tight'
    ):
        """Save figure with consistent settings."""
        try:
            if hasattr(fig, 'write_image'):  # Plotly figure
                fig.write_image(filename, width=1200, height=800)
            else:  # Matplotlib figure
                fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, 
                           facecolor='white', edgecolor='none')
            
            logger.info(f"Chart saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save chart to {filename}: {str(e)}")


class LabourForceCharts(BaseChartMaker):
    """Specialized charts for Labour Force data analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def plot_time_series(
        self,
        data: pd.DataFrame,
        title: str = "Labour Force Time Series",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """Create time series plot of labour force data."""
        logger.info("Creating time series plot")
        
        # Filter for national total
        national_data = data[
            (data['region_code'] == '_T') & 
            (data['gender_code'] == '_T')
        ].copy()
        
        if len(national_data) == 0:
            logger.error("No national total data found")
            return None
        
        # Sort by date
        national_data = national_data.sort_values('date')
        
        # Create plot
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(
            national_data['date'],
            national_data['value'] / 1000,  # Convert to thousands
            linewidth=2.5,
            color=self.colors['primary'],
            marker='o',
            markersize=4,
            alpha=0.8
        )
        
        # Formatting
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Año', fontsize=12)
        ax.set_ylabel('Fuerza de Trabajo (miles de personas)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format y-axis
        ax.ticklabel_format(style='plain', axis='y')
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        # Add trend line
        z = np.polyfit(range(len(national_data)), national_data['value'], 1)
        p = np.poly1d(z)
        ax.plot(national_data['date'], p(range(len(national_data))) / 1000, 
                "--", alpha=0.7, color=self.colors['danger'], 
                label='Tendencia')
        
        ax.legend()
        plt.tight_layout()
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Time series plot created successfully")
        return fig
    
    def plot_gender_comparison(
        self,
        data: pd.DataFrame,
        title: str = "Participación Laboral por Género",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """Create gender comparison plot."""
        logger.info("Creating gender comparison plot")
        
        # Filter national data by gender
        gender_data = data[
            (data['region_code'] == '_T') & 
            (data['gender_code'].isin(['M', 'F']))
        ].copy()
        
        if len(gender_data) == 0:
            logger.error("No gender data found")
            return None
        
        # Create plot
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot by gender
        for gender_code, gender_name, color in [
            ('M', 'Hombres', self.colors['male']),
            ('F', 'Mujeres', self.colors['female'])
        ]:
            gender_subset = gender_data[gender_data['gender_code'] == gender_code].sort_values('date')
            
            ax.plot(
                gender_subset['date'],
                gender_subset['value'] / 1000,
                linewidth=2.5,
                color=color,
                marker='o',
                markersize=3,
                label=gender_name,
                alpha=0.8
            )
        
        # Formatting
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Año', fontsize=12)
        ax.set_ylabel('Fuerza de Trabajo (miles de personas)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Gender comparison plot created successfully")
        return fig
    
    def plot_regional_heatmap(
        self,
        data: pd.DataFrame,
        year: int = None,
        title: str = "Fuerza de Trabajo por Región",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """Create regional heatmap."""
        logger.info(f"Creating regional heatmap for year {year}")
        
        # Filter data
        regional_data = data[
            (data['region_code'] != '_T') & 
            (data['gender_code'] == '_T')
        ].copy()
        
        if year:
            regional_data = regional_data[regional_data['year'] == year]
        else:
            # Use latest year
            year = regional_data['year'].max()
            regional_data = regional_data[regional_data['year'] == year]
        
        if len(regional_data) == 0:
            logger.error(f"No regional data found for year {year}")
            return None
        
        # Pivot data for heatmap
        pivot_data = regional_data.pivot_table(
            index='region_name',
            values='value',
            aggfunc='mean'
        )
        
        # Create plot
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Create heatmap
        sns.heatmap(
            pivot_data.values.reshape(-1, 1),
            yticklabels=pivot_data.index,
            xticklabels=['Fuerza de Trabajo'],
            annot=True,
            fmt='.0f',
            cmap='viridis',
            ax=ax,
            cbar_kws={'label': 'Miles de personas'}
        )
        
        # Formatting
        ax.set_title(f'{title} - {year}', fontsize=16, fontweight='bold', pad=20)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        plt.tight_layout()
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Regional heatmap created successfully")
        return fig
    
    def create_interactive_dashboard(
        self,
        data: pd.DataFrame,
        title: str = "Dashboard Interactivo - Fuerza de Trabajo Chile",
        save_path: Optional[Path] = None
    ) -> go.Figure:
        """Create interactive Plotly dashboard."""
        logger.info("Creating interactive dashboard")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Evolución Temporal Nacional',
                'Comparación por Género',
                'Top 10 Regiones (Último Año)',
                'Distribución por Trimestre'
            ),
            specs=[
                [{"secondary_y": False}, {"secondary_y": False}],
                [{"secondary_y": False}, {"secondary_y": False}]
            ]
        )
        
        # 1. National time series
        national_data = data[
            (data['region_code'] == '_T') & 
            (data['gender_code'] == '_T')
        ].sort_values('date')
        
        fig.add_trace(
            go.Scatter(
                x=national_data['date'],
                y=national_data['value'] / 1000,
                mode='lines+markers',
                name='Nacional',
                line=dict(color=self.colors['primary'], width=2)
            ),
            row=1, col=1
        )
        
        # 2. Gender comparison
        gender_data = data[
            (data['region_code'] == '_T') & 
            (data['gender_code'].isin(['M', 'F']))
        ].sort_values('date')
        
        for gender_code, color in [('M', self.colors['male']), ('F', self.colors['female'])]:
            gender_subset = gender_data[gender_data['gender_code'] == gender_code]
            fig.add_trace(
                go.Scatter(
                    x=gender_subset['date'],
                    y=gender_subset['value'] / 1000,
                    mode='lines+markers',
                    name='Hombres' if gender_code == 'M' else 'Mujeres',
                    line=dict(color=color, width=2)
                ),
                row=1, col=2
            )
        
        # 3. Top regions (latest year)
        latest_year = data['year'].max()
        regional_latest = data[
            (data['region_code'] != '_T') & 
            (data['gender_code'] == '_T') &
            (data['year'] == latest_year)
        ].sort_values('value', ascending=True).tail(10)
        
        fig.add_trace(
            go.Bar(
                y=regional_latest['region_name'],
                x=regional_latest['value'] / 1000,
                orientation='h',
                name=f'Regiones {latest_year}',
                marker_color=self.colors['success']
            ),
            row=2, col=1
        )
        
        # 4. Quarterly distribution
        quarterly_data = data[
            (data['region_code'] == '_T') & 
            (data['gender_code'] == '_T')
        ].groupby('quarter')['value'].mean() / 1000
        
        fig.add_trace(
            go.Bar(
                x=[f'Q{q}' for q in quarterly_data.index],
                y=quarterly_data.values,
                name='Promedio por Trimestre',
                marker_color=self.colors['warning']
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text=title,
            title_x=0.5,
            height=800,
            showlegend=True,
            template='plotly_white'
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Año", row=1, col=1)
        fig.update_yaxes(title_text="Miles de personas", row=1, col=1)
        
        fig.update_xaxes(title_text="Año", row=1, col=2)
        fig.update_yaxes(title_text="Miles de personas", row=1, col=2)
        
        fig.update_xaxes(title_text="Miles de personas", row=2, col=1)
        fig.update_yaxes(title_text="Región", row=2, col=1)
        
        fig.update_xaxes(title_text="Trimestre", row=2, col=2)
        fig.update_yaxes(title_text="Miles de personas", row=2, col=2)
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Interactive dashboard created successfully")
        return fig
    
    def plot_growth_analysis(
        self,
        data: pd.DataFrame,
        title: str = "Análisis de Crecimiento de la Fuerza de Trabajo",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """Create growth analysis plot."""
        logger.info("Creating growth analysis plot")
        
        # Calculate year-over-year growth
        national_data = data[
            (data['region_code'] == '_T') & 
            (data['gender_code'] == '_T')
        ].copy()
        
        # Get annual averages
        annual_data = national_data.groupby('year')['value'].mean().reset_index()
        annual_data['growth_rate'] = annual_data['value'].pct_change() * 100
        
        # Create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.figsize[0], self.figsize[1] * 1.2))
        
        # Plot 1: Absolute values
        ax1.plot(
            annual_data['year'],
            annual_data['value'] / 1000,
            linewidth=2.5,
            color=self.colors['primary'],
            marker='o',
            markersize=6
        )
        ax1.set_title('Fuerza de Trabajo Nacional (Promedio Anual)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Miles de personas', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Growth rates
        colors = [self.colors['success'] if x >= 0 else self.colors['danger'] 
                 for x in annual_data['growth_rate'].fillna(0)]
        
        ax2.bar(
            annual_data['year'][1:],  # Skip first year (no growth rate)
            annual_data['growth_rate'][1:],
            color=colors[1:],
            alpha=0.7
        )
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('Tasa de Crecimiento Anual (%)', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Año', fontsize=12)
        ax2.set_ylabel('Crecimiento (%)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold', y=0.95)
        plt.tight_layout()
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Growth analysis plot created successfully")
        return fig


class StatisticalCharts(BaseChartMaker):
    """Statistical analysis charts."""
    
    def plot_correlation_matrix(
        self,
        data: pd.DataFrame,
        title: str = "Matriz de Correlación",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """Create correlation matrix heatmap."""
        logger.info("Creating correlation matrix")
        
        # Select numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        correlation_data = data[numeric_cols].corr()
        
        # Create plot
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create heatmap
        mask = np.triu(np.ones_like(correlation_data, dtype=bool))
        sns.heatmap(
            correlation_data,
            mask=mask,
            annot=True,
            cmap='coolwarm',
            center=0,
            square=True,
            ax=ax,
            cbar_kws={'shrink': 0.8}
        )
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Correlation matrix created successfully")
        return fig
    
    def plot_distribution_analysis(
        self,
        data: pd.DataFrame,
        column: str = 'value',
        title: str = "Análisis de Distribución",
        save_path: Optional[Path] = None
    ) -> plt.Figure:
        """Create distribution analysis plot."""
        logger.info(f"Creating distribution analysis for {column}")
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Histogram
        ax1.hist(data[column] / 1000, bins=30, alpha=0.7, color=self.colors['primary'])
        ax1.set_title('Histograma', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Miles de personas')
        ax1.set_ylabel('Frecuencia')
        ax1.grid(True, alpha=0.3)
        
        # 2. Box plot
        ax2.boxplot(data[column] / 1000)
        ax2.set_title('Diagrama de Caja', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Miles de personas')
        ax2.grid(True, alpha=0.3)
        
        # 3. Q-Q plot
        from scipy import stats
        stats.probplot(data[column].dropna(), dist="norm", plot=ax3)
        ax3.set_title('Q-Q Plot (Normalidad)', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Time series
        if 'date' in data.columns:
            time_data = data.groupby('date')[column].sum() / 1000
            ax4.plot(time_data.index, time_data.values, color=self.colors['secondary'])
            ax4.set_title('Serie Temporal', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Fecha')
            ax4.set_ylabel('Miles de personas')
            ax4.grid(True, alpha=0.3)
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            self.save_figure(fig, save_path)
        
        logger.info("Distribution analysis created successfully")
        return fig
