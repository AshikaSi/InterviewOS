from sqlalchemy.orm import Session
from models import (
    InterviewSession, InterviewQuestion, CandidateAnswer, 
    Evaluation, Skill, CandidateSkillProfile, User
)
from schemas import InterviewSessionCreate, AnswerSubmit
from llm_service import InterviewerAgent, EvaluatorAgent, PlannerAgent
from adaptive_policy import AdaptivePolicy
from skills_service import SkillsService
import json
from datetime import datetime

# Initialize AI agents
interviewer = InterviewerAgent()
evaluator = EvaluatorAgent()
planner = PlannerAgent()

# Time budgets
TIME_BUDGETS = {
    "technical_qa": 45 * 60,
    "system_design": 60 * 60,
    "behavioral": 30 * 60,
}

# Turn budgets
TURN_BUDGETS = {
    "technical_qa": 10,
    "system_design": 5,
    "behavioral": 4,
}

def create_interview_session(db: Session, user_id: int, session_data: InterviewSessionCreate):
    """Create a new interview session with initialized skills"""
    
    # Initialize all skills if not already done
    SkillsService.initialize_skills(db)
    
    mode = session_data.mode
    time_budget = TIME_BUDGETS.get(mode, 45 * 60)
    turn_budget = TURN_BUDGETS.get(mode, 5)
    
    db_session = InterviewSession(
        user_id=user_id,
        mode=mode,
        role=session_data.role,
        company=session_data.company,
        difficulty=session_data.difficulty,
        initial_difficulty=session_data.difficulty,
        current_difficulty=session_data.difficulty,
        time_budget_seconds=time_budget,
        turn_budget=turn_budget,
        status="in_progress"
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    # Seed skill profiles for this session
    SkillsService.seed_skill_profiles(db, user_id, db_session.id, mode)
    
    return db_session

def generate_question(db: Session, session_id: int):
    """Generate next question using adaptive policy"""
    
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        return None
    
    # Select next skill using adaptive policy
    next_skill_profile = AdaptivePolicy.select_next_skill(
        db, session_id, session.user_id
    )
    
    if not next_skill_profile:
        return None
    
    skill_name = next_skill_profile.skill_id and db.query(Skill).filter(
        Skill.id == next_skill_profile.skill_id
    ).first().name or "General"
    
    # Call AI to generate question
    ai_response = interviewer.generate_question(
        mode=session.mode,
        skill=skill_name,
        difficulty=session.current_difficulty,
        turn_number=session.turn_count + 1
    )
    
    # Create question record
    turn_number = session.turn_count + 1
    
    db_question = InterviewQuestion(
        interview_session_id=session_id,
        turn_number=turn_number,
        question_text=ai_response["question_text"],
        rubric_json=ai_response["rubric_json"]
    )
    
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    return db_question

def submit_answer(db: Session, question_id: int, answer_data: AnswerSubmit):
    """Submit answer, evaluate, and update adaptive state"""
    
    # Get the question
    question = db.query(InterviewQuestion).filter(InterviewQuestion.id == question_id).first()
    if not question:
        return None
    
    # Get the session
    session = db.query(InterviewSession).filter(
        InterviewSession.id == question.interview_session_id
    ).first()
    
    # Save answer
    db_answer = CandidateAnswer(
        interview_question_id=question_id,
        answer_text=answer_data.answer_text
    )
    
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    
    # Get rubric
    rubric = json.loads(question.rubric_json) if question.rubric_json else {}
    
    # Call AI to evaluate
    eval_response = evaluator.evaluate_answer(
        question=question.question_text,
        answer=answer_data.answer_text,
        rubric=rubric
    )
    
    overall_level = eval_response.get("overall_level", 2)
    performance = overall_level / 4.0  # Convert to 0-1 scale
    
    # Store evaluation
    db_eval = Evaluation(
        candidate_answer_id=db_answer.id,
        overall_level=overall_level,
        feedback=eval_response.get("feedback", ""),
        scores_json=json.dumps(eval_response.get("scores", {}))
    )
    
    db.add(db_eval)
    
    # Update difficulty based on performance
    new_difficulty = AdaptivePolicy.adjust_difficulty(
        session.current_difficulty,
        performance
    )
    session.current_difficulty = new_difficulty
    
    # Update skill profile with new mastery
    skill_profile = AdaptivePolicy.select_next_skill(db, session.id, session.user_id)
    if skill_profile:
        new_mastery, new_uncertainty = AdaptivePolicy.update_mastery(
            skill_profile.mastery,
            performance,
            skill_profile.evidence_count
        )
        skill_profile.mastery = new_mastery
        skill_profile.uncertainty = new_uncertainty
        skill_profile.evidence_count += 1
    
    # Update session
    session.turn_count += 1
    
    if session.turn_count >= session.turn_budget:
        session.status = "completed"
        session.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_eval)
    
    return db_eval

def end_interview(db: Session, session_id: int):
    """End interview session"""
    
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if session:
        session.status = "completed"
        session.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
    
    return session

def generate_prep_plan(weaknesses: list, mode: str, company: str = None) -> dict:
    """Generate personalized prep plan"""
    
    return planner.generate_prep_plan(weaknesses, mode, company)