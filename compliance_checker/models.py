from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Match(BaseModel):
    """Represents a match from the worldcheck list."""
    name: str
    surname: Optional[str] = None
    birth_country: Optional[str] = None
    identification_number: List[str] = Field(default_factory=list)
    comments: Optional[str] = None
    match_score: float = Field(ge=0.0, le=1.0)
    type: str
    provider_id: str
    reference_id: str
    category: Optional[str] = None

class EvaluationResult(BaseModel):
    """Represents the evaluation result for an entry."""
    match_id: str
    evaluation_date: datetime = Field(default_factory=datetime.utcnow)
    risk_score: float = Field(ge=0.0, le=1.0)
    confidence_score: float = Field(ge=0.0, le=1.0)
    category: str
    explanation: str
    gpt_assessment: Optional[str] = None
    matches: List[Match] = Field(default_factory=list)

class RefinitivBlacklistEntry(BaseModel):
    """Represents an entry from the Refinitiv blacklist pipeline."""
    step_id: str
    step_category: str
    provider_id: str
    custom_groups: List[str] = Field(default_factory=list)
    data_creation: datetime
    information_object_id: str
    status: str
    time: int
    found: bool
    number_matches: int
    matches: List[Match] = Field(default_factory=list) 