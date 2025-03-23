#!/usr/bin/env python3
"""
Enhanced script to run the complete cheating analysis pipeline with detailed tag information.
Usage: python run_analysis.py
"""

import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import logging
from datetime import datetime
import json
import sys
from typing import Dict, List, Optional
import numpy as np

# Get the absolute path of the current script
SCRIPT_PATH = Path(__file__).resolve()

# Get the project root directory (3 levels up from scripts/run_analysis.py)
PROJECT_ROOT = SCRIPT_PATH.parent.parent.parent.resolve()

# Path to backend folder where .env is located
BACKEND_PATH = PROJECT_ROOT / "backend_FASTAPI_mongodb"

# Path to data_processing_analysis folder
DATA_PROCESSING_PATH = PROJECT_ROOT / "data_processing_analysis"

# Add required paths to Python path
import sys
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(DATA_PROCESSING_PATH))
sys.path.append(str(BACKEND_PATH))

# Set path to .env file in backend directory
ENV_PATH = BACKEND_PATH / ".env"

# If exists, load it directly
possible_env_paths = [
    PROJECT_ROOT / ".env",
    Path.cwd() / ".env",
    Path(__file__).parent.parent / ".env",
    Path(__file__).parent.parent.parent / ".env",
]

env_file_found = False
for env_path in possible_env_paths:
    if env_path.is_file():
        print(f"Found .env file at: {env_path}")
        load_dotenv(env_path)
        env_file_found = True
        break

# if not env_file_found:
#     print("No .env file found in any of these locations:")
#     for path in possible_env_paths:
#         print(f"- {path} (exists: {path.is_file()})")

# Print current environment variables (without sensitive data)
# print("\nEnvironment variable status:")
# print(f"MONGODB_URI present: {'Yes' if os.getenv('MONGODB_URI') else 'No'}")
# print(f"MONGODB_DB_NAME present: {'Yes' if os.getenv('MONGODB_DB_NAME') else 'No'}")
# print(f"FRONTEND_URL present: {'Yes' if os.getenv('FRONTEND_URL') else 'No'}")

# Import required modules
from analysis.cheating_analyzer import CheatingAnalyzer
from data_preprocessing.data_pipeline import DataPipeline

def setup_logging():
    """Setup logging configuration."""
    # Create participants_data directory in data_processing_analysis folder
    log_dir = DATA_PROCESSING_PATH / "participants_data"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    
    return logging.getLogger(__name__)

