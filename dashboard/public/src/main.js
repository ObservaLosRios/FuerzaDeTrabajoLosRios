// Test básico para verificar que los módulos funcionan
console.log('Cargando dashboard...');

import { DataService } from './services/dataService.js';
console.log('DataService cargado');

import { ChartRenderer } from './components/chartRenderer.js';
console.log('ChartRenderer cargado');

class Dashboard {
  constructor() {
    console.log('Dashboard constructor');
    this.chartRenderer = new ChartRenderer('chart-container');
  }

  async init() {
    console.log('Iniciando dashboard...');
    try {
      const data = DataService.getLosRiosData();
      console.log('Datos obtenidos:', data);
      
      if (!data.validate()) {
        throw new Error('Invalid data structure');
      }
      console.log('Datos validados correctamente');
      
      await this.chartRenderer.render(data);
      console.log('Gráfico renderizado');
    } catch (error) {
      console.error('Dashboard initialization failed:', error);
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM cargado, inicializando dashboard');
  const dashboard = new Dashboard();
  dashboard.init();
});
