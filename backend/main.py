# /backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.api import router as api_router # This uses the router setup in /backend/core/api.py
from utils import config  # This imports our configuration settings

app = FastAPI(title="Tour Planning Assistant", version="1.0")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This can be configured to more restrictive settings
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict to ['GET', 'POST', 'DELETE', etc.]
    allow_headers=["*"],
)

# Including the API router that handles all the agent interactions
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
