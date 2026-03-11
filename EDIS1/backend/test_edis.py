#!/usr/bin/env python3
"""
Test script to verify EDIS backend functionality
"""

import requests
import json
import time

API_BASE = "http://127.0.0.1:8000/api"

def test_all_indicators():
    """Test all 5 ecosystem indicators"""
    print("Testing EDIS Backend - All 5 Indicators")
    print("=" * 50)
    
    # Test location (Delhi)
    lat, lon = 28.6139, 77.2090
    
    endpoints = [
        ("/analyze/climate", "climate_stress_0_100"),
        ("/analyze/soil", "soil_stress_0_100"),
        ("/analyze/vegetation", "vegetation_stress_0_100"),
        ("/analyze/human-pressure", "human_pressure_stress"),
        ("/analyze/biodiversity", "biodiversity_stress")
    ]
    
    results = {}
    
    for endpoint, key in endpoints:
        try:
            print(f"\nTesting {endpoint}...")
            response = requests.post(
                f"{API_BASE}{endpoint}",
                json={"latitude": lat, "longitude": lon},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if key in data:
                    results[key] = data[key]
                    print(f"✅ {key}: {data[key]}")
                else:
                    print(f"❌ Missing key {key} in response")
                    print(f"Response: {data}")
            else:
                print(f"❌ Status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\nResults Summary:")
    print("=" * 30)
    for key, value in results.items():
        print(f"{key}: {value}")
    
    print(f"\nTotal indicators returned: {len(results)}/5")
    
    if len(results) == 5:
        print("✅ SUCCESS: All 5 indicators working!")
        return True
    else:
        print("❌ FAILURE: Missing indicators")
        return False

def test_ecosystem_analysis():
    """Test ecosystem analysis endpoint"""
    print("\n\nTesting Ecosystem Analysis")
    print("=" * 30)
    
    try:
        # Start analysis
        response = requests.post(
            f"{API_BASE}/analyze/ecosystem/start",
            json={"latitude": 28.6139, "longitude": 77.2090},
            timeout=30
        )
        
        if response.status_code == 200:
            task_data = response.json()
            task_id = task_data["task_id"]
            print(f"✅ Analysis started: {task_id}")
            
            # Check status
            for _ in range(10):
                response = requests.get(f"{API_BASE}/analyze/ecosystem/status/{task_id}")
                if response.status_code == 200:
                    status_data = response.json()
                    if status_data["status"] == "completed":
                        print("✅ Analysis completed!")
                        print(f"Ecosystem data: {json.dumps(status_data['analysis'], indent=2)}")
                        return True
                    else:
                        print(f"Status: {status_data['status']}")
                        time.sleep(1)
                else:
                    print(f"❌ Status check failed: {response.text}")
                    break
        else:
            print(f"❌ Failed to start analysis: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("EDIS Backend Test Suite")
    print("=" * 50)
    
    # Test individual indicators
    indicators_ok = test_all_indicators()
    
    # Test ecosystem analysis
    ecosystem_ok = test_ecosystem_analysis()
    
    print("\n\nFINAL RESULTS")
    print("=" * 30)
    print(f"Individual Indicators: {'✅ PASS' if indicators_ok else '❌ FAIL'}")
    print(f"Ecosystem Analysis: {'✅ PASS' if ecosystem_ok else '❌ FAIL'}")
    
    if indicators_ok and ecosystem_ok:
        print("\n🎉 ALL TESTS PASSED! EDIS is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
