# edis_assistant/chat_engine.py

from typing import Optional, List, Dict
import os

from .system_prompt import SYSTEM_PROMPT
from .intent_router import detect_intent

# Try to import Groq, fallback to local responses
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Groq not available, using fallback responses")

# -----------------------------
# Groq configuration (when available)
# -----------------------------
DEFAULT_MODEL = "llama-3.1-8b-instant"  # Groq's Llama3 model

def get_groq_client():
    """Initialize Groq client with API key from environment"""
    if not GROQ_AVAILABLE:
        return None
        
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "gsk_your_groq_api_key_here":
        print("Please set GROQ_API_KEY in your .env file")
        return None
    return Groq(api_key=api_key)

# -----------------------------
# Core Assistant Engine
# -----------------------------
def ask_edis_assistant(
    user_query: str,
    context: Optional[str],
    chat_history: List[Dict],
    model: Optional[str] = None
) -> Dict:
    """
    Executes a single EDIS assistant turn using Groq or fallback
    Returns:
        {
          text: str,
          intent: str,
          visualize: str | None
        }
    """

    intent = detect_intent(user_query)
    model = model or DEFAULT_MODEL

    # Try Groq first, fallback to local responses
    if GROQ_AVAILABLE:
        client = get_groq_client()
        if client:
            try:
                # -----------------------------
                # Build messages for Groq API
                # -----------------------------
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "system", "content": f"DETECTED_INTENT: {intent}"}
                ]

                if context:
                    messages.append({
                        "role": "system",
                        "content": f"ECOSYSTEM_CONTEXT:\n{context}"
                    })

                # Keep last N messages only
                messages.extend(chat_history[-8:])
                messages.append({"role": "user", "content": user_query})

                # -----------------------------
                # Groq API call
                # -----------------------------
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=500
                )

                text = response.choices[0].message.content.strip()

                # -----------------------------
                # Visualization extraction
                # -----------------------------
                visualize = None
                if "[VISUALIZE:" in text:
                    try:
                        visualize = text.split("[VISUALIZE:")[1].split("]")[0].strip()
                        text = text.replace(f"[VISUALIZE:{visualize}]", "").strip()
                    except Exception:
                        visualize = None

                return {
                    "text": text,
                    "intent": intent,
                    "visualize": visualize
                }

            except Exception as e:
                print(f"Groq API error: {e}")
                # Fall back to local responses
                pass
    
    # Fallback to local responses
    from .fallback_engine import ask_edis_assistant_fallback
    return ask_edis_assistant_fallback(user_query, context, chat_history, model)
