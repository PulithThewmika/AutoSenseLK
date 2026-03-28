import React from 'react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: '⬡' },
    { id: 'analytics', label: 'Analytics', icon: '📈' },
    { id: 'logs', label: 'Logs', icon: '📄', badge: 3 },
  ];

  const infraItems = [
    { id: 'system', label: 'System', icon: '⚙' },
    { id: 'database', label: 'Database', icon: '🗄' },
    { id: 'alerts', label: 'Alerts', icon: '🔔', badge: 2 },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-text">AutoSense<span className="logo-lk">LK</span></div>
        <div className="logo-sub">Admin Dashboard</div>
      </div>
      <nav className="sidebar-nav">
        <div className="nav-section">Main</div>
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="nav-icon">{item.icon}</span> {item.label}
            {item.badge && <span className="nav-badge" id={item.id === 'logs' ? 'logBadge' : ''}>{item.badge}</span>}
          </button>
        ))}

        <div className="nav-section">Infrastructure</div>
        {infraItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <span className="nav-icon">{item.icon}</span> {item.label}
            {item.badge && <span className="nav-badge">{item.badge}</span>}
          </button>
        ))}
      </nav>
      <div className="sidebar-status">
        <div className="status-row"><span className="sdot green"></span>API Server · Online</div>
        <div className="status-row"><span className="sdot green"></span>MongoDB · Connected</div>
        <div className="status-row"><span className="sdot green"></span>Celery · Running</div>
        <div className="status-row"><span className="sdot yellow"></span>Redis · High mem</div>
      </div>
    </aside>
  );
}
