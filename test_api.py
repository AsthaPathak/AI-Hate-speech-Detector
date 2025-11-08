"""
Quick API Test Script
Tests if Flask server is running and responding correctly
"""

import requests
import json

API_URL = 'http://127.0.0.1:5000'

def test_predict_endpoint():
    """Test single text prediction"""
    print("=" * 50)
    print("Testing /predict endpoint...")
    print("=" * 50)
    
    test_cases = [
        "You are stupid and I hate you",  # Should be hate speech
        "This is a wonderful day!",        # Should be safe
        "I love this community",           # Should be safe
    ]
    
    for text in test_cases:
        try:
            response = requests.post(
                f'{API_URL}/predict',
                json={'text': text},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✓ Text: {text[:50]}...")
                print(f"  Label: {data['label']}")
                print(f"  Confidence: {data['confidence']}")
            else:
                print(f"\n✗ Error: Status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"\n✗ Connection Error: Is Flask server running?")
            print(f"  Start server with: python app.py")
            return False
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return False
    
    return True

def test_moderate_endpoint():
    """Test bulk moderation endpoint"""
    print("\n" + "=" * 50)
    print("Testing /moderate endpoint...")
    print("=" * 50)
    
    comments = [
        {"id": "1", "text": "You are an idiot and nobody likes you"},
        {"id": "2", "text": "Great post! Very informative"},
        {"id": "3", "text": "I hate you so much you stupid person"},
        {"id": "4", "text": "Thanks for sharing this helpful content"},
    ]
    
    try:
        response = requests.post(
            f'{API_URL}/moderate',
            json={'comments': comments},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            
            print(f"\n✓ Processed {len(results)} comments")
            
            hate_count = sum(1 for r in results if r['is_hate'])
            safe_count = len(results) - hate_count
            
            print(f"  Hate Speech: {hate_count}")
            print(f"  Safe: {safe_count}")
            
            for result in results:
                status = "🚫 HATE" if result['is_hate'] else "✓ SAFE"
                print(f"\n  {status} (ID: {result['id']})")
                print(f"    Text: {result['text'][:50]}...")
                print(f"    Confidence: {result['confidence']}")
            
            return True
        else:
            print(f"\n✗ Error: Status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Connection Error: Is Flask server running?")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def main():
    print("\n🔬 AI Moderator API Test")
    print("=" * 50)
    print(f"Testing API at: {API_URL}")
    print("=" * 50)
    
    # Test predict endpoint
    if not test_predict_endpoint():
        print("\n❌ /predict endpoint failed!")
        return
    
    # Test moderate endpoint
    if not test_moderate_endpoint():
        print("\n❌ /moderate endpoint failed!")
        return
    
    print("\n" + "=" * 50)
    print("✅ All API tests passed!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Reload Chrome extension at chrome://extensions/")
    print("2. Open test_page.html in Chrome")
    print("3. Check console (F12) for 'AI Moderator' messages")
    print("4. Wait 2-3 seconds for blur to apply")
    print("\nIf blur still doesn't work, see TROUBLESHOOTING.md")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
