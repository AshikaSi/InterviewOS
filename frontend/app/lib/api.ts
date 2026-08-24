const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Auth APIs
export async function signup(email: string, password: string, fullName: string) {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
  return response.json();
}

export async function login(email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
}

// Session APIs
export async function createSession(mode: string, difficulty: string, company?: string) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode, difficulty, company }),
  });
  return response.json();
}

export async function getSession(sessionId: number) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`);
  return response.json();
}

export async function getQuestion(sessionId: number) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/question`);
  return response.json();
}

export async function submitAnswer(sessionId: number, questionId: number, answer: string) {
  const response = await fetch(
    `${API_BASE_URL}/api/sessions/${sessionId}/submit-answer?question_id=${questionId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answer_text: answer }),
    }
  );
  return response.json();
}

export async function endSession(sessionId: number) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/end`, {
    method: "POST",
  });
  return response.json();
}

export async function getReport(sessionId: number) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/report`);
  return response.json();
}

export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  return response.json();
}