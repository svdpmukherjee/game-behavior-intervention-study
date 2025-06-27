import pandas as pd
import numpy as np
import re

# Step 1: Load the CSV file
df = pd.read_csv('../data/survey_output/survey_results.csv')

# Step 1.5: Remove rows without birth year entries (incomplete survey responses)
print(f"Original dataset shape: {df.shape}")

# Check which column contains birth year data
birth_year_column = "What is your birth year?"
if birth_year_column in df.columns:
    # Remove rows where birth year is missing or empty
    df = df.dropna(subset=[birth_year_column])
    df = df[df[birth_year_column] != '']  # Also remove empty strings
    print(f"After removing incomplete entries (missing birth year): {df.shape}")
else:
    print(f"Warning: Birth year column '{birth_year_column}' not found in dataset")
    print("Available columns:", df.columns.tolist())

# Step 2: Create a dictionary to map original column names to desired column names
# Updated dictionary to map original column names from the CSV to desired column names
column_mapping = {
    # Prolific ID
    "Please enter your Prolific ID:": "Prolific ID",
    
    # Usability
    "Please indicate your agreement with the following statements: [The instructions for the word creation challenge were easy to understand]": "Usability_1",
    "Please indicate your agreement with the following statements: [The study interface was intuitive to use]": "Usability_2",
    "Please indicate your agreement with the following statements: [I found it easy to navigate through the different parts of the study]": "Usability_3",
    
    # Engagement
    "Please indicate your agreement with the following statements: [I felt detached from the outside world while engaging in the word creation challenge]": "Engagement_1",
    "Please indicate your agreement with the following statements: [I did not care to check events that were happening in the real world during the challenge]": "Engagement_2",
    "Please indicate your agreement with the following statements: [I could not tell that I was getting tired during the challenge]": "Engagement_3",
    "Please indicate your agreement with the following statements: [Sometimes I lost track of time during the challenge]": "Engagement_4",
    "Please indicate your agreement with the following statements: [I temporarily forgot about my everyday worries during the challenge]": "Engagement_5",
    "Please indicate your agreement with the following statements: [I tended to spend more time on the challenge than I had planned]": "Engagement_6",
    "Please indicate your agreement with the following statements: [I could block out most other distractions during the challenge]": "Engagement_7",
    "Please indicate your agreement with the following statements: [After the session ended, I wish I could have continued working on more challenges]": "Engagement_8",
    
    # Satisfaction
    "Please indicate your agreement with the following statements: [I think the word creation challenge was fun]": "Satisfaction_1",
    "Please indicate your agreement with the following statements: [I enjoyed participating in the challenge]": "Satisfaction_2",
    "Please indicate your agreement with the following statements: [I felt bored during the challenge]": "Satisfaction_3",
    "Please indicate your agreement with the following statements: [I am likely to recommend this challenge to others]": "Satisfaction_4",
    "Please indicate your agreement with the following statements: [If given the chance, I want to try this challenge again]": "Satisfaction_5",
    
    # Message comprehension
    "Please complete this sentence: [I remember the message talked about...]": "message_comprehend",
    "Please indicate how confident you are about the following statement [I clearly remember what the message was about.]": "message_confidence",
    
    # Understanding
    "Please indicate your agreement with the following statements:  [I understood the content of the message]": "Understand_1",
    "Please indicate your agreement with the following statements:  [The message was relevant to the task]": "Understand_2",
    "Please indicate your agreement with the following statements:  [I understood why the message was shown]": "Understand_3",
    
    # Message
    "Please describe in your own words: [What emotions or thoughts came up for you while reading the message?]": "message_attitude",
    "Please describe in your own words: [In what specific ways, if any, did the message influence how you approached the word creation challenge?]": "message_impact",
    "Please describe in your own words: [Were there any aspects of the message that stayed with you throughout the challenge? If so, what were they?]": "message_persistence",
    "Please describe in your own words: [If you were to create a similar message for future participants, what would you emphasize or include?]": "message_suggestion",
    
    # PME honest playing
    "Please indicate your agreement with the following statements: [The message made me stop and think about my behavior during the word creation challenge]": "PME_honest_playing_1",
    "Please indicate your agreement with the following statements: [The message made me feel concerned about how I approached the  challenge]": "PME_honest_playing_2",
    "Please indicate your agreement with the following statements: [The message motivated me to rely on my own skills while completing the challenge]": "PME_honest_playing_3",
    
    # PME performance
    "Please indicate your agreement with the following statements: [The message made me want to focus more on solving the word creation challenge]": "PME_performance_1",
    "Please indicate your agreement with the following statements: [I felt excited to solve the challenge after reading the message]": "PME_performance_2",
    "Please indicate your agreement with the following statements: [I was more motivated to solve this challenge after reading the message than I usually am with similar tasks]": "PME_performance_3",
    "Please indicate your agreement with the following statements: [I found it easy to stay focused on the challenge after reading the message]": "PME_performance_4",
    "Please indicate your agreement with the following statements: [I would recommend showing this type of message before similar tasks to others]": "PME_performance_5",
    
    # PME UX
    "Please indicate your agreement with the following statements: [The message was easy to understand]": "PME_UX_1",
    "Please indicate your agreement with the following statements: [The message felt personally relevant to me]": "PME_UX_2",
    "Please indicate your agreement with the following statements: [The message was believable]": "PME_UX_3",
    
    # PME SDT Components (satisfaction and frustration)
    "After reading the message... [I felt I had a lot of freedom in deciding how to approach the word creation challenge]": "PME_aut_sat_1",
    "After reading the message... [I felt capable of creating good words from the letters]": "PME_com_sat_1",
    "After reading the message... [I felt connected to the broader community of participants in this study]": "PME_rel_sat_1",
    "After reading the message... [I felt restricted in how I could approach the challenge]": "PME_aut_fru_1",
    "After reading the message... [I felt incapable of succeeding at the word creation tasks]": "PME_com_fru_1",
    "After reading the message... [I felt disconnected from the purpose of this study]": "PME_rel_fru_1",
    "After reading the message... [I felt free to choose my own strategies during the challenge]": "PME_aut_sat_2",
    "After reading the message... [I felt I could accomplish even the most difficult challenges]": "PME_com_sat_2",
    "After reading the message... [I felt that the people behind this study genuinely valued my participation]": "PME_rel_sat_2",
    "After reading the message... [I felt under pressure to approach the challenge in a certain way]": "PME_aut_fru_2",
    "After reading the message... [I felt unable to master the harder word creation challenges]": "PME_com_fru_2",
    "After reading the message... [I felt like my participation in the study didn’t really matter to anyone]": "PME_rel_fru_2",
    
    # PME Self-Efficacy Components
    "After reading the message... [I felt more confident in my ability to solve these challenges, based on my past successes with similar challenges]": "PME_efficacy_PA_1",
    "After reading the message... [The message helped me visualize how to approach the challenges effectively]": "PME_efficacy_VE_1",
    "After reading the message... [I was reminded of positive feedback I've received about my problem-solving skills]": "PME_efficacy_VP_1",
    "After reading the message... [I felt less stressed about tackling the challenges]": "PME_efficacy_EA_1",
    "After reading the message... [I believed I could handle even the most difficult word challenges]": "PME_efficacy_PA_2",
    "After reading the message... [The message motivated me by reminding me how others succeed at similar challenges]": "PME_efficacy_VE_2",
    "After reading the message... [I felt more mentally clear and focused when approaching the challenges]": "PME_efficacy_EA_2",
    "After reading the message... [I felt reassured about my skills for this specific type of challenge]": "PME_efficacy_VP_2",
    
    # PME Social Norms Components
    "After reading the message... [I understood better what behaviors are valued in the word creation challenges]": "PME_inj_norm_1",
    "After reading the message... [I got the impression that most participants solved the challenges on their own]": "PME_des_norm_1",
    "After reading the message... [I believed that solving the challenges with my own skills would be seen positively by the study organizer (researcher)]": "PME_inj_norm_2",
    "After reading the message... [I felt connected to other participants who were solving the challenges in this study]": "PME_ref_norm_1",
    "After reading the message... [I thought about how the study organizer might judge my approach to the challenges]": "PME_sanc_norm_1",
    "After reading the message... [I often considered how others typically approached solving the challenges]": "PME_des_norm_2",
    "After reading the message... [I thought about whether my approach to the challenges would be viewed positively or negatively by the study organizer]": "PME_sanc_norm_2",
    "After reading the message... [I considered how the way I solved the challenges might reflect on the kind of participant I am]": "PME_ref_norm_2",
    
    # PME Cognitive Dissonance Components
    "After reading the message... [I regretted participating in this word creation challenge]": "PME_dissonance_1",
    "After reading the message... [This challenge made me feel uncomfortable]": "PME_dissonance_2",
    "After reading the message... [I disliked the challenge because it challenged my beliefs]": "PME_dissonance_3",
    "After reading the message... [I agreed with the approach I took during the challenge]": "PME_dissonance_4",
    "After reading the message... [I felt uncomfortable while participating in this challenge]": "PME_dissonance_5",
    "After reading the message... [This challenge made me question my own beliefs]": "PME_dissonance_6",
    "After reading the message... [I enjoyed participating in this challenge]": "PME_dissonance_7",
    "After reading the message... [I would feel uncomfortable recommending the approach I took to others]": "PME_dissonance_8",
    "After reading the message... [I liked participating in this challenge]": "PME_dissonance_9",
    
    # PME Moral Disengagement
    "Please indicate your agreement with the following statements. [Sometimes getting ahead of the curve is more important than adhering to rules]": "PME_disengagement_1",
    "Please indicate your agreement with the following statements. [Rules should be flexible enough to be adapted to different situations]": "PME_disengagement_2",
    "Please indicate your agreement with the following statements. [Bending rules sometimes when tasks are difficult is appropriate because no one gets hurt]": "PME_disengagement_3",
    "Please indicate your agreement with the following statements. [If others engage in bending rules, then the behavior is morally permissible]": "PME_disengagement_4",
    "Please indicate your agreement with the following statements. [It is appropriate to bend rules as long as it is not at someone else’s expense]": "PME_disengagement_5",
    "Please indicate your agreement with the following statements. [End results are more important than the means by which one pursues those results]": "PME_disengagement_6",
    
    # Demographics - main columns only (not the "Other" fields)
    "What is your birth year?": "birth_year", 
    "To which gender identity do you most identify with?": "gender",
    "Which ethnicity best describes you? (Please choose only one)": "ethnicity",
    "What is your native language? (If multiple, please add them all)": "native_language",
    "What is the highest degree or level of school you have completed? (If currently enrolled, highest degree received)": "highest_education",
    "How many online tests did you take in the last 3 years?": "online_tests_taken_last_3_years",
    "What do you think about this study?   We would be very happy to have your opinion and feedback about any aspect of this study (the word creation task, the message text, or the quality of the survey questions).   Your feedback is invaluable to improve future studies: ": "feedback"
}

