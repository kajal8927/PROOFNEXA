from pydantic import BaseModel, Field
from typing import List


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=20)


class MatchResult(BaseModel):
    sourceFile: str
    matchedText: str
    similarity: float


class AnalyzeResponse(BaseModel):
    success: bool
    similarity: float
    matches: List[MatchResult]
