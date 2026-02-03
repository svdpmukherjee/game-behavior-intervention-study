#!/usr/bin/env python3
"""
Cheating analysis pipeline for anagram game experiment.

Pipeline steps:
1. Extract game events from MongoDB
2. Calculate data-driven dynamic windows from participant word creation times
3. Analyze cheating behavior using CheatingAnalyzer (page navigation, mouse inactivity, confessions)
4. Calculate performance scores and combine with survey data
5. Output combined dataset for statistical analysis

Usage: python run_analysis.py
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List

import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
ENV_PATH = PROJECT_ROOT / ".env"

# Load environment variables
env_file_found = False
for env_path in [ENV_PATH, Path.cwd() / ".env"]:
    if env_path.is_file():
        print(f"Found .env file at: {env_path}")
        load_dotenv(env_path)
        env_file_found = True
        break

from data_preprocessing.data_pipeline import DataPipeline
from cheating_analysis.cheating_analyzer import CheatingAnalyzer

def setup_logging():
    """Setup logging configuration."""
    # Create log in data directory (now at parent level)
    log_dir = PROJECT_ROOT.parent / "data"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "analysis.log"
    
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

def create_all_required_directories():
    """Create all required directories for the analysis pipeline."""
    data_root = PROJECT_ROOT.parent / "data"
    directories_to_create = [
        data_root,
        data_root / "participants_all_game_events_csv",
        data_root / "participants_data_analysis_json",
        data_root / "survey_output"
    ]
    
    for directory in directories_to_create:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created/verified directory: {directory}")

def calculate_data_driven_dynamic_windows(base_path: Path, logger) -> Dict[int, float]:
    """
    Calculate average time taken to create words of different lengths (5,6,7,8 letters)
    from actual participant data to create data-driven dynamic windows.
    
    Args:
        base_path: Path to the participants_all_game_events_csv directory
        logger: Logger instance
        
    Returns:
        Dictionary mapping word_length to average_time_seconds
    """
    logger.info("Calculating data-driven dynamic windows from participant data...")
    
    word_creation_times = {5: [], 6: [], 7: [], 8: []}
    total_participants = 0
    valid_word_count = 0
    
    try:
        # Process all participant CSV files
        for csv_file in base_path.glob("*.csv"):
            filename_stem = csv_file.stem
            if filename_stem.endswith("_game_events"):
                prolific_id = filename_stem.replace("_game_events", "")
            else:
                prolific_id = filename_stem
                
            logger.info(f"Processing {prolific_id} for dynamic window calculation...")
            total_participants += 1
            
            # Read participant's events
            try:
                events_df = pd.read_csv(csv_file)
                events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
                events_df = events_df.sort_values('timestamp')
                
                # Process both tutorial and main_game phases
                for phase in ['tutorial', 'main_game']:
                    phase_events = events_df[events_df['phase'] == phase].copy()
                    if phase_events.empty:
                        continue
                    
                    # Find word validation events
                    word_validations = phase_events[phase_events['eventType'] == 'word_validation'].copy()
                    
                    for idx, word_event in word_validations.iterrows():
                        try:
                            # Extract word information
                            word_text = word_event.get('word', '')
                            word_length = word_event.get('word_length', 0)
                            is_valid = word_event.get('is_valid', False)
                            
                            # Only process valid words of target lengths
                            if word_text and word_length in [5, 6, 7, 8] and is_valid:
                                current_timestamp = word_event['timestamp']
                                
                                # Find the previous event for this participant in the same phase
                                previous_events = phase_events[
                                    (phase_events['timestamp'] < current_timestamp)
                                ].sort_values('timestamp', ascending=False)
                                
                                if not previous_events.empty:
                                    previous_timestamp = previous_events.iloc[0]['timestamp']
                                    
                                    # Calculate time difference in seconds
                                    time_diff = (current_timestamp - previous_timestamp).total_seconds()
                                    
                                    # Filter out unrealistic times (too short or too long)
                                    # Reasonable range: 2 seconds to 2 minutes
                                    if 2 <= time_diff <= 120:
                                        word_creation_times[word_length].append(time_diff)
                                        valid_word_count += 1
                                        
                                        logger.debug(f"Word: {word_text} ({word_length} letters) - Time: {time_diff:.2f}s")
                                    else:
                                        logger.debug(f"Filtered out unrealistic time for {word_text}: {time_diff:.2f}s")
                                        
                        except Exception as e:
                            logger.warning(f"Error processing word event for {prolific_id}: {e}")
                            continue
                            
            except Exception as e:
                logger.warning(f"Error reading CSV file {csv_file}: {e}")
                continue
        
        # Calculate averages
        dynamic_windows = {}
        logger.info("Calculating average word creation times...")
        logger.info("=" * 60)
        
        for word_length in [5, 6, 7, 8]:
            times = word_creation_times[word_length]
            if times:
                # Simply calculate median of all times (no outlier removal)
                times_array = np.array(times)
                avg_time = np.median(times_array)
                dynamic_windows[word_length] = avg_time
                
                logger.info(f"Length {word_length}: {len(times)} samples")
                logger.info(f"  Median time: {avg_time:.2f} seconds")
                logger.info(f"  Mean time: {np.mean(times_array):.2f} seconds")
                logger.info(f"  Std deviation: {np.std(times_array):.2f} seconds")
            else:
                # Fallback to original calculation if no data
                avg_time = 10 + max(0, word_length - 5) * 5
                dynamic_windows[word_length] = avg_time
                logger.warning(f"Length {word_length}: No data available, using fallback: {avg_time}s")
        
        logger.info("=" * 60)
        logger.info(f"Dynamic window calculation completed:")
        logger.info(f"  Total participants processed: {total_participants}")
        logger.info(f"  Total valid words analyzed: {valid_word_count}")
        logger.info(f"  Final dynamic windows: {dynamic_windows}")
        
        return dynamic_windows
        
    except Exception as e:
        logger.error(f"Error calculating dynamic windows: {e}")
        # Return fallback values
        fallback_windows = {
            5: 10.0,
            6: 15.0, 
            7: 20.0,
            8: 25.0
        }
        logger.warning(f"Using fallback dynamic windows: {fallback_windows}")
        return fallback_windows

def extract_word_creation_skill_level(events_df: pd.DataFrame) -> int:
    """Extract the self-reported word creation skill level from the events."""
    skill_events = events_df[
        (events_df['eventType'] == 'self_reported_skill')
    ]
    
    if skill_events.empty:
        return 0  # Default value if not found
    
    # Get the latest skill event
    latest_skill_event = skill_events.iloc[-1]
    details = latest_skill_event['details']
    
    # Parse details if it's a string
    if isinstance(details, str):
        try:
            details = json.loads(details)
        except json.JSONDecodeError:
            return 0
    
    # Extract the skill level from details
    skill_level = details.get('skillLevel', 0)
    return skill_level

def load_interaction_data(prolific_id: str, logger) -> pd.DataFrame:
    """Load mouse interaction data for a participant (currently disabled)."""
    return pd.DataFrame()

def analyze_participant(events_df: pd.DataFrame, prolific_id: str,
                        dynamic_windows: Dict[int, float], logger) -> dict:
    """Analyze single participant's data."""
    try:
        logger.info(f"\nStarting analysis for participant {prolific_id}")
        logger.info(f"Using dynamic windows: {dynamic_windows}")

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

        # Load mouse interaction data
        interactions_df = load_interaction_data(prolific_id, logger)

        # Extract word creation skill level
        word_creation_skill_level = extract_word_creation_skill_level(events_df)

        # Initialize analyzer with events_df and dynamic_windows
        analyzer = CheatingAnalyzer(events_df, dynamic_windows)
        
        # Get complete analysis
        analysis_result = analyzer.analyze_participant()
        
        # Add participant identifier and skill level
        analysis_result['prolific_id'] = prolific_id
        analysis_result['word_creation_skill_level'] = word_creation_skill_level
        analysis_result['has_interaction_data'] = not interactions_df.empty
        analysis_result['dynamic_windows_used'] = dynamic_windows
        
        # Reorder fields in practice_round_phase
        if 'practice_round_phase' in analysis_result:
            practice_round_phase = analysis_result['practice_round_phase']
            analysis_result['practice_round_phase'] = {
                'total_words_practice_round': practice_round_phase.get('total_words_practice_round', 0),
                'cheating_intention_rate': practice_round_phase.get('cheating_rate_practice_round', 0)
            }
        
        # Extract detailed word tag information
        practice_round_words = []
        main_round_words = []
        
        for word, tag in analyzer.word_tags.items():
            # Create base word info dictionary with common fields
            base_word_info = {
                'word': word,
                'length': tag.length,
                'phase': tag.phase,
                'anagram_shown': tag.anagram_shown if hasattr(tag, 'anagram_shown') else '',
                'is_valid': tag.is_valid,
                'was_confessed': word in analysis_result.get('confessed_cheating', {}).get('words', []),
                'timestamp': tag.timestamp
            }
            
            if tag.phase == 'tutorial':
                # Add only tutorial-specific tag
                practice_round_word_info = {
                    **base_word_info,
                    'cheating_intention_tag': tag.cheating_intention_tag
                }
                practice_round_words.append(practice_round_word_info)
            else:
                # Add main round-specific tags
                main_round_word_info = {
                    **base_word_info,
                    'cheating_tag_main_round': tag.cheating_tag_main_round,
                }
                main_round_words.append(main_round_word_info)
            
        # Add detailed word information to analysis result
        analysis_result['detailed_word_analysis'] = {
            'practice_round_words': sorted(practice_round_words, key=lambda x: x['timestamp']),
            'main_round_words': sorted(main_round_words, key=lambda x: x['timestamp'])
        }
        
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error analyzing participant {prolific_id}: {e}", exc_info=True)
        return None

