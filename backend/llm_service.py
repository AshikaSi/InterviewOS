import google.genai as genai
from config import settings
import json

# Configure Gemini with new package
client = genai.Client(api_key=settings.GEMINI_API_KEY)

class InterviewerAgent:
    """Generates interview questions using Gemini AI"""
    
    def generate_question(self, mode: str, skill: str, difficulty: str, turn_number: int) -> dict:
        """Generate a question for interview"""
        
        if mode == "technical_qa":
            prompt = self._build_technical_prompt(skill, difficulty, turn_number)
        elif mode == "system_design":
            prompt = self._build_system_design_prompt(difficulty, turn_number)
        elif mode == "behavioral":
            prompt = self._build_behavioral_prompt(difficulty, turn_number)
        else:
            prompt = self._build_technical_prompt(skill, difficulty, turn_number)
        
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            result = self._parse_response(response.text)
            
            return {
                "question_text": result.get("question", ""),
                "rubric_json": json.dumps(result.get("rubric", {})),
                "success": True
            }
        except Exception as e:
            return {
                "question_text": f"Error generating question: {str(e)}",
                "rubric_json": "{}",
                "success": False
            }
    
    def generate_question_with_rag(
        self,
        db,
        mode: str,
        skill: str,
        difficulty: str,
        turn_number: int,
        similar_problems: list = None
    ) -> dict:
        """Generate question using RAG for context"""
        
        # Build RAG context
        rag_context = ""
        if similar_problems:
            rag_context = "\n\nSimilar real problems for context:\n"
            for problem in similar_problems:
                rag_context += f"- {problem['title']} ({problem['difficulty']}): {problem['description']}\n"
        
        # Build prompt with RAG context
        if mode == "technical_qa":
            prompt = self._build_technical_prompt(skill, difficulty, turn_number)
            if rag_context:
                prompt += rag_context
                prompt += "\nUse these similar problems as inspiration for realistic question generation."
        elif mode == "system_design":
            prompt = self._build_system_design_prompt(difficulty, turn_number)
            if rag_context:
                prompt += rag_context
        elif mode == "behavioral":
            prompt = self._build_behavioral_prompt(difficulty, turn_number)
        else:
            prompt = self._build_technical_prompt(skill, difficulty, turn_number)
        
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            result = self._parse_response(response.text)
            
            return {
                "question_text": result.get("question", ""),
                "rubric_json": json.dumps(result.get("rubric", {})),
                "success": True
            }
        except Exception as e:
            return {
                "question_text": f"Error generating question: {str(e)}",
                "rubric_json": "{}",
                "success": False
            }
    
    def _build_technical_prompt(self, skill: str, difficulty: str, turn_number: int) -> str:
        """Build prompt for technical Q&A"""
        
        difficulty_desc = {
            "easy": "basic concepts and simple implementation",
            "medium": "intermediate problem with some complexity",
            "hard": "complex problem with edge cases and optimization"
        }.get(difficulty, "intermediate")
        
        return f"""You are an expert technical interviewer. Generate a single interview question for {skill}.

Requirements:
- Difficulty: {difficulty_desc}
- Question number: {turn_number}
- Keep it concise (2-3 sentences)
- Make it practical and realistic
- Don't ask for code, ask for explanation/approach

Format your response EXACTLY like this:
QUESTION: [Your question here]
RUBRIC: {{"correctness": 0, "depth": 0, "communication": 0}}

Example:
QUESTION: Explain the difference between a stack and a queue, and provide a real-world use case for each.
RUBRIC: {{"correctness": 0, "depth": 0, "communication": 0}}"""
    
    def _build_system_design_prompt(self, difficulty: str, turn_number: int) -> str:
        """Build prompt for system design"""
        
        problems = [
            "Design a URL shortener like bit.ly",
            "Design a social media feed system",
            "Design a ride-sharing app like Uber",
            "Design a payment processing system",
            "Design a real-time chat application"
        ]
        
        problem = problems[turn_number % len(problems)]
        
        return f"""You are a senior system design interviewer. 

Generate a follow-up question about: {problem}

Difficulty level: {difficulty}
This is question #{turn_number} in the conversation.

Ask about a specific aspect like:
- API design
- Database schema
- Caching strategy
- Scalability concerns
- Trade-offs

Format your response EXACTLY like this:
QUESTION: [Your question here]
RUBRIC: {{"api_design": 0, "database": 0, "scalability": 0, "trade_offs": 0}}

Example:
QUESTION: How would you design the database schema for storing user data and their shortened URLs? What indexes would you add and why?
RUBRIC: {{"api_design": 0, "database": 0, "scalability": 0, "trade_offs": 0}}"""
    
    def _build_behavioral_prompt(self, difficulty: str, turn_number: int) -> str:
        """Build prompt for behavioral questions"""
        
        themes = [
            "conflict resolution",
            "leadership and initiative",
            "learning from failure",
            "time management",
            "technical decision making"
        ]
        
        theme = themes[turn_number % len(themes)]
        
        return f"""You are an experienced behavioral interviewer.

Generate a behavioral question focusing on: {theme}
Difficulty: {difficulty}
Question number: {turn_number}

Ask for a STAR format response (Situation, Task, Action, Result).
Keep it open-ended and realistic.

Format your response EXACTLY like this:
QUESTION: [Your question here]
RUBRIC: {{"situation_clarity": 0, "action_taken": 0, "result_impact": 0, "communication": 0}}

Example:
QUESTION: Tell me about a time when you had to make a critical technical decision under time pressure. Walk me through your thought process.
RUBRIC: {{"situation_clarity": 0, "action_taken": 0, "result_impact": 0, "communication": 0}}"""
    
    def _parse_response(self, response_text: str) -> dict:
        """Parse Gemini response"""
        
        try:
            lines = response_text.strip().split('\n')
            question = ""
            rubric = {}
            
            for line in lines:
                if line.startswith("QUESTION:"):
                    question = line.replace("QUESTION:", "").strip()
                elif line.startswith("RUBRIC:"):
                    rubric_str = line.replace("RUBRIC:", "").strip()
                    rubric = json.loads(rubric_str)
            
            return {
                "question": question or "Unable to parse question",
                "rubric": rubric or {}
            }
        except Exception as e:
            return {
                "question": response_text[:200],
                "rubric": {}
            }


