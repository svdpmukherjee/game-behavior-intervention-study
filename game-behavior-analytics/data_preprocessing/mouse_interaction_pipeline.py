import os
import pandas as pd
import numpy as np
from pymongo import MongoClient
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path
from datetime import datetime
import logging

class MouseInteractionPipeline:
    def __init__(self, mongodb_uri: str, db_name: str):
        """Initialize pipeline with MongoDB credentials."""
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.project_root = Path(__file__).resolve().parent.parent.resolve()
        self.data_root = self.project_root.parent / "data"

        # Use consistent directory structure - participants_all_mouse_events_csv
        self.mouse_events_path = self.data_root / "participants_all_mouse_events_csv"

        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration."""
        # Log to the main data directory
        log_path = self.data_root / 'mouse_pipeline.log'
        
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def ensure_directories(self):
        """Ensure required directories exist."""
        self.mouse_events_path.mkdir(parents=True, exist_ok=True)
        self.logger.info("Mouse events directory structure verified")

    def fetch_user_interactions(self) -> List[Dict]:
        """Fetch all user interactions from MongoDB."""
        try:
            interactions = list(self.db.user_interactions.find({}))
            self.logger.info(f"Fetched {len(interactions)} user interactions")
            return interactions
        except Exception as e:
            self.logger.error(f"Error fetching user interactions: {e}")
            raise

    def get_participant_list(self) -> List[str]:
        """Get list of unique prolific IDs from user interactions."""
        try:
            prolific_ids = self.db.user_interactions.distinct("prolificId")
            self.logger.info(f"Found {len(prolific_ids)} unique participants with interactions")
            return prolific_ids
        except Exception as e:
            self.logger.error(f"Error fetching participant list: {e}")
            raise

    def process_participant_interactions(self, prolific_id: str, interactions: List[Dict]) -> pd.DataFrame:
        """Process interactions for a single participant with exact column structure."""
        try:
            # Filter interactions for this participant
            participant_interactions = [i for i in interactions if i.get('prolificId') == prolific_id]
            
            if not participant_interactions:
                self.logger.warning(f"No interactions found for participant {prolific_id}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(participant_interactions)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Create rows with exact column structure
            processed_rows = []
            
            for _, interaction in df.iterrows():
                try:
                    data = interaction['data']
                    if not isinstance(data, dict):
                        continue
                    
                    # Base row with required columns only
                    row = {
                        'timestamp': interaction['timestamp'],
                        'prolific_id': interaction['prolificId'],
                        'phase': interaction['phase'],
                        'anagram_shown': interaction['anagramShown'],
                        'interaction_type': interaction['interactionType'],
                        'word_in_progress': data.get('wordInProgress', ''),
                        'letter': '',
                        'source_area': '',
                        'duration': 0,
                        'x_coordinate': 0,
                        'y_coordinate': 0,
                        'is_entering_game_area': False,
                        'is_leaving_game_area': False
                    }
                    
                    # Fill interaction-specific fields
                    if interaction['interactionType'] == 'mouse_move':
                        row.update({
                            'x_coordinate': data.get('x', 0),
                            'y_coordinate': data.get('y', 0),
                            'is_entering_game_area': data.get('isEnteringGameArea', False),
                            'is_leaving_game_area': data.get('isLeavingGameArea', False)
                        })
                    
                    elif interaction['interactionType'] == 'letter_hovered':
                        row.update({
                            'letter': data.get('letter', ''),
                            'source_area': data.get('sourceArea', ''),
                            'duration': data.get('hoverDuration', 0)
                        })
                    
                    elif interaction['interactionType'] == 'letter_dragged':
                        row.update({
                            'letter': data.get('letter', ''),
                            'source_area': data.get('sourceArea', ''),
                            'duration': data.get('dragDuration', 0)
                        })
                    
                    processed_rows.append(row)
                    
                except Exception as e:
                    self.logger.warning(f"Error processing interaction for {prolific_id}: {e}")
                    continue
            
            if not processed_rows:
                self.logger.warning(f"No valid interactions processed for participant {prolific_id}")
                return pd.DataFrame()
            
            # Create final DataFrame with exact column order
            result_df = pd.DataFrame(processed_rows)
            
            # Ensure exact column order as specified
            columns_order = [
                'timestamp', 'prolific_id', 'phase', 'anagram_shown', 'interaction_type',
                'word_in_progress', 'letter', 'source_area', 'duration', 
                'x_coordinate', 'y_coordinate', 'is_entering_game_area', 'is_leaving_game_area'
            ]
            
            result_df = result_df[columns_order]
            
            return result_df
            
        except Exception as e:
            self.logger.error(f"Error processing interactions for participant {prolific_id}: {e}")
            raise

    def save_participant_interactions(self, prolific_id: str, df: pd.DataFrame):
        """Save participant interaction data to CSV."""
        try:
            if df.empty:
                self.logger.warning(f"No interaction data to save for participant {prolific_id}")
                return
            
            # Extract only the part before @ if it exists in the prolific_id
            clean_id = prolific_id.split('@')[0] if '@' in prolific_id else prolific_id
            output_path = self.mouse_events_path / f'{clean_id}_mouse_events.csv'
            df.to_csv(output_path, index=False)
            self.logger.info(f"Saved interaction data for participant {prolific_id} to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving interaction data for participant {prolific_id}: {e}")
            raise

    def run_pipeline(self):
        """Execute the complete mouse interaction pipeline."""
        try:
            self.logger.info(f"Starting mouse interaction pipeline with project root: {self.project_root}")
            
            # Ensure directory structure
            self.ensure_directories()
            
            # Fetch all interactions
            interactions = self.fetch_user_interactions()
            
            # Get unique participants
            participants = self.get_participant_list()
            
            # Process each participant's interaction data
            for prolific_id in participants:
                self.logger.info(f"Processing interactions for participant {prolific_id}")
                df = self.process_participant_interactions(prolific_id, interactions)
                self.save_participant_interactions(prolific_id, df)
            
            self.logger.info("Mouse interaction pipeline completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Mouse interaction pipeline failed: {e}")
            raise

def main():
    """Main function to run the mouse interaction pipeline."""
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
        pipeline = MouseInteractionPipeline(MONGODB_URI, MONGODB_DB_NAME)
        pipeline.run_pipeline()
        
    except Exception as e:
        print(f"Error running pipeline: {e}")
        raise

if __name__ == "__main__":
    main()