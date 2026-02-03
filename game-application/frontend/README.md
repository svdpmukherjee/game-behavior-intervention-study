# Frontend - React Application

React-based interface for the word puzzle behavioral study.

## Demo

![Game Demo](src/assets/game_play.gif)

## Setup

```bash
# Install dependencies
npm install

# Configure environment (copy from .env.example)
cp .env.example .env
# Edit with your survey/Prolific codes

# Start development server
npm run dev
```

Application runs at http://localhost:5173

**Note**: Backend must be running at http://localhost:8000

## Build for Production

```bash
npm run build
```

## Application Flow

```
LandingPage → ProlificIdPage → TutorialGame → MessageDisplay → MainGame → Survey → WordMeaningCheck → Debrief → ThankYou
```

## Key Components

| Component | Purpose |
|-----------|---------|
| `GameBoard` | Drag-and-drop letter arrangement |
| `GameTimer` | Countdown timer with visual alerts |
| `MessageDisplay` | Shows intervention messages with typewriter effect |
| `EventTrack` | Monitors page visibility and mouse activity |
| `MouseTracker` | Records mouse movements and interactions |

## Game Mechanics

1. Drag letters from scrambled pool to solution area
2. Create valid English words (5+ letters)
3. Longer words earn more rewards
4. Fixed time limit per puzzle

## Configuration

API URL is configured in `vite.config.js`:
- Development: http://localhost:8000
- Production: Set via environment or build config

## Behavior Tracking

The app tracks (for research purposes):
- Tab switches and page visibility
- Mouse activity/inactivity periods
- Word submission patterns
- Time spent on intervention messages
