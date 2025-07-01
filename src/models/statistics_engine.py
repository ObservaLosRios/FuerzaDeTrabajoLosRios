"""
Motor estadístico para análisis avanzados de Los Ríos
Clean Code: Engine pattern para cálculos estadísticos complejos
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
import logging

from ...config import LosRiosConfig
from ..utils.logger import setup_logger


class StatisticsEngine:
    """
    Motor estadístico para análisis avanzados.
    
    Clean Code: Engine pattern - centraliza lógica estadística compleja
    """
    
    def __init__(self):
        """Inicializa el motor estadístico."""
        self.logger = setup_logger(self.__class__.__name__)
    
    def calculate_descriptive_statistics(self, data: pd.Series) -> Dict[str, float]:
        """Calcula estadísticas descriptivas completas."""
        try:
            clean_data = data.dropna()
            
            return {
                "count": len(clean_data),
                "mean": round(clean_data.mean(), 2),
                "median": round(clean_data.median(), 2),
                "mode": round(clean_data.mode().iloc[0] if len(clean_data.mode()) > 0 else clean_data.mean(), 2),
                "std_dev": round(clean_data.std(), 2),
                "variance": round(clean_data.var(), 2),
                "skewness": round(stats.skew(clean_data), 2),
                "kurtosis": round(stats.kurtosis(clean_data), 2),
                "min": round(clean_data.min(), 2),
                "max": round(clean_data.max(), 2),
                "range": round(clean_data.max() - clean_data.min(), 2),
                "q1": round(clean_data.quantile(0.25), 2),
                "q3": round(clean_data.quantile(0.75), 2),
                "iqr": round(clean_data.quantile(0.75) - clean_data.quantile(0.25), 2)
            }
        except Exception as e:
            self.logger.error(f"Error calculando estadísticas descriptivas: {str(e)}")
            return {}
    
    def perform_trend_analysis(self, data: pd.Series) -> Dict[str, Any]:
        """Realiza análisis de tendencias estadístico."""
        try:
            clean_data = data.dropna()
            x = np.arange(len(clean_data))
            
            # Regresión lineal
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, clean_data)
            
            # Test de Mann-Kendall para tendencias
            n = len(clean_data)
            s_statistic = 0
            
            for i in range(n-1):
                for j in range(i+1, n):
                    s_statistic += np.sign(clean_data.iloc[j] - clean_data.iloc[i])
            
            # Varianza de S
            var_s = n * (n - 1) * (2 * n + 5) / 18
            
            # Z-score para Mann-Kendall
            if s_statistic > 0:
                z_mk = (s_statistic - 1) / np.sqrt(var_s)
            elif s_statistic < 0:
                z_mk = (s_statistic + 1) / np.sqrt(var_s)
            else:
                z_mk = 0
            
            # P-value para Mann-Kendall
            p_mk = 2 * (1 - stats.norm.cdf(abs(z_mk)))
            
            return {
                "linear_regression": {
                    "slope": round(slope, 4),
                    "intercept": round(intercept, 2),
                    "r_squared": round(r_value**2, 4),
                    "p_value": round(p_value, 4),
                    "significant": p_value < 0.05
                },
                "mann_kendall": {
                    "s_statistic": s_statistic,
                    "z_score": round(z_mk, 4),
                    "p_value": round(p_mk, 4),
                    "trend": "increasing" if z_mk > 0 else "decreasing" if z_mk < 0 else "no_trend",
                    "significant": p_mk < 0.05
                }
            }
        except Exception as e:
            self.logger.error(f"Error en análisis de tendencias: {str(e)}")
            return {}
    
    def detect_change_points(self, data: pd.Series, min_size: int = 5) -> List[int]:
        """Detecta puntos de cambio en series temporales."""
        try:
            clean_data = data.dropna()
            change_points = []
            
            # Implementación simple basada en diferencias de media
            n = len(clean_data)
            
            for i in range(min_size, n - min_size):
                before = clean_data.iloc[:i]
                after = clean_data.iloc[i:]
                
                # Test t para diferencia de medias
                t_stat, p_value = stats.ttest_ind(before, after)
                
                if p_value < 0.01:  # Punto de cambio significativo
                    change_points.append(i)
            
            return change_points
            
        except Exception as e:
            self.logger.error(f"Error detectando puntos de cambio: {str(e)}")
            return []
    
    def calculate_correlation_matrix(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calcula matriz de correlaciones."""
        try:
            numeric_data = data.select_dtypes(include=[np.number])
            
            # Correlación de Pearson
            pearson_corr = numeric_data.corr()
            
            # Correlación de Spearman
            spearman_corr = numeric_data.corr(method='spearman')
            
            return {
                "pearson": pearson_corr.to_dict(),
                "spearman": spearman_corr.to_dict(),
                "strongest_correlations": self._find_strongest_correlations(pearson_corr)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculando correlaciones: {str(e)}")
            return {}
    
    def perform_normality_tests(self, data: pd.Series) -> Dict[str, Any]:
        """Realiza tests de normalidad."""
        try:
            clean_data = data.dropna()
            
            # Shapiro-Wilk test
            sw_stat, sw_p = stats.shapiro(clean_data)
            
            # Kolmogorov-Smirnov test
            ks_stat, ks_p = stats.kstest(clean_data, 'norm', args=(clean_data.mean(), clean_data.std()))
            
            # Anderson-Darling test
            ad_stat, ad_critical, ad_significance = stats.anderson(clean_data, dist='norm')
            
            return {
                "shapiro_wilk": {
                    "statistic": round(sw_stat, 4),
                    "p_value": round(sw_p, 4),
                    "is_normal": sw_p > 0.05
                },
                "kolmogorov_smirnov": {
                    "statistic": round(ks_stat, 4),
                    "p_value": round(ks_p, 4),
                    "is_normal": ks_p > 0.05
                },
                "anderson_darling": {
                    "statistic": round(ad_stat, 4),
                    "critical_values": ad_critical.tolist(),
                    "significance_levels": ad_significance.tolist()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en tests de normalidad: {str(e)}")
            return {}
    
    def _find_strongest_correlations(self, corr_matrix: pd.DataFrame) -> List[Dict[str, Any]]:
        """Encuentra las correlaciones más fuertes."""
        correlations = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                var1 = corr_matrix.columns[i]
                var2 = corr_matrix.columns[j]
                correlation = corr_matrix.iloc[i, j]
                
                if not np.isnan(correlation):
                    correlations.append({
                        "variable_1": var1,
                        "variable_2": var2,
                        "correlation": round(correlation, 4),
                        "strength": self._classify_correlation_strength(abs(correlation))
                    })
        
        # Ordenar por correlación absoluta
        correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)
        
        return correlations[:10]  # Top 10
    
    def _classify_correlation_strength(self, abs_correlation: float) -> str:
        """Clasifica la fuerza de una correlación."""
        if abs_correlation >= 0.8:
            return "very_strong"
        elif abs_correlation >= 0.6:
            return "strong"
        elif abs_correlation >= 0.4:
            return "moderate"
        elif abs_correlation >= 0.2:
            return "weak"
        else:
            return "very_weak"
