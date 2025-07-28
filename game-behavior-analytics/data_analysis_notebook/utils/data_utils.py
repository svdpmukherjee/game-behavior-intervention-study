import pandas as pd

def load_and_prepare_data(filepath):
    """Load and preprocess the dataset"""
    df = pd.read_csv(filepath)

    def categorize_cheating(rate):
        if rate == 0:
            return 0  # Non-cheater
        elif rate == 1:
            return 2  # Full cheater
        else:
            return 1  # Partial cheater

    # Construct derived variables
    df['cheating_behavior'] = df['cheating_rate_main_round'].apply(categorize_cheating)
    df['experience'] = (df['task_satisfaction'] + df['task_engagement']) / 2
    df['performance'] = df['performance_score_including_cheated_words']

    df = df.dropna(subset=['cheating_behavior', 'performance', 'experience', 'concept'])

    # Ensure 'control' is first
    df['concept'] = df['concept'].astype('category')
    if df['concept'].cat.categories[0] != 'control':
        df['concept'] = df['concept'].cat.reorder_categories(
            ['control'] + [c for c in df['concept'].cat.categories if c != 'control']
        )

    df['concept_idx'] = df['concept'].cat.codes
    concepts = [c for c in df['concept'].cat.categories if c != 'control']

    # Nested message index
    message_df = df[['concept', 'motivational_message_id']].drop_duplicates()
    concept_message_map = {
        concept: {msg: i for i, msg in enumerate(
            message_df[message_df['concept'] == concept]['motivational_message_id']
        )}
        for concept in df['concept'].cat.categories
    }

    df['message_within_concept'] = df.apply(
        lambda row: concept_message_map[row['concept']][row['motivational_message_id']], axis=1
    )

    return df, concepts

