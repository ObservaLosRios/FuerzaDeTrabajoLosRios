"""
Analizador demográfico para Los Ríos
Clean Code: Responsabilidad específica para análisis demográfico
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ...config import LosRiosConfig
from ..utils.logger import setup_logger
from ..utils.helpers import HelperFunctions


class DemographicsAnalyzer:
    """
    Analizador especializado en aspectos demográficos de la fuerza laboral.
    
    Clean Code: Single Responsibility para análisis demográfico
    """
    
    def __init__(self, config: Optional[LosRiosConfig] = None):
        """Inicializa el analizador demográfico."""
        self.config = config or LosRiosConfig()
        self.logger = setup_logger(self.__class__.__name__)
        self.helpers = HelperFunctions()
    
    def analyze_demographic_structure(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analiza la estructura demográfica de la fuerza laboral.
        
        Args:
            data: DataFrame con datos demográficos
            
        Returns:
            Análisis demográfico completo
        """
        try:
            analysis = {
                "gender_distribution": self._analyze_gender_distribution(data),
                "temporal_evolution": self._analyze_temporal_evolution(data),
                "participation_rates": self._calculate_participation_rates(data),
                "demographic_trends": self._analyze_demographic_trends(data)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error en análisis demográfico: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_gender_distribution(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza distribución por género."""
        if not all(col in data.columns for col in ['hombres', 'mujeres', 'fuerza_de_trabajo']):
            return {"error": "Columnas de género no encontradas"}
        
        total_male = data['hombres'].sum()
        total_female = data['mujeres'].sum()
        total_labour = data['fuerza_de_trabajo'].sum()
        
        return {
            "total_male": int(total_male),
            "total_female": int(total_female),
            "male_percentage": round((total_male / total_labour) * 100, 2),
            "female_percentage": round((total_female / total_labour) * 100, 2),
            "gender_ratio": round(total_male / total_female, 2),
            "male_formatted": self.helpers.format_large_numbers(total_male),
            "female_formatted": self.helpers.format_large_numbers(total_female)
        }
    
    def _analyze_temporal_evolution(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza evolución temporal por género."""
        if 'ano_trimestre' not in data.columns:
            return {"error": "Columna de período no encontrada"}
        
        # Evolución masculina
        male_evolution = self.helpers.calculate_growth_rates(data['hombres'])
        female_evolution = self.helpers.calculate_growth_rates(data['mujeres'])
        
        return {
            "male_evolution": male_evolution,
            "female_evolution": female_evolution,
            "convergence_trend": self._analyze_gender_convergence(data)
        }
    
    def _calculate_participation_rates(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calcula tasas de participación."""
        latest_data = data.iloc[-1]
        
        male_rate = (latest_data['hombres'] / latest_data['fuerza_de_trabajo']) * 100
        female_rate = (latest_data['mujeres'] / latest_data['fuerza_de_trabajo']) * 100
        
        return {
            "current_male_rate": round(male_rate, 2),
            "current_female_rate": round(female_rate, 2),
            "historical_average_male": round(data['hombres'].mean() / data['fuerza_de_trabajo'].mean() * 100, 2),
            "historical_average_female": round(data['mujeres'].mean() / data['fuerza_de_trabajo'].mean() * 100, 2)
        }
    
    def _analyze_demographic_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza tendencias demográficas."""
        # Implementación simplificada
        return {
            "overall_trend": "stable",
            "male_trend": "increasing" if data['hombres'].iloc[-1] > data['hombres'].iloc[0] else "decreasing",
            "female_trend": "increasing" if data['mujeres'].iloc[-1] > data['mujeres'].iloc[0] else "decreasing"
        }
    
    def _analyze_gender_convergence(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza convergencia entre géneros."""
        # Calcular brecha de género a lo largo del tiempo
        data_copy = data.copy()
        data_copy['gender_gap'] = abs(data_copy['hombres'] - data_copy['mujeres'])
        data_copy['gender_gap_pct'] = (data_copy['gender_gap'] / data_copy['fuerza_de_trabajo']) * 100
        
        initial_gap = data_copy['gender_gap_pct'].iloc[0]
        final_gap = data_copy['gender_gap_pct'].iloc[-1]
        
        return {
            "initial_gap_pct": round(initial_gap, 2),
            "final_gap_pct": round(final_gap, 2),
            "gap_change": round(final_gap - initial_gap, 2),
            "convergence_trend": "converging" if final_gap < initial_gap else "diverging"
        }
