"""
Centralized Gemini API wrapper for SmartTrip-AI.
Uses Flash for standard tasks, Pro for complex reasoning.
"""

import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
_API_KEY = os.getenv("GEMINI_API_KEY", "")
_MAX_RETRIES = 3
_RETRY_DELAY_SEC = 2

MODEL_FLASH = "gemini-2.5-flash"
MODEL_PRO = "gemini-2.5-pro"


def _get_client():
    """Initialize and return the Gemini client."""
    if not _API_KEY or _API_KEY == "your_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY not set. Add it to .env file."
        )
    genai.configure(api_key=_API_KEY)


def generate_json(
    prompt: str,
    system_instruction: str = "",
    use_pro: bool = False,
    temperature: float = 0.7,
) -> dict:
    """
    Send a prompt to Gemini and get structured JSON back.
    """
    _get_client()

    model_name = MODEL_PRO if use_pro else MODEL_FLASH
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction or None,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=temperature,
        ),
    )

    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            # Handle potential markdown code blocks in response
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "", 1).rsplit("```", 1)[0].strip()
            elif raw_text.startswith("```"):
                raw_text = raw_text.replace("```", "", 1).rsplit("```", 1)[0].strip()
                
            return json.loads(raw_text)

        except json.JSONDecodeError as e:
            last_error = f"JSON parse error (attempt {attempt}): {e}"
        except Exception as e:
            last_error = f"Gemini API error (attempt {attempt}): {e}"

        if attempt < _MAX_RETRIES:
            time.sleep(_RETRY_DELAY_SEC * attempt)

    raise RuntimeError(f"Gemini call failed after {_MAX_RETRIES} retries: {last_error}")


def generate_text(
    prompt: str,
    system_instruction: str = "",
    use_pro: bool = False,
    temperature: float = 0.7,
) -> str:
    """
    Send a prompt to Gemini and get plain text back.
    """
    _get_client()

    model_name = MODEL_PRO if use_pro else MODEL_FLASH
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction or None,
        generation_config=genai.GenerationConfig(
            temperature=temperature,
        ),
    )

    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            last_error = f"Gemini API error (attempt {attempt}): {e}"
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY_SEC * attempt)

    raise RuntimeError(f"Gemini call failed after {_MAX_RETRIES} retries: {last_error}")
