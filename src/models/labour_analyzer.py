"""
Analizador del mercado laboral para Los Ríos
Clean Code: Single Responsibility - análisis específico del mercado laboral
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

from ...config import LosRiosConfig, AnalysisConfig
from ..utils.logger import setup_logger, PerformanceLogger
from ..utils.validators import DataValidator
from ..utils.helpers import HelperFunctions


class LabourAnalyzer:
    """
    Analizador especializado del mercado laboral de Los Ríos.
    
    Clean Code Principles:
    - Single Responsibility: Solo análisis del mercado laboral
    - Dependency Injection: Recibe configuraciones y utilidades
    - Pure Functions: Métodos de análisis sin efectos secundarios
    """
    
    def __init__(self, config: Optional[LosRiosConfig] = None):
        """
        Inicializa el analizador del mercado laboral.
        
        Args:
            config: Configuración específica de Los Ríos
        """
        self.config = config or LosRiosConfig()
        self.analysis_config = AnalysisConfig()
        self.logger = setup_logger(
            name=self.__class__.__name__,
            log_file=self.config.LOG_FILES["analysis"]
        )
        self.validator = DataValidator()
        self.helpers = HelperFunctions()
        
        self.logger.info("LabourAnalyzer inicializado para Los Ríos")
    
    def analyze_labour_market(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Realiza análisis completo del mercado laboral.
        
        Args:
            data: DataFrame con datos de fuerza de trabajo
            
        Returns:
            Diccionario con resultados del análisis
        """
        perf_logger = PerformanceLogger("labour_market_analysis")
        perf_logger.start()
        
        try:
            # Validar datos de entrada
            is_valid, errors = self.validator.validate_los_rios_data(data)
            if not is_valid:
                raise ValueError(f"Datos inválidos: {errors}")
            
            # Filtrar datos de Los Ríos
            los_rios_data = self._filter_los_rios_data(data)
            
            perf_logger.checkpoint("data_preparation")
            
            # Análisis principales
            results = {
                "metadata": self._create_analysis_metadata(los_rios_data),
                "current_indicators": self._calculate_current_indicators(los_rios_data),
                "historical_trends": self._analyze_historical_trends(los_rios_data),
                "gender_analysis": self._analyze_gender_differences(los_rios_data),
                "seasonal_patterns": self._analyze_seasonal_patterns(los_rios_data),
                "growth_analysis": self._analyze_growth_patterns(los_rios_data),
                "comparisons": self._create_comparative_analysis(los_rios_data),
                "forecasts": self._create_basic_forecasts(los_rios_data)
            }
            
            perf_logger.checkpoint("analysis_complete")
            
            # Generar resumen ejecutivo
            results["executive_summary"] = self._create_executive_summary(results)
            
            elapsed_time = perf_logger.end(f"Analizados {len(los_rios_data)} registros")
            results["metadata"]["analysis_time_seconds"] = elapsed_time
            
            self.logger.info("Análisis del mercado laboral completado exitosamente")
            return results
            
        except Exception as e:
            self.logger.error(f"Error en análisis del mercado laboral: {str(e)}")
            raise
    
    def _filter_los_rios_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Filtra y prepara datos específicos de Los Ríos."""
        if 'region' in data.columns:
            los_rios_data = data[data['region'] == self.config.REGION_CODE].copy()
        else:
            los_rios_data = data.copy()
        
        # Ordenar por período
        if 'ano_trimestre' in los_rios_data.columns:
            los_rios_data = los_rios_data.sort_values('ano_trimestre')
        
        self.logger.info(f"Datos filtrados: {len(los_rios_data)} registros de Los Ríos")
        return los_rios_data
    
    def _create_analysis_metadata(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Crea metadatos del análisis."""
        return {
            "analysis_date": datetime.now().isoformat(),
            "region": self.config.REGION_NAME,
            "region_code": self.config.REGION_CODE,
            "total_records": len(data),
            "period_range": {
                "start": data['ano_trimestre'].min() if 'ano_trimestre' in data.columns else "N/A",
                "end": data['ano_trimestre'].max() if 'ano_trimestre' in data.columns else "N/A"
            },
            "data_quality": self.validator.generate_validation_report(data)
        }
    
    def _calculate_current_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calcula indicadores actuales del mercado laboral."""
        try:
            if data.empty:
                return {"error": "No hay datos disponibles"}
            
            # Obtener último período
            latest_data = data.iloc[-1] if len(data) > 0 else None
            
            if latest_data is None:
                return {"error": "No se pudo obtener datos del último período"}
            
            indicators = {
                "latest_period": latest_data.get('ano_trimestre', 'N/A'),
                "total_labour_force": latest_data.get('fuerza_de_trabajo', 0),
                "male_labour_force": latest_data.get('hombres', 0),
                "female_labour_force": latest_data.get('mujeres', 0)
            }
            
            # Calcular participación por género
            total = indicators["total_labour_force"]
            if total > 0:
                indicators["male_participation_pct"] = round(
                    (indicators["male_labour_force"] / total) * 100, 2
                )
                indicators["female_participation_pct"] = round(
                    (indicators["female_labour_force"] / total) * 100, 2
                )
            else:
                indicators["male_participation_pct"] = 0
                indicators["female_participation_pct"] = 0
            
            # Formatear números grandes
            for key in ["total_labour_force", "male_labour_force", "female_labour_force"]:
                indicators[f"{key}_formatted"] = self.helpers.format_large_numbers(
                    indicators[key]
                )
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error calculando indicadores actuales: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_historical_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza tendencias históricas."""
        try:
            if len(data) < 2:
                return {"error": "Insuficientes datos para análisis de tendencias"}
            
            trends = {}
            
            # Analizar fuerza de trabajo total
            if 'fuerza_de_trabajo' in data.columns:
                total_ft = data['fuerza_de_trabajo']
                trends["total_labour_force"] = {
                    "growth_rates": self.helpers.calculate_growth_rates(total_ft),
                    "trend_direction": self._determine_trend_direction(total_ft),
                    "volatility": self._calculate_volatility(total_ft),
                    "outliers": self.helpers.detect_outliers(total_ft).sum()
                }
            
            # Analizar por género
            for gender, column in [("male", "hombres"), ("female", "mujeres")]:
                if column in data.columns:
                    gender_data = data[column]
                    trends[f"{gender}_labour_force"] = {
                        "growth_rates": self.helpers.calculate_growth_rates(gender_data),
                        "trend_direction": self._determine_trend_direction(gender_data),
                        "volatility": self._calculate_volatility(gender_data)
                    }
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Error en análisis de tendencias: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_gender_differences(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza diferencias de género en el mercado laboral."""
        try:
            if not all(col in data.columns for col in ['hombres', 'mujeres']):
                return {"error": "Datos de género no disponibles"}
            
            male_data = data['hombres']
            female_data = data['mujeres']
            
            analysis = {
                "average_participation": {
                    "male": round(male_data.mean(), 0),
                    "female": round(female_data.mean(), 0)
                },
                "participation_ratio": round(
                    self.helpers.safe_divide(male_data.mean(), female_data.mean(), 1.0), 2
                ),
                "growth_comparison": {
                    "male": self.helpers.calculate_growth_rates(male_data),
                    "female": self.helpers.calculate_growth_rates(female_data)
                },
                "volatility_comparison": {
                    "male": self._calculate_volatility(male_data),
                    "female": self._calculate_volatility(female_data)
                }
            }
            
            # Determinar qué género tiene mayor crecimiento
            male_growth = analysis["growth_comparison"]["male"].get("total_growth_pct", 0)
            female_growth = analysis["growth_comparison"]["female"].get("total_growth_pct", 0)
            
            analysis["growth_leader"] = "male" if male_growth > female_growth else "female"
            analysis["growth_gap"] = abs(male_growth - female_growth)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error en análisis de género: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_seasonal_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza patrones estacionales."""
        try:
            if 'ano_trimestre' not in data.columns or len(data) < 8:
                return {"error": "Insuficientes datos para análisis estacional"}
            
            # Extraer trimestres
            data_with_quarters = data.copy()
            data_with_quarters['quarter'] = data_with_quarters['ano_trimestre'].apply(
                lambda x: self.helpers.parse_ine_period(x)[1] if isinstance(x, str) else 'Q1'
            )
            
            seasonal_analysis = {}
            
            # Análisis por trimestre
            if 'fuerza_de_trabajo' in data.columns:
                quarterly_stats = data_with_quarters.groupby('quarter')['fuerza_de_trabajo'].agg([
                    'mean', 'std', 'count'
                ]).round(0)
                
                seasonal_analysis["quarterly_patterns"] = quarterly_stats.to_dict()
                
                # Identificar trimestre con mayor/menor actividad
                seasonal_analysis["peak_quarter"] = quarterly_stats['mean'].idxmax()
                seasonal_analysis["low_quarter"] = quarterly_stats['mean'].idxmin()
                seasonal_analysis["seasonal_variation_pct"] = round(
                    ((quarterly_stats['mean'].max() - quarterly_stats['mean'].min()) / 
                     quarterly_stats['mean'].mean()) * 100, 2
                )
            
            return seasonal_analysis
            
        except Exception as e:
            self.logger.error(f"Error en análisis estacional: {str(e)}")
            return {"error": str(e)}
    
    def _analyze_growth_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analiza patrones de crecimiento detallados."""
        try:
            if 'fuerza_de_trabajo' not in data.columns or len(data) < 3:
                return {"error": "Insuficientes datos para análisis de crecimiento"}
            
            # Calcular diferencias período a período
            growth_data = self.helpers.calculate_period_differences(
                data, 'fuerza_de_trabajo'
            )
            
            patterns = {
                "period_to_period": {
                    "average_change": round(growth_data['fuerza_de_trabajo_diff'].mean(), 0),
                    "average_pct_change": round(growth_data['fuerza_de_trabajo_pct_change'].mean(), 2),
                    "max_increase": round(growth_data['fuerza_de_trabajo_diff'].max(), 0),
                    "max_decrease": round(growth_data['fuerza_de_trabajo_diff'].min(), 0),
                    "positive_periods": (growth_data['fuerza_de_trabajo_diff'] > 0).sum(),
                    "negative_periods": (growth_data['fuerza_de_trabajo_diff'] < 0).sum()
                }
            }
            
            # Análisis año sobre año si hay datos suficientes
            if 'fuerza_de_trabajo_yoy_change' in growth_data.columns:
                yoy_data = growth_data['fuerza_de_trabajo_yoy_change'].dropna()
                if len(yoy_data) > 0:
                    patterns["year_over_year"] = {
                        "average_yoy_change": round(yoy_data.mean(), 2),
                        "max_yoy_increase": round(yoy_data.max(), 2),
                        "max_yoy_decrease": round(yoy_data.min(), 2),
                        "positive_years": (yoy_data > 0).sum(),
                        "negative_years": (yoy_data < 0).sum()
                    }
            
            return patterns
            
        except Exception as e:
            self.logger.error(f"Error en análisis de crecimiento: {str(e)}")
            return {"error": str(e)}
    
    def _create_comparative_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Crea análisis comparativo."""
        try:
            # Comparar primeros vs últimos años
            if len(data) < 8:  # Al menos 2 años de datos trimestrales
                return {"error": "Insuficientes datos para comparación temporal"}
            
            # Dividir en períodos inicial y final
            split_point = len(data) // 2
            early_period = data.iloc[:split_point]
            recent_period = data.iloc[split_point:]
            
            comparison = {}
            
            if 'fuerza_de_trabajo' in data.columns:
                early_avg = early_period['fuerza_de_trabajo'].mean()
                recent_avg = recent_period['fuerza_de_trabajo'].mean()
                
                comparison["period_comparison"] = {
                    "early_period_avg": round(early_avg, 0),
                    "recent_period_avg": round(recent_avg, 0),
                    "improvement_pct": round(((recent_avg - early_avg) / early_avg) * 100, 2),
                    "periods_analyzed": {
                        "early": f"{early_period['ano_trimestre'].min()} - {early_period['ano_trimestre'].max()}",
                        "recent": f"{recent_period['ano_trimestre'].min()} - {recent_period['ano_trimestre'].max()}"
                    }
                }
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error en análisis comparativo: {str(e)}")
            return {"error": str(e)}
    
    def _create_basic_forecasts(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Crea proyecciones básicas."""
        try:
            if 'fuerza_de_trabajo' not in data.columns or len(data) < 4:
                return {"error": "Insuficientes datos para proyecciones"}
            
            # Calcular tendencia simple usando últimos períodos
            recent_data = data.tail(4)  # Últimos 4 trimestres
            recent_values = recent_data['fuerza_de_trabajo'].values
            
            # Tendencia lineal simple
            x = np.arange(len(recent_values))
            coeffs = np.polyfit(x, recent_values, 1)
            trend_slope = coeffs[0]
            
            # Proyección para próximos 2 trimestres
            last_value = recent_values[-1]
            forecast_1q = last_value + trend_slope
            forecast_2q = last_value + (2 * trend_slope)
            
            forecasts = {
                "methodology": "Linear trend based on last 4 quarters",
                "current_trend": "increasing" if trend_slope > 0 else "decreasing",
                "trend_magnitude": round(abs(trend_slope), 0),
                "projections": {
                    "next_quarter": round(forecast_1q, 0),
                    "quarter_after": round(forecast_2q, 0)
                },
                "confidence": "low" if abs(trend_slope) < 1000 else "medium"
            }
            
            return forecasts
            
        except Exception as e:
            self.logger.error(f"Error en proyecciones: {str(e)}")
            return {"error": str(e)}
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Crea resumen ejecutivo del análisis."""
        try:
            summary = {
                "region": self.config.REGION_NAME,
                "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                "key_findings": [],
                "recommendations": [],
                "data_period": results.get("metadata", {}).get("period_range", {})
            }
            
            # Extraer hallazgos clave
            current = results.get("current_indicators", {})
            trends = results.get("historical_trends", {})
            gender = results.get("gender_analysis", {})
            
            # Tamaño actual de la fuerza laboral
            total_labour = current.get("total_labour_force", 0)
            if total_labour > 0:
                summary["key_findings"].append(
                    f"La fuerza de trabajo actual en Los Ríos es de {self.helpers.format_large_numbers(total_labour)} personas"
                )
            
            # Tendencia general
            total_trend = trends.get("total_labour_force", {})
            if total_trend:
                growth_rates = total_trend.get("growth_rates", {})
                total_growth = growth_rates.get("total_growth_pct", 0)
                
                if total_growth > 0:
                    summary["key_findings"].append(
                        f"La fuerza laboral ha crecido {total_growth}% en el período analizado"
                    )
                else:
                    summary["key_findings"].append(
                        f"La fuerza laboral ha decrecido {abs(total_growth)}% en el período analizado"
                    )
            
            # Análisis de género
            if gender and not gender.get("error"):
                male_pct = current.get("male_participation_pct", 0)
                female_pct = current.get("female_participation_pct", 0)
                
                if male_pct > female_pct:
                    summary["key_findings"].append(
                        f"La participación masculina ({male_pct}%) supera a la femenina ({female_pct}%)"
                    )
                else:
                    summary["key_findings"].append(
                        f"La participación femenina ({female_pct}%) supera a la masculina ({male_pct}%)"
                    )
            
            # Recomendaciones básicas
            summary["recommendations"] = [
                "Continuar monitoreando las tendencias trimestrales",
                "Profundizar en factores que influyen en la participación laboral",
                "Analizar sectores económicos específicos de la región",
                "Desarrollar políticas para equilibrar la participación de género"
            ]
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error creando resumen ejecutivo: {str(e)}")
            return {"error": str(e)}
    
    def _determine_trend_direction(self, series: pd.Series) -> str:
        """Determina la dirección general de una tendencia."""
        if len(series) < 2:
            return "insufficient_data"
        
        # Calcular pendiente de tendencia lineal
        x = np.arange(len(series))
        coeffs = np.polyfit(x, series.values, 1)
        slope = coeffs[0]
        
        if abs(slope) < series.mean() * 0.01:  # Cambio menor al 1% promedio
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def _calculate_volatility(self, series: pd.Series) -> Dict[str, float]:
        """Calcula métricas de volatilidad."""
        try:
            pct_changes = series.pct_change().dropna()
            
            return {
                "coefficient_of_variation": round((series.std() / series.mean()) * 100, 2),
                "average_absolute_change": round(pct_changes.abs().mean() * 100, 2),
                "max_change": round(pct_changes.abs().max() * 100, 2)
            }
        except Exception:
            return {"error": "No se pudo calcular volatilidad"}
