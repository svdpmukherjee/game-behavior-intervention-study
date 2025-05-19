from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from typing import List, Dict, Any
import os

# Import configuration
from app.config.app_config import get_cors_origins, MONGODB_URI, MONGODB_DB_NAME

from app.models.schemas import (
    SessionInit, GameEvent, WordSubmission, 
    GameInit, GameResponse, MotivationalMessage, WordMeaning, WordMeaningSubmission
)

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URI)
    app.database = app.mongodb_client[MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.post("/api/initialize-session")
async def initialize_session(session_data: SessionInit):
    """Initialize a new session for a participant."""
    try:
        session_doc = {
            "prolificId": session_data.prolificId,
            "createdAt": datetime.utcnow(),
            "metadata": session_data.metadata.dict(),
            "gameState": {
                "completionStatus": {
                    "tutorial": {"completed": False},
                    "mainGame": {"completed": False},
                    "meaningCheck": {"completed": False}
                },
                "startTime": datetime.utcnow()
            }
        }

        result = await app.database.sessions.insert_one(session_doc)
        return {"sessionId": str(result.inserted_id)}
    except Exception as e:
        print(f"Session initialization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tutorial/init")
async def initialize_tutorial(sessionId: str):
    """Initialize tutorial game."""
    try:
        config = await app.database.game_config.find_one({})
        if not config:
            raise HTTPException(status_code=404, detail="Game configuration not found")
            
        tutorial_config = config.get("game_config", {}).get("tutorial_anagrams", {})
        if not tutorial_config:
            print("Tutorial config not found in:", config)
            raise HTTPException(status_code=500, detail="Tutorial configuration not found")
            
        time_settings = config.get("time_settings", {})
        if not time_settings:
            raise HTTPException(status_code=500, detail="Time settings not found")
            
        return {
            "word": tutorial_config.get("word"),
            "solutions": tutorial_config.get("solutions"),
            "timeLimit": time_settings.get("tutorial_time")
        }
    except Exception as e:
        print(f"Error initializing tutorial: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize tutorial: {str(e)}"
        )
    
@app.post("/api/tutorial/complete")
async def complete_tutorial(request: dict):
    """Mark tutorial as completed with enhanced validation."""
    try:
        session_id = request.get("sessionId")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        # Get game configuration for validation
        config = await app.database.game_config.find_one({})
        tutorial_config = config.get("game_config", {}).get("tutorial_anagrams", {})

        # Validate words and calculate rewards
        validated_words = []
        removed_words = []
        total_reward = 0

        for word in request.get("validatedWords", []):
            word_length = str(word.get("length"))
            is_valid = word.get("word").upper() in [
                s.upper() for s in tutorial_config.get("solutions", {}).get(word_length, [])
            ]
            reward = config.get("rewards", {}).get(word_length, 0) if is_valid else 0
            
            validated_words.append({
                "word": word.get("word"),
                "length": word.get("length"),
                "isValid": is_valid,
                "reward": reward,
                "validatedAt": word.get("validatedAt")
            })
            
            total_reward += reward

        # Update session
        result = await app.database.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "gameState.completionStatus.tutorial": {
                        "completed": True,
                        "completedAt": datetime.utcnow(),
                        "validatedWords": validated_words,
                        "removedWords": removed_words,
                        "totalReward": total_reward
                    }
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"status": "success", "totalReward": total_reward}
    except Exception as e:
        print(f"Error completing tutorial: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/game-events")
async def log_game_event(event: GameEvent):
    """
    Handles various event types including:
    - word_validation: Tracks word validation events
    - page_leave/page_return: Tracks when users leave or return to the page
    - mouse_inactive_start/mouse_active: Tracks mouse inactivity
    - motivational_message_shown: Tracks when motivational messages are displayed
    - meaning_submission: Handles word meaning submissions
    - self_reported_skill: Tracks user's self-reported word unscrambling skill level
    """
    try:
        event_dict = event.dict(exclude_none=True)
        event_dict["timestamp"] = datetime.utcnow()
        
        # Clean up details by removing timeSpent if present
        if "details" in event_dict and isinstance(event_dict["details"], dict):
            if "timeSpent" in event_dict["details"]:
                del event_dict["details"]["timeSpent"]
                
        if event.eventType == "motivational_message_shown":
            # Convert details to dict if it's not already
            if not isinstance(event.details, dict):
                details = event.details.dict(exclude_none=True)
            else:
                details = event.details
                
            # Clean up the details to only include relevant fields
            message_details = {
                "messageId": details.get("messageId"),
                "messageText": details.get("messageText"),
                "timeSpentOnMessage": details.get("timeSpentOnMessage"),
                "theory": details.get("theory"),
                # "variation": details.get("variation")
            }
            
            # Remove None values
            message_details = {k: v for k, v in message_details.items() if v is not None}
            
            # Update event details
            event_dict["details"] = message_details
                
        # Handling for meaning submission events
        if event.eventType == "meaning_submission":
            if not event.details or not hasattr(event.details, "providedMeaning"):
                raise HTTPException(
                    status_code=400, 
                    detail="Meaning submission requires providedMeaning"
                )
            event_dict["details"]["providedMeaning"] = event.details.providedMeaning
            
        if not hasattr(event.details, "anagramShown"):
                raise HTTPException(
                    status_code=400,
                    detail="Meaning submission requires anagramShown"
                )
        
        await app.database.game_events.insert_one(event_dict)
        return {"status": "success"}
    except Exception as e:
        print(f"Error logging game event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/word-submissions")
