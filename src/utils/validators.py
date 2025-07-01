"""
Data validation utilities for the Labour Force analysis project.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from datetime import datetime
import re

from .logger_config import get_logger

logger = get_logger(__name__)


class DataValidator:
    """Comprehensive data validator for Labour Force data."""
    
    def __init__(self):
        self.validation_results = {}
    
    def validate_dataframe(
        self,
        df: pd.DataFrame,
        required_columns: Optional[List[str]] = None,
        numeric_columns: Optional[List[str]] = None,
        date_columns: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Comprehensive DataFrame validation.
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            numeric_columns: List of columns that should be numeric
            date_columns: List of columns that should be dates
        
        Returns:
            Dictionary with validation results
        """
        results = {}
        
        # Basic structure validation
        results['not_empty'] = self._check_not_empty(df)
        results['has_required_columns'] = self._check_required_columns(df, required_columns)
        results['no_duplicate_rows'] = self._check_no_duplicates(df)
        
        # Column type validation
        if numeric_columns:
            results['numeric_columns_valid'] = self._check_numeric_columns(df, numeric_columns)
        
        if date_columns:
            results['date_columns_valid'] = self._check_date_columns(df, date_columns)
        
        # Data quality checks
        results['missing_data_acceptable'] = self._check_missing_data(df)
        results['no_extreme_outliers'] = self._check_outliers(df, numeric_columns)
        
        # Log results
        passed_checks = sum(results.values())
        total_checks = len(results)
        logger.info(f"Data validation: {passed_checks}/{total_checks} checks passed")
        
        self.validation_results = results
        return results
    
    def _check_not_empty(self, df: pd.DataFrame) -> bool:
        """Check if DataFrame is not empty."""
        is_valid = len(df) > 0 and len(df.columns) > 0
        if not is_valid:
            logger.error("DataFrame is empty")
        return is_valid
    
    def _check_required_columns(
        self,
        df: pd.DataFrame,
        required_columns: Optional[List[str]]
    ) -> bool:
        """Check if all required columns are present."""
        if not required_columns:
            return True
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        return True
    
    def _check_no_duplicates(self, df: pd.DataFrame) -> bool:
        """Check for duplicate rows."""
        duplicate_count = df.duplicated().sum()
        
        if duplicate_count > 0:
            logger.warning(f"Found {duplicate_count} duplicate rows")
            return False
        
        return True
    
    def _check_numeric_columns(
        self,
        df: pd.DataFrame,
        numeric_columns: List[str]
    ) -> bool:
        """Check if specified columns are numeric."""
        invalid_columns = []
        
        for col in numeric_columns:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    # Try to convert to numeric
                    try:
                        pd.to_numeric(df[col], errors='raise')
                    except:
                        invalid_columns.append(col)
        
        if invalid_columns:
            logger.error(f"Non-numeric columns: {invalid_columns}")
            return False
        
        return True
    
    def _check_date_columns(
        self,
        df: pd.DataFrame,
        date_columns: List[str]
    ) -> bool:
        """Check if specified columns can be converted to dates."""
        invalid_columns = []
        
        for col in date_columns:
            if col in df.columns:
                try:
                    pd.to_datetime(df[col], errors='raise')
                except:
                    invalid_columns.append(col)
        
        if invalid_columns:
            logger.error(f"Invalid date columns: {invalid_columns}")
            return False
        
        return True
    
    def _check_missing_data(
        self,
        df: pd.DataFrame,
        threshold: float = 0.3
    ) -> bool:
        """Check if missing data is within acceptable threshold."""
        missing_ratio = df.isnull().sum() / len(df)
        problematic_columns = missing_ratio[missing_ratio > threshold]
        
        if len(problematic_columns) > 0:
            logger.warning(
                f"Columns with >30% missing data: {problematic_columns.to_dict()}"
            )
            return False
        
        return True
    
    def _check_outliers(
        self,
        df: pd.DataFrame,
        numeric_columns: Optional[List[str]],
        z_threshold: float = 3.0
    ) -> bool:
        """Check for extreme outliers using Z-score."""
        if not numeric_columns:
            return True
        
        outlier_counts = {}
        
        for col in numeric_columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                # Calculate Z-scores
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outlier_count = (z_scores > z_threshold).sum()
                
                if outlier_count > 0:
                    outlier_counts[col] = outlier_count
        
        if outlier_counts:
            total_outliers = sum(outlier_counts.values())
            outlier_ratio = total_outliers / len(df)
            
            logger.warning(f"Found outliers in columns: {outlier_counts}")
            
            # Consider acceptable if less than 5% outliers
            return outlier_ratio < 0.05
        
        return True
    
    def get_validation_report(self) -> str:
        """Generate a detailed validation report."""
        if not self.validation_results:
            return "No validation results available. Run validate_dataframe() first."
        
        report_lines = ["Data Validation Report", "=" * 25]
        
        for check, passed in self.validation_results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            check_name = check.replace('_', ' ').title()
            report_lines.append(f"{check_name}: {status}")
        
        passed_count = sum(self.validation_results.values())
        total_count = len(self.validation_results)
        
        report_lines.append("")
        report_lines.append(f"Overall: {passed_count}/{total_count} checks passed")
        
        if passed_count == total_count:
            report_lines.append("🎉 All validations passed!")
        else:
            report_lines.append("⚠️  Some validations failed. Check logs for details.")
        
        return "\n".join(report_lines)


