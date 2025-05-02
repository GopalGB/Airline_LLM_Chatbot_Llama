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
        You are AirBuddy, a professional airline customer service chatbot.

        FORMATTING RULES:
        1. DO NOT use asterisks (**) around text
        2. DO NOT include meta-instructions or "waiting for response" type phrases
        3. DO NOT number your response options unless specifically asked
        4. Write in a natural, conversational style
        5. Be direct and concise
        6. USE SHORT PARAGRAPHS with line breaks between them
        7. If listing options, put each option on a new line with a dash (-)
        8. Keep responses under 4-5 short paragraphs maximum

        You are an AI assistant for an airline company. 
        Your role is to help customers with their travel needs in a friendly, professional manner.

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

        Always end your response by asking if there's anything else you can help with related to air travel.
        
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
        
        # Clean, format, and filter the response
        cleaned_response = self.clean_response(response)
        formatted_response = self.format_response(cleaned_response)
        filtered_response = self.filter_response(formatted_response)
        
        # Add bot response to conversation history
        self.memory.add_message("assistant", filtered_response)
        
        return filtered_response
    
    def clear_conversation(self):
        """
        Clear the current conversation history.
        """
        self.memory.clear()
        return "Conversation history cleared. How can I help you with your travel plans today?"

    def clean_response(self, response):
        """
        Clean the response to remove unwanted formatting and instructions.
        
        Args:
            response: The raw model response
            
        Returns:
            Cleaned response
        """
        # Remove asterisks
        cleaned = re.sub(r'\*\*', '', response)
        
        # Remove meta-instructions like "Your Input:", "Waiting for Your Response..."
        patterns_to_remove = [
            r'--- Waiting for Your Response\.\.\.', 
            r'Your Input:', 
            r'Awaiting Your First Step\.\.\.', 
            r'After You Respond:',
            r'Your Turn!',
            r'REAL ENDING THIS TIME:',
            r'Example Responses to Get You Started:'
        ]
        
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Remove numbered instructions
        cleaned = re.sub(r'\d\. \*\*.*?\*\*', '', cleaned)
        
        # Clean up double spaces and extra newlines
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned.strip()
    
    def format_response(self, response):
        """
        Improve the formatting of the response for better readability.
        
        Args:
            response: The cleaned response
            
        Returns:
            Formatted response
        """
        # Ensure there are proper line breaks after sentences
        formatted = response
        
        # Make sure list items are on new lines
        formatted = re.sub(r'- ([^\n])', r'- \1', formatted)
        
        # Add line breaks after questions
        formatted = re.sub(r'(\?)\s+([A-Z])', r'\1\n\n\2', formatted)
        
        # Ensure there's a max of one empty line between paragraphs
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        
        # Break long paragraphs (more than 150 chars without breaks)
        sentences = re.split(r'(?<=[.!?])\s+', formatted)
        result = []
        current_paragraph = ""
        
        for sentence in sentences:
            if len(current_paragraph) + len(sentence) > 150 and current_paragraph:
                result.append(current_paragraph.strip())
                current_paragraph = sentence
            else:
                if current_paragraph:
                    current_paragraph += " " + sentence
                else:
                    current_paragraph = sentence
        
        if current_paragraph:
            result.append(current_paragraph.strip())
        
        # Join with proper paragraph breaks
        formatted = "\n\n".join(result)
        
        return formatted
    
    def filter_response(self, response):
        """
        Filter the response to ensure it's appropriate.
        
        Args:
            response: The model's response
            
        Returns:
            Filtered response
        """
        # List of inappropriate words to check for
        inappropriate_words = ["****", "[profanity]", "[inappropriate content]", "[offensive content]"]
        
        # Check if any inappropriate words are in the response
        for word in inappropriate_words:
            if word in response:
                return "I apologize, but I need to provide a new response. As your airline assistant, I'm here to help with your travel needs. How can I assist you with your flight or travel arrangements today?"
        
        return response