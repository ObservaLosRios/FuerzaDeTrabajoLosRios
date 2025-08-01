import { ChartConfig } from '../config/chartConfig.js';
import { Events } from '../core/interfaces.js';

export class TraceBuilder {
  static createTrace(data, seriesKey, name, color) {
    return {
      x: data.years,
      y: data[seriesKey],
      mode: 'lines+markers',
      name,
      line: { color, width: 3 },
      marker: { size: 8, color },
      hovertemplate: `<b>${name}</b><br>Año: %{x}<br>Fuerza de Trabajo: %{y:.1f} miles<extra></extra>`
    };
  }
}

export class LayoutBuilder {
  static create() {
    return {
      title: {
        text: 'Evolución de la Fuerza de Trabajo - Región de Los Ríos (2010-2024)',
        x: 0.02,
        font: {
          size: ChartConfig.fonts.sizes.title,
          family: ChartConfig.fonts.family,
          color: ChartConfig.theme.textColor
        },
        xanchor: 'left'
      },
      xaxis: this._createXAxis(),
      yaxis: this._createYAxis(),
      hovermode: 'x unified',
      width: ChartConfig.dimensions.width,
      height: ChartConfig.dimensions.height,
      showlegend: true,
      legend: this._createLegend(),
      plot_bgcolor: ChartConfig.theme.background,
      paper_bgcolor: ChartConfig.theme.background,
      font: {
        family: ChartConfig.fonts.family,
        color: ChartConfig.theme.textColor
      },
      shapes: this._createShapes(),
      annotations: this._createAnnotations()
    };
  }

  static _createXAxis() {
    return {
      title: 'Año',
      titlefont: {
        family: ChartConfig.fonts.family,
        color: ChartConfig.theme.textColor,
        size: ChartConfig.fonts.sizes.axis
      },
      tickfont: {
        family: ChartConfig.fonts.family,
        color: ChartConfig.theme.textColor,
        size: ChartConfig.fonts.sizes.tick
      },
      showgrid: false,
      showline: true,
      linecolor: ChartConfig.theme.textColor,
      linewidth: 2,
      tick0: 2010,
      dtick: 2
    };
  }

  static _createYAxis() {
    return {
      title: 'Fuerza de Trabajo (miles de personas)',
      titlefont: {
        family: ChartConfig.fonts.family,
        color: ChartConfig.theme.textColor,
        size: ChartConfig.fonts.sizes.axis
      },
      tickfont: {
        family: ChartConfig.fonts.family,
        color: ChartConfig.theme.textColor,
        size: ChartConfig.fonts.sizes.tick
      },
      showgrid: true,
      gridcolor: ChartConfig.theme.gridColor,
      gridwidth: 1,
      showline: true,
      linecolor: ChartConfig.theme.textColor,
      linewidth: 2
    };
  }

  static _createLegend() {
    return {
      orientation: "h",
      yanchor: "top",
      y: 1.05,
      xanchor: "right",
      x: 0.98,
      bgcolor: "rgba(255,255,255,0.85)",
      bordercolor: "rgba(0,0,0,0)",
      borderwidth: 0,
      font: {
        family: ChartConfig.fonts.family,
        color: ChartConfig.theme.textColor,
        size: ChartConfig.fonts.sizes.legend
      }
    };
  }

  static _createShapes() {
    return [{
      type: 'line',
      x0: Events.COVID_YEAR,
      x1: Events.COVID_YEAR,
      y0: 0,
      y1: 1,
      yref: 'paper',
      line: {
        color: ChartConfig.colors.covid,
        width: 1.5,
        dash: 'dot'
      },
      opacity: 0.7
    }];
  }

  static _createAnnotations() {
    return [{
      x: Events.COVID_YEAR,
      y: 180,
      text: 'COVID-19',
      showarrow: false,
      font: {
        family: ChartConfig.fonts.family,
        size: ChartConfig.fonts.sizes.annotation,
        color: ChartConfig.colors.covid
      },
      bgcolor: 'rgba(255,255,255,0.8)',
      bordercolor: 'rgba(0,0,0,0)',
      xanchor: 'center'
    }];
  }
}
