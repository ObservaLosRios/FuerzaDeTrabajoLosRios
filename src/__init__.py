"""
INE Chile Labour Force Analysis - Main package.

A professional Data Science project for analyzing Chilean labor force data
from the National Institute of Statistics (INE).

Features:
- Clean Code architecture with SOLID principles
- Modular ETL pipeline
- Professional data validation
- Interactive visualizations
- Predictive modeling capabilities
- Comprehensive documentation

Author: Bruno San Martin
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Bruno San Martin"
__email__ = "bruno@example.com"
__license__ = "MIT"

from . import etl, utils, visualization, models

__all__ = ["etl", "utils", "visualization", "models"]
