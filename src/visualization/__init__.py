"""
Módulo de visualización para el proyecto Los Ríos
Clean Code: separación de responsabilidades para gráficos y dashboards
"""

from .chart_factory import ChartFactory
from .dashboard_builder import DashboardBuilder

__all__ = [
    "ChartFactory",
    "DashboardBuilder"
]
