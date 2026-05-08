import React from 'react';

const AgentStatus = ({ stage, status }) => {
  const stages = [
    { id: 'planner', name: 'The Planner', icon: '🕵️', description: 'Crafting optimal routes & vibes' },
    { id: 'auditor', name: 'The Auditor', icon: '🛡️', description: 'Validating budget & logical flow' },
    { id: 'reoptimizer', name: 'The Re-Optimizer', icon: '⚡', description: 'Adapting to real-time chaos' }
  ];

  return (
    <div className="agent-status-container glass">
      <h3>Agentic Intelligence</h3>
      <div className="steps-list">
        {stages.map((s, idx) => (
          <div key={s.id} className={`step-item ${stage === s.id ? 'active' : ''} ${idx < stages.findIndex(st => st.id === stage) ? 'completed' : ''}`}>
            <div className="step-icon">{s.icon}</div>
            <div className="step-info">
              <div className="step-name">{s.name}</div>
              <div className="step-description">{s.description}</div>
            </div>
            {stage === s.id && <div className="pulse-dot"></div>}
            {idx < stages.findIndex(st => st.id === stage) && <div className="check-mark">✓</div>}
          </div>
        ))}
      </div>

      <style>{`
        .agent-status-container {
          padding: 1.5rem;
          border-radius: 20px;
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.08);
          margin-bottom: 1.5rem;
        }

        h3 {
          font-size: 0.9rem;
          text-transform: uppercase;
          letter-spacing: 2px;
          color: var(--primary);
          margin-bottom: 1.2rem;
        }

        .steps-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .step-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.75rem;
          border-radius: 12px;
          transition: all 0.3s ease;
          opacity: 0.4;
          position: relative;
        }

        .step-item.active {
          opacity: 1;
          background: rgba(255, 255, 255, 0.05);
          box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
        }

        .step-item.completed {
          opacity: 0.8;
          color: #10b981;
        }

        .step-icon {
          font-size: 1.2rem;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.05);
          border-radius: 8px;
        }

        .step-info {
          flex: 1;
        }

        .step-name {
          font-weight: 700;
          font-size: 0.9rem;
          margin-bottom: 2px;
        }

        .step-description {
          font-size: 0.7rem;
          opacity: 0.6;
        }

        .pulse-dot {
          width: 8px;
          height: 8px;
          background: var(--primary);
          border-radius: 50%;
          box-shadow: 0 0 10px var(--primary);
          animation: pulse 1.5s infinite;
        }

        .check-mark {
          font-weight: 900;
          color: #10b981;
        }

        @keyframes pulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.5); opacity: 0.5; }
          100% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default AgentStatus;
