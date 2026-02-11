"""
Simple Gemini API test script
Run: python test_gemini.py
"""

import os
from dotenv import load_dotenv

load_dotenv()


def test_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    print("🔑 Testing Gemini API Key...\n")

    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env")
        return False

    print(f"📝 Key loaded: {api_key[:10]}...\n")

    # Try deprecated but stable SDK (what your project uses)
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            "Reply ONLY with: Gemini API is working"
        )

        text = response.candidates[0].content.parts[0].text.strip()
        print("✅ SUCCESS!")
        print("🤖 Response:", text)
        return True

    except Exception as e:
        print("❌ Gemini test failed:")
        print(e)
        return False


if __name__ == "__main__":
    if test_api_key():
        print("\n🎉 Gemini is working correctly!")
    else:
        print("\n🚨 Fix your API key before continuing.")