def calculate_metrics(result: dict, events_df: pd.DataFrame, logger) -> dict:
    """Calculate main round metrics based on the analysis results with DUAL PERFORMANCE METRICS."""
    try:
        metrics = {}
        prolific_id = result['prolific_id']
        
        # Get detailed word analysis
        main_round_words = result['detailed_word_analysis']['main_round_words']
        
        if not main_round_words:
            logger.warning(f"No main round words found for participant {prolific_id}")
            return {}
            
        # With our CheatingAnalyzer, we can directly use the calculated metrics
        main_phases = result['main_phases']
        
        # Get the word creation skill level
        metrics['word_creation_skill_level'] = result.get('word_creation_skill_level', 0)
        
        # ---- 1. Practice round phase cheating rate ----
        metrics['total_valid_words_tutorial'] = result['practice_round_phase']['total_words_practice_round']
        metrics['tutorial_cheating_rate'] = result['practice_round_phase'].get('cheating_intention_rate', 0)
        
        # ---- 2. Main round cheating rate calculations ----
        cheating_rate_main_round = main_phases.get('cheating_rate_main_round', 0)
        total_words_main_round = main_phases.get('total_words_main_round', 0)
        
        metrics['cheating_rate_main_round'] = cheating_rate_main_round
        metrics['total_words_main_round'] = total_words_main_round
        
        # ---- 3. Cheating lying rate calculation ----
        cheating_lying_rate = main_phases.get('cheating_lying_rate', 0)
        metrics['cheating_lying_rate'] = cheating_lying_rate
        
        # ---- 4. Behavioral flags ----
        metrics['has_interaction_data'] = result.get('has_interaction_data', False)
        metrics['cheating_main_round'] = result.get('cheating_main_round', False)
        metrics['has_page_left'] = 1 if result.get('has_page_left', False) else 0
        metrics['total_time_page_left'] = result.get('total_time_page_left', 0.0)
        metrics['has_mouse_inactivity'] = 1 if result.get('has_mouse_inactivity', False) else 0
        metrics['total_time_mouse_inactivity'] = result.get('total_time_mouse_inactivity', 0.0)

        # ---- 5. Count valid 7-letter and 8-letter words ----
        valid_7_letter_words = sum(1 for w in main_round_words if w['is_valid'] and w['length'] == 7)
        valid_8_letter_words = sum(1 for w in main_round_words if w['is_valid'] and w['length'] == 8)
        metrics['valid_7_letter_words'] = valid_7_letter_words
        metrics['valid_8_letter_words'] = valid_8_letter_words

        # ---- 6. Message information ----
        message_shown_events = events_df[
            (events_df['eventType'] == 'motivational_message_shown') &
            (events_df['phase'] == 'main_game')
        ]
        
        if message_shown_events.empty:
            logger.warning(f"No motivational message found for participant {prolific_id}")
            metrics['performance_score_excluding_cheated_words'] = 0
            metrics['performance_score_including_cheated_words'] = 0
            return metrics
        
        message_event = message_shown_events.iloc[0]
        message_timestamp = pd.to_datetime(message_event['timestamp'])
        
        # Extract message details
        message_details = message_event['details']
        if isinstance(message_details, str):
            try:
                message_details = json.loads(message_details)
            except json.JSONDecodeError:
                message_details = {}
            
        # Find corresponding message_read_complete event to calculate time spent
        message_read_events = events_df[
            (events_df['eventType'] == 'motivational_message_read_complete') &
            (events_df['phase'] == 'main_game')
        ]
        
        time_spent_on_message = 0
        if not message_read_events.empty:
            # Get the first read_complete event after the message shown
            matching_read_events = message_read_events[message_read_events['timestamp'] > message_timestamp]
            if not matching_read_events.empty:
                read_event = matching_read_events.iloc[0]
                # Calculate time spent (in seconds)
                time_spent_on_message = (read_event['timestamp'] - message_timestamp).total_seconds()
        
        message_id = message_details.get('messageId', '')
        theory = message_details.get('theory', '')
        
        metrics['motivational_message_id'] = message_id
        metrics['theory'] = theory
        metrics['time_spent_on_message'] = time_spent_on_message

        # ---- 8. DUAL PERFORMANCE SCORE ANALYSIS ----
        # Start time is when participant clicked continue after reading the message
        start_time = message_timestamp
        
        # If we found a read_complete event, use that as the start time
        if time_spent_on_message > 0 and not message_read_events.empty:
            read_event = message_read_events[message_read_events['timestamp'] > message_timestamp].iloc[0]
            start_time = read_event['timestamp']
        
        # Initialize performance details structure for BOTH metrics
        performance_details = {
            'total_words_main_round': total_words_main_round,
            'performance_score_excluding_cheated_words': 0,  # Cheating words get 0 points
            'performance_score_including_cheated_words': 0,      # All words scored equally based on validity
            'total_valid_words': {},
            'total_invalid_words': {},
            'total_cheated_words': {}
        }
        
        # Initialize counters by length
        for length in range(5, 9):  # Lengths 5-8
            performance_details['total_valid_words'][f'length_{length}'] = []
            performance_details['total_invalid_words'][f'length_{length}'] = []
            performance_details['total_cheated_words'][f'length_{length}'] = []
        
        def calculate_word_difficulty(word):
            try:
                # Dictionary mapping each letter to its difficulty score
                uncommon_letters = {
                    'q': 10, 'z': 10, 'x': 8, 'j': 8, 'v': 6, 'w': 6, 'y': 4, 'k': 5,
                    'f': 5, 'h': 4, 'b': 3, 'c': 3, 'g': 3, 'm': 3, 'p': 3, 'd': 2,
                    'l': 2, 'u': 2, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1, 'a': 1,
                    'e': 1, 'i': 1
                }
                
                # Sum difficulty scores for each letter
                score = 0
                for letter in word.lower():
                    score += uncommon_letters.get(letter, 1)
                
                return score
            except Exception as e:
                logger.warning(f"Error calculating word difficulty for {word}: {e}")
                # Default difficulty if calculation fails
                return len(word)
        
        # Initialize both performance scores
        performance_score_excluding_cheated_words = 0  # Original metric (cheating penalty)
        performance_score_including_cheated_words = 0      # New metric (no cheating penalty)
        
        # Sort main round words by timestamp to calculate time spent between words
        sorted_main_words = sorted(main_round_words, key=lambda x: pd.to_datetime(x['timestamp']))
        
        logger.info(f"Processing {len(sorted_main_words)} main round words for participant {prolific_id}")
        
        prev_timestamp = start_time  # Initialize with time participant finished reading the message
        
        for word_info in sorted_main_words:
            current_timestamp = pd.to_datetime(word_info['timestamp'])
            word_text = word_info['word']
            word_length = word_info['length']
            is_valid = word_info['is_valid']
            is_cheating = word_info.get('cheating_tag_main_round', 0) > 0
            
            # Calculate time spent (in seconds)
            time_spent = (current_timestamp - prev_timestamp).total_seconds()
            
            # Log time calculation for debugging
            logger.info(f"Word: {word_text}, Time spent: {time_spent:.2f}s, Valid: {is_valid}, Cheating: {is_cheating}")
            
            # Ensure time_spent is positive
            if time_spent <= 0:
                time_spent = 1  # Minimum 1 second to avoid division by zero
            
            # Calculate word difficulty
            word_difficulty = calculate_word_difficulty(word_text)

            # Calculate reward based on word length
            def calculate_reward(word_length):
                if word_length == 8:
                    return 8  # 8 pence
                elif word_length == 7:
                    return 6  # 6 pence
                elif word_length == 6:
                    return 4  # 4 pence
                elif word_length == 5:
                    return 2  # 2 pence
                else:
                    return 0  # No reward for other lengths

            word_reward = calculate_reward(word_length)

            # === METRIC 1: PERFORMANCE EXCLUDING CHEATED WORDS ===
            if is_cheating:
                # Cheating words contribute nothing to this metric
                honesty_weighted_contribution = 0
            else:
                # Non-cheating words contribute their full reward if valid, 0 if invalid
                honesty_weighted_contribution = word_reward if is_valid else 0

            performance_score_excluding_cheated_words += honesty_weighted_contribution

            # === METRIC 2: PERFORMANCE INCLUDING CHEATED WORDS ===
            # All valid words contribute their reward, regardless of cheating
            ability_only_contribution = word_reward if is_valid else 0
            performance_score_including_cheated_words += ability_only_contribution
            
            # Store word in appropriate category with time spent and difficulty
            length_key = f'length_{word_length}'
            if length_key in performance_details['total_valid_words']:
                word_entry = {
                    'word': word_text,
                    'timeSpent': int(time_spent),
                    'difficulty': word_difficulty,
                    'honesty_weighted_contribution': honesty_weighted_contribution,
                    'ability_only_contribution': ability_only_contribution
                }
                
                if is_valid:
                    if is_cheating:
                        performance_details['total_cheated_words'][length_key].append(word_entry)
                    else:
                        performance_details['total_valid_words'][length_key].append(word_entry)
                else:
                    if is_cheating:
                        performance_details['total_cheated_words'][length_key].append(word_entry)
                    else:
                        performance_details['total_invalid_words'][length_key].append(word_entry)
            
            # Update previous timestamp for next word
            prev_timestamp = current_timestamp
        
        # Store BOTH performance scores
        metrics['performance_score_excluding_cheated_words'] = performance_score_excluding_cheated_words
        metrics['performance_score_including_cheated_words'] = performance_score_including_cheated_words
        
        # Update performance details with both scores
        performance_details['performance_score_excluding_cheated_words'] = performance_score_excluding_cheated_words
        performance_details['performance_score_including_cheated_words'] = performance_score_including_cheated_words
        
        # ---- 9. Create structure for JSON output ----
        # Create cheating details
        cheating_details = {
            'cheating_rate_main_round': cheating_rate_main_round,
            'cheating_lying_rate': cheating_lying_rate
        }
        
        # Create motivational message details
        motivational_message = {
            'messageId': message_id,
            'theory': theory,
            'timeSpentOnMessage': time_spent_on_message
        }
        
        # Update the main_phases structure with the details
        result['main_phases'] = {
            'cheating_details': cheating_details,
            'performance_details': performance_details,
            'motivational_message': motivational_message
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating metrics for {prolific_id}: {e}", exc_info=True)
        return {}

def save_detailed_results(results: list, output_dir: Path):
    """Save detailed analysis results."""
    try:
        detailed_dir = output_dir / 'participants_data_analysis_json'
        detailed_dir.mkdir(exist_ok=True)
        
        for result in results:
            prolific_id = result['prolific_id']
            output_file = detailed_dir / f"{prolific_id}_analysis.json"
            
            # Ensure the result structure is cleaned up for JSON output
            # Convert any non-serializable objects to strings
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)

    except Exception as e:
        raise ValueError(f"Error saving detailed results: {str(e)}")