async def submit_words(submission: WordSubmission):
    try:
        # Get game configuration
        config = await app.database.game_config.find_one({})
        if not config:
            raise HTTPException(status_code=500, detail="Game configuration not found")
            
        game_anagrams = config.get('game_config', {}).get('game_anagrams', [])
        rewards = config.get('rewards', {})
        
        # Find current anagram index and solutions
        current_anagram = next(
            (a for a in game_anagrams if a["word"] == submission.anagramShown),
            None
        )
        
        if not current_anagram:
            raise HTTPException(status_code=400, detail="Invalid anagram")
            
        # Validate each word and calculate correct rewards
        validated_words = []
        total_reward = 0
        
        for word in submission.submittedWords:
            word_length = str(word.length)
            solutions = current_anagram["solutions"].get(word_length, [])
            is_valid = word.word.upper() in [s.upper() for s in solutions]
            
            # Calculate reward only if word is valid
            word_reward = rewards.get(word_length, 0) if is_valid else 0
            
            validated_words.append({
                "word": word.word,
                "length": word.length,
                "isValid": is_valid,
                "reward": word_reward,
                "validatedAt": word.validatedAt,
                "submittedAt": datetime.utcnow()
            })
            
            total_reward += word_reward

        # Store the submission with validated data
        update_result = await app.database.sessions.update_one(
            {"_id": ObjectId(submission.sessionId)},
            {
                "$push": {
                    "gameState.completionStatus.mainGame.anagrams": {
                        "word": submission.anagramShown,
                        "validatedWords": validated_words,
                        "totalReward": total_reward,
                        "timeSpent": submission.timeSpent,
                        "submittedAt": datetime.utcnow()
                    }
                },
                "$inc": {
                    "gameState.completionStatus.mainGame.totalReward": total_reward
                }
            }
        )

        return {"status": "success", "validatedWords": validated_words, "totalReward": total_reward}

    except Exception as e:
        print(f"Error in word submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/init")
async def initialize_game(sessionId: str):
    """Initialize main game with first anagram and motivational message."""
    try:
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID format")

        session = await app.database.sessions.find_one({"_id": ObjectId(sessionId)})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        config = await app.database.game_config.find_one({})
        if not config:
            raise HTTPException(status_code=404, detail="Game configuration not found")

        # Get game anagrams and time settings
        game_anagrams = config["game_config"]["game_anagrams"]
        time_settings = config["time_settings"]

        # Get least shown motivational message
        message = await app.database.motivational_messages.find_one_and_update(
            {
                "shown_count": {"$lt": 10},
                "_id": {"$nin": session.get('shownMessages', [])}
            },
            {"$inc": {"shown_count": 1}},
            sort=[("shown_count", 1)]
        )

        if not message:
            raise HTTPException(status_code=404, detail="No available motivational messages")

        # Get first anagram
        first_anagram = game_anagrams[0]

        # Update session
        update_result = await app.database.sessions.find_one_and_update(
            {"_id": ObjectId(sessionId)},
            {
                "$set": {
                    "currentMessage": {
                        "id": message["id"],
                        "text": message["text"],
                        "shownAt": datetime.utcnow()
                    },
                    "currentAnagramIndex": 0
                },
                # "$push": {
                #     # "shownMessages": message["_id"],
                #     # "shownAnagrams": first_anagram["word"]
                # }
            },
            return_document=True
        )

        if not update_result:
            raise HTTPException(status_code=500, detail="Failed to update session")

        return {
            "currentMessage": {
                "id": message["id"],
                "text": message["text"],
                "theory": message["theory"],
                # "variation": message["variation"]
            },
            "word": first_anagram["word"],
            "solutions": first_anagram["solutions"],
            "timeSettings": time_settings,
            "totalAnagrams": len(game_anagrams)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error initializing game: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize game: {str(e)}"
        )
        
