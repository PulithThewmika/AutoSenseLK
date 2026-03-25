import React, { useState, useEffect } from 'react';
import { Navigation } from './components/Navigation';
import { TabBar } from './components/TabBar';
import { HomeTab } from './components/tabs/HomeTab';
import { AnalyticsTab } from './components/tabs/AnalyticsTab';
import { BrandsTab } from './components/tabs/BrandsTab';
import { DealsTab } from './components/tabs/DealsTab';
import { Footer } from './components/Footer';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [isDark, setIsDark] = useState(true);

  // Initialize theme from local storage on mount
  useEffect(() => {
    const saved = localStorage.getItem('as-theme');
    if (saved === 'light') setIsDark(false);
  }, []);

  // Sync theme changes to data attribute
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
    localStorage.setItem('as-theme', isDark ? 'dark' : 'light');
  }, [isDark]);

  return (
    <>
      <Navigation 
        isDark={isDark} 
        toggleTheme={() => setIsDark(!isDark)} 
        onTabChange={setActiveTab} 
      />
      <div className="shell">
        <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
        
        {activeTab === 'home' && <HomeTab onTabChange={setActiveTab} isDark={isDark} />}
        {activeTab === 'analytics' && <AnalyticsTab isDark={isDark} />}
        {activeTab === 'brands' && <BrandsTab isDark={isDark} />}
        {activeTab === 'deals' && <DealsTab isDark={isDark} />}

        <Footer onTabChange={setActiveTab} />
      </div>
    </>
  );
}

export default App;
