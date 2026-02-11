#!/usr/bin/env python3
"""
Simple test script to validate Gemini API key
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_api_key():
    """Test if the Gemini API key is working"""
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    print("🔑 Testing Gemini API Key...")
    print(f"📝 API Key: {API_KEY[:10]}..." if API_KEY else "❌ No API Key Found")
    
    if not API_KEY or API_KEY == "AIzaSyCabc123xyz987":
        print("❌ Invalid API key detected!")
        print("📝 Please get a valid key from: https://makersuite.google.com/app/apikey")
        return False
    
    # Try new API first
    try:
        print("\n🚀 Trying new google.genai package...")
        import google.genai as genai
        
        # Check what's available
        available_attrs = [attr for attr in dir(genai) if not attr.startswith('_')]
        print(f"🔍 Available attributes: {available_attrs[:5]}...")
        
        # Try direct configure
        if 'configure' in available_attrs:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            print("✅ Using direct configure method")
            
            response = model.generate_content("Hello, respond with just 'NEW API works'")
            
            if response and response.candidates:
                result = response.candidates[0].content.parts[0].text.strip()
                print(f"✅ New API Test Successful: {result}")
                return True
            else:
                print("❌ New API Test Failed: No response received")
        else:
            print("❌ configure method not available in new API")
            
    except Exception as e:
        print(f"❌ New API failed: {e}")
        
        # Fallback to deprecated API
        try:
            print("\n⚠️ Falling back to deprecated google.generativeai package...")
            import google.generativeai as genai_old
            genai_old.configure(api_key=API_KEY)
            model_old = genai_old.GenerativeModel("gemini-1.5-flash")
            
            response = model_old.generate_content("Hello, respond with just 'OLD API works'")
            
            if response and response.candidates:
                result = response.candidates[0].content.parts[0].text.strip()
                print(f"✅ Deprecated API Test Successful: {result}")
                print("⚠️ Consider upgrading to new google.genai package")
                return True
            else:
                print("❌ Deprecated API Test Failed: No response received")
                
        except Exception as e2:
            print(f"❌ Deprecated API Also Failed: {e2}")
            
            if "API key" in str(e).lower() or "API key" in str(e2).lower():
                print("🔧 This appears to be an API key issue.")
                print("📝 Please check your key at: https://makersuite.google.com/app/apikey")
            
            return False
    
    return False

if __name__ == "__main__":
    success = test_api_key()
    
    if success:
        print("\n🎉 API Key is working! AI Care should function normally.")
    else:
        print("\n🚨 API Key issue found! Check the error messages above.")
        print("💡 Try installing: pip install google-genai")
        print("🔧 Fix the API key to get full AI functionality.")
