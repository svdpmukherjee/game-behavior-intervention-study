#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from datetime import timedelta

class EventVisualizer:
    def __init__(self, events_df: pd.DataFrame):
        """Initialize visualizer with events dataframe."""
        self.events_df = events_df.copy()
        self.events_df['timestamp'] = pd.to_datetime(self.events_df['timestamp'])
        self.events_df = self.events_df.sort_values('timestamp')
        
        # Define color scheme for event types
        self.event_colors = {
            'word_validation': '#2ecc71',      # Green
            'word_submission': '#3498db',       # Blue
            'page_leave': '#e74c3c',           # Red
            'page_return': '#f1c40f',          # Yellow
            'mouse_inactive_start': '#95a5a6',  # Gray
            'mouse_active': '#9b59b6',         # Purple
            'meaning_submission': '#1abc9c',    # Turquoise
            'confessed_external_help': '#e67e22'# Orange
        }
        
    def plot_event_timeline(self, save_path: str = None):
        """Create a timeline visualization of events."""
        plt.figure(figsize=(15, 8))
        
        # Calculate relative timestamps
        start_time = self.events_df['timestamp'].min()
        self.events_df['minutes_elapsed'] = (
            self.events_df['timestamp'] - start_time
        ).dt.total_seconds() / 60
        
        # Plot events
        unique_events = self.events_df['eventType'].unique()
        num_events = len(unique_events)
        
        # Create y-positions for different event types
        event_positions = {
            event: i for i, event in enumerate(unique_events)
        }
        
        # Plot each event type
        for event_type in unique_events:
            events = self.events_df[self.events_df['eventType'] == event_type]
            color = self.event_colors.get(event_type, '#34495e')
            
            plt.scatter(
                events['minutes_elapsed'],
                [event_positions[event_type]] * len(events),
                label=event_type,
                c=color,
                s=100,
                alpha=0.6
            )
            
            # Add word labels for validations and submissions
            if event_type in ['word_validation', 'word_submission']:
                for _, event in events.iterrows():
                    word = event.get('word', '')
                    if word:
                        plt.annotate(
                            word,
                            (event['minutes_elapsed'], event_positions[event_type]),
                            xytext=(0, 10),
                            textcoords='offset points',
                            ha='center',
                            fontsize=8,
                            rotation=45
                        )
        
        # Customize plot
        plt.yticks(
            range(num_events),
            unique_events,
            fontsize=10
        )
        plt.xlabel('Minutes Elapsed', fontsize=12)
        plt.title('Event Timeline Analysis', fontsize=14, pad=20)
        plt.grid(True, alpha=0.3)
        
        # Add phase separators
        phases = self.events_df['phase'].unique()
        current_x = 0
        for phase in phases:
            phase_events = self.events_df[self.events_df['phase'] == phase]
            phase_end = phase_events['minutes_elapsed'].max()
            
            if phase_end > current_x:
                plt.axvline(
                    x=phase_end,
                    color='gray',
                    linestyle='--',
                    alpha=0.5
                )
                plt.text(
                    (current_x + phase_end) / 2,
                    num_events + 0.5,
                    phase.upper(),
                    ha='center',
                    va='bottom',
                    fontsize=10
                )
                current_x = phase_end
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
        
        plt.close()
    
    def plot_event_heatmap(self, save_path: str = None):
        """Create a heatmap of event transitions."""
        # Create transition matrix
        events_sequence = self.events_df['eventType'].tolist()
        unique_events = sorted(set(events_sequence))
        
        # Initialize transition matrix
        n_events = len(unique_events)
        transition_matrix = np.zeros((n_events, n_events))
        
        # Fill transition matrix
        for i in range(len(events_sequence) - 1):
            current_idx = unique_events.index(events_sequence[i])
            next_idx = unique_events.index(events_sequence[i + 1])
            transition_matrix[current_idx][next_idx] += 1
        
        # Create heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            transition_matrix,
            xticklabels=unique_events,
            yticklabels=unique_events,
            cmap='YlOrRd',
            annot=True,
            fmt='.0f'
        )
        
        plt.title('Event Transition Heatmap', fontsize=14, pad=20)
        plt.xlabel('Next Event', fontsize=12)
        plt.ylabel('Current Event', fontsize=12)
        
        # Rotate axis labels
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
            
        plt.close()

def main():
    """Main function to create visualizations."""
    try:
        # Get the CSV file
        data_dir = Path(__file__).parent.parent / "participants_data" / "raw_data"
        csv_files = list(data_dir.glob("*.csv"))
        
        if not csv_files:
            print("No CSV files found in the raw_data directory")
            return
        
        # Create visualizations directory
        viz_dir = Path(__file__).parent.parent / "participants_data" / "visualizations"
        viz_dir.mkdir(parents=True, exist_ok=True)
        
        for csv_file in csv_files:
            print(f"\nVisualizing data for participant: {csv_file.stem}")
            
            # Read and process the CSV
            events_df = pd.read_csv(csv_file)
            visualizer = EventVisualizer(events_df)
            
            # Create visualizations
            timeline_path = viz_dir / f"{csv_file.stem}_timeline.png"
            heatmap_path = viz_dir / f"{csv_file.stem}_heatmap.png"
            
            visualizer.plot_event_timeline(str(timeline_path))
            # visualizer.plot_event_heatmap(str(heatmap_path))
            
            print(f"Visualizations saved to {viz_dir}")
            
    except Exception as e:
        print(f"Error in visualization: {e}")
        raise

if __name__ == "__main__":
    main()