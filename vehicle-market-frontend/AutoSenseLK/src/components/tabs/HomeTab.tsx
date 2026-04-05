import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { getSummary, getTrends, getListings } from '../../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
);

interface HomeTabProps {
  onTabChange: (tabId: string) => void;
  isDark: boolean;
}

export function HomeTab({ onTabChange, isDark }: HomeTabProps) {
  const [range, setRange] = useState<'6m' | '1y' | 'all'>('6m');
  const [summary, setSummary] = useState<any>(null);
  const [tickers, setTickers] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any>(null);

  const tc = isDark
    ? { grid: 'rgba(255,255,255,0.045)', tick: '#2a3c4e', ttBg: '#18212f', ttBorder: 'rgba(255,255,255,0.09)', ttTitle: '#64788f', ttBody: '#e6ecf4', ptBorder: '#07090e' }
    : { grid: 'rgba(0,0,0,0.06)', tick: '#9ca3af', ttBg: '#ffffff', ttBorder: 'rgba(0,0,0,0.1)', ttTitle: '#6b7280', ttBody: '#111827', ptBorder: '#f7f9fc' };

  const getGradient = (ctx: CanvasRenderingContext2D, r: number, g: number, b: number, a: number) => {
    const gr = ctx.createLinearGradient(0, 0, 0, 280);
    gr.addColorStop(0, `rgba(${r},${g},${b},${a})`);
    gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
    return gr;
  };

  useEffect(() => {
    getSummary().then(res => setSummary(res)).catch(console.error);
    getListings(1, 20).then(res => setTickers(res.results)).catch(console.error);
  }, []);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const months = range === '6m' ? 6 : range === '1y' ? 12 : 24;
        const models = [
          { make: 'Toyota', model: 'Aqua', color: '#00b8d9', rgb: [0, 184, 217] },
          { make: 'Honda', model: 'Vezel', color: '#0057ff', rgb: [0, 87, 255] },
          { make: 'Suzuki', model: 'Alto', color: '#ff5e3a', rgb: [255, 94, 58] },
          { make: 'Nissan', model: 'Leaf', color: '#f5c842', rgb: [245, 200, 66] },
          { make: 'Toyota', model: 'Prius', color: '#a855f7', rgb: [168, 85, 247] }
        ];

        const reqs = models.map(m => getTrends(m.make, m.model, months).catch(() => null));
        const res = await Promise.all(reqs);

        let labels = [] as string[];
        if (res.length > 0 && res[0]) {
           const historyKeys = Object.keys(res[0].history || {}).sort();
           labels = historyKeys.map(k => {
             const [y, m] = k.split('-');
             const name = new Date(parseInt(y), parseInt(m) - 1).toLocaleString('default', { month: 'short' });
             return `${name} ${y.slice(2)}`;
           });
        }

        const datasets = models.map((m, i) => {
          const raw = res[i]?.history || {};
          const keys = Object.keys(raw).sort();
          const data = keys.map(k => raw[k]);

          return {
            label: `${m.make} ${m.model}`,
            data,
            borderColor: m.color,
            backgroundColor: (context: any) => getGradient(context.chart.ctx, m.rgb[0], m.rgb[1], m.rgb[2], 0.17),
            borderWidth: 2.2,
            pointRadius: 0,
            pointHoverRadius: 5,
            tension: 0.42,
            fill: true,
          };
        });

        setChartData({ labels, datasets });
      } catch (err) {
        console.error(err);
      }
    };
    fetchTrends();
  }, [range]);


  const chartOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: tc.ttBg,
        borderColor: tc.ttBorder,
        borderWidth: 1,
        titleColor: tc.ttTitle,
        bodyColor: tc.ttBody,
        padding: 11,
        titleFont: { family: "'DM Mono',monospace", size: 11 },
        bodyFont: { family: "'DM Sans',sans-serif", size: 13 },
        callbacks: {
          label: (c: any) => ` ${c.dataset.label}: Rs. ${(c.parsed.y * 1).toLocaleString()}`
        }
      },
    },
    scales: {
      x: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 } } },
      y: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 }, callback: (v: any) => `Rs.${Math.round(v / 100000) / 10}M` } }
    },
  };

  return (
    <div className="tab-panel active" id="panel-home">
      <div className="home-hero">
        <div className="orb orb1"></div>
        <div className="orb orb2"></div>
        <div className="hero-body">
          <div className="hero-text">
            <div className="badge"><span className="pulse"></span>Live · Sri Lanka Vehicle Market</div>
            <h1>Sense the<br /><em>true price</em><br />of any car.</h1>
            <p className="hero-sub">AutoSenseLK tracks live ikman.lk listings across Sri Lanka — using data intelligence to help you know exactly what any car is really worth.</p>
            <div className="hero-actions">
              <button className="btn-p" onClick={() => onTabChange('analytics')}>
                Explore market 
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none" style={{ marginLeft: 6 }}>
                  <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </button>
              <button className="btn-s" onClick={() => onTabChange('deals')}>Score a listing</button>
            </div>
          </div>
          <div className="hero-stats">
            <div className="sc"><div className="sc-label">Avg. Market Price</div><div className="sc-val">Rs. {summary ? (summary.avg_price / 1000000).toFixed(2) : '-'}M</div><div className="sc-delta">Live</div></div>
            <div className="sc"><div className="sc-label">Listings Tracked</div><div className="sc-val">{summary ? summary.total_listings.toLocaleString() : '-'}</div><div className="sc-delta">Live DB Items</div></div>
            <div className="sc"><div className="sc-label">Latest Listing</div><div className="sc-val" style={{ fontSize: '13px', color: 'var(--cyan)', lineHeight: 1.4 }}>{tickers[0] ? `${tickers[0].make} ${tickers[0].model} ${tickers[0].year}` : '-'}</div><div className="sc-delta">Added Recently</div></div>
          </div>
        </div>
        
        <div className="hero-chart">
          <div className="cc">
            <div className="cc-head">
              <div><div className="cc-eye">AutoSenseLK · Market Overview</div><div className="cc-title">Average price trends — Top models</div></div>
              <div className="cc-r">
                <div className="live-dot">Updated: <span>just now</span></div>
                <div className="range-tabs">
                  <button className={`rtab ${range === '6m' ? 'active' : ''}`} onClick={() => setRange('6m')}>6M</button>
                  <button className={`rtab ${range === '1y' ? 'active' : ''}`} onClick={() => setRange('1y')}>1Y</button>
                  <button className={`rtab ${range === 'all' ? 'active' : ''}`} onClick={() => setRange('all')}>All</button>
                </div>
              </div>
            </div>
            <div className="cc-legend">
              <div className="leg"><div className="ld" style={{ background: '#00b8d9' }}></div>Aqua</div>
              <div className="leg"><div className="ld" style={{ background: '#0057ff' }}></div>Vezel</div>
              <div className="leg"><div className="ld" style={{ background: '#ff5e3a' }}></div>Alto</div>
              <div className="leg"><div className="ld" style={{ background: '#f5c842' }}></div>Leaf</div>
              <div className="leg"><div className="ld" style={{ background: '#a855f7' }}></div>Prius</div>
              <div style={{ marginLeft: 'auto', fontFamily: "'DM Mono',monospace", fontSize: '10px', color: 'var(--mu)' }}>Prices in LKR</div>
            </div>
            <div className="cc-body">
              {chartData ? <Line data={chartData} options={chartOptions} /> : <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--mu)' }}>Loading trends...</div>}
            </div>
          </div>
        </div>
        
        {tickers.length > 0 && (
          <div className="ticker">
            <div className="tick-inner">
              {[...tickers, ...tickers, ...tickers].map((i, idx) => (
                <span className="tick-item" key={idx}>
                  <span className="tm">{i.make} {i.model} {i.year || ''}</span><span className="ts">·</span><span className="tp">Rs. {i.price.toLocaleString()}</span>
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="strip">
        <div className="si"><div className="sv">Live</div><div className="sl">New listings</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">{summary ? summary.makes_count || 56 : 56}</div><div className="sl">Brands tracked</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">{summary ? summary.models_count || 300 : 300}+</div><div className="sl">Models indexed</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">Scorer</div><div className="sl">Deal Intelligence</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">Island-wide</div><div className="sl">Districts covered</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">Automated</div><div className="sl">Scrape frequency</div></div>
      </div>

      <div className="feat-section">
        <div className="sec-eye">What AutoSenseLK does</div>
        <h2 className="sec-h">Everything to buy or sell smarter. <span className="muted">No guesswork.</span></h2>
        <div className="feat-grid">
          <div className="fc"><div className="fi ic-c">📊</div><div className="fn">Live price tracking</div><div className="fd">Scrapes ikman.lk. Average prices per make, model, and year — always current, never stale.</div></div>
          <div className="fc"><div className="fi ic-b">🤖</div><div className="fn">Deal scoring</div><div className="fd">Compares any listing against thousands of similar vehicles. Good deal, fair, or overpriced — in milliseconds.</div></div>
          <div className="fc"><div className="fi ic-o">📈</div><div className="fn">Price trend charts</div><div className="fd">Monthly historical averages for every popular model. See if prices are rising, cooling, or stable before you commit.</div></div>
          <div className="fc"><div className="fi ic-y">🔔</div><div className="fn">Price alerts</div><div className="fd">Set a target price for any model. Get notified the moment a listing drops below your threshold — never miss a deal.</div></div>
          <div className="fc"><div className="fi ic-p">🗺️</div><div className="fn">District insights</div><div className="fd">Prices vary by district. Colombo vs Kandy vs Galle — see where deals concentrate across all 25 districts.</div></div>
          <div className="fc"><div className="fi ic-g">⚖️</div><div className="fn">Model comparison</div><div className="fd">Side-by-side price history, depreciation rate, and deal frequency for any two models. Make an informed choice.</div></div>
        </div>
      </div>

      <div className="how-section">
        <div className="how-inner">
          <div className="sec-eye">How it works</div>
          <h2 className="sec-h">From raw listings to real intelligence.</h2>
          <div className="how-grid">
            <div className="step"><div className="step-n">01</div><div className="step-conn"></div><div className="step-t">We scrape</div><div className="step-d">Brands × models × conditions crawled via Azure backend.</div></div>
            <div className="step"><div className="step-n">02</div><div className="step-conn"></div><div className="step-t">We clean</div><div className="step-d">Prices normalised, duplicates removed via hashing, units standardised.</div></div>
            <div className="step"><div className="step-n">03</div><div className="step-conn"></div><div className="step-t">We analyse</div><div className="step-d">Aggregated daily analytics: market-wide, per-brand, and per-make × model.</div></div>
            <div className="step"><div className="step-n">04</div><div className="step-conn"></div><div className="step-t">You decide</div><div className="step-d">Real-time dashboards and scored deal quality give you confidence.</div></div>
          </div>
        </div>
      </div>

      <div className="cta-band" style={{ marginBottom: 0 }}>
        <div className="cta-h">Stop guessing.<br />Start sensing.</div>
        <p className="cta-sub">AutoSenseLK is free and open. No login required — explore the full Sri Lankan vehicle market right now.</p>
        <div className="cta-btns">
          <button className="btn-p" onClick={() => onTabChange('analytics')}>Explore the market →</button>
          <button className="btn-s" onClick={() => onTabChange('deals')}>Score a listing</button>
        </div>
      </div>
    </div>
  );
}
