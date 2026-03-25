import React from 'react';

interface NavigationProps {
  isDark: boolean;
  toggleTheme: () => void;
  onTabChange: (tabId: string) => void;
}

export function Navigation({ isDark, toggleTheme, onTabChange }: NavigationProps) {
  return (
    <nav>
      <div className="logo" onClick={() => onTabChange('home')}>
        AutoSense<span className="logo-lk">LK</span>
      </div>
      <div className="nav-r">
        <button className="tt-btn" id="ttBtn" aria-label="Toggle theme" onClick={toggleTheme}>
          <div className="tt-thumb" id="ttThumb">{isDark ? '☀️' : '🌙'}</div>
        </button>
        <button className="btn-nav" onClick={() => onTabChange('deals')}>
          Score a listing
        </button>
      </div>
    </nav>
  );
}
