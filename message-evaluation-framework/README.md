# Message Evaluation Application

This application allows users to evaluate concept-based messages in a two-step process:

1. **Step 1**: Users identify which concept a message communicates and rate its alignment
2. **Step 2**: Users rate all messages for each concept based on how motivating they are

## Project Structure

```
├── evaluation_app.py         # Main Streamlit application file
├── styles.css                # Separated CSS styling
├── user_progress_tracker.py  # Module for tracking user progress
├── extract_data.py           # Script to extract data from source database
├── database_initialization.py # Script to initialize evaluation collections
└── requirements.txt          # Project dependencies
```

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Before running the application, you need to set up the database:

1. Extract message data from the source database:

```bash
python extract_data.py --uri <mongodb_uri> --source_db <source_db_name> --target_db <target_db_name>
```

2. Initialize the evaluation collections:

```bash
python database_initialization.py --uri <mongodb_uri> --db <db_name>
```

## Running the Application

Run the application using Streamlit:

```bash
streamlit run evaluation_app.py
```

You can configure the MongoDB connection in the application's sidebar or by setting environment variables:

- `MONGODB_URI`: MongoDB connection URI
- `DB_NAME`: Name of the database to use
- `ADMIN_PASS`: Admin password for resetting evaluation data (optional)

## CSS Modifications

The application's CSS has been separated into an external file (`styles.css`) to improve maintainability. This file contains optimized styles with redundancies removed.

To modify the styling:

1. Edit the `styles.css` file
2. Restart the application to see the changes

The CSS file is loaded in `evaluation_app.py` using the following function:

```python
def load_css(css_file):
    with open(css_file, 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Load the CSS
try:
    load_css('styles.css')
except FileNotFoundError:
    st.warning("Custom CSS file not found. Using default styling.")
```

## User Progress Tracking

The application tracks user progress through the evaluation process:

- Which messages have been evaluated in Step 1
- Which concepts have been evaluated in Step 2
- Progress metrics for each step

This information is stored in MongoDB collections with the `eval_` prefix.

## Admin Interface

An admin interface is available in the sidebar for managing evaluation data:

- View collection statistics
- Reset evaluation data for specific collections

Access to these functions requires an admin password, which can be set using the `ADMIN_PASS` environment variable.
