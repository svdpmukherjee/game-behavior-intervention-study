"""
Script to initialize evaluation collections with pre-populated user progress.

This script sets up the necessary MongoDB collections for the evaluation app,
initializing user progress data based on messages in the 'all_messages' collection.
"""

import pymongo
from datetime import datetime
import argparse
import random

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
    parser = argparse.ArgumentParser(description='Initialize evaluation collections for the evaluation app')
    parser.add_argument('--uri', required=True, help='MongoDB connection URI')
    parser.add_argument('--db', default="evaluation_results", help='Database name')
    parser.add_argument('--dry-run', action='store_true', help='Run without making changes to the database')
    parser.add_argument('--message-limit', type=int, default=None, help='Maximum number of messages to assign per user (default: all messages)')
    
    args = parser.parse_args()
    
    print(f"Starting with URI ending with: {args.uri.split('@')[-1]}")
    print(f"Target DB: {args.db}")
    
    # Get user input for message limit if not provided
    message_limit = args.message_limit
    if message_limit is None and not args.dry_run:
        show_all = input("\nDo you want to show every user all messages created by other users? (y/n): ").lower() == 'y'
        if not show_all:
            message_limit = int(input("How many messages do you want to assign to each user? "))
    
    print("\n== Initializing Evaluation Collections ==")
    stats = initialize_evaluation_collections(
        args.uri,
        args.db,
        message_limit,
        args.dry_run
    )
    
    if args.dry_run:
        print(f"DRY RUN: Would have initialized user progress for {stats.get('users_initialized', 0)} users")
        print(f"Each user would be assigned {stats.get('messages_per_user', 0)} messages across {stats.get('concepts_per_user', 0)} concepts")
    else:
        print(f"Successfully initialized user progress for {stats.get('users_initialized', 0)} users")
        print(f"Each user is assigned {stats.get('messages_per_user', 0)} messages across {stats.get('concepts_per_user', 0)} concepts")

if __name__ == "__main__":
    main()