/**
 * ChatKit Page
 *
 * Integrates OpenAI's ChatKit React component for AI task management
 * Uses the official @openai/chatkit-react package via ChatKitWidget wrapper
 */

'use client'

import { ChatKitWidget } from '@/components/ChatKit'

export default function ChatKitPage() {
  return (
    <ChatKitWidget
      showHeader={true}
      title="TaskPilot AI Chat"
      subtitle="Powered by OpenAI ChatKit"
      showBackButton={true}
      backRoute="/dashboard"
    />
  )
}
