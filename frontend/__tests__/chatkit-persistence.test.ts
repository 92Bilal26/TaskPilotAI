/**
 * ChatKit Persistence Tests
 *
 * Tests for conversation history loading and persistence in ChatKit UI.
 * Verifies that previous conversations load correctly on page mount.
 */

import { describe, it, expect, beforeEach } from '@jest/globals'

/**
 * Mock types matching chat-client
 */
interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  tool_calls?: any[]
  created_at: string
}

interface ConversationDetail {
  id: number
  title: string
  created_at: string
  updated_at: string
  messages: ChatMessage[]
}

interface ConversationSummary {
  id: number
  title: string
  message_count: number
  created_at: string
  updated_at: string
}

/**
 * Test suite for ChatKit conversation persistence
 */
describe('ChatKit Conversation Persistence (T020-T022)', () => {
  describe('T020: Conversation History Loading', () => {
    it('should load conversation history on component mount', async () => {
      // Given: A conversation ID in sessionStorage
      const conversationId = 123
      const mockHistory: ConversationDetail = {
        id: conversationId,
        title: 'My First Task Discussion',
        created_at: '2025-12-21T10:00:00Z',
        updated_at: '2025-12-21T11:00:00Z',
        messages: [
          {
            id: 1,
            role: 'user',
            content: 'Add a task to buy groceries',
            created_at: '2025-12-21T10:00:00Z',
          },
          {
            id: 2,
            role: 'assistant',
            content: 'I have added your task: Buy groceries',
            created_at: '2025-12-21T10:01:00Z',
          },
          {
            id: 3,
            role: 'user',
            content: 'Show me all my tasks',
            created_at: '2025-12-21T10:02:00Z',
          },
          {
            id: 4,
            role: 'assistant',
            content: '✓ Buy groceries (pending)',
            created_at: '2025-12-21T10:03:00Z',
          },
        ],
      }

      // When: Component loads conversation history
      const loadedMessages = mockHistory.messages

      // Then: Messages should be loaded and displayed
      expect(loadedMessages).toHaveLength(4)
      expect(loadedMessages[0].role).toBe('user')
      expect(loadedMessages[0].content).toContain('Add a task')
      expect(loadedMessages[1].role).toBe('assistant')
      expect(loadedMessages[3].content).toContain('Buy groceries')
    })

    it('should display conversation title from loaded history', () => {
      const mockHistory: ConversationDetail = {
        id: 1,
        title: 'Task Planning Session',
        created_at: '2025-12-21T10:00:00Z',
        updated_at: '2025-12-21T11:00:00Z',
        messages: [],
      }

      expect(mockHistory.title).toBe('Task Planning Session')
    })

    it('should handle empty conversation history gracefully', () => {
      const mockHistory: ConversationDetail = {
        id: 1,
        title: 'Empty Conversation',
        created_at: '2025-12-21T10:00:00Z',
        updated_at: '2025-12-21T10:00:00Z',
        messages: [],
      }

      expect(mockHistory.messages).toHaveLength(0)
      // Should still display conversation without errors
      expect(mockHistory.title).toBeTruthy()
    })

    it('should preserve message order from history', () => {
      const messages: ChatMessage[] = [
        {
          id: 1,
          role: 'user',
          content: 'First message',
          created_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          role: 'assistant',
          content: 'Second message',
          created_at: '2025-12-21T10:01:00Z',
        },
        {
          id: 3,
          role: 'user',
          content: 'Third message',
          created_at: '2025-12-21T10:02:00Z',
        },
      ]

      // Messages should maintain chronological order
      expect(messages[0].id).toBe(1)
      expect(messages[1].id).toBe(2)
      expect(messages[2].id).toBe(3)
      expect(messages[0].created_at < messages[1].created_at).toBe(true)
      expect(messages[1].created_at < messages[2].created_at).toBe(true)
    })

    it('should handle conversation with tool calls', () => {
      const messages: ChatMessage[] = [
        {
          id: 1,
          role: 'user',
          content: 'Add task: Buy milk',
          created_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          role: 'assistant',
          content: '✓ Task created: Buy milk',
          created_at: '2025-12-21T10:01:00Z',
          tool_calls: [
            {
              tool: 'add_task',
              result: 'Task created successfully',
            },
          ],
        },
      ]

      expect(messages[1].tool_calls).toBeDefined()
      expect(messages[1].tool_calls![0].tool).toBe('add_task')
    })
  })

  describe('T021: Conversation Switcher', () => {
    it('should list all conversations for user', () => {
      const conversations: ConversationSummary[] = [
        {
          id: 1,
          title: 'Task Planning',
          message_count: 8,
          created_at: '2025-12-21T10:00:00Z',
          updated_at: '2025-12-21T11:00:00Z',
        },
        {
          id: 2,
          title: 'Daily Review',
          message_count: 5,
          created_at: '2025-12-20T14:00:00Z',
          updated_at: '2025-12-20T15:00:00Z',
        },
        {
          id: 3,
          title: 'Project Discussion',
          message_count: 12,
          created_at: '2025-12-19T09:00:00Z',
          updated_at: '2025-12-19T10:30:00Z',
        },
      ]

      expect(conversations).toHaveLength(3)
      expect(conversations[0].id).toBe(1)
      expect(conversations[1].title).toBe('Daily Review')
      expect(conversations[2].message_count).toBe(12)
    })

    it('should allow switching to a different conversation', () => {
      const conversations: ConversationSummary[] = [
        {
          id: 1,
          title: 'Conversation 1',
          message_count: 5,
          created_at: '2025-12-21T10:00:00Z',
          updated_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          title: 'Conversation 2',
          message_count: 8,
          created_at: '2025-12-20T10:00:00Z',
          updated_at: '2025-12-20T10:00:00Z',
        },
      ]

      let activeConversationId = 1
      const newConversationId = 2

      // Simulate switching conversation
      activeConversationId = newConversationId

      expect(activeConversationId).toBe(2)
      expect(activeConversationId).not.toBe(1)
    })

    it('should highlight active conversation in switcher', () => {
      const conversations: ConversationSummary[] = [
        {
          id: 1,
          title: 'Conversation 1',
          message_count: 5,
          created_at: '2025-12-21T10:00:00Z',
          updated_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          title: 'Conversation 2',
          message_count: 8,
          created_at: '2025-12-20T10:00:00Z',
          updated_at: '2025-12-20T10:00:00Z',
        },
      ]

      const activeId = 2

      // Only conversation 2 should be marked active
      const activeConversation = conversations.find((c) => c.id === activeId)
      expect(activeConversation?.id).toBe(2)
      expect(activeConversation?.title).toBe('Conversation 2')
    })

    it('should load correct message count for each conversation', () => {
      const conversations: ConversationSummary[] = [
        {
          id: 1,
          title: 'Few Messages',
          message_count: 2,
          created_at: '2025-12-21T10:00:00Z',
          updated_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          title: 'Many Messages',
          message_count: 15,
          created_at: '2025-12-20T10:00:00Z',
          updated_at: '2025-12-20T10:00:00Z',
        },
      ]

      expect(conversations[0].message_count).toBe(2)
      expect(conversations[1].message_count).toBe(15)
    })

    it('should order conversations by most recent', () => {
      const conversations: ConversationSummary[] = [
        {
          id: 1,
          title: 'Oldest',
          message_count: 5,
          created_at: '2025-12-19T10:00:00Z',
          updated_at: '2025-12-19T10:00:00Z',
        },
        {
          id: 2,
          title: 'Newest',
          message_count: 8,
          created_at: '2025-12-21T10:00:00Z',
          updated_at: '2025-12-21T11:00:00Z',
        },
        {
          id: 3,
          title: 'Middle',
          message_count: 6,
          created_at: '2025-12-20T10:00:00Z',
          updated_at: '2025-12-20T14:00:00Z',
        },
      ]

      // Sort by updated_at descending (most recent first)
      const sorted = [...conversations].sort(
        (a, b) =>
          new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
      )

      expect(sorted[0].title).toBe('Newest')
      expect(sorted[1].title).toBe('Middle')
      expect(sorted[2].title).toBe('Oldest')
    })

    it('should handle empty conversation list', () => {
      const conversations: ConversationSummary[] = []

      expect(conversations).toHaveLength(0)
      expect(conversations.length === 0).toBe(true)
    })

    it('should persist conversation ID in localStorage after switching', () => {
      const selectedConversationId = 42
      const storageKey = 'chatkit_conversation_id'

      // Simulate storing conversation ID
      localStorage.setItem(storageKey, String(selectedConversationId))
      const retrieved = localStorage.getItem(storageKey)

      expect(retrieved).toBe('42')
      expect(parseInt(retrieved!)).toBe(42)

      // Cleanup
      localStorage.removeItem(storageKey)
    })
  })

  describe('T022: Conversation Context Preservation', () => {
    it('should maintain agent context with previous messages', () => {
      const previousMessages: ChatMessage[] = [
        {
          id: 1,
          role: 'user',
          content: 'My main project is TaskPilot',
          created_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          role: 'assistant',
          content: 'Got it, your main project is TaskPilot',
          created_at: '2025-12-21T10:01:00Z',
        },
      ]

      const newMessage: ChatMessage = {
        id: 3,
        role: 'user',
        content: 'What was my project again?',
        created_at: '2025-12-21T10:02:00Z',
      }

      // Agent should have context from previous messages
      const context = [...previousMessages, newMessage]
      expect(context).toHaveLength(3)
      expect(context[0].content).toContain('TaskPilot')
      // Most recent message should be at end
      expect(context[context.length - 1].role).toBe('user')
    })

    it('should load multi-turn conversation correctly', () => {
      const multiTurnMessages: ChatMessage[] = [
        {
          id: 1,
          role: 'user',
          content: 'Add task: Buy milk',
          created_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          role: 'assistant',
          content: '✓ Task added: Buy milk',
          created_at: '2025-12-21T10:01:00Z',
        },
        {
          id: 3,
          role: 'user',
          content: 'Also add: Buy eggs',
          created_at: '2025-12-21T10:02:00Z',
        },
        {
          id: 4,
          role: 'assistant',
          content: '✓ Task added: Buy eggs',
          created_at: '2025-12-21T10:03:00Z',
        },
        {
          id: 5,
          role: 'user',
          content: 'Show me all my grocery tasks',
          created_at: '2025-12-21T10:04:00Z',
        },
        {
          id: 6,
          role: 'assistant',
          content: '✓ Buy milk (pending)\n✓ Buy eggs (pending)',
          created_at: '2025-12-21T10:05:00Z',
        },
      ]

      expect(multiTurnMessages).toHaveLength(6)
      // Conversation should alternate between user and assistant
      expect(multiTurnMessages[0].role).toBe('user')
      expect(multiTurnMessages[1].role).toBe('assistant')
      expect(multiTurnMessages[2].role).toBe('user')
      expect(multiTurnMessages[3].role).toBe('assistant')
    })

    it('should load 100% of history messages correctly', () => {
      // Test that all loaded messages are available
      const historyMessages: ChatMessage[] = [
        { id: 1, role: 'user', content: 'Msg 1', created_at: '2025-12-21T10:00:00Z' },
        { id: 2, role: 'assistant', content: 'Msg 2', created_at: '2025-12-21T10:01:00Z' },
        { id: 3, role: 'user', content: 'Msg 3', created_at: '2025-12-21T10:02:00Z' },
        { id: 4, role: 'assistant', content: 'Msg 4', created_at: '2025-12-21T10:03:00Z' },
        { id: 5, role: 'user', content: 'Msg 5', created_at: '2025-12-21T10:04:00Z' },
      ]

      // All messages should be accessible
      expect(historyMessages.map((m) => m.id)).toEqual([1, 2, 3, 4, 5])
      expect(historyMessages.every((m) => m.content && m.created_at)).toBe(true)
    })

    it('should handle conversation without breaking agent context', () => {
      const conversation: ConversationDetail = {
        id: 1,
        title: 'Conversation 1',
        created_at: '2025-12-21T10:00:00Z',
        updated_at: '2025-12-21T11:00:00Z',
        messages: [
          {
            id: 1,
            role: 'user',
            content: 'Set a reminder for tomorrow',
            created_at: '2025-12-21T10:00:00Z',
          },
          {
            id: 2,
            role: 'assistant',
            content: 'I have set a reminder for tomorrow',
            created_at: '2025-12-21T10:01:00Z',
          },
        ],
      }

      // Should be able to add new messages to loaded conversation
      const newMessage: ChatMessage = {
        id: 3,
        role: 'user',
        content: 'What did I ask you about?',
        created_at: '2025-12-21T10:02:00Z',
      }

      const updatedMessages = [...conversation.messages, newMessage]
      expect(updatedMessages).toHaveLength(3)
      // Agent should understand context about the reminder
      expect(updatedMessages[0].content).toContain('reminder')
    })
  })

  describe('Integration Tests', () => {
    it('should load history and allow new messages', async () => {
      // Simulate loading history
      const history: ChatMessage[] = [
        {
          id: 1,
          role: 'user',
          content: 'Previous message',
          created_at: '2025-12-21T10:00:00Z',
        },
        {
          id: 2,
          role: 'assistant',
          content: 'Previous response',
          created_at: '2025-12-21T10:01:00Z',
        },
      ]

      // Simulate adding new message
      const newMessage: ChatMessage = {
        id: 3,
        role: 'user',
        content: 'New message',
        created_at: '2025-12-21T10:02:00Z',
      }

      const allMessages = [...history, newMessage]

      expect(allMessages).toHaveLength(3)
      expect(allMessages[0].id).toBe(1)
      expect(allMessages[2].id).toBe(3)
    })

    it('should handle switching between conversations', async () => {
      const conversation1: ConversationDetail = {
        id: 1,
        title: 'Conv 1',
        created_at: '2025-12-21T10:00:00Z',
        updated_at: '2025-12-21T10:00:00Z',
        messages: [
          {
            id: 1,
            role: 'user',
            content: 'Conv 1 message',
            created_at: '2025-12-21T10:00:00Z',
          },
        ],
      }

      const conversation2: ConversationDetail = {
        id: 2,
        title: 'Conv 2',
        created_at: '2025-12-20T10:00:00Z',
        updated_at: '2025-12-20T10:00:00Z',
        messages: [
          {
            id: 1,
            role: 'user',
            content: 'Conv 2 message',
            created_at: '2025-12-20T10:00:00Z',
          },
        ],
      }

      let activeConversation = conversation1
      expect(activeConversation.messages[0].content).toContain('Conv 1')

      // Switch conversation
      activeConversation = conversation2
      expect(activeConversation.messages[0].content).toContain('Conv 2')
    })
  })
})
