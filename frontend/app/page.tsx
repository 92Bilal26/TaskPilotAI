'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function Home() {
  const router = useRouter()
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)

    // Check if user is authenticated
    const token = localStorage.getItem('auth_token')

    if (token) {
      // User is logged in, go to dashboard
      router.push('/dashboard')
    }
    // If not authenticated, show the welcome page
  }, [router])

  // Don't render anything until client is mounted to avoid hydration mismatch
  if (!isMounted) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-600">TaskPilot AI 🤖</h1>
            <div className="flex gap-4">
              <Link
                href="/auth/signin"
                className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg font-medium transition"
              >
                Sign In
              </Link>
              <Link
                href="/auth/signup"
                className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition"
              >
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            AI-Powered Task Management
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Chat with your AI assistant to create, manage, and complete tasks.
            No complicated interfaces—just natural language commands.
          </p>

          <div className="flex gap-4 justify-center mb-12">
            <Link
              href="/test-chatbot"
              className="px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition shadow-lg"
            >
              Try Demo Chatbot 🚀
            </Link>
            <Link
              href="/auth/signin"
              className="px-8 py-4 bg-white text-blue-600 text-lg font-semibold rounded-lg border-2 border-blue-600 hover:bg-blue-50 transition"
            >
              Sign In
            </Link>
          </div>

          {/* Features */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">💬</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Natural Language
              </h3>
              <p className="text-gray-600">
                Just talk to your AI assistant. Say "Add a task to buy groceries"
                and it will do it for you.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Powered by OpenAI
              </h3>
              <p className="text-gray-600">
                Uses GPT-4 Turbo for intelligent understanding and autonomous
                tool selection.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Smart Execution
              </h3>
              <p className="text-gray-600">
                AI automatically selects the right tool to handle your request—
                no manual routing needed.
              </p>
            </div>
          </div>

          {/* Demo Instructions */}
          <div className="mt-16 bg-white p-8 rounded-lg shadow-md max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Try These Commands
            </h3>
            <div className="space-y-3 text-left">
              <div className="flex items-start gap-3">
                <span className="text-2xl">➕</span>
                <div>
                  <p className="font-semibold text-gray-900">Create Tasks</p>
                  <p className="text-sm text-gray-600">
                    "Add a task to buy groceries for dinner"
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="text-2xl">📋</span>
                <div>
                  <p className="font-semibold text-gray-900">List Tasks</p>
                  <p className="text-sm text-gray-600">
                    "Show me all my pending tasks"
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="text-2xl">✨</span>
                <div>
                  <p className="font-semibold text-gray-900">Complete Tasks</p>
                  <p className="text-sm text-gray-600">
                    "Mark task 1 as complete"
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="text-2xl">✏️</span>
                <div>
                  <p className="font-semibold text-gray-900">Update Tasks</p>
                  <p className="text-sm text-gray-600">
                    "Change task 2 title to weekend shopping"
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="text-2xl">🗑️</span>
                <div>
                  <p className="font-semibold text-gray-900">Delete Tasks</p>
                  <p className="text-sm text-gray-600">
                    "Remove the groceries task"
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="mt-12">
            <Link
              href="/test-chatbot"
              className="inline-block px-10 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-lg font-bold rounded-lg hover:shadow-lg transition"
            >
              🚀 Start Chatting Now (No Sign-Up Required!)
            </Link>
            <p className="text-gray-600 mt-4">
              Or{' '}
              <Link href="/auth/signin" className="text-blue-600 hover:underline">
                sign in
              </Link>{' '}
              to your account
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>
            TaskPilotAI Phase 3 - AI-Powered Todo Chatbot with OpenAI
            Integration
          </p>
        </div>
      </footer>
    </div>
  )
}
