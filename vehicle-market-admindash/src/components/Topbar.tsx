import { useEffect, useState } from 'react';

interface TopbarProps {
  title: string;
  isDark: boolean;
  toggleTheme: () => void;
}

export function Topbar({ title, isDark, toggleTheme }: TopbarProps) {
  const [time, setTime] = useState<string>('--:--:--');
  const [refreshText, setRefreshText] = useState('↻ Refresh');

  useEffect(() => {
    const updateTime = () => {
      setTime(new Date().toLocaleTimeString('en-GB'));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleRefresh = () => {
    setRefreshText('↻ Refreshing...');
    setTimeout(() => setRefreshText('↻ Refresh'), 800);
  };

  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="page-title">{title}</div>
        <div className="page-crumb">AutoSenseLK / Admin / {title}</div>
      </div>
      <div className="topbar-right">
        <div className="live-badge"><span className="live-dot"></span>LIVE</div>
        <div className="topbar-time">{time}</div>
        <button className="btn-refresh" onClick={handleRefresh}>{refreshText}</button>
        <button 
          className="theme-toggle" 
          onClick={toggleTheme}
          title={`Switch to ${isDark ? 'Light' : 'Dark'} Mode`}
        >
          <span style={{marginLeft: '6px', fontSize: '10px'}}>{isDark ? '🌙' : '☀️'}</span>
          <div className="tt-thumb"></div>
        </button>
      </div>
    </header>
  );
}
