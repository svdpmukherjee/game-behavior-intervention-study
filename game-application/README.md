# Word Puzzle Game - Behavioral Study Application

A full-stack web application for conducting anagram-based behavioral experiments with psychological intervention messages.

## Overview

Participants solve word puzzles while the system monitors behavior and delivers theory-based intervention messages. The study flow includes:
- Tutorial round → Intervention message → Main game → Survey → Word meaning check → Debrief

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- MongoDB instance

### Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB_NAME=your_database_name

# Initialize database and start server
python init_database.py
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Create .env file (see .env.example)
npm run dev
```

The application will be available at http://localhost:5173

## Project Structure

```
game-application/
├── frontend/          # React + Vite frontend
│   ├── src/components/   # UI components
│   └── vite.config.js    # API proxy configuration
└── backend/           # FastAPI backend
    ├── app/
    │   ├── config/db_config.json  # Game puzzles, rewards, messages
    │   └── main.py                # API endpoints
    └── init_database.py           # Database setup script
```

## Configuration

Game parameters are in `backend/app/config/db_config.json`:
- Anagram puzzles and solutions
- Time limits per round
- Reward structure (pence per word length)
- Motivational messages (based on SDT, CDT, SNT theories)

## Deployment

- **Backend**: Deploy to Render or similar Python hosting
- **Frontend**: Deploy to Vercel (`npm run build`)

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.
