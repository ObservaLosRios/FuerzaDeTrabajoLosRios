"""
Módulo de modelos de análisis para Los Ríos
Clean Code: modelos específicos del dominio con responsabilidades claras
"""

from .labour_analyzer import LabourAnalyzer
from .demographics import DemographicsAnalyzer
from .statistics_engine import StatisticsEngine

__all__ = [
    "LabourAnalyzer",
    "DemographicsAnalyzer",
    "StatisticsEngine"
]