class LabourForceValidator(DataValidator):
    """Specialized validator for Labour Force data."""
    
    def __init__(self):
        super().__init__()
        
        self.expected_columns = [
            'DTI_CL_INDICADOR', 'Indicador', 'DTI_CL_TRIMESTRE_MOVIL',
            'Trimestre Móvil', 'DTI_CL_REGION', 'Región', 'DTI_CL_SEXO',
            'Sexo', 'Value'
        ]
        
        self.valid_regions = {
            "_T", "CHL15", "CHL01", "CHL02", "CHL03", "CHL04", "CHL05",
            "CHL13", "CHL06", "CHL07", "CHL16", "CHL08", "CHL09", "CHL14",
            "CHL10", "CHL11", "CHL12"
        }
        
        self.valid_genders = {"_T", "M", "F"}
    
    def validate_labour_force_data(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validate Labour Force specific data requirements."""
        results = self.validate_dataframe(
            df,
            required_columns=self.expected_columns,
            numeric_columns=['Value']
        )
        
        # Labour Force specific validations
        results['valid_regions'] = self._check_valid_regions(df)
        results['valid_genders'] = self._check_valid_genders(df)
        results['valid_time_periods'] = self._check_valid_time_periods(df)
        results['positive_values'] = self._check_positive_values(df)
        
        return results
    
    def _check_valid_regions(self, df: pd.DataFrame) -> bool:
        """Check if all region codes are valid."""
        if 'DTI_CL_REGION' not in df.columns:
            return False
        
        invalid_regions = set(df['DTI_CL_REGION'].unique()) - self.valid_regions
        
        if invalid_regions:
            logger.warning(f"Found invalid region codes: {invalid_regions}")
            return False
        
        return True
    
    def _check_valid_genders(self, df: pd.DataFrame) -> bool:
        """Check if all gender codes are valid."""
        if 'DTI_CL_SEXO' not in df.columns:
            return False
        
        invalid_genders = set(df['DTI_CL_SEXO'].unique()) - self.valid_genders
        
        if invalid_genders:
            logger.warning(f"Found invalid gender codes: {invalid_genders}")
            return False
        
        return True
    
    def _check_valid_time_periods(self, df: pd.DataFrame) -> bool:
        """Check if time periods follow expected format."""
        if 'DTI_CL_TRIMESTRE_MOVIL' not in df.columns:
            return False
        
        # Expected format: YYYY-VQQ (e.g., 2010-V02)
        pattern = r'^\d{4}-V\d{2}$'
        
        invalid_periods = []
        for period in df['DTI_CL_TRIMESTRE_MOVIL'].unique():
            if not re.match(pattern, str(period)):
                invalid_periods.append(period)
        
        if invalid_periods:
            logger.warning(f"Found invalid time period formats: {invalid_periods}")
            return False
        
        return True
    
    def _check_positive_values(self, df: pd.DataFrame) -> bool:
        """Check if labour force values are positive."""
        if 'Value' not in df.columns:
            return False
        
        # Convert to numeric and check for negative values
        numeric_values = pd.to_numeric(df['Value'], errors='coerce')
        negative_count = (numeric_values < 0).sum()
        
        if negative_count > 0:
            logger.warning(f"Found {negative_count} negative labour force values")
            return False
        
        return True
