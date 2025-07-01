"""
Configuración centralizada del proyecto Los Ríos
Siguiendo principios de Clean Code: constantes centralizadas y configuración limpia
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any
import os


# Rutas del proyecto (Clean Code: nombres descriptivos)
PROJECT_ROOT = Path(__file__).parent
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
DATA_OUTPUTS_PATH = PROJECT_ROOT / "data" / "outputs"
LOGS_PATH = PROJECT_ROOT / "logs"
NOTEBOOKS_PATH = PROJECT_ROOT / "notebooks"


@dataclass
class LosRiosConfig:
    """
    Configuración específica para el análisis de Los Ríos
    Clean Code: clase con responsabilidad única
    """
    # Identificadores de Los Ríos
    REGION_CODE: str = "CHL14"
    REGION_NAME: str = "Región de Los Ríos"
    REGION_CAPITAL: str = "Valdivia"
    
    # Códigos de género del INE
    GENDER_CODES: Dict[str, str] = None
    
    # Códigos de indicadores
    INDICATOR_CODE: str = "ENE_FDT"
    INDICATOR_NAME: str = "Fuerza de trabajo (proyecciones base 2002)"
    
    # Configuración de análisis temporal
    START_YEAR: int = 2010
    END_YEAR: int = 2025
    
    # Archivos de datos
    RAW_DATA_FILE: str = "ENE_FDT_01072025123700776.csv"
    PROCESSED_DATA_FILE: str = "los_rios_processed.csv"
    
    def __post_init__(self):
        """Inicializar valores después de la construcción"""
        if self.GENDER_CODES is None:
            self.GENDER_CODES = {
                "_T": "Ambos sexos",
                "M": "Hombres", 
                "F": "Mujeres"
            }


@dataclass
class DataColumns:
    """
    Definición de columnas del dataset
    Clean Code: nombres de columnas centralizados
    """
    # Columnas originales del INE
    INDICATOR_CODE: str = "DTI_CL_INDICADOR"
    INDICATOR_NAME: str = "Indicador"
    QUARTER_CODE: str = "DTI_CL_TRIMESTRE_MOVIL"
    QUARTER_NAME: str = "Trimestre Móvil"
    REGION_CODE: str = "DTI_CL_REGION"
    REGION_NAME: str = "Región"
    GENDER_CODE: str = "DTI_CL_SEXO"
    GENDER_NAME: str = "Sexo"
    VALUE: str = "Value"
    FLAG_CODES: str = "Flag Codes"
    FLAGS: str = "Flags"
    
    # Columnas procesadas (Clean Code: nombres claros)
    PROCESSED_DATE: str = "fecha"
    PROCESSED_YEAR: str = "año"
    PROCESSED_QUARTER: str = "trimestre"
    PROCESSED_WORKFORCE: str = "fuerza_trabajo"
    PROCESSED_GENDER: str = "genero"


@dataclass
class VisualizationConfig:
    """
    Configuración para visualizaciones
    Clean Code: configuración específica y reutilizable
    """
    # Colores de la región Los Ríos (Verde = bosques, Azul = ríos)
    REGION_COLORS: Dict[str, str] = None
    
    # Configuración de gráficos
    FIGURE_SIZE: tuple = (12, 8)
    DPI: int = 300
    STYLE: str = "seaborn-v0_8"
    
    # Configuración de plotly
    PLOTLY_TEMPLATE: str = "plotly_white"
    
    # Formatos de exportación
    EXPORT_FORMATS: List[str] = None
    
    def __post_init__(self):
        """Inicializar valores después de la construcción"""
        if self.REGION_COLORS is None:
            self.REGION_COLORS = {
                "primary": "#2E8B57",      # Verde bosque
                "secondary": "#4682B4",    # Azul río
                "accent": "#DAA520",       # Dorado (turismo)
                "total": "#2E8B57",        # Verde para totales
                "male": "#4682B4",         # Azul para hombres
                "female": "#DC143C"        # Rojo para mujeres
            }
        
        if self.EXPORT_FORMATS is None:
            self.EXPORT_FORMATS = ["png", "pdf", "svg"]


@dataclass
class LoggingConfig:
    """
    Configuración del sistema de logging
    Clean Code: configuración centralizada de logs
    """
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "los_rios_analysis.log"
    MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT: int = 5


@dataclass
class AnalysisConfig:
    """
    Configuración para análisis estadístico
    Clean Code: parámetros de análisis centralizados
    """
    # Detección de outliers
    OUTLIER_METHOD: str = "IQR"  # IQR o Z-score
    IQR_MULTIPLIER: float = 1.5
    Z_SCORE_THRESHOLD: float = 3.0
    
    # Análisis de tendencias
    CONFIDENCE_INTERVAL: float = 0.95
    SEASONAL_PERIODS: int = 4  # Trimestres
    
    # Proyecciones
    FORECAST_PERIODS: int = 8  # 2 años (8 trimestres)
    
    # Validación de datos
    MIN_RECORDS_REQUIRED: int = 10
    MAX_MISSING_PERCENTAGE: float = 0.05  # 5%


class EnvironmentConfig:
    """
    Configuración de entorno
    Clean Code: gestión de variables de entorno
    """
    @staticmethod
    def get_environment() -> str:
        """Obtener el entorno de ejecución"""
        return os.getenv("ENVIRONMENT", "development")
    
    @staticmethod
    def is_development() -> bool:
        """Verificar si estamos en desarrollo"""
        return EnvironmentConfig.get_environment() == "development"
    
    @staticmethod
    def is_production() -> bool:
        """Verificar si estamos en producción"""
        return EnvironmentConfig.get_environment() == "production"


# Instancias globales de configuración (Singleton pattern)
LOS_RIOS_CONFIG = LosRiosConfig()
DATA_COLUMNS = DataColumns()
VISUALIZATION_CONFIG = VisualizationConfig()
LOGGING_CONFIG = LoggingConfig()
ANALYSIS_CONFIG = AnalysisConfig()


def get_full_data_path(filename: str) -> Path:
    """
    Obtener ruta completa de archivo de datos
    Clean Code: función pura con nombre descriptivo
    """
    return DATA_RAW_PATH / filename


def get_processed_data_path(filename: str) -> Path:
    """
    Obtener ruta completa de archivo procesado
    Clean Code: función pura con nombre descriptivo
    """
    return DATA_PROCESSED_PATH / filename


def get_output_path(filename: str) -> Path:
    """
    Obtener ruta completa de archivo de salida
    Clean Code: función pura con nombre descriptivo
    """
    return DATA_OUTPUTS_PATH / filename


def ensure_directories_exist() -> None:
    """
    Crear directorios necesarios si no existen
    Clean Code: función con responsabilidad única
    """
    directories = [
        DATA_RAW_PATH,
        DATA_PROCESSED_PATH, 
        DATA_OUTPUTS_PATH,
        LOGS_PATH
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Demo de configuración
    print("🌲 Configuración Los Ríos - Demo")
    print(f"Región: {LOS_RIOS_CONFIG.REGION_NAME}")
    print(f"Capital: {LOS_RIOS_CONFIG.REGION_CAPITAL}")
    print(f"Código: {LOS_RIOS_CONFIG.REGION_CODE}")
    print(f"Archivo de datos: {LOS_RIOS_CONFIG.RAW_DATA_FILE}")
    print(f"Colores principales: {VISUALIZATION_CONFIG.REGION_COLORS}")
