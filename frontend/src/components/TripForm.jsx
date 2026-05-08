import React, { useState } from 'react'

const TripForm = ({ onGenerate, loading }) => {
  const [formData, setFormData] = useState({
    destination: '',
    budget: 50000,
    startDate: '',
    endDate: '',
    interests: '',
    travelStyle: 'moderate'
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    onGenerate(formData.destination, formData.budget, formData.travelStyle)
  }

  return (
    <form className="trip-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <label>Destination</label>
        <input 
          type="text" 
          placeholder="e.g. Goa, Tokyo, Paris" 
          value={formData.destination}
          onChange={e => setFormData({...formData, destination: e.target.value})}
          required 
        />
      </div>

      <div className="form-row">
        <div className="input-group">
          <label>Start Date</label>
          <input 
            type="date" 
            value={formData.startDate}
            onChange={e => setFormData({...formData, startDate: e.target.value})}
            required 
          />
        </div>
        <div className="input-group">
          <label>End Date</label>
          <input 
            type="date" 
            value={formData.endDate}
            onChange={e => setFormData({...formData, endDate: e.target.value})}
            required 
          />
        </div>
      </div>

      <div className="input-group">
        <label>Budget (₹)</label>
        <input 
          type="number" 
          value={formData.budget}
          onChange={e => setFormData({...formData, budget: e.target.value})}
          required 
        />
      </div>

      <div className="input-group">
        <label>Interests (comma separated)</label>
        <input 
          type="text" 
          placeholder="e.g. Beaches, History, Food" 
          value={formData.interests}
          onChange={e => setFormData({...formData, interests: e.target.value})}
          required 
        />
      </div>

      <div className="input-group">
        <label>Travel Style</label>
        <select 
          value={formData.travelStyle}
          onChange={e => setFormData({...formData, travelStyle: e.target.value})}
        >
          <option value="budget">Budget</option>
          <option value="moderate">Moderate</option>
          <option value="luxury">Luxury</option>
        </select>
      </div>

      <button type="submit" className="btn-primary" disabled={loading}>
        {loading ? 'Orchestrating...' : 'Manifest My Trip ✈️'}
      </button>

      <style>{`
        .trip-form {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        
        .input-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        label {
          font-size: 0.8rem;
          font-weight: 700;
          color: var(--text-dim);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        
        input, select {
          padding: 0.8rem 1rem;
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          color: white;
          font-size: 0.95rem;
          transition: all 0.3s ease;
        }
        
        input:focus, select:focus {
          outline: none;
          border-color: var(--primary);
          background: rgba(255, 255, 255, 0.08);
          box-shadow: 0 0 15px var(--primary-glow);
        }
        
        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1rem;
        }
        
        .btn-primary {
          margin-top: 1rem;
          padding: 1rem;
          background: var(--primary);
          color: white;
          border: none;
          border-radius: 12px;
          font-weight: 800;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.3s ease;
          text-transform: uppercase;
          letter-spacing: 1px;
        }
        
        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 20px var(--primary-glow);
        }
        
        .btn-primary:active {
          transform: translateY(0);
        }
      `}</style>
    </form>
  )
}

export default TripForm