def clean_text_field(text):
    """
    Clean text fields to prevent CSV parsing issues.
    
    This function:
    1. Converts to string and handles NaN values
    2. Removes or replaces problematic characters
    3. Normalizes whitespace
    """
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to string
    text = str(text)
    
    # Replace newline characters with spaces
    text = re.sub(r'\n+', ' ', text)
    
    # Replace carriage returns with spaces
    text = re.sub(r'\r+', ' ', text)
    
    # Replace multiple whitespaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading and trailing whitespace
    text = text.strip()
    
    # Remove any remaining problematic characters that might interfere with CSV parsing
    # Remove or replace quotes that might cause issues
    text = text.replace('"', "'")  # Replace double quotes with single quotes
    
    # Remove any control characters (characters 0-31 except space)
    text = ''.join(char for char in text if ord(char) >= 32 or char in [' ', '\t'])
    
    return text

# Step 3: Create a new DataFrame with only the columns we want and renamed
new_columns = {}
for old_col, new_col in column_mapping.items():
    if old_col in df.columns:
        new_columns[old_col] = new_col
    else:
        print(f"Warning: Column '{old_col}' not found in the dataset")

# Create the new DataFrame with renamed columns
transformed_df = df[list(new_columns.keys())].rename(columns=new_columns)

