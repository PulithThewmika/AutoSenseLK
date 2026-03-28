import type { ChartOptions } from 'chart.js';

export const baseOpts = (yFmt: (val: number) => string = (v) => String(v), showLegend: boolean = false): ChartOptions<any> => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      display: showLegend,
      labels: {
        color: '#273547', // Note: use CSS variables or keep standard
        font: { family: "'DM Mono',monospace", size: 10 },
        boxWidth: 10,
        padding: 12
      }
    },
    tooltip: {
      backgroundColor: '#18212f',
      borderColor: 'rgba(255,255,255,0.09)',
      borderWidth: 1,
      titleColor: '#64788f',
      bodyColor: '#dce8f4',
      padding: 10,
      titleFont: { family: "'DM Mono',monospace", size: 10 },
      bodyFont: { family: "'DM Sans',sans-serif", size: 12 },
      callbacks: {
        label: (c: any) => ` ${c.dataset.label}: ${yFmt(c.parsed.y)}`
      }
    }
  },
  scales: {
    x: {
      grid: { color: 'rgba(128,128,128,0.1)' },
      border: { color: 'rgba(128,128,128,0.1)' },
      ticks: { color: '#8fa8be', font: { family: "'DM Mono',monospace", size: 10 }, maxRotation: 0 }
    },
    y: {
      grid: { color: 'rgba(128,128,128,0.1)' },
      border: { color: 'rgba(128,128,128,0.1)' },
      ticks: {
        color: '#8fa8be',
        font: { family: "'DM Mono',monospace", size: 10 },
        callback: (val: any) => yFmt(val)
      }
    }
  }
});

export const lineDs = (label: string, data: number[], color: string, fill: boolean, alpha: number = 0.12): any => {
  return {
    label,
    data,
    borderColor: `rgba(${color},1)`,
    backgroundColor: fill ? `rgba(${color},${alpha})` : 'transparent',
    borderWidth: 1.8,
    pointRadius: 0,
    pointHoverRadius: 4,
    tension: 0.42,
    fill
  };
};

export const barDs = (label: string, data: number[], color: string): any => {
  return {
    label,
    data,
    backgroundColor: `rgba(${color},0.7)`,
    borderColor: `rgba(${color},1)`,
    borderWidth: 1,
    borderRadius: 3,
    borderSkipped: false
  };
};

export const sparkDs = (data: number[], color: string): any => {
  return {
    data,
    borderColor: `rgba(${color},0.9)`,
    backgroundColor: 'transparent',
    borderWidth: 1.5,
    pointRadius: 0,
    tension: 0.4,
    fill: false
  };
};

export const sparkOpts = (): ChartOptions<any> => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { enabled: false } },
  scales: { x: { display: false }, y: { display: false } },
  layout: { padding: 0 }
});

export const rand = (min: number, max: number) => Math.floor(Math.random() * (max - min + 1)) + min;
export const randFloat = (min: number, max: number, dec: number = 1) => parseFloat((Math.random() * (max - min) + min).toFixed(dec));
export const genSeries = (n: number, base: number, variance: number) => {
  const out = [];
  let v = base;
  for (let i = 0; i < n; i++) {
    v = Math.max(base * 0.3, v + rand(-variance, variance));
    out.push(Math.round(v));
  }
  return out;
};
export const last24hLabels = () => {
  const labels = [];
  for (let i = 23; i >= 0; i--) {
    const d = new Date(Date.now() - i * 3600000);
    labels.push(d.getHours().toString().padStart(2, '0') + ':00');
  }
  return labels;
};
export const last30Labels = (unit: string) => {
  const labels = [];
  for (let i = 29; i >= 0; i--) {
    labels.push(i === 0 ? 'now' : i + unit);
  }
  return labels;
};
