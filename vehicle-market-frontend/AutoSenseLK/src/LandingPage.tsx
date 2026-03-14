import { useEffect, useRef, useState, useCallback } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import type { ChartOptions, ChartData } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip);

/* ── Chart data per range ─────────────────────────── */
const RANGES = {
    '6m': {
        labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        aqua: [6800, 6950, 7100, 7050, 7300, 7420, 7350, 7500, 7420, 7550, 7600, 7680],
        vezel: [9200, 9400, 9500, 9350, 9600, 9750, 9700, 9800, 9900, 9850, 10100, 10200],
        alto: [3800, 3900, 3850, 3950, 4100, 4050, 4200, 4150, 4300, 4250, 4400, 4350],
        leaf: [5200, 5400, 5300, 5500, 5600, 5700, 5650, 5800, 5750, 5900, 5950, 6100],
    },
    '1y': {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        aqua: [6200, 6350, 6400, 6500, 6600, 6700, 6800, 6950, 7100, 7050, 7300, 7420, 7350, 7500, 7420, 7550, 7600, 7680],
        vezel: [8500, 8700, 8800, 8900, 9000, 9100, 9200, 9400, 9500, 9350, 9600, 9750, 9700, 9800, 9900, 9850, 10100, 10200],
        alto: [3400, 3500, 3550, 3600, 3650, 3700, 3800, 3900, 3850, 3950, 4100, 4050, 4200, 4150, 4300, 4250, 4400, 4350],
        leaf: [4600, 4800, 4900, 5000, 5100, 5200, 5200, 5400, 5300, 5500, 5600, 5700, 5650, 5800, 5750, 5900, 5950, 6100],
    },
    all: {
        labels: ['2022 Q1', 'Q2', 'Q3', 'Q4', '2023 Q1', 'Q2', 'Q3', 'Q4', '2024 Q1', 'Q2', 'Q3', 'Q4'],
        aqua: [5800, 6000, 6200, 6400, 6600, 6900, 7100, 7300, 7420, 7550, 7650, 7680],
        vezel: [7800, 8100, 8400, 8700, 9000, 9300, 9500, 9700, 9900, 10050, 10150, 10200],
        alto: [3000, 3100, 3200, 3400, 3550, 3700, 3850, 4000, 4100, 4250, 4350, 4350],
        leaf: [3800, 4100, 4400, 4700, 5000, 5200, 5400, 5600, 5750, 5900, 6000, 6100],
    },
} as const;

type RangeKey = keyof typeof RANGES;

function makeGradient(ctx: CanvasRenderingContext2D, h: number, r: number, g: number, b: number, a: number) {
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, `rgba(${r},${g},${b},${a})`);
    grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
    return grad;
}

function buildChartData(range: RangeKey, ctx?: CanvasRenderingContext2D | null, h = 280): ChartData<'line'> {
    const d = RANGES[range];
    const base = { borderWidth: 2.2, pointRadius: 0, pointHoverRadius: 5, tension: 0.44, fill: true };
    const bg = (r: number, g: number, b: number, a: number) => ctx ? makeGradient(ctx, h, r, g, b, a) : `rgba(${r},${g},${b},${a})`;
    return {
        labels: [...d.labels],
        datasets: [
            { label: 'Toyota Aqua', data: [...d.aqua], borderColor: 'rgb(0,184,217)', backgroundColor: bg(0, 184, 217, 0.18), ...base },
            { label: 'Honda Vezel', data: [...d.vezel], borderColor: 'rgb(0,87,255)', backgroundColor: bg(0, 87, 255, 0.13), ...base },
            { label: 'Suzuki Alto', data: [...d.alto], borderColor: 'rgb(255,94,58)', backgroundColor: bg(255, 94, 58, 0.13), ...base },
            { label: 'Nissan Leaf', data: [...d.leaf], borderColor: 'rgb(245,200,66)', backgroundColor: bg(245, 200, 66, 0.11), ...base },
        ],
    };
}

