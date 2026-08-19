import math
from typing import List, Dict
from sqlalchemy.orm import Session
from models import CandidateSkillProfile, InterviewSession

class AdaptivePolicy:
    """Determines which skill to drill next based on performance"""
    
    @staticmethod
    def calculate_question_score(skill_profile: CandidateSkillProfile) -> float:
        """
        Score a skill for drilling (higher = should ask about this skill next)
        
        Score = relevance × weakness × uncertainty
        - weakness = (1 - mastery) → drill weak areas
        - uncertainty = how sure we are → drill uncertain areas
        """
        
        # Relevance weight (all skills equally important for MVP)
        relevance = 1.0
        
        # Weakness: 1 - mastery (0.5 mastery = 0.5 weakness)
        weakness = 1.0 - skill_profile.mastery
        
        # Uncertainty factor (more uncertainty = higher priority)
        uncertainty_factor = 1.0 + (0.5 * skill_profile.uncertainty)
        
        score = relevance * weakness * uncertainty_factor
        
        return score
    
    @staticmethod
    def select_next_skill(
        db: Session,
        session_id: int,
        user_id: int
    ) -> CandidateSkillProfile:
        """
        Select the next skill to drill based on adaptive policy
        """
        
        # Get all skill profiles for this session
        skill_profiles = db.query(CandidateSkillProfile).filter(
            CandidateSkillProfile.interview_session_id == session_id,
            CandidateSkillProfile.user_id == user_id
        ).all()
        
        if not skill_profiles:
            return None
        
        # Calculate scores for each skill
        scored_skills = []
        for profile in skill_profiles:
            score = AdaptivePolicy.calculate_question_score(profile)
            scored_skills.append((profile, score))
        
        # Sort by score (highest first)
        scored_skills.sort(key=lambda x: x[1], reverse=True)
        
        # Return the skill with highest score
        return scored_skills[0][0]
    
    @staticmethod
    def update_mastery(
        old_mastery: float,
        performance: float,
        evidence_count: int
    ) -> tuple:
        """
        Update mastery score based on performance (Elo-like rating)
        
        Returns: (new_mastery, new_uncertainty)
        """
        
        # Learning rate decreases with more evidence
        # More evidence = we're more confident, so change slower
        learning_rate = 0.5 / math.sqrt(evidence_count + 1)
        
        # Update mastery: move towards performance
        new_mastery = old_mastery + (learning_rate * (performance - old_mastery))
        new_mastery = max(0.0, min(1.0, new_mastery))  # Clamp to [0, 1]
        
        # Uncertainty decreases with more evidence
        new_uncertainty = 0.85 ** (evidence_count + 1)
        new_uncertainty = max(0.1, new_uncertainty)  # Minimum uncertainty
        
        return new_mastery, new_uncertainty
    
    @staticmethod
    def adjust_difficulty(
        current_difficulty: str,
        performance: float  # 0-1 scale
    ) -> str:
        """
        Adjust difficulty based on performance
        
        performance >= 0.8 (score 3.2+/4) → increase difficulty
        performance >= 0.6 (score 2.4+/4) → keep same
        performance < 0.6 (score < 2.4/4) → decrease difficulty
        """
        
        if performance >= 0.8:
            # User did well, increase difficulty
            if current_difficulty == "easy":
                return "medium"
            elif current_difficulty == "medium":
                return "hard"
            else:  # already hard
                return "hard"
        
        elif performance >= 0.6:
            # User did okay, keep same difficulty
            return current_difficulty
        
        else:
            # User struggled, decrease difficulty
            if current_difficulty == "hard":
                return "medium"
            elif current_difficulty == "medium":
                return "easy"
            else:  # already easy
                return "easy"