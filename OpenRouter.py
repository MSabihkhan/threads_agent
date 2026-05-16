import requests
import os
from dotenv import load_dotenv
load_dotenv()

def call_openrouter(system_prompt, user_message, model="baidu/cobuddy:free"):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('OPEN_ROUTER_KEY')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    
    print("Sending request...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)  # 30 sec timeout
        print(f"Status: {response.status_code}")
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        return "Error: Request timed out after 30 seconds"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}\nResponse: {response.text if 'response' in locals() else 'No response'}"
