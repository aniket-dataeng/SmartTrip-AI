# Architectural Prompts

## 1. Project Initialization
**Prompt:** `instantiate` (based on AGENTS.md instructions)
**Action:** Set up 3-layer architecture: Directives, Orchestration (LLM), and Execution (Deterministic scripts).
**Date:** 2026-05-08

## 2. Phase 1 — Backend AI Engine
**Prompt:** `Create the backend AI engine: Gemini client (Flash/Pro), itinerary generation with budget optimization + route sequencing, dynamic replanning engine, weather/places services with mock fallback, FastAPI server with 4 REST endpoints, Pydantic models for all contracts, and 29 unit tests.`
**Architecture Decisions:**
- 3-layer architecture: Directives (SOPs) → Orchestration (FastAPI) → Execution (Python scripts)
- Gemini 2.5 Flash as default (cost-efficient), Pro reserved for complex reasoning
- Curated local data fallback when Google Places/Weather API keys are absent
- Budget optimizer with travel-style-based category ratios
- Nearest-neighbor route optimization with haversine distance
**Date:** 2026-05-08

