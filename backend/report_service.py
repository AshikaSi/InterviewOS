from sqlalchemy.orm import Session
from models import (
    InterviewReport, InterviewSession, Evaluation, 
    CandidateAnswer, InterviewQuestion, CandidateSkillProfile, Skill
)
from llm_service import PlannerAgent
import json
from datetime import datetime

planner = PlannerAgent()

class ReportService:
    """Generates comprehensive interview reports"""
    
    @staticmethod
    def generate_report(db: Session, session_id: int) -> InterviewReport:
        """Generate a complete report for an interview session"""
        
        # Get session
        session = db.query(InterviewSession).filter(
            InterviewSession.id == session_id
        ).first()
        
        if not session:
            return None
        
        # Check if report already exists
        existing_report = db.query(InterviewReport).filter(
            InterviewReport.interview_session_id == session_id
        ).first()
        
        if existing_report:
            return existing_report
        
        # Calculate overall score
        evaluations = db.query(Evaluation).join(
            CandidateAnswer
        ).join(
            InterviewQuestion
        ).filter(
            InterviewQuestion.interview_session_id == session_id
        ).all()
        
        if evaluations:
            overall_score = sum(e.overall_level for e in evaluations) // len(evaluations)
        else:
            overall_score = 0
        
        # Calculate duration
        duration_seconds = int(
            (session.completed_at - session.started_at).total_seconds()
        ) if session.completed_at else 0
        
        # Calculate skill scores
        skill_profiles = db.query(CandidateSkillProfile).filter(
            CandidateSkillProfile.interview_session_id == session_id
        ).all()
        
        skill_scores = {}
        weakest_skill = None
        weakest_score = 1.0
        
        for profile in skill_profiles:
            skill = db.query(Skill).filter(Skill.id == profile.skill_id).first()
            if skill:
                score = profile.mastery
                skill_scores[skill.name] = score
                
                if score < weakest_score:
                    weakest_score = score
                    weakest_skill = skill
        
        # Get top 3 weaknesses
        sorted_skills = sorted(skill_scores.items(), key=lambda x: x[1])
        top_3_weaknesses = [skill[0] for skill in sorted_skills[:3]]
        
        # Identify strengths
        sorted_skills_desc = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
        strengths = [skill[0] for skill in sorted_skills_desc[:3]]
        
        # Generate prep plan
        prep_plan = planner.generate_prep_plan(
            weaknesses=top_3_weaknesses,
            interview_mode=session.mode,
            company=session.company
        )
        
        # Create report
        report = InterviewReport(
            interview_session_id=session_id,
            user_id=session.user_id,
            overall_score=overall_score,
            duration_seconds=duration_seconds,
            skill_scores_json=json.dumps(skill_scores),
            weakest_skill_id=weakest_skill.id if weakest_skill else None,
            weakest_skill_score=weakest_score,
            top_3_weaknesses_json=json.dumps(top_3_weaknesses),
            strengths_json=json.dumps(strengths),
            prep_plan_json=json.dumps(prep_plan)
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return report
    
    @staticmethod
    def get_report(db: Session, session_id: int) -> InterviewReport:
        """Get or generate report for a session"""
        
        report = db.query(InterviewReport).filter(
            InterviewReport.interview_session_id == session_id
        ).first()
        
        if not report:
            report = ReportService.generate_report(db, session_id)
        
        return report
    
    @staticmethod
    def get_user_reports(db: Session, user_id: int) -> list:
        """Get all reports for a user"""
        
        return db.query(InterviewReport).filter(
            InterviewReport.user_id == user_id
        ).order_by(InterviewReport.created_at.desc()).all()