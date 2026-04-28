from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from app.config.config import settings

class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="The text to analyze for plagiarism")
    submissionId: Optional[str] = Field(None, description="Optional submission ID")

    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Text cannot be empty or only whitespace")
        if len(v) > settings.MAX_TEXT_LENGTH:
            raise ValueError(f"Text exceeds maximum allowed length of {settings.MAX_TEXT_LENGTH} characters")
        return v

class CompareTwoRequest(BaseModel):
    text1: str = Field(..., description="First text to compare")
    text2: str = Field(..., description="Second text to compare")

    @field_validator('text1', 'text2')
    @classmethod
    def validate_texts(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Text cannot be empty")
        if len(v) > settings.MAX_TEXT_LENGTH:
            raise ValueError(f"Text exceeds maximum length")
        return v

class MatchResult(BaseModel):
    sourceId: str
    sourceName: str
    similarity: float
    matchedText: str
    inputText: str
    matchType: str

class AnalyzeResponse(BaseModel):
    success: bool
    similarity: float
    riskLevel: str
    matches: List[MatchResult]
    processingTimeMs: int
