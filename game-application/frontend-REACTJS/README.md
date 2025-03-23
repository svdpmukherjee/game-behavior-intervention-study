### Frontend-REACTJS

````markdown
# Frontend React.js Application

This directory contains the React.js frontend for the anagram game study application.

## Setup and Running

### Installation

1. Install dependencies:

   ```bash
   npm install

   # Make sure lucide-react is installed
   npm install lucide-react
   ```
````

2. Create a .env file in the root of this directory:
   ```bash
   VITE_API_URL=http://localhost:8000  # For local development
   # VITE_API_URL=https://your-backend-api.com  # For production
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   (The frontend will be available at http://localhost:5173)

## Building for Production

To build the application for production:

```bash
npm run build
```

# Application Flow

App.jsx (Entry point)
├── LandingPage
│ ├── RewardDisplay
│ └── CoinIcon
├── ProlificIdPage
├── TutorialGame
│ ├── GameBoard
│ └── GameTimer
├── TestPage (with message display)
│ └── AnagramGame
│ ├── MessageDisplay
│ ├── GameBoard
│ └── GameTimer
├── SurveyPage
├── WordMeaningCheck
├── DebriefPage
└── ThankYouPage

## Component Overview

1. App.jsx: The main entry point that manages the overall flow and state of the application. It controls the progression through different steps of the study.
2. LandingPage: Presents the introductory information about the study, including reward structure and participation details. Includes:

- RewardDisplay: Shows the reward structure for different word lengths
- CoinIcon: Graphical representation of rewards

3. ProlificIdPage: Collects the participant's Prolific ID to initialize their session.
4. TutorialGame: Provides a practice round for participants to learn the game mechanics. Includes:

- GameBoard: The interactive area where participants solve anagrams
- GameTimer: Displays the remaining time for the current phase

5. TestPage: The main game component where participants solve anagrams and receive intervention messages. Contains:

- AnagramGame: The core game component that includes:
  - MessageDisplay: Shows anti-cheating messages based on psychological theories
  - GameBoard: The interactive board for solving anagrams
  - GameTimer: Timer for the current anagram

6. SurveyPage: Collects feedback from participants about their experience.
7. WordMeaningCheck: Asks participants to provide meanings for the words they created, used to assess potential cheating.
8. DebriefPage: Provides information about the study's purpose and results.
9. ThankYouPage: Final page thanking participants for their contribution.

### Utility Components

1. Container.jsx: Provides consistent layout container for all pages
2. EventTrack.jsx: Tracks user behaviors like page visibility and mouse activity

### Key Files

1. App.jsx: Main application component with step management
2. index.jsx (in components/AnagramGame/): Core game logic implementation
3. GameBoard.jsx: Interactive anagram solving interface
4. MessageDisplay.jsx: Displays anti-cheating messages
5. EventTrack.jsx: The application includes comprehensive event tracking to monitor potential cheating behaviors:
   - Page visibility changes (tab switching)
   - Mouse activity and inactivity
   - Response times for solving anagrams
   - Word submission patterns
     All events are logged to the backend for later analysis.

### State Management

The application uses React's useState and useEffect hooks for state management:

1. Game progress is tracked in App.jsx
2. User input and game state are managed within respective components
3. Event tracking for cheating detection is implemented throughout

## Configuration

```bash
server: {
  proxy: {
    "/api": {
      target: "http://localhost:8000",
      changeOrigin: true,
    },
  },
},
```

You may need to adjust these settings based on your backend configuration.
