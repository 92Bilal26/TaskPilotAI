'use client'

import { Button } from '@/components/ui'

interface HeaderActionsProps {
  showChatKit: boolean
  onToggleChatKit: () => void
  onNewTask: () => void
}

/**
 * Header Actions Component
 * Separated to avoid hydration issues with inline JSX in props
 */
export function HeaderActions({
  showChatKit,
  onToggleChatKit,
  onNewTask,
}: HeaderActionsProps) {
  return (
    <div className="flex gap-2">
      <Button
        onClick={onToggleChatKit}
        className={showChatKit ? "bg-green-600 hover:bg-green-700 text-white" : "bg-blue-600 hover:bg-blue-700 text-white"}
        title="Toggle ChatKit AI Assistant"
      >
        {showChatKit ? "✓ Chat Active" : "💬 Open Chat"}
      </Button>
      <Button
        onClick={onNewTask}
        className="bg-primary-600 hover:bg-primary-700 text-white"
      >
        + New Task
      </Button>
    </div>
  )
}
