import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import { baseOpts, lineDs, barDs, last30Labels, genSeries } from '../utils/ChartHelpers';

export function Analytics() {
  const chartBrandsRef = useRef<HTMLCanvasElement>(null);
  const chartPricesRef = useRef<HTMLCanvasElement>(null);
  const chartSalesRef = useRef<HTMLCanvasElement>(null);
  const chartGeoRef = useRef<HTMLCanvasElement>(null);
  const chartsRef = useRef<any>({});

  useEffect(() => {
    if (chartBrandsRef.current) {
      chartsRef.current.brands = new Chart(chartBrandsRef.current, {
        type: 'bar',
        data: {
          labels: ['Toyota', 'Honda', 'Suzuki', 'Nissan', 'Mitsubishi', 'Audi', 'BMW'],
          datasets: [barDs('Listings', [8450, 4210, 3800, 2150, 1840, 680, 520], '0,208,132')]
        },
        options: baseOpts()
      });
    }

    const priceLabels = ['< 2M', '2-5M', '5-10M', '10-20M', '20-30M', '30M+'];
    const p1 = [400, 3100, 8400, 5200, 2100, 850];
    if (chartPricesRef.current) {
      chartsRef.current.prices = new Chart(chartPricesRef.current, {
        type: 'bar',
        data: {
          labels: priceLabels,
          datasets: [barDs('Vehicle counts by range', p1, '59,111,245')]
        },
        options: baseOpts()
      });
    }

    const salesLabels = last30Labels('d');
    const s1 = genSeries(30, 240, 40);
    const s2 = genSeries(30, 180, 50);
    if (chartSalesRef.current) {
      chartsRef.current.sales = new Chart(chartSalesRef.current, {
        type: 'line',
        data: {
          labels: salesLabels,
          datasets: [
            lineDs('New listings', s1, '0,184,217', true),
            lineDs('Sold/Removed', s2, '255,71,87', false)
          ]
        },
        options: baseOpts()
      });
    }

    if (chartGeoRef.current) {
      chartsRef.current.geo = new Chart(chartGeoRef.current, {
        type: 'doughnut',
        data: {
          labels: ['Colombo', 'Gampaha', 'Kandy', 'Kurunegala', 'Kalutara', 'Other'],
          datasets: [{
            data: [42, 28, 12, 8, 6, 4],
            backgroundColor: [
              'rgba(0,184,217,0.8)', 'rgba(59,111,245,0.8)',
              'rgba(245,200,66,0.8)', 'rgba(255,145,56,0.8)',
              'rgba(255,71,87,0.8)', 'rgba(100,100,100,0.6)'
            ],
            borderWidth: 0,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'right', labels: { color: '#8b9bb4', boxWidth: 12, font: {family: '"Inter", sans-serif'} } }
          }
        }
      });
    }

    return () => {
      Object.values(chartsRef.current).forEach((c: any) => c.destroy());
    };
  }, []);

  return (
    <div className="page active view-fade-in">
      <div className="grid-2 mb16">
        <div className="card">
          <div className="card-header">
            <div className="card-title">Top brands distribution</div>
            <div className="card-badge cb-cyan">OVERALL</div>
          </div>
          <div style={{height: '240px'}}><canvas ref={chartBrandsRef}></canvas></div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-title">Price segments distribution</div>
            <div className="card-badge cb-blue">OVERALL</div>
          </div>
          <div style={{height: '240px'}}><canvas ref={chartPricesRef}></canvas></div>
        </div>
      </div>
      
      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <div className="card-title">Market velocity - last 30 days</div>
            <div className="card-badge cb-blue">30 DAYS</div>
          </div>
          <div style={{height: '240px'}}><canvas ref={chartSalesRef}></canvas></div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-title">Geographical split (%)</div>
            <div className="card-badge cb-cyan">REGION</div>
          </div>
          <div style={{height: '240px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{width: '90%', height: '90%'}}><canvas ref={chartGeoRef}></canvas></div>
          </div>
        </div>
      </div>
    </div>
  );
}
