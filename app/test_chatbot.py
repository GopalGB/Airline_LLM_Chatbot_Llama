from app.models.chatbot import AirlineChatbot

def test_chatbot_responses():
    """
    Test the chatbot for proper formatting and appropriate responses.
    """
    chatbot = AirlineChatbot()
    
    test_messages = [
        "Hello, I need help booking a flight",
        "What's the baggage policy?",
        "Can you check the status of flight AA123?",
        "I need help with wheelchair assistance"
    ]
    
    print("CHATBOT RESPONSE TEST\n" + "="*50)
    
    for message in test_messages:
        print(f"\nTEST MESSAGE: '{message}'")
        response = chatbot.process_message(message)
        print(f"RESPONSE:\n{response}")
        print("-"*50)
    
    print("\nTest complete! Check responses for formatting issues.")

if __name__ == "__main__":
    test_chatbot_responses()