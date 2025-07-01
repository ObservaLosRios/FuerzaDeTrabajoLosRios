"""
Data processor for INE Labour Force data.
Implements Clean Code and SOLID principles.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import re
from datetime import datetime
import logging

from .base import DataExtractor, DataTransformer, DataLoader
from ..utils.validators import DataValidator
from ..utils.logger_config import get_logger

logger = get_logger(__name__)


class INECSVExtractor(DataExtractor):
    """Extractor for INE CSV files."""
    
    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding
    
    def extract(self, source: Union[str, Path]) -> pd.DataFrame:
        """Extract data from INE CSV file."""
        try:
            df = pd.read_csv(source, encoding=self.encoding)
            logger.info(f"Successfully extracted {len(df)} rows from {source}")
            return df
        except Exception as e:
            logger.error(f"Failed to extract data from {source}: {str(e)}")
            raise
    
    def validate_source(self, source: Union[str, Path]) -> bool:
        """Validate if CSV source exists and is readable."""
        path = Path(source)
        if not path.exists():
            logger.error(f"Source file does not exist: {source}")
            return False
        
        if not path.suffix.lower() == '.csv':
            logger.error(f"Source is not a CSV file: {source}")
            return False
        
        try:
            # Try to read first few lines
            pd.read_csv(source, nrows=5, encoding=self.encoding)
            return True
        except Exception as e:
            logger.error(f"Cannot read CSV file {source}: {str(e)}")
            return False


class LabourForceTransformer(DataTransformer):
    """Transformer for INE Labour Force data."""
    
    def __init__(self):
        self.regional_codes = {
            "_T": "Total país",
            "CHL15": "Región de Arica y Parinacota",
            "CHL01": "Región de Tarapacá",
            "CHL02": "Región de Antofagasta",
            "CHL03": "Región de Atacama",
            "CHL04": "Región de Coquimbo",
            "CHL05": "Región de Valparaíso",
            "CHL13": "Región Metropolitana",
            "CHL06": "Región del Libertador General Bernardo O'Higgins",
            "CHL07": "Región del Maule",
            "CHL16": "Región de Ñuble",
            "CHL08": "Región del Biobío",
            "CHL09": "Región de La Araucanía",
            "CHL14": "Región de Los Ríos",
            "CHL10": "Región de Los Lagos",
            "CHL11": "Región Aysén del General Carlos Ibáñez del Campo",
            "CHL12": "Región de Magallanes y de la Antártica Chilena",
        }
        
        self.gender_mapping = {
            "_T": "Total",
            "M": "Hombres",
            "F": "Mujeres"
        }
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform raw INE data to clean format."""
        logger.info("Starting data transformation")
        
        df = data.copy()
        
        # Clean column names
        df = self._clean_column_names(df)
        
        # Parse time periods
        df = self._parse_time_periods(df)
        
        # Map regional codes
        df = self._map_regional_codes(df)
        
        # Map gender codes
        df = self._map_gender_codes(df)
        
        # Clean and convert values
        df = self._clean_values(df)
        
        # Add derived columns
        df = self._add_derived_columns(df)
        
        # Remove unnecessary columns
        df = self._remove_unnecessary_columns(df)
        
        # Sort data
        df = self._sort_data(df)
        
        logger.info(f"Transformation completed. Final shape: {df.shape}")
        return df
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        column_mapping = {
            'DTI_CL_INDICADOR': 'indicator_code',
            'Indicador': 'indicator',
            'DTI_CL_TRIMESTRE_MOVIL': 'period_code',
            'Trimestre Móvil': 'period',
            'DTI_CL_REGION': 'region_code',
            'Región': 'region',
            'DTI_CL_SEXO': 'gender_code',
            'Sexo': 'gender',
            'Value': 'value',
            'Flag Codes': 'flag_codes',
            'Flags': 'flags'
        }
        
        df = df.rename(columns=column_mapping)
        logger.debug("Column names cleaned")
        return df
    
    def _parse_time_periods(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse time periods and extract year/quarter information."""
        # Extract year and quarter from period_code (e.g., "2010-V02" -> year=2010, quarter=2)
        df['year'] = df['period_code'].str.extract(r'(\d{4})').astype(int)
        df['quarter'] = df['period_code'].str.extract(r'V(\d{2})').astype(int)
        
        # Create quarter name
        quarter_names = {1: 'ene-mar', 2: 'abr-jun', 3: 'jul-sep', 4: 'oct-dic'}
        df['quarter_name'] = df['quarter'].map(quarter_names)
        
        # Create date column (using first month of quarter)
        month_mapping = {1: 1, 2: 4, 3: 7, 4: 10}
        df['date'] = pd.to_datetime(
            df['year'].astype(str) + '-' + 
            df['quarter'].map(month_mapping).astype(str) + '-01'
        )
        
        logger.debug("Time periods parsed")
        return df
    
    def _map_regional_codes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map regional codes to full names."""
        df['region_name'] = df['region_code'].map(self.regional_codes)
        
        # Handle unmapped regions
        unmapped = df['region_name'].isna()
        if unmapped.any():
            logger.warning(f"Found {unmapped.sum()} rows with unmapped regional codes")
            df.loc[unmapped, 'region_name'] = df.loc[unmapped, 'region']
        
        logger.debug("Regional codes mapped")
        return df
    
    def _map_gender_codes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Map gender codes to full names."""
        df['gender_name'] = df['gender_code'].map(self.gender_mapping)
        
        # Handle unmapped genders
        unmapped = df['gender_name'].isna()
        if unmapped.any():
            logger.warning(f"Found {unmapped.sum()} rows with unmapped gender codes")
            df.loc[unmapped, 'gender_name'] = df.loc[unmapped, 'gender']
        
        logger.debug("Gender codes mapped")
        return df
    
    def _clean_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and convert value column."""
        # Convert to numeric, handling any string values
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Log any NaN values created
        nan_count = df['value'].isna().sum()
        if nan_count > 0:
            logger.warning(f"Found {nan_count} non-numeric values in value column")
        
        # Convert from thousands to actual numbers (assuming values are in thousands)
        df['value_thousands'] = df['value']
        df['value'] = df['value'] * 1000
        
        logger.debug("Values cleaned and converted")
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived columns for analysis."""
        # Add period string for plotting
        df['period_str'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
        
        # Add decade
        df['decade'] = (df['year'] // 10) * 10
        
        # Add is_national flag
        df['is_national'] = df['region_code'] == '_T'
        
        # Add is_total_gender flag
        df['is_total_gender'] = df['gender_code'] == '_T'
        
        logger.debug("Derived columns added")
        return df
    
    def _remove_unnecessary_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove columns that are no longer needed."""
        columns_to_remove = ['flag_codes', 'flags']
        existing_columns = [col for col in columns_to_remove if col in df.columns]
        
        if existing_columns:
            df = df.drop(columns=existing_columns)
            logger.debug(f"Removed columns: {existing_columns}")
        
        return df
    
    def _sort_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sort data by date, region, and gender."""
        df = df.sort_values(['date', 'region_code', 'gender_code']).reset_index(drop=True)
        logger.debug("Data sorted")
        return df
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate data structure and quality."""
        required_columns = [
            'DTI_CL_INDICADOR', 'Indicador', 'DTI_CL_TRIMESTRE_MOVIL',
            'Trimestre Móvil', 'DTI_CL_REGION', 'Región', 'DTI_CL_SEXO',
            'Sexo', 'Value'
        ]
        
        # Check required columns
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        # Check if data is not empty
        if len(data) == 0:
            logger.error("Data is empty")
            return False
        
        # Check for basic data types
        if data['Value'].dtype not in ['float64', 'int64', 'object']:
            logger.error("Value column has unexpected data type")
            return False
        
        logger.info("Data validation passed")
        return True


class ProcessedDataLoader(DataLoader):
    """Loader for processed data."""
    
    def __init__(self, file_format: str = "csv"):
        self.file_format = file_format.lower()
        
        if self.file_format not in ['csv', 'parquet', 'excel']:
            raise ValueError(f"Unsupported file format: {file_format}")
    
    def load(self, data: pd.DataFrame, destination: Union[str, Path]) -> bool:
        """Load processed data to destination."""
        try:
            destination = Path(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            if self.file_format == 'csv':
                data.to_csv(destination, index=False, encoding='utf-8')
            elif self.file_format == 'parquet':
                data.to_parquet(destination, index=False)
            elif self.file_format == 'excel':
                data.to_excel(destination, index=False)
            
            logger.info(f"Successfully loaded {len(data)} rows to {destination}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load data to {destination}: {str(e)}")
            return False
    
    def validate_destination(self, destination: Union[str, Path]) -> bool:
        """Validate if destination directory is writable."""
        try:
            destination = Path(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            # Try to create a test file
            test_file = destination.parent / "test_write.tmp"
            test_file.touch()
            test_file.unlink()
            
            return True
            
        except Exception as e:
            logger.error(f"Cannot write to destination {destination}: {str(e)}")
            return False


class LabourForceProcessor:
    """Main processor for Labour Force data."""
    
    def __init__(self):
        self.extractor = INECSVExtractor()
        self.transformer = LabourForceTransformer()
        self.loader = ProcessedDataLoader()
    
    def process_file(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path]
    ) -> pd.DataFrame:
        """Process a single Labour Force file."""
        logger.info(f"Processing Labour Force file: {input_path}")
        
        # Extract
        raw_data = self.extractor.extract(input_path)
        
        # Transform
        processed_data = self.transformer.transform(raw_data)
        
        # Load
        self.loader.load(processed_data, output_path)
        
        logger.info(f"Processing completed. Output saved to: {output_path}")
        return processed_data
    
    def get_summary_statistics(self, data: pd.DataFrame) -> Dict:
        """Generate summary statistics for the processed data."""
        stats = {
            'total_records': len(data),
            'date_range': {
                'min': data['date'].min().strftime('%Y-%m-%d'),
                'max': data['date'].max().strftime('%Y-%m-%d')
            },
            'regions_count': data['region_code'].nunique(),
            'years_count': data['year'].nunique(),
            'value_statistics': {
                'mean': float(data['value'].mean()),
                'median': float(data['value'].median()),
                'std': float(data['value'].std()),
                'min': float(data['value'].min()),
                'max': float(data['value'].max())
            },
            'missing_values': int(data['value'].isna().sum())
        }
        
        logger.info("Summary statistics generated")
        return stats
