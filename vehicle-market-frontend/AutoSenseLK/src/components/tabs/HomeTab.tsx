import React, { useState } from 'react';
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
import { CD, TICKERS } from '../../data/mockData';

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

  const tc = isDark
    ? { grid: 'rgba(255,255,255,0.045)', tick: '#2a3c4e', ttBg: '#18212f', ttBorder: 'rgba(255,255,255,0.09)', ttTitle: '#64788f', ttBody: '#e6ecf4', ptBorder: '#07090e' }
    : { grid: 'rgba(0,0,0,0.06)', tick: '#9ca3af', ttBg: '#ffffff', ttBorder: 'rgba(0,0,0,0.1)', ttTitle: '#6b7280', ttBody: '#111827', ptBorder: '#f7f9fc' };

  const getGradient = (ctx: CanvasRenderingContext2D, r: number, g: number, b: number, a: number) => {
    const gr = ctx.createLinearGradient(0, 0, 0, 280);
    gr.addColorStop(0, `rgba(${r},${g},${b},${a})`);
    gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
    return gr;
  };

  const chartData = {
    labels: CD[range].labels,
    datasets: [
      {
        label: 'Toyota Aqua',
        data: CD[range].aqua,
        borderColor: '#00b8d9',
        backgroundColor: (context: any) => getGradient(context.chart.ctx, 0, 184, 217, 0.17),
        borderWidth: 2.2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.42,
        fill: true,
      },
      {
        label: 'Honda Vezel',
        data: CD[range].vezel,
        borderColor: '#0057ff',
        backgroundColor: (context: any) => getGradient(context.chart.ctx, 0, 87, 255, 0.12),
        borderWidth: 2.2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.42,
        fill: true,
      },
      {
        label: 'Suzuki Alto',
        data: CD[range].alto,
        borderColor: '#ff5e3a',
        backgroundColor: (context: any) => getGradient(context.chart.ctx, 255, 94, 58, 0.12),
        borderWidth: 2.2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.42,
        fill: true,
      },
      {
        label: 'Nissan Leaf',
        data: CD[range].leaf,
        borderColor: '#f5c842',
        backgroundColor: (context: any) => getGradient(context.chart.ctx, 245, 200, 66, 0.10),
        borderWidth: 2.2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.42,
        fill: true,
      },
      {
        label: 'Toyota Prius',
        data: CD[range].prius,
        borderColor: '#a855f7',
        backgroundColor: (context: any) => getGradient(context.chart.ctx, 168, 85, 247, 0.10),
        borderWidth: 2.2,
        pointRadius: 0,
        pointHoverRadius: 5,
        tension: 0.42,
        fill: true,
      },
    ],
  };

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
          label: (c: any) => ` ${c.dataset.label}: Rs. ${(c.parsed.y * 1000).toLocaleString()}`
        }
      },
    },
    scales: {
      x: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 } } },
      y: { grid: { color: tc.grid }, border: { color: tc.grid }, ticks: { color: tc.tick, font: { family: "'DM Mono',monospace", size: 10 }, callback: (v: any) => `Rs.${Math.round(v / 1000)}K` } }
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
            <p className="hero-sub">AutoSenseLK tracks 24,000+ ikman.lk listings across 55 brands in real time — using ML to instantly score every deal so you know exactly what any car is really worth.</p>
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
            <div className="sc"><div className="sc-label">Avg. Market Price</div><div className="sc-val">Rs. 8.42M</div><div className="sc-delta">↑ 3.2% this month</div></div>
            <div className="sc"><div className="sc-label">Listings Tracked</div><div className="sc-val">24,810</div><div className="sc-delta">Updated 8 mins ago</div></div>
            <div className="sc"><div className="sc-label">Best Deal Today</div><div className="sc-val" style={{ fontSize: '13px', color: 'var(--cyan)', lineHeight: 1.4 }}>Toyota Aqua 2016</div><div className="sc-delta">↓ 18% below market avg</div></div>
          </div>
        </div>
        
        <div className="hero-chart">
          <div className="cc">
            <div className="cc-head">
              <div><div className="cc-eye">AutoSenseLK · Market Overview</div><div className="cc-title">Average price trends — Top models 2024–2025</div></div>
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
              <div className="leg"><div className="ld" style={{ background: '#00b8d9' }}></div>Toyota Aqua</div>
              <div className="leg"><div className="ld" style={{ background: '#0057ff' }}></div>Honda Vezel</div>
              <div className="leg"><div className="ld" style={{ background: '#ff5e3a' }}></div>Suzuki Alto</div>
              <div className="leg"><div className="ld" style={{ background: '#f5c842' }}></div>Nissan Leaf</div>
              <div className="leg"><div className="ld" style={{ background: '#a855f7' }}></div>Toyota Prius</div>
              <div style={{ marginLeft: 'auto', fontFamily: "'DM Mono',monospace", fontSize: '10px', color: 'var(--mu)' }}>Rs. thousands</div>
            </div>
            <div className="cc-body">
              <Line data={chartData} options={chartOptions} />
            </div>
          </div>
        </div>
        
        <div className="ticker">
          <div className="tick-inner">
            {[...TICKERS, ...TICKERS].map((i, idx) => (
              <span className="tick-item" key={idx}>
                <span className="tm">{i.make}</span><span className="ts">·</span><span className="tp">{i.price}</span>
                <span className={i.up ? 'tu' : 'td-n'}>{i.delta}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className="strip">
        <div className="si"><div className="sv">4,210+</div><div className="sl">New listings / week</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">55</div><div className="sl">Brands tracked</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">300+</div><div className="sl">Models indexed</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv" style={{ color: 'var(--cyan)' }}>12.4%</div><div className="sl">Good deal listings</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">25</div><div className="sl">Districts covered</div></div>
        <div className="sdiv"></div>
        <div className="si"><div className="sv">6h</div><div className="sl">Scrape frequency</div></div>
      </div>

      <div className="feat-section">
        <div className="sec-eye">What AutoSenseLK does</div>
        <h2 className="sec-h">Everything to buy or sell smarter. <span className="muted">No guesswork.</span></h2>
        <div className="feat-grid">
          <div className="fc"><div className="fi ic-c">📊</div><div className="fn">Live price tracking</div><div className="fd">Scrapes ikman.lk every 6 hours. Average prices per make, model, and year — always current, never stale.</div></div>
          <div className="fc"><div className="fi ic-b">🤖</div><div className="fn">ML deal scoring</div><div className="fd">A regression model compares any listing against thousands of similar vehicles. Good deal, fair, or overpriced — in milliseconds.</div></div>
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
            <div className="step"><div className="step-n">01</div><div className="step-conn"></div><div className="step-t">We scrape</div><div className="step-d">55 brands × 300+ models × 3 conditions crawled via httpx and Playwright every 6 hours across all 25 districts.</div></div>
            <div className="step"><div className="step-n">02</div><div className="step-conn"></div><div className="step-t">We clean</div><div className="step-d">Prices normalised, duplicates removed via SHA-256 hashing, mileage units standardised, year validated.</div></div>
            <div className="step"><div className="step-n">03</div><div className="step-conn"></div><div className="step-t">We analyse</div><div className="step-d">4-level daily analytics: market-wide, per-brand, per-condition, and per-make × model × year × condition.</div></div>
            <div className="step"><div className="step-n">04</div><div className="step-conn"></div><div className="step-t">You decide</div><div className="step-d">Real-time dashboards and ML-scored deal quality give you the confidence to negotiate, buy, or walk away.</div></div>
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
