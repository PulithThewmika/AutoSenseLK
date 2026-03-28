import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { baseOpts, lineDs, last30Labels, genSeries } from '../utils/ChartHelpers';

export function Database() {
  const chartDbQueryRef = useRef<HTMLCanvasElement>(null);
  const chartsRef = useRef<any>({});

  useEffect(() => {
    if (chartDbQueryRef.current) {
      chartsRef.current.dbq = new Chart(chartDbQueryRef.current, {
        type: 'line',
        data: {
          labels: last30Labels('m'),
          datasets: [
            lineDs('Reads/s', genSeries(30, 800, 200), '0,184,217', false),
            lineDs('Writes/s', genSeries(30, 150, 40), '255,145,56', false)
          ]
        },
        options: baseOpts()
      });
    }

    return () => {
      Object.values(chartsRef.current).forEach((c: any) => c.destroy());
    };
  }, []);

  const cols = [
    { coll: 'vehicles', docs: '24,810', size: '1.2 GB', iSize: '84 MB', op: '142/s' },
    { coll: 'history_prices', docs: '1.4M', size: '4.8 GB', iSize: '420 MB', op: '840/s' },
    { coll: 'deal_scores', docs: '24,810', size: '0.4 GB', iSize: '42 MB', op: '12/s' },
    { coll: 'users', docs: '8,412', size: '0.1 GB', iSize: '12 MB', op: '2/s' },
    { coll: 'activity_logs', docs: '4.2M', size: '6.4 GB', iSize: '512 MB', op: '84/s' },
  ];

  return (
    <div className="page active view-fade-in">
      <div className="grid-2 mb16">
        <div className="card">
          <div className="card-header">
            <div className="card-title">MongoDB Cluster Stats</div>
            <div className="card-badge cb-green">PRIMARY</div>
          </div>
          <table className="status-table">
            <tbody>
              <tr><td style={{color:'var(--mu)'}}>Version</td><td>6.0.4 Enterprise</td></tr>
              <tr><td style={{color:'var(--mu)'}}>Uptime</td><td>14d 6h 12m</td></tr>
              <tr><td style={{color:'var(--mu)'}}>Connections</td><td>842 / 2000 (Active)</td></tr>
              <tr><td style={{color:'var(--mu)'}}>Network In / Out</td><td>18 MB/s / 42 MB/s</td></tr>
              <tr><td style={{color:'var(--mu)'}}>Storage Engine</td><td>WiredTiger</td></tr>
              <tr><td style={{color:'var(--mu)'}}>Oplog Window</td><td>48 hrs</td></tr>
            </tbody>
          </table>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-title">Query Performance</div>
            <div className="card-badge cb-cyan">REALTIME</div>
          </div>
          <div style={{height: '210px'}}><canvas ref={chartDbQueryRef}></canvas></div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <div className="card-title">Collection Metrics</div>
        </div>
        <table className="logs-table">
          <thead>
            <tr>
              <th>Namespace</th>
              <th>Document Count</th>
              <th>Data Size</th>
              <th>Index Size</th>
              <th>Hot Ops (R/W)</th>
            </tr>
          </thead>
          <tbody>
            {cols.map((c, i) => (
              <tr key={i}>
                <td style={{fontFamily:'monospace', color:'var(--cyan)'}}>{c.coll}</td>
                <td>{c.docs}</td>
                <td>{c.size}</td>
                <td>{c.iSize}</td>
                <td>{c.op}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
