from sqlalchemy.orm import Session
from models import Skill, CandidateSkillProfile, InterviewSession

class SkillsService:
    """Manages skill tracking and initialization"""
    
    # Define all skills by mode
    SKILLS_BY_MODE = {
        "technical_qa": [
            ("Data Structures", "technical_qa"),
            ("Algorithms", "technical_qa"),
            ("DBMS", "technical_qa"),
            ("Operating Systems", "technical_qa"),
            ("Networks", "technical_qa"),
            ("OOP", "technical_qa"),
        ],
        "system_design": [
            ("Requirements Analysis", "system_design"),
            ("API Design", "system_design"),
            ("Database Design", "system_design"),
            ("Caching", "system_design"),
            ("Scalability", "system_design"),
            ("Reliability", "system_design"),
        ],
        "behavioral": [
            ("Problem Solving", "behavioral"),
            ("Collaboration", "behavioral"),
            ("Learning & Growth", "behavioral"),
            ("Time Management", "behavioral"),
            ("Leadership", "behavioral"),
            ("Communication", "behavioral"),
        ]
    }
    
    @staticmethod
    def initialize_skills(db: Session):
        """Create all skills in database if they don't exist"""
        
        for mode, skills in SkillsService.SKILLS_BY_MODE.items():
            for skill_name, skill_mode in skills:
                # Check if skill exists
                existing = db.query(Skill).filter(
                    Skill.name == skill_name,
                    Skill.mode == skill_mode
                ).first()
                
                if not existing:
                    # Create new skill
                    new_skill = Skill(
                        name=skill_name,
                        mode=skill_mode
                    )
                    db.add(new_skill)
        
        db.commit()
    
    @staticmethod
    def seed_skill_profiles(
        db: Session,
        user_id: int,
        session_id: int,
        mode: str
    ):
        """Initialize skill profiles for a new interview session"""
        
        # Get all skills for this mode
        skills = db.query(Skill).filter(Skill.mode == mode).all()
        
        if not skills:
            return  # No skills found
        
        for skill in skills:
            # Check if profile already exists
            existing = db.query(CandidateSkillProfile).filter(
                CandidateSkillProfile.user_id == user_id,
                CandidateSkillProfile.interview_session_id == session_id,
                CandidateSkillProfile.skill_id == skill.id
            ).first()
            
            if not existing:
                # Create new profile
                profile = CandidateSkillProfile(
                    user_id=user_id,
                    interview_session_id=session_id,
                    skill_id=skill.id,
                    mastery=0.5,  # Start neutral
                    uncertainty=1.0,  # High uncertainty initially
                    evidence_count=0
                )
                db.add(profile)
        
        db.commit()