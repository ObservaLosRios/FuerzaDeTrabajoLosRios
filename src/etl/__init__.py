"""
ETL package for INE Chile Labour Force Analysis.
Contains modules for data extraction, transformation, and loading.
"""

from .data_processor import LabourForceProcessor
from .base import ETLPipeline, DataExtractor, DataTransformer, DataLoader

__version__ = "0.1.0"
__author__ = "Bruno San Martin"

__all__ = [
    "LabourForceProcessor",
    "ETLPipeline", 
    "DataExtractor",
    "DataTransformer", 
    "DataLoader"
]
