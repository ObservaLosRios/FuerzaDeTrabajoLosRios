"""
Módulo ETL para análisis de Los Ríos
Clean Code: módulos bien organizados con responsabilidades claras
"""

from .data_extractor import LosRiosDataExtractor
from .data_transformer import LosRiosDataTransformer  
from .data_loader import LosRiosDataLoader

__all__ = [
    "LosRiosDataExtractor",
    "LosRiosDataTransformer", 
    "LosRiosDataLoader"
]