print(f"Transformed dataset shape: {transformed_df.shape}")

# Step 4: Handle the "Other" fields for demographics
# For gender
if "To which gender identity do you most identify with?" in df.columns and "To which gender identity do you most identify with? [Other]" in df.columns:
    # Create a mask for rows where "Other" was selected
    other_gender_mask = (df["To which gender identity do you most identify with?"] == "Other")
    
    # Get the "Other" text values
    other_gender_values = df.loc[other_gender_mask, "To which gender identity do you most identify with? [Other]"]
    
    # Apply these values to the gender column in the transformed DataFrame
    for idx, value in other_gender_values.items():
        if not pd.isna(value):  # Only update if there's an actual value
            transformed_df.loc[idx, "gender"] = clean_text_field(value)

# For ethnicity
if "Which ethnicity best describes you? (Please choose only one)" in df.columns and "Which ethnicity best describes you? (Please choose only one) [Other]" in df.columns:
    # Create a mask for rows where "Other" was selected
    other_ethnicity_mask = (df["Which ethnicity best describes you? (Please choose only one)"] == "Other")
    
    # Get the "Other" text values
    other_ethnicity_values = df.loc[other_ethnicity_mask, "Which ethnicity best describes you? (Please choose only one) [Other]"]
    
    # Apply these values to the ethnicity column in the transformed DataFrame
    for idx, value in other_ethnicity_values.items():
        if not pd.isna(value):  # Only update if there's an actual value
            transformed_df.loc[idx, "ethnicity"] = clean_text_field(value)

