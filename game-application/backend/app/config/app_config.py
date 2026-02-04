"""
Configuration module for the application.
Contains environment settings and URL configurations.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Base URLs configuration
def get_cors_origins():
    """Get CORS origins based on environment."""
    # Production URL - update this with your Production frontend URL
    production_url = "https://anagram-solving-game-study.vercel.app"
    
    # Local URL - for development locally
    local_url = "http://localhost:5173"
    
    # Return both to support multiple environments
    return [production_url, local_url]

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

# Validate required configuration
if not MONGODB_URI or not MONGODB_DB_NAME:
    raise ValueError("MongoDB environment variables (MONGODB_URI, MONGODB_DB_NAME) must be set")