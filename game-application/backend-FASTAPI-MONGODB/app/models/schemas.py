from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
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

class AntiCheatingMessage(BaseModel):
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
    # Make all these fields optional
    submittedAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None
    validatedAt: Optional[datetime] = None

class SessionInit(BaseModel):
    prolificId: str
    metadata: Metadata

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
    currentMessage: Optional[AntiCheatingMessage]
    word: str
    solutions: Dict[str, List[str]]
    timeSettings: Dict[str, int]
    totalAnagrams: int

class GameResponse(BaseModel):
    word: str
    solutions: Dict[str, List[str]]