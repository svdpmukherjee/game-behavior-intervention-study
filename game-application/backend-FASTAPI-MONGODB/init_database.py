from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

if not MONGODB_URI or not MONGODB_DB_NAME:
    raise ValueError("MongoDB environment variables not set!")

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

def load_config():
    """Load configuration from JSON file"""
    try:
        config_path = 'app/config/db_config.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def verify_config():
    """Verify database configuration structure"""
    config = db.game_config.find_one({})
    if not config:
        print("❌ No configuration found in database")
        return False
        
    required_fields = [
        "tutorial_anagrams",
        "game_anagrams",
        "rewards",
        "time_settings",
        "study_compensation", 
    ]
    
    for field in required_fields:
        if field not in config:
            print(f"❌ Missing required field: {field}")
            return False
    
    print("✓ Configuration structure verified")
    return True

def verify_game_config():
    """Verify game configuration is properly initialized."""
    try:
        config = db.game_config.find_one({})
        if not config:
            print("❌ Game configuration not found in database")
            return False

        # Check required fields
        required_fields = ["game_anagrams", "tutorial_anagrams", "time_settings", "rewards"]
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field: {field}")
                return False

        # Verify game anagrams structure
        game_anagrams = config["game_anagrams"]
        if not isinstance(game_anagrams, list) or not game_anagrams:
            print("❌ Invalid or empty game_anagrams configuration")
            return False

        # Verify anagram structure
        for idx, anagram in enumerate(game_anagrams):
            if not all(key in anagram for key in ["word", "solutions"]):
                print(f"❌ Invalid anagram structure at index {idx}")
                return False

        # Check motivational messages
        message_count = db.motivational_messages.count_documents({})
        if message_count == 0:
            print("❌ No motivational messages found")
            return False

        print("✓ Game configuration verified successfully")
        return True

    except Exception as e:
        print(f"❌ Error verifying game configuration: {e}")
        return False

def reset_database():
    """Delete all collections in the database - UPDATED: Removed game_areas collection"""
    try:
        collections = [
            'game_config',
            'motivational_messages',
            'sessions',  # Now contains gameArea data
            'game_events',
            'user_interactions',
            # REMOVED: 'game_areas' - no longer needed
        ]

        for collection in collections:
            result = db[collection].delete_many({})
            print(f"Cleared collection: {collection} ({result.deleted_count} documents)")

        print("✅ All collections have been reset successfully")
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        raise
    
def create_optimized_indexes():
    """Create optimized indexes for the integrated structure - UPDATED"""
    try:
        print("\n Dropping existing indexes...")
        
        # Drop indexes from existing collections
        try:
            db.user_interactions.drop_indexes()
            print("✓ Dropped user_interactions indexes")
        except Exception as e:
            print(f"ℹ️ user_interactions indexes: {e}")
            
        try:
            db.sessions.drop_indexes()
            print("✓ Dropped sessions indexes")
        except Exception as e:
            print(f"ℹ️ sessions indexes: {e}")
            
        try:
            db.game_events.drop_indexes()
            print("✓ Dropped game_events indexes")
        except Exception as e:
            print(f"ℹ️ game_events indexes: {e}")

        print("\n Creating optimized indexes...")

        # User interactions collection - Updated indexes without batchId and batchIndex
        print("Creating user_interactions indexes...")
        db.user_interactions.create_index([
            ("sessionId", 1),
            ("timestamp", 1)
        ], name="sessionId_timestamp")
        
        db.user_interactions.create_index([
            ("prolificId", 1),
            ("phase", 1)
        ], name="prolificId_phase")
        
        db.user_interactions.create_index([
            ("sessionId", 1),
            ("interactionType", 1),
            ("timestamp", 1)
        ], name="sessionId_interactionType_timestamp")
        
        db.user_interactions.create_index([
            ("interactionType", 1)
        ], name="interactionType")
        
        # Removed batchId index since we're no longer using it
        
        print("✓ user_interactions indexes created")
        
        # Sessions collection - UPDATED with gameArea indexes
        print("Creating sessions indexes...")
        db.sessions.create_index("prolificId", unique=True, name="prolificId_unique")
        
        # NEW: Index for game area queries
        db.sessions.create_index("gameArea.calculatedAt", name="gameArea_calculatedAt")
        db.sessions.create_index("gameArea.bounds", name="gameArea_bounds")
        
        # Existing session indexes
        db.sessions.create_index("createdAt", name="createdAt")
        db.sessions.create_index([
            ("gameState.completionStatus.mainGame.completed", 1)
        ], name="mainGame_completed")
        
        print("✓ sessions indexes created")
        
        # Game events collection
        print("Creating game_events indexes...")
        db.game_events.create_index([
            ("sessionId", 1),
            ("timestamp", 1)
        ], name="sessionId_timestamp")
        
        db.game_events.create_index([
            ("prolificId", 1),
            ("eventType", 1)
        ], name="prolificId_eventType")
        
        db.game_events.create_index("eventType", name="eventType")
        
        print("✓ game_events indexes created")
        
        # Game config and motivational messages
        print("Creating config indexes...")
        db.game_config.create_index("game_config.game_anagrams.word", name="anagram_word")
        db.motivational_messages.create_index("shown_count", name="shown_count")
        db.motivational_messages.create_index("id", unique=True, name="message_id_unique")
        
        print("✓ config indexes created")
        
        print("\n✅ All indexes created successfully")
        
        # Print index summary
        print("\n Index Summary:")
        for collection_name in ['sessions', 'user_interactions', 'game_events', 'game_config', 'motivational_messages']:
            try:
                indexes = list(db[collection_name].list_indexes())
                print(f"  {collection_name}: {len(indexes)} indexes")
                for idx in indexes:
                    if idx['name'] != '_id_':
                        print(f"    - {idx['name']}")
            except Exception as e:
                print(f"  {collection_name}: Error listing indexes - {e}")
        
    except Exception as e:
        print(f"❌ Error creating indexes: {e}")
        raise
    
