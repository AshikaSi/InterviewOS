# InterviewOS 🚀

## The Complete AI-Powered Adaptive Mock Interview Platform

**InterviewOS** is a production-ready, full-stack AI interview preparation platform that helps candidates practice and master technical, system design, and behavioral interviews through intelligent, adaptive questioning and real-time AI evaluation.

Built with modern technologies (FastAPI, Next.js, Google Gemini, RAG), InterviewOS provides a realistic interview experience with personalized feedback and adaptive difficulty that adjusts to your skill level.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features Explained](#features-explained)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [How to Use](#how-to-use)
7. [API Endpoints](#api-endpoints)
8. [How It Works](#how-it-works)
9. [Database Schema](#database-schema)
10. [Deployment](#deployment)
11. [Contributing](#contributing)
12. [License](#license)

---

## 🎯 Overview

InterviewOS is designed for engineering students and professionals preparing for competitive interviews at FAANG and other top tech companies. It combines artificial intelligence, machine learning, and proven interview preparation techniques to create a personalized interview coach.

**What Makes InterviewOS Different?**
- ✅ **AI-Powered**: Uses Google Gemini 3.6 to generate realistic questions
- ✅ **Adaptive**: Adjusts difficulty based on your real-time performance
- ✅ **Personalized**: Tailors questions to your resume and skill level
- ✅ **Comprehensive**: 3 interview types, 18+ skills, intelligent evaluation
- ✅ **Production-Ready**: Fully functional, tested, and deployable
- ✅ **Voice-Enabled**: Speak your answers and listen to questions
- ✅ **Beautiful UI**: Modern, intuitive, mobile-friendly interface

---

## ✨ Features Explained

### 🔐 1. User Authentication System

**What It Does:**
- Secure user registration and login
- JWT-based token authentication
- Password hashing with PBKDF2-SHA256
- Persistent sessions across browser refreshes

**How It Works:**


User Signs Up → Password Hashed → User Stored in DB → JWT Token Generated
↓
Token Stored in localStorage
↓
All API Requests Include Token


**Technical Details:**
- Uses `python-jose` for JWT generation/validation
- PBKDF2-SHA256 hashing ensures passwords are never stored in plain text
- Tokens expire after 30 minutes (access token)
- Refresh tokens valid for 7 days

**User Experience:**
- Sign up page with email validation
- Login with email/password
- Automatic logout after token expiration
- Seamless redirect to login if session expires

---

### 📊 2. Interview Session Management

**What It Does:**
- Creates and manages interview sessions
- Tracks session progress (questions answered, time spent)
- Maintains session state (ongoing, completed)
- Records all session metadata

**Features:**

#### Session Creation
- Choose interview type (Technical, System Design, Behavioral)
- Select difficulty (Easy, Medium, Hard)
- Optional resume upload for personalization
- 10-question default session length (configurable)

#### Session Tracking
- Real-time question counter (e.g., "Question 3/10")
- Timer for session duration
- Performance snapshot during interview
- Auto-save progress

#### Session Types

**Technical Q&A**
- Tests core computer science fundamentals
- Topics: Data Structures, Algorithms, DBMS, OS, Networks, OOP
- Format: Explain concepts, design solutions, discuss trade-offs
- Real-world examples from actual tech interviews

**System Design**
- Tests ability to design large-scale systems
- Topics: Requirements Analysis, API Design, Database Design, Caching, Scalability
- Format: Design systems like YouTube, Instagram, Uber
- Evaluates on architecture, trade-offs, scalability considerations

**Behavioral**
- Tests interpersonal skills and experiences
- Topics: Problem Solving, Collaboration, Learning, Time Management, Leadership
- Format: STAR method (Situation, Task, Action, Result)
- Evaluates on impact, communication, growth mindset

---

### 🤖 3. AI Question Generation (Gemini Integration)

**What It Does:**
- Generates contextual, realistic interview questions
- Creates unique questions each time (no repetition)
- Adapts questions based on skill level and performance
- Provides rubric for evaluation

**How It Works:**



Backend Receives Request
↓
Select Next Skill (Adaptive Policy)
↓
Find Similar Problems (RAG System)
↓
Build AI Prompt with Context
↓
Call Gemini 3.6 API
↓
Parse Response & Extract Question
↓
Return to Frontend
↓
Display to User


**AI Prompting Strategy:**
- **Context Injection**: Include similar problems from knowledge base
- **Format Specification**: Exact JSON format for parsing
- **Difficulty Hints**: Instructions like "basic concepts" or "complex edge cases"
- **Rubric Definition**: What to evaluate in answers

**Question Characteristics:**
- Realistic (based on actual interview questions)
- Focused (one clear problem per question)
- Progressive (difficulty adjusts based on answers)
- Educational (questions teach concepts)

**Example Prompt:**


You are an expert technical interviewer.
Generate a HARD question about Data Structures.

Similar real problems:

Two Sum (Medium, 60% solve rate)

LRU Cache (Hard, 30% solve rate)

Format your response as JSON:
{
"question": "Design an autocomplete feature...",
"rubric": {"correctness": 0, "depth": 0, "communication": 0}
}


---

### 🧠 4. Adaptive Intelligence Engine

**What It Does:**
- Tracks your mastery level for each skill
- Predicts your weakness areas
- Adjusts question difficulty in real-time
- Selects optimal next skill to practice

**Core Concepts:**

#### Elo-Like Mastery System


Each Skill Has:
├── Mastery: 0-1 (your estimated proficiency)
├── Uncertainty: 0-1 (confidence in estimate)
└── Evidence Count: number of questions answered


#### Mastery Updates


After Each Answer:

Evaluate performance (0-1 scale)

Calculate new mastery: new_mastery = old_mastery + learning_rate × (performance - old_mastery) where learning_rate = 0.5 / sqrt(evidence_count + 1)

Decrease uncertainty as evidence accumulates

Adjust difficulty for next question


**Learning Rate Explanation:**
- First answer: Learning rate = 0.5 (big changes)
- After 4 answers: Learning rate ≈ 0.22 (smaller changes)
- After 100 answers: Learning rate ≈ 0.05 (very small changes)

**Reason:** Early feedback shapes your path, later feedback refines your skill

#### Difficulty Adjustment Algorithm



If Performance ≥ 0.8:
Difficulty = Hard (you're doing great, time to challenge yourself)

If 0.6 ≤ Performance < 0.8:
Difficulty = Same (you're on track, maintain momentum)

If Performance < 0.6:
Difficulty = Easy (struggling, build confidence first)


#### Skill Selection Algorithm



For Each Skill, Calculate:
Score = Relevance × Weakness × Uncertainty_Factor

Example:
Data Structures (0.9 relevance, 0.3 mastery, high uncertainty)
Score = 0.9 × 0.7 × 1.2 = 0.756

Algorithms (0.9 relevance, 0.7 mastery, low uncertainty)
    Score = 0.9 × 0.3 × 0.5 = 0.135

→ Select Data Structures (higher score)



**Intelligent Features:**
- **Weakness Detection**: Identifies skills you struggle with
- **Uncertainty Tracking**: Knows which skills you're uncertain about
- **Optimal Path**: Selects skills in optimal learning order
- **Anti-Sandbagging**: Prevents easy questions even if you're weak (with intelligent difficulty)

---

### 📖 5. RAG System (Retrieval Augmented Generation)

**What It Does:**
- Maintains a knowledge base of real interview problems (Blind 75)
- Uses semantic similarity to find relevant problems
- Provides context to AI for more realistic questions
- Ensures generated questions align with actual interviews

**Components:**

#### Knowledge Base


Stores Problems With:
├── Title (e.g., "Two Sum")
├── Description (problem statement)
├── Difficulty (Easy/Medium/Hard)
├── Associated Skills
├── Topic Tags (array, hash, two-pointer, etc.)
└── Vector Embedding (semantic representation)


#### Semantic Similarity Search


When Generating Question for "Data Structures":

Get embedding for "Data Structures"

Compare with embeddings of all 75 problems

Calculate cosine similarity to each

Return top 3 most relevant problems

Example Results:
├── LRU Cache (0.87 similarity)
├── Contains Duplicate (0.84 similarity)
└── Valid Anagram (0.81 similarity)


#### Context Injection to AI


Prompt to Gemini:

"Generate a Data Structures question.

Similar Real Problems:

LRU Cache (Medium) - Design cache with get/put in O(1)

Contains Duplicate - Check if array has duplicates

Valid Anagram - Determine if strings are anagrams

Use these as inspiration for realistic question generation."


**Benefits:**
- Generated questions mirror actual interview problems
- AI has context of what's actually asked
- Questions match difficulty levels realistically
- Candidates practice with relevant problems

**Knowledge Base Source:**
- **Blind 75 LeetCode Questions**: Industry-standard interview prep list
- **18+ Coding Skills**: Organized by topic
- **Realistic Difficulty Distribution**: Matches actual interviews

---

### ⭐ 6. Answer Evaluation System

**What It Does:**
- Uses AI to evaluate your answers
- Provides instant feedback on strengths/weaknesses
- Scores based on configurable rubric
- Detects incorrect approaches early

**Evaluation Process:**



User Submits Answer
↓
Backend Sends to Gemini:
├── Original Question
├── User's Answer
├── Evaluation Rubric
↓
Gemini Returns:
├── Scores (0-4) for each rubric item
├── Overall Level (1-4)
├── Specific Feedback
↓
Frontend Displays Results


**Rubric Examples:**

For Technical Questions:


{
"correctness": (0-4) Does the approach solve the problem?
"depth": (0-4) Does it cover edge cases and optimizations?
"communication": (0-4) Can someone understand the explanation?
}


For System Design:


{
"api_design": (0-4) Are endpoints well-designed?
"database": (0-4) Is schema appropriate?
"scalability": (0-4) Will it handle scale?
"trade_offs": (0-4) Discussed important trade-offs?
}


For Behavioral:


{
"situation_clarity": (0-4) Story is clear?
"action_taken": (0-4) Shows good decision-making?
"result_impact": (0-4) Demonstrates impact?
"communication": (0-4) Answers naturally?
}


**Feedback Quality:**
- Specific (not just "good job")
- Actionable (what to improve)
- Encouraging (acknowledges strengths)
- Educational (teaches concepts)

**Example Feedback:**


Score: 3/4

Strengths:
✓ Correct use of HashMap for O(1) lookups
✓ Understood time complexity requirements
✓ Clear explanation of approach

Areas to Improve:
→ Didn't mention space complexity trade-offs
→ Could discuss alternative approaches (binary search, tree)
→ Edge cases: empty array, duplicate values

Next Steps:
Practice LRU Cache and similar design problems
Study hash table collision resolution


---

### 📊 7. Report Generation & Analytics

**What It Does:**
- Generates comprehensive performance reports
- Shows skill-by-skill breakdown
- Identifies strengths and weaknesses
- Creates personalized prep plans

**Report Contents:**

#### Overall Score


Displayed as: 3/4 stars
Calculation: Average of all answer scores
Range: 1-4
Interpretation:
├── 1 = Needs significant improvement
├── 2 = Below average, requires practice
├── 3 = Good, competitive level
└── 4 = Excellent, ready to interview


#### Skill Scores


Shows mastery for each skill:

Data Structures:    ████░░░░░░ 42%
Algorithms:         ██████░░░░ 65%
DBMS:               ████████░░ 82%
System Design:      ███░░░░░░░ 28%
...


#### Strengths & Weaknesses


Top Strengths:
✓ DBMS (82%) - Strong understanding of databases
✓ Algorithms (65%) - Good problem-solving approach
✓ Networks (71%) - Solid networking knowledge

Top Weaknesses:
→ System Design (28%) - Needs more experience
→ OOP (35%) - Review design patterns
→ Networks (39%) - Study network protocols


#### Personalized Prep Plan


Generated by AI based on your weaknesses:

WEEK 1: Foundation Building
├── Monday-Tuesday: System Design fundamentals (6 hrs)
├── Wednesday-Thursday: Design patterns (4 hrs)
├── Friday: Case study analysis (3 hrs)
├── Weekend: Review & practice (4 hrs)
└── Total: 17 hours

WEEK 2: Advanced Topics
├── Monday-Tuesday: Scalability patterns (5 hrs)
├── Wednesday-Thursday: Database design (4 hrs)
├── Friday: Mock interview (2 hrs)
├── Weekend: Review (3 hrs)
└── Total: 14 hours

Recommended Resources:

System Design Interview (Educative)

Designing Data-Intensive Applications (Book)

LeetCode System Design Problems


#### Session Metadata


Interview Duration: 47 minutes
Questions Completed: 10/10
Average Time per Question: 4.7 minutes
Questions by Difficulty:
├── Easy: 2 (avg score: 3.5)
├── Medium: 5 (avg score: 2.8)
└── Hard: 3 (avg score: 2.2)


---

### 🎙️ 8. Text-to-Speech (TTS) - Listen to Questions

**What It Does:**
- Reads interview questions aloud
- Uses browser's native speech synthesis
- Helps you practice listening comprehension
- Makes interviews more realistic

**How It Works:**


User Clicks "🔊 Hear" Button
↓
Browser's Web Speech API Activates
↓
Question Text Converted to Speech
↓
Audio Played Through Device Speakers
↓
User Hears Question Naturally


**Technical Details:**
- **API Used**: Web Speech Synthesis API (built into browsers)
- **No Server Overhead**: Entirely browser-based
- **Multiple Voices**: Can select different voice options
- **Speed Control**: Can adjust speech rate

**Benefits:**
- Practice listening to questions (interviews are verbal)
- Helps with auditory learning
- Catch details you might miss reading
- More realistic interview experience

**Limitations:**
- Voice quality varies by browser/OS
- Doesn't work in some older browsers
- Can't customize voice significantly

---

### 🎤 9. Speech-to-Text (STT) - Voice Input for Answers

**What It Does:**
- Records your voice while answering
- Converts speech to text
- Lets you practice speaking clearly
- More realistic interview practice

**How It Works:**


User Clicks "🎤 Speak" Button
↓
Browser Requests Microphone Access
↓
User Grants Permission
↓
Recording Starts (visual feedback)
↓
User Speaks Answer
↓
Click "🛑 Stop Recording" or Auto-Stop After 30 Seconds
↓
Browser's Web Speech Recognition API Processes Audio
↓
Speech Converted to Text
↓
Text Appears in Answer Field


**Technical Details:**
- **API Used**: Web Speech Recognition API
- **Language**: English (en-US) by default
- **Timeout**: Auto-stops after 30 seconds or no speech detected
- **Browser Support**: Chrome, Edge, Safari (limited)

**Benefits:**
- Practice speaking clearly and concisely
- Work on communication skills
- Time yourself while explaining
- More realistic than typing

**Limitations:**
- Browser must support Web Speech API
- Accuracy depends on microphone quality
- Background noise affects recognition
- Accents may affect accuracy

---

### 📄 10. Resume Upload & Skill Extraction

**What It Does:**
- Parse your resume (PDF, DOCX, TXT)
- Extract technical skills automatically
- Use extracted skills to personalize questions
- Show you what skills InterviewOS detected

**Features:**

#### Resume Parsing


Upload Resume (PDF/DOCX/TXT)
↓
Extract Raw Text
↓
AI Analyzes to Find Skills
↓
Categorize Skills:
├── Languages (Python, Java, C++)
├── Frameworks (React, FastAPI, Django)
├── Databases (PostgreSQL, MongoDB)
├── Tools (Docker, Kubernetes, Git)
└── Other (REST APIs, Microservices)
↓
Display Extracted Skills to User
↓
Send to Interview Session


#### Skill Personalization


Example Resume Contains: Python, Docker, FastAPI

Interview System Maps To:
├── Python → Boost Algorithms, Data Structures
├── FastAPI → Boost System Design, APIs
└── Docker → Boost DevOps, Scalability

Result:

Questions about Python/algorithms asked first

Easier questions on unfamiliar topics

Personalized difficulty adjustment


#### Resume Display


✨ Resume Analyzed!

Extracted Skills:
[Python] [Docker] [FastAPI] [React] [PostgreSQL]
[REST APIs] [Microservices] [Linux] [Git]

We'll focus on skills you know and help you
master areas you're less familiar with.


**Supported Formats:**
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Plain Text (.txt)

**Privacy:**
- Resume deleted after session ends
- Never stored permanently
- Used only for skill extraction

---

### 📱 11. Beautiful, Modern UI

**Design Philosophy:**
- Minimalist, clean interface
- Focus on content (questions)
- Intuitive navigation
- Mobile-responsive

**Key Pages:**

**Login/Signup**
- Gradient background (blue to indigo)
- Smooth form validation
- Social login ready
- Password strength indicator

**Dashboard**
- Stats cards (interviews completed, average score, improvement)
- Quick action buttons
- Interview history
- Recent achievements

**Interview Setup**
- Large, readable options
- Resume upload with drag-and-drop
- Visual difficulty selector
- Mode description

**Interview Room**
- Question prominently displayed
- Audio controls (Hear button)
- Large text area for answers
- Voice input button
- Clear submit button
- Timer and progress indicator

**Reports**
- Large score display
- Colorful skill charts
- Strength/weakness highlights
- Actionable recommendations

---

### 🔒 12. Security Features

**Authentication:**
- JWT tokens (secure, stateless)
- PBKDF2-SHA256 password hashing
- Token expiration (30 min access, 7 day refresh)

**Data Protection:**
- HTTPS-only in production
- CORS protection
- Environment variables for secrets
- .gitignore prevents credential leaks

**Privacy:**
- Minimal data collection
- Resumes deleted after use
- No third-party tracking
- Transparent privacy policy

---

## 🛠️ Tech Stack

### Backend (Python)

**Framework & Server**
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server, supports async operations

**Database & ORM**
- **SQLAlchemy**: Industry-standard ORM
- **SQLite**: Development database (easy, no setup)
- **PostgreSQL**: Production option (scalable)

**AI & NLP**
- **Google Gemini 3.6**: Question generation & evaluation
- **Sentence Transformers**: Embeddings for RAG
- **PyPDF2 & python-docx**: Resume parsing

**Authentication & Security**
- **python-jose**: JWT token management
- **passlib**: Password hashing
- **PBKDF2-SHA256**: Secure hashing algorithm

**API & Communication**
- **Pydantic**: Data validation
- **CORS Middleware**: Cross-origin requests

### Frontend (JavaScript/TypeScript)

**Framework & Build**
- **Next.js 16**: React framework with SSR, API routes
- **React 19**: UI components
- **TypeScript**: Type safety

**Styling & UI**
- **Tailwind CSS**: Utility-first CSS framework
- **CSS Grid/Flexbox**: Responsive layouts

**HTTP & API**
- **Axios**: HTTP client for API calls
- **Fetch API**: Native browser API (backup)

**Browser APIs**
- **Web Speech Recognition**: Speech-to-Text
- **Web Speech Synthesis**: Text-to-Speech
- **MediaRecorder API**: Audio recording

**State & Storage**
- **React Hooks**: State management (useState, useEffect)
- **localStorage**: Client-side persistence

---

## 📂 Project Structure



InterviewOS/
│
├── backend/
│   ├── main.py                          # FastAPI app entry point
│   ├── config.py                        # Settings & environment
│   ├── database.py                      # Database connection & session
│   │
│   ├── models.py                        # SQLAlchemy database models
│   │   ├── User                         # User accounts
│   │   ├── InterviewSession             # Interview metadata
│   │   ├── InterviewQuestion            # Questions asked
│   │   ├── CandidateAnswer              # User responses
│   │   ├── Evaluation                   # AI evaluation results
│   │   ├── Skill                        # Available skills
│   │   ├── CandidateSkillProfile        # User skill levels
│   │   ├── KnowledgeBaseQuestion        # Blind 75 problems
│   │   ├── InterviewReport              # Generated reports
│   │   └── CandidateResume              # Uploaded resumes
│   │
│   ├── schemas.py                       # Pydantic validation models
│   │   ├── UserCreate, UserResponse     # User schemas
│   │   ├── InterviewCreate, InterviewResponse
│   │   ├── EvaluationResponse
│   │   └── ReportResponse
│   │
│   ├── auth.py                          # Authentication utilities
│   │   ├── hash_password()              # Password hashing
│   │   ├── verify_password()            # Password verification
│   │   ├── create_access_token()        # JWT generation
│   │   └── decode_token()               # JWT validation
│   │
│   ├── auth_routes.py                   # Authentication endpoints
│   │   ├── POST /api/auth/signup        # Register new user
│   │   ├── POST /api/auth/login         # Login user
│   │   └── GET /api/auth/me             # Get current user
│   │
│   ├── interview_routes.py              # Interview endpoints
│   │   ├── POST /api/sessions/create    # Start interview
│   │   ├── GET /api/sessions/{id}       # Get session
│   │   ├── GET /api/sessions/{id}/question     # Get next question
│   │   ├── POST /api/sessions/{id}/submit-answer   # Submit answer
│   │   ├── POST /api/sessions/{id}/end          # End interview
│   │   ├── GET /api/sessions/{id}/report        # Get report
│   │   └── POST /api/resume/parse               # Parse resume
│   │
│   ├── interview_service.py             # Interview logic
│   │   ├── create_interview()           # Session initialization
│   │   ├── generate_question()          # Get next question
│   │   ├── submit_answer()              # Process answer
│   │   └── end_interview()              # Finalize session
│   │
│   ├── llm_service.py                   # AI integration (Gemini)
│   │   ├── InterviewerAgent             # Question generation
│   │   │   ├── generate_question()      # Create questions
│   │   │   ├── _build_technical_prompt()
│   │   │   ├── _build_system_design_prompt()
│   │   │   └── _build_behavioral_prompt()
│   │   ├── EvaluatorAgent               # Answer evaluation
│   │   │   └── evaluate_answer()        # Score answers
│   │   └── PlannerAgent                 # Prep plan generation
│   │       └── generate_prep_plan()     # Create study plans
│   │
│   ├── adaptive_policy.py               # Adaptive algorithm
│   │   ├── select_next_skill()          # Choose skill via weighted score
│   │   ├── update_mastery()             # Elo-like updates
│   │   └── adjust_difficulty()          # Difficulty logic
│   │
│   ├── skills_service.py                # Skill management
│   │   ├── init_skills()                # Create default skills
│   │   ├── seed_candidate_profiles()    # Initialize user skills
│   │   └── get_skill_profile()          # Get user skill
│   │
│   ├── knowledge_base_service.py        # RAG system
│   │   ├── seed_knowledge_base()        # Load Blind 75
│   │   ├── get_embedding()              # Get vector embedding
│   │   └── find_similar_problems()      # Semantic search
│   │
│   ├── report_service.py                # Report generation
│   │   ├── generate_report()            # Create full report
│   │   ├── calculate_scores()           # Score calculation
│   │   └── generate_prep_plan()         # Study recommendations
│   │
│   ├── resume_parser.py                 # Resume processing
│   │   ├── extract_text_from_pdf()      # PDF parsing
│   │   ├── extract_text_from_docx()     # Word parsing
│   │   └── extract_skills()             # Skill extraction (AI)
│   │
│   ├── stt_service.py                   # Speech-to-text
│   │   └── transcribe_audio()           # Audio processing
│   │
│   ├── requirements.txt                 # Python dependencies
│   └── .env                             # Environment variables (not in git)
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx                     # Home page
│   │   ├── layout.tsx                   # Root layout
│   │   │
│   │   ├── login/
│   │   │   └── page.tsx                 # Login form
│   │   │       ├── Email input
│   │   │       ├── Password input
│   │   │       ├── Sign up link
│   │   │       └── Submit button
│   │   │
│   │   ├── signup/
│   │   │   └── page.tsx                 # Registration form
│   │   │       ├── Full name input
│   │   │       ├── Email input
│   │   │       ├── Password input
│   │   │       ├── Login link
│   │   │       └── Submit button
│   │   │
│   │   ├── dashboard/
│   │   │   └── page.tsx                 # Main dashboard
│   │   │       ├── Stats cards
│   │   │       ├── Interview history
│   │   │       ├── Start interview button
│   │   │       ├── User profile
│   │   │       └── Logout button
│   │   │
│   │   ├── interview/
│   │   │   ├── setup/
│   │   │   │   └── page.tsx             # Interview configuration
│   │   │   │       ├── Resume upload
│   │   │   │       ├── Mode selection
│   │   │   │       ├── Difficulty selection
│   │   │   │       └── Start button
│   │   │   │
│   │   │   └── [id]/
│   │   │       └── page.tsx             # Interview room
│   │   │           ├── Question display
│   │   │           ├── Audio controls (🔊 Hear)
│   │   │           ├── Answer textarea
│   │   │           ├── Voice input (🎤 Speak)
│   │   │           ├── Submit button
│   │   │           ├── End interview button
│   │   │           └── Results/Report display
│   │   │
│   │   ├── lib/
│   │   │   └── api.ts                   # API client
│   │   │       ├── signup()             # Auth endpoints
│   │   │       ├── login()
│   │   │       ├── getSession()         # Session endpoints
│   │   │       ├── createSession()
│   │   │       ├── getQuestion()
│   │   │       ├── submitAnswer()
│   │   │       ├── endSession()
│   │   │       ├── getReport()
│   │   │       └── healthCheck()
│   │   │
│   │   └── globals.css                  # Global styles
│   │
│   ├── package.json                     # Node dependencies
│   ├── tsconfig.json                    # TypeScript config
│   ├── next.config.js                   # Next.js config
│   └── tailwind.config.js               # Tailwind config
│
├── README.md                            # This file
├── .gitignore                           # Git ignore rules
└── LICENSE                              # MIT License


---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.14+ (Windows/Mac/Linux)
- Node.js 18+ (for frontend)
- Git

### Backend Setup

**1. Clone and Navigate**
```bash
git clone https://github.com/AshikaSi/InterviewOS.git
cd InterviewOS/backend


2. Create Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install fastapi uvicorn sqlalchemy pydantic google-genai sentence-transformers PyPDF2 python-docx python-dotenv python-jose passlib


4. Create .env File

notepad .env
# or nano .env (Mac/Linux)


Add:

GEMINI_API_KEY=your_api_key_here
CORS_ORIGINS=["http://localhost:3000"]


Get Gemini API key: https://ai.google.dev

5. Run Backend

python main.py


Backend runs on: http://localhost:8000

Frontend Setup

1. Navigate to Frontend

cd ../frontend


2. Install Dependencies

npm install


3. Run Frontend

npm run dev


Frontend runs on: http://localhost:3000

Access the Application

Sign Up: http://localhost:3000/signup
Login: http://localhost:3000/login
Dashboard: http://localhost:3000/dashboard
API Docs: http://localhost:8000/docs

📖 How to Use

Step-by-Step Guide

1. Create Account

Go to http://localhost:3000/signup

Enter email, password, full name

Account created, auto-redirected to dashboard

2. Dashboard Overview

See stats: total interviews, average score, improvement %

View interview history

Click "Start Interview" to begin

3. Interview Setup

Choose interview type: Technical / System Design / Behavioral

Choose difficulty: Easy / Medium / Hard

(Optional) Upload resume for personalization

Click "🚀 Start Interview"

4. During Interview

Read question or click "🔊 Hear" to listen

Type your answer or click "🎤 Speak" to use voice

Click "Submit Answer" when done

Get instant AI evaluation and feedback

Proceed to next question

5. After Interview

See overall score (1-4 stars)

View skill-by-skill breakdown

Identify strengths and weaknesses

Get personalized 2-week prep plan

Click "Practice Again" for another interview

🔌 API Endpoints

Base URL: http://localhost:8000

Authentication

POST   /api/auth/signup              Create account
POST   /api/auth/login               Login
GET    /api/auth/me                  Get current user


Interviews

POST   /api/sessions/create          Start new interview
GET    /api/sessions/{id}            Get session details
GET    /api/sessions/{id}/question   Get next question
POST   /api/sessions/{id}/submit-answer   Submit answer
POST   /api/sessions/{id}/end        End interview
GET    /api/sessions/{id}/report     Get performance report


Resume & Skills

POST   /api/resume/parse             Parse & extract from resume
POST   /api/sessions/{id}/seed-skills    Initialize skills from resume


Health

GET    /api/health                   Check API health


Interactive Docs: http://localhost:8000/docs

🧠 How It Works

Interview Flow Diagram

User Starts Interview
         ↓
┌─────────────────────────────────────────────┐
│  ADAPTIVE INTELLIGENCE LAYER                │
│  ├─ Select Next Skill (Adaptive Policy)     │
│  ├─ Determine Difficulty                    │
│  └─ Track Mastery Updates                   │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│  QUESTION GENERATION LAYER                  │
│  ├─ Find Similar Problems (RAG)             │
│  ├─ Build AI Prompt                         │
│  ├─ Call Gemini API                         │
│  └─ Parse Response                          │
└─────────────────────────────────────────────┘
         ↓
Question Displayed to User
         ↓
User Submits Answer (Text or Voice)
         ↓
┌─────────────────────────────────────────────┐
│  EVALUATION LAYER                           │
│  ├─ Send to Gemini API                      │
│  ├─ Score on Rubric                         │
│  ├─ Generate Feedback                       │
│  └─ Update Skill Mastery                    │
└─────────────────────────────────────────────┘
         ↓
Feedback Displayed to User
         ↓
Repeat or End Interview
         ↓
┌─────────────────────────────────────────────┐
│  REPORT GENERATION LAYER                    │
│  ├─ Calculate Overall Score                 │
│  ├─ Generate Skill Breakdown                │
│  ├─ Identify Strengths/Weaknesses           │
│  └─ Create 2-Week Prep Plan                 │
└─────────────────────────────────────────────┘
         ↓
Report Displayed to User


Data Flow in System

FRONTEND                          BACKEND                         EXTERNAL

User Input ──────────────────→ FastAPI Router
   ↓                             ↓
   │                        Database Query
   │                             ↓
   │                        Business Logic
   │                             ↓
   │                        Gemini API Call ──────────→ Google Gemini
   │                             ↓
   │                        Response Parse
   │                             ↓
Response Output ←──────────────────

LocalStorage                     SQLite/PostgreSQL
(Tokens)                         (Persistent Data)


📊 Database Schema

Users Table

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL,
  username VARCHAR,
  full_name VARCHAR,
  is_active BOOLEAN,
  created_at DATETIME,
  updated_at DATETIME
);


Interview Sessions

CREATE TABLE interview_sessions (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY,
  mode VARCHAR,                    -- technical_qa, system_design, behavioral
  difficulty VARCHAR,              -- easy, medium, hard
  status VARCHAR,                  -- ongoing, completed
  turn_count INTEGER,
  turn_budget INTEGER,             -- 10 questions default
  started_at DATETIME,
  completed_at DATETIME
);


Questions & Answers

CREATE TABLE interview_questions (
  id INTEGER PRIMARY KEY,
  session_id INTEGER FOREIGN KEY,
  turn_number INTEGER,
  question_text TEXT,
  rubric_json JSON                -- Evaluation criteria
);

CREATE TABLE candidate_answers (
  id INTEGER PRIMARY KEY,
  question_id INTEGER FOREIGN KEY,
  answer_text TEXT,
  answered_at DATETIME
);


Evaluations

CREATE TABLE evaluations (
  id INTEGER PRIMARY KEY,
  answer_id INTEGER FOREIGN KEY,
  overall_level INTEGER,          -- 1-4
  feedback TEXT,
  scores_json JSON,               -- Individual rubric scores
  created_at DATETIME
);


Skills Tracking

CREATE TABLE skills (
  id INTEGER PRIMARY KEY,
  name VARCHAR,                   -- Data Structures, Algorithms, etc.
  mode VARCHAR                    -- technical_qa, system_design, behavioral
);

CREATE TABLE candidate_skill_profiles (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY,
  session_id INTEGER FOREIGN KEY,
  skill_id INTEGER FOREIGN KEY,
  mastery FLOAT,                  -- 0-1
  uncertainty FLOAT,              -- 0-1
  evidence_count INTEGER,         -- Questions answered
  created_at DATETIME
);


Knowledge Base

CREATE TABLE knowledge_base_questions (
  id INTEGER PRIMARY KEY,
  source VARCHAR,                 -- blind_75
  skill_id INTEGER FOREIGN KEY,
  question_title VARCHAR,
  question_description TEXT,
  difficulty_level VARCHAR,
  topic_tags VARCHAR,             -- comma-separated
  is_public BOOLEAN,
  created_at DATETIME
);


Reports

CREATE TABLE interview_reports (
  id INTEGER PRIMARY KEY,
  session_id INTEGER FOREIGN KEY,
  user_id INTEGER FOREIGN KEY,
  overall_score INTEGER,          -- 1-4
  duration_seconds INTEGER,
  skill_scores_json JSON,
  top_3_weaknesses_json JSON,
  strengths_json JSON,
  prep_plan_json JSON,
  created_at DATETIME
);


🌐 Deployment

Deploy Backend (Railway)

1. Push to GitHub

git push origin main


2. Connect Railway

Sign up at railway.app

Create new project

Connect GitHub repo

Set environment variables

Auto-deploys on push

3. Database Setup

# Use PostgreSQL on Railway
# Update DATABASE_URL in environment


Deploy Frontend (Vercel)

1. Connect Repository

Sign up at vercel.com

Import GitHub repo

Auto-detects Next.js

2. Environment Variables

NEXT_PUBLIC_API_URL=https://your-railway-app.up.railway.app


3. Deploy

Auto-deploys on main push

Custom domain setup available

Domain & SSL

Frontend: yourdomain.com (Vercel)
Backend: api.yourdomain.com (Railway)
Both: Auto HTTPS with Vercel


🤝 Contributing

This is a personal project showcasing full-stack development capabilities. Feedback and suggestions are welcome!

To Contribute:

Fork the repository

Create a feature branch

Make improvements

Submit a pull request

Engage in discussion

Areas for Contribution:

Additional interview types

More skills in knowledge base

UI/UX improvements

Performance optimization

Testing & bug fixes

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

You are free to:

Use commercially

Modify the code

Distribute copies

Use privately

You must:

Include the license

State changes made

👤 Author

Ashika Singh

🎓 IIT Dhanbad Student

💻 Full-Stack Developer

📧 ashikasinghiitdhn@gmail.com

🔗 GitHub: @AshikaSi

🎯 Future Roadmap

Phase 2 Features:

Video recording with playback

Peer mock interviews (multiplayer)

Global leaderboards

Interview scheduling

Mobile native app

Spaced repetition system

Topic-based practice paths

Interview company-specific questions

Technical Improvements:

PostgreSQL migration

Redis caching layer

WebSocket for real-time features

Kubernetes deployment

CI/CD pipeline

Monitoring & analytics

📚 Resources

Interview Preparation:

Blind 75 LeetCode

System Design Primer
