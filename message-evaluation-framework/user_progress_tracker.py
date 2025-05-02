"""
User progress tracker module for evaluation app.

Handles tracking which messages have been evaluated by each user and
provides functions to get messages for evaluation based on the user's progress.
"""

import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from bson.objectid import ObjectId

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
        
        # Ensure collections exist
        self._ensure_collections()
 
    
    def _ensure_collections(self):
        """Ensure that required collections exist."""
        # Check if the progress collection exists
        self.progress_collection = f"{self.eval_collection_prefix}user_progress"
        
        collections = self.db.list_collection_names()
        
        # Check if progress collection exists in a safe way
        progress_exists = any(coll == self.progress_collection for coll in collections)
        
        if not progress_exists:
            self.db.create_collection(self.progress_collection)
            # Create indexes
            self.db[self.progress_collection].create_index("evaluator_id")
        
        # Ensure step1 and step2 collections exist
        step1_collection = f"{self.eval_collection_prefix}step1_evaluations"
        step2_collection = f"{self.eval_collection_prefix}step2_evaluations"
        
        # Check if step1 collection exists in a safe way
        step1_exists = any(coll == step1_collection for coll in collections)
        
        if not step1_exists:
            self.db.create_collection(step1_collection)
            self.db[step1_collection].create_index("evaluator_id")
            self.db[step1_collection].create_index("message_id")
        
        # Check if step2 collection exists in a safe way
        step2_exists = any(coll == step2_collection for coll in collections)
        
        if not step2_exists:
            self.db.create_collection(step2_collection)
            self.db[step2_collection].create_index("evaluator_id")
            self.db[step2_collection].create_index("concept_name")
    
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
            
            return result.modified_count > 0
        except Exception as e:
            return False
    
    def assign_messages_for_step1(self, evaluator_id, batch_size=60):
        """
        Assign messages for step 1 evaluation.
        The default batch size is now 60 messages.
        
        Args:
            evaluator_id: ID of the evaluator
            batch_size: Number of messages to assign at once (default: 60)
            
        Returns:
            List of assigned messages
        """
        # Get user progress
        progress = self.get_or_initialize_user_progress(evaluator_id)
        
        # If user already has assigned messages, return them
        if len(progress["step1_assigned_messages"]) > 0:
            # Get the messages by IDs
            message_ids = [m["message_id"] for m in progress["step1_assigned_messages"]]
            # Convert string IDs to ObjectId
            object_ids = [ObjectId(id_str) for id_str in message_ids]
            
            assigned_messages = list(self.db[self.collection_name].find({"_id": {"$in": object_ids}}))
            
            # Return messages not yet completed
            completed_ids = [m["message_id"] for m in progress["step1_completed_messages"]]
            remaining_messages = [m for m in assigned_messages if str(m["_id"]) not in completed_ids]
            
            return remaining_messages
        
        # Get all messages except those created by this user
        try:
            # Check if collection exists and has documents
            count = self.db[self.collection_name].count_documents({})
            
            # Get messages not created by this user
            all_messages = list(self.db[self.collection_name].find({"user_id": {"$ne": evaluator_id}}))
            
            
            if len(all_messages) == 0:
                # If no messages are found with user_id filter, try getting all messages
                all_messages = list(self.db[self.collection_name].find())
                
                if len(all_messages) == 0:
                    return []
        except Exception as e:
            return []
        
        # Randomly shuffle messages
        random.shuffle(all_messages)
        
        # Take a batch of messages (up to batch_size or all available messages)
        assigned_batch = all_messages[:min(batch_size, len(all_messages))]
        
        # Store the assignment in user progress
        assigned_message_refs = [{"message_id": str(m["_id"]), "concept_name": m["concept_name"]} for m in assigned_batch]
        
        self.update_user_progress(evaluator_id, {
            "step1_assigned_messages": assigned_message_refs
        })
        
        return assigned_batch
    
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
            
            self.update_user_progress(evaluator_id, {
                "step1_completed_messages": completed_messages,
                "step1_current_index": current_index
            })
            
            return True
            
        except Exception as e:
            return False
    
    def get_available_concepts_for_step2(self, evaluator_id):
        """
        Get concepts that have messages from other users for step 2 evaluation.
        
        Args:
            evaluator_id: ID of the evaluator
            
        Returns:
            Dictionary of concept names to lists of messages
        """
        # Get user progress
        progress = self.get_or_initialize_user_progress(evaluator_id)
        
        # If user already has assigned concepts, return them
        if len(progress["step2_assigned_concepts"]) > 0:
            assigned_concepts = progress["step2_assigned_concepts"]
            completed_concepts = [c["concept_name"] for c in progress["step2_completed_concepts"]]
            
            # Get remaining concepts
            remaining_concepts = [c for c in assigned_concepts if c["concept_name"] not in completed_concepts]
            
            concept_messages = {}
            for concept_data in remaining_concepts:
                concept_name = concept_data["concept_name"]
                # Get messages for this concept
                messages = list(self.db[self.collection_name].find({
                    "concept_name": concept_name,
                    "user_id": {"$ne": evaluator_id}
                }))
                
                if len(messages) > 0:
                    concept_messages[concept_name] = messages
                else:
                    # If no messages found with user filter, try without filter
                    messages = list(self.db[self.collection_name].find({
                        "concept_name": concept_name
                    }))
                    if len(messages) > 0:
                        concept_messages[concept_name] = messages
            
            return concept_messages
        
        # Find all concepts with messages
        try:
            # Get all distinct concept names
            pipeline = [
                {"$group": {"_id": "$concept_name"}}
            ]
            
            available_concepts = list(self.db[self.collection_name].aggregate(pipeline))
            available_concept_names = [doc["_id"] for doc in available_concepts if doc["_id"] is not None]
            
            # Randomly shuffle concepts
            random.shuffle(available_concept_names)
            
            # Assign all concepts
            assigned_concept_refs = [{"concept_name": name} for name in available_concept_names]
            
            self.update_user_progress(evaluator_id, {
                "step2_assigned_concepts": assigned_concept_refs
            })
            
            # Get messages for each concept
            concept_messages = {}
            for concept_name in available_concept_names:
                # Try with user filter first
                messages = list(self.db[self.collection_name].find({
                    "concept_name": concept_name,
                    "user_id": {"$ne": evaluator_id}
                }))
                
                if len(messages) > 0:
                    concept_messages[concept_name] = messages
                else:
                    # If no messages found with user filter, try without filter
                    messages = list(self.db[self.collection_name].find({
                        "concept_name": concept_name
                    }))
                    if len(messages) > 0:
                        concept_messages[concept_name] = messages
            
            return concept_messages
        except Exception as e:
            return {}
    
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
            
            self.update_user_progress(evaluator_id, {
                "step2_completed_concepts": completed_concepts,
                "step2_current_index": current_index
            })
            
            return True
            
        except Exception as e:
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
        
        metrics = {
            "step1": {
                "total": step1_total,
                "completed": step1_completed,
                "percentage": min(100, int(step1_percentage))
            },
            "step2": {
                "total": step2_total,
                "completed": step2_completed,
                "percentage": min(100, int(step2_percentage))
            }
        }
        
        # Check if steps are complete
        metrics["step1"]["is_complete"] = step1_completed >= step1_total and step1_total > 0
        metrics["step2"]["is_complete"] = step2_completed >= step2_total and step2_total > 0
        
        return metrics
    
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
        except Exception as e:
            return None
    
    def get_current_step2_concept(self, evaluator_id):
        """
        Get the current concept for step 2 evaluation.
        
        Args:
            evaluator_id: ID of the evaluator
            
        Returns:
            Current concept name and messages or None if all concepts have been evaluated
        """
        # Get user progress
        progress = self.get_or_initialize_user_progress(evaluator_id)
        
        # If no assigned concepts or all completed, return None
        if len(progress["step2_assigned_concepts"]) == 0 or \
           len(progress["step2_completed_concepts"]) >= len(progress["step2_assigned_concepts"]):
            return None, []
        
        # Get current index
        current_index = progress["step2_current_index"]
        
        # Get current concept
        if current_index >= len(progress["step2_assigned_concepts"]):
            return None, []
            
        concept_name = progress["step2_assigned_concepts"][current_index]["concept_name"]
        
        # Get messages for this concept
        try:
            # First try with user ID filter
            messages = list(self.db[self.collection_name].find({
                "concept_name": concept_name,
                "user_id": {"$ne": evaluator_id}
            }))
            
            # If no messages found, try without the user ID filter
            if len(messages) == 0:
                messages = list(self.db[self.collection_name].find({
                    "concept_name": concept_name
                }))
            
            if len(messages) == 0:
                # Move to next concept
                self.update_user_progress(evaluator_id, {"step2_current_index": current_index + 1})
                return self.get_current_step2_concept(evaluator_id)
            
            return concept_name, messages
        except Exception as e:
            return None, []