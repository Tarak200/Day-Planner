# /backend/models/request_models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class LLMRequest(BaseModel):
    conversation: List[Dict[str, str]]
    query: str


class TourRequest(BaseModel):
    city: str
    date: str  # Assuming date in ISO format, e.g., "2023-01-01"
    start_time: str
    end_time: str
    interests: List[str]
    budget: float
    start_point: Optional[str] = None
    user_id: Optional[str] = None  # For identifying user in memory agent

    class Config:
        schema_extra = {
            "example": {
                "city": "Rome",
                "date": "2023-11-10",
                "start_time": "09:00",
                "end_time": "18:00",
                "interests": ["historical sites", "food"],
                "budget": 150,
                "start_point": "Hotel Roma",
                "user_id": "12345"
            }
        }
