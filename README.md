# Game Behavior Intervention Study

This project implements a comprehensive framework to study the effects of message interventions, designed based on psychological constructs, on game-playing behavior in word puzzle-solving games.

## Project Structure

```
game-behavior-intervention-study/
├── game-application/               # The actual game web application
│   ├── frontend-REACTJS/           # React-based game interface
│   └── backend-FASTAPI-MONGODB/    # FastAPI server with MongoDB integration
├── message-intervention-framework/ # Framework for generating motivational messages for honest game playing
└── game-behavior-analytics/        # Data analysis and visualization tools
```

## Components

### 1. Game Application (`game-application/`)

A full-stack web application that implements a word puzzle solving game:

- **Frontend (React.js)**:

  - Interactive anagram puzzle interface
  - Behavior tracking system
  - Survey forms for data collection
  - Tutorial and main game modes

- **Backend (FastAPI + MongoDB)**:
  - Session management
  - Game data storage
  - Event tracking
  - API endpoints for frontend interaction

### 2. Message Intervention Framework (`message-intervention-framework/`)

Creates, evaluates, and optimizes messages designed to reduce cheating behavior:

- **Generator**: Uses Llama 3.3 (70B) to create messages based on 15 psychological constructs from 4 behavioral theories:

  - Self-Determination Theory (SDT)
  - Cognitive Dissonance Theory (CDT)
  - Self-Efficacy Theory (SET)
  - Social Norm Theory (SNT)

- **Evaluator**: Utilizes GPT-4o to assess message effectiveness in targeting specific psychological constructs

- **Optimizer**: Implements an iterative feedback loop to refine and improve message effectiveness

### 3. Game Behavior Analytics (`game-behavior-analytics/`)

Processes and analyzes game event data to understand player behavior:

- **Data Preprocessing**: Extracts and prepares data from MongoDB
- **Analysis**: Detects potential cheating behavior and evaluates intervention effectiveness
- **Visualization**: Generates visual representations of player interactions and behavior patterns

## Setup and Deployment

### Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB
- API keys for required LLM models (OpenAI, Together.ai)

### Installation and Execution

1. **Clone the repository**

   ```bash
   git clone https://github.com/svdpmukherjee/game-behavior-intervention-study.git
   cd game-behavior-intervention-study
   ```

2. **Set up environment files**

   Create `.env` files in each component directory with the required configuration.

3. **Message Generation**

   ```bash
   cd message-intervention-framework
   pip install -r requirements.txt
   python run_optimizer.py
   ```

4. **Initialize Database**

   ```bash
   cd ../game-application/backend-FASTAPI-MONGODB
   pip install -r requirements.txt
   python init_database.py
   ```

5. **Run Backend Server**

   ```bash
   cd ../game-application/backend-FASTAPI-MONGODB
   uvicorn app.main:app --reload
   ```

6. **Run Frontend Application**

   ```bash
   cd ../game-application/frontend-REACTJS
   npm install
   npm run dev
   ```

7. **Analyze Collected Data**
   ```bash
   cd ../game-behavior-analytics
   pip install -r requirements.txt
   python scripts/run_analysis.py
   ```

## Detailed Documentation

Each component contains its own README with detailed setup and usage instructions:

- `game-application/README.md` - Game setup and deployment
- `message-intervention-framework/README.md` - Message generation and optimization
- `game-behavior-analytics/README.md` - Data analysis and visualization

## Citation

If you use this game or message generation framework in your research, please cite:

```bibtex
@misc{message-intervention-framework,
  author = {Mukherjee, Suvadeep},
  title = {Message Intervention Framework for Game Behavior Study},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/svdpmukherjee/game-behavior-intervention-study}}
}
```

## License

[MIT License](LICENSE)
