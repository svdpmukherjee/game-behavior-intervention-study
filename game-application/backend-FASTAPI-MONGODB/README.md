# Backend FastAPI with MongoDB

This directory contains the backend service for the puzzle-solving game study, built with FastAPI and MongoDB.

## Directory Structure

```
backend-FASTAPI-MONGODB/
├── app/
│   ├── config/
│   │   ├── db_config.json     # Game configuration (anagrams, rewards, messages)
│   │   └── app_config.py      # Environment settings and URL configurations
│   ├── models/
│   │   └── schemas.py         # Pydantic schemas for data validation
│   └── main.py                # API endpoints implementation
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── init_database.py           # Database initialization script
└── README.md                  # This documentation
```

## Setup and Configuration

### Environment Setup

1. Create and activate a virtual environment:

   ```bash
   # Using conda
   conda create -n game_behavior_study python=3.12
   conda activate game_behavior_study

   # Or using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:

   ```
   MONGODB_URI=mongodb://username:password@hostname:port/
   MONGODB_DB_NAME=your_database_name
   ```

### Database Initialization

The `init_database.py` script initializes the MongoDB database with the necessary configuration for the game. This includes:

- Word puzzles (anagrams) and their solutions
- Tutorial/practice round anagram
- Timing settings
- Reward structures
- Motivational messages

To run the database initialization:

```bash
python init_database.py
```

**Important**: This will reset all collections in the database. The script will ask for confirmation before proceeding.

## API Endpoints

The backend provides the following API endpoints:

| Endpoint                  | Method | Description                               |
| ------------------------- | ------ | ----------------------------------------- |
| `/api/initialize-session` | POST   | Create a new user session                 |
| `/api/study-config`       | GET    | Get study configuration                   |
| `/api/tutorial/init`      | GET    | Initialize tutorial round                 |
| `/api/tutorial/complete`  | POST   | Complete tutorial round                   |
| `/api/game/init`          | GET    | Initialize main game with first anagram   |
| `/api/game/next`          | GET    | Get next anagram puzzle                   |
| `/api/game-events`        | POST   | Log user events and interactions          |
| `/api/word-submissions`   | POST   | Submit words for validation               |
| `/api/meanings/submit`    | POST   | Submit word meanings from post-game check |
| `/api/game-results`       | GET    | Get game results and statistics           |
| `/health`                 | GET    | Health check endpoint                     |

## Customizing Game Configuration

The game configuration is loaded from `app/config/db_config.json`. You can modify this file to customize various aspects of the game:

### Game Anagrams

The `game_config.game_anagrams` section defines the word puzzles used in the main game:

```json
"game_anagrams": [
  {
    "word": "TEADRCEN",
    "solutions": {
      "8": ["CANTERED", "CRENATED", "DECANTER", "RECANTED"],
      "7": ["ARDENTE", "CATERED", ...],
      "6": ["ANTEED", "ARDENT", ...],
      "5": ["ACNED", "ACRED", ...]
    }
  },
  ...
]
```

- Each anagram is defined by the scrambled word and a dictionary of valid solutions
- Solutions are organized by word length (5, 6, 7, 8 letters)
- Add more anagrams by adding new objects to the array

### Tutorial Anagram

The `game_config.tutorial_anagrams` section defines the practice anagram:

```json
"tutorial_anagrams": {
  "word": "PRORATED",
  "solutions": {
    "8": ["PARROTED", "PREDATOR", "PRORATED", "TEARDROP"],
    "7": ["ADOPTER", "EARDROP", ...],
    "6": ["ADORER", "DARTER", ...],
    "5": ["ADEPT", "ADOPT", ...]
  }
}
```

### Time Settings

The `time_settings` section controls the time limits for different game phases:

```json
"time_settings": {
  "tutorial_time": 60,  // Time in seconds for tutorial/practice round
  "game_time": 120,     // Time in seconds per anagram in main game
  "survey_time": 300    // Time in seconds for survey completion
}
```

### Rewards

The `rewards` section defines the points awarded for words of different lengths:

```json
"rewards": {
  "8": 8,  // 8 pence for 8-letter words
  "7": 6,  // 6 pence for 7-letter words
  "6": 4,  // 4 pence for 6-letter words
  "5": 2   // 2 pence for 5-letter words
}
```

### Study Compensation

The `study_compensation` section defines the participant compensation structure:

```json
"study_compensation": {
  "prolific_rate": "£2.00",      // Base compensation
  "max_reward_per_anagram": 25   // Maximum bonus reward per anagram
}
```

### Motivational Messages

The `motivational_messages` array contains messages shown to participants:

```json
"motivational_messages": [
  {
    "id": "autonomy_1",
    "theory": "Self-Determination Theory",
    "text": "Are you aware that it is up to you how you tackle these challenges?...",
    "shown_count": 0
  },
  ...
]
```

- Each message has a unique ID, theoretical basis (theory), and message content (text)
- The `shown_count` tracks how many times each message has been displayed
- Messages are based on various theories: Self-Determination Theory, Cognitive Dissonance Theory, and Social Norms Theory

## Running the Backend Server

Start the FastAPI server with:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

For API documentation, visit http://localhost:8000/docs

## CORS Configuration

The backend is configured to allow cross-origin requests from the following URLs:

- https://puzzle-solving-game-study.vercel.app (production)
- http://localhost:5173 (development)

These settings can be modified in `app/config/app_config.py`.

## Database Collections

The backend uses the following MongoDB collections:

- `game_config`: Stores game settings, anagrams, rewards, and time limits
- `motivational_messages`: Stores intervention messages shown to participants
- `sessions`: Stores participant session data including game progress
- `game_events`: Logs all participant interactions and game events

## Event Tracking

The backend tracks various events during the study:

- Game initialization and completion
- Word validations and submissions
- Page leave/return events
- Mouse inactivity periods
- Message displays
- Word meaning submissions
- Self-reported skill levels

This data is used to analyze participant behavior during the study.
