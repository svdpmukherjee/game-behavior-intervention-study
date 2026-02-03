# Backend - FastAPI with MongoDB

REST API service for the word puzzle behavioral study.

## Setup

```bash
# Create virtual environment
conda create -n game_study python=3.12
conda activate game_study

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy from .env.example)
cp .env.example .env
# Edit .env with your MongoDB credentials

# Initialize database
python init_database.py

# Start server
uvicorn app.main:app --reload --port 8000
```

API documentation: http://localhost:8000/docs

## Directory Structure

```
backend/
├── app/
│   ├── config/
│   │   ├── db_config.json   # Game config (puzzles, rewards, messages)
│   │   └── app_config.py    # CORS and environment settings
│   ├── models/schemas.py    # Pydantic data models
│   └── main.py              # API endpoints
├── init_database.py         # Database initialization
└── requirements.txt
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/initialize-session` | POST | Create participant session |
| `/api/tutorial/init` | GET | Get tutorial puzzle |
| `/api/tutorial/complete` | POST | Submit tutorial results |
| `/api/game/init` | GET | Get main game + intervention message |
| `/api/game/next` | GET | Get next puzzle |
| `/api/word-submissions` | POST | Submit words for validation |
| `/api/game-events` | POST | Log behavioral events |
| `/api/meanings/submit` | POST | Submit word meanings |
| `/api/game-results` | GET | Get final results |
| `/health` | GET | Health check |

## Game Configuration

Edit `app/config/db_config.json` to customize:

**Puzzles**: Add anagrams with solutions organized by word length (5-8 letters)

**Time Settings**:
```json
"time_settings": {
  "tutorial_time": 60,
  "game_time": 120
}
```

**Rewards** (pence per word):
```json
"rewards": { "8": 8, "7": 6, "6": 4, "5": 2 }
```

**Messages**: Theory-based intervention messages (SDT, CDT, SNT)

## Database Collections

- `game_config` - Puzzles, timing, rewards
- `motivational_messages` - Intervention messages
- `sessions` - Participant data and progress
- `game_events` - Behavioral event logs
- `user_interactions` - Mouse/interaction tracking
