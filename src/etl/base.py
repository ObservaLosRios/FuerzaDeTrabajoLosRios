"""
Base classes for ETL operations following SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataExtractor(ABC):
    """Abstract base class for data extraction operations."""
    
    @abstractmethod
    def extract(self, source: Union[str, Path]) -> pd.DataFrame:
        """Extract data from source."""
        pass
    
    @abstractmethod
    def validate_source(self, source: Union[str, Path]) -> bool:
        """Validate if source exists and is accessible."""
        pass


class DataTransformer(ABC):
    """Abstract base class for data transformation operations."""
    
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Transform data according to business rules."""
        pass
    
    @abstractmethod
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate data quality and structure."""
        pass


class DataLoader(ABC):
    """Abstract base class for data loading operations."""
    
    @abstractmethod
    def load(self, data: pd.DataFrame, destination: Union[str, Path]) -> bool:
        """Load data to destination."""
        pass
    
    @abstractmethod
    def validate_destination(self, destination: Union[str, Path]) -> bool:
        """Validate if destination is writable."""
        pass


class ETLPipeline:
    """Main ETL pipeline orchestrator."""
    
    def __init__(
        self,
        extractor: DataExtractor,
        transformer: DataTransformer,
        loader: DataLoader
    ):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.logger = logging.getLogger(__name__)
    
    def run(
        self,
        source: Union[str, Path],
        destination: Union[str, Path],
        validate: bool = True
    ) -> bool:
        """Run the complete ETL pipeline."""
        try:
            # Extract
            self.logger.info(f"Extracting data from {source}")
            if validate and not self.extractor.validate_source(source):
                raise ValueError(f"Invalid source: {source}")
            
            data = self.extractor.extract(source)
            self.logger.info(f"Extracted {len(data)} records")
            
            # Transform
            self.logger.info("Transforming data")
            if validate and not self.transformer.validate_data(data):
                raise ValueError("Data validation failed before transformation")
            
            transformed_data = self.transformer.transform(data)
            self.logger.info(f"Transformed to {len(transformed_data)} records")
            
            # Load
            self.logger.info(f"Loading data to {destination}")
            if validate and not self.loader.validate_destination(destination):
                raise ValueError(f"Invalid destination: {destination}")
            
            success = self.loader.load(transformed_data, destination)
            
            if success:
                self.logger.info("ETL pipeline completed successfully")
            else:
                self.logger.error("ETL pipeline failed during loading")
            
            return success
            
        except Exception as e:
            self.logger.error(f"ETL pipeline failed: {str(e)}")
            raise
