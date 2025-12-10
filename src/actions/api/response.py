from pydantic import BaseModel
from typing import Optional, Dict, Any

class UploadResponse(BaseModel):
    filename: str
    parsed_text: str
    cached: bool

class ExtractInfoResponse(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    intent: Optional[str]
    experience_years: Optional[float]
    education: Optional[str]
    raw_text: Optional[str]

class MatchResponse(BaseModel):
    filename: str
    job_desc: str
    match_score: float
    detail: Dict[str, Any]

class ErrorResponse(BaseModel):
    error: str
