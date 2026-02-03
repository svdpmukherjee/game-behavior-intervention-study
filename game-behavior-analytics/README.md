# Game Behavior Analytics

A Python-based analytics pipeline for detecting and analyzing cheating behavior in a word creation game experiment. This module processes game events from MongoDB, detects cheating patterns, and produces comprehensive participant analysis.

## Overview

This module analyzes participant behavior during an anagram-based word creation game to detect potential cheating (e.g., using external resources like word solvers). It combines multiple detection signals:

- **Page navigation patterns**: Detecting when participants leave and return to the game page
- **Mouse inactivity patterns**: Identifying periods of mouse inactivity that may indicate external tool usage
- **Word creation timing**: Analyzing how quickly participants create words relative to word length
- **Confession reconciliation**: Comparing detected cheating with self-reported external help usage

## Project Structure

```
game-behavior-analytics/
├── cheating_analysis/
│   └── cheating_analyzer.py      # Core cheating detection algorithms
├── data_preprocessing/
│   ├── data_pipeline.py          # MongoDB to CSV data extraction pipeline
│   ├── mongodel.py               # MongoDB data model utilities
│   ├── mouse_interaction_pipeline.py  # Mouse event processing pipeline
│   └── survey_transform.py       # Survey data transformation and column mapping
├── scripts/
│   ├── run_analysis.py           # Main analysis pipeline orchestrator
│   └── event_visualizer.py       # Event timeline visualization utilities
├── notebook/
│   └── data_analysis.ipynb       # Jupyter notebook for exploratory analysis
├── .env                          # Environment variables (MongoDB credentials)
├── .gitignore
├── requirements.txt              # Python dependencies
└── README.md
```

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables (create a `.env` file):

```
MONGODB_URI=your_mongodb_connection_string
MONGODB_DB_NAME=your_database_name
```

## Usage

Run the complete analysis pipeline:

```bash
cd scripts
python run_analysis.py
```

The pipeline will:

1. Extract game events from MongoDB and save as CSV files
2. Calculate data-driven dynamic time windows from participant behavior
3. Analyze each participant for cheating patterns
4. Calculate performance metrics
5. Combine results with survey data
6. Output a combined dataset with all metrics

## Key Metrics

The analysis produces the following metrics for each participant:

### Cheating Detection

- `cheating_rate_practice_round`: Rate of detected cheating intention in tutorial phase
- `cheating_rate_main_round`: Rate of detected cheating in main game phase
- `cheating_main_round`: Boolean flag if any cheating was detected in main round
- `cheating_lying_rate`: Discrepancy between detected cheating and confessed cheating

### Behavioral Signals

- `has_page_left`: Whether participant left the game page
- `total_time_page_left`: Total time spent away from the game page (seconds)
- `has_mouse_inactivity`: Whether mouse inactivity was detected
- `total_time_mouse_inactivity`: Total duration of mouse inactivity (seconds)

### Performance

- `performance_score_excluding_cheated_words`: Performance score excluding words flagged as cheated
- `performance_score_including_cheated_words`: Performance score including all valid words
- `valid_7_letter_words`: Count of valid 7-letter words created
- `valid_8_letter_words`: Count of valid 8-letter words created

### Motivational Message

- `motivational_message_id`: ID of the intervention message shown
- `theory`: Psychological theory behind the message
- `time_spent_on_message`: Time participant spent reading the message

## Output Files

The pipeline generates:

- `data/participants_all_game_events_csv/`: Individual participant event CSVs
- `data/participants_data_analysis_json/`: Detailed JSON analysis per participant
- `data/combined_dataset.csv`: Final combined dataset with all metrics and survey data

## Dependencies

- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- openai
- scikit-learn
- networkx
- pymongo
- python-dotenv

## Cheating Detection Algorithm

The analyzer uses a multi-signal approach:

1. **Suspicious Sequences**: Identifies `{page_leave → page_return}` and `{mouse_inactive_start → mouse_active}` patterns
2. **Word Analysis**: Examines words created after suspicious sequences:
   - Rule 1: First/second word is 7-8 letters (indicative of using anagram solver)
   - Rule 2: Majority of subsequent words are 6+ letters
   - Rule 3: Word creation times are faster than data-driven thresholds
3. **Confession Reconciliation**: Words self-reported as cheated are marked accordingly
