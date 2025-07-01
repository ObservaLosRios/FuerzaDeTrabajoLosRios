"""
Funciones auxiliares para el proyecto Los Ríos
Clean Code: utilidades específicas del dominio
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import re
from pathlib import Path

from ...config import LosRiosConfig


class HelperFunctions:
    """
    Conjunto de funciones auxiliares para el análisis de Los Ríos.
    
    Clean Code Principles:
    - Pure Functions: Sin efectos secundarios
    - Single Responsibility: Cada método con propósito específico
    - Descriptive Names: Nombres que describen claramente su función
    """
    
    @staticmethod
    def parse_ine_period(period_str: str) -> Tuple[int, str]:
        """
        Parsea períodos del INE al formato estándar.
        
        Args:
            period_str: String de período del INE (ej: "2024-MAR")
            
        Returns:
            Tupla (año, trimestre)
            
        Examples:
            >>> parse_ine_period("2024-MAR")
            (2024, "Q1")
        """
        try:
            if not isinstance(period_str, str):
                raise ValueError("El período debe ser un string")
            
            # Formato típico: "YYYY-MES"
            parts = period_str.split('-')
            if len(parts) != 2:
                raise ValueError(f"Formato de período inválido: {period_str}")
            
            year = int(parts[0])
            month_str = parts[1].upper()
            
            # Mapear meses a trimestres
            month_to_quarter = {
                'ENE': 'Q1', 'FEB': 'Q1', 'MAR': 'Q1',
                'ABR': 'Q2', 'MAY': 'Q2', 'JUN': 'Q2',
                'JUL': 'Q3', 'AGO': 'Q3', 'SEP': 'Q3',
                'OCT': 'Q4', 'NOV': 'Q4', 'DIC': 'Q4'
            }
            
            quarter = month_to_quarter.get(month_str, 'Q1')
            return year, quarter
            
        except Exception as e:
            raise ValueError(f"Error parseando período {period_str}: {str(e)}")
    
    @staticmethod
    def calculate_period_differences(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
        """
        Calcula diferencias período a período.
        
        Args:
            df: DataFrame con datos temporales
            value_column: Columna con valores numéricos
            
        Returns:
            DataFrame con columnas adicionales de diferencias
        """
        result_df = df.copy()
        
        # Ordenar por período
        if 'ano_trimestre' in result_df.columns:
            result_df = result_df.sort_values('ano_trimestre')
        
        # Calcular diferencias absolutas
        result_df[f'{value_column}_diff'] = result_df[value_column].diff()
        
        # Calcular diferencias porcentuales
        result_df[f'{value_column}_pct_change'] = result_df[value_column].pct_change() * 100
        
        # Calcular diferencias anuales (año sobre año)
        if len(result_df) >= 4:  # Al menos 4 trimestres
            result_df[f'{value_column}_yoy_change'] = result_df[value_column].pct_change(periods=4) * 100
        
        return result_df
    
    @staticmethod
    def detect_outliers(series: pd.Series, method: str = "iqr") -> pd.Series:
        """
        Detecta outliers en una serie numérica.
        
        Args:
            series: Serie numérica
            method: Método de detección ("iqr", "zscore", "modified_zscore")
            
        Returns:
            Serie booleana indicando outliers
        """
        if method == "iqr":
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return (series < lower_bound) | (series > upper_bound)
        
        elif method == "zscore":
            z_scores = np.abs((series - series.mean()) / series.std())
            return z_scores > 3
        
        elif method == "modified_zscore":
            median = series.median()
            mad = np.median(np.abs(series - median))
            modified_z_scores = 0.6745 * (series - median) / mad
            return np.abs(modified_z_scores) > 3.5
        
        else:
            raise ValueError(f"Método {method} no soportado")
    
    @staticmethod
    def create_age_groups(ages: pd.Series) -> pd.Series:
        """
        Crea grupos etarios estándar.
        
        Args:
            ages: Serie con edades
            
        Returns:
            Serie con grupos etarios
        """
        def categorize_age(age):
            if pd.isna(age):
                return "No especificado"
            elif age < 25:
                return "15-24 años"
            elif age < 35:
                return "25-34 años"
            elif age < 45:
                return "35-44 años"
            elif age < 55:
                return "45-54 años"
            elif age < 65:
                return "55-64 años"
            else:
                return "65+ años"
        
        return ages.apply(categorize_age)
    
    @staticmethod
    def standardize_text(text: str) -> str:
        """
        Estandariza texto removiendo acentos y caracteres especiales.
        
        Args:
            text: Texto a estandarizar
            
        Returns:
            Texto estandarizado
        """
        if not isinstance(text, str):
            return str(text)
        
        # Remover acentos
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N'
        }
        
        for original, replacement in replacements.items():
            text = text.replace(original, replacement)
        
        # Limpiar espacios y caracteres especiales
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def calculate_growth_rates(values: pd.Series) -> Dict[str, float]:
        """
        Calcula diferentes tipos de tasas de crecimiento.
        
        Args:
            values: Serie con valores temporales
            
        Returns:
            Diccionario con tasas de crecimiento
        """
        if len(values) < 2:
            return {"error": "Insuficientes datos para calcular crecimiento"}
        
        clean_values = values.dropna()
        if len(clean_values) < 2:
            return {"error": "Insuficientes valores válidos"}
        
        first_value = clean_values.iloc[0]
        last_value = clean_values.iloc[-1]
        
        # Crecimiento total
        total_growth = ((last_value - first_value) / first_value) * 100
        
        # Crecimiento anualizado (CAGR)
        periods = len(clean_values) - 1
        if periods > 0 and first_value > 0:
            annual_growth = ((last_value / first_value) ** (1/periods) - 1) * 100
        else:
            annual_growth = 0
        
        # Crecimiento promedio período a período
        period_changes = clean_values.pct_change().dropna()
        avg_period_growth = period_changes.mean() * 100
        
        return {
            "total_growth_pct": round(total_growth, 2),
            "annual_growth_pct": round(annual_growth, 2),
            "avg_period_growth_pct": round(avg_period_growth, 2),
            "periods": periods
        }
    
    @staticmethod
    def create_summary_statistics(df: pd.DataFrame, group_columns: List[str] = None) -> Dict[str, Any]:
        """
        Crea estadísticas resumen para un DataFrame.
        
        Args:
            df: DataFrame a resumir
            group_columns: Columnas para agrupar (opcional)
            
        Returns:
            Diccionario con estadísticas
        """
        summary = {
            "shape": df.shape,
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "dtypes": df.dtypes.to_dict(),
            "null_counts": df.isnull().sum().to_dict(),
            "unique_counts": df.nunique().to_dict()
        }
        
        # Estadísticas numéricas
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            summary["numeric_stats"] = df[numeric_columns].describe().to_dict()
        
        # Estadísticas categóricas
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_columns) > 0:
            summary["categorical_stats"] = {}
            for col in categorical_columns:
                summary["categorical_stats"][col] = {
                    "unique_values": df[col].nunique(),
                    "most_common": df[col].value_counts().head(5).to_dict()
                }
        
        # Estadísticas por grupo si se especifican
        if group_columns and all(col in df.columns for col in group_columns):
            summary["group_stats"] = {}
            for col in group_columns:
                summary["group_stats"][col] = df.groupby(col).size().to_dict()
        
        return summary
    
    @staticmethod
    def format_large_numbers(number: Union[int, float], precision: int = 1) -> str:
        """
        Formatea números grandes con sufijos (K, M, B).
        
        Args:
            number: Número a formatear
            precision: Decimales a mostrar
            
        Returns:
            String formateado
        """
        if pd.isna(number):
            return "N/A"
        
        abs_number = abs(number)
        
        if abs_number >= 1_000_000_000:
            formatted = f"{number / 1_000_000_000:.{precision}f}B"
        elif abs_number >= 1_000_000:
            formatted = f"{number / 1_000_000:.{precision}f}M"
        elif abs_number >= 1_000:
            formatted = f"{number / 1_000:.{precision}f}K"
        else:
            formatted = f"{number:.{precision}f}"
        
        return formatted
    
    @staticmethod
    def validate_file_path(file_path: Union[str, Path]) -> Path:
        """
        Valida y convierte rutas de archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Path validado
            
        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")
        
        if not path.is_file():
            raise ValueError(f"La ruta no es un archivo: {path}")
        
        return path
    
    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        """
        División segura que maneja división por cero.
        
        Args:
            numerator: Numerador
            denominator: Denominador
            default: Valor por defecto si denominador es 0
            
        Returns:
            Resultado de la división o valor por defecto
        """
        try:
            if pd.isna(numerator) or pd.isna(denominator):
                return default
            
            if denominator == 0:
                return default
            
            return numerator / denominator
            
        except Exception:
            return default
