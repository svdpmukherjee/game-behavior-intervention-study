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
        # Set base path relative to project root
        self.project_root = Path(__file__).parent.parent.parent.absolute()
        self.base_path = self.project_root / "participants_data"
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        log_path = self.base_path / 'pipeline.log'
        # Ensure directory exists
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Add console handler for immediate feedback
        # console = logging.StreamHandler()
        # console.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # console.setFormatter(formatter)
        # self.logger.addHandler(console)

    def ensure_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.base_path,
            self.base_path / 'raw_data',
            self.base_path / 'processed_data',
            self.base_path / 'analysis_results'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            # self.logger.info(f"Verified directory: {directory}")
            
        # self.logger.info("Directory structure verified")

    def fetch_game_events(self) -> List[Dict]:
        """Fetch all game events from MongoDB."""
        try:
            events = list(self.db.game_events.find({}))
            # self.logger.info(f"Fetched {len(events)} game events")
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
        """Process events for a single participant with comprehensive word-level extraction."""
        try:
            # Filter events for this participant
            participant_events = [e for e in events if e.get('prolificId') == prolific_id]
            
            # Expanded rows to capture word-level details
            expanded_rows = []
            
            for event in participant_events:
                # Safely parse details
                details = event.get('details', {})
                if isinstance(details, str):
                    try:
                        details = json.loads(details)
                    except json.JSONDecodeError:
                        details = {}
                
                # Ensure details is serialized consistently
                try:
                    details_json = json.dumps(details) if details else '{}'
                except TypeError:
                    details_json = '{}'
                
                # Word extraction strategies
                words = []
                
                # Strategy for word_validation events
                if event.get('eventType') == 'word_validation':
                    if details.get('word'):
                        words.append({
                            'word': details.get('word', ''),
                            'word_length': details.get('wordLength', 0),
                            'is_valid': details.get('isValid', False)
                        })
                
                # Strategy for word_submission events
                elif event.get('eventType') == 'word_submission':
                    submitted_words = []
                    if 'submittedWords' in details:
                        submitted_words = details.get('submittedWords', [])
                    elif 'words' in details:
                        submitted_words = details.get('words', [])
                    
                    for word_data in submitted_words:
                        if isinstance(word_data, dict):
                            words.append({
                                'word': word_data.get('word', ''),
                                'word_length': word_data.get('length', 0),
                                'is_valid': word_data.get('isValid', False)
                            })
                
                # Create expanded rows for each word
                if words:
                    for word_info in words:
                        expanded_row = {
                            'timestamp': event.get('timestamp'),
                            'sessionId': event.get('sessionId'),
                            'prolificId': event.get('prolificId'),
                            'phase': event.get('phase', ''),
                            'anagramShown': event.get('anagramShown', ''),
                            'eventType': event.get('eventType', ''),
                            'details': details_json,  # Store serialized JSON
                            **word_info
                        }
                        expanded_rows.append(expanded_row)
                else:
                    # If no words, keep the original event
                    expanded_row = {
                        'timestamp': event.get('timestamp'),
                        'sessionId': event.get('sessionId'),
                        'prolificId': event.get('prolificId'),
                        'phase': event.get('phase', ''),
                        'anagramShown': event.get('anagramShown', ''),
                        'eventType': event.get('eventType', ''),
                        'details': details_json,  # Store serialized JSON
                        'word': '',
                        'word_length': 0,
                        'is_valid': False
                    }
                    expanded_rows.append(expanded_row)
            
            # Convert to DataFrame
            df = pd.DataFrame(expanded_rows)
            
            # Convert timestamp and sort
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing data for participant {prolific_id}: {e}")
            raise

    def save_participant_data(self, prolific_id: str, df: pd.DataFrame):
        """Save participant data to CSV."""
        try:
            output_path = self.base_path / 'raw_data' / f'{prolific_id}.csv'
            df.to_csv(output_path, index=False)
            # self.logger.info(f"Saved data for participant {prolific_id} to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving data for participant {prolific_id}: {e}")
            raise

    def run_pipeline(self):
        """Execute the complete data pipeline."""
        try:
            # self.logger.info(f"Starting data pipeline with base path: {self.base_path}")
            
            # Ensure directory structure
            self.ensure_directories()
            
            # Fetch all events
            events = self.fetch_game_events()
            
            # Get unique participants
            participants = self.get_participant_list()
            
            # Process each participant's data
            for prolific_id in participants:
                # self.logger.info(f"Processing participant {prolific_id}")
                df = self.process_participant_data(prolific_id, events)
                self.save_participant_data(prolific_id, df)
            
            # self.logger.info("Data pipeline completed successfully")
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
        
        # Debug information
        # logger.info(f"Project root path: {project_root}")
        # logger.info(f"Current working directory: {os.getcwd()}")
        # logger.info(f".env file path: {project_root / '.env'}")
        # logger.info(f".env file exists: {(project_root / '.env').exists()}")
        
        # Load environment variables with explicit path and override
        from dotenv import load_dotenv
        dotenv_path = project_root / ".env"
        load_dotenv(dotenv_path, override=True)
        
        # Get environment variables
        MONGODB_URI = os.getenv("MONGODB_URI")
        MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
        
        # Debug environment variables (masked for security)
        # logger.info("Environment variables loaded:")
        # logger.info(f"MONGODB_URI set: {'Yes' if MONGODB_URI else 'No'}")
        # logger.info(f"MONGODB_DB_NAME set: {'Yes' if MONGODB_DB_NAME else 'No'}")
        
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