def analyze_participant_with_tags(events_df: pd.DataFrame, prolific_id: str, logger) -> dict:
    """Analyze single participant's data with detailed tag information."""
    try:
        logger.info(f"\nStarting analysis for participant {prolific_id}")

        # Ensure timestamps are in datetime format
        events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])

        # Handle the details column - parse JSON strings and keep dictionaries
        def parse_details(x):
            if isinstance(x, str):
                try:
                    return json.loads(x)
                except json.JSONDecodeError:
                    return {}
            return x if isinstance(x, dict) else {}

        events_df['details'] = events_df['details'].apply(parse_details)
            
        # Create expanded rows list to store all events
        expanded_rows = []
        
        for idx, row in events_df.iterrows():
            try:
                details = row['details']
                event_type = row['eventType']
                
                if event_type == 'word_validation':
                    # Extract word information from validation events
                    word = details.get('word', '')
                    if word:
                        expanded_rows.append({
                            **row.to_dict(),
                            'word': word,
                            'word_length': details.get('wordLength', len(word)),
                            'is_valid': details.get('isValid', False),
                            'anagram_shown': details.get('currentWord', '')
                        })
                        
                elif event_type == 'meaning_submission':
                    word = details.get('word', '')
                    if word:
                        expanded_rows.append({
                            **row.to_dict(),
                            'word': word,
                            'word_length': len(word),
                            'is_valid': True,
                            'anagram_shown': details.get('anagram', '')
                        })
                        
                elif event_type == 'confessed_external_help':
                    words_with_help = details.get('wordsWithExternalHelp', [])
                    if words_with_help:
                        for word_info in words_with_help:
                            if isinstance(word_info, dict):
                                expanded_rows.append({
                                    **row.to_dict(),
                                    'word': word_info.get('word', ''),
                                    'word_length': word_info.get('length', 0),
                                    'is_valid': word_info.get('isValid', False),
                                    'anagram_shown': word_info.get('anagramShown', '')
                                })
                    
                expanded_rows.append(row.to_dict())
                    
            except Exception as e:
                logger.warning(f"Error processing row {idx}: {e}")
                continue
                
        # Convert back to DataFrame and sort
        events_df = pd.DataFrame(expanded_rows)
        events_df = events_df.sort_values('timestamp')

        # Initialize analyzer with processed events
        analyzer = CheatingAnalyzer(events_df)
        
        # Get complete analysis
        analysis_result = analyzer.analyze_participant()
        
        # Add participant identifier
        analysis_result['prolific_id'] = prolific_id
        
        # Extract detailed word tag information
        tutorial_words = []
        main_game_words = []
        
        for word, tag in analyzer.word_tags.items():
            # Create base word info dictionary with common fields
            base_word_info = {
                'word': word,
                'length': tag.length,
                'phase': tag.phase,
                'anagram_shown': tag.anagram_shown if hasattr(tag, 'anagram_shown') else '',
                'is_valid': tag.is_valid,
                'was_confessed': word in analysis_result.get('confessed_cheating', {}).get('words', [])
            }
            
            if tag.phase == 'tutorial':
                # Add only tutorial-specific tag
                tutorial_word_info = {
                    **base_word_info,
                    'cheating_intention_tag': tag.cheating_intention_tag
                }
                tutorial_words.append(tutorial_word_info)
            else:
                # Add only main game-specific tag
                main_game_word_info = {
                    **base_word_info,
                    'cheating_chance_tag': tag.cheating_chance_tag
                }
                main_game_words.append(main_game_word_info)
            
        # Add detailed word information to analysis result
        analysis_result['detailed_word_analysis'] = {
            'tutorial_words': sorted(tutorial_words, key=lambda x: x['word']),
            'main_game_words': sorted(main_game_words, key=lambda x: x['word'])
        }
        
        # Log detailed word analysis
        logger.info("\nDetailed Word Analysis:")
        logger.info("=" * 50)
        
        logger.info("\nTutorial Phase Words:")
        for word in tutorial_words:
            logger.info(f"\nWord: {word['word']}")
            logger.info(f"Length: {word['length']}")
            logger.info(f"Anagram: {word['anagram_shown']}")
            logger.info(f"Cheating Intention Tag: {word['cheating_intention_tag']}")
            logger.info(f"Was Confessed: {word['was_confessed']}")
            
        logger.info("\nMain Game Words:")
        for word in main_game_words:
            logger.info(f"\nWord: {word['word']}")
            logger.info(f"Length: {word['length']}")
            logger.info(f"Anagram: {word['anagram_shown']}")
            logger.info(f"Cheating Chance Tag: {word['cheating_chance_tag']}")
            logger.info(f"Was Confessed: {word['was_confessed']}")

        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing participant {prolific_id}: {e}", exc_info=True)
        return None

def save_detailed_results(results: list, output_dir: Path):
    """Save detailed analysis results."""
    try:
        detailed_dir = output_dir / 'detailed_results'
        detailed_dir.mkdir(exist_ok=True)
        
        for result in results:
            prolific_id = result['prolific_id']
            output_file = detailed_dir / f"{prolific_id}_analysis.json"
            
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)

    except Exception as e:
        raise ValueError(f"Error saving detailed results: {str(e)}")

