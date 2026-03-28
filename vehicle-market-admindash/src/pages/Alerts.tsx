import { useState } from 'react';

export function Alerts() {
  const [alerts, setAlerts] = useState([
    { id: 'ALT-8412', lvl: 'CRIT', rule: 'DB Connection Timeout', cur: '> 5000ms', thr: '5000ms', stat: 'ACTIVE', time: '12m ago', active: true },
    { id: 'ALT-8411', lvl: 'WARN', rule: 'Scraper Rate Limited', cur: '10/min', thr: '5/min', stat: 'ACK', time: '1h ago', active: true },
    { id: 'ALT-8410', lvl: 'WARN', rule: 'High Memory Worker', cur: '1.2GB', thr: '1.0GB', stat: 'RESOLVED', time: '4h ago', active: false },
    { id: 'ALT-8409', lvl: 'INFO', rule: 'API Spike Detected', cur: '240 req/s', thr: '100 req/s', stat: 'RESOLVED', time: '1d ago', active: false },
  ]);

  const toggleAck = (i: number) => {
    const newA = [...alerts];
    if (newA[i].stat === 'ACTIVE') newA[i].stat = 'ACK';
    else if (newA[i].stat === 'ACK') newA[i].stat = 'RESOLVED';
    else newA[i].stat = 'ACTIVE';
    setAlerts(newA);
  };

  return (
    <div className="page active view-fade-in">
      <div className="card">
        <div className="card-header">
          <div className="card-title">Configured Rules Triggered</div>
          <div className="card-badge cb-red">1 CRIT • 1 WARN</div>
        </div>
        <table className="logs-table">
          <thead>
            <tr>
              <th style={{width:'80px'}}>Alert ID</th>
              <th style={{width:'80px'}}>Severity</th>
              <th>Rule Name</th>
              <th>Current Val</th>
              <th>Threshold</th>
              <th style={{width:'100px'}}>Status</th>
              <th>Triggered</th>
              <th style={{width:'80px', textAlign:'center'}}>Action</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((a, i) => (
              <tr key={i} style={{opacity: a.active ? 1 : 0.6}}>
                <td style={{fontFamily:'monospace', color:'var(--mu)'}}>{a.id}</td>
                <td>
                  <span className={`pill ${a.lvl === 'CRIT' ? 'err' : a.lvl === 'WARN' ? 'warn' : 'ok'}`}>
                    {a.lvl}
                  </span>
                </td>
                <td style={{fontWeight:500, color: a.active ? 'var(--text)' : 'var(--mu)'}}>{a.rule}</td>
                <td style={{color: a.lvl === 'CRIT' && a.active ? 'var(--red)' : ''}}>{a.cur}</td>
                <td>{a.thr}</td>
                <td>
                  <div style={{
                    fontSize:'10px', fontWeight:700, padding:'2px 6px', borderRadius:'3px', textAlign:'center',
                    background: a.stat === 'ACTIVE' ? 'rgba(255,71,87,0.1)' : a.stat === 'ACK' ? 'rgba(245,200,66,0.1)' : 'rgba(0,208,132,0.1)',
                    color: a.stat === 'ACTIVE' ? 'var(--red)' : a.stat === 'ACK' ? 'var(--yellow)' : 'var(--green)'
                  }}>
                    {a.stat}
                  </div>
                </td>
                <td style={{color:'var(--mu)'}}>{a.time}</td>
                <td style={{textAlign:'center'}}>
                  <button 
                    onClick={() => toggleAck(i)}
                    style={{
                      background:'var(--border)', border:'none', color:'var(--text)', 
                      padding:'4px 8px', borderRadius:'3px', cursor:'pointer', fontSize:'11px'
                    }}>
                    {a.stat === 'RESOLVED' ? 'REOPEN' : 'ACK'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="grid-2 mt16">
        <div className="card">
          <div className="card-header">
            <div className="card-title">PagerDuty Schedule</div>
          </div>
          <div style={{padding:'0 16px 16px 16px'}}>
            <div style={{display:'flex', justifyContent:'space-between', padding:'12px 0', borderBottom:'1px solid var(--border)'}}>
              <span style={{color:'var(--mu)'}}>Primary On-Call</span>
              <span style={{fontWeight:500}}>DevOps Team A</span>
            </div>
            <div style={{display:'flex', justifyContent:'space-between', padding:'12px 0', borderBottom:'1px solid var(--border)'}}>
              <span style={{color:'var(--mu)'}}>Secondary</span>
              <span style={{fontWeight:500}}>Backend Team B</span>
            </div>
            <div style={{display:'flex', justifyContent:'space-between', padding:'12px 0', borderBottom:'1px solid var(--border)'}}>
              <span style={{color:'var(--mu)'}}>Escalation Policy</span>
              <span style={{fontWeight:500}}>15m -&gt; Eng Manager</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
