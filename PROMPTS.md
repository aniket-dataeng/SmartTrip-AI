# SmartTrip-AI Architectural Prompts

This log documents the high-level prompts used to build and fix the SmartTrip-AI travel copilot.

## System Foundation
- "Create a 3-layer architecture for an AI travel copilot: Directives (SOPs), Execution (Python AI Engine), and Frontend (React/Vite)."
- "Design Pydantic models for structured itinerary data, including day-wise activities, costs, and budget tracking."

## AI Engine Calibration
- "Implement a Gemini API client with automatic retries and structured JSON output using Pydantic validation."
- "Orchestrate itinerary generation by fetching local attractions via Google Places API and processing them with Gemini 2.5 Flash."
- "Build a dynamic replanning engine that adjusts itineraries based on weather disruptions or budget changes."

## High-Fidelity Frontend
- "Design a premium, glassmorphic React dashboard for travel planning with a sidebar for inputs and a timeline-based viewport for itineraries."
- "Implement mobile-first responsive layouts using CSS variables and modern flex/grid systems."
- "Integrate a Vite proxy to provide seamless communication between the React frontend (5174) and FastAPI backend (8001)."

## Fixes & Optimization
- "Resolved Gemini 'Model Not Found' errors by identifying and switching to the latest available Gemini 2.5 models."
- "Restored missing core components and fixed CSS @import order for clean production builds."
