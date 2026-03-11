#!/usr/bin/env python3
"""
Test Groq integration for EDIS Assistant
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_groq_integration():
    """Test Groq API integration"""
    print("Testing Groq Integration for EDIS Assistant")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "gsk_your_groq_api_key_here":
        print("❌ Please set GROQ_API_KEY in your .env file")
        print("See GROQ_SETUP.md for instructions")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        # Test basic API call
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": "What is ecosystem health in one sentence?"}
            ],
            max_tokens=50
        )
        
        print("✅ Groq API connection successful")
        print(f"Response: {response.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Groq API error: {e}")
        return False

def test_edis_assistant():
    """Test EDIS Assistant with Groq"""
    print("\nTesting EDIS Assistant with Groq")
    print("=" * 40)
    
    try:
        from edis_assistant.chat_engine import ask_edis_assistant
        
        # Test with ecosystem context
        result = ask_edis_assistant(
            user_query="What are the main environmental risks here?",
            context="LOCATION: Test City\nECOSYSTEM STRESS INDEX: 65.2\nSTRESS INDICATORS:\n- Climate Stress: 45.0%\n- Soil Stress: 70.0%\n- Vegetation Stress: 60.0%\n- Human Pressure: 80.0%\n- Biodiversity Stress: 55.0%",
            chat_history=[],
            model="llama3-70b-8192"
        )
        
        print("✅ EDIS Assistant working with Groq")
        print(f"Response: {result['text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ EDIS Assistant error: {e}")
        return False

if __name__ == "__main__":
    print("EDIS Groq Integration Test")
    print("=" * 30)
    
    # Test basic Groq connection
    groq_ok = test_groq_integration()
    
    if groq_ok:
        # Test EDIS Assistant
        assistant_ok = test_edis_assistant()
        
        print("\nFinal Results:")
        print("=" * 20)
        print(f"Groq API: {'✅ PASS' if groq_ok else '❌ FAIL'}")
        print(f"EDIS Assistant: {'✅ PASS' if assistant_ok else '❌ FAIL'}")
        
        if groq_ok and assistant_ok:
            print("\n🎉 Groq integration successful!")
            print("EDIS Assistant is ready with Groq API.")
        else:
            print("\n⚠️  Some tests failed. Check the errors above.")
    else:
        print("\n❌ Please configure Groq API key first (see GROQ_SETUP.md)")