def create_summary_dataframe(results: list) -> pd.DataFrame:
    """Create a summary DataFrame from analysis results."""
    summary_data = []
    
    for result in results:
        if not result:
            continue
            
        # Extract key metrics
        tutorial = result['tutorial_phase']
        main_phases = result['main_phases']
        confessed = result['confessed_cheating']
        message_info = main_phases.get('anti_cheating_message', {})
        
        # Add basic metrics
        summary_row = {
            'prolific_id': result['prolific_id'],
            # Tutorial phase metrics
            'tutorial_cheating_intention_rate': tutorial['cheating_intention_rate'],
            # 'tutorial_cheating_indications': tutorial['cheating_intention'],
            'total_valid_words_tutorial': tutorial['total_valid_words_tutorial'],
            
            # Main game phase metrics
            'main_phases_cheating_chance_rate': main_phases['cheating_chance_rate'],
            'high_confidence_cheating_chance_rate': main_phases['high_confidence_cheating_chance_rate'],
            'medium_confidence_cheating_chance_rate': main_phases['medium_confidence_cheating_chance_rate'],
            'cheating_lying_rate': main_phases.get('cheating_lying_rate', 0.0),
            'total_valid_words_main_game': main_phases['total_valid_words_main_game'],
            
            # Anti-cheating message metrics
            'anti_cheating_message_shown': message_info.get('message_shown', False),
            'messageId': message_info.get('messageId'),
            'theory': message_info.get('theory'),
            'variation': message_info.get('variation'),
            # 'messageText': message_info.get('messageText'),
            'timeSpentOnMessage': message_info.get('timeSpentOnMessage'),
            
            
            # Confession metrics
            'used_external_resources': confessed['used_external_resources'],
            'confessed_words_count': confessed['confessed_words_count']
        }
        
        summary_data.append(summary_row)
    
    return pd.DataFrame(summary_data)

def main():
    """Run the complete analysis pipeline."""
    try:
        # Setup logging
        logger = setup_logging()
        logger.info("Starting enhanced analysis pipeline")
        
        # Try to read .env file directly
        env_path = ENV_PATH
        
        # Try to read and load .env file
        if not env_path.exists():
            raise FileNotFoundError(f".env file not found at {env_path}")
            
        # Load environment variables with explicit path
        # logger.info(f"Loading .env from: {env_path}")
        load_dotenv(env_path)
        
        # Get MongoDB credentials
        MONGODB_URI = os.getenv("MONGODB_URI")
        MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
        
        if not MONGODB_URI or not MONGODB_DB_NAME:
            raise ValueError("MongoDB environment variables not set")
        
        # Define paths
        base_path = DATA_PROCESSING_PATH / "participants_data"
        raw_data_path = base_path / "raw_data"
        analysis_path = base_path / "analysis_results"
        
        # Create directories
        raw_data_path.mkdir(parents=True, exist_ok=True)
        analysis_path.mkdir(parents=True, exist_ok=True)
        
        # Run data pipeline
        logger.info("Initializing data pipeline")
        pipeline = DataPipeline(MONGODB_URI, MONGODB_DB_NAME)
        pipeline.base_path = base_path
        pipeline.run_pipeline()
        logger.info("Data pipeline completed")
        
        # Analyze each participant's data
        results = []
        for csv_file in raw_data_path.glob("*.csv"):
            prolific_id = csv_file.stem
            logger.info(f"\nProcessing participant {prolific_id}")
            
            # Read participant's events
            events_df = pd.read_csv(csv_file)
            
            # Analyze participant with detailed tag information
            participant_results = analyze_participant_with_tags(events_df, prolific_id, logger)
            if participant_results:
                results.append(participant_results)
        
        if results:
            # Save detailed results
            save_detailed_results(results, analysis_path)
            
            # Create and save summary DataFrame
            summary_df = create_summary_dataframe(results)
            summary_file = analysis_path / "cheating_analysis_summary.csv"
            summary_df.to_csv(summary_file, index=False)
            
            # Print final summary statistics
            logger.info("\nFinal Analysis Summary:")
            logger.info("=" * 50)
            logger.info(f"Total participants processed: {len(results)}")
            
            # Calculate and log aggregate statistics
            stats_to_report = [
                'tutorial_cheating_intention_rate',
                'main_phases_cheating_chance_rate',
                'high_confidence_cheating_chance_rate',
                'medium_confidence_cheating_chance_rate'
            ]
            
            for stat in stats_to_report:
                desc = summary_df[stat].describe()
                logger.info(f"\n{stat}:")
                logger.info(f"Mean: {desc['mean']:.3f}")
                logger.info(f"Std: {desc['std']:.3f}")
                logger.info(f"Min: {desc['min']:.3f}")
                logger.info(f"Max: {desc['max']:.3f}")
            
            logger.info(f"\nAnalysis results saved to {summary_file}")
            
        else:
            logger.warning("No valid analysis results found")
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
    

