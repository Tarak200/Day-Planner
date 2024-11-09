# /backend/utils/config.py
import os

class Config:
    # Load sensitive data from environment variables
    API_KEY = os.getenv('API_KEY', 'your_default_api_key')
    DATABASE_URL = os.getenv('DATABASE_URL', 'bolt://localhost:7687')
    DATABASE_USER = os.getenv('DATABASE_USER', 'neo4j')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')

    # Other configurations
    MODEL_NAME = 'gpt-3'
    TOKENIZER_NAME = 'gpt-3'
    MAX_LENGTH = 100
    NUM_RETURN_SEQUENCES = 1
