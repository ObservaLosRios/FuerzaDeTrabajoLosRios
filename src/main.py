"""
Main entry point for the INE Chile Labour Force Analysis project.
"""

import sys
from pathlib import Path
import logging

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from config import config
from utils.logger_config import configure_logging, get_logger
from etl.data_processor import LabourForceProcessor
from visualization.charts import LabourForceCharts


def main():
    """Main function to run the complete analysis pipeline."""
    
    # Configure logging
    configure_logging(
        log_file=config.paths.LOGS_DIR / "analysis.log",
        level=config.logging.LOG_LEVEL
    )
    
    logger = get_logger(__name__)
    logger.info("Starting INE Chile Labour Force Analysis")
    
    try:
        # Initialize processor
        processor = LabourForceProcessor()
        
        # Process data
        raw_data_files = list(config.paths.RAW_DATA_DIR.glob("*.csv"))
        
        if not raw_data_files:
            logger.error("No CSV files found in raw data directory")
            return
        
        # Process first file found
        input_file = raw_data_files[0]
        output_file = config.paths.PROCESSED_DATA_DIR / "labour_force_processed.csv"
        
        logger.info(f"Processing file: {input_file}")
        processed_data = processor.process_file(input_file, output_file)
        
        # Generate visualizations
        charts = LabourForceCharts()
        
        # Time series plot
        time_series_fig = charts.plot_time_series(
            processed_data,
            save_path=config.paths.OUTPUT_DATA_DIR / "time_series.png"
        )
        
        # Interactive dashboard
        dashboard_fig = charts.create_interactive_dashboard(
            processed_data,
            save_path=config.paths.OUTPUT_DATA_DIR / "dashboard.html"
        )
        
        # Generate summary statistics
        stats = processor.get_summary_statistics(processed_data)
        
        # Save summary
        summary_file = config.paths.OUTPUT_DATA_DIR / "summary_report.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("INE CHILE LABOUR FORCE ANALYSIS - SUMMARY REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            for key, value in stats.items():
                f.write(f"{key}: {value}\n")
        
        logger.info("Analysis completed successfully")
        logger.info(f"Results saved to: {config.paths.OUTPUT_DATA_DIR}")
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
