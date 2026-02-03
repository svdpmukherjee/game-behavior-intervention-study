"""
Simple MongoDB connection test script.
Run this standalone to verify your MongoDB connection.
"""

import sys
from pymongo import MongoClient

def test_mongodb_connection(uri, db_name, collection_name="messages"):
    """Test connection to MongoDB and verify database/collection access."""
    try:
        print(f"Attempting to connect to MongoDB...")
        print(f"Database name: {db_name}")
        print(f"Collection name: {collection_name}")
        
        # Connect to MongoDB
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Force a connection to verify it works
        client.admin.command('ping')
        print("Connected successfully to MongoDB server!")
        
        # Get database
        db = client[db_name]
        print(f"Accessed database: {db_name}")
        
        # Get list of collections
        collections = db.list_collection_names()
        print(f"Collections in database: {collections}")
        
        # Check if our collection exists
        if collection_name in collections:
            print(f"Collection '{collection_name}' exists!")
            # Count documents
            count = db[collection_name].count_documents({})
            print(f"Collection contains {count} documents")
        else:
            print(f"Collection '{collection_name}' does not exist yet. It will be created when you insert the first document.")
            
        # Close connection
        client.close()
        print("Connection closed.")
        return True
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print(f"Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    # Get connection details from command line or use defaults
    if len(sys.argv) > 2:
        uri = sys.argv[1]
        db_name = sys.argv[2]
    else:
        # Default values
        uri = "mongodb://localhost:27017/"
        db_name = "collection_of_concept-based_messages"
    
    collection_name = "messages"
    if len(sys.argv) > 3:
        collection_name = sys.argv[3]
    
    # Test connection
    success = test_mongodb_connection(uri, db_name, collection_name)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)