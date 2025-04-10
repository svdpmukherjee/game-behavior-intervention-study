"""
Header module.
Contains functions for displaying the application header.
"""

import streamlit as st

def display_header():
    """Display the application header."""
    st.markdown(
        """
        <div class="header-container">
            <div class="main-header">Generate Concept-Based Messages using LLMs with Human-in-the-Loop</div>
            <div class="header-description">
                This tool helps researchers and practitioners craft messages that closely align with specific psychological concepts.
                You'll generate, evaluate, and iteratively refine messages with AI assistance and your own expert feedback.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

        # st.markdown(
        #     '<div class="section-explanation">This tool helps researchers and practitioners craft messages that closely '
        #     'align with specific psychological concepts. You\'ll generate, evaluate, and iteratively refine messages '
        #     'with AI assistance and your own expert feedback.</div>',
        #     unsafe_allow_html=True
        # )