# /backend/core/api.py
from fastapi import APIRouter, Depends, HTTPException
from models.request_models import TourRequest
from models.response_models import TourResponse  # Assuming you create this model
from agents.user_interaction import UserInteractionAgent
from agents.itinerary_generation import ItineraryGenerationAgent
from agents.optimization import OptimizationAgent
from agents.weather import WeatherAgent
from agents.news import NewsAgent
from agents.memory import MemoryAgent

router = APIRouter()

# Dependency functions
def get_user_agent():
    return UserInteractionAgent()

def get_itinerary_agent():
    return ItineraryGenerationAgent()

def get_optimization_agent():
    return OptimizationAgent()

def get_weather_agent():
    return WeatherAgent()

def get_news_agent():
    return NewsAgent()

def get_memory_agent():
    return MemoryAgent(uri="bolt://localhost:7687", user="neo4j", password="password")

from fastapi import APIRouter, HTTPException
from models.request_models import LLMRequest  # You need to define this model
from models.response_models import LLMResponse  # And this one
from services.llm_service import LLMService  # Ensure this service exists

router = APIRouter()

llm_service = LLMService()

# /backend/core/api.py
from fastapi import APIRouter, HTTPException
from models.request_models import LLMRequest
from models.response_models import LLMResponse
from services.llm_service import LLMService

router = APIRouter()

# Initialize the LLMService instance
llm_service = LLMService()

@router.post("/api/llm", response_model=LLMResponse)
async def llm_endpoint(request: LLMRequest):
    try:
        print("$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(request)
        print("$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # Call the async process_request method
        response = await llm_service.process_request(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan-tour/", response_model=TourResponse)  # Correct response model
async def plan_tour(request: TourRequest, 
                    user_agent: UserInteractionAgent = Depends(get_user_agent),
                    itinerary_agent: ItineraryGenerationAgent = Depends(get_itinerary_agent),
                    optimization_agent: OptimizationAgent = Depends(get_optimization_agent),
                    weather_agent: WeatherAgent = Depends(get_weather_agent),
                    news_agent: NewsAgent = Depends(get_news_agent),
                    memory_agent: MemoryAgent = Depends(get_memory_agent)):
    try:
        user_details = user_agent.handle_user_request(request)
        weather_info = await weather_agent.fetch_weather(request.city, request.date)
        news = await news_agent.fetch_local_news(request.city)
        optimized_route = optimization_agent.optimize_route(request.city, request.interests, request.budget)
        itinerary = itinerary_agent.generate_itinerary(user_details)

        # Optionally store user details in memory
        memory_agent.remember_preferences(request.user_id, user_details)

        return {
            "user_details": user_details,
            "weather": weather_info,
            "news": news,
            "optimized_route": optimized_route,
            "itinerary": itinerary
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

