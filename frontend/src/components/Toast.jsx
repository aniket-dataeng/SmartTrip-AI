import React from 'react'

const Toast = ({ message, type = 'success' }) => {
  return (
    <div className={`toast ${type}`}>
      <div className="toast-content">
        <span className="icon">{type === 'success' ? '✓' : '!'}</span>
        <p>{message}</p>
      </div>
      
      <style>{`
        .toast {
          position: fixed;
          bottom: 2rem;
          right: 2rem;
          padding: 1rem 2rem;
          border-radius: 12px;
          background: var(--anthropic-dark);
          color: white;
          box-shadow: 0 20px 40px rgba(0,0,0,0.2);
          animation: slideIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
          z-index: 10000;
        }
        
        .toast.error { background: #d9534f; }
        
        .toast-content {
          display: flex;
          align-items: center;
          gap: 1rem;
        }
        
        .icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: rgba(255,255,255,0.2);
          font-weight: 700;
        }
        
        p {
          font-family: var(--font-heading);
          font-weight: 600;
          font-size: 0.9rem;
          margin: 0;
        }
        
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `}</style>
    </div>
  )
}

export default Toast
