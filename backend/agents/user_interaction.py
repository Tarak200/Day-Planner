# /backend/agents/user_interaction.py

class UserInteractionAgent:
    def handle_user_request(self, request):
        """Process user request and extract relevant details."""
        details = {
            'city': request.city,
            'date': request.date,
            'start_time': request.start_time,
            'end_time': request.end_time,
            'interests': request.interests,
            'budget': request.budget,
            'start_point': request.start_point or "City center"
        }
        return details
