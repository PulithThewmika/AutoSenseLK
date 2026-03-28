import { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import { sparkDs, sparkOpts, baseOpts, lineDs, last30Labels,  } from '../utils/ChartHelpers';
import { getMarketSummary, getHealth, getScrapeStatus, triggerFullScrape, triggerBrandScrape, getAvailableBrands } from '../services/api'; 

export function Overview() {
  const rpm = 0;
  const resp = 0;
  const errRate = 0;

  const [marketStats, setMarketStats] = useState({ total_listings: 0, makes_count: 0, models_count: 0 });
  const [apiStatus, setApiStatus] = useState('Checking...');
  const [scrapeState, setScrapeState] = useState<any>({ cycle_status: 'no_runs_yet' });
  const [brands, setBrands] = useState<string[]>([]);
  const [selectedBrand, setSelectedBrand] = useState<string>('');
  const [triggering, setTriggering] = useState(false);

  const sparkListingsRef = useRef<HTMLCanvasElement>(null);
  const sparkRpmRef = useRef<HTMLCanvasElement>(null);
  const sparkRespRef = useRef<HTMLCanvasElement>(null);
  const sparkErrRef = useRef<HTMLCanvasElement>(null);
  const overviewRpmRef = useRef<HTMLCanvasElement>(null);
  const overviewRespRef = useRef<HTMLCanvasElement>(null);

  const chartsRef = useRef<any>({});

  const fetchData = async () => {
    try {
      const summary = await getMarketSummary();
      setMarketStats(summary || { total_listings: 0, makes_count: 0, models_count: 0 });
    } catch (e) {}

    try {
      await getHealth();
      setApiStatus('â— Online');
    } catch (e) {
      setApiStatus('Offline');
    }

    try {
      const status = await getScrapeStatus();
      if (status) setScrapeState(status);
    } catch (e) {}

    try {
      const brandsData = await getAvailableBrands();
      setBrands(brandsData.brands || []);
    } catch (e) {}
  };

  useEffect(() => {
    fetchData();
    const intervalData = setInterval(fetchData, 10000);

    // Initialize Sparklines (static empty or zeros for no mock data)
    if (sparkListingsRef.current) {
      chartsRef.current.sparkListings = new Chart(sparkListingsRef.current, {   
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs(Array(12).fill(0), '0,184,217')] },
        options: sparkOpts()
      });
    }
    if (sparkRpmRef.current) {
      chartsRef.current.sparkRpm = new Chart(sparkRpmRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs(Array(12).fill(0), '0,208,132')] },
        options: sparkOpts()
      });
    }
    if (sparkRespRef.current) {
      chartsRef.current.sparkResp = new Chart(sparkRespRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs(Array(12).fill(0), '245,200,66')] },
        options: sparkOpts()
      });
    }
    if (sparkErrRef.current) {
      chartsRef.current.sparkErr = new Chart(sparkErrRef.current, {
        type: 'line',
        data: { labels: Array(12).fill(''), datasets: [sparkDs(Array(12).fill(0), '255,71,87')] },
        options: sparkOpts()
      });
    }

    // Main Charts (static empty)
    const rpmLabels = last30Labels('m');
    if (overviewRpmRef.current) {
      chartsRef.current.overviewRpm = new Chart(overviewRpmRef.current, {       
        type: 'line',
        data: { labels: rpmLabels, datasets: [lineDs('Req/min', Array(30).fill(0), '0,184,217', true)] },
        options: baseOpts((v: number) => `${v}/m`, false)
      });
    }

    if (overviewRespRef.current) {
      chartsRef.current.overviewResp = new Chart(overviewRespRef.current, {     
        type: 'line',
        data: { labels: rpmLabels, datasets: [lineDs('Avg ms', Array(30).fill(0), '59,111,245', true)] },
        options: baseOpts((v: number) => `${v}ms`, false)
      });
    }

    return () => {
      clearInterval(intervalData);
      Object.values(chartsRef.current).forEach((c: any) => c.destroy());        
    };
  }, []);

  const handleFullScrape = async () => {
    if (triggering) return;
    setTriggering(true);
    try {
      await triggerFullScrape();
      await fetchData();
      alert('Full scrape cycle triggered successfully.');
    } catch (error) {
      alert('Failed to trigger full scrape');
    } finally {
      setTriggering(false);
    }
  };

  const handleBrandScrape = async () => {
    if (triggering || !selectedBrand) return;
    setTriggering(true);
    try {
      await triggerBrandScrape(selectedBrand);
      await fetchData();
      alert(`Scrape cycle for ${selectedBrand} triggered successfully.`);
    } catch (error) {
      alert(`Failed to trigger scrape for ${selectedBrand}`);
    } finally {
      setTriggering(false);
    }
  };

  return (
    <div className="page active view-fade-in">
      <div className="grid-4">
        <div className="kpi">
          <div className="kpi-icon">ðŸ•·</div>
          <div className="kpi-label">Total Listings</div>
          <div className="kpi-val">{marketStats.total_listings.toLocaleString()}</div>
          <div className="kpi-delta up">{marketStats.makes_count} makes / {marketStats.models_count} models</div>
          <div className="kpi-spark"><canvas ref={sparkListingsRef}></canvas></div>
        </div>
        <div className="kpi">
          <div className="kpi-icon">âš¡</div>
          <div className="kpi-label">API Req / min</div>
          <div className="kpi-val">{rpm}</div>
          <div className="kpi-delta up">â†‘ 0% vs avg</div>
          <div className="kpi-spark"><canvas ref={sparkRpmRef}></canvas></div>  
        </div>
        <div className="kpi">
          <div className="kpi-icon">â±</div>
          <div className="kpi-label">Avg Response</div>
          <div className="kpi-val">{resp}<span style={{fontSize:'14px',color:'var(--mu)'}}>ms</span></div>
          <div className="kpi-delta up">â†“ 0ms better</div>
          <div className="kpi-spark"><canvas ref={sparkRespRef}></canvas></div> 
        </div>
        <div className="kpi">
          <div className="kpi-icon">âŒ</div>
          <div className="kpi-label">Error Rate</div>
          <div className="kpi-val">{errRate.toFixed(1)}<span style={{fontSize:'14px',color:'var(--mu)'}}>%</span></div>
          <div className="kpi-delta dn">0.0% spike</div>
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

      <div className="grid-3">
        <div className="card">
          <div className="card-header">
            <div className="card-title">Service status</div>
            <div className="card-badge cb-green">ALL SYSTEMS</div>
          </div>
          <table className="status-table">
            <thead><tr><th>Service</th><th>Status</th><th>Uptime</th><th>Latency</th></tr></thead>
            <tbody>
              <tr><td>FastAPI</td><td><span className={`pill ${apiStatus === 'â— Online' ? 'ok' : 'err'}`}>{apiStatus}</span></td><td>-</td><td>-</td></tr>   
              <tr><td>MongoDB</td><td><span className="pill ok">â— Connected</span></td><td>-</td><td>-</td></tr>
              <tr><td>Celery Worker</td><td><span className="pill ok">â— Running</span></td><td>-</td><td>-</td></tr>
              <tr><td>Redis</td><td><span className="pill ok">â— Normal</span></td><td>-</td><td>-</td></tr>
              <tr><td>Playwright</td><td><span className="pill ok">â— Ready</span></td><td>-</td><td>-</td></tr>
            </tbody>
          </table>
        </div>
        
        <div className="card">
          <div className="card-header">
            <div className="card-title">Scraper Controls</div>
            <div className="card-badge cb-cyan">OPERATIONS</div>
          </div>
          <div className="card-body" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <button 
              className="btn btn-primary" 
              onClick={handleFullScrape} 
              disabled={triggering}
              style={{ padding: '8px 16px', background: 'var(--brand)', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            >
              {triggering ? 'Triggering...' : 'Trigger Full Scrape Cycle'}
            </button>
            
            <div style={{ display: 'flex', gap: '10px' }}>
              <select 
                 value={selectedBrand} 
                 onChange={e => setSelectedBrand(e.target.value)}
                 style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid var(--border)', backgroundColor: 'var(--bg)', color: 'var(--fg)' }}
              >
                 <option value="">Select a Brand</option>
                 {brands.map(b => (
                   <option key={b} value={b}>{b}</option>
                 ))}
              </select>
              <button 
                 className="btn btn-secondary" 
                 onClick={handleBrandScrape}
                 disabled={triggering || !selectedBrand}
                 style={{ padding: '8px 16px', background: 'var(--panel)', border: '1px solid var(--border)', color: 'var(--fg)', borderRadius: '4px', cursor: 'pointer' }}
              >
                 Scrape Brand
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-title">Scraper pipeline</div>
            <div className="card-badge cb-green">LAST CYCLE</div>
          </div>
          <table className="status-table">
            <thead><tr><th>Stage</th><th>Target</th><th>Error / Output</th></tr></thead>
            <tbody>
              {scrapeState.status !== 'no_runs_yet' ? (
              <tr>
                <td><span className={`pill ${scrapeState.status === 'running' || scrapeState.status === 'success' ? 'ok' : 'err'}`}>{scrapeState.status}</span></td>
                <td>{scrapeState.brand || scrapeState.type || 'All'}</td>
                <td style={{ maxWidth: '100px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={scrapeState.error || scrapeState.message || 'None'}>
                  {scrapeState.error || scrapeState.message || 'None'}
                </td>
              </tr>
              ) : (
                <tr><td colSpan={3} style={{ textAlign: 'center', padding: '10px' }}>No recent runs</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
