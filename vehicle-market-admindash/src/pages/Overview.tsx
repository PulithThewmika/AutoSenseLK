import { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import { sparkDs, sparkOpts, baseOpts, lineDs, last30Labels, genSeries, rand, randFloat } from '../utils/ChartHelpers';

export function Overview() {
  const [rpm, setRpm] = useState(184);
  const [resp, setResp] = useState(108);
  const [errRate, setErrRate] = useState(0.8);

  const sparkListingsRef = useRef<HTMLCanvasElement>(null);
  const sparkRpmRef = useRef<HTMLCanvasElement>(null);
  const sparkRespRef = useRef<HTMLCanvasElement>(null);
  const sparkErrRef = useRef<HTMLCanvasElement>(null);
  const overviewRpmRef = useRef<HTMLCanvasElement>(null);
  const overviewRespRef = useRef<HTMLCanvasElement>(null);

  const chartsRef = useRef<any>({});

  useEffect(() => {
    // Initialize Sparklines
    if (sparkListingsRef.current) {
      chartsRef.current.sparkListings = new Chart(sparkListingsRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs([380,390,412,401,420,438,445,430,450,460,482,412], '0,184,217')] },
        options: sparkOpts()
      });
    }
    if (sparkRpmRef.current) {
      chartsRef.current.sparkRpm = new Chart(sparkRpmRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs([140,155,168,172,165,180,184,190,178,184,192,184], '0,208,132')] },
        options: sparkOpts()
      });
    }
    if (sparkRespRef.current) {
      chartsRef.current.sparkResp = new Chart(sparkRespRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs([125,118,122,115,120,112,108,115,110,106,110,108], '245,200,66')] },
        options: sparkOpts()
      });
    }
    if (sparkErrRef.current) {
      chartsRef.current.sparkErr = new Chart(sparkErrRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs([0.4,0.5,0.6,0.4,0.5,0.7,0.6,0.9,1.0,0.8,0.8,0.8], '255,71,87')] },
        options: sparkOpts()
      });
    }

    // Main Charts
    const rpmLabels = last30Labels('m');
    const rpmData = genSeries(30, 160, 28);
    if (overviewRpmRef.current) {
      chartsRef.current.overviewRpm = new Chart(overviewRpmRef.current, {
        type: 'line',
        data: { labels: rpmLabels, datasets: [lineDs('Req/min', rpmData, '0,184,217', true)] },
        options: baseOpts((v: number) => `${v}/m`, false)
      });
    }

    const respData = genSeries(30, 110, 22);
    if (overviewRespRef.current) {
      chartsRef.current.overviewResp = new Chart(overviewRespRef.current, {
        type: 'line',
        data: { labels: rpmLabels, datasets: [lineDs('Avg ms', respData, '59,111,245', true)] },
        options: baseOpts((v: number) => `${v}ms`, false)
      });
    }

    // Interval for updates
    const timer = setInterval(() => {
      const newRpm = rand(160, 210);
      const newResp = rand(95, 130);
      const newErr = randFloat(0.4, 1.2);
      
      setRpm(newRpm);
      setResp(newResp);
      setErrRate(newErr);

      const pushPoint = (chart: Chart, val: number, max: number = 30) => {
        if (!chart) return;
        chart.data.datasets[0].data.push(val as never);
        if (chart.data.datasets[0].data.length > max) chart.data.datasets[0].data.shift();
        if (chart.data.labels && chart.data.labels.length > 0) {
          chart.data.labels.push('');
          if (chart.data.labels.length > max) chart.data.labels.shift();
        }
        chart.update('none');
      };

      pushPoint(chartsRef.current.sparkRpm, newRpm, 12);
      pushPoint(chartsRef.current.sparkResp, newResp, 12);
      pushPoint(chartsRef.current.sparkErr, newErr, 12);
      pushPoint(chartsRef.current.overviewRpm, newRpm);
      pushPoint(chartsRef.current.overviewResp, newResp);

    }, 2000);

    return () => {
      clearInterval(timer);
      Object.values(chartsRef.current).forEach((c: any) => c.destroy());
    };
  }, []);

  return (
    <div className="page active view-fade-in">
      <div className="grid-4">
        <div className="kpi">
          <div className="kpi-icon">🕷</div>
          <div className="kpi-label">Total Listings</div>
          <div className="kpi-val">24,810</div>
          <div className="kpi-delta up">↑ 412 today</div>
          <div className="kpi-spark"><canvas ref={sparkListingsRef}></canvas></div>
        </div>
        <div className="kpi">
          <div className="kpi-icon">⚡</div>
          <div className="kpi-label">API Req / min</div>
          <div className="kpi-val">{rpm}</div>
          <div className="kpi-delta up">↑ 22% vs avg</div>
          <div className="kpi-spark"><canvas ref={sparkRpmRef}></canvas></div>
        </div>
        <div className="kpi">
          <div className="kpi-icon">⏱</div>
          <div className="kpi-label">Avg Response</div>
          <div className="kpi-val">{resp}<span style={{fontSize:'14px',color:'var(--mu)'}}>ms</span></div>
          <div className="kpi-delta up">↓ 12ms better</div>
          <div className="kpi-spark"><canvas ref={sparkRespRef}></canvas></div>
        </div>
        <div className="kpi">
          <div className="kpi-icon">❌</div>
          <div className="kpi-label">Error Rate</div>
          <div className="kpi-val">{errRate.toFixed(1)}<span style={{fontSize:'14px',color:'var(--mu)'}}>%</span></div>
          <div className="kpi-delta dn">↑ 0.2% spike</div>
          <div className="kpi-spark"><canvas ref={sparkErrRef}></canvas></div>
        </div>
      </div>

      <div className="grid-2 mb16">
        <div className="card">
          <div className="card-header">
            <div className="card-title">Requests per minute</div>
            <div className="card-badge cb-cyan">LIVE</div>
          </div>
          <div style={{height:'160px'}}><canvas ref={overviewRpmRef}></canvas></div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-title">Response time trend</div>
            <div className="card-badge cb-blue">30 MIN</div>
          </div>
          <div style={{height:'160px'}}><canvas ref={overviewRespRef}></canvas></div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <div className="card-title">Service status</div>
            <div className="card-badge cb-green">ALL SYSTEMS</div>
          </div>
          <table className="status-table">
            <thead><tr><th>Service</th><th>Status</th><th>Uptime</th><th>Latency</th></tr></thead>
            <tbody>
              <tr><td>FastAPI</td><td><span className="pill ok">● Online</span></td><td>14d 6h</td><td>2ms</td></tr>
              <tr><td>MongoDB</td><td><span className="pill ok">● Connected</span></td><td>14d 6h</td><td>4ms</td></tr>
              <tr><td>Celery Worker</td><td><span className="pill ok">● Running</span></td><td>2d 18h</td><td>—</td></tr>
              <tr><td>Redis</td><td><span className="pill warn">⚠ High mem</span></td><td>14d 6h</td><td>1ms</td></tr>
              <tr><td>Playwright</td><td><span className="pill ok">● Ready</span></td><td>2d 18h</td><td>—</td></tr>
            </tbody>
          </table>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-title">Scraper pipeline</div>
            <div className="card-badge cb-green">LAST CYCLE</div>
          </div>
          <table className="status-table">
            <thead><tr><th>Stage</th><th>Status</th><th>Count</th><th>Duration</th></tr></thead>
            <tbody>
              <tr><td>Crawl</td><td><span className="pill ok">✓ Done</span></td><td>28,440</td><td>18m 42s</td></tr>
              <tr><td>Parse</td><td><span className="pill ok">✓ Done</span></td><td>28,219</td><td>4m 12s</td></tr>
              <tr><td>Clean</td><td><span className="pill ok">✓ Done</span></td><td>26,810</td><td>1m 08s</td></tr>
              <tr><td>Dedup</td><td><span className="pill ok">✓ Done</span></td><td>+412 new</td><td>23s</td></tr>
              <tr><td>Analytics</td><td><span className="pill ok">✓ Done</span></td><td>4 levels</td><td>2m 31s</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
