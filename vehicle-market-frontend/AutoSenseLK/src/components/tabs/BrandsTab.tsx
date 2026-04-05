import { useState, useEffect } from 'react';
import type { ChartData, ChartOptions, ScriptableContext, TooltipItem } from 'chart.js';
import { Line } from 'react-chartjs-2';
import { getDailyBrands, getDailyHistory } from '../../services/api';

const getGradient = (ctx: CanvasRenderingContext2D) => {
  const gr = ctx.createLinearGradient(0, 0, 0, 130);
  gr.addColorStop(0, 'rgba(0,184,217,0.15)');
  gr.addColorStop(1, 'rgba(0,184,217,0)');
  return gr;
};

interface BrandApiItem {
  brand: string;
  price_change_pct?: number;
  avg_price: number;
  total_listings: number;
}

interface BrandItem {
  name: string;
  logo: string;
  cat: string;
  models: number;
  change: string;
  up: boolean;
  avgPrice: string;
  count: number;
  goodRate: string;
}

interface HistoryApiItem {
  date: string;
  avg_price: number;
}

interface BrandsTabProps {
  isDark: boolean;
}

export function BrandsTab({ isDark }: BrandsTabProps) {
  const [filter, setFilter] = useState<string>('all');
  const [brandsData, setBrandsData] = useState<BrandItem[]>([]);
  const [selectedBrand, setSelectedBrand] = useState<BrandItem | null>(null);
  const [brandHistory, setBrandHistory] = useState<ChartData<'line'> | null>(null);

  useEffect(() => {
    getDailyBrands().then(res => {
      // Map API array to UI array format with generic emojis
      // Add fake categories so filters do not break
      const logos: Record<string, string> = { Toyota:'🚗', Honda:'🚙', BMW:'🏎', Mercedes:'⭐', Nissan:'🔵', Suzuki:'🟡' };
      const cats: Record<string, string> = { Toyota:'japanese', Honda:'japanese', BMW:'european', Mercedes:'european', Nissan:'japanese', Suzuki:'japanese' };
      
      const arr = res.brands ? res.brands : (Array.isArray(res) ? res : res.data || []);
      const mapped = arr.map((i: BrandApiItem) => ({
         name: i.brand,
         logo: logos[i.brand] || '🚘',
         cat: cats[i.brand] || 'other',
         models: 0,
         change: i.price_change_pct ? `${i.price_change_pct > 0 ? '+' : ''}${i.price_change_pct.toFixed(2)}%` : '-',
         up: (i.price_change_pct || 0) > 0,
         avgPrice: `Rs. ${(i.avg_price / 1000000).toFixed(1)}M`,
         count: i.total_listings,
         goodRate: 'N/A'
      })).sort((a: BrandItem, b: BrandItem) => b.count - a.count);
      
      setBrandsData(mapped);
    }).catch(console.error);
  }, []);

  const tc = isDark
    ? { grid: 'rgba(255,255,255,0.045)', tick: '#2a3c4e', ttBg: '#18212f', ttBorder: 'rgba(255,255,255,0.09)', ttTitle: '#64788f', ttBody: '#e6ecf4', ptBorder: '#07090e' }
    : { grid: 'rgba(0,0,0,0.06)', tick: '#9ca3af', ttBg: '#ffffff', ttBorder: 'rgba(0,0,0,0.1)', ttTitle: '#6b7280', ttBody: '#111827', ptBorder: '#f7f9fc' };



  const filteredBrands = brandsData.filter((b: BrandItem) => filter === 'all' || b.cat === filter);

  const handleBrandClick = (b: BrandItem) => {
    setSelectedBrand(b);
    setBrandHistory(null);
    getDailyHistory('brand', b.name, 30).then(res => {
      const arr = Array.isArray(res) ? res : res.data || Object.values(res);
      const sorted = arr.sort((x: HistoryApiItem, y: HistoryApiItem) => new Date(x.date).getTime() - new Date(y.date).getTime());
      setBrandHistory({
         labels: sorted.map((s: HistoryApiItem) => s.date.slice(5)),
         datasets: [{
           label: b.name,
           data: sorted.map((s: HistoryApiItem) => s.avg_price),
           borderColor: '#00b8d9',
           backgroundColor: (ctx: ScriptableContext<'line'>) => getGradient(ctx.chart.ctx),
           borderWidth: 2, pointRadius: 4, pointBackgroundColor: '#00b8d9',
           pointBorderColor: tc.ptBorder, pointBorderWidth: 2, tension: 0.38, fill: true
         }]
      });
    }).catch(console.error);

    setTimeout(() => {
      document.getElementById('brandDetail')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 50);
  };

  const chartOpts: ChartOptions<'line'> = {
    responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: tc.ttBg, borderColor: tc.ttBorder, borderWidth: 1,
        titleColor: tc.ttTitle, bodyColor: tc.ttBody, padding: 11,
        titleFont: { family: "'DM Mono',monospace", size: 11 }, bodyFont: { family: "'DM Sans',sans-serif", size: 13 },
        callbacks: { label: (c: TooltipItem<'line'>) => ` Rs. ${((c.parsed.y || 0) * 1).toLocaleString()}` }
      }
    },
    scales: {
      x: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 } } },
      y: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 }, callback: (v: string | number) => `Rs.${Math.round(Number(v) / 100000) / 10}M` } }
    }
  };

  return (
    <div className="tab-panel active" id="panel-brands">
      <div className="brands-pad">
        <div className="sec-eye">Supported brands</div>
        <h2 className="sec-h">Live market taxonomy. <span className="muted">All covered.</span></h2>
        <p className="sec-sub">Model-level crawling from the live API. Click any brand to see detailed 30-day historical trendlines.</p>
        
        <div className="brand-filter-row">
          <button className={`bfbtn ${filter === 'all' ? 'active' : ''}`} onClick={() => { setFilter('all'); setSelectedBrand(null); }}>All brands</button>
          <button className={`bfbtn ${filter === 'japanese' ? 'active' : ''}`} onClick={() => { setFilter('japanese'); setSelectedBrand(null); }}>Japanese</button>
          <button className={`bfbtn ${filter === 'european' ? 'active' : ''}`} onClick={() => { setFilter('european'); setSelectedBrand(null); }}>European</button>
          <button className={`bfbtn ${filter === 'korean' ? 'active' : ''}`} onClick={() => { setFilter('korean'); setSelectedBrand(null); }}>Korean</button>
          <button className={`bfbtn ${filter === 'other' ? 'active' : ''}`} onClick={() => { setFilter('other'); setSelectedBrand(null); }}>Other</button>
        </div>
        
        <div className="brand-grid">
          {filteredBrands.map((b, i) => {
            return (
              <div key={i} className="brand-card" onClick={() => handleBrandClick(b)}>
                <div className="brand-logo">{b.logo}</div>
                <div className="brand-name">{b.name}</div>
                <div className="brand-count">{b.count.toLocaleString()} samples</div>
                {b.change && b.change !== '-' && (
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
              <div className="bd-stat"><div className="bd-stat-l">Network Volume</div><div className="bd-stat-v">{selectedBrand.count.toLocaleString()}</div></div>
              <div className="bd-stat">
                <div className="bd-stat-l">Monthly change</div>
                <div className="bd-stat-v" style={{ color: selectedBrand.up ? 'var(--green)' : 'var(--orange)' }}>{selectedBrand.change}</div>
              </div>
              <div className="bd-stat"><div className="bd-stat-l">Good deal rate</div><div className="bd-stat-v">{selectedBrand.goodRate}</div></div>
            </div>
            <div className="sec-eye" style={{ fontSize: 10, marginBottom: 6 }}>30-day price trend</div>
            <div className="bd-chart-h">
              {brandHistory ? <Line data={brandHistory} options={chartOpts} /> : <div style={{height:'100%', display:'flex', alignItems:'center', justifyContent:'center', color:'var(--mu)'}}>Loading 30-day API history curve...</div>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
