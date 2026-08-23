from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str]
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse

# Interview Schemas
class InterviewSessionCreate(BaseModel):
    mode: str  # technical_qa, system_design, behavioral
    role: Optional[str] = "general"
    company: Optional[str] = None
    difficulty: str = "medium"

class InterviewSessionResponse(BaseModel):
    id: int
    user_id: int
    mode: str
    role: Optional[str]
    company: Optional[str]
    difficulty: str
    status: str
    turn_count: int
    turn_budget: Optional[int]
    time_budget_seconds: Optional[int]
    started_at: datetime
    
    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    turn_number: int
    rubric_json: Optional[str]
    
    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    answer_text: str

class AnswerResponse(BaseModel):
    id: int
    answer_text: str
    answered_at: datetime
    
    class Config:
        from_attributes = True

class EvaluationResponse(BaseModel):
    id: int
    scores_json: Optional[str]
    overall_level: Optional[int]
    feedback: Optional[str]
    
    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    id: int
    interview_session_id: int
    overall_score: Optional[int]
    duration_seconds: Optional[int]
    skill_scores_json: Optional[str]
    weakest_skill_id: Optional[int]
    weakest_skill_score: Optional[float]
    top_3_weaknesses_json: Optional[str]
    strengths_json: Optional[str]
    prep_plan_json: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True