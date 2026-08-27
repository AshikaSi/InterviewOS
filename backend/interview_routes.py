from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from database import get_db
from models import InterviewSession, User
from schemas import InterviewSessionCreate, InterviewSessionResponse, QuestionResponse, AnswerSubmit, EvaluationResponse
from interview_service import (
    create_interview_session, generate_question, submit_answer, end_interview
)
import json
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


@router.get("/{session_id}/report", response_model=dict)
async def get_report(session_id: int, db: Session = Depends(get_db)):
    """Get interview report"""
    
    from report_service import ReportService
    
    report = ReportService.get_report(db, session_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {
        "id": report.id,
        "overall_score": report.overall_score,
        "duration_seconds": report.duration_seconds,
        "skill_scores": json.loads(report.skill_scores_json) if report.skill_scores_json else {},
        "top_3_weaknesses": json.loads(report.top_3_weaknesses_json) if report.top_3_weaknesses_json else [],
        "strengths": json.loads(report.strengths_json) if report.strengths_json else [],
        "prep_plan": json.loads(report.prep_plan_json) if report.prep_plan_json else {}
    }

@router.get("/user/all-reports")
async def get_all_user_reports(
    db: Session = Depends(get_db),
    user_id: int = 1
):
    """Get all reports for a user"""
    
    from report_service import ReportService
    
    reports = ReportService.get_user_reports(db, user_id)
    
    return [{
        "id": r.id,
        "session_id": r.interview_session_id,
        "overall_score": r.overall_score,
        "created_at": r.created_at,
        "weakest_skills": json.loads(r.top_3_weaknesses_json) if r.top_3_weaknesses_json else []
    } for r in reports]


@router.get("/{session_id}/question/audio")
async def get_question_audio(session_id: int, db: Session = Depends(get_db)):
    """Get audio version of the current question"""
    
    from audio_service import audio_service
    
    # Get latest question
    question = db.query(InterviewQuestion).filter(
        InterviewQuestion.interview_session_id == session_id
    ).order_by(InterviewQuestion.id.desc()).first()
    
    if not question:
        raise HTTPException(status_code=404, detail="No question found")
    
    # Generate audio
    audio_base64 = audio_service.text_to_speech_base64(question.question_text)
    
    return {
        "question_id": question.id,
        "audio": audio_base64,
        "format": "mp3"
    }


@router.post("/{session_id}/transcribe-audio")
async def transcribe_audio(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Transcribe audio to text using Whisper"""
    
    from stt_service import stt_service
    
    try:
        # Read audio file
        audio_bytes = await file.read()
        
        # Transcribe using Whisper
        transcribed_text = stt_service.transcribe_from_bytes(
            audio_bytes,
            filename=file.filename or "audio.wav"
        )
        
        if not transcribed_text:
            raise HTTPException(
                status_code=400,
                detail="Failed to transcribe audio"
            )
        
        return {
            "text": transcribed_text,
            "success": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription error: {str(e)}"
        )