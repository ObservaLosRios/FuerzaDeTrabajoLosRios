import { DataService } from './services/dataService.js';
import { ChartRenderer } from './components/chartRenderer.js';

class Dashboard {
  constructor() {
    this.chartRenderer = new ChartRenderer('chart-container');
  }

  async init() {
    try {
      const data = DataService.getLosRiosData();
      
      if (!data.validate()) {
        throw new Error('Invalid data structure');
      }
      
      await this.chartRenderer.render(data);
    } catch (error) {
      console.error('Dashboard initialization failed:', error);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const dashboard = new Dashboard();
  dashboard.init();
});
