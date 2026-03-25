import React from 'react';

interface TabBarProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
}

export function TabBar({ activeTab, onTabChange }: TabBarProps) {
  const tabs = [
    { id: 'home', icon: '🏠', label: 'Home' },
    { id: 'analytics', icon: '📈', label: 'Analytics' },
    { id: 'brands', icon: '🏷️', label: 'Brands', badge: '55' },
    { id: 'deals', icon: '⚡', label: 'Deal Scorer' },
  ];

  return (
    <div className="tab-bar">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => onTabChange(tab.id)}
        >
          <span className="tab-icon">{tab.icon}</span>
          {tab.label}
          {tab.badge && <span className="tab-pill">{tab.badge}</span>}
        </button>
      ))}
    </div>
  );
}
