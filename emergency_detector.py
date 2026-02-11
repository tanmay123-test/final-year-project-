import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SAFETY_KEYWORDS = [
    "chest pain", "can't breathe", "shortness of breath",
    "stroke", "unconscious", "heavy bleeding",
    "heart attack", "seizure"
]


def is_emergency(text: str) -> bool:
    text_lower = text.lower()

    # 🛡️ Step 1 — Safety keyword backup
    for word in SAFETY_KEYWORDS:
        if word in text_lower:
            return True

    # 🤖 Step 2 — Ask AI severity dynamically
    try:
        prompt = f"""
Is this a medical emergency?

Symptoms: {text}

Answer only YES or NO.
"""

        response = model.generate_content(prompt)
        answer = response.text.strip().lower()

        return "yes" in answer

    except:
        return False
