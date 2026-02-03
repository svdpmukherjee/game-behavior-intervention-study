from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from typing import List, Dict, Any
import os
import time
import asyncio

# Import configuration
from app.config.app_config import get_cors_origins, MONGODB_URI, MONGODB_DB_NAME

from app.models.schemas import (
    SessionInit, GameEvent, WordSubmission, 
    GameInit, GameResponse, MotivationalMessage, WordMeaning, WordMeaningSubmission, 
    UserInteraction, InteractionBatch, BatchProcessingResult, InteractionSummary
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
                },
                "startTime": datetime.utcnow()
            }
        }
        
        # Add game area data if provided
        if session_data.gameArea:
            session_doc["gameArea"] = session_data.gameArea.dict()

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
    """Mark tutorial as completed and validate submitted words."""
    try:
        session_id = request.get("sessionId")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")

        # Get game configuration for validation
        config = await app.database.game_config.find_one({})
        tutorial_config = config.get("game_config", {}).get("tutorial_anagrams", {})

        # Validate words and calculate rewards
        validated_words = []
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

        # Get current session to check how many anagrams have been completed
        session = await app.database.sessions.find_one({"_id": ObjectId(submission.sessionId)})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        # Count existing anagrams + 1 (current submission)
        existing_anagrams = session.get("gameState", {}).get("completionStatus", {}).get("mainGame", {}).get("anagrams", [])
        total_completed_anagrams = len(existing_anagrams) + 1
        
        # Check if this is the final anagram
        is_game_complete = total_completed_anagrams >= len(game_anagrams)

        # Prepare the update operation
        update_operation = {
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
        
        # If game is complete, also set the completed flag and completion timestamp
        if is_game_complete:
            update_operation["$set"] = {
                "gameState.completionStatus.mainGame.completed": True,
                "gameState.completionStatus.mainGame.completedAt": datetime.utcnow()
            }

        # Store the submission with validated data
        update_result = await app.database.sessions.update_one(
            {"_id": ObjectId(submission.sessionId)},
            update_operation
        )

        return {"status": "success", "validatedWords": validated_words, "totalReward": total_reward}

    except Exception as e:
        print(f"Error in word submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/init")
async def initialize_game(sessionId: str, fetch_message: bool = True):
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

        # Get message based on fetch_message parameter
        message = None
        if fetch_message:
            # Only fetch and increment a new message if explicitly requested
            message = await app.database.motivational_messages.find_one_and_update(
                {
                    "shown_count": {"$lt": 20},
                    "_id": {"$nin": session.get('shownMessages', [])}
                },
                {"$inc": {"shown_count": 1}},
                sort=[("shown_count", 1)]
            )

            if not message:
                raise HTTPException(status_code=404, detail="No available motivational messages")
            
            # Update session with the new message
            await app.database.sessions.update_one(
                {"_id": ObjectId(sessionId)},
                {
                    "$set": {
                        "currentMessage": {
                            "id": message["id"],
                            "text": message["text"],
                            "theory": message["theory"],
                            "shownAt": datetime.utcnow()
                        },
                    },
                    "$push": {
                        "shownMessages": message["_id"]
                    }
                }
            )
        else:
            # Use existing message from session if fetch_message is False
            if session.get("currentMessage"):
                message = {
                    "id": session["currentMessage"].get("id"),
                    "text": session["currentMessage"].get("text"),
                    "theory": session["currentMessage"].get("theory", "")
                }
            
            # If no message exists (unlikely but possible), use a default or none
            if not message:
                message = {
                    "id": "default",
                    "text": "Ready to start the main game!",
                    "theory": ""
                }

        # Get first anagram
        first_anagram = game_anagrams[0]

        return {
            "currentMessage": {
                "id": message["id"],
                "text": message["text"],
                "theory": message["theory"]
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



@app.post("/api/sessions/{sessionId}/game-area")
async def update_session_game_area(sessionId: str, game_area: dict):
    """Store game area bounds in session document."""
    try:
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        result = await app.database.sessions.update_one(
            {"_id": ObjectId(sessionId)},
            {"$set": {"gameArea": game_area}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"Error updating game area: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{sessionId}/game-area")
async def get_session_game_area(sessionId: str):
    """Get game area bounds for a session."""
    try:
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        session = await app.database.sessions.find_one(
            {"_id": ObjectId(sessionId)},
            {"gameArea": 1, "metadata.screenSize": 1, "metadata.browser": 1}
        )
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "sessionId": sessionId,
            "gameArea": session.get("gameArea"),
            "metadata": session.get("metadata", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving game area: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
   

@app.post("/api/interactions/batch")
async def log_interaction_batch(
    batch: InteractionBatch, 
    background_tasks: BackgroundTasks) -> BatchProcessingResult:
    """Store batch of user interactions."""
    start_time = time.time()
    
    try:
        if not batch.interactions:
            return BatchProcessingResult(
                status="success",
                processedCount=0,
                processingTime=time.time() - start_time
            )
        
        # Validate session exists
        session = await app.database.sessions.find_one({"_id": ObjectId(batch.sessionId)})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        interaction_docs = []
        processing_errors = []
        
        # Count interaction types for debugging
        interaction_counts = {}
        
        for i, interaction in enumerate(batch.interactions):
            try:
                # Count interaction types
                interaction_type = interaction.interactionType
                interaction_counts[interaction_type] = interaction_counts.get(interaction_type, 0) + 1
                
                # Parse timestamp string to datetime
                try:
                    if isinstance(interaction.timestamp, str):
                        # Parse ISO format string to datetime
                        parsed_timestamp = datetime.fromisoformat(interaction.timestamp.replace('Z', '+00:00'))
                    else:
                        # If it's already a datetime, use it directly
                        parsed_timestamp = interaction.timestamp
                except (ValueError, TypeError) as e:
                    processing_errors.append(f"Invalid timestamp format at index {i}: {str(e)}")
                    continue
                
                doc = {
                    "sessionId": interaction.sessionId,
                    "prolificId": interaction.prolificId,
                    "phase": interaction.phase,
                    "anagramShown": interaction.anagramShown,
                    "interactionType": interaction.interactionType,
                    "timestamp": parsed_timestamp,
                    "data": interaction.data
                }
                
                # Validate interaction type and data consistency
                if interaction.interactionType == "letter_dragged":
                    required_fields = ["letter", "sourceArea", "dragDuration"]
                    if not all(field in interaction.data for field in required_fields):
                        processing_errors.append(f"Missing required fields for letter_dragged at index {i}")
                        continue
                    
                    # Log drag event for debugging
                    print(f"[BACKEND] Drag event: {interaction.data.get('letter')} from {interaction.data.get('sourceArea')} to {interaction.data.get('targetArea')}")
                        
                elif interaction.interactionType == "letter_hovered":
                    required_fields = ["letter", "sourceArea", "hoverDuration"]
                    if not all(field in interaction.data for field in required_fields):
                        processing_errors.append(f"Missing required fields for letter_hovered at index {i}")
                        continue
                        
                elif interaction.interactionType == "mouse_move":
                    required_fields = ["x", "y"]
                    if not all(field in interaction.data for field in required_fields):
                        processing_errors.append(f"Missing required fields for mouse_move at index {i}")
                        continue
                
                interaction_docs.append(doc)
                
            except Exception as e:
                processing_errors.append(f"Error processing interaction {i}: {str(e)}")
                continue
        
        # Insert valid interactions
        inserted_count = 0
        if interaction_docs:
            result = await app.database.user_interactions.insert_many(interaction_docs)
            inserted_count = len(result.inserted_ids)
        
        # Log interaction summary for debugging
        print(f"[BACKEND] Batch processed: {interaction_counts}")
        
        # Schedule background task for analytics processing
        if inserted_count > 0:
            background_tasks.add_task(
                process_interaction_analytics,
                batch.sessionId,
                batch.prolificId,
                len(interaction_docs)
            )
        
        processing_time = time.time() - start_time
        
        return BatchProcessingResult(
            status="success" if not processing_errors else "partial_success",
            processedCount=inserted_count,
            errors=processing_errors if processing_errors else None,
            processingTime=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error storing interaction batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
 
async def process_interaction_analytics(session_id: str, prolific_id: str, interaction_count: int):
    """Process interaction analytics in the background."""
    try:
        # Update session with interaction counts
        await app.database.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {
                "$inc": {
                    "interactionStats.totalInteractions": interaction_count
                },
                "$set": {
                    "interactionStats.lastProcessed": datetime.utcnow()
                }
            }
        )
        
        print(f"Processed analytics for session {session_id}: {interaction_count} interactions")
        
    except Exception as e:
        print(f"Error processing interaction analytics: {str(e)}")


@app.get("/api/sessions/{sessionId}/interaction-summary")
async def get_interaction_summary(sessionId: str) -> InteractionSummary:
    """Get summary of interactions for a session."""
    try:
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Aggregate interaction statistics
        pipeline = [
            {"$match": {"sessionId": sessionId}},
            {
                "$group": {
                    "_id": "$interactionType",
                    "count": {"$sum": 1},
                    "avgHoverDuration": {
                        "$avg": {
                            "$cond": [
                                {"$eq": ["$interactionType", "letter_hovered"]},
                                "$data.hoverDuration",
                                None
                            ]
                        }
                    }
                }
            }
        ]
        
        results = await app.database.user_interactions.aggregate(pipeline).to_list(None)
        
        # Process results
        total_interactions = sum(result["count"] for result in results)
        drag_events = next((r["count"] for r in results if r["_id"] == "letter_dragged"), 0)
        hover_events = next((r["count"] for r in results if r["_id"] == "letter_hovered"), 0)
        mouse_movements = next((r["count"] for r in results if r["_id"] == "mouse_move"), 0)
        
        avg_hover_duration = next(
            (r["avgHoverDuration"] for r in results if r["_id"] == "letter_hovered" and r["avgHoverDuration"]),
            0.0
        ) or 0.0
        
        # Count game area exits (mouse movements with isLeavingGameArea=true)
        game_area_exits = await app.database.user_interactions.count_documents({
            "sessionId": sessionId,
            "interactionType": "mouse_move",
            "data.isLeavingGameArea": True
        })
        
        return InteractionSummary(
            totalInteractions=total_interactions,
            dragEvents=drag_events,
            hoverEvents=hover_events,
            mouseMovements=mouse_movements,
            averageHoverDuration=avg_hover_duration,
            totalGameAreaExits=game_area_exits
        )
        
    except Exception as e:
        print(f"Error getting interaction summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{sessionId}/interactions")
async def get_session_interactions(
    sessionId: str,
    interaction_type: str = None,
    limit: int = 1000,
    skip: int = 0):
    """Get interaction data for a session with optional filtering."""
    try:
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Build query
        query = {"sessionId": sessionId}
        if interaction_type:
            query["interactionType"] = interaction_type
        
        # Get interactions with pagination
        interactions = await app.database.user_interactions.find(
            query,
            {"_id": 0}  # Exclude MongoDB _id field
        ).sort("timestamp", 1).skip(skip).limit(limit).to_list(None)
        
        # Get total count
        total_count = await app.database.user_interactions.count_documents(query)
        
        return {
            "sessionId": sessionId,
            "interactions": interactions,
            "totalCount": total_count,
            "returnedCount": len(interactions),
            "hasMore": skip + len(interactions) < total_count
        }
        
    except Exception as e:
        print(f"Error getting session interactions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))  
   
           
# Create database indexes for optimal performance
async def create_interaction_indexes():
    """Create indexes for the interaction collections."""
    try:
        # User interactions collection indexes
        await app.database.user_interactions.create_index([
            ("sessionId", 1),
            ("timestamp", 1)
        ], name="sessionId_timestamp")
        
        await app.database.user_interactions.create_index([
            ("prolificId", 1),
            ("phase", 1)
        ], name="prolificId_phase")
        
        await app.database.user_interactions.create_index([
            ("sessionId", 1),
            ("interactionType", 1),
            ("timestamp", 1)
        ], name="sessionId_interactionType_timestamp")
        
        await app.database.user_interactions.create_index([
            ("interactionType", 1)
        ], name="interactionType")
        
        await app.database.user_interactions.create_index([
            ("batchId", 1)
        ], name="batchId")
        
        # Session interaction stats indexes
        await app.database.sessions.create_index([
            ("interactionStats.totalInteractions", 1)
        ], name="interaction_total")
        
        print("✓ Interaction indexes created successfully")
        
    except Exception as e:
        print(f"Error creating interaction indexes: {str(e)}")

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

# Endpoints for saving game states

@app.post("/api/game-state/save")
async def save_game_state(request: dict):
    """Save current game state during gameplay."""
    try:
        # Validate required fields
        session_id = request.get("sessionId")
        prolific_id = request.get("prolificId")
        phase = request.get("phase")  # "tutorial" or "main_game"
        game_state = request.get("gameState")
        
        if not all([session_id, prolific_id, phase, game_state]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Validate ObjectId format
        if not ObjectId.is_valid(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        # Validate phase
        if phase not in ["tutorial", "main_game"]:
            raise HTTPException(status_code=400, detail="Invalid phase. Must be 'tutorial' or 'main_game'")
        
        # Prepare update data with safe defaults
        update_data = {
            f"gameState.currentGameSession.{phase}": {
                "currentWord": game_state.get("currentWord", ""),
                "solution": game_state.get("solution", []),
                "availableLetters": game_state.get("availableLetters", []),
                "validatedWords": game_state.get("validatedWords", []),
                "wordIndex": game_state.get("wordIndex", 0),
                "timeLeft": game_state.get("timeLeft", 0),
                "totalTime": game_state.get("totalTime", 0),
                "isTimeUp": game_state.get("isTimeUp", False),
                "solutions": game_state.get("solutions", {}),
                "allValidatedWords": game_state.get("allValidatedWords", []),
                "gameStartTime": game_state.get("gameStartTime"),
                "lastUpdated": datetime.utcnow(),
                "showOverview": game_state.get("showOverview", False),
                "isSubmitted": game_state.get("isSubmitted", False)
            }
        }
        
        # Update session document
        result = await app.database.sessions.update_one(
            {"_id": ObjectId(session_id), "prolificId": prolific_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            # Check if session exists but prolific ID doesn't match
            session_exists = await app.database.sessions.find_one({"_id": ObjectId(session_id)})
            if session_exists:
                raise HTTPException(status_code=403, detail="Session ID and Prolific ID don't match")
            else:
                raise HTTPException(status_code=404, detail="Session not found")
        
        return {"status": "success", "message": "Game state saved successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error saving game state: {str(e)}")
        print(f"Request data: {request}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/game-state/restore")
async def restore_game_state(sessionId: str, prolificId: str, phase: str):
    """Restore game state after page refresh."""
    try:
        # Validate inputs
        if not sessionId or not prolificId or not phase:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        if phase not in ["tutorial", "main_game"]:
            raise HTTPException(status_code=400, detail="Invalid phase. Must be 'tutorial' or 'main_game'")
        
        # Find session
        session = await app.database.sessions.find_one({
            "_id": ObjectId(sessionId),
            "prolificId": prolificId
        })
        
        if not session:
            # Check if session exists but prolific ID doesn't match
            session_exists = await app.database.sessions.find_one({"_id": ObjectId(sessionId)})
            if session_exists:
                raise HTTPException(status_code=403, detail="Session ID and Prolific ID don't match")
            else:
                raise HTTPException(status_code=404, detail="Session not found")
        
        # Get saved game state for the specific phase
        game_state_path = session.get("gameState", {}).get("currentGameSession", {})
        saved_state = game_state_path.get(phase) if game_state_path else None
        
        if not saved_state:
            # No saved state found - return initial state indicator
            return {"hasState": False, "message": "No saved game state found"}
        
        # Check if the saved state is recent (within last 3 hours to prevent stale state)
        last_updated = saved_state.get("lastUpdated")
        if last_updated:
            try:
                if isinstance(last_updated, str):
                    last_updated = datetime.fromisoformat(last_updated)
                time_diff = datetime.utcnow() - last_updated
                if time_diff.total_seconds() > 10800:  # 3 hours
                    return {"hasState": False, "message": "Saved state is too old"}
            except Exception as e:
                print(f"Error parsing lastUpdated timestamp: {e}")
                # Continue anyway, don't fail on timestamp issues
        
        # Calculate actual remaining time based on when game started and current time
        game_start_time = saved_state.get("gameStartTime")
        total_time = saved_state.get("totalTime", 0)
        
        if game_start_time and not saved_state.get("isTimeUp", False):
            try:
                # Parse game start time
                if isinstance(game_start_time, str):
                    start_time = datetime.fromisoformat(game_start_time.replace('Z', '+00:00'))
                else:
                    start_time = game_start_time
                
                elapsed_time = (datetime.utcnow() - start_time).total_seconds()
                calculated_time_left = max(0, total_time - int(elapsed_time))
            except Exception as e:
                print(f"Error calculating remaining time: {e}")
                # Fallback to saved time left
                calculated_time_left = saved_state.get("timeLeft", 0)
        else:
            calculated_time_left = saved_state.get("timeLeft", 0)
        
        # Prepare response with safe defaults
        response_data = {
            "hasState": True,
            "message": "Game state restored successfully",
            "gameState": {
                "currentWord": saved_state.get("currentWord", ""),
                "solution": saved_state.get("solution", []),
                "availableLetters": saved_state.get("availableLetters", []),
                "validatedWords": saved_state.get("validatedWords", []),
                "wordIndex": saved_state.get("wordIndex", 0),
                "timeLeft": calculated_time_left,
                "totalTime": saved_state.get("totalTime", 0),
                "isTimeUp": calculated_time_left <= 0,
                "solutions": saved_state.get("solutions", {}),
                "allValidatedWords": saved_state.get("allValidatedWords", []),
                "showOverview": saved_state.get("showOverview", False)
            }
        }
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error restoring game state: {str(e)}")
        print(f"SessionId: {sessionId}, ProlificId: {prolificId}, Phase: {phase}")
        # Don't raise an error here - return no state instead to allow game to continue
        return {"hasState": False, "message": f"Error restoring state: {str(e)}"}

@app.delete("/api/game-state/clear")
async def clear_game_state(sessionId: str, prolificId: str, phase: str):
    """Clear saved game state when game is completed."""
    try:
        # Validate inputs
        if not sessionId or not prolificId or not phase:
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        if not ObjectId.is_valid(sessionId):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        if phase not in ["tutorial", "main_game"]:
            raise HTTPException(status_code=400, detail="Invalid phase. Must be 'tutorial' or 'main_game'")
        
        # Clear the specific phase data
        result = await app.database.sessions.update_one(
            {"_id": ObjectId(sessionId), "prolificId": prolificId},
            {"$unset": {f"gameState.currentGameSession.{phase}": ""}}
        )
        
        if result.modified_count == 0:
            # Check if session exists but prolific ID doesn't match
            session_exists = await app.database.sessions.find_one({"_id": ObjectId(sessionId)})
            if session_exists:
                raise HTTPException(status_code=403, detail="Session ID and Prolific ID don't match")
            else:
                raise HTTPException(status_code=404, detail="Session not found")
        
        return {"status": "success", "message": f"Game state cleared for phase: {phase}"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error clearing game state: {str(e)}")
        print(f"SessionId: {sessionId}, ProlificId: {prolificId}, Phase: {phase}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
