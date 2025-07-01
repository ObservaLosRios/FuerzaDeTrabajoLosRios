"""
Paquete principal del proyecto de análisis de Los Ríos
"""

__version__ = "1.0.0"
__author__ = "Bruno San Martín"
__email__ = "bruno.sanmartin@uach.cl"
__description__ = "Análisis profesional de la Fuerza de Trabajo en la Región de Los Ríos"

from .etl import DataExtractor, DataTransformer, DataLoader
from .models import LabourAnalyzer, DemographicsAnalyzer, StatisticsEngine
from .utils import DataValidator, LoggerConfig, HelperFunctions
from .visualization import ChartFactory, DashboardBuilder

__all__ = [
    "DataExtractor",
    "DataTransformer", 
    "DataLoader",
    "LabourAnalyzer",
    "DemographicsAnalyzer",
    "StatisticsEngine",
    "DataValidator",
    "LoggerConfig",
    "HelperFunctions",
    "ChartFactory",
    "DashboardBuilder"
]
