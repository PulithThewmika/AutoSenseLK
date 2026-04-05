import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';
import { getDepreciation, getMileage, getAvgPrice } from '../../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface AnalyticsTabProps {
  isDark: boolean;
}

export function AnalyticsTab({ isDark }: AnalyticsTabProps) {
  const [aView, setAView] = useState<'overview' | 'models'>('overview');
  
  const [depData, setDepData] = useState<any>(null);
  const [mileData, setMileData] = useState<any>(null);
  const [topModels, setTopModels] = useState<any[]>([
    { make: 'Toyota', model: 'Aqua', price: 0, count: 0 },
    { make: 'Honda', model: 'Vezel', price: 0, count: 0 },
    { make: 'Suzuki', model: 'Alto', price: 0, count: 0 },
    { make: 'Nissan', model: 'Leaf', price: 0, count: 0 },
    { make: 'Toyota', model: 'Prius', price: 0, count: 0 },
    { make: 'Honda', model: 'Fit', price: 0, count: 0 },
    { make: 'Mazda', model: 'Demio', price: 0, count: 0 },
    { make: 'Perodua', model: 'Axia', price: 0, count: 0 },
  ]);

  const tc = isDark
    ? { grid: 'rgba(255,255,255,0.045)', tick: '#2a3c4e', ttBg: '#18212f', ttBorder: 'rgba(255,255,255,0.09)', ttTitle: '#64788f', ttBody: '#e6ecf4', ptBorder: '#07090e' }
    : { grid: 'rgba(0,0,0,0.06)', tick: '#9ca3af', ttBg: '#ffffff', ttBorder: 'rgba(0,0,0,0.1)', ttTitle: '#6b7280', ttBody: '#111827', ptBorder: '#f7f9fc' };

  const getGradient = (ctx: CanvasRenderingContext2D, r: number, g: number, b: number, a: number, h: number = 280) => {
    const gr = ctx.createLinearGradient(0, 0, h, h); // fixed start param, though the original was (0,0,0,h)
    gr.addColorStop(0, `rgba(${r},${g},${b},${a})`);
    gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
    return gr;
  };

  useEffect(() => {
    // Top model data (Aqua by default for overview)
    getDepreciation('Toyota', 'Aqua').then(res => {
      if(res && res.data) {
        const sorted = res.data.sort((a: any, b: any) => a.year - b.year);
        setDepData({
          labels: sorted.map((i: any) => i.year.toString()),
          datasets: [{
            label: 'Avg Price',
            data: sorted.map((i: any) => i.avg_price),
            backgroundColor: 'rgba(0,184,217,0.7)', borderColor: '#00b8d9', borderWidth: 1, borderRadius: 5
          }]
        });
      }
    }).catch(console.error);

    getMileage('Honda', 'Vezel').then(res => {
      // Assuming res shape is similar array or obj
      // For lack of explicit mileage curve API shape docs, mapped safely:
      if(res && res.data) {
        const arr = Array.isArray(res.data) ? res.data : Object.values(res.data);
        setMileData({
          labels: arr.map((i: any) => i.band || i.mileage || 'Odometer'),
          datasets: [{
             label: 'Vezel Price vs Mileage',
             data: arr.map((i: any) => i.avg_price || i.price),
             borderColor: '#0057ff', backgroundColor: (ctx: any) => getGradient(ctx.chart.ctx, 0, 87, 255, 0.13, 200),
             borderWidth: 2.2, pointRadius: 5, pointBackgroundColor: '#0057ff',
             pointBorderColor: tc.ptBorder, pointBorderWidth: 2, tension: 0.35, fill: true
          }]
        });
      }
    }).catch(console.error);
    
    // Fetch live prices for top models
    Promise.all(topModels.map(m => getAvgPrice(m.make, m.model).catch(() => null)))
      .then(results => {
         const updated = topModels.map((m, i) => {
           if(results[i]) {
             return { ...m, price: results[i].avg_price, count: results[i].sample_count };
           }
           return m;
         });
         setTopModels(updated.sort((a,b) => b.count - a.count));
      });
  }, []);


  const baseOpts = (yCb: (val: any) => string): any => ({
    responsive: true, maintainAspectRatio: false, interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: tc.ttBg, borderColor: tc.ttBorder, borderWidth: 1,
        titleColor: tc.ttTitle, bodyColor: tc.ttBody, padding: 11,
        titleFont: { family: "'DM Mono',monospace", size: 11 }, bodyFont: { family: "'DM Sans',sans-serif", size: 13 }
      }
    },
    scales: {
      x: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 } } },
      y: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 }, callback: yCb } }
    }
  });

  const depOpts = baseOpts((v) => `Rs.${Math.round(v / 100000) / 10}M`);
  depOpts.plugins.tooltip.callbacks = { label: (c: any) => ` Rs. ${(c.parsed.y * 1).toLocaleString()}` };

  const mileOpts = baseOpts((v) => `Rs.${Math.round(v / 100000) / 10}M`);
  mileOpts.plugins.tooltip.callbacks = { label: (c: any) => ` Rs. ${(c.parsed.y * 1).toLocaleString()}` };

  return (
    <div className="tab-panel active" id="panel-analytics">
      <div className="analytics-pad">
        <div className="sec-eye">Market Analytics</div>
        <h2 className="sec-h">Live data. <span className="muted">In focus.</span></h2>
        <p className="sec-sub" style={{ marginBottom: 26 }}>Daily analytics derived straight from Azure backend models mapping thousands of real-time listings.</p>
        
        <div className="a-subtabs">
          <button className={`astab ${aView === 'overview' ? 'active' : ''}`} onClick={() => setAView('overview')}>Overview</button>
          <button className={`astab ${aView === 'models' ? 'active' : ''}`} onClick={() => setAView('models')}>Top Models</button>
        </div>

        {aView === 'overview' && (
          <div className="a-view active" id="av-overview">
            <div className="ag">
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Depreciation by year — Toyota Aqua</div><div className="ac-badge">DEPRECIATION</div></div>
                <div className="ch200">
                  {depData ? <Bar data={depData} options={depOpts} /> : <div style={{height:'100%', display:'flex', alignItems:'center', justifyContent:'center', color:'var(--mu)'}}>Loading curve...</div>}
                </div>
              </div>
              
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Price vs mileage — Honda Vezel</div><div className="ac-badge">MILEAGE CURVE</div></div>
                <div className="ch200">
                  {mileData ? <Line data={mileData} options={mileOpts} /> : <div style={{height:'100%', display:'flex', alignItems:'center', justifyContent:'center', color:'var(--mu)'}}>Loading curve...</div>}
                </div>
              </div>
            </div>
          </div>
        )}

        {aView === 'models' && (
          <div className="a-view active" id="av-models">
            <div className="ag" style={{ gridTemplateColumns: '1fr' }}>
              <div className="ac">
                <div className="ac-head"><div className="ac-title">Live Averages & Availability</div><div className="ac-badge">LIVE</div></div>
                <div className="model-list">
                  {topModels.map((m, idx) => {
                     const maxCount = Math.max(...topModels.map(x => x.count), 1);
                     const width = `${Math.max(10, (m.count / maxCount) * 100)}%`;
                     return (
                       <div className="mr" key={m.model}>
                         <div className="mr-rank">{idx + 1}</div>
                         <div className="mr-info">
                           <div className="mr-name">{m.make} {m.model}</div>
                           <div className="mr-count">{m.count > 0 ? m.count.toLocaleString() : '-'} tracked samples</div>
                         </div>
                         <div className="mr-bar-out"><div className="mr-bar-in" style={{ width }}></div></div>
                         <div className="mr-price">Rs. {m.price > 0 ? (m.price/1000000).toFixed(2) + 'M' : '...'}</div>
                       </div>
                     )
                  })}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
