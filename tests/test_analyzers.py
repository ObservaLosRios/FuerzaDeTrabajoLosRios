"""
Tests unitarios para los analizadores de Los Ríos
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Agregar directorio del proyecto al path
sys.path.append(str(Path(__file__).parent.parent))

from src.models.labour_analyzer import LabourAnalyzer
from src.models.demographics import DemographicsAnalyzer
from src.models.statistics_engine import StatisticsEngine
from src.utils.helpers import HelperFunctions


class TestLabourAnalyzer(unittest.TestCase):
    """Tests para el analizador del mercado laboral."""
    
    def setUp(self):
        """Configuración inicial."""
        self.analyzer = LabourAnalyzer()
        self.test_data = self._create_test_data()
    
    def _create_test_data(self) -> pd.DataFrame:
        """Crea datos de prueba para testing."""
        return pd.DataFrame({
            'region': ['CHL14'] * 12,
            'ano_trimestre': [
                '2022-Q1', '2022-Q2', '2022-Q3', '2022-Q4',
                '2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4',
                '2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4'
            ],
            'fuerza_de_trabajo': [
                100000, 102000, 104000, 103000,
                105000, 107000, 109000, 108000,
                110000, 112000, 114000, 113000
            ],
            'hombres': [
                55000, 56000, 57000, 56500,
                57500, 58500, 59500, 59000,
                60000, 61000, 62000, 61500
            ],
            'mujeres': [
                45000, 46000, 47000, 46500,
                47500, 48500, 49500, 49000,
                50000, 51000, 52000, 51500
            ]
        })
    
    def test_analyzer_initialization(self):
        """Test de inicialización del analizador."""
        self.assertIsInstance(self.analyzer, LabourAnalyzer)
        self.assertEqual(self.analyzer.config.REGION_CODE, "CHL14")
    
    def test_current_indicators_calculation(self):
        """Test de cálculo de indicadores actuales."""
        results = self.analyzer.analyze_labour_market(self.test_data)
        current_indicators = results.get('current_indicators', {})
        
        # Verificar que se calcularon los indicadores
        self.assertIn('latest_period', current_indicators)
        self.assertIn('total_labour_force', current_indicators)
        self.assertIn('male_participation_pct', current_indicators)
        self.assertIn('female_participation_pct', current_indicators)
        
        # Verificar que los porcentajes suman aproximadamente 100%
        male_pct = current_indicators.get('male_participation_pct', 0)
        female_pct = current_indicators.get('female_participation_pct', 0)
        self.assertAlmostEqual(male_pct + female_pct, 100.0, places=1)
    
    def test_trends_analysis(self):
        """Test de análisis de tendencias."""
        results = self.analyzer.analyze_labour_market(self.test_data)
        trends = results.get('historical_trends', {})
        
        # Verificar que se analizaron las tendencias
        self.assertIn('total_labour_force', trends)
        
        total_trend = trends['total_labour_force']
        self.assertIn('growth_rates', total_trend)
        self.assertIn('trend_direction', total_trend)
        
        # Verificar que la tendencia es creciente (datos de prueba van en aumento)
        self.assertEqual(total_trend['trend_direction'], 'increasing')
    
    def test_gender_analysis(self):
        """Test de análisis de género."""
        results = self.analyzer.analyze_labour_market(self.test_data)
        gender_analysis = results.get('gender_analysis', {})
        
        # Verificar estructura del análisis de género
        self.assertIn('average_participation', gender_analysis)
        self.assertIn('participation_ratio', gender_analysis)
        self.assertIn('growth_comparison', gender_analysis)


class TestDemographicsAnalyzer(unittest.TestCase):
    """Tests para el analizador demográfico."""
    
    def setUp(self):
        """Configuración inicial."""
        self.analyzer = DemographicsAnalyzer()
        self.test_data = pd.DataFrame({
            'region': ['CHL14'] * 8,
            'ano_trimestre': ['2023-Q1', '2023-Q2', '2023-Q3', '2023-Q4',
                             '2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4'],
            'fuerza_de_trabajo': [100000, 102000, 104000, 103000,
                                 105000, 107000, 109000, 108000],
            'hombres': [55000, 56000, 57000, 56500,
                       57500, 58500, 59500, 59000],
            'mujeres': [45000, 46000, 47000, 46500,
                       47500, 48500, 49500, 49000]
        })
    
    def test_gender_distribution_analysis(self):
        """Test de análisis de distribución por género."""
        results = self.analyzer.analyze_demographic_structure(self.test_data)
        gender_dist = results.get('gender_distribution', {})
        
        # Verificar estructura
        self.assertIn('total_male', gender_dist)
        self.assertIn('total_female', gender_dist)
        self.assertIn('male_percentage', gender_dist)
        self.assertIn('female_percentage', gender_dist)
        self.assertIn('gender_ratio', gender_dist)
        
        # Verificar que los porcentajes son razonables
        male_pct = gender_dist['male_percentage']
        female_pct = gender_dist['female_percentage']
        self.assertAlmostEqual(male_pct + female_pct, 100.0, places=1)
        self.assertGreater(male_pct, 0)
        self.assertGreater(female_pct, 0)
    
    def test_participation_rates_calculation(self):
        """Test de cálculo de tasas de participación."""
        results = self.analyzer.analyze_demographic_structure(self.test_data)
        participation = results.get('participation_rates', {})
        
        # Verificar estructura
        self.assertIn('current_male_rate', participation)
        self.assertIn('current_female_rate', participation)
        self.assertIn('historical_average_male', participation)
        self.assertIn('historical_average_female', participation)


class TestStatisticsEngine(unittest.TestCase):
    """Tests para el motor estadístico."""
    
    def setUp(self):
        """Configuración inicial."""
        self.engine = StatisticsEngine()
        self.test_series = pd.Series([100, 102, 105, 103, 108, 110, 107, 112, 115])
    
    def test_descriptive_statistics(self):
        """Test de estadísticas descriptivas."""
        stats = self.engine.calculate_descriptive_statistics(self.test_series)
        
        # Verificar que se calcularon todas las estadísticas
        expected_keys = ['count', 'mean', 'median', 'std_dev', 'variance',
                        'skewness', 'kurtosis', 'min', 'max', 'range', 'q1', 'q3', 'iqr']
        
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Verificar valores lógicos
        self.assertEqual(stats['count'], len(self.test_series))
        self.assertEqual(stats['min'], self.test_series.min())
        self.assertEqual(stats['max'], self.test_series.max())
        self.assertEqual(stats['range'], stats['max'] - stats['min'])
    
    def test_trend_analysis(self):
        """Test de análisis de tendencias."""
        trend_analysis = self.engine.perform_trend_analysis(self.test_series)
        
        # Verificar estructura
        self.assertIn('linear_regression', trend_analysis)
        self.assertIn('mann_kendall', trend_analysis)
        
        # Verificar regresión lineal
        linear_reg = trend_analysis['linear_regression']
        self.assertIn('slope', linear_reg)
        self.assertIn('r_squared', linear_reg)
        self.assertIn('p_value', linear_reg)
        
        # Verificar Mann-Kendall
        mk_test = trend_analysis['mann_kendall']
        self.assertIn('trend', mk_test)
        self.assertIn('significant', mk_test)
    
    def test_correlation_matrix(self):
        """Test de matriz de correlaciones."""
        test_df = pd.DataFrame({
            'var1': [1, 2, 3, 4, 5],
            'var2': [2, 4, 6, 8, 10],  # Perfectamente correlacionada
            'var3': [5, 4, 3, 2, 1]   # Negativamente correlacionada
        })
        
        corr_analysis = self.engine.calculate_correlation_matrix(test_df)
        
        # Verificar estructura
        self.assertIn('pearson', corr_analysis)
        self.assertIn('spearman', corr_analysis)
        self.assertIn('strongest_correlations', corr_analysis)
        
        # Verificar que encuentra correlaciones fuertes
        strongest_corrs = corr_analysis['strongest_correlations']
        self.assertGreater(len(strongest_corrs), 0)


class TestHelperFunctions(unittest.TestCase):
    """Tests para funciones auxiliares."""
    
    def setUp(self):
        """Configuración inicial."""
        self.helpers = HelperFunctions()
    
    def test_parse_ine_period(self):
        """Test de parseo de períodos del INE."""
        # Test casos válidos
        year, quarter = self.helpers.parse_ine_period("2023-MAR")
        self.assertEqual(year, 2023)
        self.assertEqual(quarter, "Q1")
        
        year, quarter = self.helpers.parse_ine_period("2023-JUN")
        self.assertEqual(year, 2023)
        self.assertEqual(quarter, "Q2")
        
        # Test caso inválido
        with self.assertRaises(ValueError):
            self.helpers.parse_ine_period("invalid-format")
    
    def test_detect_outliers(self):
        """Test de detección de outliers."""
        # Serie con outlier obvio
        series_with_outlier = pd.Series([10, 12, 11, 13, 12, 100, 11, 10])
        outliers = self.helpers.detect_outliers(series_with_outlier, method="iqr")
        
        # Debería detectar al menos un outlier
        self.assertTrue(outliers.any())
        
        # El valor 100 debería ser outlier
        self.assertTrue(outliers[series_with_outlier == 100].iloc[0])
    
    def test_calculate_growth_rates(self):
        """Test de cálculo de tasas de crecimiento."""
        # Serie creciente
        growing_series = pd.Series([100, 110, 121, 133])
        growth_rates = self.helpers.calculate_growth_rates(growing_series)
        
        # Verificar estructura
        self.assertIn('total_growth_pct', growth_rates)
        self.assertIn('annual_growth_pct', growth_rates)
        self.assertIn('avg_period_growth_pct', growth_rates)
        
        # Verificar que detecta crecimiento
        self.assertGreater(growth_rates['total_growth_pct'], 0)
    
    def test_format_large_numbers(self):
        """Test de formateo de números grandes."""
        # Test diferentes escalas
        self.assertEqual(self.helpers.format_large_numbers(1500), "1.5K")
        self.assertEqual(self.helpers.format_large_numbers(1500000), "1.5M")
        self.assertEqual(self.helpers.format_large_numbers(1500000000), "1.5B")
        self.assertEqual(self.helpers.format_large_numbers(150), "150.0")
    
    def test_safe_divide(self):
        """Test de división segura."""
        # División normal
        self.assertEqual(self.helpers.safe_divide(10, 2), 5.0)
        
        # División por cero
        self.assertEqual(self.helpers.safe_divide(10, 0), 0.0)
        self.assertEqual(self.helpers.safe_divide(10, 0, default=999), 999)
        
        # Valores NaN
        self.assertEqual(self.helpers.safe_divide(np.nan, 2), 0.0)
        self.assertEqual(self.helpers.safe_divide(10, np.nan), 0.0)


if __name__ == '__main__':
    # Ejecutar todos los tests
    unittest.main(verbosity=2)