@app.get("/api/game/next")
async def get_next_anagram(sessionId: str, currentIndex: int):
    """Get next anagram in sequence."""
    try:
        # First verify session exists
        session = await app.database.sessions.find_one({"_id": ObjectId(sessionId)})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Get game configuration
        config = await app.database.game_config.find_one({})
        if not config:
            raise HTTPException(status_code=404, detail="Game configuration not found")

        # Access game_anagrams correctly based on your config structure
        game_anagrams = config.get("game_config", {}).get("game_anagrams", [])
        if not game_anagrams:
            raise HTTPException(status_code=500, detail="Game anagrams not found in configuration")

        next_index = int(currentIndex) + 1

        if next_index >= len(game_anagrams):
            return JSONResponse(content={
                "status": "complete",
                "message": "No more anagrams available"
            })

        next_anagram = game_anagrams[next_index]
        
        # Update session with new anagram
        await app.database.sessions.update_one(
            {"_id": ObjectId(sessionId)},
            {"$set": {"currentAnagramIndex": next_index}}
        )

        return JSONResponse(content={
            "status": "success",
            "word": next_anagram["word"],
            "solutions": next_anagram["solutions"]
        })

    except Exception as e:
        print(f"Error getting next anagram: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Failed to get next anagram",
                "error": str(e)
            }
        )

@app.get("/api/study-config")
async def get_study_config():
    """Get study configuration."""
    try:
        config = await app.database.game_config.find_one({})
        if not config:
            raise HTTPException(status_code=404, detail="Configuration not found")
        
        # Format the response according to what the frontend expects
        response = {
            "timeSettings": config["time_settings"],  # Direct mapping
            "rewards": config["rewards"],
            "compensation": config["study_compensation"],
            "game_anagrams": len(config["game_config"]["game_anagrams"])
        }
        
        return JSONResponse(content=response)
    except Exception as e:
        print(f"Error fetching study config: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch study configuration: {str(e)}"
        )

@app.post("/api/meanings/submit")
async def submit_word_meanings(request: dict):
    """Submit word meanings for validation and storage."""
    try:
        session_id = request.get("sessionId")
        prolific_id = request.get("prolificId")
        word_meanings = request.get("wordMeanings", [])
        completed_at = request.get("completedAt")

        if not session_id or not prolific_id or not word_meanings:
            raise HTTPException(
                status_code=400,
                detail="Missing required fields"
            )
            
        # Ensure each word meaning has required fields
        for meaning in word_meanings:
            if not all(key in meaning for key in ["word", "providedMeaning", "anagramShown"]):
                raise HTTPException(
                    status_code=400,
                    detail="Each word meaning must include word, providedMeaning, and anagramShown"
                )

        # Update session with word meanings
        update_result = await app.database.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$set": {
                    "gameState.completionStatus.meaningCheck": {
                        "completed": True,
                        "completedAt": datetime.fromisoformat(completed_at) if completed_at else datetime.utcnow(),
                        "wordMeanings": word_meanings
                    }
                }
            }
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")

        return {"status": "success"}

    except Exception as e:
        print(f"Error submitting word meanings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit word meanings: {str(e)}"
        )

@app.get("/api/game-results")
async def get_game_results(sessionId: str, prolificId: str):
    try:
        session = await app.database.sessions.find_one({
            "_id": ObjectId(sessionId),
            "prolificId": prolificId
        })

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        config = await app.database.game_config.find_one({})
        if not config:
            raise HTTPException(status_code=404, detail="Game configuration not found")

        # Get game events for validation and removal tracking
        validation_events = await app.database.game_events.find({
            "sessionId": sessionId,
            "prolificId": prolificId,
            "eventType": "word_validation"
        }).to_list(None)

        removal_events = await app.database.game_events.find({
            "sessionId": sessionId,
            "prolificId": prolificId,
            "eventType": "word_removal"
        }).to_list(None)

        removed_words = {
            event.get("details", {}).get("word", "").upper()
            for event in removal_events
        }

        valid_words = []
        invalid_words = []
        total_reward = 0
        seen_words = set()
        anagram_details = []

        main_game = session.get("gameState", {}).get("completionStatus", {}).get("mainGame", {})
        anagrams = main_game.get("anagrams", [])

        for anagram_entry in anagrams:
            current_anagram = anagram_entry.get("word")
            current_words = []
            
            solutions = next(
                (a["solutions"] for a in config["game_config"]["game_anagrams"] 
                 if a["word"] == current_anagram),
                {}
            )

            for word_entry in anagram_entry.get("validatedWords", []):
                word = word_entry.get("word", "").upper()
                if word in removed_words or word in seen_words:
                    continue

                seen_words.add(word)
                length = str(word_entry.get("length"))
                is_valid = word in [s.upper() for s in solutions.get(length, [])]
                word_data = {
                    "word": word,
                    "length": word_entry.get("length"),
                    "anagramShown": current_anagram
                }

                if is_valid:
                    reward = config["rewards"].get(length, 0)
                    word_data["reward"] = reward
                    valid_words.append(word_data)
                    current_words.append(word_data)
                    total_reward += reward
                else:
                    invalid_words.append(word_data)
                    current_words.append(word_data)

            anagram_details.append({
                "anagram": current_anagram,
                "words": current_words
            })

        return {
            "validWords": valid_words,
            "invalidWords": invalid_words,
            "totalReward": total_reward,
            "anagramsAttempted": len(anagrams),
            "anagramDetails": anagram_details
        }

    except Exception as e:
        print(f"Error fetching game results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        await app.database.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }