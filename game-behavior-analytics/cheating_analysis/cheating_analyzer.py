import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class WordTag:
    """Class for tracking cheating tags with phase-specific tracking."""
    word: str
    timestamp: datetime
    length: int
    is_valid: bool
    phase: str
    anagram_shown: str
    cheating_intention_tag: int = 0  # For practice round phase
    cheating_tag_main_round: int = 0     # For main round word creation phase
    cheating_main_round: bool = False  # Flag for cheating during main round word creation

class CheatingAnalyzer:
    def __init__(self, events_df: pd.DataFrame, dynamic_windows: Dict[int, float] = None):
        self.events_df = self._preprocess_events(events_df)
        self.word_tags: Dict[str, WordTag] = {}
        self.total_valid_validations = 0
        self.cheating_rate_practice_round = 0
        self.cheating_rate_main_round = 0
        
        # New metrics
        self.has_page_left = False
        self.total_time_page_left = 0.0
        self.has_mouse_inactivity = False
        self.total_time_mouse_inactivity = 0.0
        self.cheating_main_round_boolean = False
        
        # Use data-driven dynamic windows or fallback to original calculation
        if dynamic_windows:
            self.dynamic_windows = dynamic_windows
        else:
            # Fallback to original calculation
            self.dynamic_windows = {
                5: 10.0,
                6: 15.0,
                7: 20.0,
                8: 25.0
            }

    def _preprocess_events(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')

    def _calculate_page_navigation_metrics(self) -> None:
        """Calculate page navigation metrics for the entire session."""
        # Find all page_leave events
        page_leave_events = self.events_df[
            self.events_df['eventType'] == 'page_leave'
        ].copy()
        
        # Find all page_return events
        page_return_events = self.events_df[
            self.events_df['eventType'] == 'page_return'
        ].copy()
        
        if page_leave_events.empty and page_return_events.empty:
            self.has_page_left = False
            self.total_time_page_left = 0.0
            return
        
        self.has_page_left = True
        total_duration = 0.0
        
        # Sort events by timestamp
        page_leave_events = page_leave_events.sort_values('timestamp')
        
        for _, leave_event in page_leave_events.iterrows():
            leave_timestamp = leave_event['timestamp']
            
            # Find the next immediate event after page_leave
            next_events = self.events_df[
                self.events_df['timestamp'] > leave_timestamp
            ].sort_values('timestamp')
            
            if not next_events.empty:
                next_event = next_events.iloc[0]
                duration = (next_event['timestamp'] - leave_timestamp).total_seconds()
                total_duration += duration
        
        self.total_time_page_left = total_duration

    def _calculate_mouse_inactivity_metrics(self) -> None:
        """Calculate mouse inactivity metrics for the entire session."""
        # Find all mouse_inactive_start events
        inactive_start_events = self.events_df[
            self.events_df['eventType'] == 'mouse_inactive_start'
        ].copy()
        
        # Find all mouse_active events
        mouse_active_events = self.events_df[
            self.events_df['eventType'] == 'mouse_active'
        ].copy()
        
        if inactive_start_events.empty and mouse_active_events.empty:
            self.has_mouse_inactivity = False
            self.total_time_mouse_inactivity = 0.0
            return
        
        self.has_mouse_inactivity = True
        total_duration = 0.0
        
        # Sort events by timestamp
        inactive_start_events = inactive_start_events.sort_values('timestamp')
        
        for _, inactive_event in inactive_start_events.iterrows():
            inactive_timestamp = inactive_event['timestamp']
            
            # Find the next immediate event after mouse_inactive_start
            next_events = self.events_df[
                self.events_df['timestamp'] > inactive_timestamp
            ].sort_values('timestamp')
            
            if not next_events.empty:
                next_event = next_events.iloc[0]
                duration = (next_event['timestamp'] - inactive_timestamp).total_seconds()
                total_duration += duration
        
        self.total_time_mouse_inactivity = total_duration

    def _get_dynamic_time_window(self, word_length: int) -> float:
        """Get dynamic time window using data-driven values."""
        if word_length in self.dynamic_windows:
            return self.dynamic_windows[word_length]
        else:
            # Fallback to original calculation for unexpected lengths
            base_time = 10  # Base time for 5-letter word
            additional_time = max(0, word_length - 5) * 5
            return base_time + additional_time

    def _get_word_info(self, event: pd.Series) -> Tuple[str, int, bool, str]:
        """Extract word information from event, including anagram."""
        try:
            word = event.get('word', '')
            word_length = event.get('word_length', 0)
            is_valid = event.get('is_valid', False)
            anagram_shown = event.get('anagramShown', '')

            if not word or word_length == 0:
                details = event['details']
                if isinstance(details, str):
                    details = json.loads(details)
                word = details.get('word', '')
                word_length = details.get('wordLength', len(word))
                is_valid = details.get('isValid', False)
                anagram_shown = details.get('currentWord', '') or details.get('anagramShown', '')

            if not anagram_shown:
                # Try to get anagram from the event itself
                anagram_shown = event.get('anagramShown', '')

            return word, int(word_length), bool(is_valid), anagram_shown
        except Exception as e:
            print(f"Error extracting word info: {e}")
            return '', 0, False, ''

    def _calculate_word_creation_time(self, current_event: pd.Series, phase: str) -> float:
        """Calculate time taken to create a word by finding the previous event."""
        current_timestamp = current_event['timestamp']
        
        # Get all events in the same phase before current event
        previous_events = self.events_df[
            (self.events_df['phase'] == phase) &
            (self.events_df['timestamp'] < current_timestamp)
        ].sort_values('timestamp', ascending=False)
        
        if previous_events.empty:
            return float('inf')  # No previous event, can't calculate time
        
        previous_timestamp = previous_events.iloc[0]['timestamp']
        creation_time = (current_timestamp - previous_timestamp).total_seconds()
        
        return creation_time

    def _find_suspicious_sequences(self, phase: str) -> List[Tuple[datetime, str]]:
        """
        Find all {mouse_inactive_start → mouse_active} and {page_leave → page_return} sequences.
        Returns list of (end_timestamp, sequence_type) tuples.
        """
        phase_events = self.events_df[self.events_df['phase'] == phase].copy()
        sequences = []
        
        # Find mouse inactivity sequences
        mouse_inactive_events = phase_events[phase_events['eventType'] == 'mouse_inactive_start']
        mouse_active_events = phase_events[phase_events['eventType'] == 'mouse_active']
        
        for _, inactive_event in mouse_inactive_events.iterrows():
            inactive_timestamp = inactive_event['timestamp']
            
            # Find the next mouse_active event after this mouse_inactive_start
            next_active = mouse_active_events[
                mouse_active_events['timestamp'] > inactive_timestamp
            ].sort_values('timestamp')
            
            if not next_active.empty:
                active_timestamp = next_active.iloc[0]['timestamp']
                sequences.append((active_timestamp, 'mouse_inactive'))
        
        # Find page navigation sequences
        page_leave_events = phase_events[phase_events['eventType'] == 'page_leave']
        page_return_events = phase_events[phase_events['eventType'] == 'page_return']
        
        for _, leave_event in page_leave_events.iterrows():
            leave_timestamp = leave_event['timestamp']
            
            # Find the next page_return event after this page_leave
            next_return = page_return_events[
                page_return_events['timestamp'] > leave_timestamp
            ].sort_values('timestamp')
            
            if not next_return.empty:
                return_timestamp = next_return.iloc[0]['timestamp']
                sequences.append((return_timestamp, 'page_navigation'))
        
        # Sort sequences by timestamp
        sequences.sort(key=lambda x: x[0])
        return sequences

    def _analyze_words_after_sequence(self, sequence_end: datetime, phase: str) -> List[pd.Series]:
        """
        Get all word_validation events that come after a suspicious sequence.
        Look until the next suspicious sequence or end of phase.
        """
        phase_events = self.events_df[self.events_df['phase'] == phase].copy()
        
        # Get all suspicious sequences to find the boundary
        all_sequences = self._find_suspicious_sequences(phase)
        
        # Find the next sequence after current one
        next_sequence_time = None
        for seq_time, _ in all_sequences:
            if seq_time > sequence_end:
                next_sequence_time = seq_time
                break
        
        # Get word validation events after this sequence
        if next_sequence_time:
            words_after = phase_events[
                (phase_events['eventType'] == 'word_validation') &
                (phase_events['timestamp'] > sequence_end) &
                (phase_events['timestamp'] < next_sequence_time)
            ].sort_values('timestamp')
        else:
            # No next sequence, take all words until end of phase
            words_after = phase_events[
                (phase_events['eventType'] == 'word_validation') &
                (phase_events['timestamp'] > sequence_end)
            ].sort_values('timestamp')
        
        return words_after

    def _apply_cheating_rules(self, words_after_sequence: pd.DataFrame, sequence_end: datetime, phase: str) -> List[str]:
        """
        Apply the 3 cheating detection rules to words after a suspicious sequence.
        Returns list of words that should be marked as cheating.
        """
        if words_after_sequence.empty:
            return []
        
        cheating_words = []
        
        # Rule 1: Check if first or second word is 7-8 letters
        immediate_words = words_after_sequence.head(2)  # First or second word
        for _, word_event in immediate_words.iterrows():
            word, word_length, is_valid, anagram_shown = self._get_word_info(word_event)
            if word and word_length >= 7:  # 7 or 8 letter words
                cheating_words.append(word)
        
        # Rule 2: Check if majority of words are >=6 letters
        all_word_lengths = []
        all_words = []
        for _, word_event in words_after_sequence.iterrows():
            word, word_length, is_valid, anagram_shown = self._get_word_info(word_event)
            if word:
                all_word_lengths.append(word_length)
                all_words.append(word)
        
        if all_word_lengths:
            words_6_or_more = sum(1 for length in all_word_lengths if length >= 6)
            if words_6_or_more > len(all_word_lengths) / 2:  # Majority
                cheating_words.extend(all_words)
        
        # Rule 3: Check if word creation time <= dynamic window for majority of words
        fast_words = []
        previous_timestamp = sequence_end
        
        for _, word_event in words_after_sequence.iterrows():
            word, word_length, is_valid, anagram_shown = self._get_word_info(word_event)
            if not word:
                continue
            
            current_timestamp = word_event['timestamp']
            creation_time = (current_timestamp - previous_timestamp).total_seconds()
            dynamic_window = self._get_dynamic_time_window(word_length)
            
            if creation_time <= dynamic_window:
                fast_words.append(word)
            
            previous_timestamp = current_timestamp
        
        # If majority of words are created too fast, mark them as cheating
        if len(fast_words) > len(all_words) / 2:
            cheating_words.extend(fast_words)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(cheating_words))

    def analyze_practice_round_validation(self, event: pd.Series) -> None:
        """Practice round phase cheating intention analysis with simplified logic."""
        word, word_length, is_valid, anagram_shown = self._get_word_info(event)
        if not word:
            return

        timestamp = event['timestamp']

        # Create word tag if not exists
        if word not in self.word_tags:
            self.word_tags[word] = WordTag(
                word=word,
                timestamp=timestamp,
                length=word_length,
                is_valid=is_valid,
                phase='tutorial',
                anagram_shown=anagram_shown
            )
            self.total_valid_validations += 1

        # Skip if already tagged
        tag = self.word_tags[word]
        if tag.cheating_intention_tag > 0:
            return

        # Check if this word should be marked as cheating based on sequences
        sequences = self._find_suspicious_sequences('tutorial')
        
        for sequence_end, sequence_type in sequences:
            if timestamp > sequence_end:  # Word comes after this sequence
                words_after = self._analyze_words_after_sequence(sequence_end, 'tutorial')
                cheating_words = self._apply_cheating_rules(words_after, sequence_end, 'tutorial')
                
                if word in cheating_words:
                    tag.cheating_intention_tag = 1
                    self.cheating_rate_practice_round += 1
                    break

    def analyze_main_round_validation(self, event: pd.Series) -> None:
        """Main round cheating detection with simplified logic."""
        word, word_length, is_valid, anagram_shown = self._get_word_info(event)
        if not word:
            return

        # Check if word already exists but in a different phase
        if word in self.word_tags and self.word_tags[word].phase != 'main_game':
            # Create a new tag for this word in main_game phase with a modified key
            word_key = f"{word}_main_game"
            if word_key not in self.word_tags:
                self.word_tags[word_key] = WordTag(
                    word=word,
                    timestamp=event['timestamp'],
                    length=word_length,
                    is_valid=is_valid,
                    phase='main_game',
                    anagram_shown=anagram_shown
                )
                self.total_valid_validations += 1
            tag = self.word_tags[word_key]
        else:
            # Create word tag if needed (normal case)
            if word not in self.word_tags:
                self.word_tags[word] = WordTag(
                    word=word,
                    timestamp=event['timestamp'],
                    length=word_length,
                    is_valid=is_valid,
                    phase='main_game',
                    anagram_shown=anagram_shown
                )
                self.total_valid_validations += 1
            tag = self.word_tags[word]
        
        if tag.cheating_tag_main_round > 0:
            return

        timestamp = event['timestamp']
        
        # Check if this word should be marked as cheating based on sequences
        sequences = self._find_suspicious_sequences('main_game')
        
        for sequence_end, sequence_type in sequences:
            if timestamp > sequence_end:  # Word comes after this sequence
                words_after = self._analyze_words_after_sequence(sequence_end, 'main_game')
                cheating_words = self._apply_cheating_rules(words_after, sequence_end, 'main_game')
                
                if word in cheating_words:
                    tag.cheating_tag_main_round = 1
                    tag.cheating_main_round = True
                    self.cheating_rate_main_round += 1
                    self.cheating_main_round_boolean = True
                    break

    def _analyze_confessed_cheating(self) -> Dict:
        """Analyze confessed cheating from debrief phase and mark confessed words as cheating."""
        debrief_events = self.events_df[
            (self.events_df['phase'] == 'debrief') &
            (self.events_df['eventType'] == 'confessed_external_help')
        ]

        if debrief_events.empty:
            return {
                'used_external_resources': False,
                'confessed_words_count': 0,
                'words': []
            }

        try:
            last_confession = debrief_events.iloc[-1]
            details = last_confession['details']
            if isinstance(details, str):
                try:
                    details = json.loads(details)
                except json.JSONDecodeError:
                    details = {}

            used_external = details.get('usedExternalResources', False)
            confessed_words = []

            if used_external and 'wordsWithExternalHelp' in details:
                words_with_help = details['wordsWithExternalHelp']
                if isinstance(words_with_help, list):
                    confessed_words = [
                        w['word'] for w in words_with_help 
                        if isinstance(w, dict) and 'word' in w
                    ]
                    
                    # Mark all confessed words as cheating in our word_tags
                    self._reconcile_confessed_words(confessed_words)

            return {
                'used_external_resources': used_external,
                'confessed_words_count': len(confessed_words),
                'words': confessed_words,
                'details': details
            }

        except Exception as e:
            print(f"Error analyzing confessed cheating: {e}")
            return {
                'used_external_resources': False,
                'confessed_words_count': 0,
                'words': [],
                'error': str(e)
            }
            
    def _reconcile_confessed_words(self, confessed_words: List[str]) -> None:
        """Method to mark all confessed words as cheating in our records."""
        for word in confessed_words:
            # Check if word exists in main game
            if word in self.word_tags and self.word_tags[word].phase == 'main_game':
                # Mark as cheating if not already marked
                tag = self.word_tags[word]
                if tag.cheating_tag_main_round == 0:
                    tag.cheating_tag_main_round = 1
                    tag.cheating_main_round = True
                    self.cheating_rate_main_round += 1
                    self.cheating_main_round_boolean = True
            
            # Check if word exists with _main_game suffix
            word_key = f"{word}_main_game"
            if word_key in self.word_tags:
                # Mark as cheating if not already marked
                tag = self.word_tags[word_key]
                if tag.cheating_tag_main_round == 0:
                    tag.cheating_tag_main_round = 1
                    tag.cheating_main_round = True
                    self.cheating_rate_main_round += 1
                    self.cheating_main_round_boolean = True

    def analyze_phase(self, phase: str) -> Dict:
        """Analyze events for a specific phase."""
        # Now we only need events from the specific phase
        phase_events = self.events_df[self.events_df['phase'] == phase].copy()
        
        self.total_valid_validations = 0
        self.cheating_rate_practice_round = 0
        self.cheating_rate_main_round = 0

        if phase_events.empty:
            return self._create_empty_results(phase)

        # Process word validations
        validation_events = phase_events[phase_events['eventType'] == 'word_validation']
        for _, event in validation_events.iterrows():
            if phase == 'tutorial':
                self.analyze_practice_round_validation(event)
            else:
                self.analyze_main_round_validation(event)

        return self._calculate_phase_metrics(phase)

    def _calculate_phase_metrics(self, phase: str) -> Dict:
        """Calculate metrics based on phase with tracking."""
        phase_words = sum(1 for tag in self.word_tags.values() if tag.phase == phase)
    
        if phase == 'tutorial':
            return {
                'cheating_rate_practice_round': self.cheating_rate_practice_round / phase_words if phase_words != 0 else 0,
                'total_words_practice_round': phase_words
            }
        else:
            # Count words tagged as cheating in main round
            game_play_cheating = sum(
                1 for tag in self.word_tags.values()
                if tag.phase == 'main_game' and tag.cheating_main_round
            )
            
            # Get confessed words
            confessed_info = self._analyze_confessed_cheating()
            confessed_words_count = confessed_info.get('confessed_words_count', 0)
            
            # Calculate lying rate
            cheating_lying_rate = 0.0
            if game_play_cheating > 0:
                lying_rate = 1 - (confessed_words_count / game_play_cheating)
                cheating_lying_rate = max(0, min(lying_rate, 1.0))

            # Calculate main round cheating rate
            game_play_rate = game_play_cheating / phase_words if phase_words != 0 else 0
            
            return {
                'cheating_rate_main_round': game_play_rate,
                'cheating_lying_rate': cheating_lying_rate,
                'total_words_main_round': phase_words
            }

    def _create_empty_results(self, phase: str) -> Dict:
        """Create empty results structure."""
        if phase == 'tutorial':
            return {
                'cheating_rate_practice_round': 0,
                'total_words_practice_round': 0
            }
        else:
            return {
                'cheating_rate_main_round': 0,
                'cheating_lying_rate': 0,
                'total_words_main_round': 0
            }

    def analyze_participant(self) -> Dict:
        """Complete participant analysis with all new metrics."""
        # Calculate page navigation and mouse inactivity metrics first
        self._calculate_page_navigation_metrics()
        self._calculate_mouse_inactivity_metrics()
        
        practice_round_results = self.analyze_phase('tutorial')
        main_phase_results = self.analyze_phase('main_game')
        confessed_info = self._analyze_confessed_cheating()
        
        # Get motivational message shown info
        message_events = self.events_df[
            (self.events_df['eventType'] == 'motivational_message_shown') &
            (self.events_df['phase'] == 'main_game')
        ]
        
        message_info = {
            'message_shown': False,
            'messageId': None,
            'theory': None,
            'timeSpentOnMessage': None
        }
        
        if not message_events.empty:
            last_message = message_events.iloc[-1]
            details = last_message['details']
            if isinstance(details, str):
                try:
                    details = json.loads(details)
                except json.JSONDecodeError:
                    details = {}
            
            # Get the messageId and theory
            message_id = details.get('messageId')
            theory = details.get('theory')
            
            # Look for corresponding message_read_complete event to calculate time spent
            message_read_events = self.events_df[
                (self.events_df['eventType'] == 'motivational_message_read_complete') &
                (self.events_df['phase'] == 'main_game')
            ]
            
            time_spent = None
            if not message_read_events.empty:
                # Find the matching read_complete event for this message
                matching_read_events = message_read_events[
                    message_read_events.apply(
                        lambda event: (
                            isinstance(event['details'], dict) and 
                            event['details'].get('messageId') == message_id
                        ) or (
                            isinstance(event['details'], str) and
                            json.loads(event['details']).get('messageId') == message_id
                        ), 
                        axis=1
                    )
                ]
                
                if not matching_read_events.empty:
                    read_event = matching_read_events.iloc[-1]
                    # Calculate time spent (in seconds)
                    time_spent = (read_event['timestamp'] - last_message['timestamp']).total_seconds()
            
            # Update message info
            message_info = {
                'message_shown': True,
                'messageId': message_id,
                'theory': theory,
                'timeSpentOnMessage': time_spent
            }
        
        # Add message info to main_phase_results
        main_phase_results.update({
            'motivational_message': message_info
        })

        return {
            'practice_round_phase': practice_round_results,
            'main_phases': main_phase_results,
            'confessed_cheating': {
                'used_external_resources': confessed_info['used_external_resources'],
                'confessed_words_count': confessed_info['confessed_words_count'],
                'words': confessed_info['words']
            },
            # NEW METRICS
            'cheating_main_round': self.cheating_main_round_boolean,
            'has_page_left': self.has_page_left,
            'total_time_page_left': self.total_time_page_left,
            'has_mouse_inactivity': self.has_mouse_inactivity,
            'total_time_mouse_inactivity': self.total_time_mouse_inactivity
        }