import sys
import google.genai as genai
from google.genai.errors import APIError

def check_api_key(api_key):
    model_name = 'gemini-3.1-flash-lite'
    try:
        # Client सेटअप गर्ने
        client = genai.Client(api_key=api_key)
        
        print(f"\nगुगलको सर्भरमा चेक गरिँदैछ... [Model: {model_name}]")
        
        # एउटा सानो टेक्स्ट पठाएर चेक गर्ने
        response = client.models.generate_content(
            model=model_name,
            contents="Hello! Are you working?"
        )
        
        print("\n✅ सफलता! यो API Key एकदम सही छ र यसमा अझै लिमिट बाँकी छ।")
        print(f"गुगलको जवाफ: {response.text}")
        
    except APIError as e:
        error_msg = str(e)
        if '429' in error_msg or 'Quota' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg:
            print("\n❌ एरर: यो API Key को आजको लिमिट (Quota) पूर्ण रूपमा सकिसकेको छ!")
            print("कृपया भोलिसम्म कुर्नुहोस् वा नयाँ Key प्रयोग गर्नुहोस्।")
        elif 'API_KEY_INVALID' in error_msg or '400' in error_msg:
            print("\n❌ एरर: तपाईंले हाल्नुभएको API Key गलत छ। कृपया राम्ररी कपी गरेर हाल्नुहोला।")
        else:
            print(f"\n❌ अन्य एरर आयो: {error_msg}")
    except Exception as e:
        print(f"\n❌ इन्टरनेट वा अन्य समस्या: {e}")

if __name__ == "__main__":
    print("========================================")
    print("API Key चेक गर्ने सफ्टवेयर")
    print("========================================")
    user_key = input("कृपया आफ्नो API Key यहाँ पेस्ट गर्नुहोस्: ").strip()
    
    if user_key:
        check_api_key(user_key)
    else:
        print("तपाईंले कुनै API Key हाल्नुभएन!")
