"""
Styling module.
Contains custom CSS and styling functions for the application.
"""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS to the application."""
    st.markdown("""
    <style>
        /* General spacing for better readability */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Add spacing between sections/containers */
        [data-testid="stVerticalBlock"] > div:has(> [data-testid="stHorizontalBlock"]) {
            margin-bottom: 2rem;
        }
        
        /* Improve container styling */
        section[data-testid="stSidebar"] .block-container,
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        
        /* Add spacing between elements in containers */
        div.element-container {
            margin-bottom: 1rem;
        }
        
        /* Add spacing for containers with borders */
        div[data-testid="stExpander"], 
        div.streamlit-expanderContent {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Container styling */
        [data-testid="stContainer"] {
            margin-top: 1.5rem;
            margin-bottom: 2rem;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        
        /* Headers */
        .main-header {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            color: #1E3A8A;
        }
        
        .sub-header {
            font-size: 1rem;
            font-weight: bold;
            margin: 1.5rem 0;
            color: #1E3A8A;
        }
        
        .section-header {
            font-size: 1.2rem;
            font-weight: bold;
            margin: 1.2rem 0 1rem 0;
            color: #2563EB;
        }
        
        /* Explanation text */
        .section-explanation {
            font-size: 0.9rem;
            color: #555;
            margin-bottom: 1.2rem;
            padding: 12px;
            background-color: #F0FFFF;
            border-radius: 5px;
            border-left: 3px solid #4e8cff;
        }
        
        /* Message display box */
        .message-box {
            background-color: #F0FFFF;
            border-radius: 0.5rem;
            padding: 1.2rem;
            margin: 0.8rem 0;
            border: 1px solid #E0F7FA;
        }
        
        .iteration-label {
            font-size: 0.8rem;
            color: #555;
            margin-top: 0.5rem;
        }
        
        .score-indicator {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.5rem 0;
        }
        
        .score-high {
            color: #28a745;
        }
        
        .score-medium {
            color: #ffc107;
        }
        
        .score-low {
            color: #dc3545;
        }
        
        .feedback-box {
            background-color: #e6f7ff;
            border-left: 4px solid #1890ff;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .control-panel {
            background-color: #f8f9fa;
            border-radius: 0.5rem;
            padding: 1.2rem;
            margin: 1rem 0;
        }
        
        .model-info {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }
        
        .edit-button {
            margin-left: 0.5rem;
        }
        
        .concept-panel {
            display: flex;
            gap: 20px;
            margin: 1rem 0;
        }
        
        .concept-list {
            flex: 1;
        }
        
        .concept-definition {
            flex: 2;
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
        }
        
        .task-context-panel {
            display: flex;
            gap: 20px;
            margin: 1rem 0;
        }
        
        .task-list {
            flex: 1;
        }
        
        .task-details {
            flex: 2;
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
        }
        
        .delete-button {
            background-color: #ff6b6b;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            cursor: pointer;
        }
        
        .stButton>button {
            width: 100%;
            margin-top: 0.5rem;
        }
        
        /* Add extra bottom padding when multiple buttons are stacked */
        .stButton:not(:last-child) {
            margin-bottom: 0.75rem;
        }
        
        .expander-container {
        display: inline-block;
        max-width: 60px;  /* Adjust based on how narrow you want it */
    }
    
    </style>
    """, unsafe_allow_html=True)