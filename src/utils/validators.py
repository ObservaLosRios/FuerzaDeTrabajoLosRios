"""
Validadores de datos para el proyecto Los Ríos
Clean Code: Principio de Responsabilidad Única - solo validación
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime

from ...config import LosRiosConfig, DataConfig


class DataValidator:
    """
    Clase para validar datos en todas las etapas del pipeline.
    
    Clean Code Principles:
    - Single Responsibility: Solo validación de datos
    - Pure Functions: Métodos sin efectos secundarios
    - Descriptive Names: Nombres claros de métodos
    """
    
    def __init__(self):
        """Inicializa el validador con configuraciones."""
        self.config = LosRiosConfig()
        self.data_config = DataConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        """
        Valida que un DataFrame tenga estructura básica válida.
        
        Args:
            df: DataFrame a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        try:
            if df is None:
                self.logger.error("DataFrame es None")
                return False
            
            if not isinstance(df, pd.DataFrame):
                self.logger.error("El objeto no es un DataFrame")
                return False
            
            if df.empty:
                self.logger.warning("DataFrame está vacío")
                return False
            
            if len(df.columns) == 0:
                self.logger.error("DataFrame no tiene columnas")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando DataFrame: {str(e)}")
            return False
    
    def validate_los_rios_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida que los datos pertenezcan específicamente a Los Ríos.
        
        Args:
            df: DataFrame con datos del INE
            
        Returns:
            Tupla (es_valido, lista_errores)
        """
        errors = []
        
        try:
            # Verificar columnas requeridas
            required_columns = self.data_config.REQUIRED_COLUMNS
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                errors.append(f"Columnas faltantes: {missing_columns}")
            
            # Verificar que existan datos de Los Ríos
            if 'region' in df.columns:
                los_rios_data = df[df['region'] == self.config.REGION_CODE]
                if los_rios_data.empty:
                    errors.append(f"No se encontraron datos para {self.config.REGION_CODE}")
                else:
                    self.logger.info(f"Encontrados {len(los_rios_data)} registros de Los Ríos")
            
            # Verificar tipos de datos
            if 'ano_trimestre' in df.columns:
                if not pd.api.types.is_string_dtype(df['ano_trimestre']):
                    errors.append("Columna 'ano_trimestre' debe ser string")
            
            # Verificar valores numéricos válidos
            numeric_columns = ['fuerza_de_trabajo', 'hombres', 'mujeres']
            for col in numeric_columns:
                if col in df.columns:
                    if df[col].isna().all():
                        errors.append(f"Columna '{col}' contiene solo valores nulos")
                    elif (df[col] < 0).any():
                        errors.append(f"Columna '{col}' contiene valores negativos")
            
            is_valid = len(errors) == 0
            return is_valid, errors
            
        except Exception as e:
            errors.append(f"Error en validación: {str(e)}")
            return False, errors
    
    def validate_date_format(self, date_column: pd.Series) -> bool:
        """
        Valida formato de fechas/períodos.
        
        Args:
            date_column: Serie con fechas/períodos
            
        Returns:
            True si el formato es válido
        """
        try:
            # Verificar que no esté vacía
            if date_column.empty:
                return False
            
            # Verificar formato típico del INE (ej: "2024-MAR")
            sample_values = date_column.dropna().head(10)
            
            for value in sample_values:
                if not isinstance(value, str):
                    return False
                
                # Formato esperado: YYYY-MES o similar
                if len(value.split('-')) != 2:
                    self.logger.warning(f"Formato de fecha inesperado: {value}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validando formato de fecha: {str(e)}")
            return False
    
    def validate_numeric_range(
        self, 
        series: pd.Series, 
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> Tuple[bool, List[str]]:
        """
        Valida que los valores numéricos estén en un rango esperado.
        
        Args:
            series: Serie numérica a validar
            min_value: Valor mínimo permitido
            max_value: Valor máximo permitido
            
        Returns:
            Tupla (es_valido, lista_errores)
        """
        errors = []
        
        try:
            # Verificar que sea numérica
            if not pd.api.types.is_numeric_dtype(series):
                errors.append("La serie no es numérica")
                return False, errors
            
            # Verificar valores nulos
            null_count = series.isna().sum()
            if null_count > 0:
                errors.append(f"Encontrados {null_count} valores nulos")
            
            # Verificar rango mínimo
            if min_value is not None:
                below_min = (series < min_value).sum()
                if below_min > 0:
                    errors.append(f"{below_min} valores por debajo del mínimo ({min_value})")
            
            # Verificar rango máximo
            if max_value is not None:
                above_max = (series > max_value).sum()
                if above_max > 0:
                    errors.append(f"{above_max} valores por encima del máximo ({max_value})")
            
            # Verificar valores infinitos
            inf_count = np.isinf(series).sum()
            if inf_count > 0:
                errors.append(f"Encontrados {inf_count} valores infinitos")
            
            is_valid = len(errors) == 0
            return is_valid, errors
            
        except Exception as e:
            errors.append(f"Error validando rango numérico: {str(e)}")
            return False, errors
    
    def validate_data_consistency(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valida consistencia interna de los datos.
        
        Args:
            df: DataFrame a validar
            
        Returns:
            Tupla (es_valido, lista_errores)
        """
        errors = []
        
        try:
            # Verificar que total = hombres + mujeres
            if all(col in df.columns for col in ['fuerza_de_trabajo', 'hombres', 'mujeres']):
                calculated_total = df['hombres'] + df['mujeres']
                difference = abs(df['fuerza_de_trabajo'] - calculated_total)
                
                # Permitir pequeñas diferencias de redondeo
                tolerance = 0.1
                inconsistent_rows = (difference > tolerance).sum()
                
                if inconsistent_rows > 0:
                    errors.append(
                        f"{inconsistent_rows} filas con inconsistencia en totales "
                        f"(fuerza_de_trabajo ≠ hombres + mujeres)"
                    )
            
            # Verificar duplicados
            if 'ano_trimestre' in df.columns and 'region' in df.columns:
                duplicates = df.duplicated(subset=['ano_trimestre', 'region']).sum()
                if duplicates > 0:
                    errors.append(f"Encontrados {duplicates} registros duplicados")
            
            # Verificar tendencias anómalas (cambios extremos)
            if 'fuerza_de_trabajo' in df.columns and len(df) > 1:
                df_sorted = df.sort_values('ano_trimestre')
                pct_change = df_sorted['fuerza_de_trabajo'].pct_change().abs()
                extreme_changes = (pct_change > 0.5).sum()  # Cambios > 50%
                
                if extreme_changes > 0:
                    errors.append(f"Detectados {extreme_changes} cambios extremos en fuerza de trabajo")
            
            is_valid = len(errors) == 0
            return is_valid, errors
            
        except Exception as e:
            errors.append(f"Error validando consistencia: {str(e)}")
            return False, errors
    
    def generate_validation_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera un reporte completo de validación.
        
        Args:
            df: DataFrame a validar
            
        Returns:
            Diccionario con resultados de validación
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "dataframe_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024
            },
            "validations": {},
            "overall_valid": True,
            "errors": [],
            "warnings": []
        }
        
        try:
            # Validación básica de DataFrame
            report["validations"]["basic_structure"] = self.validate_dataframe(df)
            
            # Validación específica de Los Ríos
            is_valid, errors = self.validate_los_rios_data(df)
            report["validations"]["los_rios_data"] = is_valid
            if not is_valid:
                report["errors"].extend(errors)
            
            # Validación de consistencia
            is_consistent, consistency_errors = self.validate_data_consistency(df)
            report["validations"]["data_consistency"] = is_consistent
            if not is_consistent:
                report["errors"].extend(consistency_errors)
            
            # Información adicional de calidad de datos
            report["data_quality"] = self._calculate_data_quality_metrics(df)
            
            # Determinar validez general
            report["overall_valid"] = all(report["validations"].values())
            
            return report
            
        except Exception as e:
            report["errors"].append(f"Error generando reporte: {str(e)}")
            report["overall_valid"] = False
            return report
    
    def _calculate_data_quality_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcula métricas de calidad de datos."""
        try:
            metrics = {
                "completeness": {},
                "uniqueness": {},
                "validity": {}
            }
            
            # Completitud (% de valores no nulos)
            for col in df.columns:
                non_null_pct = (df[col].notna().sum() / len(df)) * 100
                metrics["completeness"][col] = round(non_null_pct, 2)
            
            # Unicidad (% de valores únicos)
            for col in df.columns:
                unique_pct = (df[col].nunique() / len(df)) * 100
                metrics["uniqueness"][col] = round(unique_pct, 2)
            
            # Validez de tipos de datos
            for col in df.columns:
                dtype_str = str(df[col].dtype)
                metrics["validity"][col] = dtype_str
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculando métricas de calidad: {str(e)}")
            return {}