class EvaluatorAgent:
    """Evaluates answers using Gemini AI"""
    
    def evaluate_answer(self, question: str, answer: str, rubric: dict) -> dict:
        """Evaluate a candidate's answer"""
        
        prompt = f"""You are an expert technical interviewer evaluating a candidate's answer.

QUESTION: {question}

CANDIDATE'S ANSWER: {answer}

EVALUATION RUBRIC: {json.dumps(rubric)}

Score the answer on a scale of 0-4 for each rubric item:
- 0 = No understanding
- 1 = Vague, lacks clarity
- 2 = Partial understanding
- 3 = Solid understanding
- 4 = Expert level

Provide specific feedback on strengths and gaps.

Format your response EXACTLY like this:
SCORES: {{"rubric_key_1": 3, "rubric_key_2": 2, "rubric_key_3": 3}}
OVERALL_LEVEL: 3
FEEDBACK: [Your feedback here - 1-2 sentences highlighting strengths and areas to improve]

Example:
SCORES: {{"correctness": 3, "depth": 2, "communication": 3}}
OVERALL_LEVEL: 3
FEEDBACK: Good understanding of the core concepts with clear explanation. Could have gone deeper into edge cases and optimization strategies."""
        
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            result = self._parse_evaluation(response.text)
            return result
        except Exception as e:
            return {
                "scores": {},
                "overall_level": 2,
                "feedback": "Unable to evaluate at this moment",
                "success": False
            }
    
    def _parse_evaluation(self, response_text: str) -> dict:
        """Parse evaluation response"""
        
        try:
            scores = {}
            overall_level = 2
            feedback = ""
            
            lines = response_text.strip().split('\n')
            
            for line in lines:
                if line.startswith("SCORES:"):
                    scores_str = line.replace("SCORES:", "").strip()
                    scores = json.loads(scores_str)
                elif line.startswith("OVERALL_LEVEL:"):
                    overall_level = int(line.replace("OVERALL_LEVEL:", "").strip())
                elif line.startswith("FEEDBACK:"):
                    feedback = line.replace("FEEDBACK:", "").strip()
            
            return {
                "scores": scores,
                "overall_level": overall_level,
                "feedback": feedback,
                "success": True
            }
        except Exception as e:
            return {
                "scores": {},
                "overall_level": 2,
                "feedback": str(e),
                "success": False
            }


class PlannerAgent:
    """Generates personalized prep plans"""
    
    def generate_prep_plan(self, weaknesses: list, interview_mode: str, company: str = None) -> dict:
        """Generate personalized prep plan"""
        
        company_context = f" for {company}" if company else ""
        
        prompt = f"""You are a career coach helping someone prepare for a {interview_mode} interview{company_context}.

Their weakest areas are:
{chr(10).join([f"- {w}" for w in weaknesses])}

Create a 2-week personalized prep plan with:
- 3 focus areas
- Specific topics to study each week
- Estimated hours needed
- Resources/practice recommendations

Format your response EXACTLY like this:
WEEK_1_FOCUS: [Topic]
WEEK_1_TOPICS: [Specific topics]
WEEK_1_HOURS: [Number]
WEEK_1_RESOURCES: [Resources]

WEEK_2_FOCUS: [Topic]
WEEK_2_TOPICS: [Specific topics]
WEEK_2_HOURS: [Number]
WEEK_2_RESOURCES: [Resources]"""
        
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            result = self._parse_plan(response.text)
            return result
        except Exception as e:
            return {
                "plan": f"Error generating plan: {str(e)}",
                "success": False
            }
    
    def _parse_plan(self, response_text: str) -> dict:
        """Parse prep plan response"""
        
        return {
            "plan": response_text,
            "success": True
        }