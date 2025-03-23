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

        # Check anti-cheating messages
        message_count = db.anti_cheating_messages.count_documents({})
        if message_count == 0:
            print("❌ No anti-cheating messages found")
            return False

        print("✓ Game configuration verified successfully")
        return True

    except Exception as e:
        print(f"❌ Error verifying game configuration: {e}")
        return False

def reset_database():
    """Delete all collections in the database"""
    try:
        collections = [
            'game_config',
            'anti_cheating_messages',
            'sessions',
            'game_events',
        ]

        for collection in collections:
            db[collection].delete_many({})
            print(f"Cleared collection: {collection}")

        print("All collections have been reset successfully")
    except Exception as e:
        print(f"Error resetting database: {e}")
        raise

def initialize_database():
    """Initialize database with unified configuration."""
    try:
        config = load_config()
        if not config:
            return

        confirmation = input("This will reset ALL collections and reinitialize the database. Are you sure? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Database initialization cancelled.")
            return

        print("\nResetting all collections...")
        reset_database()

        print("\nInitializing collections with fresh data...")

        # Initialize anti_cheating_messages
        db.anti_cheating_messages.insert_many(config['anti_cheating_messages'])
        print("✓ Anti-cheating messages initialized")

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
        
        db.game_config.insert_one(game_config_doc)
        print("✓ Game configuration initialized")

        # Verify the configuration
        config_check = db.game_config.find_one({})
        if not config_check:
            print("⚠️ Warning: Failed to retrieve game configuration after insertion")
            return False
            
        if 'game_config' not in config_check or 'game_anagrams' not in config_check['game_config']:
            print("⚠️ Warning: Inserted configuration is missing required fields")
            print("Actual configuration structure:", config_check)
            return False

        print("✓ Configuration verification passed")
        # print("Configuration structure:", config_check)

        # Create indices
        db.sessions.create_index("prolificId", unique=True)
        print("✓ Session index created")

        print("\n✓ Database initialization completed successfully!")

    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        raise

if __name__ == "__main__":
    initialize_database()