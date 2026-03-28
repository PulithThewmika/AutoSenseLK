import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Topbar } from './components/Topbar';
import { Overview } from './pages/Overview';
import { Analytics } from './pages/Analytics';
import { Logs } from './pages/Logs';
import { System } from './pages/System';
import { Database } from './pages/Database';
import { Alerts } from './pages/Alerts';

export function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [isDark, setIsDark] = useState(true);

  // Initialize theme from localStorage or default to dark
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
      setIsDark(false);
      document.documentElement.setAttribute('data-theme', 'light');
    } else {
      setIsDark(true);
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }, []);

  const toggleTheme = () => {
    const newMode = !isDark;
    setIsDark(newMode);
    document.documentElement.setAttribute('data-theme', newMode ? 'dark' : 'light');
    localStorage.setItem('theme', newMode ? 'dark' : 'light');
  };

  const renderContent = () => {
    switch(activeTab) {
      case 'overview': return <Overview />;
      case 'analytics': return <Analytics />;
      case 'logs': return <Logs />;
      case 'system': return <System />;
      case 'database': return <Database />;
      case 'alerts': return <Alerts />;
      default: return <Overview />;
    }
  };

  return (
    <>
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="main-content">
        <Topbar title="Dashboard" isDark={isDark} toggleTheme={toggleTheme} />
        {renderContent()}
      </div>
    </>
  );
}

export default App;
