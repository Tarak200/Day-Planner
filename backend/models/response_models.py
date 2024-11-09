# /backend/models/response_models.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ItineraryItem(BaseModel):
    place: str
    time: str
    description: Optional[str] = None

class LLMResponse(BaseModel):
    response: str


class TourResponse(BaseModel):
    user_details: Dict[str, Any]
    weather: str
    news: List[str]
    optimized_route: str
    itinerary: List[ItineraryItem]

    class Config:
        schema_extra = {
            "example": {
                "user_details": {
                    "city": "Rome",
                    "date": "2023-11-10",
                    "interests": ["historical sites", "food"],
                    "budget": 150,
                    "start_point": "Hotel Roma"
                },
                "weather": "Sunny",
                "news": ["Local festival starting next week"],
                "optimized_route": "Optimized route based on interests and budget.",
                "itinerary": [
                    {
                        "place": "Colosseum",
                        "time": "09:00 - 10:30",
                        "description": "Guided tour of ancient amphitheatre."
                    },
                    {
                        "place": "Roman Forum",
                        "time": "11:00 - 12:30",
                        "description": "Explore the heart of ancient Rome."
                    }
                ]
            }
        }
