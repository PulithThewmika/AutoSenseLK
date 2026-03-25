import React from 'react';

interface FooterProps {
  onTabChange: (tabId: string) => void;
}

export function Footer({ onTabChange }: FooterProps) {
  return (
    <footer>
      <div>
        <div className="foot-logo">
          AutoSense<span className="foot-lk">LK</span>
        </div>
        <div className="foot-tag">
          Sri Lanka's open vehicle market intelligence platform. Powered by ML and real listing data from ikman.lk.
        </div>
      </div>
      <div className="foot-nav">
        <div className="foot-col">
          <h4>Navigation</h4>
          <ul>
            <li><a href="#" onClick={(e) => { e.preventDefault(); onTabChange('home'); }}>Home</a></li>
            <li><a href="#" onClick={(e) => { e.preventDefault(); onTabChange('analytics'); }}>Analytics</a></li>
            <li><a href="#" onClick={(e) => { e.preventDefault(); onTabChange('brands'); }}>Brands</a></li>
            <li><a href="#" onClick={(e) => { e.preventDefault(); onTabChange('deals'); }}>Deal Scorer</a></li>
          </ul>
        </div>
        <div className="foot-col">
          <h4>Developers</h4>
          <ul>
            <li><a href="#">Swagger UI</a></li>
            <li><a href="#">GitHub</a></li>
            <li><a href="#">Changelog</a></li>
            <li><a href="#">ikman.lk</a></li>
          </ul>
        </div>
      </div>
      <div className="foot-r">
        <div className="foot-badges">
          <span className="foot-badge">FastAPI 0.115</span>
          <span className="foot-badge">MongoDB 6+</span>
          <span className="foot-badge">React 19</span>
          <span className="foot-badge">scikit-learn</span>
          <span className="foot-badge">Celery + Redis</span>
          <span className="foot-badge">Beanie ODM</span>
        </div>
        <div className="foot-copy">© 2025 AutoSenseLK · Sri Lanka Vehicle Intelligence</div>
      </div>
    </footer>
  );
}
