import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

@dataclass
class WordTag:
    """Class strictly for tracking cheating tags following algorithm."""
    word: str
    timestamp: datetime
    length: int
    is_valid: bool
    phase: str
    anagram_shown: str
    cheating_intention_tag: int = 0  # For tutorial phase
    cheating_chance_tag: int = 0     # For main game phase
    counted_in_case_3: bool = False  # Specifically for tracking Case 3 pairs
    processed_in_meaning_phase: bool = False  # For meaning submission tracking

class CheatingAnalyzer:
    def __init__(self, events_df: pd.DataFrame):
        self.events_df = self._preprocess_events(events_df)
        self.word_tags: Dict[str, WordTag] = {}
        self.total_valid_validations = 0
        self.cheating_intention_rate = 0
        self.cheating_chance_rate = 0

    def _preprocess_events(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df.sort_values('timestamp')

    def _calculate_dynamic_time_window(self, word_length: int) -> timedelta:
        base_time = 20  # Base time for 5-letter word
        additional_time = max(0, word_length - 5) * 5
        return timedelta(seconds=base_time + additional_time)

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

    def analyze_tutorial_validation(self, event: pd.Series) -> None:
        """Tutorial phase cheating intention analysis following algorithm.
        
        Cases for tutorial phase:
            1. If word_validation(isValid=TRUE) is immediately preceded by page_return within time window
            2. If word_validation(isValid=TRUE) is immediately preceded by word_validation(isValid=TRUE) with cheating_intention_tag=1
            3. If sequence: mouse_active -> word_validation(isValid=TRUE) -> word_validation(isValid=TRUE) (either word length >= 6 letters and gap between mouse_active and first word_validation should be within time window)
        """
        
        word, word_length, is_valid, anagram_shown = self._get_word_info(event)
        if not word or not is_valid:
            return

        timestamp = event['timestamp']
        time_window = self._calculate_dynamic_time_window(word_length)

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

        tag = self.word_tags[word]

        # Get events within time window
        window_events = self.events_df[
            (self.events_df['timestamp'] >= timestamp - time_window) &
            (self.events_df['timestamp'] < timestamp) &
            (self.events_df['phase'] == 'tutorial')
        ]

        # Case 1: Check for immediate page_return
        if not window_events.empty and window_events.iloc[-1]['eventType'] == 'page_return':
            if tag.cheating_intention_tag == 0:  # Only if not already tagged
                tag.cheating_intention_tag = 1
                self.cheating_intention_rate += 1
            return

        # Case 2: Check for previous validation with tag=1
        prev_validations = window_events[window_events['eventType'] == 'word_validation']
        if not prev_validations.empty:
            prev_word_info = self._get_word_info(prev_validations.iloc[-1])
            prev_word = prev_word_info[0]
            if prev_word in self.word_tags and self.word_tags[prev_word].cheating_intention_tag == 1:
                if tag.cheating_intention_tag == 0:  # Only if not already tagged
                    tag.cheating_intention_tag = 1
                    self.cheating_intention_rate += 1
                return

       # Case 3: Check sequence mouse_active -> validation -> validation
        if not tag.counted_in_case_3:
            # Get mouse active events within the time window
            mouse_active_events = self.events_df[
                (self.events_df['eventType'] == 'mouse_active') &
                (self.events_df['timestamp'] < timestamp) &
                (self.events_df['phase'] == 'tutorial')
            ]

            if not mouse_active_events.empty:
                last_mouse_active = mouse_active_events.iloc[-1]['timestamp']
                
                # Get valid validations after mouse activity
                subsequent_validations = self.events_df[
                    (self.events_df['eventType'] == 'word_validation') &
                    (self.events_df['timestamp'] > last_mouse_active) &
                    (self.events_df['timestamp'] <= timestamp) &
                    (self.events_df['phase'] == 'tutorial')
                ]

                if len(subsequent_validations) >= 2:
                    first_validation = subsequent_validations.iloc[-2]
                    first_word_info = self._get_word_info(first_validation)
                    first_word, first_length, first_is_valid, _ = first_word_info
                    
                    # Time checks
                    time_to_first = (first_validation['timestamp'] - last_mouse_active).total_seconds()
                    allowed_window = self._calculate_dynamic_time_window(max(word_length, first_length)).total_seconds()
                    
                    # All conditions must be met:
                    if (word_length >= 6 or first_length >= 6) and is_valid and first_is_valid and time_to_first <= allowed_window:            
                        
                        # Tag both words
                        tag.cheating_intention_tag = 1
                        tag.counted_in_case_3 = True
                        
                        if first_word in self.word_tags and not self.word_tags[first_word].counted_in_case_3:
                            self.word_tags[first_word].cheating_intention_tag = 1
                            self.word_tags[first_word].counted_in_case_3 = True
                        
                        # Increment counter once for both words together
                        self.cheating_intention_rate += 1

    def analyze_main_game_validation(self, event: pd.Series) -> None:
        """Main game phase validation analysis following algorithm.
        
        Cases for main game phase (Cases 1-3):
            1. If word_validation(isValid=TRUE) is immediately preceded by page_return within time window
            2. If word_validation(isValid=TRUE) is immediately preceded by word_validation(isValid=TRUE) with cheating_intention_tag=1
            3. If sequence: mouse_active -> word_validation(isValid=TRUE) -> word_validation(isValid=TRUE) (either word length >= 6 letters and gap between mouse_active and first word_validation should be within time window)
        """
        
        word, word_length, is_valid, anagram_shown = self._get_word_info(event)
        if not word or not is_valid:
            return

        timestamp = event['timestamp']
        time_window = self._calculate_dynamic_time_window(word_length)

        if word not in self.word_tags:
            self.word_tags[word] = WordTag(
                word=word,
                timestamp=timestamp,
                length=word_length,
                is_valid=is_valid,
                phase='main_game',
                anagram_shown=anagram_shown
            )
            self.total_valid_validations += 1

        tag = self.word_tags[word]

        # Get events within time window
        window_events = self.events_df[
            (self.events_df['timestamp'] >= timestamp - time_window) &
            (self.events_df['timestamp'] < timestamp) &
            (self.events_df['phase'] == 'main_game')
        ]

        # Case 1: Check for immediate page_return
        if not window_events.empty and window_events.iloc[-1]['eventType'] == 'page_return':
            if tag.cheating_chance_tag == 0:
                tag.cheating_chance_tag = 1
                self.cheating_chance_rate += 1
            return

        # Case 2: Check for previous validation with tag=1
        prev_validations = window_events[window_events['eventType'] == 'word_validation']
        if not prev_validations.empty:
            prev_word_info = self._get_word_info(prev_validations.iloc[-1])
            prev_word = prev_word_info[0]
            if prev_word in self.word_tags and self.word_tags[prev_word].cheating_chance_tag == 1:
                if tag.cheating_chance_tag == 0:
                    tag.cheating_chance_tag = 1
                    self.cheating_chance_rate += 1
                return

        # Case 3: Check sequence mouse_active -> validation -> validation
        if not tag.counted_in_case_3:
            # Get mouse active events within the time window
            mouse_active_events = self.events_df[
                (self.events_df['eventType'] == 'mouse_active') &
                (self.events_df['timestamp'] < timestamp) &
                (self.events_df['phase'] == 'main_game')
            ]

            if not mouse_active_events.empty:
                last_mouse_active = mouse_active_events.iloc[-1]['timestamp']
                
                # Get valid validations after mouse activity
                subsequent_validations = self.events_df[
                    (self.events_df['eventType'] == 'word_validation') &
                    (self.events_df['timestamp'] > last_mouse_active) &
                    (self.events_df['timestamp'] <= timestamp) &
                    (self.events_df['phase'] == 'main_game')
                ]

                if len(subsequent_validations) >= 2:
                    first_validation = subsequent_validations.iloc[-2]
                    first_word_info = self._get_word_info(first_validation)
                    first_word, first_length, first_is_valid, _ = first_word_info
                    
                    # Time checks
                    time_to_first = (first_validation['timestamp'] - last_mouse_active).total_seconds()
                    allowed_window = self._calculate_dynamic_time_window(max(word_length, first_length)).total_seconds()
                    
                    # All conditions must be met:
                    if (word_length >= 6 or first_length >= 6) and is_valid and first_is_valid and time_to_first <= allowed_window:            
                        
                        # Tag both words
                        tag.cheating_chance_tag = 1
                        tag.counted_in_case_3 = True
                        
                        if first_word in self.word_tags and not self.word_tags[first_word].counted_in_case_3:
                            self.word_tags[first_word].cheating_chance_tag = 1
                            self.word_tags[first_word].counted_in_case_3 = True
                        
                        # Increment counter once for both words together
                        self.cheating_chance_rate += 2

    def analyze_meaning_submission(self, event: pd.Series) -> None:
        """Analyze meaning submission following algorithm."""
        word, _, _, _ = self._get_word_info(event)
        if not word or word not in self.word_tags:
            return

        tag = self.word_tags[word]
        if tag.processed_in_meaning_phase or tag.cheating_chance_tag > 1:
            return

        timestamp = event['timestamp']

        # Get all previous events up to this meaning submission
        window_events = self.events_df[
            self.events_df['timestamp'] < timestamp
        ]

        # Case 4: Check for immediate page_return
        if not window_events.empty and window_events.iloc[-1]['eventType'] == 'page_return':
            tag.cheating_chance_tag += 1
            tag.processed_in_meaning_phase = True
            return  # Skip Case 5 if Case 4 triggers

        # Case 5: Check for mouse activity after inactivity
        inactive_events = window_events[window_events['eventType'] == 'mouse_inactive_start']
        if not inactive_events.empty:
            last_inactive = inactive_events.iloc[-1]
            active_events = window_events[
                (window_events['eventType'] == 'mouse_active') &
                (window_events['timestamp'] > last_inactive['timestamp'])
            ]

            if not active_events.empty:
                inactive_duration = (
                    active_events.iloc[0]['timestamp'] - 
                    last_inactive['timestamp']
                ).total_seconds()

                if inactive_duration > 5:
                    tag.cheating_chance_tag += 1
                    tag.processed_in_meaning_phase = True

    def analyze_phase(self, phase: str) -> Dict:
        """Analyze events for a specific phase."""
        # Special handling for main game phase to include meaning check events
        if phase == 'main_game':
            phase_events = self.events_df[
                self.events_df['phase'].isin(['main_game', 'meaning_check'])
            ].copy()
        else:
            phase_events = self.events_df[self.events_df['phase'] == phase].copy()
        
        self.total_valid_validations = 0
        self.cheating_intention_rate = 0
        self.cheating_chance_rate = 0
        # self.word_tags.clear()

        if phase_events.empty:
            return self._create_empty_results(phase)

        # Process word validations
        validation_events = phase_events[phase_events['eventType'] == 'word_validation']
        for _, event in validation_events.iterrows():
            if phase == 'tutorial':
                self.analyze_tutorial_validation(event)
            else:
                self.analyze_main_game_validation(event)

        # Process meaning submissions for main game
        meaning_events = phase_events[phase_events['eventType'] == 'meaning_submission']
        for _, event in meaning_events.iterrows():
            self.analyze_meaning_submission(event)

        return self._calculate_phase_metrics(phase)

    def _calculate_phase_metrics(self, phase: str) -> Dict:
        """Calculate metrics based on phase."""
        if self.total_valid_validations == 0:
            return self._create_empty_results(phase)

        if phase == 'tutorial':
            return {
                # 'cheating_intention': self.cheating_intention,
                'cheating_intention_rate': self.cheating_intention_rate / self.total_valid_validations if self.total_valid_validations != 0 else 0,
                'total_valid_words_tutorial': self.total_valid_validations
            }
        else:
            high_confidence = sum(
                1 for tag in self.word_tags.values()
                if tag.cheating_chance_tag >= 2
            )
            medium_confidence = sum(
                1 for tag in self.word_tags.values()
                if tag.cheating_chance_tag == 1
            )
            
            # Get confessed words
            confessed_info = self._analyze_confessed_cheating()
            confessed_words_count = confessed_info.get('confessed_words_count', 0)
            
            # Calculate lying rate
            lying_rate = 0.0
            if high_confidence > 0:  # Avoid division by zero
                lying_rate = 1 - (confessed_words_count / high_confidence)

            return {
                'cheating_chance_rate': (high_confidence + medium_confidence) / self.total_valid_validations if self.total_valid_validations != 0 else 0,
                'high_confidence_cheating_chance_rate': high_confidence / self.total_valid_validations if self.total_valid_validations != 0 else 0,
                'medium_confidence_cheating_chance_rate': medium_confidence / self.total_valid_validations if self.total_valid_validations != 0 else 0,

                'cheating_lying_rate': lying_rate,
                'total_valid_words_main_game': self.total_valid_validations
            }

    def _create_empty_results(self, phase: str) -> Dict:
        """Create empty results structure."""
        if phase == 'tutorial':
            return {
                # 'cheating_intention': 0,
                'cheating_intention_rate': 0,
                'total_valid_words_tutorial': 0
            }
        else:
            return {
                'cheating_chance_rate': 0,
                'high_confidence_cheating_chance_rate': 0,
                'medium_confidence_cheating_chance_rate': 0,
                'total_valid_words_main_game': 0
            }

    def analyze_participant(self) -> Dict:
        """Complete participant analysis."""
        tutorial_results = self.analyze_phase('tutorial')
        main_phase_results = self.analyze_phase('main_game')
        confessed_info = self._analyze_confessed_cheating()
        
        # Get anti-cheating message shown info
        message_events = self.events_df[
            (self.events_df['eventType'] == 'anti_cheating_message_shown') &
            (self.events_df['phase'] == 'main_game')
        ]
        
        message_info = {
            'message_shown': False,
            'messageId': None,
            # 'messageText': None,
            'theory': None,
            'variation': None,
            'timeSpentOnMessage': None
        }
        
        if not message_events.empty:
            last_message = message_events.iloc[-1]
            details = last_message['details']
            if isinstance(details, str):
                details = json.loads(details)
                
            message_info = {
                'message_shown': True,
                'messageId': details.get('messageId'),
                # 'messageText': details.get('messageText'),
                'theory': details.get('theory'),
                'variation': details.get('variation'),
                'timeSpentOnMessage': details.get('timeSpentOnMessage')
            }

        # Add message info to main_phase_results
        main_phase_results.update({
            'anti_cheating_message': message_info
        })

        return {
            'tutorial_phase': tutorial_results,
            'main_phases': main_phase_results,
            'confessed_cheating': {
                'used_external_resources': confessed_info['used_external_resources'],
                'confessed_words_count': confessed_info['confessed_words_count'],
                'words': confessed_info['words']
            }
        }

    def _analyze_confessed_cheating(self) -> Dict:
        """Analyze confessed cheating from debrief phase."""
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
                details = json.loads(details)

            used_external = details.get('usedExternalResources', False)
            confessed_words = []

            if used_external and 'wordsWithExternalHelp' in details:
                words_with_help = details['wordsWithExternalHelp']
                if isinstance(words_with_help, list):
                    confessed_words = [
                        w['word'] for w in words_with_help 
                        if isinstance(w, dict) and 'word' in w
                    ]

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
            
# import pandas as pd
# import numpy as np
# from typing import Dict, List, Tuple, Optional
# from datetime import datetime, timedelta
# from dataclasses import dataclass
# import json

# @dataclass
# class WordTag:
#     """Class strictly for tracking cheating tags following algorithm."""
#     word: str
#     timestamp: datetime
#     length: int
#     is_valid: bool
#     phase: str
#     anagram_shown: str
#     cheating_intention_tag: int = 0  # For tutorial phase
#     cheating_chance_tag: int = 0     # For main game phase
#     counted_in_case_3: bool = False  # Specifically for tracking Case 3 pairs
#     processed_in_meaning_phase: bool = False  # For meaning submission tracking

# class CheatingAnalyzer:
#     def __init__(self, events_df: pd.DataFrame):
#         self.events_df = self._preprocess_events(events_df)
#         self.word_tags: Dict[str, WordTag] = {}
#         self.total_valid_validations = 0
#         self.cheating_intention = 0
#         self.cheating_chance_rate = 0

#     def _preprocess_events(self, df: pd.DataFrame) -> pd.DataFrame:
#         df = df.copy()
#         df['timestamp'] = pd.to_datetime(df['timestamp'])
#         return df.sort_values('timestamp')

#     def _calculate_dynamic_time_window(self, word_length: int) -> timedelta:
#         base_time = 20  # Base time for 5-letter word
#         additional_time = max(0, word_length - 5) * 5
#         return timedelta(seconds=base_time + additional_time)

#     def _get_word_info(self, event: pd.Series) -> Tuple[str, int, bool, str]:
#         """Extract word information from event, including anagram."""
#         try:
#             word = event.get('word', '')
#             word_length = event.get('word_length', 0)
#             is_valid = event.get('is_valid', False)
#             anagram_shown = event.get('anagramShown', '')

#             if not word or word_length == 0:
#                 details = event['details']
#                 if isinstance(details, str):
#                     details = json.loads(details)
#                 word = details.get('word', '')
#                 word_length = details.get('wordLength', len(word))
#                 is_valid = details.get('isValid', False)
#                 anagram_shown = details.get('currentWord', '') or details.get('anagramShown', '')

#             if not anagram_shown:
#                 # Try to get anagram from the event itself
#                 anagram_shown = event.get('anagramShown', '')

#             return word, int(word_length), bool(is_valid), anagram_shown
#         except Exception as e:
#             print(f"Error extracting word info: {e}")
#             return '', 0, False, ''

#     def analyze_tutorial_validation(self, event: pd.Series) -> None:
#         """Tutorial phase cheating intention analysis following algorithm.
        
#         Cases for tutorial phase:
#             1. If word_validation(isValid=TRUE) is immediately preceded by page_return within time window
#             2. If word_validation(isValid=TRUE) is immediately preceded by word_validation(isValid=TRUE) with cheating_intention_tag=1
#             3. If sequence: mouse_active -> word_validation(isValid=TRUE) -> word_validation(isValid=TRUE) (either word length >= 6 letters and gap between mouse_active and first word_validation should be within time window)
#         """
        
#         word, word_length, is_valid, anagram_shown = self._get_word_info(event)
#         if not word or not is_valid:
#             return

#         timestamp = event['timestamp']
#         time_window = self._calculate_dynamic_time_window(word_length)

#         # Create word tag if not exists
#         if word not in self.word_tags:
#             self.word_tags[word] = WordTag(
#                 word=word,
#                 timestamp=timestamp,
#                 length=word_length,
#                 is_valid=is_valid,
#                 phase='tutorial',
#                 anagram_shown=anagram_shown
#             )
#             self.total_valid_validations += 1

#         tag = self.word_tags[word]

#         # Get events within time window
#         window_events = self.events_df[
#             (self.events_df['timestamp'] >= timestamp - time_window) &
#             (self.events_df['timestamp'] < timestamp) &
#             (self.events_df['phase'] == 'tutorial')
#         ]

#         # Case 1: Check for immediate page_return
#         if not window_events.empty and window_events.iloc[-1]['eventType'] == 'page_return':
#             if tag.cheating_intention_tag == 0:  # Only if not already tagged
#                 tag.cheating_intention_tag = 1
#                 self.cheating_intention += 1
#             return

#         # Case 2: Check for previous validation with tag=1
#         prev_validations = window_events[window_events['eventType'] == 'word_validation']
#         if not prev_validations.empty:
#             prev_word_info = self._get_word_info(prev_validations.iloc[-1])
#             prev_word = prev_word_info[0]
#             if prev_word in self.word_tags and self.word_tags[prev_word].cheating_intention_tag == 1:
#                 if tag.cheating_intention_tag == 0:  # Only if not already tagged
#                     tag.cheating_intention_tag = 1
#                     self.cheating_intention += 1
#                 return

#        # Case 3: Check sequence mouse_active -> validation -> validation
#         if not tag.counted_in_case_3:
#             # Get mouse active events within the time window
#             mouse_active_events = self.events_df[
#                 (self.events_df['eventType'] == 'mouse_active') &
#                 (self.events_df['timestamp'] < timestamp) &
#                 (self.events_df['phase'] == 'tutorial')
#             ]

#             if not mouse_active_events.empty:
#                 last_mouse_active = mouse_active_events.iloc[-1]['timestamp']
                
#                 # Get valid validations after mouse activity
#                 subsequent_validations = self.events_df[
#                     (self.events_df['eventType'] == 'word_validation') &
#                     (self.events_df['timestamp'] > last_mouse_active) &
#                     (self.events_df['timestamp'] <= timestamp) &
#                     (self.events_df['phase'] == 'tutorial')
#                 ]

#                 if len(subsequent_validations) >= 2:
#                     first_validation = subsequent_validations.iloc[-2]
#                     first_word_info = self._get_word_info(first_validation)
#                     first_word, first_length, first_is_valid, _ = first_word_info
                    
#                     # Time checks
#                     time_to_first = (first_validation['timestamp'] - last_mouse_active).total_seconds()
#                     allowed_window = self._calculate_dynamic_time_window(max(word_length, first_length)).total_seconds()
                    
#                     # All conditions must be met:
#                     if (word_length >= 6 or first_length >= 6) and is_valid and first_is_valid and time_to_first <= allowed_window:            
                        
#                         # Tag both words
#                         tag.cheating_intention_tag = 1
#                         tag.counted_in_case_3 = True
                        
#                         if first_word in self.word_tags and not self.word_tags[first_word].counted_in_case_3:
#                             self.word_tags[first_word].cheating_intention_tag = 1
#                             self.word_tags[first_word].counted_in_case_3 = True
                        
#                         # Increment counter once for both words together
#                         self.cheating_intention += 2

#     def analyze_main_game_validation(self, event: pd.Series) -> None:
#         """Main game phase validation analysis following algorithm.
        
#         Cases for main game phase (Cases 1-3):
#             1. If word_validation(isValid=TRUE) is immediately preceded by page_return within time window
#             2. If word_validation(isValid=TRUE) is immediately preceded by word_validation(isValid=TRUE) with cheating_intention_tag=1
#             3. If sequence: mouse_active -> word_validation(isValid=TRUE) -> word_validation(isValid=TRUE) (either word length >= 6 letters and gap between mouse_active and first word_validation should be within time window)
#         """
        
#         word, word_length, is_valid, anagram_shown = self._get_word_info(event)
#         if not word or not is_valid:
#             return

#         timestamp = event['timestamp']
#         time_window = self._calculate_dynamic_time_window(word_length)

#         if word not in self.word_tags:
#             self.word_tags[word] = WordTag(
#                 word=word,
#                 timestamp=timestamp,
#                 length=word_length,
#                 is_valid=is_valid,
#                 phase='main_game',
#                 anagram_shown=anagram_shown
#             )
#             self.total_valid_validations += 1

#         tag = self.word_tags[word]

#         # Get events within time window
#         window_events = self.events_df[
#             (self.events_df['timestamp'] >= timestamp - time_window) &
#             (self.events_df['timestamp'] < timestamp) &
#             (self.events_df['phase'] == 'main_game')
#         ]

#         # Case 1: Check for immediate page_return
#         if not window_events.empty and window_events.iloc[-1]['eventType'] == 'page_return':
#             if tag.cheating_chance_tag == 0:
#                 tag.cheating_chance_tag = 1
#                 self.cheating_chance_rate += 1
#             return

#         # Case 2: Check for previous validation with tag=1
#         prev_validations = window_events[window_events['eventType'] == 'word_validation']
#         if not prev_validations.empty:
#             prev_word_info = self._get_word_info(prev_validations.iloc[-1])
#             prev_word = prev_word_info[0]
#             if prev_word in self.word_tags and self.word_tags[prev_word].cheating_chance_tag == 1:
#                 if tag.cheating_chance_tag == 0:
#                     tag.cheating_chance_tag = 1
#                     self.cheating_chance_rate += 1
#                 return

#         # Case 3: Check sequence mouse_active -> validation -> validation
#         if not tag.counted_in_case_3:
#             # Get mouse active events within the time window
#             mouse_active_events = self.events_df[
#                 (self.events_df['eventType'] == 'mouse_active') &
#                 (self.events_df['timestamp'] < timestamp) &
#                 (self.events_df['phase'] == 'main_game')
#             ]

#             if not mouse_active_events.empty:
#                 last_mouse_active = mouse_active_events.iloc[-1]['timestamp']
                
#                 # Get valid validations after mouse activity
#                 subsequent_validations = self.events_df[
#                     (self.events_df['eventType'] == 'word_validation') &
#                     (self.events_df['timestamp'] > last_mouse_active) &
#                     (self.events_df['timestamp'] <= timestamp) &
#                     (self.events_df['phase'] == 'main_game')
#                 ]

#                 if len(subsequent_validations) >= 2:
#                     first_validation = subsequent_validations.iloc[-2]
#                     first_word_info = self._get_word_info(first_validation)
#                     first_word, first_length, first_is_valid, _ = first_word_info
                    
#                     # Time checks
#                     time_to_first = (first_validation['timestamp'] - last_mouse_active).total_seconds()
#                     allowed_window = self._calculate_dynamic_time_window(max(word_length, first_length)).total_seconds()
                    
#                     # All conditions must be met:
#                     if (word_length >= 6 or first_length >= 6) and is_valid and first_is_valid and time_to_first <= allowed_window:            
                        
#                         # Tag both words
#                         tag.cheating_chance_tag = 1
#                         tag.counted_in_case_3 = True
                        
#                         if first_word in self.word_tags and not self.word_tags[first_word].counted_in_case_3:
#                             self.word_tags[first_word].cheating_chance_tag = 1
#                             self.word_tags[first_word].counted_in_case_3 = True
                        
#                         # Increment counter once for both words together
#                         self.cheating_chance_rate += 2

#     def analyze_meaning_submission(self, event: pd.Series) -> None:
#         """Analyze meaning submission following algorithm."""
#         word, _, _, _ = self._get_word_info(event)
#         if not word or word not in self.word_tags:
#             return

#         tag = self.word_tags[word]
#         if tag.processed_in_meaning_phase or tag.cheating_chance_tag > 1:
#             return

#         timestamp = event['timestamp']

#         # Get all previous events up to this meaning submission
#         window_events = self.events_df[
#             self.events_df['timestamp'] < timestamp
#         ]

#         # Case 4: Check for immediate page_return
#         if not window_events.empty and window_events.iloc[-1]['eventType'] == 'page_return':
#             tag.cheating_chance_tag += 1
#             tag.processed_in_meaning_phase = True
#             return  # Skip Case 5 if Case 4 triggers

#         # Case 5: Check for mouse activity after inactivity
#         inactive_events = window_events[window_events['eventType'] == 'mouse_inactive_start']
#         if not inactive_events.empty:
#             last_inactive = inactive_events.iloc[-1]
#             active_events = window_events[
#                 (window_events['eventType'] == 'mouse_active') &
#                 (window_events['timestamp'] > last_inactive['timestamp'])
#             ]

#             if not active_events.empty:
#                 inactive_duration = (
#                     active_events.iloc[0]['timestamp'] - 
#                     last_inactive['timestamp']
#                 ).total_seconds()

#                 if inactive_duration > 5:
#                     tag.cheating_chance_tag += 1
#                     tag.processed_in_meaning_phase = True

#     def analyze_phase(self, phase: str) -> Dict:
#         """Analyze events for a specific phase."""
#         # Special handling for main game phase to include meaning check events
#         if phase == 'main_game':
#             phase_events = self.events_df[
#                 self.events_df['phase'].isin(['main_game', 'meaning_check'])
#             ].copy()
#         else:
#             phase_events = self.events_df[self.events_df['phase'] == phase].copy()
        
#         self.total_valid_validations = 0
#         self.cheating_intention = 0
#         self.cheating_chance_rate = 0
#         # self.word_tags.clear()

#         if phase_events.empty:
#             return self._create_empty_results(phase)

#         # Process word validations
#         validation_events = phase_events[phase_events['eventType'] == 'word_validation']
#         for _, event in validation_events.iterrows():
#             if phase == 'tutorial':
#                 self.analyze_tutorial_validation(event)
#             else:
#                 self.analyze_main_game_validation(event)

#         # Process meaning submissions for main game
#         meaning_events = phase_events[phase_events['eventType'] == 'meaning_submission']
#         for _, event in meaning_events.iterrows():
#             self.analyze_meaning_submission(event)

#         return self._calculate_phase_metrics(phase)

#     def _calculate_phase_metrics(self, phase: str) -> Dict:
#         """Calculate metrics based on phase."""
#         if self.total_valid_validations == 0:
#             return self._create_empty_results(phase)

#         if phase == 'tutorial':
#             cheating_intention_rate = self.cheating_intention / self.total_valid_validations if self.total_valid_validations > 0 else 0
#             return {
#                 'cheating_intention': self.cheating_intention,
#                 'cheating_intention_rate': cheating_intention_rate,
#                 'total_valid_words_tutorial': self.total_valid_validations
#             }
#         else:
#             high_confidence = sum(
#                 1 for tag in self.word_tags.values()
#                 if tag.cheating_chance_tag >= 2
#             )
#             medium_confidence = sum(
#                 1 for tag in self.word_tags.values()
#                 if tag.cheating_chance_tag == 1
#             )
            
#             # Get confessed words
#             confessed_info = self._analyze_confessed_cheating()
#             confessed_words_count = confessed_info.get('confessed_words_count', 0)
            
#             # Calculate rates
#             total_valid = max(1, self.total_valid_validations)  # Prevent division by zero
#             cheating_rate = (high_confidence + medium_confidence) / total_valid
#             high_confidence_rate = high_confidence / total_valid
#             medium_confidence_rate = medium_confidence / total_valid
            
#             # Calculate lying rate
#             lying_rate = 0.0
#             if high_confidence > 0:  # Avoid division by zero
#                 lying_rate = 1 - (min(confessed_words_count, high_confidence) / high_confidence)

#             return {
#                 'cheating_rate': cheating_rate,
#                 'high_confidence_cheating_rate': high_confidence_rate,
#                 'medium_confidence_cheating_rate': medium_confidence_rate,
#                 'cheating_lying_rate': lying_rate,
#                 'total_valid_words_main_game': self.total_valid_validations
#             }

#     def _create_empty_results(self, phase: str) -> Dict:
#         """Create empty results structure."""
#         if phase == 'tutorial':
#             return {
#                 'cheating_intention': 0,
#                 'cheating_intention_rate': 0.0,  # Added explicit 0.0
#                 'total_valid_words_tutorial': 0
#             }
#         else:
#             return {
#                 'cheating_rate': 0.0,
#                 'high_confidence_cheating_rate': 0.0,
#                 'medium_confidence_cheating_rate': 0.0,
#                 'cheating_lying_rate': 0.0,
#                 'total_valid_words_main_game': 0
#             }

#     def analyze_participant(self) -> Dict:
#         """Complete participant analysis."""
#         tutorial_results = self.analyze_phase('tutorial')
#         main_phase_results = self.analyze_phase('main_game')
#         confessed_info = self._analyze_confessed_cheating()
        
#         # Get anti-cheating message shown info
#         message_events = self.events_df[
#             (self.events_df['eventType'] == 'anti_cheating_message_shown') &
#             (self.events_df['phase'] == 'main_game')
#         ]
        
#         message_info = {
#             'message_shown': False,
#             'messageId': None,
#             # 'messageText': None,
#             'theory': None,
#             'variation': None,
#             'timeSpentOnMessage': None
#         }
        
#         if not message_events.empty:
#             last_message = message_events.iloc[-1]
#             details = last_message['details']
#             if isinstance(details, str):
#                 details = json.loads(details)
                
#             message_info = {
#                 'message_shown': True,
#                 'messageId': details.get('messageId'),
#                 # 'messageText': details.get('messageText'),
#                 'theory': details.get('theory'),
#                 'variation': details.get('variation'),
#                 'timeSpentOnMessage': details.get('timeSpentOnMessage')
#             }

#         # Add message info to main_phase_results
#         main_phase_results.update({
#             'anti_cheating_message': message_info
#         })

#         return {
#             'tutorial_phase': tutorial_results,
#             'main_phases': main_phase_results,
#             'confessed_cheating': {
#                 'used_external_resources': confessed_info['used_external_resources'],
#                 'confessed_words_count': confessed_info['confessed_words_count'],
#                 'words': confessed_info['words']
#             }
#         }

#     def _analyze_confessed_cheating(self) -> Dict:
#         """Analyze confessed cheating from debrief phase."""
#         debrief_events = self.events_df[
#             (self.events_df['phase'] == 'debrief') &
#             (self.events_df['eventType'] == 'confessed_external_help')
#         ]

#         if debrief_events.empty:
#             return {
#                 'used_external_resources': False,
#                 'confessed_words_count': 0,
#                 'words': []
#             }

#         try:
#             last_confession = debrief_events.iloc[-1]
#             details = last_confession['details']
#             if isinstance(details, str):
#                 details = json.loads(details)

#             used_external = details.get('usedExternalResources', False)
#             confessed_words = []

#             if used_external and 'wordsWithExternalHelp' in details:
#                 words_with_help = details['wordsWithExternalHelp']
#                 if isinstance(words_with_help, list):
#                     confessed_words = [
#                         w['word'] for w in words_with_help 
#                         if isinstance(w, dict) and 'word' in w
#                     ]

#             return {
#                 'used_external_resources': used_external,
#                 'confessed_words_count': len(confessed_words),
#                 'words': confessed_words,
#                 'details': details
#             }

#         except Exception as e:
#             print(f"Error analyzing confessed cheating: {e}")
#             return {
#                 'used_external_resources': False,
#                 'confessed_words_count': 0,
#                 'words': [],
#                 'error': str(e)
#             }