from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union
from datetime import datetime

class WordWithAnagram(BaseModel):
    word: str
    length: Optional[int]
    isValid: bool
    anagramShown: str

class ResourceUsageDetails(BaseModel):
    usedExternalResources: bool
    wordsWithExternalHelp: List[WordWithAnagram]
    totalWordsChecked: int
    responseTimestamp: datetime

class ValidWord(BaseModel):
    word: str
    length: int
    reward: Optional[int] = None
    validatedAt: Optional[datetime] = None
    isValid: Optional[bool] = None
    anagramShown: Optional[str] = None
    
class AnagramDetail(BaseModel):
    anagram: str
    words: List[ValidWord]
    
class Metadata(BaseModel):
    browser: str
    platform: Optional[str] = None
    screenSize: Dict[str, int]

class MotivationalMessage(BaseModel):
    id: int
    text: str
    shownAt: Optional[datetime] = None

class GameEventDetails(BaseModel):
    word: Optional[str] = None
    wordLength: Optional[int] = None
    isValid: Optional[bool] = None
    timeSpent: Optional[int] = None
    timeSinceLastAction: Optional[int] = None
    timeElapsed: Optional[int] = None
    wordCount: Optional[int] = None
    messageId: Optional[str] = None
    messageText: Optional[str] = None
    timeSpentOnMessage: Optional[int] = None
    theory: Optional[str] = None
    words: Optional[List[ValidWord]] = None
    reason: Optional[str] = None
    timeInList: Optional[int] = None
    providedMeaning: Optional[str] = None
    anagram: Optional[str] = None
    anagramShown: Optional[str] = None
    wordIndex: Optional[int] = None
    usedExternalResources: Optional[bool] = None
    wordsWithExternalHelp: Optional[List[WordWithAnagram]] = None
    totalWordsChecked: Optional[int] = None
    skillLevel: Optional[int] = None

class GameEvent(BaseModel):
    sessionId: str
    prolificId: str
    phase: str
    currentMessageId: Optional[int] = None
    anagramShown: Optional[str] = None
    eventType: str
    details: Optional[GameEventDetails] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class WordSubmission(BaseModel):
    sessionId: str
    prolificId: str
    phase: str
    anagramShown: str 
    submittedWords: List[ValidWord]
    totalReward: int
    timeSpent: int
    submittedAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None
    validatedAt: Optional[datetime] = None

class WordMeaningCheck(BaseModel):
    word: str
    providedMeaning: str
    isCorrect: Optional[bool] = None
    
class WordMeaning(BaseModel):
    word: str
    providedMeaning: str
    isCorrect: Optional[bool] = None
    submittedAt: Optional[datetime] = None

class WordMeaningSubmission(BaseModel):
    sessionId: str
    prolificId: str
    wordMeanings: List[WordMeaning]
    completedAt: datetime
    totalTimeSpent: Optional[int] = None
    
class GameInit(BaseModel):
    currentMessage: Optional[MotivationalMessage]
    word: str
    solutions: Dict[str, List[str]]
    timeSettings: Dict[str, int]
    totalAnagrams: int

class GameResponse(BaseModel):
    word: str
    solutions: Dict[str, List[str]]

class Position(BaseModel):
    x: int
    y: int

class MouseMoveData(BaseModel):
    x: int
    y: int
    pressure: Optional[float] = 0
    distanceMoved: Optional[int] = None
    isFirstMove: Optional[bool] = False
    isEnteringGameArea: Optional[bool] = None
    isLeavingGameArea: Optional[bool] = None
    wordInProgress: Optional[str] = ""
    sessionEventId: Optional[int] = None  # NEW
    conflictType: Optional[str] = None    # NEW
    relatedDragId: Optional[int] = None   # NEW

class LetterDraggedData(BaseModel):
    letter: str
    sourceArea: str
    dragDuration: int = 0  # Always 0 in new approach
    wordInProgress: Optional[str] = ""
    sessionEventId: Optional[int] = None

class LetterHoverData(BaseModel):
    letter: str
    sourceArea: str
    hoverDuration: int
    wordInProgress: Optional[str] = ""
    sessionEventId: Optional[int] = None  # NEW
    conflictType: Optional[str] = None    # NEW
    relatedDragId: Optional[int] = None   # NEW

class UserInteraction(BaseModel):
    sessionId: str
    prolificId: str
    phase: str
    anagramShown: str
    interactionType: str  # 'mouse_move', 'letter_dragged', 'letter_hovered'
    timestamp: str  # Changed to string to accept ISO format
    data: Dict[str, Any]  # Flexible data structure
    
    class Config:
        # Allow extra fields in data for future extensibility
        extra = "allow"

class InteractionBatch(BaseModel):
    sessionId: str
    prolificId: str
    phase: str
    anagramShown: str
    interactions: List[UserInteraction]
    batchStartTime: str
    batchEndTime: str

class GameAreaBounds(BaseModel):
    left: float
    top: float
    width: float
    height: float

class ScreenSize(BaseModel):
    width: int
    height: int

class GameAreaData(BaseModel):
    """Game area information to be stored within session document"""
    bounds: GameAreaBounds
    screenSize: ScreenSize
    userAgent: str
    calculatedAt: datetime = Field(default_factory=datetime.utcnow)

class SessionInit(BaseModel):
    prolificId: str
    metadata: Metadata
    gameArea: Optional[GameAreaData] = None

class InteractionSummary(BaseModel):
    """Summary of interactions for analytics"""
    totalInteractions: int
    dragEvents: int
    hoverEvents: int
    mouseMovements: int
    averageHoverDuration: float
    totalGameAreaExits: int

class BatchProcessingResult(BaseModel):
    """Result of batch processing"""
    status: str
    processedCount: int
    errors: Optional[List[str]] = None
    processingTime: Optional[float] = None
    
class GameStateData(BaseModel):
    """Schema for saving/restoring game state"""
    currentWord: Optional[str] = None
    solution: List[str] = []
    availableLetters: List[str] = []
    validatedWords: List[Dict[str, Any]] = []
    wordIndex: Optional[int] = 0
    timeLeft: Optional[int] = 0
    totalTime: Optional[int] = 0
    isTimeUp: Optional[bool] = False
    solutions: Dict[str, List[str]] = {}
    allValidatedWords: List[Dict[str, Any]] = []
    gameStartTime: Optional[str] = None
    showOverview: Optional[bool] = False
    isSubmitted: Optional[bool] = False

class SaveGameStateRequest(BaseModel):
    """Request schema for saving game state"""
    sessionId: str
    prolificId: str
    phase: str  # "tutorial" or "main_game"
    gameState: GameStateData

class RestoreGameStateResponse(BaseModel):
    """Response schema for restoring game state"""
    hasState: bool
    gameState: Optional[GameStateData] = None

class ClearGameStateRequest(BaseModel):
    """Request schema for clearing game state"""
    sessionId: str
    prolificId: str
    phase: str