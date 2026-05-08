import React, { useState } from 'react'
import Header from './components/Header'
import TripForm from './components/TripForm'
import ItineraryList from './components/ItineraryList'
import Hero from './components/Hero'
import Toast from './components/Toast'
import AgentStatus from './components/AgentStatus'
import DisruptionPanel from './components/DisruptionPanel'
import './styles/theme.css'

function App() {
  const [itinerary, setItinerary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)
  const [agentStage, setAgentStage] = useState(null) // 'planner', 'auditor', 'reoptimizer'

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  const simulateThinking = async (stages) => {
    for (const stage of stages) {
      setAgentStage(stage)
      await new Promise(resolve => setTimeout(resolve, 1500))
    }
  }

  const handleGenerate = async (destination, budget, travelStyle) => {
    setLoading(true)
    setItinerary(null)
    
    // Mimic multi-agent thinking
    await simulateThinking(['planner', 'auditor'])
    
    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ destination, budget, travel_style: travelStyle, interests: [] })
      })
      const data = await response.json()
      if (data.success) {
        setItinerary(data.itinerary)
        showToast('Itinerary orchestrated successfully!')
      } else {
        showToast(data.error || 'Failed to generate', 'error')
      }
    } catch (err) {
      showToast('Backend connection error', 'error')
    } finally {
      setLoading(false)
      setAgentStage(null)
    }
  }

  const handleDisrupt = async (type) => {
    if (!itinerary) {
      showToast('Generate a trip first!', 'error')
      return
    }

    setLoading(true)
    showToast(`CHAOS DETECTED: ${type.toUpperCase()}`, 'error')
    
    // Mimic the Re-Optimizer thinking
    await simulateThinking(['reoptimizer'])

    // In a real app, we'd call /api/replan. For this mimic, we'll simulate a change.
    const updated = JSON.parse(JSON.stringify(itinerary))
    if (type === 'rain') {
      updated.days[0].activities = updated.days[0].activities.map(a => ({
        ...a,
        title: a.weather_resistant ? a.title : `[INDOOR] ${a.title} Alternative`,
        description: `Re-planned for rainy conditions. Original: ${a.description}`
      }))
    }
    
    setItinerary(updated)
    setLoading(false)
    setAgentStage(null)
    showToast('Plan re-optimized for real-time conditions!', 'success')
  }

  return (
    <div className="app-shell">
      <Header />
      <div className="main-layout">
        <aside className="sidebar glass">
          <div className="sidebar-content">
            <div className="brand-badge">SMART TRIP AI</div>
            <h2>Global Concierge</h2>
            <p className="subtitle">Agentic Multi-Agent Orchestration</p>
            
            <AgentStatus stage={agentStage} />

            {!itinerary && (
              <TripForm
                onGenerate={handleGenerate}
                loading={loading}
                showToast={showToast}
              />
            )}

            {itinerary && <DisruptionPanel onDisrupt={handleDisrupt} />}
          </div>
        </aside>

        <main className="content-area">
          {loading ? (
            <div className="loading-container">
              <div className="ripple-loader">
                <div></div><div></div>
              </div>
              <h3>Orchestrating...</h3>
              <p>Fetching real-time vibes & routes</p>
            </div>
          ) : itinerary ? (
            <div className="itinerary-viewport">
              <div className="tab-icons-row">
                <div className="icon-item active">🗺️ <span>Route</span></div>
                <div className="icon-item">🏨 <span>Stay</span></div>
                <div className="icon-item">🍱 <span>Food</span></div>
                <div className="icon-item">🎭 <span>Vibe</span></div>
              </div>
              <div className="scroll-lock-container">
                <ItineraryList itinerary={itinerary} />
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <Hero />
            </div>
          )}
        </main>
      </div>

      {toast && <Toast message={toast.message} type={toast.type} />}

      <style>{`
        .app-shell {
          height: 100vh;
          width: 100vw;
          display: flex;
          flex-direction: column;
          overflow: hidden;
          background: var(--bg-deep);
        }
        
        .main-layout {
          flex: 1;
          display: flex;
          overflow: hidden;
          padding: 1rem;
          gap: 1.5rem;
        }
        
        .sidebar {
          width: 400px;
          border-radius: 24px;
          padding: 2rem;
          display: flex;
          flex-direction: column;
          overflow-y: auto;
          scrollbar-width: none;
        }
        
        .sidebar::-webkit-scrollbar { display: none; }
        
        .content-area {
          flex: 1;
          border-radius: 24px;
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid rgba(255, 255, 255, 0.05);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          position: relative;
        }
        
        .brand-badge {
          font-size: 0.7rem;
          font-weight: 900;
          color: var(--primary);
          letter-spacing: 0.2rem;
          margin-bottom: 0.5rem;
        }
        
        h2 { font-size: 1.8rem; margin-bottom: 0.25rem; }
        .subtitle { color: var(--text-dim); margin-bottom: 2rem; font-size: 0.9rem; }
        
        .loading-container {
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        
        .ripple-loader {
          position: relative;
          width: 80px;
          height: 80px;
          margin-bottom: 2rem;
        }
        
        .ripple-loader div {
          position: absolute;
          border: 4px solid var(--primary);
          opacity: 1;
          border-radius: 50%;
          animation: ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
        }
        
        .ripple-loader div:nth-child(2) { animation-delay: -0.5s; }
        
        @keyframes ripple {
          0% { top: 36px; left: 36px; width: 0; height: 0; opacity: 1; }
          100% { top: 0px; left: 0px; width: 72px; height: 72px; opacity: 0; }
        }
        
        .itinerary-viewport {
          display: flex;
          flex-direction: column;
          height: 100%;
          padding: 1.5rem;
        }
        
        .tab-icons-row {
          display: flex;
          gap: 2rem;
          margin-bottom: 1.5rem;
          padding: 0.75rem 1.5rem;
          background: rgba(255,255,255,0.05);
          border-radius: 100px;
          align-self: flex-start;
        }
        
        .icon-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.9rem;
          font-weight: 600;
          color: var(--text-dim);
          cursor: pointer;
          transition: all 0.3s ease;
        }
        
        .icon-item.active { color: white; transform: scale(1.1); }
        .icon-item span { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
        
        .scroll-lock-container {
          flex: 1;
          overflow-y: auto;
          padding-right: 0.5rem;
        }
        
        .scroll-lock-container::-webkit-scrollbar { width: 4px; }
        .scroll-lock-container::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
        
        .empty-state {
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          color: var(--text-dim);
        }
        
        .hero-visual { font-size: 4rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite; }
        
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-20px); }
        }
        
        @media (max-width: 900px) {
          .main-layout { flex-direction: column; overflow-y: auto; }
          .sidebar { width: 100%; }
        }
      `}</style>
    </div>
  )
}

export default App