const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index' as const, intersect: false },
    plugins: {
        legend: { display: false },
        tooltip: {
            backgroundColor: '#18212f',
            borderColor: 'rgba(255,255,255,0.09)',
            borderWidth: 1,
            titleColor: '#64788f',
            bodyColor: '#e6ecf4',
            padding: 13,
            titleFont: { family: "'DM Mono',monospace", size: 11 },
            bodyFont: { family: "'DM Sans',sans-serif", size: 13 },
            callbacks: { label: (c) => ` ${c.dataset.label}: Rs. ${((c.parsed.y) * 1000).toLocaleString()}` },
        },
    },
    scales: {
        x: { grid: { color: 'rgba(255,255,255,0.03)' }, border: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#2e3d50', font: { family: "'DM Mono',monospace", size: 11 } } },
        y: { grid: { color: 'rgba(255,255,255,0.03)' }, border: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#2e3d50', font: { family: "'DM Mono',monospace", size: 11 }, callback: (v) => `Rs.${(Number(v) / 1000).toFixed(0)}K` } },
    },
};

/* ── Ticker data ──────────────────────────────────── */
const TICKER = [
    { make: 'Toyota Aqua 2016', price: 'Rs. 7,680,000', delta: '+2.1%', up: true },
    { make: 'Honda Vezel 2015', price: 'Rs. 10,200,000', delta: '+1.8%', up: true },
    { make: 'Suzuki Alto 2020', price: 'Rs. 4,350,000', delta: '-0.5%', up: false },
    { make: 'Nissan Leaf 2017', price: 'Rs. 6,100,000', delta: '+3.4%', up: true },
    { make: 'Toyota Prius 2014', price: 'Rs. 8,900,000', delta: '+0.9%', up: true },
    { make: 'Honda Fit 2013', price: 'Rs. 5,200,000', delta: '-1.2%', up: false },
    { make: 'Mazda Demio 2015', price: 'Rs. 5,750,000', delta: '+1.5%', up: true },
    { make: 'Toyota Vitz 2012', price: 'Rs. 4,800,000', delta: '-0.8%', up: false },
    { make: 'Perodua Axia 2019', price: 'Rs. 3,900,000', delta: '+2.6%', up: true },
    { make: 'Mitsubishi Attrage', price: 'Rs. 6,450,000', delta: '+1.1%', up: true },
];
const tickerItems = [...TICKER, ...TICKER];


export default function LandingPage() {
    const [range, setRange] = useState<RangeKey>('6m');
    const chartRef = useRef<ChartJS<'line'>>(null);
    const barRef = useRef<HTMLDivElement>(null);

    /* Reveal-on-scroll observer */
    useEffect(() => {
        const obs = new IntersectionObserver(
            (entries) => entries.forEach((e) => { if (e.isIntersecting) e.target.classList.add('visible'); }),
            { threshold: 0.08 },
        );
        document.querySelectorAll('.reveal').forEach((el) => obs.observe(el));
        return () => obs.disconnect();
    }, []);

    /* Deal bar animation */
    useEffect(() => {
        const t = setTimeout(() => { if (barRef.current) barRef.current.style.width = '38%'; }, 900);
        return () => clearTimeout(t);
    }, []);

    const getChartData = useCallback(() => {
        const ctx = chartRef.current?.ctx ?? null;
        const h = chartRef.current?.height ?? 280;
        return buildChartData(range, ctx, h);
    }, [range]);

    return (
        <>
            {/* ── NAV ──────────────────────────────────────── */}
            <nav>
                <div className="nav-logo">AutoSense<span className="nav-lk">LK</span></div>
                <ul className="nav-links">
                    <li><a href="#">Market</a></li>
                    <li><a href="#">Compare</a></li>
                    <li><a href="#">Trends</a></li>
                    <li><a href="#">Alerts</a></li>
                    <li><a href="#">About</a></li>
                </ul>
                <div className="nav-cta">
                    <button className="btn-ghost">Sign in</button>
                    <button className="btn-nav">Get started</button>
                </div>
            </nav>

            {/* ── HERO ─────────────────────────────────────── */}
            <section className="hero">
                <div className="orb orb1" />
                <div className="orb orb2" />
                <div className="orb orb3" />

                <div className="hero-top">
                    <div className="hero-text">
                        <div className="hero-tag"><span className="tag-dot" />Live · Sri Lanka Vehicle Market</div>
                        <h1>Sense the<br /><em>true price</em><br />of any car.</h1>
                        <p className="hero-sub">
                            AutoSenseLK tracks tens of thousands of vehicle listings across Sri Lanka — powered by ML to tell you instantly whether a deal is fair, overpriced, or a hidden gem.
                        </p>
                        <div className="hero-actions">
                            <button className="btn-main">
                                Explore market
                                <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" /></svg>
                            </button>
                            <button className="btn-outline">Check a listing</button>
                        </div>
                    </div>

                    <div className="hero-stats">
                        <div className="stat-card">
                            <div className="s-label">Avg. Market Price</div>
                            <div className="s-value">Rs. 8.4M</div>
                            <div className="s-delta">↑ 3.2% this month</div>
                        </div>
                        <div className="stat-card">
                            <div className="s-label">Listings Tracked</div>
                            <div className="s-value">24,810</div>
                            <div className="s-delta">Updated 8 mins ago</div>
                        </div>
                        <div className="stat-card">
                            <div className="s-label">Best Deal Today</div>
                            <div className="s-value" style={{ fontSize: 15, color: 'var(--accent)', lineHeight: 1.4 }}>Toyota Aqua 2016</div>
                            <div className="s-delta">↓ 18% below market avg</div>
                        </div>
                    </div>
                </div>

                {/* ── CHART ────────────────────────────────────── */}
                <div className="chart-wrap">
                    <div className="chart-card">
                        <div className="chart-head">
                            <div>
                                <div className="chart-eyebrow">AutoSenseLK · Market Overview</div>
                                <div className="chart-title-t">Average price trends — Top models 2024–2025</div>
                            </div>
                            <div className="chart-meta">
                                <div className="chart-live">Last updated: <span>just now</span></div>
                                <div className="tabs">
                                    {(['6m', '1y', 'all'] as RangeKey[]).map((r) => (
                                        <button key={r} className={`tab ${range === r ? 'active' : ''}`} onClick={() => setRange(r)}>
                                            {r === '6m' ? '6M' : r === '1y' ? '1Y' : 'All'}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="chart-legend">
                            <div className="leg"><div className="leg-dot" style={{ background: '#00b8d9' }} />Toyota Aqua</div>
                            <div className="leg"><div className="leg-dot" style={{ background: '#0057ff' }} />Honda Vezel</div>
                            <div className="leg"><div className="leg-dot" style={{ background: '#ff5e3a' }} />Suzuki Alto</div>
                            <div className="leg"><div className="leg-dot" style={{ background: '#f5c842' }} />Nissan Leaf</div>
                            <div style={{ marginLeft: 'auto', fontFamily: "'DM Mono',monospace", fontSize: 10, color: 'var(--muted)' }}>Values in Rs. thousands</div>
                        </div>
                        <div className="chart-body">
                            <Line ref={chartRef} data={getChartData()} options={chartOptions} />
                        </div>
                    </div>
                </div>

                {/* ── TICKER ───────────────────────────────────── */}
                <div className="ticker">
                    <div className="ticker-inner">
                        {tickerItems.map((item, i) => (
                            <span className="t-item" key={i}>
                                <span className="t-make">{item.make}</span>
                                <span className="t-sep">·</span>
                                <span className="t-price">{item.price}</span>
                                <span className={`t-delta ${item.up ? 't-up' : 't-dn'}`}>{item.delta}</span>
                            </span>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── STRIP ────────────────────────────────────── */}
            <div className="strip reveal">
                <div className="strip-stat"><div className="sv">4,210+</div><div className="sl">New listings / week</div></div>
                <div className="sdiv" />
                <div className="strip-stat"><div className="sv">38</div><div className="sl">Makes tracked</div></div>
                <div className="sdiv" />
                <div className="strip-stat"><div className="sv">Rs. 4.1M</div><div className="sl">Median price</div></div>
                <div className="sdiv" />
                <div className="strip-stat"><div className="sv" style={{ color: 'var(--accent)' }}>12.4%</div><div className="sl">Listings = good deals</div></div>
                <div className="sdiv" />
                <div className="strip-stat"><div className="sv">25</div><div className="sl">Districts covered</div></div>
                <div className="sdiv" />
                <div className="strip-stat"><div className="sv">6h</div><div className="sl">Scrape frequency</div></div>
            </div>

            {/* ── FEATURES ─────────────────────────────────── */}
            <section className="features">
                <div className="sec-label">What AutoSenseLK does</div>
                <h2 className="sec-h">Everything you need to buy or sell smarter. <span>No guesswork.</span></h2>
                <div className="feat-grid reveal">
                    <div className="feat-card"><div className="feat-icon ic-c">📊</div><div className="feat-name">Live price tracking</div><div className="feat-desc">Scrapes ikman.lk every 6 hours. Average prices per make, model, and year — always current, never stale.</div></div>
                    <div className="feat-card"><div className="feat-icon ic-b">🤖</div><div className="feat-name">ML deal scoring</div><div className="feat-desc">Our regression model compares any listing against thousands of similar vehicles. Good deal, fair, or overpriced — in milliseconds.</div></div>
                    <div className="feat-card"><div className="feat-icon ic-o">📈</div><div className="feat-name">Price trend charts</div><div className="feat-desc">Monthly historical averages for every popular model. See if the market is rising, cooling, or holding steady before you commit.</div></div>
                    <div className="feat-card"><div className="feat-icon ic-y">🔔</div><div className="feat-name">Price alerts</div><div className="feat-desc">Set a target price for any model. Get notified the moment a listing drops below your threshold — never miss a deal again.</div></div>
                    <div className="feat-card"><div className="feat-icon ic-p">🗺️</div><div className="feat-name">Location insights</div><div className="feat-desc">Prices vary by district. Colombo vs Kandy vs Galle — see exactly where the best deals are geographically concentrated.</div></div>
                    <div className="feat-card"><div className="feat-icon ic-g">⚖️</div><div className="feat-name">Model comparison</div><div className="feat-desc">Side-by-side price history, depreciation rate, and deal frequency for any two models. Make an informed choice, not a hopeful one.</div></div>
                </div>
            </section>

            {/* ── DEAL PREVIEW ─────────────────────────────── */}
            <section className="deal-sec">
                <div className="reveal">
                    <div className="sec-label">Deal Intelligence</div>
                    <h2 className="sec-h" style={{ marginBottom: 18 }}>Know in seconds if a listing is worth your time.</h2>
                    <p className="deal-desc">Paste any ikman.lk vehicle URL and AutoSenseLK scores it instantly against our market model — showing the actual fair price, how this listing compares, and a clear verdict on whether to make an offer.</p>
                    <button className="btn-main" style={{ fontSize: 14, padding: '12px 24px' }}>Try it on a listing →</button>
                </div>
                <div className="deal-card reveal">
                    <div className="deal-head">
                        <div>
                            <div className="deal-name">Toyota Aqua S</div>
                            <div className="deal-sub">2016 · 68,000 km · Petrol Hybrid · Colombo 07</div>
                        </div>
                        <div className="deal-badge db-g">Good deal</div>
                    </div>
                    <div className="deal-prices">
                        <div className="dp"><div className="dpl">Listed price</div><div className="dpv" style={{ color: 'var(--text)' }}>Rs. 6,750,000</div></div>
                        <div className="dp"><div className="dpl">Market average</div><div className="dpv" style={{ color: 'var(--accent)' }}>Rs. 7,420,000</div></div>
                    </div>
                    <div className="bar-labels"><span>Cheap end</span><span>▲ This listing</span><span>Expensive</span></div>
                    <div className="bar-track"><div className="bar-fill" ref={barRef} /></div>
                    <div className="deal-meta">
                        <div className="dm"><div className="dml">Saving vs market</div><div className="dmv" style={{ color: 'var(--accent)' }}>Rs. 670,000</div></div>
                        <div className="dm"><div className="dml">Below avg by</div><div className="dmv" style={{ color: 'var(--accent)' }}>9.0%</div></div>
                        <div className="dm"><div className="dml">Similar listings</div><div className="dmv">34</div></div>
                    </div>
                </div>
            </section>

            {/* ── HOW IT WORKS ─────────────────────────────── */}
            <section className="how-sec reveal">
                <div className="sec-label">How it works</div>
                <h2 className="sec-h">From raw listings to real market intelligence.</h2>
                <div className="steps">
                    <div className="step"><div className="step-n">01</div><div className="step-c" /><div className="step-name">We scrape</div><div className="step-desc">Thousands of listings collected from ikman.lk every 6 hours — automatically, across all 25 districts.</div></div>
                    <div className="step"><div className="step-n">02</div><div className="step-c" /><div className="step-name">We clean</div><div className="step-desc">Prices normalised, duplicates removed, mileage standardised. Only verified data enters the model.</div></div>
                    <div className="step"><div className="step-n">03</div><div className="step-c" /><div className="step-name">We analyse</div><div className="step-desc">ML calculates the fair market price for every make, model, year, and mileage combination in Sri Lanka.</div></div>
                    <div className="step"><div className="step-n">04</div><div className="step-c" /><div className="step-name">You decide</div><div className="step-desc">Clear dashboards and instant deal scores give you the confidence to negotiate hard, buy smart, or walk away.</div></div>
                </div>
            </section>

            {/* ── CTA ──────────────────────────────────────── */}
            <section className="cta-sec reveal">
                <h2>Stop guessing.<br />Start sensing.</h2>
                <p className="cta-sub">Join buyers and sellers using AutoSenseLK to navigate the Sri Lankan vehicle market with real data.</p>
                <div className="cta-actions">
                    <button className="btn-main" style={{ fontSize: 14, padding: '13px 28px' }}>Explore the market free →</button>
                    <button className="btn-outline" style={{ fontSize: 14, padding: '13px 28px' }}>View live dashboard</button>
                </div>
            </section>

            {/* ── FOOTER ───────────────────────────────────── */}
            <footer>
                <div className="foot-logo">AutoSense<span className="foot-lk">LK</span></div>
                <div className="foot-links">
                    <a href="#">Market</a><a href="#">Compare</a><a href="#">Trends</a><a href="#">API</a><a href="#">Privacy</a>
                </div>
                <div className="foot-copy">© 2025 AutoSenseLK · Sri Lanka Vehicle Intelligence</div>
            </footer>
        </>
    );
}
