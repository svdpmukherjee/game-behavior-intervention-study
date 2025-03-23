### Backend-FASTAPI-MONGODB

````markdown
# Backend FastAPI with MongoDB

This directory contains the backend service for the anagram game study, built with FastAPI and MongoDB.

## Setup and Configuration

### Environment Setup

1. Create and activate a virtual environment:

   ```bash
   # Using conda
   conda create -n <env name e.g. game_intervention_behavior>
   conda activate game_intervention_behavior

   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

   ```

3. Create a .env file in the root of this directory with the following variables:
   ```bash
   MONGODB_URI=mongodb://username:password@hostname:port/
   MONGODB_DB_NAME=your_database_name
   FRONTEND_URL=http://localhost:5173  # For local development
   # FRONTEND_URL=https://your-production-url.com  # For production
   ```

### Database Initialization

The init_database.py script initializes the MongoDB database with the necessary configuration for the game. This includes:

- Word puzzles and their solutions
- Word puzzles practice round
- Timing settings
- Reward structures
- Anti-cheating messages

To run the database initialization:

```bash
python init_database.py
```
````

Important: This will reset all collections in the database. The script will ask for confirmation before proceeding.

### Customizing Game Configuration

The game configuration is loaded from app/config/db_config.json. You can modify this file to customize various aspects of the game:

#### Game Anagrams

The game_config.game_anagrams section in db_config.json defines the word puzzles or anagrams used in the main game:

"game_anagrams": [
{
"word": "RECRATED",
"solutions": {
"8": ["CRATERED", "RECRATED", "RETRACED", "TERRACED"],
"7": ["CATERED", "CATERER", ...],
"6": ["CARDER", "CAREER", ...],
"5": ["ACRED", "ACTED", ...]
}
},
...
]

Each anagram is defined by the scrambled word and a dictionary of valid solutions
Solutions are organized by word length (5, 6, 7, 8 letters)
Add more anagrams by adding new objects to the array

#### Tutorial Anagrams

The game_config.tutorial_anagrams section defines the practice anagram:

"tutorial_anagrams": {
"word": "PRORATED",
"solutions": {
"8": ["PARROTED", "PREDATOR", ...],
"7": ["ADOPTER", "EARDROP", ...],
"6": ["ADORER", "DARTER", ...],
"5": ["ADEPT", "ADOPT", ...]
}
}

#### Time Settings

The time_settings section controls the time limits for different game phases:

"time_settings": {
"tutorial_time": 90, // Time in seconds for tutorial or practice round
"game_time": 180, // Time in seconds per anagram in main game
"survey_time": 300 // Time in seconds for survey completion
}

#### Rewards

The rewards section defines the points awarded for words of different lengths:

"rewards": {
"8": 15, // 15 pence for 8-letter words
"7": 10, // 10 pence for 7-letter words
"6": 5, // 5 pence for 6-letter words
"5": 2 // 2 pence for 5-letter words
}

#### Study Compensation

The study_compensation section defines the participant compensation structure:

"study_compensation": {
"prolific_rate": "£2.00", // Base compensation
"max_reward_per_anagram": 30 // Maximum bonus reward per anagram
}

#### Anti-Cheating Messages

The anti_cheating_messages array contains messages shown to discourage cheating:

"anti_cheating_messages": [
{
"id": "T1C1",
"theory": "Self-Determination Theory",
"text": "Each word puzzle you solve strengthens your abilities...",
"shown_count": 0
},
...
]

Each message has a unique id, theoretical basis (theory), and message content (text)
The shown_count is used by the system to track how many times each message has been displayed

### Running the Backend Server

Start the FastAPI server with:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

### Database Schema

The backend uses the following MongoDB collections:

- game_config: Stores game settings, anagrams, and rewards
- anti_cheating_messages: Stores intervention messages
- sessions: Stores participant session data
- game_events: Stores all game events and interactions