def verify_session_structure():
    """Verify that sessions can store gameArea data properly"""
    try:
        # Test session document structure
        test_session = {
            "prolificId": "test_structure_check",
            "createdAt": "2025-01-01T00:00:00Z",
            "metadata": {
                "browser": "Test Browser",
                "platform": "Test Platform",
                "screenSize": {"width": 1920, "height": 1080}
            },
            "gameArea": {
                "bounds": {
                    "left": 100.0,
                    "top": 200.0,
                    "width": 800.0,
                    "height": 400.0
                },
                "screenSize": {"width": 1920, "height": 1080},
                "userAgent": "Test User Agent",
                "calculatedAt": "2025-01-01T00:05:00Z"
            },
            "gameState": {
                "completionStatus": {
                    "tutorial": {"completed": False},
                    "mainGame": {"completed": False}
                }
            }
        }
        
        # Insert test document
        result = db.sessions.insert_one(test_session)
        
        # Verify retrieval
        retrieved = db.sessions.find_one({"_id": result.inserted_id})
        
        # Check structure
        assert "gameArea" in retrieved
        assert "bounds" in retrieved["gameArea"]
        assert "screenSize" in retrieved["gameArea"]
        
        # Clean up test document
        db.sessions.delete_one({"_id": result.inserted_id})
        
        print("✅ Session structure verification passed")
        return True
        
    except Exception as e:
        print(f"❌ Session structure verification failed: {e}")
        return False

def initialize_database():
    """Initialize database with unified configuration - UPDATED"""
    try:
        config = load_config()
        if not config:
            return

        confirmation = input("This will reset ALL collections and reinitialize the database. Are you sure? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Database initialization cancelled.")
            return

        print("\n Resetting all collections...")
        reset_database()

        print("\n Initializing collections with fresh data...")

        # Initialize motivational_messages
        messages_result = db.motivational_messages.insert_many(config['motivational_messages'])
        print(f"✅ Motivational messages initialized ({len(messages_result.inserted_ids)} documents)")

        # Initialize game configuration
        game_config_doc = {
            "game_config": {
                "game_anagrams": config['game_config']['game_anagrams'],
                "tutorial_anagrams": config['game_config']['tutorial_anagrams']
            },
            "time_settings": config['game_config']['time_settings'],
            "rewards": config['game_config']['rewards'],
            "study_compensation": config['game_config']['study_compensation']
        }
        
        config_result = db.game_config.insert_one(game_config_doc)
        print("✅ Game configuration initialized")

        # Verify the configuration
        config_check = db.game_config.find_one({})
        if not config_check:
            print("⚠️ Warning: Failed to retrieve game configuration after insertion")
            return False
            
        if 'game_config' not in config_check or 'game_anagrams' not in config_check['game_config']:
            print("⚠️ Warning: Inserted configuration is missing required fields")
            print("Actual configuration structure:", config_check)
            return False

        print("✅ Configuration verification passed")

        # Verify session structure can handle gameArea
        print("\nVerifying session structure...")
        if not verify_session_structure():
            return False

        # Create indices
        print("\n Creating database indexes...")
        create_optimized_indexes()

        print("\n Database initialization completed successfully!")
        
        # Print summary
        print("\n Database Summary:")
        for collection_name in ['game_config', 'motivational_messages', 'sessions', 'game_events', 'user_interactions']:
            try:
                count = db[collection_name].count_documents({})
                print(f"  {collection_name}: {count} documents")
            except Exception as e:
                print(f"  {collection_name}: Error counting - {e}")

    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        raise

# Migration function removed - not needed for fresh databases

if __name__ == "__main__":
    print("=== Database Initialization Tool ===")
    print("1. Initialize database (full reset)")
    print("2. Create indexes only")
    print("3. Verify configuration")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        initialize_database()
    elif choice == "2":
        create_optimized_indexes()
    elif choice == "3":
        verify_game_config()
    else:
        print("Invalid choice. Exiting.")