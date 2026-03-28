import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { baseOpts, lineDs, last30Labels, genSeries } from '../utils/ChartHelpers';

export function System() {
  const chartCpuRef = useRef<HTMLCanvasElement>(null);
  const chartMemRef = useRef<HTMLCanvasElement>(null);
  const chartNetRef = useRef<HTMLCanvasElement>(null);
  const chartIO_Ref = useRef<HTMLCanvasElement>(null);
  const chartsRef = useRef<any>({});

  useEffect(() => {
    const sysLabels = last30Labels('m');

    if (chartCpuRef.current) {
      chartsRef.current.cpu = new Chart(chartCpuRef.current, {
        type: 'line',
        data: { labels: sysLabels, datasets: [lineDs('CPU Usage %', genSeries(30, 40, 20), '0,184,217', true)] },
        options: baseOpts()
      });
    }

    if (chartMemRef.current) {
      chartsRef.current.mem = new Chart(chartMemRef.current, {
        type: 'line',
        data: { labels: sysLabels, datasets: [lineDs('Memory GB', genSeries(30, 12, 1), '59,111,245', true)] },
        options: baseOpts()
      });
    }

    if (chartNetRef.current) {
      chartsRef.current.net = new Chart(chartNetRef.current, {
        type: 'line',
        data: {
          labels: sysLabels,
          datasets: [
            lineDs('In (MB/s)', genSeries(30, 5, 2), '0,208,132', false),
            lineDs('Out (MB/s)', genSeries(30, 1.5, 0.5), '245,200,66', false)
          ]
        },
        options: baseOpts()
      });
    }

    if (chartIO_Ref.current) {
      chartsRef.current.io = new Chart(chartIO_Ref.current, {
        type: 'line',
        data: { labels: sysLabels, datasets: [lineDs('Disk IOPS', genSeries(30, 800, 300), '255,145,56', true)] },
        options: baseOpts()
      });
    }

    return () => {
      Object.values(chartsRef.current).forEach((c: any) => c.destroy());
    };
  }, []);

  return (
    <div className="page active view-fade-in">
      <div className="grid-4 mb16">
        <div className="kpi">
          <div className="kpi-label">Avg CPU Core 1-4</div>
          <div className="kpi-val">42%</div>
          <div className="kpi-delta dn">↑ 5% last hour</div>
        </div>
        <div className="kpi">
          <div className="kpi-label">Mem Consumption</div>
          <div className="kpi-val">11.8<span style={{fontSize:'14px',color:'var(--mu)'}}>GB</span></div>
          <div className="kpi-delta up">↓ 0.2GB freed</div>
        </div>
        <div className="kpi">
          <div className="kpi-label">Active Conns</div>
          <div className="kpi-val">1,842</div>
          <div className="kpi-delta up">↑ 412 peak</div>
        </div>
        <div className="kpi">
          <div className="kpi-label">Load Average</div>
          <div className="kpi-val">1.14</div>
          <div className="kpi-delta up">Normal threshold</div>
        </div>
      </div>
      
      <div className="grid-2 mb16">
        <div className="card">
          <div className="card-header">
            <div className="card-title">CPU Utilization (Cluster Avg)</div>
          </div>
          <div style={{height: '200px'}}><canvas ref={chartCpuRef}></canvas></div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-title">RAM Usage (Absolute GB)</div>
          </div>
          <div style={{height: '200px'}}><canvas ref={chartMemRef}></canvas></div>
        </div>
      </div>
      
      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <div className="card-title">Network Throughput</div>
          </div>
          <div style={{height: '200px'}}><canvas ref={chartNetRef}></canvas></div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-title">Disk I/O</div>
          </div>
          <div style={{height: '200px'}}><canvas ref={chartIO_Ref}></canvas></div>
        </div>
      </div>
    </div>
  );
}
