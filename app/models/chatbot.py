from app.utils.api_client import call_llama_api
from app.memory.conversation_memory import ConversationMemory
from app.core.config import AIRLINE_TOPICS
import re

class AirlineChatbot:
    """
    A chatbot specialized in airline customer service.
    """
    
    def __init__(self):
        # Initialize conversation memory
        self.memory = ConversationMemory()
        
        # Create a system prompt that gives the chatbot its personality and knowledge
        self.system_prompt = """
        You are an AI assistant for an airline company. 
        Your name is AirBuddy and your job is to help customers with their travel needs.
        
        Be friendly, helpful, and concise in your responses.
        If you don't know something, admit it rather than making things up.
        
        You can help with:
        - Flight bookings and information
        - Check-in procedures
        - Baggage policies
        - Flight status updates
        - Frequent flyer programs
        - In-flight services
        - Special assistance requests
        - Cancellation and refund policies
        - Airport information
        
        Always end your response by asking if there's anything else you can help with.
        """
    
    def extract_user_info(self, message):
        """
        Extract useful information about the user from their message.
        
        Args:
            message: The user's message
        """
        # Look for flight numbers (like AA123, DL456)
        flight_match = re.search(r'\b([A-Z]{2}|[A-Z]\d|\d[A-Z])\s*(\d{1,4})\b', message)
        if flight_match:
            flight_number = flight_match.group(0).replace(" ", "")
            self.memory.store_user_info("flight_number", flight_number)
        
        # Look for travel dates
        date_matches = re.findall(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?(?:\s*,\s*\d{4})?\b', message, re.IGNORECASE)
        if date_matches:
            self.memory.store_user_info("travel_date", date_matches[0])
        
        # Look for destinations (simple approach - would need to be expanded with a real database)
        cities = ["New York", "Los Angeles", "Chicago", "Miami", "Dallas", "Atlanta", 
                  "San Francisco", "Seattle", "Denver", "Boston", "Las Vegas", "Orlando",
                  "London", "Paris", "Tokyo", "Sydney", "Dubai", "Singapore"]
        
        for city in cities:
            if city.lower() in message.lower():
                self.memory.store_user_info("destination", city)
                break
    
    def process_message(self, user_message):
        """
        Process a user message and generate a response.
        
        Args:
            user_message: The message from the user
            
        Returns:
            The chatbot's response
        """
        # Extract any user information from the message
        self.extract_user_info(user_message)
        
        # Add user message to conversation history
        self.memory.add_message("user", user_message)
        
        # Get user context for more personalized responses
        user_context = self.memory.get_user_context()
        
        # Create a custom system prompt that includes user context if available
        custom_system_prompt = self.system_prompt
        if user_context:
            custom_system_prompt += f"\n\nUser Information: {user_context}"
        
        # Call the LLaMa API with the conversation history and custom system prompt
        response = call_llama_api(
            self.memory.get_conversation_history(),
            system_prompt=custom_system_prompt
        )
        
        # Add bot response to conversation history
        self.memory.add_message("assistant", response)
        
        return response
    
    def clear_conversation(self):
        """
        Clear the current conversation history.
        """
        self.memory.clear()
        return "Conversation history cleared. How can I help you with your travel plans today?"