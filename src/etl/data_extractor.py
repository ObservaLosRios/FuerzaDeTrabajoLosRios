"""
Extractor de datos para la Región de Los Ríos
Clean Code: Principio de Responsabilidad Única - Solo extrae datos
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import logging
from abc import ABC, abstractmethod

from config import (
    LOS_RIOS_CONFIG, 
    DATA_COLUMNS, 
    get_full_data_path,
    LOGGING_CONFIG
)


# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG.LOG_LEVEL),
    format=LOGGING_CONFIG.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class DataExtractor(ABC):
    """
    Clase abstracta para extractores de datos
    Clean Code: Interface Segregation Principle
    """
    
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extraer datos del origen"""
        pass
    
    @abstractmethod
    def validate_data_source(self) -> bool:
        """Validar que la fuente de datos existe y es válida"""
        pass


class LosRiosDataExtractor(DataExtractor):
    """
    Extractor específico para datos de Los Ríos del INE
    Clean Code: Nombres descriptivos y responsabilidad única
    """
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Inicializar extractor para Los Ríos
        
        Args:
            data_file: Nombre del archivo CSV (opcional)
        """
        self.data_file = data_file or LOS_RIOS_CONFIG.RAW_DATA_FILE
        self.data_path = get_full_data_path(self.data_file)
        self.region_code = LOS_RIOS_CONFIG.REGION_CODE
        
        logger.info(f"Inicializando extractor para {LOS_RIOS_CONFIG.REGION_NAME}")
    
    def validate_data_source(self) -> bool:
        """
        Validar que el archivo de datos existe y es accesible
        Clean Code: Método con una sola responsabilidad
        
        Returns:
            bool: True si el archivo es válido
        """
        try:
            if not self.data_path.exists():
                logger.error(f"Archivo no encontrado: {self.data_path}")
                return False
            
            if not self.data_path.is_file():
                logger.error(f"La ruta no es un archivo: {self.data_path}")
                return False
            
            # Verificar que tiene extensión CSV
            if self.data_path.suffix.lower() != '.csv':
                logger.error(f"Archivo no es CSV: {self.data_path}")
                return False
            
            # Verificar que no está vacío
            if self.data_path.stat().st_size == 0:
                logger.error(f"Archivo está vacío: {self.data_path}")
                return False
            
            logger.info(f"Archivo validado correctamente: {self.data_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error validando archivo: {e}")
            return False
    
    def _detect_encoding(self) -> str:
        """
        Detectar la codificación del archivo CSV
        Clean Code: Método privado con responsabilidad específica
        
        Returns:
            str: Codificación detectada
        """
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings_to_try:
            try:
                with open(self.data_path, 'r', encoding=encoding) as f:
                    f.read(1024)  # Leer una muestra
                logger.info(f"Codificación detectada: {encoding}")
                return encoding
            except UnicodeDecodeError:
                continue
        
        logger.warning("No se pudo detectar codificación, usando utf-8")
        return 'utf-8'
    
    def extract_raw_data(self) -> pd.DataFrame:
        """
        Extraer todos los datos del archivo CSV
        Clean Code: Método con nombre descriptivo
        
        Returns:
            pd.DataFrame: Datos completos del archivo
        """
        if not self.validate_data_source():
            raise FileNotFoundError(f"No se puede acceder al archivo: {self.data_path}")
        
        try:
            encoding = self._detect_encoding()
            
            logger.info("Iniciando extracción de datos completos...")
            df = pd.read_csv(self.data_path, encoding=encoding)
            
            logger.info(f"Datos extraídos: {len(df)} filas, {len(df.columns)} columnas")
            return df
            
        except Exception as e:
            logger.error(f"Error extrayendo datos: {e}")
            raise
    
    def extract(self) -> pd.DataFrame:
        """
        Extraer datos específicos de Los Ríos
        Clean Code: Método principal con responsabilidad clara
        
        Returns:
            pd.DataFrame: Datos filtrados de Los Ríos
        """
        # Extraer datos completos
        df_complete = self.extract_raw_data()
        
        # Filtrar por Los Ríos
        logger.info(f"Filtrando datos para región {self.region_code}")
        
        region_column = DATA_COLUMNS.REGION_CODE
        if region_column not in df_complete.columns:
            raise ValueError(f"Columna de región no encontrada: {region_column}")
        
        df_los_rios = df_complete[
            df_complete[region_column] == self.region_code
        ].copy()
        
        if df_los_rios.empty:
            raise ValueError(f"No se encontraron datos para región {self.region_code}")
        
        logger.info(f"Datos de Los Ríos extraídos: {len(df_los_rios)} registros")
        return df_los_rios
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Obtener resumen de los datos extraídos
        Clean Code: Método informativo con retorno tipado
        
        Returns:
            Dict[str, Any]: Resumen de los datos
        """
        try:
            df = self.extract()
            
            # Calcular estadísticas básicas
            summary = {
                "total_records": len(df),
                "columns": list(df.columns),
                "region_code": self.region_code,
                "region_name": LOS_RIOS_CONFIG.REGION_NAME,
                "data_file": self.data_file,
                "date_range": None,
                "gender_breakdown": None
            }
            
            # Agregar información de fechas si existe
            quarter_col = DATA_COLUMNS.QUARTER_NAME
            if quarter_col in df.columns:
                quarters = df[quarter_col].unique()
                summary["date_range"] = {
                    "start": quarters.min() if len(quarters) > 0 else None,
                    "end": quarters.max() if len(quarters) > 0 else None,
                    "total_quarters": len(quarters)
                }
            
            # Agregar breakdown por género
            gender_col = DATA_COLUMNS.GENDER_NAME
            if gender_col in df.columns:
                gender_counts = df[gender_col].value_counts().to_dict()
                summary["gender_breakdown"] = gender_counts
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generando resumen: {e}")
            return {"error": str(e)}
    
    def extract_sample(self, n_records: int = 10) -> pd.DataFrame:
        """
        Extraer una muestra de datos para revisión
        Clean Code: Método utilitario con parámetro por defecto
        
        Args:
            n_records: Número de registros a extraer
            
        Returns:
            pd.DataFrame: Muestra de datos
        """
        df = self.extract()
        sample = df.head(n_records).copy()
        
        logger.info(f"Muestra extraída: {len(sample)} registros")
        return sample


def extract_los_rios_data() -> pd.DataFrame:
    """
    Función de conveniencia para extraer datos de Los Ríos
    Clean Code: Función pura con nombre descriptivo
    
    Returns:
        pd.DataFrame: Datos de Los Ríos
    """
    extractor = LosRiosDataExtractor()
    return extractor.extract()


if __name__ == "__main__":
    # Demo del extractor
    print("🌲 Demo: Extractor de Datos Los Ríos")
    
    extractor = LosRiosDataExtractor()
    
    # Validar fuente
    if extractor.validate_data_source():
        print("✅ Fuente de datos válida")
        
        # Obtener resumen
        summary = extractor.get_data_summary()
        print(f"📊 Registros totales: {summary.get('total_records', 'N/A')}")
        print(f"📅 Rango temporal: {summary.get('date_range', 'N/A')}")
        print(f"👥 Breakdown género: {summary.get('gender_breakdown', 'N/A')}")
        
        # Extraer muestra
        sample = extractor.extract_sample(5)
        print(f"\n📋 Muestra de datos:")
        print(sample.head())
        
    else:
        print("❌ Fuente de datos no válida")
