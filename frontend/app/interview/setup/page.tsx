"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createSession } from "@/app/lib/api";
import Link from "next/link";

export default function SetupPage() {
  const [mode, setMode] = useState("technical_qa");
  const [difficulty, setDifficulty] = useState("medium");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleStartInterview(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await createSession(mode, difficulty);
      
      if (result.id) {
        router.push(`/interview/${result.id}`);
      } else {
        setError("Failed to create session");
      }
    } catch (err) {
      setError("Error starting interview");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <Link href="/dashboard" className="text-2xl font-bold text-gray-900">
            InterviewOS
          </Link>
          <Link href="/dashboard" className="text-blue-600 hover:underline">
            Back to Dashboard
          </Link>
        </div>
      </header>

      {/* Setup Form */}
      <main className="max-w-2xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Start Interview</h1>

          <form onSubmit={handleStartInterview} className="space-y-6">
            {/* Interview Mode */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">Interview Mode</label>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="technical_qa"
                    checked={mode === "technical_qa"}
                    onChange={(e) => setMode(e.target.value)}
                    className="w-4 h-4"
                  />
                  <span className="ml-3 text-gray-700">
                    <strong>Technical Q&A</strong> - DSA, DBMS, OS, Networks
                  </span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="system_design"
                    checked={mode === "system_design"}
                    onChange={(e) => setMode(e.target.value)}
                    className="w-4 h-4"
                  />
                  <span className="ml-3 text-gray-700">
                    <strong>System Design</strong> - Large-scale system design
                  </span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="behavioral"
                    checked={mode === "behavioral"}
                    onChange={(e) => setMode(e.target.value)}
                    className="w-4 h-4"
                  />
                  <span className="ml-3 text-gray-700">
                    <strong>Behavioral</strong> - STAR format questions
                  </span>
                </label>
              </div>
            </div>

            {/* Difficulty */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">Difficulty Level</label>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="easy"
                    checked={difficulty === "easy"}
                    onChange={(e) => setDifficulty(e.target.value)}
                    className="w-4 h-4"
                  />
                  <span className="ml-3 text-gray-700">Easy</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="medium"
                    checked={difficulty === "medium"}
                    onChange={(e) => setDifficulty(e.target.value)}
                    className="w-4 h-4"
                  />
                  <span className="ml-3 text-gray-700">Medium (Recommended)</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="radio"
                    value="hard"
                    checked={difficulty === "hard"}
                    onChange={(e) => setDifficulty(e.target.value)}
                    className="w-4 h-4"
                  />
                  <span className="ml-3 text-gray-700">Hard</span>
                </label>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 transition"
            >
              {loading ? "Starting..." : "Start Interview"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}