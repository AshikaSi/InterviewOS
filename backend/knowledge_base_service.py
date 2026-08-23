import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from sqlalchemy.orm import Session
from models import KnowledgeBaseQuestion, Skill

class KnowledgeBaseService:
    """Manages the knowledge base of interview problems"""
    
    # Blind 75 problems with correct skill names
    BLIND_75_PROBLEMS = [
        {
            "title": "Two Sum",
            "skill": "Algorithms",
            "difficulty": "easy",
            "description": "Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.",
            "tags": ["array", "hash-table", "two-pointer"]
        },
        {
            "title": "Best Time to Buy and Sell Stock",
            "skill": "Algorithms",
            "difficulty": "easy",
            "description": "You are given an array prices. Find the maximum profit from buying and selling once.",
            "tags": ["array", "dynamic-programming"]
        },
        {
            "title": "Contains Duplicate",
            "skill": "Data Structures",
            "difficulty": "easy",
            "description": "Given an integer array, return true if any value appears at least twice.",
            "tags": ["array", "hash-table"]
        },
        {
            "title": "Valid Anagram",
            "skill": "Data Structures",
            "difficulty": "easy",
            "description": "Given two strings s and t, return true if t is an anagram of s.",
            "tags": ["string", "hash-table", "sorting"]
        },
        {
            "title": "LRU Cache",
            "skill": "Data Structures",
            "difficulty": "hard",
            "description": "Design a Least Recently Used (LRU) cache data structure.",
            "tags": ["design", "hash-table", "linked-list"]
        },
        {
            "title": "Merge K Sorted Lists",
            "skill": "Algorithms",
            "difficulty": "hard",
            "description": "Merge k sorted linked lists into one sorted linked list.",
            "tags": ["linked-list", "divide-and-conquer", "heap"]
        },
        {
            "title": "Reverse Linked List",
            "skill": "Data Structures",
            "difficulty": "easy",
            "description": "Reverse a singly linked list.",
            "tags": ["linked-list", "recursion"]
        },
        {
            "title": "Longest Substring Without Repeating Characters",
            "skill": "Algorithms",
            "difficulty": "medium",
            "description": "Find the length of the longest substring without repeating characters.",
            "tags": ["string", "hash-table", "sliding-window"]
        },
        {
            "title": "ACID Transactions",
            "skill": "DBMS",
            "difficulty": "medium",
            "description": "Explain ACID properties in database transactions.",
            "tags": ["database", "transactions"]
        },
        {
            "title": "Process vs Thread",
            "skill": "Operating Systems",
            "difficulty": "medium",
            "description": "Explain the difference between processes and threads.",
            "tags": ["os", "concurrency"]
        },
    ]
    
    def __init__(self):
        """Initialize embedding model"""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings_cache = {}
    
    def seed_knowledge_base(self, db: Session):
        """Seed the knowledge base with problems"""
        
        for problem in self.BLIND_75_PROBLEMS:
            # Check if problem already exists
            existing = db.query(KnowledgeBaseQuestion).filter(
                KnowledgeBaseQuestion.question_title == problem["title"]
            ).first()
            
            if existing:
                continue
            
            # Get skill by name
            skill = db.query(Skill).filter(
                Skill.name == problem["skill"]
            ).first()
            
            if not skill:
                print(f"[KB] Skill '{problem['skill']}' not found in database")
                continue
            
            # Create knowledge base question
            kb_question = KnowledgeBaseQuestion(
                source="blind_75",
                skill_id=skill.id,
                question_title=problem["title"],
                question_description=problem["description"],
                difficulty_level=problem["difficulty"],
                topic_tags=",".join(problem["tags"]),
                is_public=True
            )
            
            db.add(kb_question)
            print(f"[KB] Added: {problem['title']} -> {skill.name}")
        
        db.commit()
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text"""
        
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        embedding = self.model.encode(text)
        self.embeddings_cache[text] = embedding
        return embedding
    
    def find_similar_problems(
        self,
        db: Session,
        query: str,
        skill_id: int = None,
        top_k: int = 3
    ) -> List[Dict]:
        """Find similar problems from knowledge base"""
        
        # Get embedding for query
        query_embedding = self.get_embedding(query)
        
        # Get all KB questions
        kb_questions = db.query(KnowledgeBaseQuestion).all()
        
        if not kb_questions:
            print(f"[RAG] No KB questions in database")
            return []
        
        # Calculate similarity for each problem
        similarities = []
        for kb_q in kb_questions:
            text = f"{kb_q.question_title} {kb_q.question_description or ''}"
            embedding = self.get_embedding(text)
            
            # Cosine similarity
            norm_q = np.linalg.norm(query_embedding)
            norm_kb = np.linalg.norm(embedding)
            
            if norm_q == 0 or norm_kb == 0:
                similarity = 0
            else:
                similarity = np.dot(query_embedding, embedding) / (norm_q * norm_kb)
            
            similarities.append({
                "problem": kb_q,
                "similarity": similarity
            })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top K
        results = [
            {
                "title": item["problem"].question_title,
                "description": item["problem"].question_description,
                "difficulty": item["problem"].difficulty_level,
                "similarity": float(item["similarity"])
            }
            for item in similarities[:top_k]
        ]
        
        print(f"[RAG] Found {len(results)} problems for '{query}'")
        for r in results:
            print(f"      - {r['title']} (sim: {r['similarity']:.2f})")
        
        return results