"""
Configuration settings for INE Chile Labour Force Analysis project.
Following Clean Code and SOLID principles.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class PathConfig:
    """Configuration for project paths following SOLID principles."""
    
    # Project root
    PROJECT_ROOT: Path = Path(__file__).parent
    
    # Data directories
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    OUTPUT_DATA_DIR: Path = DATA_DIR / "outputs"
    
    # Source code directories
    SRC_DIR: Path = PROJECT_ROOT / "src"
    NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"
    SCRIPTS_DIR: Path = PROJECT_ROOT / "scripts"
    TESTS_DIR: Path = PROJECT_ROOT / "tests"
    DOCS_DIR: Path = PROJECT_ROOT / "docs"
    
    # Logs
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    
    def __post_init__(self):
        """Create directories if they don't exist."""
        for path in [
            self.RAW_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.OUTPUT_DATA_DIR,
            self.LOGS_DIR,
        ]:
            path.mkdir(parents=True, exist_ok=True)


@dataclass
class DataConfig:
    """Configuration for data processing and analysis."""
    
    # INE Data Settings
    INE_BASE_URL: str = "https://www.ine.cl"
    INE_API_BASE: str = "https://si3.ine.cl/siete"
    
    # File settings
    ENCODING: str = "utf-8"
    DECIMAL_SEPARATOR: str = ","
    THOUSANDS_SEPARATOR: str = "."
    
    # Data quality settings
    MAX_MISSING_THRESHOLD: float = 0.3  # 30% missing data threshold
    OUTLIER_THRESHOLD: float = 3.0  # Z-score threshold for outliers
    
    # Time series settings
    MIN_YEAR: int = 2010
    MAX_YEAR: int = 2025
    
    # Regional codes mapping
    REGIONAL_CODES: Dict[str, str] = None
    
    def __post_init__(self):
        """Initialize regional codes mapping."""
        self.REGIONAL_CODES = {
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


@dataclass
class VisualizationConfig:
    """Configuration for visualizations and plots."""
    
    # Plot settings
    FIGURE_SIZE: tuple = (12, 8)
    DPI: int = 300
    STYLE: str = "seaborn-v0_8"
    COLOR_PALETTE: str = "viridis"
    
    # Colors for specific categories
    COLORS: Dict[str, str] = None
    
    # Font settings
    FONT_SIZE: int = 12
    TITLE_SIZE: int = 16
    LABEL_SIZE: int = 10
    
    def __post_init__(self):
        """Initialize color mapping."""
        self.COLORS = {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "danger": "#d62728",
            "warning": "#ff7f0e",
            "info": "#17a2b8",
            "light": "#f8f9fa",
            "dark": "#343a40",
        }


@dataclass
class LoggingConfig:
    """Configuration for logging system."""
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "30 days"


class Config:
    """Main configuration class that aggregates all configurations."""
    
    def __init__(self):
        self.paths = PathConfig()
        self.data = DataConfig()
        self.visualization = VisualizationConfig()
        self.logging = LoggingConfig()
        
        # Environment settings
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # Performance settings
        self.n_jobs = int(os.getenv("N_JOBS", "-1"))  # -1 uses all available cores
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "10000"))
        
    def get_database_url(self) -> str:
        """Get database URL if needed for future extensions."""
        return os.getenv("DATABASE_URL", "sqlite:///labour_force.db")
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"
    
    def get_cache_settings(self) -> Dict[str, Any]:
        """Get cache configuration."""
        return {
            "cache_type": os.getenv("CACHE_TYPE", "simple"),
            "cache_timeout": int(os.getenv("CACHE_TIMEOUT", "300")),
        }


# Global configuration instance
config = Config()
