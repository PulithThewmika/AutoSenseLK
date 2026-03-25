import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import { BRANDS } from '../data/mockData';

interface BrandsTabProps {
  isDark: boolean;
}

export function BrandsTab({ isDark }: BrandsTabProps) {
  const [filter, setFilter] = useState<string>('all');
  const [selectedBrand, setSelectedBrand] = useState<any | null>(null);

  const tc = isDark
    ? { grid: 'rgba(255,255,255,0.045)', tick: '#2a3c4e', ttBg: '#18212f', ttBorder: 'rgba(255,255,255,0.09)', ttTitle: '#64788f', ttBody: '#e6ecf4', ptBorder: '#07090e' }
    : { grid: 'rgba(0,0,0,0.06)', tick: '#9ca3af', ttBg: '#ffffff', ttBorder: 'rgba(0,0,0,0.1)', ttTitle: '#6b7280', ttBody: '#111827', ptBorder: '#f7f9fc' };

  const getGradient = (ctx: CanvasRenderingContext2D) => {
    const gr = ctx.createLinearGradient(0, 0, 0, 130);
    gr.addColorStop(0, 'rgba(0,184,217,0.15)');
    gr.addColorStop(1, 'rgba(0,184,217,0)');
    return gr;
  };

  const filteredBrands = BRANDS.filter(b => filter === 'all' || b.cat === filter || b.name === '44 more');

  const handleBrandClick = (b: any) => {
    if (b.name === '44 more' || !b.hist || !b.hist.length) return;
    setSelectedBrand(b);
    setTimeout(() => {
      document.getElementById('brandDetail')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 50);
  };

  const chartOpts: any = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: tc.ttBg, borderColor: tc.ttBorder, borderWidth: 1,
        titleColor: tc.ttTitle, bodyColor: tc.ttBody, padding: 11,
        titleFont: { family: "'DM Mono',monospace", size: 11 },
        bodyFont: { family: "'DM Sans',sans-serif", size: 13 },
        callbacks: { label: (c: any) => ` Rs. ${(c.parsed.y * 1000).toLocaleString()}` }
      }
    },
    scales: {
      x: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 } } },
      y: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 }, callback: (v: any) => `Rs.${Math.round(v / 1000)}K` } }
    }
  };

  return (
    <div className="tab-panel active" id="panel-brands">
      <div className="brands-pad">
        <div className="sec-eye">Supported brands</div>
        <h2 className="sec-h">55 brands. 300+ models. <span className="muted">All covered.</span></h2>
        <p className="sec-sub">Model-level crawling for 11 major brands, plus 44 additional brands at brand level. Click any brand to see details.</p>
        
        <div className="brand-filter-row">
          <button className={`bfbtn ${filter === 'all' ? 'active' : ''}`} onClick={() => { setFilter('all'); setSelectedBrand(null); }}>All brands</button>
          <button className={`bfbtn ${filter === 'japanese' ? 'active' : ''}`} onClick={() => { setFilter('japanese'); setSelectedBrand(null); }}>Japanese</button>
          <button className={`bfbtn ${filter === 'european' ? 'active' : ''}`} onClick={() => { setFilter('european'); setSelectedBrand(null); }}>European</button>
          <button className={`bfbtn ${filter === 'korean' ? 'active' : ''}`} onClick={() => { setFilter('korean'); setSelectedBrand(null); }}>Korean</button>
          <button className={`bfbtn ${filter === 'other' ? 'active' : ''}`} onClick={() => { setFilter('other'); setSelectedBrand(null); }}>Other</button>
        </div>
        
        <div className="brand-grid">
          {filteredBrands.map((b, i) => {
            const isDashed = b.name === '44 more';
            return (
              <div 
                key={i} 
                className="brand-card" 
                style={isDashed ? { borderStyle: 'dashed', opacity: 0.6, cursor: 'default' } : {}}
                onClick={() => handleBrandClick(b)}
              >
                <div className="brand-logo">{b.logo}</div>
                <div className="brand-name">{b.name}</div>
                <div className="brand-count">{b.models ? `${b.models} models` : 'brand-level'}</div>
                {b.change && (
                  <div className={`brand-trend ${b.up ? 'brand-up' : 'brand-dn'}`}>{b.change}</div>
                )}
              </div>
            );
          })}
        </div>

        {selectedBrand && (
          <div className="brand-detail open" id="brandDetail">
            <div className="bd-head">
              <div className="bd-title">{selectedBrand.logo} {selectedBrand.name}</div>
              <button className="bd-close" onClick={() => setSelectedBrand(null)}>✕</button>
            </div>
            <div className="bd-grid">
              <div className="bd-stat"><div className="bd-stat-l">Avg price</div><div className="bd-stat-v">{selectedBrand.avgPrice}</div></div>
              <div className="bd-stat"><div className="bd-stat-l">Listings / week</div><div className="bd-stat-v">{selectedBrand.count.toLocaleString()}</div></div>
              <div className="bd-stat">
                <div className="bd-stat-l">Monthly change</div>
                <div className="bd-stat-v" style={{ color: selectedBrand.up ? 'var(--green)' : 'var(--orange)' }}>{selectedBrand.change}</div>
              </div>
              <div className="bd-stat"><div className="bd-stat-l">Good deal rate</div><div className="bd-stat-v">{selectedBrand.goodRate}</div></div>
            </div>
            <div className="sec-eye" style={{ fontSize: 10, marginBottom: 6 }}>6-month price trend</div>
            <div className="bd-chart-h">
              <Line
                data={{
                  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                  datasets: [{
                    label: selectedBrand.name,
                    data: selectedBrand.hist,
                    borderColor: '#00b8d9',
                    backgroundColor: (ctx: any) => getGradient(ctx.chart.ctx),
                    borderWidth: 2, pointRadius: 4, pointBackgroundColor: '#00b8d9',
                    pointBorderColor: tc.ptBorder, pointBorderWidth: 2, tension: 0.38, fill: true
                  }]
                }}
                options={chartOpts}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