def create_summary_dataframe(results: list, metrics_list: list) -> pd.DataFrame:
    """Create a summary DataFrame from analysis results with DUAL PERFORMANCE METRICS."""
    summary_data = []
    
    for i, result in enumerate(results):
        if not result:
            continue
        
        # Get metrics
        metrics = metrics_list[i] if i < len(metrics_list) else {}
            
        # Extract key metrics
        prolific_id = result['prolific_id']
        practice_round = result['practice_round_phase']
        main_phases = result['main_phases']
        confessed = result['confessed_cheating']
        
        # Get message info from the motivational_message structure
        message_info = main_phases.get('motivational_message', {})
        
        # Add metrics including DUAL PERFORMANCE METRICS
        summary_row = {
            'prolific_id': prolific_id,
            # Word creation skill level
            'word_creation_skill_level': result.get('word_creation_skill_level', 0),
            
            # Practice round phase metrics
            'total_words_practice_round': practice_round['total_words_practice_round'],
            'cheating_rate_practice_round': practice_round['cheating_intention_rate'],
            
            # Main round metrics
            'total_words_main_round': metrics.get('total_words_main_round', 0),
            'cheating_rate_main_round': metrics.get('cheating_rate_main_round', 0),
            'cheating_lying_rate': metrics.get('cheating_lying_rate', 0),
            
            # DUAL PERFORMANCE SCORES
            'performance_score_excluding_cheated_words': metrics.get('performance_score_excluding_cheated_words', 0),
            'performance_score_including_cheated_words': metrics.get('performance_score_including_cheated_words', 0),
            
            # Motivational message metrics
            'motivational_message_id': message_info.get('messageId', ''),
            'theory': message_info.get('theory', ''),
            'time_spent_on_message': message_info.get('timeSpentOnMessage', 0),
            
            # Confession metrics
            'used_external_resources': confessed['used_external_resources'],
            'confessed_words_count': confessed['confessed_words_count'],

            # Behavioral metrics
            'cheating_main_round': metrics.get('cheating_main_round', False),
            'has_page_left': metrics.get('has_page_left', 0),
            'total_time_page_left': metrics.get('total_time_page_left', 0.0),
            'has_mouse_inactivity': metrics.get('has_mouse_inactivity', 0),
            'total_time_mouse_inactivity': metrics.get('total_time_mouse_inactivity', 0.0),
            'valid_7_letter_words': metrics.get('valid_7_letter_words', 0.0),
            'valid_8_letter_words': metrics.get('valid_8_letter_words', 0.0)
        }
        
        summary_data.append(summary_row)
    
    return pd.DataFrame(summary_data)

