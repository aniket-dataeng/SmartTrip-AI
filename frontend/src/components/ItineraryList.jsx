import React from 'react'

const ItineraryList = ({ itinerary }) => {
  if (!itinerary) return null

  return (
    <div className="itinerary-view">
      <div className="itinerary-header">
        <span className="dest-tag">Destination Unlocked</span>
        <h2>{itinerary.destination}</h2>
        <p className="summary">{itinerary.summary}</p>

        <div className="itinerary-stats glass">
          <div className="stat-pill">₹{itinerary.total_cost} Total</div>
          <div className="stat-pill">₹{itinerary.budget_remaining} Left</div>
          <div className="stat-pill">{itinerary.days?.length} Days</div>
        </div>
      </div>

      <div className="timeline">
        {itinerary.days?.map((day, idx) => (
          <div key={idx} className="day-block">
            <div className="day-header">
              <div className="day-num">DAY {day.day_number}</div>
              <div className="day-theme">{day.theme}</div>
            </div>

            <div className="activities-grid">
              {day.activities?.map((act, i) => (
                <div key={i} className="act-card glass">
                  <div className="act-top">
                    <span className="category">{act.category}</span>
                    <span className="duration">{act.duration_minutes}m</span>
                  </div>
                  <h4>{act.name}</h4>
                  <p>{act.description}</p>
                  <div className="act-bottom">
                    <span className="loc">📍 {act.location}</span>
                    <span className="price">₹{act.cost}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {itinerary.travel_tips && (
        <div className="tips-grid">
          <h3>Pro Tips 💡</h3>
          <div className="tips-container">
            {itinerary.travel_tips.map((tip, i) => (
              <div key={i} className="tip-card glass">{tip}</div>
            ))}
          </div>
        </div>
      )}

      <style>{`
        .itinerary-view { padding: 1rem 0; width: 100%; }
        
        .itinerary-header { text-align: left; margin-bottom: 3rem; }
        
        .dest-tag {
          color: var(--primary);
          font-weight: 800;
          font-size: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.2em;
        }
        
        .itinerary-header h2 { font-size: 2.5rem; margin: 0.5rem 0; }
        
        .summary { color: var(--text-dim); max-width: 800px; margin-bottom: 2rem; }
        
        .itinerary-stats {
          display: inline-flex;
          gap: 1rem;
          padding: 0.75rem 1.5rem;
          border-radius: 50px;
        }
        
        .stat-pill {
          background: rgba(255,255,255,0.05);
          padding: 0.4rem 0.8rem;
          border-radius: 12px;
          font-size: 0.75rem;
          font-weight: 700;
        }
        
        .timeline { width: 100%; }
        
        .day-block { margin-bottom: 4rem; }
        
        .day-header {
          display: flex;
          align-items: center;
          gap: 1.5rem;
          margin-bottom: 2rem;
        }
        
        .day-num {
          background: var(--primary);
          padding: 0.4rem 1.2rem;
          border-radius: 50px;
          font-weight: 900;
          font-size: 1rem;
        }
        
        .day-theme { font-size: 1.3rem; font-weight: 800; }
        
        .activities-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 1rem;
        }
        
        .act-card {
           padding: 1.5rem;
           border-radius: 20px;
           transition: transform 0.3s ease;
           display: flex;
           flex-direction: column;
           justify-content: space-between;
        }
        
        .act-card:hover { transform: translateY(-4px); border-color: var(--primary); }
        
        .act-top { display: flex; justify-content: space-between; margin-bottom: 0.75rem; }
        
        .category {
          background: var(--primary-glow);
          color: var(--primary);
          padding: 0.15rem 0.5rem;
          border-radius: 4px;
          font-size: 0.65rem;
          font-weight: 800;
          text-transform: uppercase;
        }
        
        .duration { color: var(--text-dim); font-size: 0.75rem; }
        
        .act-card h4 { margin-bottom: 0.5rem; font-size: 1.1rem; }
        
        .act-card p { color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1rem; flex: 1; }
        
        .act-bottom {
          display: flex;
          justify-content: space-between;
          border-top: 1px solid rgba(255,255,255,0.05);
          padding-top: 0.75rem;
          font-size: 0.8rem;
        }
        
        .price { color: var(--accent); font-weight: 800; }
        
        .tips-grid { margin-top: 4rem; padding-bottom: 2rem; }
        .tips-grid h3 { margin-bottom: 1.5rem; }
        
        .tips-container {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
          gap: 1rem;
        }
        
        .tip-card { padding: 1.25rem; border-radius: 16px; font-weight: 600; font-size: 0.85rem; }
      `}</style>
    </div>
  )
}

export default ItineraryList

