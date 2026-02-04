# Game Behavior Intervention Study

This project implements a comprehensive framework to study the effects of message interventions, designed based on psychological constructs, on game-playing behavior in word puzzle-solving anagram games.

## Project Structure

```
game-behavior-intervention-study/
├── game-application/               # The actual anagram game web application
│   ├── frontend/                   # React-based game interface
│   └── backend/                    # FastAPI server with MongoDB integration
├── message-generation-framework/   # Framework for generating motivational messages for honest game playing
├── message-evaluation-framework/   # Framework for blind evaluation of generated messages by experts
└── game-behavior-analytics/        # Data analysis and visualization tools
```

## Components

### 1. Game Application (`game-application/`)

A full-stack web application that implements a an anagram game

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

### 2. Message Generation Framework (`message-generation-framework/`)

Creates, evaluates and optimizes messages (with Human-in-the-Loop feedback) designed to reduce cheating behavior

- **Generator**: Uses Llama 3.3 (70B) to create messages based on 15 psychological concepts from 4 behavioral theories:
  - Self-Determination Theory (SDT)
  - Cognitive Dissonance Theory (CDT)
  - Self-Efficacy Theory (SET)
  - Social Norm Theory (SNT)

- **Evaluator**: Utilizes GPT-4o to assess message effectiveness in targeting specific psychological concepts

- **Optimizer**: Implements an iterative feedback loop to refine and improve message effectiveness using LLM + human feedback

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
   cd message-generation-framework
   conda activate <env_name>
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. **Initialize Database**

   ```bash
   cd ../game-application/backend
   conda activate <env_name>
   pip install -r requirements.txt
   python init_database.py
   ```

5. **Run Backend Server**

   ```bash
   cd ../game-application/backend
   conda activate <env_name>
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Run Frontend Application**

   ```bash
   cd ../game-application/frontend
   npm install
   npm run dev
   ```

<!-- 7. **Analyze Collected Data**
   ```bash
   cd ../game-behavior-analytics
   pip install -r requirements.txt
   python scripts/run_analysis.py
   ``` -->

## Detailed Documentation

Each component contains its own README with detailed setup and usage instructions:

- `game-application/README.md` - Game setup and deployment
- `message-generation-framework/README.md` - Message generation and optimization
<!-- - `game-behavior-analytics/README.md` - Data analysis and visualization -->

## Citation

If you replicate or use (1) anagram game development codes, (2) message generation/evaluation framework, (3) cheating algorithm implemented, or (4) our published datasets in your research, please cite:

```bibtex
@misc{mukherjee2025cheating,
  author = {Mukherjee, Suvadeep and Cardoso-Leite, Pedro},
  title = {Game Behavior Intervention Study: Theory-Informed Messages on Cheating Behavior},
  year = {2025},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/svdpmukherjee/game-behavior-intervention-study}},
  note = {GitHub repository}
}
```

## License

[MIT License](LICENSE)