def combine_with_survey_results(summary_df: pd.DataFrame, survey_path: Path) -> pd.DataFrame:
    """Combine analysis results with survey data."""
    try:
        # Read survey data
        survey_df = pd.read_csv(survey_path)
        
        # Ensure consistent column naming for merging
        if 'Prolific ID' in survey_df.columns:
            survey_df = survey_df.rename(columns={'Prolific ID': 'prolific_id'})
        
        # Merge dataframes on prolific_id
        combined_df = pd.merge(
            summary_df, 
            survey_df, 
            on='prolific_id', 
            how='left'
        )
        
        return combined_df
        
    except Exception as e:
        logging.error(f"Error combining with survey results: {e}")
        return summary_df

def run_data_pipelines(mongodb_uri: str, mongodb_db_name: str, logger) -> bool:
    """Run data pipeline to extract game events from MongoDB."""
    try:
        logger.info("Starting data pipeline (game events)")
        pipeline = DataPipeline(mongodb_uri, mongodb_db_name)
        pipeline.run_pipeline()
        logger.info("Data pipeline completed")
        return True
    except Exception as e:
        logger.error(f"Error running data pipeline: {e}")
        raise

def main():
    """Run the complete analysis pipeline."""
    try:
        # Setup logging
        logger = setup_logging()
        logger.info("Starting analysis pipeline")
        logger.info("=" * 80)
        
        # Create all required directories first
        logger.info("Creating required directories")
        create_all_required_directories()
        
        # Try to read .env file directly
        env_path = ENV_PATH
        
        # Try to read and load .env file
        if not env_file_found:
            raise FileNotFoundError(f".env file not found")
            
        # Get MongoDB credentials
        MONGODB_URI = os.getenv("MONGODB_URI")
        MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
        
        if not MONGODB_URI or not MONGODB_DB_NAME:
            raise ValueError("MongoDB environment variables not set")
        
        # Define paths (data folder is at parent level)
        data_root = PROJECT_ROOT.parent / "data"
        base_path = data_root / "participants_all_game_events_csv"
        analysis_path = data_root
        
        # Run data pipeline to extract events from MongoDB
        logger.info("Running data extraction pipeline")
        run_data_pipelines(MONGODB_URI, MONGODB_DB_NAME, logger)
        
        # STEP 1: Calculate data-driven dynamic windows
        logger.info("=" * 60)
        logger.info("STEP 1: Calculating data-driven dynamic windows")
        logger.info("=" * 60)
        dynamic_windows = calculate_data_driven_dynamic_windows(base_path, logger)
        
        # STEP 2: Analyze each participant's data
        logger.info("=" * 60)
        logger.info("STEP 2: Analyzing participants")
        logger.info("=" * 60)
        
        results = []
        metrics_list = []
        
        for csv_file in base_path.glob("*.csv"):
            filename_stem = csv_file.stem
            if filename_stem.endswith("_game_events"):
                prolific_id = filename_stem.replace("_game_events", "")
            else:
                prolific_id = filename_stem
            logger.info(f"\nProcessing participant {prolific_id}")
            
            # Read participant's events
            events_df = pd.read_csv(csv_file)
            
            # Analyze participant
            participant_results = analyze_participant(
                events_df, prolific_id, dynamic_windows, logger
            )
            
            if participant_results:
                results.append(participant_results)
                
                # Calculate metrics
                metrics = calculate_metrics(participant_results, events_df, logger)
                metrics_list.append(metrics)
                
                logger.info(f"Metrics - Skill: {metrics.get('word_creation_skill_level', 0)}, "
                           f"Cheating rate: {metrics.get('cheating_rate_main_round', 0):.3f}, "
                           f"Page left: {metrics.get('has_page_left', 0)}, "
                           f"Mouse inactivity: {metrics.get('has_mouse_inactivity', 0)}")
        
        if results:
            # Save detailed results
            save_detailed_results(results, analysis_path)
            
            # Create summary DataFrame
            summary_df = create_summary_dataframe(results, metrics_list)
            
            # Combine with survey results
            survey_path = data_root / "survey_output" / "transformed_survey_results.csv"
            logger.info(f"Combining with survey results from {survey_path}")
            combined_df = combine_with_survey_results(summary_df, survey_path)
            
            # Save combined results
            output_file = analysis_path / "combined_dataset.csv"
            combined_df.to_csv(output_file, index=False)
            logger.info(f"Combined results saved to {output_file}")
            
            # Print final summary statistics
            logger.info("\nAnalysis Summary:")
            logger.info("=" * 80)
            logger.info(f"Total participants processed: {len(results)}")
            logger.info(f"Participants with interaction data: {sum(r.get('has_interaction_data', False) for r in results)}")
            logger.info(f"Data-driven dynamic windows used: {dynamic_windows}")
            
            # Calculate and log aggregate statistics
            stats_to_report = [
                'word_creation_skill_level',
                'cheating_rate_practice_round',
                'cheating_rate_main_round',
                'cheating_lying_rate',
                'performance_score',
                'has_page_left',
                'total_time_page_left',
                'has_mouse_inactivity',
                'total_time_mouse_inactivity'
            ]
            
            for stat in stats_to_report:
                if stat in summary_df.columns:
                    desc = summary_df[stat].describe()
                    logger.info(f"\n{stat}:")
                    logger.info(f"Mean: {desc['mean']:.3f}")
                    logger.info(f"Std: {desc['std']:.3f}")
                    logger.info(f"Min: {desc['min']:.3f}")
                    logger.info(f"Max: {desc['max']:.3f}")
            
            # Log cheating detection statistics
            total_cheating_practice = summary_df['cheating_rate_practice_round'].sum()
            total_cheating_main = summary_df['cheating_rate_main_round'].sum()
            total_participants = len(summary_df)
            
            participants_with_page_navigation = summary_df['has_page_left'].sum()
            participants_with_mouse_inactivity = summary_df['has_mouse_inactivity'].sum()
            participants_cheated_main = summary_df['cheating_main_round'].sum()
            
            logger.info("\nCheating Detection Summary:")
            logger.info("=" * 60)
            logger.info(f"Participants flagged for cheating in practice round: {total_cheating_practice}")
            logger.info(f"Participants flagged for cheating in main round: {total_cheating_main}")
            logger.info(f"Participants who cheated in main round (boolean): {participants_cheated_main}")
            logger.info(f"Total participants analyzed: {total_participants}")
            
            logger.info("\nBehavioral Metrics Summary:")
            logger.info("=" * 60)
            logger.info(f"Participants with page navigation events: {participants_with_page_navigation}")
            logger.info(f"Participants with mouse inactivity events: {participants_with_mouse_inactivity}")
            
            if total_participants > 0:
                practice_cheating_rate = (total_cheating_practice / total_participants) * 100
                main_cheating_rate = (total_cheating_main / total_participants) * 100
                page_nav_rate = (participants_with_page_navigation / total_participants) * 100
                mouse_inactivity_rate = (participants_with_mouse_inactivity / total_participants) * 100
                
                logger.info(f"Overall practice round cheating rate: {practice_cheating_rate:.1f}%")
                logger.info(f"Overall main round cheating rate: {main_cheating_rate:.1f}%")
                logger.info(f"Page navigation rate: {page_nav_rate:.1f}%")
                logger.info(f"Mouse inactivity rate: {mouse_inactivity_rate:.1f}%")
            
        else:
            logger.warning("No valid analysis results found")
        
        logger.info("Analysis completed successfully")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()