# #!/usr/bin/env python3
# """
# Enhanced script to run the complete cheating analysis pipeline with detailed tag information.
# Usage: python run_analysis.py
# """

# import os
# import pandas as pd
# from pathlib import Path
# from dotenv import load_dotenv
# import logging
# from datetime import datetime
# import json
# import sys
# from typing import Dict, List, Optional
# import numpy as np

# # Get the absolute path of the current script
# SCRIPT_PATH = Path(__file__).resolve()

# # Get the project root directory (3 levels up from scripts/run_analysis.py)
# PROJECT_ROOT = SCRIPT_PATH.parent.parent.parent.resolve()

# # Path to backend folder where .env is located
# BACKEND_PATH = PROJECT_ROOT / "backend_FASTAPI_mongodb"

# # Path to data_processing_analysis folder
# DATA_PROCESSING_PATH = PROJECT_ROOT / "data_processing_analysis"

# # Add required paths to Python path
# import sys
# sys.path.append(str(PROJECT_ROOT))
# sys.path.append(str(DATA_PROCESSING_PATH))
# sys.path.append(str(BACKEND_PATH))

# # Set path to .env file in backend directory
# ENV_PATH = BACKEND_PATH / ".env"

# # If exists, load it directly
# possible_env_paths = [
#     PROJECT_ROOT / ".env",
#     Path.cwd() / ".env",
#     Path(__file__).parent.parent / ".env",
#     Path(__file__).parent.parent.parent / ".env",
# ]

# env_file_found = False
# for env_path in possible_env_paths:
#     if env_path.is_file():
#         print(f"Found .env file at: {env_path}")
#         load_dotenv(env_path)
#         env_file_found = True
#         break

# # if not env_file_found:
# #     print("No .env file found in any of these locations:")
# #     for path in possible_env_paths:
# #         print(f"- {path} (exists: {path.is_file()})")

# # Print current environment variables (without sensitive data)
# # print("\nEnvironment variable status:")
# # print(f"MONGODB_URI present: {'Yes' if os.getenv('MONGODB_URI') else 'No'}")
# # print(f"MONGODB_DB_NAME present: {'Yes' if os.getenv('MONGODB_DB_NAME') else 'No'}")
# # print(f"FRONTEND_URL present: {'Yes' if os.getenv('FRONTEND_URL') else 'No'}")

# # Import required modules
# from analysis.cheating_analyzer import CheatingAnalyzer
# from data_preprocessing.data_pipeline import DataPipeline

# def setup_logging():
#     """Setup logging configuration."""
#     # Create participants_data directory in data_processing_analysis folder
#     log_dir = DATA_PROCESSING_PATH / "participants_data"
#     log_dir.mkdir(parents=True, exist_ok=True)
    
#     log_file = log_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
#     logging.basicConfig(
#         filename=log_file,
#         level=logging.INFO,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )
    
#     # Also log to console
#     console = logging.StreamHandler()
#     console.setLevel(logging.INFO)
#     logging.getLogger('').addHandler(console)
    
