from Zernoi import post 
from OpenRouter import call_openrouter

def run_(user_message):
    system_prompt = "You are a helpful assistant that creates engaging social media posts based on user input."
    
    # 1. Get the text back from the AI
    ai_response = call_openrouter(system_prompt, user_message)
    print(f"AI response: {ai_response}")
    
    # 2. Check if the AI responded with a valid message (not None, not empty, and didn't return an error string)
    if not ai_response or "Error" in ai_response:
        print("AI failed to generate a valid post text.")
        return f"Post failed: AI generation error."
        
    # 3. Since we have a valid AI message, pass it to your post function
    print("AI generated text successfully. Attempting to post to Zernoi...")
    response = post(ai_response)
    print(f"Zernoi response: {response}")
    # 4. NOW look at the status code returned by the POST function
    try:
        status_code = int(response.get("status", 0))
    except (ValueError, TypeError, AttributeError):
        status_code = 0  
    
    # 5. Check if the Zernoi server accepted your post request
    if 201 <= status_code < 300:
        print(f"Post successful! ID: {response.get('id')}, Status: {status_code}")
        if response.get('success'):
            reply = f"Post successful!\n\n{ai_response}"
        else:
            reply = f"Post failed: {response.get('error', 'Unknown error')}"
    else:
        print(f"Post failed with status code: {status_code}, Error: {response.get('error')}")
        reply = f"Post failed: {response.get('error', 'Unknown error')}"
        
    return reply