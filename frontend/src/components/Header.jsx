import React from 'react'

const Header = () => {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">
          <div className="glow-orb"></div>
          <span>SMART TRIP <span className="ai-badge">AI</span></span>
        </div>
        <nav className="nav">
          <span className="status-pill"><div className="dot"></div> System Live</span>
          <button className="btn-auth">Login</button>
        </nav>
      </div>
      
      <style>{`
        .header {
          width: 100%;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          background: rgba(15, 23, 42, 0.8);
          backdrop-filter: blur(8px);
          z-index: 1000;
        }
        
        .header-inner {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 2rem;
        }
        
        .logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          font-size: 1rem;
          letter-spacing: 0.05em;
        }
        
        .glow-orb {
          width: 10px;
          height: 10px;
          background: var(--primary);
          border-radius: 50%;
          box-shadow: 0 0 10px var(--primary);
        }
        
        .ai-badge {
          background: var(--primary);
          padding: 0.1rem 0.4rem;
          border-radius: 4px;
          font-size: 0.65rem;
        }
        
        .nav {
          display: flex;
          align-items: center;
          gap: 2rem;
        }
        
        .status-pill {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--text-dim);
          background: rgba(255,255,255,0.05);
          padding: 0.3rem 0.8rem;
          border-radius: 100px;
        }
        
        .dot {
          width: 6px;
          height: 6px;
          background: var(--accent);
          border-radius: 50%;
          box-shadow: 0 0 5px var(--accent);
          animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
          0% { opacity: 0.5; }
          50% { opacity: 1; }
          100% { opacity: 0.5; }
        }
        
        .btn-auth {
          background: white;
          color: black;
          border: none;
          padding: 0.4rem 1.25rem;
          border-radius: 8px;
          font-weight: 700;
          font-size: 0.85rem;
          cursor: pointer;
          transition: transform 0.2s ease;
        }
        
        .btn-auth:hover { transform: translateY(-1px); }
      `}</style>
    </header>
  )
}

export default Header

