# Game Behavior Intervention Study - Web Application

This repository contains a full-stack application for conducting a word puzzle game experiment designed to study user behavior and the effectiveness of different intervention messages.

## Application Overview

The application presents users with anagram puzzles where they create valid English words from scrambled letters. The system includes:

- A practice/tutorial round
- Main game rounds with behavior monitoring
- Intervention messages based on psychological theories
- Post-game surveys and debriefing
- Analytics for detecting and analyzing user behavior

## Repository Structure

```
game-application/
├── frontend-REACTJS/               # React frontend application
│   ├── src/                        # Source code
│   │   ├── components/             # UI components
│   │   │   ├── AnagramGame/        # Game-specific components
│   │   │   ├── Shared/             # Shared utilities
│   │   ├── assets/                 # Static assets
│   ├── .env                        # Environment variables
│   ├── package.json                # Dependencies
│   └── vite.config.js              # Vite configuration
│
└── backend-FASTAPI-MONGODB/        # FastAPI backend service
    ├── app/                        # Application code
    │   ├── config/                 # Configuration files
    │   │   └── db_config.json      # Game configuration
    │   │   └── app_config.json     # Environment settings and URL configurations
    │   ├── models/                 # Data models
    │   │   └── schemas.py          # Pydantic schemas
    │   └── main.py                 # API endpoints
    ├── .env                        # Environment variables
    ├── requirements.txt            # Python dependencies
    └── init_database.py            # Database initialization script
```

## Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- MongoDB instance (local or remote)
- Git

## Backend Setup

1. Navigate to the backend directory:

```bash
cd backend-FASTAPI-MONGODB
```

2. Create and activate a virtual environment:

```bash
# Using conda
conda create -n <env_name e.g. game_intervention_behavior>
conda activate game_intervention_behavior
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with the following variables:

```
MONGODB_URI=mongodb://username:password@hostname:port/
MONGODB_DB_NAME=your_database_name
```

5. Initialize the database:

```bash
python init_database.py
```

6. Start the backend server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend-REACTJS
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file in the frontend directory:

```
SURVEY_COMPLETION_CODE=your_survey_code
```

4. Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:5173

## Game Configuration

The game behavior and parameters can be modified in:

- `backend-FASTAPI-MONGODB/app/config/db_config.json`

This file contains configurations for:

- Anagram puzzles
- Time limits
- Reward structure
- Messages created based on psychological theories

## API Endpoints

The main API endpoints include:

| Endpoint                  | Method | Description                 |
| ------------------------- | ------ | --------------------------- |
| `/api/initialize-session` | POST   | Create a new user session   |
| `/api/tutorial/init`      | GET    | Initialize tutorial round   |
| `/api/tutorial/complete`  | POST   | Complete tutorial round     |
| `/api/game/init`          | GET    | Initialize main game round  |
| `/api/game/next`          | GET    | Get next anagram puzzle     |
| `/api/word-submissions`   | POST   | Submit words for validation |
| `/api/game-events`        | POST   | Log user events             |
| `/api/meanings/submit`    | POST   | Submit word meanings        |
| `/api/game-results`       | GET    | Get game results            |
| `/api/study-config`       | GET    | Get study configuration     |
| `/health`                 | GET    | Health check endpoint       |

## Deployment

### Full Stack WebApp Deployment

The backend can be deployed to platforms that support Python applications: e.g. `Render`

The frontend can be deployed to any platform that supports static sites: e.g. `Vercel`

Build for production:

```bash
npm run build
```

## Analytics

The application includes behavioral analytics that:

1. Tracks user interactions
2. Monitors potential cheating behavior
3. Analyzes intervention effectiveness
4. Processes survey feedback

## Troubleshooting

- **MongoDB Connection Issues**: Verify MongoDB connection string in app/app_config.json and ensure the database is running
- **CORS Errors**: Check local and production URLs in app/app_config.json
- **API Connection Errors**: Check local and production URLs in app/app_config.json

## License

[MIT License](LICENSE)
