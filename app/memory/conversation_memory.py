from app.core.config import MAX_HISTORY_LENGTH

class ConversationMemory:
    """
    Manages the conversation history and context for the chatbot.
    """
    
    def __init__(self):
        # Initialize empty conversation history
        self.conversation_history = []
        self.user_info = {}
        
    def add_message(self, role, content):
        """
        Add a new message to the conversation history.
        
        Args:
            role: The role of the message sender (user or assistant)
            content: The content of the message
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Keep only the most recent messages based on MAX_HISTORY_LENGTH
        if len(self.conversation_history) > MAX_HISTORY_LENGTH:
            # Remove the oldest message
            self.conversation_history.pop(0)
    
    def get_conversation_history(self):
        """
        Get the current conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history
    
    def store_user_info(self, key, value):
        """
        Store information about the user.
        
        Args:
            key: The type of information (e.g., "name", "flight_number")
            value: The value of the information
        """
        self.user_info[key] = value
    
    def get_user_info(self, key):
        """
        Retrieve information about the user.
        
        Args:
            key: The type of information to retrieve
            
        Returns:
            The value of the information, or None if not found
        """
        return self.user_info.get(key)
    
    def get_user_context(self):
        """
        Create a summary of user information for context.
        
        Returns:
            A string summarizing what we know about the user
        """
        if not self.user_info:
            return ""
        
        context_parts = []
        
        # Add each piece of information we have about the user
        for key, value in self.user_info.items():
            if key == "name":
                context_parts.append(f"User's name is {value}.")
            elif key == "destination":
                context_parts.append(f"User is traveling to {value}.")
            elif key == "flight_number":
                context_parts.append(f"User's flight number is {value}.")
            elif key == "travel_date":
                context_parts.append(f"User is traveling on {value}.")
            else:
                context_parts.append(f"User's {key} is {value}.")
                
        return " ".join(context_parts)
    
    def clear(self):
        """
        Clear the conversation history and user information.
        """
        self.conversation_history = []
        self.user_info = {}