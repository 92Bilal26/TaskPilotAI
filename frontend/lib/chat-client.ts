/**
 * Chat Client - API Communication
 *
 * Handles all HTTP requests to the backend chat endpoint.
 * Manages authentication headers and error handling.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ChatMessageRequest {
  content: string
  conversation_id?: number
}

interface ToolCall {
  name: string
  arguments: Record<string, unknown>
  result?: unknown
}

interface ChatResponse {
  conversation_id: number
  message_id: number
  response: string
  tool_calls: ToolCall[]
  status: string
}

interface Conversation {
  id: number
  title: string
  message_count: number
  created_at: string
  updated_at: string
}

interface ConversationDetail {
  id: number
  title: string
  created_at: string
  updated_at: string
  messages: Array<{
    id: number
    role: 'user' | 'assistant'
    content: string
    tool_calls?: ToolCall[]
    created_at: string
  }>
}

class ChatClient {
  /**
   * Send a message to the chatbot
   */
  async sendMessage(
    userId: string,
    message: ChatMessageRequest,
    authToken: string
  ): Promise<ChatResponse> {
    const response = await fetch(`${API_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify(message),
    })

    if (!response.ok) {
      throw new Error(`Chat error: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get all conversations for a user
   */
  async listConversations(
    userId: string,
    authToken: string
  ): Promise<Conversation[]> {
    const response = await fetch(`${API_URL}/api/${userId}/conversations`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to load conversations: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Get a specific conversation with all messages
   */
  async getConversation(
    userId: string,
    conversationId: number,
    authToken: string
  ): Promise<ConversationDetail> {
    const response = await fetch(
      `${API_URL}/api/${userId}/conversations/${conversationId}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error(`Failed to load conversation: ${response.statusText}`)
    }

    return response.json()
  }

  /**
   * Create a new task via chat
   * This is a convenience method that sends a message to create a task
   */
  async createTask(
    userId: string,
    taskDescription: string,
    authToken: string
  ): Promise<ChatResponse> {
    return this.sendMessage(
      userId,
      {
        content: `Add a task: ${taskDescription}`,
      },
      authToken
    )
  }

  /**
   * Get pending tasks via chat
   */
  async getPendingTasks(
    userId: string,
    authToken: string
  ): Promise<ChatResponse> {
    return this.sendMessage(
      userId,
      {
        content: 'Show me my pending tasks',
      },
      authToken
    )
  }

  /**
   * Mark task as complete via chat
   */
  async completeTask(
    userId: string,
    taskIdentifier: string,
    authToken: string
  ): Promise<ChatResponse> {
    return this.sendMessage(
      userId,
      {
        content: `Mark ${taskIdentifier} as complete`,
      },
      authToken
    )
  }

  /**
   * Delete task via chat
   */
  async deleteTask(
    userId: string,
    taskIdentifier: string,
    authToken: string
  ): Promise<ChatResponse> {
    return this.sendMessage(
      userId,
      {
        content: `Delete ${taskIdentifier}`,
      },
      authToken
    )
  }

  /**
   * Update task via chat
   */
  async updateTask(
    userId: string,
    taskIdentifier: string,
    updates: string,
    authToken: string
  ): Promise<ChatResponse> {
    return this.sendMessage(
      userId,
      {
        content: `Update ${taskIdentifier}: ${updates}`,
      },
      authToken
    )
  }
}

// Export singleton instance
export const chatClient = new ChatClient()
