"""
Transformador de datos para la Región de Los Ríos
Clean Code: Principio de Responsabilidad Única - Solo transforma datos
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
import re
from datetime import datetime
from abc import ABC, abstractmethod

from config import (
    LOS_RIOS_CONFIG,
    DATA_COLUMNS,
    ANALYSIS_CONFIG,
    LOGGING_CONFIG
)


# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG.LOG_LEVEL),
    format=LOGGING_CONFIG.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class DataTransformer(ABC):
    """
    Clase abstracta para transformadores de datos
    Clean Code: Interface Segregation Principle
    """
    
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transformar datos"""
        pass
    
    @abstractmethod
    def validate_input(self, df: pd.DataFrame) -> bool:
        """Validar datos de entrada"""
        pass


class LosRiosDataTransformer(DataTransformer):
    """
    Transformador específico para datos de Los Ríos
    Clean Code: Clase con responsabilidad única y nombres descriptivos
    """
    
    def __init__(self):
        """Inicializar transformador para Los Ríos"""
        self.region_code = LOS_RIOS_CONFIG.REGION_CODE
        self.region_name = LOS_RIOS_CONFIG.REGION_NAME
        
        logger.info(f"Inicializando transformador para {self.region_name}")
    
    def validate_input(self, df: pd.DataFrame) -> bool:
        """
        Validar que los datos de entrada son correctos
        Clean Code: Método con responsabilidad única
        
        Args:
            df: DataFrame a validar
            
        Returns:
            bool: True si los datos son válidos
        """
        try:
            # Verificar que no está vacío
            if df.empty:
                logger.error("DataFrame está vacío")
                return False
            
            # Verificar columnas requeridas
            required_columns = [
                DATA_COLUMNS.REGION_CODE,
                DATA_COLUMNS.QUARTER_NAME,
                DATA_COLUMNS.GENDER_NAME,
                DATA_COLUMNS.VALUE
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Columnas faltantes: {missing_columns}")
                return False
            
            # Verificar que todos los registros son de Los Ríos
            region_values = df[DATA_COLUMNS.REGION_CODE].unique()
            if len(region_values) != 1 or region_values[0] != self.region_code:
                logger.error(f"Datos contienen regiones distintas a {self.region_code}")
                return False
            
            logger.info("Datos de entrada validados correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error validando datos de entrada: {e}")
            return False
    
    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpiar nombres de columnas
        Clean Code: Método privado con responsabilidad específica
        
        Args:
            df: DataFrame con columnas a limpiar
            
        Returns:
            pd.DataFrame: DataFrame con columnas limpias
        """
        df_clean = df.copy()
        
        # Mapeo de columnas originales a nombres limpios
        column_mapping = {
            DATA_COLUMNS.QUARTER_NAME: DATA_COLUMNS.PROCESSED_DATE,
            DATA_COLUMNS.GENDER_NAME: DATA_COLUMNS.PROCESSED_GENDER,
            DATA_COLUMNS.VALUE: DATA_COLUMNS.PROCESSED_WORKFORCE
        }
        
        # Renombrar columnas existentes
        df_clean = df_clean.rename(columns=column_mapping)
        
        logger.info("Nombres de columnas limpiados")
        return df_clean
    
    def _parse_quarter_to_date(self, quarter_str: str) -> Dict[str, Any]:
        """
        Convertir string de trimestre a información de fecha
        Clean Code: Función pura con nombre descriptivo
        
        Args:
            quarter_str: String como "2010 ene-mar" o "2024-V04"
            
        Returns:
            Dict con año, trimestre y fecha aproximada
        """
        try:
            # Patrones para diferentes formatos
            # Formato: "2010 ene-mar", "2010 feb-abr", etc.
            pattern1 = r'(\d{4})\s+(\w{3})-(\w{3})'
            # Formato: "2024-V04", "2024-V01", etc.
            pattern2 = r'(\d{4})-V(\d{2})'
            
            match1 = re.match(pattern1, quarter_str)
            match2 = re.match(pattern2, quarter_str)
            
            if match1:
                year = int(match1.group(1))
                start_month = match1.group(2)
                
                # Mapeo de meses en español
                month_map = {
                    'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4,
                    'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
                    'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12
                }
                
                month_num = month_map.get(start_month, 1)
                quarter = (month_num - 1) // 3 + 1
                
                return {
                    'year': year,
                    'quarter': quarter,
                    'month_start': month_num,
                    'date_approx': f"{year}-{month_num:02d}-01"
                }
            
            elif match2:
                year = int(match2.group(1))
                quarter_num = int(match2.group(2))
                
                # V01=Q1, V02=Q1, V03=Q1, V04=Q2, etc.
                quarter = ((quarter_num - 1) // 3) + 1
                month_start = ((quarter_num - 1) % 12) + 1
                
                return {
                    'year': year,
                    'quarter': quarter,
                    'month_start': month_start,
                    'date_approx': f"{year}-{month_start:02d}-01"
                }
            
            else:
                logger.warning(f"Formato de trimestre no reconocido: {quarter_str}")
                return {
                    'year': None,
                    'quarter': None,
                    'month_start': None,
                    'date_approx': None
                }
        
        except Exception as e:
            logger.error(f"Error procesando trimestre {quarter_str}: {e}")
            return {
                'year': None,
                'quarter': None, 
                'month_start': None,
                'date_approx': None
            }
    
    def _transform_temporal_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transformar datos temporales (trimestres a fechas)
        Clean Code: Método con responsabilidad única
        
        Args:
            df: DataFrame con datos temporales
            
        Returns:
            pd.DataFrame: DataFrame con columnas temporales procesadas
        """
        df_temporal = df.copy()
        
        # Procesar información temporal
        logger.info("Procesando información temporal...")
        
        temporal_info = df_temporal[DATA_COLUMNS.PROCESSED_DATE].apply(
            self._parse_quarter_to_date
        )
        
        # Extraer información en columnas separadas
        df_temporal[DATA_COLUMNS.PROCESSED_YEAR] = temporal_info.apply(
            lambda x: x['year']
        )
        df_temporal[DATA_COLUMNS.PROCESSED_QUARTER] = temporal_info.apply(
            lambda x: x['quarter']
        )
        
        # Crear columna de fecha aproximada
        df_temporal['fecha_completa'] = temporal_info.apply(
            lambda x: x['date_approx']
        )
        
        # Convertir a datetime si es posible
        try:
            df_temporal['fecha_completa'] = pd.to_datetime(
                df_temporal['fecha_completa']
            )
        except:
            logger.warning("No se pudo convertir fechas a datetime")
        
        logger.info("Información temporal procesada")
        return df_temporal
    
    def _standardize_gender_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Estandarizar valores de género
        Clean Code: Método con responsabilidad específica
        
        Args:
            df: DataFrame con columna de género
            
        Returns:
            pd.DataFrame: DataFrame con género estandarizado
        """
        df_gender = df.copy()
        
        # Mapeo de códigos de género a nombres estándar
        gender_mapping = LOS_RIOS_CONFIG.GENDER_CODES
        
        # Aplicar mapeo
        df_gender[DATA_COLUMNS.PROCESSED_GENDER] = (
            df_gender[DATA_COLUMNS.PROCESSED_GENDER].map(gender_mapping)
        )
        
        logger.info("Valores de género estandarizados")
        return df_gender
    
    def _clean_workforce_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpiar y validar valores de fuerza de trabajo
        Clean Code: Método con responsabilidad única
        
        Args:
            df: DataFrame con valores de fuerza de trabajo
            
        Returns:
            pd.DataFrame: DataFrame con valores limpios
        """
        df_clean = df.copy()
        workforce_col = DATA_COLUMNS.PROCESSED_WORKFORCE
        
        # Convertir a numérico
        df_clean[workforce_col] = pd.to_numeric(
            df_clean[workforce_col], 
            errors='coerce'
        )
        
        # Identificar valores problemáticos
        null_values = df_clean[workforce_col].isnull().sum()
        if null_values > 0:
            logger.warning(f"Se encontraron {null_values} valores nulos en fuerza de trabajo")
        
        # Verificar valores negativos
        negative_values = (df_clean[workforce_col] < 0).sum()
        if negative_values > 0:
            logger.warning(f"Se encontraron {negative_values} valores negativos")
            # Convertir negativos a 0
            df_clean.loc[df_clean[workforce_col] < 0, workforce_col] = 0
        
        # Verificar valores muy altos (outliers extremos)
        if not df_clean[workforce_col].empty:
            mean_val = df_clean[workforce_col].mean()
            std_val = df_clean[workforce_col].std()
            threshold = mean_val + (5 * std_val)  # 5 desviaciones estándar
            
            extreme_values = (df_clean[workforce_col] > threshold).sum()
            if extreme_values > 0:
                logger.warning(f"Se encontraron {extreme_values} valores extremadamente altos")
        
        logger.info("Valores de fuerza de trabajo limpiados")
        return df_clean
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agregar columnas derivadas útiles para análisis
        Clean Code: Método con responsabilidad específica
        
        Args:
            df: DataFrame base
            
        Returns:
            pd.DataFrame: DataFrame con columnas adicionales
        """
        df_derived = df.copy()
        
        # Agregar información de región
        df_derived['region_codigo'] = self.region_code
        df_derived['region_nombre'] = self.region_name
        
        # Agregar período académico/fiscal si corresponde
        if DATA_COLUMNS.PROCESSED_YEAR in df_derived.columns:
            df_derived['periodo_fiscal'] = df_derived[DATA_COLUMNS.PROCESSED_YEAR].apply(
                lambda x: f"FY{x}" if x else None
            )
        
        # Agregar indicador de temporada (alta/baja según trimestre)
        if DATA_COLUMNS.PROCESSED_QUARTER in df_derived.columns:
            season_map = {1: 'Verano', 2: 'Otoño', 3: 'Invierno', 4: 'Primavera'}
            df_derived['temporada'] = (
                df_derived[DATA_COLUMNS.PROCESSED_QUARTER].map(season_map)
            )
        
        logger.info("Columnas derivadas agregadas")
        return df_derived
    
    def _detect_and_handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detectar y manejar outliers en los datos
        Clean Code: Método con responsabilidad específica
        
        Args:
            df: DataFrame con datos
            
        Returns:
            pd.DataFrame: DataFrame con outliers marcados
        """
        df_outliers = df.copy()
        workforce_col = DATA_COLUMNS.PROCESSED_WORKFORCE
        
        if workforce_col not in df_outliers.columns:
            return df_outliers
        
        # Método IQR para detección de outliers
        Q1 = df_outliers[workforce_col].quantile(0.25)
        Q3 = df_outliers[workforce_col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - (ANALYSIS_CONFIG.IQR_MULTIPLIER * IQR)
        upper_bound = Q3 + (ANALYSIS_CONFIG.IQR_MULTIPLIER * IQR)
        
        # Marcar outliers
        df_outliers['es_outlier'] = (
            (df_outliers[workforce_col] < lower_bound) |
            (df_outliers[workforce_col] > upper_bound)
        )
        
        outlier_count = df_outliers['es_outlier'].sum()
        logger.info(f"Detectados {outlier_count} outliers ({outlier_count/len(df_outliers)*100:.1f}%)")
        
        return df_outliers
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transformar datos completos de Los Ríos
        Clean Code: Método principal con flujo claro
        
        Args:
            df: DataFrame crudo de Los Ríos
            
        Returns:
            pd.DataFrame: DataFrame transformado y listo para análisis
        """
        # Validar entrada
        if not self.validate_input(df):
            raise ValueError("Datos de entrada no válidos")
        
        logger.info("Iniciando transformación de datos de Los Ríos")
        
        # Pipeline de transformación
        df_transformed = df.copy()
        
        # 1. Limpiar nombres de columnas
        df_transformed = self._clean_column_names(df_transformed)
        
        # 2. Procesar datos temporales
        df_transformed = self._transform_temporal_data(df_transformed)
        
        # 3. Estandarizar género
        df_transformed = self._standardize_gender_values(df_transformed)
        
        # 4. Limpiar valores de fuerza de trabajo
        df_transformed = self._clean_workforce_values(df_transformed)
        
        # 5. Agregar columnas derivadas
        df_transformed = self._add_derived_columns(df_transformed)
        
        # 6. Detectar outliers
        df_transformed = self._detect_and_handle_outliers(df_transformed)
        
        # 7. Ordenar por fecha
        if 'fecha_completa' in df_transformed.columns:
            df_transformed = df_transformed.sort_values('fecha_completa')
        
        logger.info(f"Transformación completada: {len(df_transformed)} registros procesados")
        return df_transformed
    
    def get_transformation_summary(self, df_original: pd.DataFrame, df_transformed: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtener resumen de la transformación realizada
        Clean Code: Método informativo con retorno tipado
        
        Args:
            df_original: DataFrame original
            df_transformed: DataFrame transformado
            
        Returns:
            Dict con resumen de la transformación
        """
        try:
            summary = {
                "records_original": len(df_original),
                "records_transformed": len(df_transformed),
                "columns_original": len(df_original.columns),
                "columns_transformed": len(df_transformed.columns),
                "new_columns": list(set(df_transformed.columns) - set(df_original.columns)),
                "outliers_detected": 0,
                "null_values": {},
                "data_quality": {}
            }
            
            # Contar outliers si existe la columna
            if 'es_outlier' in df_transformed.columns:
                summary["outliers_detected"] = df_transformed['es_outlier'].sum()
            
            # Contar valores nulos por columna
            summary["null_values"] = df_transformed.isnull().sum().to_dict()
            
            # Información de calidad de datos
            workforce_col = DATA_COLUMNS.PROCESSED_WORKFORCE
            if workforce_col in df_transformed.columns:
                summary["data_quality"] = {
                    "workforce_mean": df_transformed[workforce_col].mean(),
                    "workforce_std": df_transformed[workforce_col].std(),
                    "workforce_min": df_transformed[workforce_col].min(),
                    "workforce_max": df_transformed[workforce_col].max()
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generando resumen de transformación: {e}")
            return {"error": str(e)}


def transform_los_rios_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Función de conveniencia para transformar datos de Los Ríos
    Clean Code: Función pura con nombre descriptivo
    
    Args:
        df: DataFrame crudo de Los Ríos
        
    Returns:
        pd.DataFrame: DataFrame transformado
    """
    transformer = LosRiosDataTransformer()
    return transformer.transform(df)


if __name__ == "__main__":
    # Demo del transformador
    print("🌲 Demo: Transformador de Datos Los Ríos")
    
    # Crear datos de ejemplo para testing
    sample_data = {
        DATA_COLUMNS.REGION_CODE: [LOS_RIOS_CONFIG.REGION_CODE] * 6,
        DATA_COLUMNS.QUARTER_NAME: ["2023 ene-mar", "2023 feb-abr", "2023 mar-may"] * 2,
        DATA_COLUMNS.GENDER_NAME: ["_T", "_T", "_T", "M", "M", "M"],
        DATA_COLUMNS.VALUE: [150.5, 155.2, 152.8, 95.1, 97.3, 96.5]
    }
    
    df_sample = pd.DataFrame(sample_data)
    print("📊 Datos de ejemplo creados")
    
    transformer = LosRiosDataTransformer()
    
    if transformer.validate_input(df_sample):
        print("✅ Datos de entrada válidos")
        
        df_transformed = transformer.transform(df_sample)
        print(f"✅ Transformación completada: {len(df_transformed)} registros")
        
        summary = transformer.get_transformation_summary(df_sample, df_transformed)
        print(f"📋 Columnas nuevas: {summary.get('new_columns', [])}")
        print(f"🎯 Outliers detectados: {summary.get('outliers_detected', 0)}")
        
    else:
        print("❌ Datos de entrada no válidos")
