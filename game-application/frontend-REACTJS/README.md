# Play a Word Puzzle Game

https://puzzle-solving-game-study.vercel.app/

# Frontend React.js Application

This directory contains the React.js frontend for the anagram game study application.

## Setup and Running

### Installation

1. Install dependencies:

   ```bash
   npm install
   ```

2. Create a `.env` file in the root of this directory:

   ```bash
   # This code is used by the survey completion component
   SURVEY_COMPLETION_CODE=your_survey_code
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:5173

## Building for Production

To build the application for production:

```bash
npm run build
```

## Application Flow

The application guides users through a sequence of steps:

```
App.jsx (Entry point)
├── LandingPage
│       ├── RewardDisplay
│       └── CoinIcon
├── ProlificIdPage
├── TutorialGame
│       ├── GameBoard
│       └── GameTimer
├── TestPage (with message display)
│   └── AnagramGame
│       ├── MessageDisplay
│       ├── GameBoard
│       └── GameTimer
├── SurveyPage
├── WordMeaningCheck
├── DebriefPage
└── ThankYouPage
```

## Component Overview

1. **App.jsx**: The main entry point that manages the overall flow and state of the application.

2. **LandingPage**: Presents introductory information about the study, including reward structure and participation details.

3. **ProlificIdPage**: Collects the participant's Prolific ID to initialize their session.

4. **TutorialGame**: Provides a practice round for participants to learn the game mechanics.

5. **TestPage**: The main game component where participants solve anagrams and receive intervention messages.

6. **SurveyPage**: Collects feedback from participants about their experience.

7. **WordMeaningCheck**: Asks participants to provide meanings for the words they created, used to assess potential cheating.

8. **DebriefPage**: Provides information about the study's purpose and results.

9. **ThankYouPage**: Final page thanking participants for their contribution.

### Utility Components

- **Container.jsx**: Provides consistent layout container for all pages
- **EventTrack.jsx**: Tracks user behaviors like page visibility and mouse activity

## Behavior Tracking System

The application includes comprehensive event tracking to monitor participant behaviors:

- **Page visibility changes**: Detects when users switch tabs, minimize the window, or use Alt+Tab
- **Mouse activity monitoring**: Tracks periods of mouse inactivity (5+ seconds)
- **Focus/blur events**: Records when the application loses or gains focus
- **Response times**: Measures time spent on each anagram and word
- **Submission patterns**: Analyzes patterns in word submissions that might indicate external help

This tracking is implemented through the `EventTrack.jsx` component, which captures these behaviors and sends them to the backend for analysis.

## Configuration

The application's API connection is configured in `vite.config.js`:

```javascript
export default defineConfig(({ mode }) => {
  // Determine API URL based on mode
  const apiUrl =
    mode === "production"
      ? "https://puzzle-solving-game-study.onrender.com"
      : "http://localhost:8000";

  return {
    plugins: [react(), tailwindcss()],
    // Define environment variables that will be statically replaced at build time
    define: {
      "import.meta.env.VITE_API_URL": JSON.stringify(apiUrl),
    },
    server: {
      proxy: {
        "/api": {
          target: apiUrl,
          changeOrigin: true,
        },
      },
    },
  };
});
```

This configuration automatically selects the appropriate backend URL based on whether you're in development or production mode, eliminating the need to specify the API URL in the `.env` file.
