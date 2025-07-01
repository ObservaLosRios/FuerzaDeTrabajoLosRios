"""
Data Loader para el proyecto Los Ríos
Clean Code: Principio de Responsabilidad Única - solo carga y persistencia de datos
"""

import pandas as pd
import json
import pickle
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging
from datetime import datetime

from ...config import LosRiosConfig, DataConfig, LoggingConfig
from ..utils.logger import setup_logger
from ..utils.validators import DataValidator


class LosRiosDataLoader:
    """
    Clase responsable de la carga y persistencia de datos procesados.
    
    Clean Code Principles:
    - Single Responsibility: Solo maneja la carga/guardado de datos
    - Dependency Inversion: Depende de abstracciones (configuraciones)
    - Open/Closed: Extensible para nuevos formatos sin modificar código existente
    """
    
    def __init__(self, config: Optional[LosRiosConfig] = None):
        """
        Inicializa el data loader con configuración.
        
        Args:
            config: Configuración específica de Los Ríos
        """
        self.config = config or LosRiosConfig()
        self.data_config = DataConfig()
        self.logger = setup_logger(
            name=self.__class__.__name__,
            log_file=LoggingConfig().LOG_FILES["data_loader"]
        )
        self.validator = DataValidator()
        
        # Crear directorios si no existen
        self._ensure_directories()
        
        self.logger.info("LosRiosDataLoader inicializado correctamente")
    
    def _ensure_directories(self) -> None:
        """Crea directorios necesarios si no existen."""
        directories = [
            self.data_config.PROCESSED_PATH,
            self.data_config.OUTPUTS_PATH,
            self.data_config.REPORTS_PATH
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_processed_data(
        self, 
        data: pd.DataFrame, 
        filename: Optional[str] = None,
        format_type: str = "csv"
    ) -> Path:
        """
        Guarda datos procesados en el formato especificado.
        
        Args:
            data: DataFrame con datos procesados
            filename: Nombre del archivo (opcional)
            format_type: Formato de salida ("csv", "parquet", "excel", "json")
            
        Returns:
            Path del archivo guardado
            
        Raises:
            ValueError: Si el formato no es soportado
            IOError: Si hay problemas al guardar el archivo
        """
        try:
            # Validar datos de entrada
            if not self.validator.validate_dataframe(data):
                raise ValueError("DataFrame no válido para guardar")
            
            # Generar nombre de archivo si no se proporciona
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"los_rios_processed_{timestamp}"
            
            # Determinar extensión y ruta según formato
            file_path = self._get_file_path(filename, format_type, "processed")
            
            # Guardar según formato
            self._save_by_format(data, file_path, format_type)
            
            # Log y estadísticas
            file_size = file_path.stat().st_size / 1024 / 1024  # MB
            self.logger.info(
                f"Datos procesados guardados: {file_path.name} "
                f"({len(data)} registros, {file_size:.2f} MB)"
            )
            
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error guardando datos procesados: {str(e)}")
            raise
    
    def save_analysis_results(
        self, 
        results: Dict[str, Any], 
        analysis_name: str,
        format_type: str = "json"
    ) -> Path:
        """
        Guarda resultados de análisis.
        
        Args:
            results: Diccionario con resultados del análisis
            analysis_name: Nombre del análisis
            format_type: Formato de salida ("json", "pickle")
            
        Returns:
            Path del archivo guardado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{analysis_name}_results_{timestamp}"
            file_path = self._get_file_path(filename, format_type, "outputs")
            
            if format_type == "json":
                # Convertir objetos no serializables a string
                serializable_results = self._make_json_serializable(results)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            elif format_type == "pickle":
                with open(file_path, 'wb') as f:
                    pickle.dump(results, f)
            
            else:
                raise ValueError(f"Formato {format_type} no soportado para resultados")
            
            self.logger.info(f"Resultados de análisis guardados: {file_path.name}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error guardando resultados: {str(e)}")
            raise
    
    def save_visualization(
        self, 
        figure, 
        name: str, 
        format_type: str = "png"
    ) -> Path:
        """
        Guarda visualizaciones generadas.
        
        Args:
            figure: Objeto de figura (matplotlib, plotly, etc.)
            name: Nombre de la visualización
            format_type: Formato de imagen ("png", "svg", "pdf", "html")
            
        Returns:
            Path del archivo guardado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}"
            file_path = self._get_file_path(filename, format_type, "outputs")
            
            # Guardar según el tipo de figura
            if hasattr(figure, 'savefig'):  # matplotlib
                figure.savefig(file_path, dpi=300, bbox_inches='tight')
            elif hasattr(figure, 'write_html'):  # plotly
                if format_type == "html":
                    figure.write_html(file_path)
                else:
                    figure.write_image(file_path, width=1200, height=800)
            else:
                raise ValueError("Tipo de figura no soportado")
            
            self.logger.info(f"Visualización guardada: {file_path.name}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error guardando visualización: {str(e)}")
            raise
    
    def load_processed_data(self, filename: str) -> pd.DataFrame:
        """
        Carga datos procesados desde archivo.
        
        Args:
            filename: Nombre del archivo a cargar
            
        Returns:
            DataFrame con los datos cargados
        """
        try:
            file_path = self.data_config.PROCESSED_PATH / filename
            
            if not file_path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            
            # Detectar formato por extensión
            extension = file_path.suffix.lower()
            
            if extension == '.csv':
                data = pd.read_csv(file_path)
            elif extension == '.parquet':
                data = pd.read_parquet(file_path)
            elif extension in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path)
            elif extension == '.json':
                data = pd.read_json(file_path)
            else:
                raise ValueError(f"Formato {extension} no soportado para carga")
            
            self.logger.info(f"Datos cargados: {filename} ({len(data)} registros)")
            return data
            
        except Exception as e:
            self.logger.error(f"Error cargando datos: {str(e)}")
            raise
    
    def _get_file_path(self, filename: str, format_type: str, folder: str) -> Path:
        """Construye la ruta completa del archivo."""
        if folder == "processed":
            base_path = self.data_config.PROCESSED_PATH
        elif folder == "outputs":
            base_path = self.data_config.OUTPUTS_PATH
        else:
            base_path = self.data_config.REPORTS_PATH
        
        return base_path / f"{filename}.{format_type}"
    
    def _save_by_format(self, data: pd.DataFrame, file_path: Path, format_type: str) -> None:
        """Guarda DataFrame según el formato especificado."""
        if format_type == "csv":
            data.to_csv(file_path, index=False, encoding='utf-8')
        elif format_type == "parquet":
            data.to_parquet(file_path, index=False)
        elif format_type == "excel":
            data.to_excel(file_path, index=False, engine='openpyxl')
        elif format_type == "json":
            data.to_json(file_path, orient='records', indent=2, force_ascii=False)
        else:
            raise ValueError(f"Formato {format_type} no soportado")
    
    def _make_json_serializable(self, obj: Any) -> Any:
        """Convierte objetos no serializables a JSON."""
        if isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        elif isinstance(obj, (pd.Series, pd.DataFrame)):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return str(obj)
        else:
            return obj
    
    def get_saved_files_summary(self) -> Dict[str, Any]:
        """
        Retorna un resumen de archivos guardados.
        
        Returns:
            Diccionario con información de archivos
        """
        summary = {
            "processed_files": [],
            "output_files": [],
            "total_size_mb": 0
        }
        
        try:
            # Archivos procesados
            for file_path in self.data_config.PROCESSED_PATH.glob("*"):
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / 1024 / 1024
                    summary["processed_files"].append({
                        "name": file_path.name,
                        "size_mb": round(size_mb, 2),
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
                    summary["total_size_mb"] += size_mb
            
            # Archivos de salida
            for file_path in self.data_config.OUTPUTS_PATH.glob("*"):
                if file_path.is_file():
                    size_mb = file_path.stat().st_size / 1024 / 1024
                    summary["output_files"].append({
                        "name": file_path.name,
                        "size_mb": round(size_mb, 2),
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
                    summary["total_size_mb"] += size_mb
            
            summary["total_size_mb"] = round(summary["total_size_mb"], 2)
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generando resumen de archivos: {str(e)}")
            return summary
