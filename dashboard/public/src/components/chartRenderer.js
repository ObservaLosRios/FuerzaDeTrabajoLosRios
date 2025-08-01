import { TraceBuilder, LayoutBuilder } from './chartBuilder.js';
import { ChartConfig } from '../config/chartConfig.js';

export class ChartRenderer {
  constructor(containerId) {
    this.containerId = containerId;
    this.config = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
    };
  }

  render(data) {
    const traces = this._buildTraces(data);
    const layout = LayoutBuilder.create();
    
    return Plotly.newPlot(this.containerId, traces, layout, this.config);
  }

  _buildTraces(data) {
    return [
      TraceBuilder.createTrace(data, 'total', 'Ambos sexos', ChartConfig.colors.total),
      TraceBuilder.createTrace(data, 'male', 'Hombres', ChartConfig.colors.male),
      TraceBuilder.createTrace(data, 'female', 'Mujeres', ChartConfig.colors.female)
    ];
  }
}
