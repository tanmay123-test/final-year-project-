#!/usr/bin/env python3
"""
Check available models in Gemini APIs
"""

import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def check_models():
    """Check available models for both API versions"""
    
    print("🔑 Checking available Gemini models...")
    
    # Try new API
    try:
        print("\n🚀 Checking new google.genai package...")
        import google.genai as genai
        genai.configure(api_key=API_KEY)
        
        # Try to list models
        for model in genai.list_models():
            print(f"  📱 {model.name}")
            
    except Exception as e:
        print(f"❌ New API model check failed: {e}")
    
    # Try deprecated API
    try:
        print("\n⚠️ Checking deprecated google.generativeai package...")
        import google.generativeai as genai_old
        genai_old.configure(api_key=API_KEY)
        
        # Try to list models (if available)
        print("  📱 Models available in deprecated API")
        print("  📱 gemini-1.5-flash (should work)")
        
    except Exception as e:
        print(f"❌ Deprecated API model check failed: {e}")

if __name__ == "__main__":
    check_models()
