/**
 * Tests for Chat Client - API Communication
 *
 * Tests for:
 * - Message sending to chat endpoint
 * - Conversation listing
 * - Conversation details retrieval
 * - Error handling
 * - Authentication token usage
 */

import { chatClient } from '@/lib/chat-client'

// Mock fetch
global.fetch = jest.fn()

describe('ChatClient', () => {
  const mockUserId = 'test-user-001'
  const mockAuthToken = 'test-token-abc123'
  const mockConversationId = 1

  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('sendMessage', () => {
    it('should send a message to the chat endpoint', async () => {
      // Arrange
      const mockResponse: any = {
        conversation_id: mockConversationId,
        message_id: 1,
        response: "I've added 'Buy groceries' to your task list",
        tool_calls: [],
        status: 'success',
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      // Act
      const result = await chatClient.sendMessage(
        mockUserId,
        { content: 'Add a task to buy groceries' },
        mockAuthToken
      )

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/chat`,
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/json',
            Authorization: `Bearer ${mockAuthToken}`,
          }),
        })
      )
      expect(result).toEqual(mockResponse)
    })

    it('should include conversation_id if provided', async () => {
      // Arrange
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: mockConversationId,
          message_id: 2,
          response: 'Task updated',
          tool_calls: [],
          status: 'success',
        }),
      })

      // Act
      await chatClient.sendMessage(
        mockUserId,
        {
          content: 'Update the task',
          conversation_id: mockConversationId,
        },
        mockAuthToken
      )

      // Assert
      const callBody = JSON.parse(
        (global.fetch as jest.Mock).mock.calls[0][1].body
      )
      expect(callBody.conversation_id).toBe(mockConversationId)
    })

    it('should throw error on failed response', async () => {
      // Arrange
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        statusText: 'Unauthorized',
      })

      // Act & Assert
      await expect(
        chatClient.sendMessage(
          mockUserId,
          { content: 'Hello' },
          mockAuthToken
        )
      ).rejects.toThrow('Chat error: Unauthorized')
    })
  })

  describe('listConversations', () => {
    it('should fetch all conversations for user', async () => {
      // Arrange
      const mockConversations = [
        {
          id: 1,
          title: 'Task discussion',
          message_count: 5,
          created_at: '2025-12-15T10:00:00Z',
          updated_at: '2025-12-15T10:30:00Z',
        },
      ]

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockConversations,
      })

      // Act
      const result = await chatClient.listConversations(mockUserId, mockAuthToken)

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/conversations`,
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            Authorization: `Bearer ${mockAuthToken}`,
          }),
        })
      )
      expect(result).toEqual(mockConversations)
    })

    it('should handle empty conversations list', async () => {
      // Arrange
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      })

      // Act
      const result = await chatClient.listConversations(mockUserId, mockAuthToken)

      // Assert
      expect(result).toEqual([])
    })
  })

  describe('getConversation', () => {
    it('should fetch conversation with all messages', async () => {
      // Arrange
      const mockConversation = {
        id: mockConversationId,
        title: 'Task discussion',
        created_at: '2025-12-15T10:00:00Z',
        updated_at: '2025-12-15T10:30:00Z',
        messages: [
          {
            id: 1,
            role: 'user' as const,
            content: 'Add a task',
            created_at: '2025-12-15T10:00:00Z',
          },
          {
            id: 2,
            role: 'assistant' as const,
            content: "I've added the task",
            tool_calls: [
              {
                name: 'add_task',
                arguments: { title: 'Test task' },
                result: { task_id: '123' },
              },
            ],
            created_at: '2025-12-15T10:00:05Z',
          },
        ],
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockConversation,
      })

      // Act
      const result = await chatClient.getConversation(
        mockUserId,
        mockConversationId,
        mockAuthToken
      )

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        `http://localhost:8000/api/${mockUserId}/conversations/${mockConversationId}`,
        expect.objectContaining({
          method: 'GET',
        })
      )
      expect(result).toEqual(mockConversation)
      expect(result.messages).toHaveLength(2)
    })
  })

  describe('Convenience methods', () => {
    it('createTask should send properly formatted message', async () => {
      // Arrange
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: 1,
          message_id: 1,
          response: "I've added the task",
          tool_calls: [],
          status: 'success',
        }),
      })

      // Act
      await chatClient.createTask(mockUserId, 'Buy groceries', mockAuthToken)

      // Assert
      const callBody = JSON.parse(
        (global.fetch as jest.Mock).mock.calls[0][1].body
      )
      expect(callBody.content).toContain('Buy groceries')
    })

    it('getPendingTasks should ask for pending tasks', async () => {
      // Arrange
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: 1,
          message_id: 1,
          response: 'You have 3 pending tasks',
          tool_calls: [],
          status: 'success',
        }),
      })

      // Act
      await chatClient.getPendingTasks(mockUserId, mockAuthToken)

      // Assert
      const callBody = JSON.parse(
        (global.fetch as jest.Mock).mock.calls[0][1].body
      )
      expect(callBody.content).toBe('Show me my pending tasks')
    })

    it('completeTask should mark task as complete', async () => {
      // Arrange
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: 1,
          message_id: 1,
          response: "I've marked 'Buy groceries' as complete",
          tool_calls: [],
          status: 'success',
        }),
      })

      // Act
      await chatClient.completeTask(mockUserId, 'Buy groceries', mockAuthToken)

      // Assert
      const callBody = JSON.parse(
        (global.fetch as jest.Mock).mock.calls[0][1].body
      )
      expect(callBody.content).toBe('Mark Buy groceries as complete')
    })
  })
})