# For highest education
if "What is the highest degree or level of school you have completed? (If currently enrolled, highest degree received)" in df.columns and "What is the highest degree or level of school you have completed? (If currently enrolled, highest degree received) [Other]" in df.columns:
    # Create a mask for rows where "Other" was selected
    other_education_mask = (df["What is the highest degree or level of school you have completed? (If currently enrolled, highest degree received)"] == "Other")
    
    # Get the "Other" text values
    other_education_values = df.loc[other_education_mask, "What is the highest degree or level of school you have completed? (If currently enrolled, highest degree received) [Other]"]
    
    # Apply these values to the highest_education column in the transformed DataFrame
    for idx, value in other_education_values.items():
        if not pd.isna(value):  # Only update if there's an actual value
            transformed_df.loc[idx, "highest_education"] = clean_text_field(value)

# Step 4.5: Clean all text fields to prevent CSV parsing issues
text_columns = [
    "Prolific ID", 
    "message_comprehend", 
    "message_attitude", 
    "message_impact", 
    "message_persistence", 
    "message_suggestion",
    "gender",
    "ethnicity",
    "native_language",
    "highest_education",
    "feedback"
]

print("Cleaning text fields to prevent CSV parsing issues...")
for col in text_columns:
    if col in transformed_df.columns:
        print(f"  Cleaning column: {col}")
        original_count = transformed_df[col].notna().sum()
        transformed_df[col] = transformed_df[col].apply(clean_text_field)
        cleaned_count = (transformed_df[col] != '').sum()
        print(f"    Original non-null entries: {original_count}, After cleaning: {cleaned_count}")

# Step 5: Convert all Likert scale responses to numeric values if needed
likert_mapping = {
    "Strongly disagree": 1,
    "Disagree": 2,
    "Somewhat disagree": 3,
    "Neither disagree nor agree": 4,
    "Somewhat agree": 5,
    "Agree": 6,
    "Strongly agree": 7,
    "Not confident at all": 1,
    "Slightly confident": 2,
    "Somewhat confident": 3,
    "Fairly confident": 4,
    "Completely confident": 5,
}

