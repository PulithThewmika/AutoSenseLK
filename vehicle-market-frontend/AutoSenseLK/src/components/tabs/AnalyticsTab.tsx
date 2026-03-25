import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import { DISTRICTS } from '../data/mockData';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface AnalyticsTabProps {
  isDark: boolean;
}

export function AnalyticsTab({ isDark }: AnalyticsTabProps) {
  const [aView, setAView] = useState<'overview' | 'models' | 'districts'>('overview');

  const tc = isDark
    ? { grid: 'rgba(255,255,255,0.045)', tick: '#2a3c4e', ttBg: '#18212f', ttBorder: 'rgba(255,255,255,0.09)', ttTitle: '#64788f', ttBody: '#e6ecf4', ptBorder: '#07090e' }
    : { grid: 'rgba(0,0,0,0.06)', tick: '#9ca3af', ttBg: '#ffffff', ttBorder: 'rgba(0,0,0,0.1)', ttTitle: '#6b7280', ttBody: '#111827', ptBorder: '#f7f9fc' };

  const getGradient = (ctx: CanvasRenderingContext2D, r: number, g: number, b: number, a: number, h: number = 280) => {
    const gr = ctx.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, `rgba(${r},${g},${b},${a})`);
    gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
    return gr;
  };

  const baseOpts = (yCb: (val: any) => string): any => ({
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: tc.ttBg, borderColor: tc.ttBorder, borderWidth: 1,
        titleColor: tc.ttTitle, bodyColor: tc.ttBody, padding: 11,
        titleFont: { family: "'DM Mono',monospace", size: 11 },
        bodyFont: { family: "'DM Sans',sans-serif", size: 13 }
      }
    },
    scales: {
      x: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 } } },
      y: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 }, callback: yCb } }
    }
  });

  const depOpts = baseOpts((v) => `Rs.${Math.round(v / 1000)}K`);
  depOpts.plugins.tooltip.callbacks = { label: (c: any) => ` Rs. ${(c.parsed.y * 1000).toLocaleString()}` };

  const mileOpts = baseOpts((v) => `Rs.${Math.round(v / 1000)}K`);
  mileOpts.plugins.tooltip.callbacks = { label: (c: any) => ` Honda Vezel: Rs. ${(c.parsed.y * 1000).toLocaleString()}` };

  const changeOpts = baseOpts((v) => `${v}%`);
  changeOpts.plugins.tooltip.callbacks = { label: (c: any) => ` ${c.parsed.y}%` };
  changeOpts.scales.y.min = -2;
  changeOpts.scales.y.max = 4;

  const distOpts = baseOpts((v) => v.toString());
  distOpts.plugins.tooltip.callbacks = { label: (c: any) => ` ${c.parsed.y.toLocaleString()} listings` };

  const doughnutOpts = {
    responsive: true, maintainAspectRatio: false, cutout: '64%',
    plugins: {
      legend: { display: false },
      tooltip: { backgroundColor: tc.ttBg, bodyColor: tc.ttBody, padding: 10, bodyFont: { family: "'DM Sans',sans-serif" } }
    }
  };

  return (
    <div className="tab-panel active" id="panel-analytics">
      <div className="analytics-pad">
        <div className="sec-eye">Market Analytics</div>
        <h2 className="sec-h">Live data. <span className="muted">Four levels deep.</span></h2>
        <p className="sec-sub" style={{ marginBottom: 26 }}>Daily analytics at market-wide, per-brand, per-condition, and per-make×model×year levels.</p>
        
        <div className="a-subtabs">
          <button className={`astab ${aView === 'overview' ? 'active' : ''}`} onClick={() => setAView('overview')}>Overview</button>
          <button className={`astab ${aView === 'models' ? 'active' : ''}`} onClick={() => setAView('models')}>Top Models</button>
          <button className={`astab ${aView === 'districts' ? 'active' : ''}`} onClick={() => setAView('districts')}>Districts</button>
        </div>

        {aView === 'overview' && (
          <div className="a-view active" id="av-overview">
            <div className="ag">
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Depreciation by year — Toyota Aqua</div><div className="ac-badge">DEPRECIATION</div></div>
                <div className="ch200">
                  <Bar
                    data={{
                      labels: ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
                      datasets: [{
                        label: 'Avg Price',
                        data: [3800, 4200, 5100, 5800, 7400, 8200, 9100, 10200, 11500, 12800, 14200],
                        backgroundColor: 'rgba(0,184,217,0.7)', borderColor: '#00b8d9', borderWidth: 1, borderRadius: 5
                      }]
                    }}
                    options={depOpts}
                  />
                </div>
              </div>
              
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Market condition split — All brands</div><div className="ac-badge">TODAY</div></div>
                <div className="cond-row" style={{ marginBottom: 12 }}>
                  <div className="cond-item"><div className="cond-dot" style={{ background: 'var(--cyan)' }}></div><div className="cond-label">Used</div><div className="cond-bar-out"><div className="cond-bar-in" style={{ width: '62%', background: 'var(--cyan)' }}></div></div><div className="cond-pct">62%</div></div>
                  <div className="cond-item"><div className="cond-dot" style={{ background: 'var(--green)' }}></div><div className="cond-label">Reconditioned</div><div className="cond-bar-out"><div className="cond-bar-in" style={{ width: '24%', background: 'var(--green)' }}></div></div><div className="cond-pct">24%</div></div>
                  <div className="cond-item"><div className="cond-dot" style={{ background: 'var(--yellow)' }}></div><div className="cond-label">Brand new</div><div className="cond-bar-out"><div className="cond-bar-in" style={{ width: '14%', background: 'var(--yellow)' }}></div></div><div className="cond-pct">14%</div></div>
                </div>
                <div className="ch160">
                  <Doughnut
                    data={{
                      labels: ['Used', 'Reconditioned', 'Brand New'],
                      datasets: [{ data: [62, 24, 14], backgroundColor: ['rgba(0,184,217,0.85)', 'rgba(0,208,132,0.85)', 'rgba(245,200,66,0.85)'], borderWidth: 0, hoverOffset: 5 }]
                    }}
                    options={doughnutOpts}
                  />
                </div>
              </div>

              <div className="ac">
                <div className="ac-head"><div className="ac-title">Price vs mileage — Honda Vezel</div><div className="ac-badge">MILEAGE CURVE</div></div>
                <div className="ch200">
                  <Line
                    data={{
                      labels: ['0–25k', '25–50k', '50–75k', '75–100k', '100–125k', '125–150k', '150k+'],
                      datasets: [{
                        label: 'Honda Vezel', data: [12800, 11200, 10200, 9100, 7800, 6900, 5800],
                        borderColor: '#0057ff', backgroundColor: (ctx: any) => getGradient(ctx.chart.ctx, 0, 87, 255, 0.13, 200),
                        borderWidth: 2.2, pointRadius: 5, pointBackgroundColor: '#0057ff',
                        pointBorderColor: tc.ptBorder, pointBorderWidth: 2, tension: 0.35, fill: true
                      }]
                    }}
                    options={mileOpts}
                  />
                </div>
              </div>

              <div className="ac">
                <div className="ac-head"><div className="ac-title">Deal quality distribution — This week</div><div className="ac-badge">DEAL SPLIT</div></div>
                <div className="cond-row" style={{ marginBottom: 12 }}>
                  <div className="cond-item"><div className="cond-dot" style={{ background: 'var(--green)' }}></div><div className="cond-label">Good deals</div><div className="cond-bar-out"><div className="cond-bar-in" style={{ width: '12%', background: 'var(--green)' }}></div></div><div className="cond-pct">12%</div></div>
                  <div className="cond-item"><div className="cond-dot" style={{ background: 'var(--yellow)' }}></div><div className="cond-label">Fair price</div><div className="cond-bar-out"><div className="cond-bar-in" style={{ width: '55%', background: 'var(--yellow)' }}></div></div><div className="cond-pct">55%</div></div>
                  <div className="cond-item"><div className="cond-dot" style={{ background: 'var(--orange)' }}></div><div className="cond-label">Overpriced</div><div className="cond-bar-out"><div className="cond-bar-in" style={{ width: '33%', background: 'var(--orange)' }}></div></div><div className="cond-pct">33%</div></div>
                </div>
                <div className="ch160">
                  <Doughnut
                    data={{
                      labels: ['Good deal', 'Fair price', 'Overpriced'],
                      datasets: [{ data: [12, 55, 33], backgroundColor: ['rgba(0,208,132,0.85)', 'rgba(245,200,66,0.85)', 'rgba(255,94,58,0.85)'], borderWidth: 0, hoverOffset: 5 }]
                    }}
                    options={doughnutOpts}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {aView === 'models' && (
          <div className="a-view active" id="av-models">
            <div className="ag">
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Top models by listing count</div><div className="ac-badge">THIS WEEK</div></div>
                <div className="model-list">
                  <div className="mr"><div className="mr-rank">1</div><div className="mr-info"><div className="mr-name">Toyota Aqua</div><div className="mr-count">1,240 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '100%' }}></div></div><div className="mr-price">Rs. 7.68M</div></div>
                  <div className="mr"><div className="mr-rank">2</div><div className="mr-info"><div className="mr-name">Suzuki Alto</div><div className="mr-count">980 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '79%' }}></div></div><div className="mr-price">Rs. 4.35M</div></div>
                  <div className="mr"><div className="mr-rank">3</div><div className="mr-info"><div className="mr-name">Honda Vezel</div><div className="mr-count">820 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '66%' }}></div></div><div className="mr-price">Rs. 10.2M</div></div>
                  <div className="mr"><div className="mr-rank">4</div><div className="mr-info"><div className="mr-name">Toyota Prius</div><div className="mr-count">760 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '61%' }}></div></div><div className="mr-price">Rs. 8.90M</div></div>
                  <div className="mr"><div className="mr-rank">5</div><div className="mr-info"><div className="mr-name">Nissan Leaf</div><div className="mr-count">590 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '48%' }}></div></div><div className="mr-price">Rs. 6.10M</div></div>
                  <div className="mr"><div className="mr-rank">6</div><div className="mr-info"><div className="mr-name">Honda Fit</div><div className="mr-count">510 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '41%' }}></div></div><div className="mr-price">Rs. 5.20M</div></div>
                  <div className="mr"><div className="mr-rank">7</div><div className="mr-info"><div className="mr-name">Mazda Demio</div><div className="mr-count">445 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '36%' }}></div></div><div className="mr-price">Rs. 5.75M</div></div>
                  <div className="mr"><div className="mr-rank">8</div><div className="mr-info"><div className="mr-name">Perodua Axia</div><div className="mr-count">390 listings</div></div><div className="mr-bar-out"><div className="mr-bar-in" style={{ width: '31%' }}></div></div><div className="mr-price">Rs. 3.90M</div></div>
                </div>
              </div>
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Price change vs last month — Top models</div><div className="ac-badge">CHANGE %</div></div>
                <div className="ch200">
                  <Bar
                    data={{
                      labels: ['Aqua', 'Alto', 'Vezel', 'Prius', 'Leaf', 'Fit', 'Demio', 'Axia'],
                      datasets: [{
                        label: 'Change %',
                        data: [2.1, -0.5, 1.8, 0.9, 3.4, -1.2, 1.5, 2.6],
                        backgroundColor: [2.1, -0.5, 1.8, 0.9, 3.4, -1.2, 1.5, 2.6].map(v => v >= 0 ? 'rgba(0,208,132,0.75)' : 'rgba(255,94,58,0.75)'),
                        borderWidth: 0, borderRadius: 4
                      }]
                    }}
                    options={changeOpts}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {aView === 'districts' && (
          <div className="a-view active" id="av-districts">
            <div className="ac">
              <div className="ac-head"><div className="ac-title">Average listing price by district</div><div className="ac-badge">ALL BRANDS</div></div>
              <div className="dist-grid">
                {DISTRICTS.map((d, i) => (
                  <div key={i} className="dist-card">
                    <div className="dist-name">{d.name}</div>
                    <div className="dist-price">{d.price}</div>
                    <div className="dist-count">{d.count.toLocaleString()} listings</div>
                  </div>
                ))}
              </div>
            </div>
            <div className="ac" style={{ marginTop: 16 }}>
              <div className="ac-head"><div className="ac-title">Listing volume by district</div><div className="ac-badge">THIS WEEK</div></div>
              <div className="ch200">
                <Bar
                  data={{
                    labels: DISTRICTS.map(d => d.name),
                    datasets: [{
                      label: 'Listings',
                      data: DISTRICTS.map(d => d.count),
                      backgroundColor: 'rgba(0,184,217,0.65)', borderColor: '#00b8d9', borderWidth: 1, borderRadius: 3
                    }]
                  }}
                  options={distOpts}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
