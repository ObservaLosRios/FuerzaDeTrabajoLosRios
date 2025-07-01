"""
Tests unitarios para el módulo de extracción de datos de Los Ríos
"""

import unittest
import pandas as pd
from pathlib import Path
import sys

# Agregar directorio del proyecto al path
sys.path.append(str(Path(__file__).parent.parent))

from src.etl.data_extractor import LosRiosDataExtractor
from src.utils.validators import DataValidator
from config import LosRiosConfig


class TestLosRiosDataExtractor(unittest.TestCase):
    """Tests para el extractor de datos de Los Ríos."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.extractor = LosRiosDataExtractor()
        self.validator = DataValidator()
        self.config = LosRiosConfig()
    
    def test_extractor_initialization(self):
        """Test de inicialización del extractor."""
        self.assertIsInstance(self.extractor, LosRiosDataExtractor)
        self.assertEqual(self.extractor.config.REGION_CODE, "CHL14")
        self.assertEqual(self.extractor.config.REGION_NAME, "Región de Los Ríos")
    
    def test_data_validation(self):
        """Test de validación de datos básica."""
        # Crear datos de prueba
        test_data = pd.DataFrame({
            'region': ['CHL14', 'CHL14', 'CHL13'],
            'ano_trimestre': ['2023-Q1', '2023-Q2', '2023-Q1'],
            'fuerza_de_trabajo': [100000, 102000, 95000],
            'hombres': [55000, 56000, 52000],
            'mujeres': [45000, 46000, 43000]
        })
        
        # Validar estructura básica
        self.assertTrue(self.validator.validate_dataframe(test_data))
        
        # Validar datos específicos de Los Ríos
        is_valid, errors = self.validator.validate_los_rios_data(test_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_los_rios_filtering(self):
        """Test de filtrado de datos de Los Ríos."""
        # Crear datos de prueba con múltiples regiones
        test_data = pd.DataFrame({
            'region': ['CHL14', 'CHL14', 'CHL13', 'CHL15'],
            'ano_trimestre': ['2023-Q1', '2023-Q2', '2023-Q1', '2023-Q1'],
            'fuerza_de_trabajo': [100000, 102000, 95000, 88000],
            'hombres': [55000, 56000, 52000, 48000],
            'mujeres': [45000, 46000, 43000, 40000]
        })
        
        # Filtrar solo Los Ríos
        los_rios_data = test_data[test_data['region'] == self.config.REGION_CODE]
        
        # Verificar que solo quedan datos de Los Ríos
        self.assertEqual(len(los_rios_data), 2)
        self.assertTrue(all(los_rios_data['region'] == 'CHL14'))
    
    def test_data_consistency_validation(self):
        """Test de validación de consistencia de datos."""
        # Datos consistentes
        consistent_data = pd.DataFrame({
            'region': ['CHL14', 'CHL14'],
            'ano_trimestre': ['2023-Q1', '2023-Q2'],
            'fuerza_de_trabajo': [100000, 102000],
            'hombres': [55000, 56000],
            'mujeres': [45000, 46000]
        })
        
        is_valid, errors = self.validator.validate_data_consistency(consistent_data)
        self.assertTrue(is_valid)
        
        # Datos inconsistentes
        inconsistent_data = pd.DataFrame({
            'region': ['CHL14', 'CHL14'],
            'ano_trimestre': ['2023-Q1', '2023-Q2'],
            'fuerza_de_trabajo': [100000, 102000],
            'hombres': [55000, 56000],
            'mujeres': [40000, 46000]  # Total no suma
        })
        
        is_valid, errors = self.validator.validate_data_consistency(inconsistent_data)
        # Debería detectar inconsistencia (con tolerancia)
        self.assertGreater(len(errors), 0)
    
    def test_numeric_range_validation(self):
        """Test de validación de rangos numéricos."""
        # Serie con valores válidos
        valid_series = pd.Series([50000, 55000, 60000, 58000])
        is_valid, errors = self.validator.validate_numeric_range(
            valid_series, min_value=0, max_value=100000
        )
        self.assertTrue(is_valid)
        
        # Serie con valores fuera de rango
        invalid_series = pd.Series([50000, -5000, 60000, 150000])
        is_valid, errors = self.validator.validate_numeric_range(
            invalid_series, min_value=0, max_value=100000
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)


class TestDataValidator(unittest.TestCase):
    """Tests para el validador de datos."""
    
    def setUp(self):
        """Configuración inicial."""
        self.validator = DataValidator()
    
    def test_empty_dataframe_validation(self):
        """Test con DataFrame vacío."""
        empty_df = pd.DataFrame()
        self.assertFalse(self.validator.validate_dataframe(empty_df))
    
    def test_none_dataframe_validation(self):
        """Test con DataFrame None."""
        self.assertFalse(self.validator.validate_dataframe(None))
    
    def test_validation_report_generation(self):
        """Test de generación de reporte de validación."""
        test_data = pd.DataFrame({
            'region': ['CHL14', 'CHL14'],
            'ano_trimestre': ['2023-Q1', '2023-Q2'],
            'fuerza_de_trabajo': [100000, 102000],
            'hombres': [55000, 56000],
            'mujeres': [45000, 46000]
        })
        
        report = self.validator.generate_validation_report(test_data)
        
        # Verificar estructura del reporte
        self.assertIn('timestamp', report)
        self.assertIn('dataframe_info', report)
        self.assertIn('validations', report)
        self.assertIn('overall_valid', report)
        
        # Verificar información del DataFrame
        self.assertEqual(report['dataframe_info']['rows'], 2)
        self.assertEqual(report['dataframe_info']['columns'], 5)


if __name__ == '__main__':
    # Configurar suite de tests
    unittest.main(verbosity=2)
