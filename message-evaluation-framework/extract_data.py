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

def main():
    parser = argparse.ArgumentParser(description='Extract latest messages from source database to target database')
    parser.add_argument('--uri', required=True, help='MongoDB connection URI')
    parser.add_argument('--source_db', default="collection_of_concept_based_messages", help='Source database name')
    parser.add_argument('--target_db', default="evaluation_results", help='Target database name')
    parser.add_argument('--collection', default='all_messages', help='Target collection name')
    parser.add_argument('--dry-run', action='store_true', help='Run without making changes to the database')
    
    args = parser.parse_args()
    
    print(f"Starting with URI ending with: {args.uri.split('@')[-1]}")
    print(f"Source DB: {args.source_db}")
    print(f"Target DB: {args.target_db}, Target Collection: {args.collection}")
    
    print("\n== Extracting Messages ==")
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

if __name__ == "__main__":
    main()