#     return logging.getLogger(__name__)

# def analyze_participant_with_tags(events_df: pd.DataFrame, prolific_id: str, logger) -> dict:
#     """Analyze single participant's data with detailed tag information."""
#     try:
#         logger.info(f"\nStarting analysis for participant {prolific_id}")

#         # Ensure timestamps are in datetime format
#         events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])

#         # Handle the details column - parse JSON strings and keep dictionaries
#         def parse_details(x):
#             if isinstance(x, str):
#                 try:
#                     return json.loads(x)
#                 except json.JSONDecodeError:
#                     return {}
#             return x if isinstance(x, dict) else {}

#         events_df['details'] = events_df['details'].apply(parse_details)
            
#         # Create expanded rows list to store all events
#         expanded_rows = []
        
#         for idx, row in events_df.iterrows():
#             try:
#                 details = row['details']
#                 event_type = row['eventType']
                
#                 if event_type == 'word_validation':
#                     # Extract word information from validation events
#                     word = details.get('word', '')
#                     if word:
#                         expanded_rows.append({
#                             **row.to_dict(),
#                             'word': word,
#                             'word_length': details.get('wordLength', len(word)),
#                             'is_valid': details.get('isValid', False),
#                             'anagram_shown': details.get('currentWord', '')
#                         })
                        
#                 elif event_type == 'meaning_submission':
#                     word = details.get('word', '')
#                     if word:
#                         expanded_rows.append({
#                             **row.to_dict(),
#                             'word': word,
#                             'word_length': len(word),
#                             'is_valid': True,
#                             'anagram_shown': details.get('anagram', '')
#                         })
                        
#                 elif event_type == 'confessed_external_help':
#                     words_with_help = details.get('wordsWithExternalHelp', [])
#                     if words_with_help:
#                         for word_info in words_with_help:
#                             if isinstance(word_info, dict):
#                                 expanded_rows.append({
#                                     **row.to_dict(),
#                                     'word': word_info.get('word', ''),
#                                     'word_length': word_info.get('length', 0),
#                                     'is_valid': word_info.get('isValid', False),
#                                     'anagram_shown': word_info.get('anagramShown', '')
#                                 })
                    
#                 expanded_rows.append(row.to_dict())
                    
#             except Exception as e:
#                 logger.warning(f"Error processing row {idx}: {e}")
#                 continue
                
#         # Convert back to DataFrame and sort
#         events_df = pd.DataFrame(expanded_rows)
#         events_df = events_df.sort_values('timestamp')

#         # Initialize analyzer with processed events
#         analyzer = CheatingAnalyzer(events_df)
        
#         # Get complete analysis
#         analysis_result = analyzer.analyze_participant()
        
#         # Add participant identifier
#         analysis_result['prolific_id'] = prolific_id
        
#         # Extract detailed word tag information
#         tutorial_words = []
#         main_game_words = []
        
#         for word, tag in analyzer.word_tags.items():
#             # Create base word info dictionary with common fields
#             base_word_info = {
#                 'word': word,
#                 'length': tag.length,
#                 'phase': tag.phase,
#                 'anagram_shown': tag.anagram_shown if hasattr(tag, 'anagram_shown') else '',
#                 'is_valid': tag.is_valid,
#                 'was_confessed': word in analysis_result.get('confessed_cheating', {}).get('words', [])
#             }
            
#             if tag.phase == 'tutorial':
#                 # Add only tutorial-specific tag
#                 tutorial_word_info = {
#                     **base_word_info,
#                     'cheating_intention_tag': tag.cheating_intention_tag
#                 }
#                 tutorial_words.append(tutorial_word_info)
#             else:
#                 # Add only main game-specific tag
#                 main_game_word_info = {
#                     **base_word_info,
#                     'cheating_chance_tag': tag.cheating_chance_tag
#                 }
#                 main_game_words.append(main_game_word_info)
            
