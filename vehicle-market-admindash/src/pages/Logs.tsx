import React, { useState } from 'react';

export function Logs() {
  const [logs] = useState([
    { ts: "13:24:02", lvl: "ERR", sys: "Backend", msg: "Timeout connecting to secondary node at 10.4.22.4", badge: "err" },
    { ts: "13:23:41", lvl: "WRN", sys: "Scraper", msg: "Rate limit detected from riyasewana. Backing off 60s.", badge: "warn" },
    { ts: "13:21:05", lvl: "INF", sys: "Worker", msg: "Task 'train_predictive_model' completed in 184s", badge: "ok" },
    { ts: "13:19:12", lvl: "INF", sys: "API", msg: "New admin session started via OAuth2", badge: "ok" },
    { ts: "13:18:44", lvl: "ERR", sys: "Scraper", msg: "Failed to parse listing id=8812 - Missing price node", badge: "err" },
    { ts: "13:15:00", lvl: "INF", sys: "Cron", msg: "Scheduled 'db-backup-daily' triggered", badge: "ok" },
    { ts: "13:10:22", lvl: "WRN", sys: "API", msg: "High traffic: 284 req/s on /deals/recommended", badge: "warn" },
    { ts: "13:08:15", lvl: "INF", sys: "Worker", msg: "Scraped 1,440 items from autolanka page 12", badge: "ok" },
    { ts: "13:05:01", lvl: "INF", sys: "System", msg: "Memory optimized. Recovered 412MB", badge: "ok" },
    { ts: "13:02:18", lvl: "INF", sys: "API", msg: "User agent blocked - detected bot signature", badge: "ok" },
  ]);

  return (
    <div className="page active view-fade-in">
      <div className="card">
        <div className="card-header">
          <div className="card-title">Realtime System Stream</div>
          <div className="card-badge cb-green">TAIL • 100</div>
        </div>
        
        <table className="logs-table mb16">
          <thead>
            <tr>
              <th style={{width: '90px'}}>Time</th>
              <th style={{width: '60px'}}>Lvl</th>
              <th style={{width: '100px'}}>System</th>
              <th>Message</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((L, i) => (
              <tr key={i}>
                <td style={{color: 'var(--mu)', fontFamily: 'monospace'}}>{L.ts}</td>
                <td><span className={`pill ${L.badge}`}>{L.lvl}</span></td>
                <td>{L.sys}</td>
                <td style={{color: L.badge === 'err' ? 'var(--red)' : ''}}>{L.msg}</td>
              </tr>
            ))}
          </tbody>
        </table>
        
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <button style={{
            background: 'var(--border)', 
            border: 'none', 
            borderRadius: '4px',
            color: 'var(--text)', 
            padding: '6px 16px', 
            cursor: 'pointer',
            fontSize: '12px', 
            fontWeight: 600
          }}>
            LOAD OLDER LOGS ↓
          </button>
        </div>
      </div>
    </div>
  );
}
