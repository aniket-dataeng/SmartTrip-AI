import React from 'react'

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-badge">Next-Gen Travel Engine</div>
      <h1>Map Your <span className="gradient-text">Main Character</span> Energy.</h1>
      <p>Stop scrolling, start living. AI-powered itineraries that hit different.</p>
      
      <div className="stats-strip glass">
        <div className="stat"><span>10k+</span> Locations</div>
        <div className="stat"><span>2s</span> Gen Speed</div>
        <div className="stat"><span>100%</span> Vibe Check</div>
      </div>

      <style>{`
        .hero {
          text-align: center;
          padding: 8rem 1rem 4rem;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        
        .hero-badge {
          background: rgba(124, 58, 237, 0.1);
          color: var(--primary);
          padding: 0.5rem 1.25rem;
          border-radius: 50px;
          border: 1px solid var(--primary-glow);
          font-weight: 700;
          font-size: 0.8rem;
          margin-bottom: 2rem;
          text-transform: uppercase;
          letter-spacing: 0.1em;
        }
        
        h1 {
          font-size: clamp(3rem, 8vw, 5.5rem);
          max-width: 900px;
          margin-bottom: 1.5rem;
          line-height: 0.95;
        }
        
        .gradient-text {
          background: linear-gradient(90deg, var(--primary), var(--accent));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        
        p {
          color: var(--text-dim);
          font-size: 1.25rem;
          max-width: 500px;
          margin-bottom: 3rem;
        }
        
        .stats-strip {
          display: flex;
          gap: 3rem;
          padding: 1.5rem 3rem;
          border-radius: 30px;
        }
        
        .stat {
          display: flex;
          flex-direction: column;
          font-size: 0.8rem;
          color: var(--text-dim);
          font-weight: 600;
        }
        
        .stat span {
          color: var(--text-main);
          font-size: 1.25rem;
          font-weight: 800;
        }
        
        @media (max-width: 600px) {
          .stats-strip { flex-direction: column; gap: 1.5rem; padding: 2rem; width: 100%; }
        }
      `}</style>
    </section>
  )
}

export default Hero
