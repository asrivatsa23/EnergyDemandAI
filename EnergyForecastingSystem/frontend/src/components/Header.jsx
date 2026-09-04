import React from 'react';
import { Zap, LayoutDashboard, TrendingUp, BarChart2, Cpu, Activity } from 'lucide-react';

const Header = ({ activePage, setActivePage, isOnline = true }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'forecast', label: 'Forecast', icon: TrendingUp },
    { id: 'comparison', label: 'Model Comparison', icon: BarChart2 },
    { id: 'explainability', label: 'Explainability (XAI)', icon: Cpu },
    { id: 'analysis', label: 'Data Analysis', icon: Activity },
  ];

  return (
    <header className="app-header">
      <div className="brand-logo">
        <Zap className="h-6 w-6 text-cyan-400" style={{ color: '#06b6d4' }} />
        <span>EnergyDemandAI</span>
        <span className="brand-badge">India Power Grid</span>
      </div>

      <nav className="nav-links">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={`nav-btn ${activePage === item.id ? 'active' : ''}`}
              onClick={() => setActivePage(item.id)}
            >
              <Icon size={16} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="status-pill">
        <span className="status-dot" />
        <span>{isOnline ? 'Grid System Online' : 'Connecting...'}</span>
      </div>
    </header>
  );
};

export default Header;
