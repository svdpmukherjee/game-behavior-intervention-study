# Game Application

This directory contains a full-stack web application for running a word puzzle solving game study. The application consists of a React frontend and a FastAPI backend with MongoDB integration.

## Structure

game-application/
├── frontend-REACTJS/ # React frontend application
├── backend-FASTAPI-MONGODB/ # FastAPI backend service

## Setup and Running

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend-FASTAPI-MONGODB

   ```

2. Create and activate a virtual environment:

   ```bash
   conda create -n <env name e.g. game_intervention_behavior>
   conda activate game_intervention_behavior

   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt

   ```

4. Create a .env file in the backend directory with the following variables:

   ```bash
   MONGODB_URI=mongodb://username:password@hostname:port/
   MONGODB_DB_NAME=your_database_name
   FRONTEND_URL=http://localhost:5173  # For local development
   # FRONTEND_URL=https://your-production-url.com  # For production

   ```

5. Initialize the database (one-time setup):

   ```bash
   python init_database.py

   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   (The API will be available at http://localhost:8000)
   ```

### Frontend Setup

1. In a new terminal, navigate to the frontend directory:

   ```bash
   cd frontend-REACTJS

   ```

2. Install dependencies:

   ```bash
   npm install
   # Make sure lucide-react is installed
   npm install lucide-react

   ```

3. Create a .env file in the frontend directory:

   ```bash
   VITE_API_URL=http://localhost:8000  # For local development
   # VITE_API_URL=https://your-backend-api.com  # For production

   ```

4. Start the development server:
   ```bash
   npm run dev
   (The frontend will be available at http://localhost:5173)
   ```

## Configuration

1. Backend configurations for the game (anagrams, time limits, rewards) can be modified in "backend-FASTAPI-MONGODB/app/config/db_config.json"
2. API endpoints and game logic are implemented in "backend-FASTAPI-MONGODB/app/main.py"
3. Frontend game flow and UI components are in the "frontend-REACTJS/src/components/" directory
