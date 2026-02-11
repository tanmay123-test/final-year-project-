#!/usr/bin/env python3
"""
Test script using deprecated API that we know works
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_api_key():
    """Test if Gemini API key is working with deprecated API"""
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    print("🔑 Testing Gemini API Key (Deprecated Method)...")
    print(f"📝 API Key: {API_KEY[:10]}..." if API_KEY else "❌ No API Key Found")
    
    if not API_KEY or API_KEY == "AIzaSyCabc123xyz987":
        print("❌ Invalid API key detected!")
        print("📝 Please get a valid key from: https://makersuite.google.com/app/apikey")
        return False
    
    # Use deprecated API (which we know works)
    try:
        print("\n⚠️ Using deprecated google.generativeai package (stable)...")
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        
        # Try different model names
        models_to_try = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.5-pro", "gemini-flash-latest"]
        
        for model_name in models_to_try:
            try:
                print(f"🔍 Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content("Reply ONLY with: Working!")
                
                if response and response.candidates:
                    result = response.candidates[0].content.parts[0].text.strip()
                    print(f"✅ API Test Successful with {model_name}: {result}")
                    return True
                else:
                    print(f"❌ Model {model_name} failed: No response received")
                    
            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue
                
        print("❌ All models failed!")
        return False
                
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        
        if "API key" in str(e).lower():
            print("🔧 This appears to be an API key issue.")
            print("📝 Please check your key at: https://makersuite.google.com/app/apikey")
        
        return False
    
    return False

if __name__ == "__main__":
    success = test_api_key()
    
    if success:
        print("\n🎉 API Key is working! AI Care should function normally.")
        print("🚀 Ready for conversational AI testing!")
    else:
        print("\n🚨 API Key issue found! Check the error messages above.")
        print("🔧 Fix the API key to get full AI functionality.")
