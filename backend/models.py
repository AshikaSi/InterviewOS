from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, func
from database import Base
from datetime import datetime
from enum import Enum

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(128))
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(256))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
from enum import Enum

class InterviewMode(str, Enum):
    TECHNICAL_QA = "technical_qa"
    SYSTEM_DESIGN = "system_design"
    BEHAVIORAL = "behavioral"

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mode = Column(String(32), nullable=False)
    role = Column(String(128))
    company = Column(String(256))
    difficulty = Column(String(32), default="medium")
    initial_difficulty = Column(String(32), default="medium")  # ADD THIS
    current_difficulty = Column(String(32), default="medium")  # ADD THIS
    status = Column(String(32), default="in_progress")
    turn_count = Column(Integer, default=0)
    turn_budget = Column(Integer)
    time_budget_seconds = Column(Integer)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    turn_number = Column(Integer)
    question_text = Column(String(2000), nullable=False)
    rubric_json = Column(String(2000))
    created_at = Column(DateTime, default=datetime.utcnow)

class CandidateAnswer(Base):
    __tablename__ = "candidate_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_question_id = Column(Integer, ForeignKey("interview_questions.id"), nullable=False)
    answer_text = Column(String(5000), nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_answer_id = Column(Integer, ForeignKey("candidate_answers.id"), nullable=False)
    scores_json = Column(String(500))
    overall_level = Column(Integer)
    feedback = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    mode = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)

class CandidateSkillProfile(Base):
    __tablename__ = "candidate_skill_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    mastery = Column(Float, default=0.5)
    uncertainty = Column(Float, default=1.0)
    evidence_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeBaseQuestion(Base):
    __tablename__ = "knowledge_base_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(32))  # "blind_75", "leetcode", etc
    skill_id = Column(Integer, ForeignKey("skills.id"))
    question_title = Column(String(256), nullable=False)
    question_description = Column(String(2000))
    difficulty_level = Column(String(32))
    topic_tags = Column(String(512))
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)