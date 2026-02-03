"""
Script to extract the latest message from each user for each concept and
store them in a single collection for easy access during evaluation.

This preprocessing step improves the performance of the evaluation app
by avoiding repeated calculations when users access the app.
"""

import pymongo
from datetime import datetime
import argparse
import sys
import os
import importlib.util
import random

def load_concept_definitions_from_concepts_py():
    """
    Load concept definitions from concepts.py file.
    
    Returns:
        Dictionary mapping concept names to definitions
    """
    # Try to find concepts.py in various paths
    possible_paths = [
        os.path.join("data", "concepts.py"),          # data/concepts.py
        os.path.join("..", "data", "concepts.py"),    # ../data/concepts.py
        "concepts.py",                                # concepts.py in current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location("concepts", path)
                concepts_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(concepts_module)
                
                # Extract concept definitions from ALL_CONCEPTS
                if hasattr(concepts_module, 'ALL_conceptS'):
                    concept_definitions = {}
                    for concept, info in concepts_module.ALL_conceptS.items():
                        concept_definitions[concept] = info.get('description', f"Definition for {concept} not available")
                    
                    return concept_definitions
                else:
                    return {}
            except Exception:
                pass
    
    # Fallback definitions if concepts.py can't be loaded
    return {}

def extract_latest_messages(source_uri, source_db_name, target_db_name, target_collection="all_messages", dry_run=False):
    """
    Extract the latest message from each user for each concept in the source DB
    and store them in a target DB under a specified collection.
    
    Args:
        source_uri: MongoDB connection URI for the source database
        source_db_name: Name of the source database
        target_db_name: Name of the target database
        target_collection: Name of the collection in the target database
        dry_run: If True, don't write to the database, just log what would be done
    
    Returns:
        Number of messages extracted and (optionally) inserted
    """
    try:
        # Load concept definitions
        concept_definitions = load_concept_definitions_from_concepts_py()
        
        # Connect to MongoDB
        client = pymongo.MongoClient(source_uri)
        source_db = client[source_db_name]
        target_db = client[target_db_name]
        
        # Get all collections (concepts) in source DB
        source_collections = source_db.list_collection_names()
        concept_collections = [c for c in source_collections if not c.startswith("eval_") and c != target_collection]
        
        # Prepare target collection
        if not dry_run:
            if target_collection in target_db.list_collection_names():
                target_db[target_collection].drop()
            target_db.create_collection(target_collection)
            target_db[target_collection].create_index([("user_id", pymongo.ASCENDING)])
            target_db[target_collection].create_index([("concept_name", pymongo.ASCENDING)])
        
        # Store latest messages
        latest_messages = []
        
        for concept in concept_collections:
            messages = list(source_db[concept].find())
            users_latest = {}
            
            for message in messages:
                user_id = message.get("user_id")
                timestamp = message.get("timestamp")
                
                if not user_id or not timestamp:
                    continue
                
                if user_id not in users_latest or users_latest[user_id].get("timestamp", datetime.min) < timestamp:
                    users_latest[user_id] = message
            
            for user_id, message in users_latest.items():
                concept_definition = concept_definitions.get(concept, f"Definition for {concept} not available")
                
                simplified_message = {
                    "original_id": str(message["_id"]),
                    "message": message["message"],
                    "concept_name": concept,
                    "concept_definition": concept_definition,
                    "user_id": user_id,
                    "timestamp": message["timestamp"]
                }
                
                latest_messages.append(simplified_message)
        
        if not dry_run and latest_messages:
            result = target_db[target_collection].insert_many(latest_messages)
            return len(result.inserted_ids)
        
        return len(latest_messages)
    
    except Exception as e:
        print(f"Error extracting messages: {e}")
        return 0
    
    finally:
        if 'client' in locals():
            client.close()

def initialize_evaluation_collections(mongo_uri, db_name, message_limit=None, dry_run=False):
    """
    Initialize evaluation collections with pre-populated user progress
    
    Args:
        mongo_uri: MongoDB connection URI
        db_name: Name of the database
        message_limit: Maximum number of messages to assign per user (None = all messages)
        dry_run: If True, don't write to the database, just log what would be done
        
    Returns:
        Dictionary with stats about the initialization
    """
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)
        db = client[db_name]
        
        # Create evaluation collections if they don't exist
        eval_collection_prefix = "eval_"
        progress_collection = f"{eval_collection_prefix}user_progress"
        step1_collection = f"{eval_collection_prefix}step1_evaluations"
        step2_collection = f"{eval_collection_prefix}step2_evaluations"
        
        if not dry_run:
            collections = db.list_collection_names()
            
            # Create or reset collections as needed
            for collection_name in [progress_collection, step1_collection, step2_collection]:
                if collection_name in collections:
                    db[collection_name].drop()
                db.create_collection(collection_name)
            
            # Create indexes
            db[progress_collection].create_index("evaluator_id")
            db[step1_collection].create_index([("evaluator_id", pymongo.ASCENDING)])
            db[step1_collection].create_index([("message_id", pymongo.ASCENDING)])
            db[step2_collection].create_index([("evaluator_id", pymongo.ASCENDING)])
            db[step2_collection].create_index([("concept_name", pymongo.ASCENDING)])
        
        # Get all users and concept data
        all_users = db.all_messages.distinct("user_id")
        all_concepts = db.all_messages.distinct("concept_name")
        
        # Print stats
        print(f"Found {len(all_users)} users and {len(all_concepts)} concepts")
        
        # Initialize progress documents for each user
        progress_docs = []
        
        for user_id in all_users:
            if not user_id:  # Skip empty user IDs
                continue
                
            # Get all messages not created by this user
            messages = list(db.all_messages.find({"user_id": {"$ne": user_id}}))
            
            # If no messages are found with user_id filter, use all messages
            if not messages:
                messages = list(db.all_messages.find())
            
            # Shuffle messages randomly
            random.shuffle(messages)
            
            # Apply message limit if specified
            if message_limit is not None and message_limit > 0:
                messages = messages[:min(message_limit, len(messages))]
            
            # Create assigned message references
            assigned_message_refs = [
                {
                    "message_id": str(msg["_id"]), 
                    "concept_name": msg["concept_name"],
                    "message_text": msg["message"]
                } 
                for msg in messages
            ]
            
            # Create assigned concept references
            assigned_concept_refs = [{"concept_name": concept} for concept in all_concepts]
            
            # Create progress document
            progress_doc = {
                "evaluator_id": user_id,
                "step1_assigned_messages": assigned_message_refs,
                "step1_completed_messages": [],
                "step1_current_index": 0,
                "step2_assigned_concepts": assigned_concept_refs,
                "step2_completed_concepts": [],
                "step2_current_index": 0,
                "step1_is_complete": False,
                "step2_is_complete": False,
                "last_updated": datetime.now()
            }
            
            progress_docs.append(progress_doc)
        
        # Insert progress documents
        if not dry_run and progress_docs:
            db[progress_collection].insert_many(progress_docs)
            
        return {
            "users_initialized": len(progress_docs),
            "concepts_per_user": len(all_concepts),
            "messages_per_user": len(assigned_message_refs) if "assigned_message_refs" in locals() else 0
        }
        
    except Exception as e:
        print(f"Error initializing evaluation collections: {e}")
        return {"error": str(e)}
    
    finally:
        if 'client' in locals():
            client.close()

