# edis_assistant/intent_router.py

GENERAL_KNOWLEDGE_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning",
    "deep learning", "chatgpt", "who are you"
]

VISUAL_KEYWORDS = [
    "chart", "graph", "plot", "map", "visualization", "diagram"
]

ADVICE_KEYWORDS = [
    "what should", "how to reduce", "how can we",
    "steps", "action", "solution", "mitigation", "recommend"
]

EXPLANATION_KEYWORDS = [
    "why", "explain", "reason", "cause", "interpret", "meaning"
]

TREND_KEYWORDS = [
    "trend", "over time", "increase", "decrease",
    "change", "pattern", "historical"
]

def detect_intent(user_query: str) -> str:
    q = user_query.lower().strip()

    # -----------------------------
    # Out-of-domain (AI/general chat)
    # -----------------------------
    if any(k in q for k in GENERAL_KNOWLEDGE_KEYWORDS):
        return "out_of_domain"

    # -----------------------------
    # Visualization intent
    # -----------------------------
    if any(k in q for k in VISUAL_KEYWORDS):
        return "visual_request"

    # -----------------------------
    # Advice / Action
    # -----------------------------
    if any(k in q for k in ADVICE_KEYWORDS):
        return "advice"

    # -----------------------------
    # Explanation / Interpretation
    # -----------------------------
    if any(k in q for k in EXPLANATION_KEYWORDS):
        return "explain"

    # -----------------------------
    # Trend analysis
    # -----------------------------
    if any(k in q for k in TREND_KEYWORDS):
        return "trend"

    # -----------------------------
    # Ecosystem/environment fallback
    # -----------------------------
    if "ecosystem" in q or "environment" in q:
        return "explain"

    return "general"
