"""
Improved Message Evaluation Application.
A Streamlit application for evaluating concept-based messages in a two-step process:
1. Step 1: Users identify which concept a message communicates and rate its alignment
2. Step 2: Users rate all messages for each concept
"""

import streamlit as st
from pymongo import MongoClient
import random
import pandas as pd
from datetime import datetime
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Message Evaluation App",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
    .header-container {
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1E3A8A;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.2rem 0 1rem 0;
        color: #2563EB;
    }
    .message-box {
        background-color: #F0FFFF;
        border-radius: 0.5rem;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border: 1px solid #E0F7FA;
    }
    .progress-indicator {
        font-size: 1.2rem;
        margin: 1rem 0;
        color: #2563EB;
    }
    .step-label {
            color: gray;
        }
    .step-title {
        color: gray;
        font-weight: bold;
        margin-left: 4px;
    }
    .step-stats {
        color: #3399FF;  /* light blue */
        margin-left: 8px;
        font-weight: bold;
    }
    .stProgress > div > div > div {
        background-color: #ADD8E6 !important;  /* light blue bar */
    }
    .concept-name {
        font-weight: bold;
        color: #2563EB;
    }
    .step-complete {
        color: green;
        font-weight: bold;
    }
    .evaluation-section {
        margin-top: 2rem;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background-color: #fafafa;
    }
    .result-box {
        background-color: #E8F4F8;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #B3E5FC;
    }
    .concept-header {
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        color: #1565C0;
    }
    .true-concept-reveal {
        margin-top: 1.5rem;
        padding: 1rem;
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        border-radius: 0.25rem;
    }
    .concept-definition {
        margin-top: 0.5rem;
        color: #37038c;
    }
    .message-separator {
        margin: 2rem 0;
        border-top: 1px dashed #E5E7EB;
    }
    .message-counter {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 1rem;
    }
    .transition-message {
        margin: 2rem 0;
        padding: 0.5rem;
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        font-size: 1.1rem;
    }
    .message-rating-grid {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .message-cell {
        padding: 0.5rem;
    }
    .rating-cell {
        padding: 0.5rem;
        background-color: #F9FAFB;
        border-radius: 0.5rem;
    }
    .intro-section {
        margin: 2rem auto;
        max-width: 800px;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .intro-step {
        margin: 1.5rem 0;
        padding: 1rem;
        background-color: #e4fbfe;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
    }
    .start-button {
        margin-top: 2rem;
        padding: 0.75rem 1.5rem;
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-size: 1.1rem;
        cursor: pointer;
        text-align: center;
    }
    .concept-definitions-expander {
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        background-color: #f9fafb;
    }
    .alignment-container {
        background-color: #ECFDF5;
        padding: 1rem;
        border-radius: 0.25rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# User Progress Tracker
class UserProgressTracker:
    """Track user's evaluation progress and manage message assignments."""
    
    def __init__(self, db, collection_name="all_messages", eval_collection_prefix="eval_"):
        """
        Initialize the user progress tracker.
        
        Args:
            db: MongoDB database connection
            collection_name: Name of the collection containing all messages
            eval_collection_prefix: Prefix for evaluation collections
        """
        self.db = db
        self.collection_name = collection_name
        self.eval_collection_prefix = eval_collection_prefix
        
        # Set progress collection name
        self.progress_collection = f"{eval_collection_prefix}user_progress"
    
    def get_or_initialize_user_progress(self, evaluator_id):
        """
        Get or initialize user progress document.
        
        Args:
            evaluator_id: ID of the evaluator
            
        Returns:
            User progress document
        """
        # Check if user progress exists
        progress = self.db[self.progress_collection].find_one({"evaluator_id": evaluator_id})
        
        if progress is None:
            # Initialize new progress document
            progress = {
                "evaluator_id": evaluator_id,
                "step1_assigned_messages": [],
                "step1_completed_messages": [],
                "step1_current_index": 0,
                "step2_assigned_concepts": [],
                "step2_completed_concepts": [],
                "step2_current_index": 0,
                "step1_is_complete": False,
                "step2_is_complete": False,
                "last_updated": datetime.now()
            }
            
            # Insert the new progress document
            self.db[self.progress_collection].insert_one(progress)
        
        return progress
    
    def update_user_progress(self, evaluator_id, progress_updates):
        """
        Update user progress document.
        
        Args:
            evaluator_id: ID of the evaluator
            progress_updates: Dictionary of fields to update
            
        Returns:
            True if update was successful, False otherwise
        """
        try:
            # Add last_updated timestamp
            progress_updates["last_updated"] = datetime.now()
            
            # Update progress document
            result = self.db[self.progress_collection].update_one(
                {"evaluator_id": evaluator_id},
                {"$set": progress_updates}
            )
            
            return result.matched_count > 0
        except Exception:
            return False
    
    def get_current_step1_message(self, evaluator_id):
        """
        Get the current message for step 1 evaluation.
        
        Args:
            evaluator_id: ID of the evaluator
            
        Returns:
            Current message or None if all messages have been evaluated
        """
        # Get user progress
        progress = self.get_or_initialize_user_progress(evaluator_id)
        
        # If no assigned messages or all completed, return None
        if len(progress["step1_assigned_messages"]) == 0 or \
           len(progress["step1_completed_messages"]) >= len(progress["step1_assigned_messages"]):
            return None
        
        # Get current index
        current_index = progress["step1_current_index"]
        
        # Get current message ID
        if current_index >= len(progress["step1_assigned_messages"]):
            return None
            
        message_id = progress["step1_assigned_messages"][current_index]["message_id"]
        
        # Get message
        try:
            message = self.db[self.collection_name].find_one({"_id": ObjectId(message_id)})
            
            if message is None:
                # Try to increment index and get next message
                self.update_user_progress(evaluator_id, {"step1_current_index": current_index + 1})
                return self.get_current_step1_message(evaluator_id)
            
            return message
        except Exception:
            return None
    
    def record_step1_evaluation(self, evaluator_id, message_id, evaluation_data):
        """
        Record a step 1 evaluation.
        
        Args:
            evaluator_id: ID of the evaluator
            message_id: ID of the evaluated message
            evaluation_data: Evaluation data
            
        Returns:
            True if recording was successful, False otherwise
        """
        try:
            # Get user progress
            progress = self.get_or_initialize_user_progress(evaluator_id)
            
            # Add evaluation to step1 collection
            step1_collection = f"{self.eval_collection_prefix}step1_evaluations"
            
            # Add timestamp
            evaluation_data["timestamp"] = datetime.now()
            evaluation_data["evaluator_id"] = evaluator_id
            evaluation_data["message_id"] = message_id
            
            result = self.db[step1_collection].insert_one(evaluation_data)
            
            if not result.acknowledged:
                return False
            
            # Update user progress
            completed_messages = progress["step1_completed_messages"]
            completed_messages.append({
                "message_id": message_id,
                "concept_name": evaluation_data["true_concept"],
                "evaluation_id": str(result.inserted_id)
            })
            
            # Find the assigned message index
            current_index = progress["step1_current_index"]
            if current_index < len(progress["step1_assigned_messages"]):
                current_index += 1
            
            # Check if all assigned messages are completed
            step1_is_complete = len(completed_messages) >= len(progress["step1_assigned_messages"])
            
            self.update_user_progress(evaluator_id, {
                "step1_completed_messages": completed_messages,
                "step1_current_index": current_index,
                "step1_is_complete": step1_is_complete
            })
            
            return True
            
        except Exception:
            return False
    
    def get_concept_messages_for_step2(self, evaluator_id, concept_name):
        """
        Get messages for a specific concept from other users.
        
        Args:
            evaluator_id: ID of the evaluator
            concept_name: Name of the concept
            
        Returns:
            List of messages for the concept
        """
        try:
            # Get messages for this concept not created by this user
            messages = list(self.db[self.collection_name].find({
                "concept_name": concept_name,
                "user_id": {"$ne": evaluator_id}
            }))
            
            # If no messages found, try without user filter
            if len(messages) == 0:
                messages = list(self.db[self.collection_name].find({
                    "concept_name": concept_name
                }))
            
            return messages
        except Exception:
            return []
    
    def get_current_step2_concept(self, evaluator_id):
        """
        Get the current concept for step 2 evaluation.
        
        Args:
            evaluator_id: ID of the evaluator
            
        Returns:
            Current concept name or None if all concepts have been evaluated
        """
        # Get user progress
        progress = self.get_or_initialize_user_progress(evaluator_id)
        
        # If no assigned concepts or all completed, return None
        if len(progress["step2_assigned_concepts"]) == 0 or \
           len(progress["step2_completed_concepts"]) >= len(progress["step2_assigned_concepts"]):
            return None
        
        # Get current index
        current_index = progress["step2_current_index"]
        
        # Get current concept
        if current_index >= len(progress["step2_assigned_concepts"]):
            return None
            
        concept_name = progress["step2_assigned_concepts"][current_index]["concept_name"]
        return concept_name
    
    def record_step2_evaluation(self, evaluator_id, concept_name, evaluation_data):
        """
        Record a step 2 evaluation.
        
        Args:
            evaluator_id: ID of the evaluator
            concept_name: Name of the evaluated concept
            evaluation_data: Evaluation data
            
        Returns:
            True if recording was successful, False otherwise
        """
        try:
            # Get user progress
            progress = self.get_or_initialize_user_progress(evaluator_id)
            
            # Add evaluation to step2 collection
            step2_collection = f"{self.eval_collection_prefix}step2_evaluations"
            
            # Add timestamp and identifiers
            evaluation_data["timestamp"] = datetime.now()
            evaluation_data["evaluator_id"] = evaluator_id
            evaluation_data["concept_name"] = concept_name
            
            result = self.db[step2_collection].insert_one(evaluation_data)
            
            if not result.acknowledged:
                return False
            
            # Update user progress
            completed_concepts = progress["step2_completed_concepts"]
            completed_concepts.append({
                "concept_name": concept_name,
                "evaluation_id": str(result.inserted_id)
            })
            
            # Find the assigned concept index
            current_index = progress["step2_current_index"]
            if current_index < len(progress["step2_assigned_concepts"]):
                current_index += 1
            
            # Check if all concepts are completed
            step2_is_complete = len(completed_concepts) >= len(progress["step2_assigned_concepts"])
            
            self.update_user_progress(evaluator_id, {
                "step2_completed_concepts": completed_concepts,
                "step2_current_index": current_index,
                "step2_is_complete": step2_is_complete
            })
            
            return True
            
        except Exception:
            return False
    
    def get_progress_metrics(self, evaluator_id):
        """
        Get user's progress metrics for both evaluation steps.
        
        Args:
            evaluator_id: ID of the evaluator
            
        Returns:
            Dictionary with progress metrics
        """
        # Get user progress
        progress = self.get_or_initialize_user_progress(evaluator_id)
        
        # Calculate step 1 metrics
        step1_total = len(progress["step1_assigned_messages"])
        step1_completed = len(progress["step1_completed_messages"])
        step1_percentage = (step1_completed / step1_total * 100) if step1_total > 0 else 0
        
        # Calculate step 2 metrics
        step2_total = len(progress["step2_assigned_concepts"])
        step2_completed = len(progress["step2_completed_concepts"])
        step2_percentage = (step2_completed / step2_total * 100) if step2_total > 0 else 0
        
        # Create metrics dictionary
        metrics = {
            "step1": {
                "total": step1_total,
                "completed": step1_completed,
                "percentage": min(100, int(step1_percentage)),
                "is_complete": progress.get("step1_is_complete", False)
            },
            "step2": {
                "total": step2_total,
                "completed": step2_completed,
                "percentage": min(100, int(step2_percentage)),
                "is_complete": progress.get("step2_is_complete", False)
            }
        }
        
        return metrics

def admin_interface(db):
    """
    Admin interface for managing evaluation data.
    
    Args:
        db: MongoDB database connection
    """
    import os

    admin_enabled = True
    admin_password = os.getenv("ADMIN_PASS")

    if admin_enabled:
        with st.sidebar.expander("Admin Controls", expanded=False):
            # st.warning("Admin operations can result in data loss!")
            st.subheader("Collection Statistics")
            
            collections = db.list_collection_names()
            eval_collections = [coll for coll in collections if coll.startswith("eval_")]
            
            if not eval_collections:
                st.info("No evaluation collections found.")
            else:
                stats = [{"Collection": coll, "Documents": db[coll].count_documents({})}
                         for coll in eval_collections]
                st.dataframe(pd.DataFrame(stats), use_container_width=True, hide_index=True)
            
            st.subheader("Reset Evaluation Data")

            clear_options = {
                "eval_step1_evaluations": "Step 1 Evaluations",
                "eval_step2_evaluations": "Step 2 Evaluations", 
                "eval_user_progress": "User Progress"
            }

            if "selected_collections" not in st.session_state:
                st.session_state.selected_collections = []
            if "confirm_step" not in st.session_state:
                st.session_state.confirm_step = 0
            if "entered_pass" not in st.session_state:
                st.session_state.entered_pass = ""

            st.session_state.selected_collections = []
            for coll_name, display_name in clear_options.items():
                if st.checkbox(f"Clear {display_name}", value=True, key=f"check_{coll_name}"):
                    st.session_state.selected_collections.append(coll_name)

            if st.session_state.confirm_step == 0 and st.session_state.selected_collections:
                if st.button("Clear Selected Collections", type="primary", key="btn_clear_init"):
                    st.session_state.confirm_step = 1
                    st.rerun()

            if st.session_state.confirm_step == 1:
                st.warning("This will permanently delete data from the selected collections.")
                st.session_state.entered_pass = st.text_input(
                    "Enter Admin Passcode", type="password", key="admin_pass_input"
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Cancel", key="btn_cancel"):
                        st.session_state.confirm_step = 0
                        st.rerun()
                with col2:
                    if st.button("Proceed!", type="primary", key="btn_confirm"):
                        if st.session_state.entered_pass == admin_password:
                            st.session_state.confirm_step = 2
                        else:
                            st.error("Incorrect passcode. Access denied.")
                            st.session_state.confirm_step = 1  # stay on same step
                        st.rerun()

            if st.session_state.confirm_step == 2:
                success_count = 0
                for coll_name in st.session_state.selected_collections:
                    try:
                        if coll_name in collections:
                            db[coll_name].drop()
                            db.create_collection(coll_name)
                            success_count += 1
                    except Exception as e:
                        st.error(f"Error clearing {coll_name}: {str(e)}")
                
                if success_count > 0:
                    st.success(f"Successfully cleared {success_count} collections")
                else:
                    st.error("No collections were cleared. Please try again.")
                
                if st.button("Done", key="btn_done"):
                    st.session_state.confirm_step = 0
                    st.session_state.entered_pass = ""
                    st.rerun()
    # else:
    #     st.sidebar.markdown("🔒 *Admin controls are currently disabled.*")

def get_concept_definitions_from_db(db):
    """Get concept definitions from database"""
    definitions = {}
    try:
        # Find all unique concepts and their definitions
        pipeline = [
            {"$group": {
                "_id": "$concept_name", 
                "definition": {"$first": "$concept_definition"}
            }}
        ]
        
        results = list(db.all_messages.aggregate(pipeline))
        
        # Create a dictionary of concept names to definitions
        for item in results:
            concept_name = item["_id"]
            definition = item.get("definition")
            if concept_name and definition:
                definitions[concept_name] = definition
                
    except Exception as e:
        print(f"Error retrieving concept definitions: {e}")
        
    return definitions

def main():
    """Main application function."""
    
    # Setup database connections from environment variables
    mongo_uri = os.getenv("MONGODB_URI", "mongodb+srv://svdpmukherjee:mongodb_110789@cluster1.bybvc.mongodb.net/")
    db_name = os.getenv("DB_NAME", "evaluation_results")
    
    # Add a sidebar with database configuration UI
    with st.sidebar:
        st.title("Database Settings")
        
        # MongoDB URI field
        mongo_uri_input = st.text_input(
            "MongoDB URI",
            type="password",
            value=mongo_uri,
            help="Connection string for MongoDB"
        )
        
        # Source database name field
        db_name_input = st.text_input(
            "Database Name",
            value=db_name,
            help="Name of the database"
        )
        
        # Apply settings button
        if st.button("Apply Database Settings", use_container_width=True):
            # Update values
            mongo_uri = mongo_uri_input
            db_name = db_name_input
            
            # Clear existing connections and force reconnect
            if "db" in st.session_state:
                del st.session_state["db"]
            if "progress_tracker" in st.session_state:
                del st.session_state["progress_tracker"]
            
            st.success("Database settings updated. Reconnecting...")
            st.rerun()
        
        # Add a force reconnect button for troubleshooting
        # if st.button("Force Reconnect", use_container_width=True):
        #     if "db" in st.session_state:
        #         del st.session_state["db"]
        #     if "progress_tracker" in st.session_state:
        #         del st.session_state["progress_tracker"]
        #     st.success("Forcing reconnection...")
        #     st.rerun()
    
    # Create a fresh database connection each time
    db = None
    try:
        client = MongoClient(mongo_uri)
        client.admin.command('ping')  # Test connection
        db = client[db_name]
        st.sidebar.success(f"Connected to {db_name}")
        
        # Add the admin interface
        admin_interface(db)
    except Exception as e:
        st.sidebar.error(f"Connection error: {e}")
        st.error("Failed to connect to databases. Please check your settings and try again.")
        return
    
    # Check if the collection exists and has data
    if "all_messages" not in db.list_collection_names():
        st.error("'all_messages' collection not found in the database.")
        return
    
    message_count = db.all_messages.count_documents({})
    if message_count == 0:
        st.error("No messages found in the 'all_messages' collection.")
        return
    
    # st.sidebar.info(f"Found {message_count} messages in collection.")
    
    # Initialize progress tracker
    progress_tracker = UserProgressTracker(db, "all_messages", "eval_")
    
    # Load concept definitions from database
    if "concept_definitions" not in st.session_state:
        st.session_state.concept_definitions = get_concept_definitions_from_db(db)
    
    # Get user IDs
    user_ids = []
    try:
        distinct_users = db.all_messages.distinct("user_id")
        user_ids = sorted([u for u in distinct_users if u])
    except Exception as e:
        st.warning(f"Error loading user IDs: {e}")
    
    if not user_ids:
        st.error("No user IDs found in the database.")
        return
    
    # Introduction page
    if "intro_completed" not in st.session_state:
        st.session_state.intro_completed = False
    
    if not st.session_state.intro_completed:
        st.markdown(f"""
            <div class="">
                <h2>Welcome to the Message Evaluation Process!</h2>
                
            </div>
        """, unsafe_allow_html=True)
        st.markdown('<br/>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="intro-step" style="padding: 1em; solid #ccc; border-radius: 5px;">
                <h5>Step 1: Concept Identification and Alignment Rating</h5>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        In this first step, you will:
        - view messages created by others
        - **identify which concept you think each message communicates** (definitions are provided)
        - after submitting your guess, you will see the concept the message was originally intended to convey
        - rate how well the message fits its **intended concept**
        
        This helps us assess how clearly messages communicate their concepts.
        """)

        st.markdown(f"""
            <div class="intro-step" style="padding: 1em; solid #ccc; border-radius: 5px;">
                <h5>Step 2: Rating Messages by Concept</h5>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(""" 
        In the second step, you will:
        - see all messages for each concept grouped together
        - **rate how effective each message would be in motivating you**, imagining yourself as a participant in the study
        - provide any comments or feedback on the messages
        
        This helps us identify the most effective messages for each concept.
        """)
        
        if st.button("Start Evaluation", use_container_width=True, key="start_evaluation"):
            st.session_state.intro_completed = True
            st.rerun()
        
        # Return to stop execution of the rest of the app until user clicks Start
        return
    
    # Add a placeholder option at the beginning
    user_ids = ["Select"] + user_ids
    
    selected_user_id = st.selectbox(
        "Select your User ID",
        options=user_ids,
        help="Select the same User ID you used when generating messages"
    )
    
    if not selected_user_id or selected_user_id == "Select":
        st.warning("Please select your User ID to continue.")
        return
    
    # Store selected user ID in session state
    st.session_state.selected_user_id = selected_user_id
    
    # Get progress metrics for this user
    progress = progress_tracker.get_progress_metrics(selected_user_id)
    
    # Display progress
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div class="progress-indicator">'
            f'<span class="step-label">Step 1:</span>'
            f'<span class="step-title"> Concept Identification and Alignment Rating</span>'
            f'<span class="step-stats"> {progress["step1"]["completed"]}/{progress["step1"]["total"]} ({progress["step1"]["percentage"]}%)</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.progress(progress["step1"]["percentage"] / 100)

    with col2:
        st.markdown(
            f'<div class="progress-indicator">'
            f'<span class="step-label">Step 2:</span>'
            f'<span class="step-title"> Rating Messages by Concept</span>'
            f'<span class="step-stats"> {progress["step2"]["completed"]}/{progress["step2"]["total"]} ({progress["step2"]["percentage"]}%)</span>'
            f'</div>',
            unsafe_allow_html=True
        )
        st.progress(progress["step2"]["percentage"] / 100)
    
    # STEP 1: Concept Identification and Alignment Rating
    if not progress["step1"]["is_complete"]:
        # Get current message for evaluation
        current_message = progress_tracker.get_current_step1_message(selected_user_id)
        
        if current_message:
            # Display step 1 evaluation form
            with st.container():
                st.markdown('<br/>', unsafe_allow_html=True)
                # Get current progress again to get the correct index
                user_progress = progress_tracker.get_or_initialize_user_progress(selected_user_id)
                current_index = user_progress["step1_current_index"]
                total_assigned = len(user_progress["step1_assigned_messages"])
                
                st.markdown(f'<div class="message-counter">Message {current_index + 1} of {total_assigned}</div>', unsafe_allow_html=True)
                
                # Display the message
                st.markdown(f'#### "{current_message["message"]}"')
                
                # Add concept definitions expander for reference
                with st.expander("View Concept Definitions", expanded=False):
                    for concept, definition in st.session_state.concept_definitions.items():
                        st.markdown(f"**{concept}**: {definition}")
                    st.markdown("---")
                    st.markdown("*Use these definitions to help identify which concept the message communicates.*")
                
                st.markdown('<br/>', unsafe_allow_html=True)
                
                # Form for evaluation
                with st.form(key=f"step1_form_{current_index}"):
                    # Create a separate form key for each message evaluation
                    form_key = f"concept_selection_{current_message['_id']}"
                    
                    # Initialize state for this specific message
                    if form_key not in st.session_state:
                        st.session_state[form_key] = {
                            "selected_concept": None,
                            "show_true_concept": False,
                            "confirm_clicked": False
                        }
                    
                    message_state = st.session_state[form_key]
                    
                    # Get concept options from session state
                    concept_options = list(st.session_state.concept_definitions.keys())
                    
                    # Concept selection dropdown - disabled if concept is already confirmed
                    selected_concept = st.selectbox(
                        "Q1: Which concept do you think the message communicates?",
                        options=concept_options,
                        index=0,
                        key=f"concept_select_{form_key}",
                        disabled=message_state["confirm_clicked"]
                    )
                    
                    # Only show confirm button if concept isn't confirmed yet
                    if not message_state["confirm_clicked"]:
                        confirm_button = st.form_submit_button("Confirm Concept Selection")
                        if confirm_button:
                            # Store the selected concept and update state
                            message_state["selected_concept"] = selected_concept
                            message_state["confirm_clicked"] = True
                            message_state["show_true_concept"] = True
                            
                            st.markdown(
                                """
                                <script>
                                    window.scrollTo(0, document.body.scrollHeight);
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                            
                            # Force rerun to update UI
                            st.rerun()
                    
                    # Show true concept after confirmation
                    if message_state["show_true_concept"]:
                        true_concept = current_message["concept_name"]
                        creator_user_id = current_message.get("user_id", "unknown user")
                        
                        # Use the concept definition from the message if available
                        concept_definition = current_message.get("concept_definition", 
                                             st.session_state.concept_definitions.get(true_concept, "Definition not available"))
                        
                        # Create a container for the concept reveal and alignment rating
                        st.markdown(f"""
                            <div class="true-concept-reveal">
                                <h5>This message was originally created for the concept: <strong>{true_concept}</strong></h5>
                                <div class="concept-definition">Note: {concept_definition}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        # st.markdown(f"""
                        #     <div class="true-concept-reveal">
                        #         <h5>This message was created for the concept by {creator_user_id}: <strong>{true_concept}</strong></h5>
                        #         <div class="concept-definition">Note: {concept_definition}</div>
                        #     </div>
                        # """, unsafe_allow_html=True)
                        
                        st.markdown('<br/>', unsafe_allow_html=True)
                        # Place the alignment rating in the same visual container
                        alignment_rating = st.slider(
                            "Q2: How well do you think this message aligns with the intended concept? *(1-lowest alignment, 10-highest alignment)*",
                            min_value=1,
                            max_value=10,
                            value=5,
                            key=f"alignment_{form_key}"
                        )
                        
                        # Text input for comments
                        comments = st.text_area(
                            "If you want to comment on your choice or indicate doubts, write your comments here (optional)",
                            key=f"comments_{form_key}"
                        )
                        
                        # Submit button for evaluation
                        submit_btn = st.form_submit_button("Move to Next Message")
                        
                        if submit_btn:
                            # Prepare evaluation data
                            evaluation_data = {
                                "message_text": current_message["message"],
                                "true_concept": true_concept,
                                "selected_concept": message_state["selected_concept"],
                                "alignment_rating": alignment_rating,
                                "comments": comments,
                                "creator_user_id": creator_user_id
                            }
                            
                            # Record the evaluation
                            success = progress_tracker.record_step1_evaluation(
                                selected_user_id,
                                str(current_message["_id"]),
                                evaluation_data
                            )
                            
                            if success:
                                # Clear message state to prepare for next message
                                st.session_state.pop(form_key, None)
                                st.success("Evaluation saved successfully!")
                                # Force rerun to show next message
                                st.rerun()
                            else:
                                st.error("Failed to save evaluation. Please try again.")
        else:
            # Mark Step 1 as complete
            progress_tracker.update_user_progress(selected_user_id, {"step1_is_complete": True})
            st.success("You've completed your assigned messages for Step 1! Moving to Step 2.")
            # Force rerun to show Step 2
            st.rerun()
    
    # STEP 2: Rating Messages for Each Concept
    elif not progress["step2"]["is_complete"]:
        # Display transition message if Step 1 was just completed
        if "showed_transition" not in st.session_state or not st.session_state.showed_transition:
            # st.markdown('<div class="transition-message">', unsafe_allow_html=True)
            st.markdown(f"""
                        <div class="transition-message">
                            <h5>You have successfully completed Step 1!</h5>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("""
                - Now you're moving to **Step 2** of the evaluation process. In this step, you'll be shown multiple messages for each psychological concept.
                - For each set of messages related to a specific concept, you will **rate how effective each message would be in motivating you**, imagining yourself as a participant in the study.
                
                Let's get started with your first concept!

            """)
            
            # Add a continue button to acknowledge the transition
            if st.button("Continue to Step 2"):
                st.session_state.showed_transition = True
                st.rerun()
            
            return
        
        # Get current concept for evaluation
        current_concept = progress_tracker.get_current_step2_concept(selected_user_id)
        
        if current_concept is None:
            # If all concepts are evaluated, show completion message
            st.success("You've completed all concepts for Step 2! Your evaluation is complete.")
            progress_tracker.update_user_progress(selected_user_id, {"step2_is_complete": True})
        else:
            # Get messages for this concept (only from other users)
            concept_messages = progress_tracker.get_concept_messages_for_step2(selected_user_id, current_concept)
            
            if not concept_messages:
                # Skip this concept if no messages available
                user_progress = progress_tracker.get_or_initialize_user_progress(selected_user_id)
                current_index = user_progress["step2_current_index"]
                progress_tracker.update_user_progress(selected_user_id, {"step2_current_index": current_index + 1})
                st.rerun()
            
            # Display step 2 evaluation form
            with st.container():
                # Get current progress again to get the correct index
                user_progress = progress_tracker.get_or_initialize_user_progress(selected_user_id)
                current_index = user_progress["step2_current_index"]
                total_assigned = len(user_progress["step2_assigned_concepts"])
                
                st.markdown('<br/>', unsafe_allow_html=True)
                
                # Use the concept definition from the first message if available, otherwise from concept_definitions
                concept_definition = concept_messages[0].get("concept_definition", 
                                     st.session_state.concept_definitions.get(current_concept, "Definition not available")) if concept_messages else st.session_state.concept_definitions.get(current_concept, "Definition not available")
                
                # Instruction for the grid layout
                st.markdown("#### Rate each message based on how effective it would be at motivating you to perform well and your user experience? ")
                    
                # Display concept info
                st.markdown(f'<div class="message-counter">Concept {current_index + 1} of {total_assigned}: {current_concept}</div>', unsafe_allow_html=True)
                st.markdown(f"> ##### {concept_definition}", unsafe_allow_html=True)
                
                st.markdown('<br/>', unsafe_allow_html=True)
                
                # Create a form for rating all messages for this concept
                with st.form(key=f"step2_form_{current_concept}"):
                    # Store message ratings
                    message_ratings = []
                    
                    # Display each message with rating slider in a grid layout
                    for i, message in enumerate(concept_messages):
                        creator_user_id = message.get("user_id", "unknown user")
                        
                        col1, col2 = st.columns([3, 2])  # Adjust ratio as needed for layout balance
    
                        with col1:
                            # st.markdown(f"**Message {i+1}** (Created by: {creator_user_id})")
                            # st.markdown(f"> **Message {i+1}** (Created by: {creator_user_id}): {message['message']}")
                            st.markdown(f"> **Message {i+1}**: {message['message']}")
                            # Display a horizontal rule
                            st.markdown("---")
                        
                        with col2:
                            rating = st.slider(
                                f"Rate Message {i+1} *(1-least favorite, 10-most favorite)*",
                                min_value=1,
                                max_value=10 ,
                                value=5,
                                key=f"step2_rating_{current_concept}_{i}"
                            )
                        
                        # Store rating
                        message_ratings.append({
                            "message_id": str(message["_id"]),
                            "message_text": message["message"],
                            "creator_user_id": creator_user_id,
                            "rating": rating
                        })
                    
                    # Text input for comments about this concept's messages
                    comments = st.text_area(
                        "If you want to comment your choice or indicate doubts, write your comments here (optional)",
                        key=f"step2_comments_{current_concept}"
                    )
                    
                    # Submit button for this concept
                    submit_text = "Submit Evaluation & Move to Next Concept" 
                    submit_btn = st.form_submit_button(submit_text)
                    
                    if submit_btn:
                        # Prepare evaluation data
                        evaluation_data = {
                            "message_ratings": message_ratings,
                            "comments": comments
                        }
                        
                        # Record the evaluation
                        success = progress_tracker.record_step2_evaluation(
                            selected_user_id,
                            current_concept,
                            evaluation_data
                        )
                        
                        if success:
                            st.success("Evaluation saved successfully!")
                            st.markdown(
                                """
                                <script>
                                    window.scrollTo(0, 0);
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                            # Force rerun to show next concept
                            st.rerun()
                        else:
                            st.error("Failed to save evaluation. Please try again.")
    
    # Both steps completed
    else:
        st.markdown('<div class="section-header">Evaluation Complete</div>', unsafe_allow_html=True)
        st.success("Thank you for completing the message evaluation!")
        
        # Show evaluation summary
        st.markdown("### Your Evaluation Summary")
        
        st.markdown(f"""
        - Step 1 (Concept Identification and Alignment Rating): <span class="step-complete">{progress["step1"]["completed"]}/{progress["step1"]["total"]} messages evaluated</span>
        - Step 2 (Rating Messages by Concept): <span class="step-complete">{progress["step2"]["completed"]}/{progress["step2"]["total"]} concepts evaluated</span>
        """, unsafe_allow_html=True)
       
if __name__ == "__main__":
    # Initialize session state for intro page
    if "intro_completed" not in st.session_state:
        st.session_state.intro_completed = False
    
    main()