#         # Add detailed word information to analysis result
#         analysis_result['detailed_word_analysis'] = {
#             'tutorial_words': sorted(tutorial_words, key=lambda x: x['word']),
#             'main_game_words': sorted(main_game_words, key=lambda x: x['word'])
#         }
        
#         # Log detailed word analysis
#         logger.info("\nDetailed Word Analysis:")
#         logger.info("=" * 50)
        
#         logger.info("\nTutorial Phase Words:")
#         for word in tutorial_words:
#             logger.info(f"\nWord: {word['word']}")
#             logger.info(f"Length: {word['length']}")
#             logger.info(f"Anagram: {word['anagram_shown']}")
#             logger.info(f"Cheating Intention Tag: {word['cheating_intention_tag']}")
#             logger.info(f"Was Confessed: {word['was_confessed']}")
            
#         logger.info("\nMain Game Words:")
#         for word in main_game_words:
#             logger.info(f"\nWord: {word['word']}")
#             logger.info(f"Length: {word['length']}")
#             logger.info(f"Anagram: {word['anagram_shown']}")
#             logger.info(f"Cheating Chance Tag: {word['cheating_chance_tag']}")
#             logger.info(f"Was Confessed: {word['was_confessed']}")

#         return analysis_result
        
#     except Exception as e:
#         logger.error(f"Error analyzing participant {prolific_id}: {e}", exc_info=True)
#         return None

# def save_detailed_results(results: list, output_dir: Path):
#     """Save detailed analysis results."""
#     try:
#         detailed_dir = output_dir / 'detailed_results'
#         detailed_dir.mkdir(exist_ok=True)
        
#         for result in results:
#             prolific_id = result['prolific_id']
#             output_file = detailed_dir / f"{prolific_id}_analysis.json"
            
#             with open(output_file, 'w') as f:
#                 json.dump(result, f, indent=2, default=str)
#     except Exception as e:
#         raise ValueError(f"Error saving detailed results: {str(e)}")

# def create_summary_dataframe(results: list) -> pd.DataFrame:
#     """Create a summary DataFrame from analysis results."""
#     summary_data = []
    
#     for result in results:
#         if not result:
#             continue
            
#         # Extract key metrics
#         tutorial = result.get('tutorial_phase', {})
#         main_phases = result.get('main_phases', {})
#         confessed = result.get('confessed_cheating', {})
#         message_info = main_phases.get('anti_cheating_message', {})
        
#         # Add basic metrics
#         summary_row = {
#             'prolific_id': result.get('prolific_id', ''),
#             # Tutorial phase metrics
#             'cheating_intention_rate': tutorial.get('cheating_intention_rate', 0.0),
#             'cheating_intention': tutorial.get('cheating_intention', 0),
#             'total_valid_words_tutorial': tutorial.get('total_valid_words_tutorial', 0),
            
#             # Main game phase metrics
#             'cheating_rate': main_phases.get('cheating_rate', 0.0),
#             'high_confidence_cheating_rate': main_phases.get('high_confidence_cheating_rate', 0.0),
#             'medium_confidence_cheating_rate': main_phases.get('medium_confidence_cheating_rate', 0.0),
#             'cheating_lying_rate': main_phases.get('cheating_lying_rate', 0.0),
#             'total_valid_words_main_game': main_phases.get('total_valid_words_main_game', 0),
            
#             # Anti-cheating message metrics
#             'anti_cheating_message_shown': message_info.get('message_shown', False),
#             'messageId': message_info.get('messageId'),
#             'theory': message_info.get('theory'),
#             'variation': message_info.get('variation'),
#             'timeSpentOnMessage': message_info.get('timeSpentOnMessage'),
            
#             # Confession metrics
#             'used_external_resources': confessed.get('used_external_resources', False),
#             'confessed_words_count': confessed.get('confessed_words_count', 0)
#         }
        
#         summary_data.append(summary_row)
    