def main():
    parser = argparse.ArgumentParser(description='Extract latest messages and initialize evaluation collections')
    parser.add_argument('--uri', required=True, help='MongoDB connection URI')
    parser.add_argument('--source_db', default="collection_of_concept_based_messages", help='Source database name')
    parser.add_argument('--target_db', default="evaluation_results", help='Target database name')
    parser.add_argument('--collection', default='all_messages', help='Target collection name')
    parser.add_argument('--dry-run', action='store_true', help='Run without making changes to the database')
    parser.add_argument('--message-limit', type=int, default=None, help='Maximum number of messages to assign per user (default: all messages)')
    parser.add_argument('--skip-extraction', action='store_true', help='Skip message extraction step')
    parser.add_argument('--skip-initialization', action='store_true', help='Skip evaluation initialization step')
    
    args = parser.parse_args()
    
    print(f"Starting with URI ending with: {args.uri.split('@')[-1]}")
    print(f"Target DB: {args.target_db}, Target Collection: {args.collection}")
    
    if not args.skip_extraction:
        print("\n== Step 1: Extracting Messages ==")
        count = extract_latest_messages(
            args.uri, 
            args.source_db,
            args.target_db,
            args.collection,
            args.dry_run
        )
        
        if args.dry_run:
            print(f"DRY RUN: Would have extracted {count} messages")
        else:
            print(f"Successfully extracted {count} messages")
    else:
        print("\n== Skipping Message Extraction ==")
    
    if not args.skip_initialization:
        # Get user input for message limit if not provided
        message_limit = args.message_limit
        if message_limit is None and not args.dry_run:
            show_all = input("\nDo you want to show every user all messages created by other users? (y/n): ").lower() == 'y'
            if not show_all:
                message_limit = int(input("How many messages do you want to assign to each user? "))
        
        print("\n== Step 2: Initializing Evaluation Collections ==")
        stats = initialize_evaluation_collections(
            args.uri,
            args.target_db,
            message_limit,
            args.dry_run
        )
        
        if args.dry_run:
            print(f"DRY RUN: Would have initialized user progress for {stats.get('users_initialized', 0)} users")
            print(f"Each user would be assigned {stats.get('messages_per_user', 0)} messages across {stats.get('concepts_per_user', 0)} concepts")
        else:
            print(f"Successfully initialized user progress for {stats.get('users_initialized', 0)} users")
            print(f"Each user is assigned {stats.get('messages_per_user', 0)} messages across {stats.get('concepts_per_user', 0)} concepts")
    else:
        print("\n== Skipping Evaluation Initialization ==")

if __name__ == "__main__":
    main()