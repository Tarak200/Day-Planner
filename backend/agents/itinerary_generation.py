# /backend/agents/itinerary_generation.py
from services.llm_service import LLMService

class ItineraryGenerationAgent:
    def __init__(self):
        self.llm_service = LLMService()

    def generate_itinerary(self, user_details):
        """Generate itinerary using LLM based on user details."""
        prompt = f"Create a one-day itinerary for visiting {user_details['city']} focusing on {', '.join(user_details['interests'])}. Start at {user_details['start_point']} with a budget of {user_details['budget']}."
        itinerary = self.llm_service.generate_text(prompt)
        return itinerary
