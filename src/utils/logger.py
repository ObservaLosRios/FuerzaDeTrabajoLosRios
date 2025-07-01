"""
Sistema de logging para el proyecto Los Ríos
Clean Code: configuración centralizada de logging
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from datetime import datetime
import sys

from ...config import LoggingConfig


class LoggerConfig:
    """
    Configuración centralizada del sistema de logging.
    
    Clean Code Principles:
    - Single Responsibility: Solo configuración de logging
    - Configuration Management: Centralización de configuraciones
    """
    
    def __init__(self):
        """Inicializa la configuración de logging."""
        self.config = LoggingConfig()
        self._ensure_log_directory()
    
    def _ensure_log_directory(self) -> None:
        """Crea el directorio de logs si no existe."""
        self.config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    def get_formatter(self) -> logging.Formatter:
        """
        Retorna el formateador estándar para logs.
        
        Returns:
            Formatter configurado
        """
        return logging.Formatter(
            fmt=self.config.LOG_FORMAT,
            datefmt=self.config.DATE_FORMAT
        )
    
    def setup_file_handler(self, log_file: Path) -> logging.FileHandler:
        """
        Configura un handler para archivo de log.
        
        Args:
            log_file: Ruta del archivo de log
            
        Returns:
            FileHandler configurado
        """
        # Usar RotatingFileHandler para evitar archivos demasiado grandes
        handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=self.config.MAX_LOG_SIZE,
            backupCount=self.config.BACKUP_COUNT,
            encoding='utf-8'
        )
        handler.setFormatter(self.get_formatter())
        return handler
    
    def setup_console_handler(self) -> logging.StreamHandler:
        """
        Configura un handler para consola.
        
        Returns:
            StreamHandler configurado
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.get_formatter())
        return handler


def setup_logger(
    name: str, 
    log_file: Optional[Path] = None, 
    level: int = logging.INFO,
    console_output: bool = True
) -> logging.Logger:
    """
    Configura un logger específico para un módulo.
    
    Args:
        name: Nombre del logger (generalmente nombre de la clase)
        log_file: Archivo específico de log (opcional)
        level: Nivel de logging
        console_output: Si mostrar también en consola
        
    Returns:
        Logger configurado
        
    Clean Code: Factory Method Pattern para creación de loggers
    """
    # Crear logger
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Configurar handlers
    config = LoggerConfig()
    
    # Handler de archivo
    if log_file:
        file_handler = config.setup_file_handler(log_file)
        logger.addHandler(file_handler)
    
    # Handler de consola
    if console_output:
        console_handler = config.setup_console_handler()
        logger.addHandler(console_handler)
    
    # Evitar propagación al root logger
    logger.propagate = False
    
    return logger


def setup_project_logging() -> None:
    """
    Configura el logging para todo el proyecto.
    
    Clean Code: Single point of configuration
    """
    config = LoggingConfig()
    
    # Configurar logger raíz del proyecto
    root_logger = logging.getLogger('los_rios_analysis')
    root_logger.setLevel(config.LOG_LEVEL)
    
    # Handler principal del proyecto
    main_log_file = config.LOG_FILES["main"]
    logger_config = LoggerConfig()
    
    file_handler = logger_config.setup_file_handler(main_log_file)
    console_handler = logger_config.setup_console_handler()
    
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configurar loggers de bibliotecas externas
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('plotly').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Log inicial
    root_logger.info("=" * 50)
    root_logger.info("Sistema de logging inicializado")
    root_logger.info(f"Directorio de logs: {config.LOG_DIR}")
    root_logger.info("=" * 50)


class PerformanceLogger:
    """
    Logger especializado para medir performance.
    
    Clean Code: Specific purpose class
    """
    
    def __init__(self, name: str):
        """
        Inicializa el logger de performance.
        
        Args:
            name: Nombre del proceso a monitorear
        """
        self.name = name
        self.logger = setup_logger(
            f"{name}_performance",
            LoggingConfig().LOG_FILES["performance"]
        )
        self.start_time = None
    
    def start(self) -> None:
        """Inicia el monitoreo de tiempo."""
        self.start_time = datetime.now()
        self.logger.info(f"INICIO - {self.name}")
    
    def end(self, additional_info: str = "") -> float:
        """
        Finaliza el monitoreo y registra el tiempo transcurrido.
        
        Args:
            additional_info: Información adicional para el log
            
        Returns:
            Tiempo transcurrido en segundos
        """
        if self.start_time is None:
            self.logger.warning(f"Timer no iniciado para {self.name}")
            return 0.0
        
        end_time = datetime.now()
        elapsed_time = (end_time - self.start_time).total_seconds()
        
        info_str = f"FIN - {self.name} - Tiempo: {elapsed_time:.2f}s"
        if additional_info:
            info_str += f" - {additional_info}"
        
        self.logger.info(info_str)
        return elapsed_time
    
    def checkpoint(self, checkpoint_name: str) -> float:
        """
        Registra un checkpoint intermedio.
        
        Args:
            checkpoint_name: Nombre del checkpoint
            
        Returns:
            Tiempo transcurrido desde el inicio
        """
        if self.start_time is None:
            self.logger.warning(f"Timer no iniciado para checkpoint {checkpoint_name}")
            return 0.0
        
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()
        
        self.logger.info(f"CHECKPOINT - {checkpoint_name} - Tiempo: {elapsed_time:.2f}s")
        return elapsed_time


def log_function_call(func):
    """
    Decorador para loggear automáticamente llamadas a funciones.
    
    Clean Code: Decorator pattern para cross-cutting concerns
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        
        # Log de entrada
        logger.debug(f"Llamando a {func.__name__} con args={args}, kwargs={kwargs}")
        
        try:
            # Ejecutar función
            result = func(*args, **kwargs)
            
            # Log de éxito
            logger.debug(f"{func.__name__} ejecutada exitosamente")
            return result
            
        except Exception as e:
            # Log de error
            logger.error(f"Error en {func.__name__}: {str(e)}")
            raise
    
    return wrapper


def log_dataframe_info(df, operation_name: str, logger: logging.Logger) -> None:
    """
    Registra información detallada sobre un DataFrame.
    
    Args:
        df: DataFrame a loggear
        operation_name: Nombre de la operación
        logger: Logger a usar
        
    Clean Code: Specific utility function
    """
    if df is not None and hasattr(df, 'shape'):
        logger.info(
            f"{operation_name} - Shape: {df.shape}, "
            f"Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB, "
            f"Columns: {list(df.columns)[:5]}..." if len(df.columns) > 5 else f"Columns: {list(df.columns)}"
        )
    else:
        logger.warning(f"{operation_name} - DataFrame es None o inválido")
