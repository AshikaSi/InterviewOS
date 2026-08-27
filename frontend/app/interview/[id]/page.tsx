"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter, useParams } from "next/navigation";
import {
  getSession,
  getQuestion,
  submitAnswer,
  endSession,
  getReport,
} from "@/app/lib/api";
import Link from "next/link";
import axios from "axios";

interface Question {
  id: number;
  question_text: string;
  turn_number: number;
  rubric_json: string;
}

interface Evaluation {
  overall_level: number;
  feedback: string;
}

interface Report {
  overall_score: number;
  duration_seconds: number;
  skill_scores: Record<string, number>;
  top_3_weaknesses: string[];
  strengths: string[];
}

export default function InterviewPage() {
  const params = useParams();
  const sessionId = params.id as string;
  const router = useRouter();

  // All state inside component
  const [session, setSession] = useState<any>(null);
  const [question, setQuestion] = useState<Question | null>(null);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [report, setReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(false);
  const [phase, setPhase] = useState<
    "loading" | "question" | "evaluating" | "completed"
  >("loading");
  const [error, setError] = useState("");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState<BlobPart[]>([]);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Load session and first question
  useEffect(() => {
    async function loadSession() {
      try {
        const sessionData = await getSession(parseInt(sessionId));
        setSession(sessionData);

        const questionData = await getQuestion(parseInt(sessionId));
        setQuestion(questionData);

        setPhase("question");
      } catch (err) {
        setError("Failed to load session");
        setPhase("loading");
      }
    }

    loadSession();
  }, [sessionId]);

  // Text-to-Speech function
  function handlePlayAudio() {
    if (!question) return;

    setIsPlayingAudio(true);

    try {
      const utterance = new SpeechSynthesisUtterance(question.question_text);

      utterance.rate = 1;
      utterance.pitch = 1;
      utterance.volume = 1;

      utterance.onend = () => {
        setIsPlayingAudio(false);
      };

      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    } catch (err) {
      setError("Failed to play audio");
      setIsPlayingAudio(false);
    }
  }

  // Voice recording function
  async function handleVoiceInput() {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError("Speech Recognition not supported. Please type your answer.");
      return;
    }

    if (isRecording) {
      setIsRecording(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";

      setIsRecording(true);
      setError("");
      let transcript = "";

      recognition.onstart = () => {
        console.log("Listening...");
      };

      recognition.onresult = (event: any) => {
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript + " ";
        }

        if (transcript) {
          setAnswer(transcript.trim());
        }
      };

      recognition.onerror = (event: any) => {
        console.log("Error:", event.error);
        if (event.error !== "no-speech") {
          setError(`Speech recognition: ${event.error}`);
        }
      };

      recognition.onend = () => {
        setIsRecording(false);
        console.log("Recording stopped");
      };

      recognition.start();
    } catch (err) {
      setError("Microphone error. Please check permissions.");
      setIsRecording(false);
    }
  }

  // Submit answer
  async function handleSubmitAnswer() {
    if (!answer.trim()) {
      setError("Please provide an answer");
      return;
    }

    setLoading(true);
    setError("");
    setPhase("evaluating");

    try {
      const evaluation = await submitAnswer(
        parseInt(sessionId),
        question!.id,
        answer
      );

      setEvaluation(evaluation);

      if (session.turn_count + 1 >= session.turn_budget) {
        const reportData = await getReport(parseInt(sessionId));

        setReport(reportData);
        setPhase("completed");
      } else {
        setTimeout(() => {
          handleNextQuestion();
        }, 2000);
      }
    } catch (err) {
      setError("Error submitting answer");
      setPhase("question");
    } finally {
      setLoading(false);
    }
  }

  // Get next question
  async function handleNextQuestion() {
    try {
      const questionData = await getQuestion(parseInt(sessionId));

      setQuestion(questionData);
      setAnswer("");
      setEvaluation(null);
      setPhase("question");
    } catch (err) {
      setError("Failed to load next question");
    }
  }

  // End interview early
  async function handleEndInterview() {
    if (confirm("Are you sure you want to end the interview?")) {
      try {
        await endSession(parseInt(sessionId));

        const reportData = await getReport(parseInt(sessionId));

        setReport(reportData);
        setPhase("completed");
      } catch (err) {
        setError("Error ending interview");
      }
    }
  }

  if (phase === "loading") {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-lg text-gray-600">Loading interview...</p>
        </div>
      </div>
    );
  }

  if (phase === "completed" && report) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="max-w-4xl mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              Interview Complete!
            </h1>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 py-12">
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <div className="text-center mb-8">
              <p className="text-gray-600 text-sm font-medium mb-2">
                Overall Score
              </p>

              <p className="text-6xl font-bold text-blue-600">
                {report.overall_score}/4
              </p>
            </div>

            <div className="text-center mb-8">
              <p className="text-gray-600">
                Duration: {Math.floor(report.duration_seconds / 60)} minutes
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div>
                <h3 className="font-bold text-gray-900 mb-4">Strengths</h3>

                <ul className="space-y-2">
                  {report.strengths.map((skill, i) => (
                    <li key={i} className="text-green-600">
                      ✓ {skill}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-bold text-gray-900 mb-4">
                  Areas to Improve
                </h3>

                <ul className="space-y-2">
                  {report.top_3_weaknesses.map((skill, i) => (
                    <li key={i} className="text-orange-600">
                      → {skill}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="mb-8">
              <h3 className="font-bold text-gray-900 mb-4">Skill Scores</h3>

              <div className="space-y-3">
                {Object.entries(report.skill_scores).map(([skill, score]) => (
                  <div key={skill}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-700">{skill}</span>

                      <span className="text-gray-600">
                        {((score as number) * 100).toFixed(0)}%
                      </span>
                    </div>

                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{
                          width: `${(score as number) * 100}%`,
                        }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <Link
              href="/dashboard"
              className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition text-center"
            >
              Back to Dashboard
            </Link>

            <Link
              href="/interview/setup"
              className="flex-1 bg-green-600 text-white py-3 rounded-lg font-medium hover:bg-green-700 transition text-center"
            >
              Practice Again
            </Link>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-4xl mx-auto px-4 py-6 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">InterviewOS</h1>

            <p className="text-gray-600 text-sm">
              Question {question?.turn_number}/{session?.turn_budget}
            </p>
          </div>

          <button
            onClick={handleEndInterview}
            className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
          >
            End Interview
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-12">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {phase === "question" && question && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex justify-between items-start gap-4 mb-6">
                <h2 className="text-2xl font-bold text-gray-900">
                  {question.question_text}
                </h2>

                <button
                  onClick={handlePlayAudio}
                  disabled={isPlayingAudio}
                  className="whitespace-nowrap bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
                >
                  {isPlayingAudio ? "🔊 Playing..." : "🔊 Hear"}
                </button>
              </div>

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSubmitAnswer();
                }}
              >
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Answer
                  </label>

                  <textarea
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                    rows={8}
                    disabled={loading || isRecording}
                  />
                </div>

                <div className="flex gap-4 mb-4">
                  <button
                    type="button"
                    onClick={handleVoiceInput}
                    disabled={loading}
                    className={`flex-1 px-4 py-2 rounded-lg font-medium transition ${
                      isRecording
                        ? "bg-red-600 text-white hover:bg-red-700"
                        : "bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-400"
                    }`}
                  >
                    {isRecording ? "🛑 Stop Recording" : "🎤 Speak"}
                  </button>
                  {loading && (
                    <p className="text-gray-600 text-sm">Transcribing...</p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={loading || !answer.trim()}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition"
                >
                  {loading ? "Evaluating..." : "Submit Answer"}
                </button>
              </form>
            </div>
          </div>
        )}

        {phase === "evaluating" && evaluation && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Evaluation
              </h3>

              <div className="bg-blue-50 rounded-lg p-6 mb-6">
                <p className="text-5xl font-bold text-blue-600 mb-2">
                  {evaluation.overall_level}/4
                </p>

                <p className="text-gray-700">{evaluation.feedback}</p>
              </div>

              <p className="text-gray-600">Loading next question...</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}