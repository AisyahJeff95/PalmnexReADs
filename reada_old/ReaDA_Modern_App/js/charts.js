/**
 * ReaDA Custom SVG Charting Engine
 * Renders high-performance, responsive SVG yield trends and leaf nutrient radar charts.
 */

export class ChartEngine {
  static renderYieldTrend(containerId, yieldData) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!yieldData || yieldData.length === 0) {
      container.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-muted);">No FFB Yield Data Available</div>';
      return;
    }

    const width = container.clientWidth || 600;
    const height = 300;
    const padding = { top: 30, right: 30, bottom: 40, left: 50 };

    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    const maxY = Math.max(...yieldData.map(d => d.FFB_YIELD || 0), 35);
    const minY = 0;

    // X points
    const stepX = chartWidth / (yieldData.length > 1 ? yieldData.length - 1 : 1);

    let points = yieldData.map((d, i) => {
      const x = padding.left + (yieldData.length === 1 ? chartWidth / 2 : i * stepX);
      const y = padding.top + chartHeight - ((d.FFB_YIELD || 0) / maxY) * chartHeight;
      return { x, y, val: d.FFB_YIELD, label: d.TRIAL_CODE || `P-${d.PALM_NO}` };
    });

    const pathD = points.reduce((acc, p, i) => `${acc} ${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`, '');
    const areaD = `${pathD} L ${points[points.length - 1].x} ${padding.top + chartHeight} L ${points[0].x} ${padding.top + chartHeight} Z`;

    let gridLines = '';
    for (let i = 0; i <= 4; i++) {
      const val = Math.round((maxY / 4) * i);
      const y = padding.top + chartHeight - (i / 4) * chartHeight;
      gridLines += `
        <line x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}" class="chart-grid-line" />
        <text x="${padding.left - 10}" y="${y + 4}" class="chart-axis-label" text-anchor="end">${val}</text>
      `;
    }

    let xLabels = points.map(p => `
      <text x="${p.x}" y="${height - 10}" class="chart-axis-label" text-anchor="middle">${p.label}</text>
    `).join('');

    let circles = points.map(p => `
      <circle cx="${p.x}" cy="${p.y}" r="5" class="chart-point" data-val="${p.val}" data-label="${p.label}" />
    `).join('');

    container.innerHTML = `
      <svg class="chart-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none">
        <defs>
          <linearGradient id="chart-gradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#10b981" stop-opacity="0.0"/>
          </linearGradient>
        </defs>
        ${gridLines}
        <path d="${areaD}" class="chart-area" />
        <path d="${pathD}" class="chart-line" />
        ${circles}
        ${xLabels}
      </svg>
    `;
  }

  static renderNutrientRadar(containerId, leafRecord) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const nutrients = [
      { name: 'N', val: leafRecord?.TISSUE_N || 2.65, opt: 2.65, scale: 3.5 },
      { name: 'P', val: leafRecord?.TISSUE_P || 0.16, opt: 0.165, scale: 0.25 },
      { name: 'K', val: leafRecord?.TISSUE_K || 1.18, opt: 1.12, scale: 1.6 },
      { name: 'Ca', val: leafRecord?.TISSUE_CA || 0.58, opt: 0.60, scale: 0.9 },
      { name: 'Mg', val: leafRecord?.TISSUE_MG || 0.32, opt: 0.32, scale: 0.5 },
      { name: 'B', val: (leafRecord?.TISSUE_B || 18.5) / 100, opt: 0.20, scale: 0.35 }
    ];

    const width = 280;
    const height = 280;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = 90;
    const totalAxes = nutrients.length;

    let axisLines = '';
    let webCircles = '';
    let labels = '';

    // Web circles (3 rings)
    [0.33, 0.66, 1.0].forEach(rFactor => {
      let r = radius * rFactor;
      let webPoints = nutrients.map((_, i) => {
        let angle = (Math.PI * 2 / totalAxes) * i - Math.PI / 2;
        return `${centerX + r * Math.cos(angle)},${centerY + r * Math.sin(angle)}`;
      }).join(' ');
      webCircles += `<polygon points="${webPoints}" class="radar-web" />`;
    });

    let currentPoints = [];
    let optimumPoints = [];

    nutrients.forEach((n, i) => {
      let angle = (Math.PI * 2 / totalAxes) * i - Math.PI / 2;
      let endX = centerX + radius * Math.cos(angle);
      let endY = centerY + radius * Math.sin(angle);

      axisLines += `<line x1="${centerX}" y1="${centerY}" x2="${endX}" y2="${endY}" class="radar-axis" />`;

      // Labels
      let labelX = centerX + (radius + 20) * Math.cos(angle);
      let labelY = centerY + (radius + 15) * Math.sin(angle);
      labels += `<text x="${labelX}" y="${labelY}" class="radar-label">${n.name}</text>`;

      // Values ratio
      let curR = radius * Math.min(1.0, n.val / n.scale);
      let optR = radius * Math.min(1.0, n.opt / n.scale);

      currentPoints.push(`${centerX + curR * Math.cos(angle)},${centerY + curR * Math.sin(angle)}`);
      optimumPoints.push(`${centerX + optR * Math.cos(angle)},${centerY + optR * Math.sin(angle)}`);
    });

    container.innerHTML = `
      <svg class="radar-svg" viewBox="0 0 ${width} ${height}">
        ${webCircles}
        ${axisLines}
        <polygon points="${optimumPoints.join(' ')}" class="radar-optimum-polygon" />
        <polygon points="${currentPoints.join(' ')}" class="radar-polygon" />
        ${labels}
      </svg>
    `;
  }
}
