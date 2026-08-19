from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import InterviewSession, User
from schemas import InterviewSessionCreate, InterviewSessionResponse, QuestionResponse, AnswerSubmit, EvaluationResponse
from interview_service import (
    create_interview_session, generate_question, submit_answer, end_interview
)

router = APIRouter(prefix="/api/sessions", tags=["interviews"])

def get_current_user(db: Session = Depends(get_db)):
    """Get current user (simplified for now)"""
    # In real app, extract from JWT token
    # For now, return user_id = 1
    return 1

@router.post("/create", response_model=InterviewSessionResponse)
async def create_session(
    session_data: InterviewSessionCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """Create new interview session"""
    
    db_session = create_interview_session(db, user_id, session_data)
    
    return {
        "id": db_session.id,
        "user_id": db_session.user_id,
        "mode": db_session.mode,
        "role": db_session.role,
        "company": db_session.company,
        "difficulty": db_session.difficulty,
        "status": db_session.status,
        "turn_count": db_session.turn_count,
        "turn_budget": db_session.turn_budget,
        "time_budget_seconds": db_session.time_budget_seconds,
        "started_at": db_session.started_at
    }

@router.get("/{session_id}", response_model=InterviewSessionResponse)
async def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get interview session details"""
    
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "id": session.id,
        "user_id": session.user_id,
        "mode": session.mode,
        "role": session.role,
        "company": session.company,
        "difficulty": session.difficulty,
        "status": session.status,
        "turn_count": session.turn_count,
        "turn_budget": session.turn_budget,
        "time_budget_seconds": session.time_budget_seconds,
        "started_at": session.started_at
    }

@router.get("/{session_id}/question", response_model=QuestionResponse)
async def get_next_question(session_id: int, db: Session = Depends(get_db)):
    """Get next question for interview"""
    
    question = generate_question(db, session_id)
    if not question:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "id": question.id,
        "question_text": question.question_text,
        "turn_number": question.turn_number,
        "rubric_json": question.rubric_json
    }

@router.post("/{session_id}/submit-answer", response_model=EvaluationResponse)
async def submit_answer_endpoint(
    session_id: int,
    answer_data: AnswerSubmit,
    question_id: int,
    db: Session = Depends(get_db)
):
    """Submit answer and get evaluation"""
    
    evaluation = submit_answer(db, question_id, answer_data)
    if not evaluation:
        raise HTTPException(status_code=400, detail="Error submitting answer")
    
    return {
        "id": evaluation.id,
        "scores_json": evaluation.scores_json,
        "overall_level": evaluation.overall_level,
        "feedback": evaluation.feedback
    }

@router.post("/{session_id}/end")
async def end_interview_endpoint(session_id: int, db: Session = Depends(get_db)):
    """End interview session"""
    
    session = end_interview(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"status": "completed", "session_id": session_id}