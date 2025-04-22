"""
MongoDB service module.
Handles interactions with MongoDB for storing and retrieving messages.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import pymongo
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class MongoDBService:
    """Service for storing and retrieving messages from MongoDB."""
    
    def __init__(self, uri: str, db_name: str):
        """
        Initialize the MongoDB service.
        
        Args:
            uri: MongoDB connection URI
            db_name: Name of the database
        """
        try:
            # Log connection details (be careful with sensitive info)
            logger.info(f"Attempting to connect to MongoDB with database: {db_name}")
            
            # Redact sensitive parts of URI for logging
            safe_uri = uri
            if "@" in uri:
                # This preserves the server/host part but redacts credentials
                safe_uri = uri.split("@")[1]
            logger.info(f"Connecting to MongoDB host: {safe_uri}")
            
            # Attempt connection
            self.client = MongoClient(uri)
            
            # Validate connection by requesting server info (will raise exception if not connected)
            server_info = self.client.server_info()
            logger.info(f"Successfully connected to MongoDB version: {server_info.get('version', 'unknown')}")
            
            self.db = self.client[db_name]
            
            # List available collections to verify database structure
            collections = self.db.list_collection_names()
            logger.info(f"Available collections in {db_name}: {collections}")
            
            logger.info(f"MongoDB service fully initialized with database: {db_name}")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB service: {e}", exc_info=True)
            self.client = None
            self.db = None
    
    def save_message(self, 
                message: str, 
                concept_name: str, 
                user_id: str,
                context: str = "",
                focus: str = "",
                tone: str = "",
                style: str = "",
                message_length: int = 0,
                iterations: int = 0,
                diversity_metrics: dict = None) -> Optional[str]:
        """
        Save a message to MongoDB with diversity metrics.
        
        Args:
            message: The message text
            concept_name: The concept name (also used as collection name)
            user_id: ID of the user who created the message
            context: Task context
            focus: Message focus
            tone: Message tone
            style: Message style
            message_length: Number of sentences
            iterations: Number of iterations to create the message
            diversity_metrics: Metrics about message's diversity compared to previous messages
            
        Returns:
            ID of the saved message or None if saving failed
        """
        if self.db is None:
            logger.error("MongoDB service not properly initialized")
            return None
        
        try:
            # Use concept_name as the collection name
            collection = self.db[concept_name]
            
            # Create indexes for efficient queries if they don't exist
            collection.create_index([("user_id", pymongo.ASCENDING)])
            collection.create_index([("timestamp", pymongo.DESCENDING)])
            
            # Create document
            doc = {
                "message": message,
                "concept_name": concept_name,
                "user_id": user_id,
                "context": context,
                "focus": focus,
                "tone": tone,
                "style": style,
                "message_length": message_length,
                "iterations": iterations,
                "timestamp": datetime.now()
            }
            
            # Add diversity metrics if provided
            if diversity_metrics:
                doc["diversity_metrics"] = diversity_metrics
            
            # Insert document
            result = collection.insert_one(doc)
            logger.info(f"Message saved to MongoDB collection {concept_name} with ID: {result.inserted_id}")
            
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error saving message to MongoDB: {e}")
            return None
    
    def get_messages_by_concept(self, concept_name: str) -> List[str]:
        """
        Get all messages for a specific concept.
        
        Args:
            concept_name: Name of the concept (also the collection name)
            
        Returns:
            List of message texts
        """
        if self.db is None:
            logger.error("MongoDB service not properly initialized")
            return []
        
        try:
            # Use concept_name as the collection name
            if concept_name not in self.db.list_collection_names():
                logger.info(f"Collection {concept_name} does not exist yet")
                return []
                
            collection = self.db[concept_name]
            
            # Query for all messages in this concept collection
            cursor = collection.find()
            
            # Extract message texts
            messages = [doc["message"] for doc in cursor]
            
            logger.info(f"Retrieved {len(messages)} messages for concept: {concept_name}")
            
            return messages
        except Exception as e:
            logger.error(f"Error retrieving messages from MongoDB: {e}")
            return []
    
    def get_all_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages with metadata from all collections.
        
        Returns:
            List of message documents
        """
        if self.db is None:
            logger.error("MongoDB service not properly initialized")
            return []
        
        try:
            # Get all collection names (concepts)
            collection_names = self.db.list_collection_names()
            
            all_messages = []
            for collection_name in collection_names:
                collection = self.db[collection_name]
                
                # Query for all messages in this collection, sorted by timestamp
                cursor = collection.find().sort("timestamp", pymongo.DESCENDING)
                
                # Convert to list and handle ObjectId serialization
                for doc in cursor:
                    doc["_id"] = str(doc["_id"])
                    doc["timestamp"] = doc["timestamp"].isoformat()
                    doc["collection"] = collection_name  # Add collection name for reference
                    all_messages.append(doc)
            
            logger.info(f"Retrieved {len(all_messages)} messages from all collections")
            
            return all_messages
        except Exception as e:
            logger.error(f"Error retrieving all messages from MongoDB: {e}")
            return []
    
    def delete_messages_by_concept(self, concept_name: str) -> int:
        """
        Delete all messages for a specific concept.
        
        Args:
            concept_name: Name of the concept (also the collection name)
            
        Returns:
            Number of deleted messages
        """
        if self.db is None:
            logger.error("MongoDB service not properly initialized")
            return 0
        
        try:
            if concept_name not in self.db.list_collection_names():
                logger.info(f"Collection {concept_name} does not exist")
                return 0
                
            collection = self.db[concept_name]
            count = collection.count_documents({})
            collection.drop()
            
            logger.info(f"Deleted collection {concept_name} with {count} messages")
            
            return count
        except Exception as e:
            logger.error(f"Error deleting messages for concept {concept_name}: {e}")
            return 0
    
    def delete_all_messages(self) -> int:
        """
        Delete all messages from all collections in the database.
        
        Returns:
            Number of deleted collections
        """
        if self.db is None:
            logger.error("MongoDB service not properly initialized")
            return 0
        
        try:
            # Get all collection names
            collection_names = self.db.list_collection_names()
            count = len(collection_names)
            
            # Drop each collection
            for collection_name in collection_names:
                self.db[collection_name].drop()
            
            logger.info(f"Deleted {count} collections from MongoDB")
            
            return count
        except Exception as e:
            logger.error(f"Error deleting all collections from MongoDB: {e}")
            return 0