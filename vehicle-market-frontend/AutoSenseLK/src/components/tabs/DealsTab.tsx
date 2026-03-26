import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { getMakes, getModels, getAvgPrice, getTrends } from '../../services/api';

interface DealsTabProps {
  isDark: boolean;
}

export function DealsTab({ isDark }: DealsTabProps) {
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [price, setPrice] = useState('');

  const [makesList, setMakesList] = useState<string[]>([]);
  const [modelsList, setModelsList] = useState<string[]>([]);
  const [recentScores, setRecentScores] = useState<any[]>([]);
  const [currentResult, setCurrentResult] = useState<any | null>(null);

  useEffect(() => {
    getMakes().then(res => {
      // API returns { makes: [{ name: "Toyota", slug: "toyota" }, ...], total: 56 }
      if (res && res.makes) {
        setMakesList(res.makes.map((m: any) => m.name));
      }
    }).catch(console.error);
  }, []);

  useEffect(() => {
    if (make) {
      // Find slug for make (API expects slug usually, or we pass the string)
      getModels(make.toLowerCase()).then(res => {
         if(res && res.models) {
           setModelsList(res.models.map((m: any) => m.name));
         } else {
           setModelsList([]);
         }
      }).catch(() => setModelsList([]));
    } else {
      setModelsList([]);
    }
    setModel('');
  }, [make]);

  const handleScore = async () => {
    const y = parseInt(year) || 0;
    const p = parseInt(price) || 0;

    if (!make) { alert('Please select a make.'); return; }
    if (!model) { alert('Please select a model.'); return; }
    if (y < 2000 || y > 2025) { alert('Please enter a valid year (2000–2025).'); return; }
    if (p < 100000) { alert('Please enter a valid listed price (Rs.).'); return; }

    try {
      const avgRes = await getAvgPrice(make, model);
      if (!avgRes || !avgRes.avg_price) {
        alert('Not enough market data to score this model currently.');
        return;
      }

      const mAvg = avgRes.avg_price;
      const sampleCount = avgRes.sample_count || 10;
      const ratio = p / mAvg;

      let label, cls, col;
      if (ratio < 0.85) { label = 'Good deal'; cls = 'db-g'; col = 'var(--green)'; }
      else if (ratio <= 1.15) { label = 'Fair price'; cls = 'db-f'; col = 'var(--yellow)'; }
      else { label = 'Overpriced'; cls = 'db-o'; col = 'var(--orange)'; }

      const diff = Math.abs(mAvg - p);
      const pct = Math.abs((ratio - 1) * 100).toFixed(1);
      const barW = Math.min(90, Math.max(8, ratio * 55));

      const trendsRes = await getTrends(make, model, 12).catch(() => null);
      let hist = [6800, 6950, 7100, 7050, 7300, 7420, 7350, 7500, 7420, 7550, 7600, 7680];
      if (trendsRes && trendsRes.history) {
        const sortedKeys = Object.keys(trendsRes.history).sort();
        hist = sortedKeys.map(k => trendsRes.history[k] / 1000); // Scale down to K
      }
      
      const result = {
        make, model, year: y, price: p, label, cls, col, mAvg, diff, pct, barW, ratio, hist, sampleCount
      };

      setCurrentResult(result);
      setRecentScores(prev => {
        const updated = [{ make, model, year: y, price: p, label, cls }, ...prev];
        return updated.slice(0, 4);
      });

      setTimeout(() => {
        document.getElementById('dealCard')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 50);

    } catch (err) {
      alert('Error fetching market average. Please try again.');
    }
  };

  const chartOpts: any = {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { enabled: false } },
    scales: { x: { display: false }, y: { display: false } }
  };

  let currentHist = [6800, 6950, 7100, 7050, 7300, 7420, 7350, 7500, 7420, 7550, 7600, 7680];
  let currentPriceHist = Array(12).fill(6750);
  let chartLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  
  if (currentResult) {
    currentHist = currentResult.hist;
    if (currentHist.length > 0) {
      currentPriceHist = Array(currentHist.length).fill(currentResult.price / 1000);
      chartLabels = Array(currentHist.length).fill('');
    }
  }

  const chartData = {
    labels: chartLabels,
    datasets: [
      {
        data: currentHist,
        borderColor: 'rgba(0,184,217,0.9)', backgroundColor: 'rgba(0,184,217,0.07)',
        borderWidth: 1.8, pointRadius: 0, tension: 0.44, fill: true
      },
      {
        data: currentPriceHist,
        borderColor: 'rgba(255,94,58,0.7)', borderDash: [5, 4],
        borderWidth: 1.5, pointRadius: 0, tension: 0, fill: false
      }
    ]
  };

  return (
    <div className="tab-panel active" id="panel-deals">
      <div className="deal-pad">
        <div className="sec-eye">Deal Intelligence</div>
        <h2 className="sec-h">Know in seconds if a listing is worth it.</h2>
        
        <div className="deal-layout">
          <div className="deal-form-card">
            <div className="score-legend">
              <div className="sl-item">
                <div className="dbadge db-g">Good deal</div>
                <div className="sl-text">Listed <strong style={{ color: 'var(--green)' }}>&gt;15% below</strong> market avg for same make/model</div>
              </div>
              <div className="sl-item">
                <div className="dbadge db-f">Fair price</div>
                <div className="sl-text">Within <strong style={{ color: 'var(--yellow)' }}>±15%</strong> of rolling market average</div>
              </div>
              <div className="sl-item">
                <div className="dbadge db-o">Overpriced</div>
                <div className="sl-text">Listed <strong style={{ color: 'var(--orange)' }}>&gt;15% above</strong> market avg for same make/model</div>
              </div>
            </div>

            <div className="score-form-title">Enter listing details</div>
            <div className="score-row">
              <select className="score-input" value={make} onChange={e => setMake(e.target.value)}>
                <option value="">Select Make</option>
                {makesList.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
              <select className="score-input" value={model} onChange={e => setModel(e.target.value)} disabled={!make}>
                <option value="">Select Model</option>
                {modelsList.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
            <div className="score-row">
              <input type="number" className="score-input" placeholder="Year (2000–2025)" min="2000" max="2025" value={year} onChange={e => setYear(e.target.value)} />
              <input type="number" className="score-input" placeholder="Listed price (Rs.)" value={price} onChange={e => setPrice(e.target.value)} />
            </div>
            <button className="score-btn" onClick={handleScore}>Score this listing →</button>

            <div className="recent-scores">
              <div className="rs-title">Recently scored</div>
              <div className="rs-list">
                {recentScores.length === 0 ? (
                  <div className="rs-empty">No scores yet. Try the scorer above.</div>
                ) : (
                  recentScores.map((s, i) => (
                    <div key={i} className="rs-item">
                      <div>
                        <div className="rs-name">{s.make} {s.model}</div>
                        <div className="rs-meta">{s.year} · Rs. {s.price.toLocaleString()}</div>
                      </div>
                      <div className={`dbadge ${s.cls}`}>{s.label}</div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="deal-result-card" id="dealCard" style={{ opacity: currentResult ? 1 : 0.4, pointerEvents: currentResult ? 'auto' : 'none' }}>
            {currentResult ? (
              <>
                <div className="dh">
                  <div>
                    <div className="dn">{currentResult.make} {currentResult.model}</div>
                    <div className="dm-meta">{currentResult.year} · Used · Sri Lanka</div>
                  </div>
                  <div className={`dbadge ${currentResult.cls}`}>{currentResult.label}</div>
                </div>
                <div className="deal-prices">
                  <div className="dp"><div className="dp-l">Listed price</div><div className="dp-v" style={{ color: 'var(--tx)' }}>Rs. {currentResult.price.toLocaleString()}</div></div>
                  <div className="dp"><div className="dp-l">Market average</div><div className="dp-v" style={{ color: 'var(--cyan)' }}>Rs. {currentResult.mAvg.toLocaleString()}</div></div>
                </div>
                <div className="bar-lbls"><span>Cheap end</span><span>▲ Listing</span><span>Expensive</span></div>
                <div className="bar-track"><div className="bar-fill" style={{ width: `${currentResult.barW}%` }}></div></div>
                <div className="deal-stats">
                  <div className="ds">
                    <div className="ds-l">Saving vs market</div>
                    <div className="ds-v" style={{ color: currentResult.col }}>
                      {currentResult.ratio < 1 ? '' : '+'}Rs. {currentResult.diff.toLocaleString()}
                    </div>
                  </div>
                  <div className="ds">
                    <div className="ds-l">Difference</div>
                    <div className="ds-v" style={{ color: currentResult.col }}>
                      {currentResult.ratio < 1 ? '−' : '+'}{currentResult.pct}%
                    </div>
                  </div>
                  <div className="ds"><div className="ds-l">Similar listings</div><div className="ds-v">{currentResult.sampleCount}</div></div>
                </div>
                <div className="mini-chart-wrap">
                  <div className="mini-chart-title">12-month history · {currentResult.make} {currentResult.model}</div>
                  <div className="mini-chart-h"><Line data={chartData} options={chartOpts} /></div>
                </div>
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--mu)', fontSize: 14 }}>
                Fill out the form to see deal intelligence results here.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
