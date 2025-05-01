import requests
import json
from app.core.config import OPENROUTER_API_KEY, OPENROUTER_API_URL, MODEL_NAME, TEMPERATURE, MAX_TOKENS

def call_llama_api(messages, system_prompt=None):
    """
    Call the LLaMa-2-7B model through OpenRouter API
    
    Args:
        messages: List of conversation messages
        system_prompt: Optional system prompt to guide the model behavior
    
    Returns:
        The model's response text
    """
    # Prepare headers with API key
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  # Your website URL
        "X-Title": "Airline Customer Service Chatbot"  # Optional, shows in stats
    }
    
    # Prepare the conversation history in the format expected by OpenRouter
    conversation = []
    
    # Add system prompt if provided
    if system_prompt:
        conversation.append({
            "role": "system",
            "content": system_prompt
        })
    
    # Add all conversation messages
    for message in messages:
        conversation.append({
            "role": message["role"],
            "content": message["content"]
        })
    
    # Prepare the request payload
    payload = {
        "model": MODEL_NAME,
        "messages": conversation,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS
    }
    
    try:
        # Make the API call
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        
        # Extract and return the generated text
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "I'm sorry, I couldn't generate a response at the moment."
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter API: {e}")
        return "I'm sorry, there was an error connecting to my brain. Please try again later."