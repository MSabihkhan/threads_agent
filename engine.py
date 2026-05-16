from Zernoi import post 
from OpenRouter import call_openrouter

def run_(user_message):
    system_prompt = "You are a helpful assistant that creates engaging social media posts strictly under 500 characters based on user input."
    
    # 1. Get the text back from the AI
    ai_response = call_openrouter(system_prompt, user_message)
    print(f"AI response: {ai_response}")
    
    # 2. Check if the AI responded with a valid message
    if not ai_response or "Error" in ai_response:
        print("AI failed to generate a valid post text.")
        return "Post failed: AI generation error."
        
    # 3. Pass it to your post function
    print("AI generated text successfully. Attempting to post to Zernoi...")
    response = post(ai_response)
    print(f"Zernoi response: {response}")
    
    # 4. FIX: Check 'success' directly since Zernoi explicitly provides it
    if response.get('success') is True:
        # Safely extract status for printing logs
        status_val = response.get('status')
        print(f"Post successful! ID: {response.get('id')}, Status: {status_val}")
        
        reply = f"Post successful!\n\n{ai_response}"
    else:
        # Handles cases where success is False or missing entirely
        error_msg = response.get('error', 'Unknown error')
        print(f"Post failed. Error: {error_msg}")
        reply = f"Post failed: {error_msg}"
        
    return reply