# Define the reverse-coded items
reverse_coded_items = [
    "Satisfaction_3",        # "I felt bored during the challenge"
    "PME_dissonance_4",      # "I agreed with the approach I took during the challenge"
    "PME_dissonance_7",      # "I enjoyed participating in this challenge"
    "PME_dissonance_9"       # "I liked participating in this challenge]": "PME_dissonance_9"
]

# Apply the mapping to all columns except the text-based ones
print("Converting Likert scale responses to numeric values...")
for col in transformed_df.columns:
    if col not in text_columns and col not in ['birth_year', 'online_tests_taken_last_3_years']:
        if col in reverse_coded_items:
            # For reverse-coded items, flip the Likert scale (1→7, 2→6, etc.)
            # First convert to numeric values
            print(f"  Processing reverse-coded item: {col}")
            transformed_df[col] = transformed_df[col].map(likert_mapping)
            # Then reverse the scale (1→7, 2→6, etc.)
            transformed_df[col] = 8 - transformed_df[col]
        else:
            # For regular items, apply the standard mapping
            print(f"  Processing regular item: {col}")
            transformed_df[col] = transformed_df[col].map(likert_mapping)

# Step 6: Calculate age from birth year
from datetime import datetime
current_year = datetime.now().year

# First make sure birth_year is numeric, and handle any conversions/cleaning needed
transformed_df['birth_year'] = pd.to_numeric(transformed_df['birth_year'], errors='coerce')

# Now calculate age
transformed_df['age'] = (current_year - transformed_df['birth_year']).astype(int)

# Drop the birth_year column as we now have age
transformed_df = transformed_df.drop('birth_year', axis=1)

# Convert online_tests_taken_last_3_years to numeric if needed
transformed_df['online_tests_taken_last_3_years'] = pd.to_numeric(transformed_df['online_tests_taken_last_3_years'], errors='coerce')

# Step 7: Final cleanup - remove any rows that still have missing critical data after transformation
print(f"Dataset shape before final cleanup: {transformed_df.shape}")

# Remove rows where age couldn't be calculated (invalid birth years)
transformed_df = transformed_df.dropna(subset=['age'])
print(f"Final dataset shape after removing rows with invalid age: {transformed_df.shape}")

# Step 8: Additional validation to ensure no problematic characters remain
print("Performing final validation...")
for col in text_columns:
    if col in transformed_df.columns:
        # Check for any remaining newlines or carriage returns
        problematic_rows = transformed_df[transformed_df[col].str.contains(r'[\n\r]', na=False)]
        if len(problematic_rows) > 0:
            print(f"Warning: Found {len(problematic_rows)} rows with remaining newlines in {col}")
            # Clean them again if any remain
            transformed_df[col] = transformed_df[col].apply(clean_text_field)

# Step 9: Save the transformed data to a new CSV file with proper quoting
print("Saving transformed survey results...")
transformed_df.to_csv('../data/survey_output/transformed_survey_results.csv', 
                     index=False,
                     quoting=1,  # QUOTE_ALL - ensures all fields are quoted
                     escapechar='\\',  # Use backslash as escape character
                     lineterminator='\n')  # Use consistent line terminator

print("Survey results transformed successfully!")
print(f"Final dataset contains {len(transformed_df)} complete survey responses.")

# Step 10: Verification - read the saved file back to ensure it parses correctly
print("Verifying saved file...")
try:
    verification_df = pd.read_csv('../data/survey_output/transformed_survey_results.csv')
    print(f"Verification successful! Saved file shape: {verification_df.shape}")
    print(f"Expected shape: {transformed_df.shape}")
    
    if verification_df.shape == transformed_df.shape:
        print("✓ File saved and verified successfully!")
    else:
        print("⚠ Warning: Saved file shape doesn't match expected shape")
        
except Exception as e:
    print(f"✗ Error reading saved file: {e}")
    print("This indicates there might still be CSV parsing issues.")