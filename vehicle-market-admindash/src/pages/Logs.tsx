import { useEffect, useState, useRef } from 'react';

type LogEntry = {
  ts: string;
  lvl: string;
  sys: string;
  msg: string;
  badge: string;
};

export function Logs() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const MAX_LOGS = 100;
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Determine WS URL based on current host if dynamic, or fixed for dev
    const wsUrl = 'ws://localhost:8000/api/v1/logs/stream';
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const logData: LogEntry = JSON.parse(event.data);
        setLogs(prevLogs => {
          const newLogs = [logData, ...prevLogs];
          if (newLogs.length > MAX_LOGS) {
            return newLogs.slice(0, MAX_LOGS);
          }
          return newLogs;
        });
      } catch (e) {
        console.error("Failed to parse log message", e);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error", error);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    return () => {
      if (ws.readyState === 1) {
        ws.close();
      }
    };
  }, []);

  return (
    <div className="page active view-fade-in">
      <div className="card">
        <div className="card-header">
          <div className="card-title">Realtime System Stream</div>
          <div className="card-badge cb-green">TAIL • {MAX_LOGS}</div>
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
            {logs.length === 0 && (
              <tr>
                <td colSpan={4} style={{ textAlign: 'center', padding: '20px', color: 'var(--mu)' }}>
                  Awaiting logs...
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}