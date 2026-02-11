#!/usr/bin/env python3
"""
Check what models are available in Gemini API
"""

import os
from dotenv import load_dotenv
load_dotenv()

def check_models():
    """Check available models in Gemini API"""
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not API_KEY:
        print("❌ GEMINI_API_KEY not found")
        return
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        
        print("🔍 Checking available models...")
        
        # Try to list models (if available)
        try:
            models = genai.list_models()
            print("📱 Available models:")
            for model in models:
                print(f"  - {model.name}")
        except:
            print("❌ list_models not available in deprecated API")
        
        # Test common model names
        test_models = [
            "gemini-1.5-flash",
            "gemini-pro", 
            "gemini-1.0-flash",
            "gemini-pro-vision",
            "gemini-1.5-pro"
        ]
        
        for model_name in test_models:
            try:
                print(f"\n🔍 Testing model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Test")
                
                if response and response.candidates:
                    result = response.candidates[0].content.parts[0].text.strip()
                    print(f"✅ {model_name} works: {result}")
                    return model_name
                else:
                    print(f"❌ {model_name} failed")
                    
            except Exception as e:
                print(f"❌ {model_name} error: {e}")
                
        print("\n❌ No working models found!")
        
    except Exception as e:
        print(f"❌ Failed to check models: {e}")

if __name__ == "__main__":
    check_models()
