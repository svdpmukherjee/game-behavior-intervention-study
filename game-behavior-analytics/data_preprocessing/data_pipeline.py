import os
import pandas as pd
from pymongo import MongoClient
from typing import List, Dict
import json
from pathlib import Path
from datetime import datetime, date
import logging

class DataPipeline:
    def __init__(self, mongodb_uri: str, db_name: str):
        """Initialize pipeline with MongoDB credentials."""
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.project_root = Path(__file__).resolve().parent.parent.resolve()
        
        # Create the correct paths - only for game events (mouse events handled separately)
        self.events_path = self.project_root / "data" / "participants_all_game_events_csv"
        
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        # Log to the main data directory
        log_path = self.project_root / 'data' / 'pipeline.log'
        # Ensure directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def ensure_directories(self):
        """Ensure required directories exist."""
        directories = [
            self.events_path,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        self.logger.info("Directory structure verified")

    def fetch_game_events(self) -> List[Dict]:
        """Fetch all game events from MongoDB."""
        try:
            events = list(self.db.game_events.find({}))
            self.logger.info(f"Fetched {len(events)} game events")
            return events
        except Exception as e:
            self.logger.error(f"Error fetching game events: {e}")
            raise

    def get_participant_list(self) -> List[str]:
        """Get list of unique prolific IDs."""
        try:
            prolific_ids = self.db.game_events.distinct("prolificId")
            self.logger.info(f"Found {len(prolific_ids)} unique participants")
            return prolific_ids
        except Exception as e:
            self.logger.error(f"Error fetching participant list: {e}")
            raise
    
    def datetime_converter(self, o):
        """
        Custom JSON serializer for datetime objects.
        Converts datetime and date objects to ISO format strings.
        """
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

    def process_participant_data(self, prolific_id: str, events: List[Dict]) -> pd.DataFrame:
        """Process events for a single participant with corrected CSV structure."""
        try:
            # Filter events for this participant
            participant_events = [e for e in events if e.get('prolificId') == prolific_id]
            
            # Process each event into the correct structure
            processed_rows = []
            
            for event in participant_events:
                # Safely parse details
                details = event.get('details', {})
                if isinstance(details, str):
                    try:
                        details = json.loads(details)
                    except json.JSONDecodeError:
                        details = {}
                
                event_type = event.get('eventType', '')
                
                # Handle different event types according to requirements
                if event_type == 'word_validation':
                    # For word_validation: single row with word info, empty details
                    word_text = details.get('word', '')
                    word_length = details.get('wordLength', 0)
                    is_valid = details.get('isValid', False)
                    
                    processed_row = {
                        'timestamp': event.get('timestamp'),
                        'prolificId': event.get('prolificId'),
                        'phase': event.get('phase', ''),
                        'anagramShown': event.get('anagramShown', ''),
                        'eventType': event_type,
                        'details': '{}',  # Empty details as requested
                        'word': word_text,
                        'word_length': word_length,
                        'is_valid': is_valid
                    }
                    processed_rows.append(processed_row)
                    
                elif event_type == 'word_submission':
                    # For word_submission: single row with all words in details JSON
                    # Keep the original details structure intact
                    try:
                        details_json = json.dumps(details, default=self.datetime_converter) if details else '{}'
                    except TypeError:
                        details_json = '{}'
                    
                    processed_row = {
                        'timestamp': event.get('timestamp'),
                        'prolificId': event.get('prolificId'),
                        'phase': event.get('phase', ''),
                        'anagramShown': event.get('anagramShown', ''),
                        'eventType': event_type,
                        'details': details_json,  # Keep full details with all words
                        'word': '',  # No individual word for submission events
                        'word_length': 0,
                        'is_valid': False
                    }
                    processed_rows.append(processed_row)
                    
                elif event_type == 'confessed_external_help':
                    # For confessed_external_help: single row with all confessed words in details
                    try:
                        details_json = json.dumps(details, default=self.datetime_converter) if details else '{}'
                    except TypeError:
                        details_json = '{}'
                    
                    processed_row = {
                        'timestamp': event.get('timestamp'),
                        'prolificId': event.get('prolificId'),
                        'phase': event.get('phase', ''),
                        'anagramShown': event.get('anagramShown', ''),
                        'eventType': event_type,
                        'details': details_json,  # Keep full details with all confessed words
                        'word': '',  # No individual word for confession events
                        'word_length': 0,
                        'is_valid': False
                    }
                    processed_rows.append(processed_row)
                    
                else:
                    # For all other events: keep as single row with original details
                    try:
                        details_json = json.dumps(details, default=self.datetime_converter) if details else '{}'
                    except TypeError:
                        # Handle any serialization issues
                        details_json = '{}'
                    
                    processed_row = {
                        'timestamp': event.get('timestamp'),
                        'prolificId': event.get('prolificId'),
                        'phase': event.get('phase', ''),
                        'anagramShown': event.get('anagramShown', ''),
                        'eventType': event_type,
                        'details': details_json,
                        'word': '',
                        'word_length': 0,
                        'is_valid': False
                    }
                    processed_rows.append(processed_row)
            
            # Convert to DataFrame
            if not processed_rows:
                self.logger.warning(f"No valid events processed for participant {prolific_id}")
                return pd.DataFrame()
            
            df = pd.DataFrame(processed_rows)
            
            # Convert timestamp and sort
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing data for participant {prolific_id}: {e}")
            raise

    def save_participant_data(self, prolific_id: str, df: pd.DataFrame):
        """Save participant event data to CSV with correct filename."""
        try:
            # Extract only the part before @ if it exists in the prolific_id
            clean_id = prolific_id.split('@')[0] if '@' in prolific_id else prolific_id
            # Updated filename to include _game_events suffix
            output_path = self.events_path / f'{clean_id}_game_events.csv'
            df.to_csv(output_path, index=False)
            self.logger.info(f"Saved event data for participant {prolific_id} to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving event data for participant {prolific_id}: {e}")
            raise

    def run_pipeline(self):
        """Execute the complete data pipeline for game events only."""
        try:
            self.logger.info(f"Starting data pipeline with project root: {self.project_root}")
            
            # Ensure directory structure
            self.ensure_directories()
            
            # Fetch all events
            events = self.fetch_game_events()
            
            # Get unique participants
            participants = self.get_participant_list()
            
            # Process each participant's data
            for prolific_id in participants:
                self.logger.info(f"Processing participant {prolific_id}")
                
                # Process game events
                df = self.process_participant_data(prolific_id, events)
                self.save_participant_data(prolific_id, df)
            
            self.logger.info("Data pipeline completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}")
            raise

def main():
    """Main function to run the data pipeline."""
    try:
        # Determine project root and load environment variables
        project_root = Path(__file__).parent.parent.parent.absolute()
        
        # Setup basic logging for debugging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Load environment variables with explicit path and override
        from dotenv import load_dotenv
        dotenv_path = project_root / ".env"
        load_dotenv(dotenv_path, override=True)
        
        # Get environment variables
        MONGODB_URI = os.getenv("MONGODB_URI")
        MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
        
        if not MONGODB_URI or not MONGODB_DB_NAME:
            logger.error("MongoDB environment variables not found in .env file")
            logger.error("Please verify .env file contents and format")
            raise ValueError("MongoDB environment variables not set! Check .env file in project root.")
        
        # Initialize and run pipeline
        pipeline = DataPipeline(MONGODB_URI, MONGODB_DB_NAME)
        pipeline.run_pipeline()
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
        raise

if __name__ == "__main__":
    main()