import React from 'react';

const DisruptionPanel = ({ onDisrupt }) => {
  const options = [
    { id: 'rain', label: 'Simulate Rain 🌧️', desc: 'Swap outdoor activities for indoor alternatives' },
    { id: 'delay', label: 'Flight Delay ✈️', desc: 'Truncate schedule and re-prioritize events' },
    { id: 'budget', label: 'Budget Cut 📉', desc: 'Re-optimize for 30% less spend' }
  ];

  return (
    <div className="disruption-panel glass">
      <div className="panel-header">
        <h4>Chaos Monitor</h4>
        <div className="live-badge">LIVE</div>
      </div>
      <p className="panel-hint">Inject real-time disruptions to see the Re-Optimizer in action.</p>
      
      <div className="disruption-grid">
        {options.map(opt => (
          <button 
            key={opt.id} 
            className="disruption-btn"
            onClick={() => onDisrupt(opt.id)}
          >
            <span className="btn-label">{opt.label}</span>
            <span className="btn-desc">{opt.desc}</span>
          </button>
        ))}
      </div>

      <style>{`
        .disruption-panel {
          padding: 1.2rem;
          border-radius: 20px;
          background: rgba(239, 68, 68, 0.05);
          border: 1px solid rgba(239, 68, 68, 0.15);
        }

        .panel-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }

        h4 {
          color: #f87171;
          margin: 0;
          font-size: 0.85rem;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .live-badge {
          background: #ef4444;
          color: white;
          font-size: 0.6rem;
          padding: 2px 6px;
          border-radius: 4px;
          font-weight: 800;
          animation: blink 1s infinite;
        }

        .panel-hint {
          font-size: 0.75rem;
          opacity: 0.7;
          margin-bottom: 1rem;
        }

        .disruption-grid {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .disruption-btn {
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.05);
          padding: 0.75rem;
          border-radius: 12px;
          color: white;
          text-align: left;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          flex-direction: column;
        }

        .disruption-btn:hover {
          background: rgba(239, 68, 68, 0.1);
          border-color: rgba(239, 68, 68, 0.3);
          transform: translateX(4px);
        }

        .btn-label {
          font-weight: 700;
          font-size: 0.85rem;
          margin-bottom: 2px;
        }

        .btn-desc {
          font-size: 0.65rem;
          opacity: 0.5;
        }

        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
};

export default DisruptionPanel;