#     # Create DataFrame with explicit dtypes
#     df = pd.DataFrame(summary_data)
    
#     # Convert numeric columns to float
#     numeric_columns = [
#         'cheating_intention_rate',
#         'cheating_intention',
#         'cheating_rate',
#         'high_confidence_cheating_rate',
#         'medium_confidence_cheating_rate',
#         'cheating_lying_rate',
#         'timeSpentOnMessage'
#     ]
    
#     for col in numeric_columns:
#         df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    
#     return df

# def main():
#     """Run the complete analysis pipeline."""
#     try:
#         # Setup logging
#         logger = setup_logging()
#         logger.info("Starting enhanced analysis pipeline")
        
#         # Try to read .env file directly
#         env_path = ENV_PATH
        
#         # Try to read and load .env file
#         if not env_path.exists():
#             raise FileNotFoundError(f".env file not found at {env_path}")
            
#         # Load environment variables with explicit path
#         # logger.info(f"Loading .env from: {env_path}")
#         load_dotenv(env_path)
        
#         # Get MongoDB credentials
#         MONGODB_URI = os.getenv("MONGODB_URI")
#         MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
        
#         if not MONGODB_URI or not MONGODB_DB_NAME:
#             raise ValueError("MongoDB environment variables not set")
        
#         # Define paths
#         base_path = DATA_PROCESSING_PATH / "participants_data"
#         raw_data_path = base_path / "raw_data"
#         analysis_path = base_path / "analysis_results"
        
#         # Create directories
#         raw_data_path.mkdir(parents=True, exist_ok=True)
#         analysis_path.mkdir(parents=True, exist_ok=True)
        
#         # Run data pipeline
#         logger.info("Initializing data pipeline")
#         pipeline = DataPipeline(MONGODB_URI, MONGODB_DB_NAME)
#         pipeline.base_path = base_path
#         pipeline.run_pipeline()
#         logger.info("Data pipeline completed")
        
#         # Analyze each participant's data
#         results = []
#         for csv_file in raw_data_path.glob("*.csv"):
#             prolific_id = csv_file.stem
#             logger.info(f"\nProcessing participant {prolific_id}")
            
#             # Read participant's events
#             events_df = pd.read_csv(csv_file)
            
#             # Analyze participant with detailed tag information
#             participant_results = analyze_participant_with_tags(events_df, prolific_id, logger)
#             if participant_results:
#                 results.append(participant_results)
        
#         if results:
#             # Save detailed results
#             save_detailed_results(results, analysis_path)
            
#             # Create and save summary DataFrame
#             summary_df = create_summary_dataframe(results)
#             summary_file = analysis_path / "cheating_analysis_summary.csv"
#             summary_df.to_csv(summary_file, index=False)
            
#             # Print final summary statistics
#             logger.info("\nFinal Analysis Summary:")
#             logger.info("=" * 50)
#             logger.info(f"Total participants processed: {len(results)}")
            
#             # Calculate and log aggregate statistics
#             stats_to_report = [
#                 'cheating_intention_rate',
#                 'cheating_rate',
#                 'high_confidence_cheating_rate',
#                 'medium_confidence_cheating_rate'
#             ]
            
#             for stat in stats_to_report:
#                 desc = summary_df[stat].describe()
#                 logger.info(f"\n{stat}:")
#                 logger.info(f"Mean: {desc['mean']:.3f}")
#                 logger.info(f"Std: {desc['std']:.3f}")
#                 logger.info(f"Min: {desc['min']:.3f}")
#                 logger.info(f"Max: {desc['max']:.3f}")
            
#             logger.info(f"\nAnalysis results saved to {summary_file}")
            
#         else:
#             logger.warning("No valid analysis results found")
        
#         logger.info("Analysis completed successfully")
        
#     except Exception as e:
#         logger.error(f"Error in analysis pipeline: {e}", exc_info=True)
#         raise

# if __name__ == "__main__":
#     main()