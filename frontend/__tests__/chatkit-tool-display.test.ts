/**
 * ChatKit Tool Display Tests
 *
 * Tests for tool invocation feedback and display in ChatKit UI.
 * Verifies that tool confirmations, results, and widgets display correctly.
 */

import { describe, it, expect } from '@jest/globals'

/**
 * Mock ChatKit widget types
 */
interface MockNoticeEvent {
  level: 'info' | 'warning' | 'error'
  message: string
}

interface MockWidgetItem {
  type: 'widget'
  widget: any
}

/**
 * Mock tool call result types
 */
interface ToolCall {
  tool: string
  result: string
  status: 'executed' | 'failed'
  error?: string
}

/**
 * Test suite for ChatKit tool display
 */
describe('ChatKit Tool Display', () => {
  describe('Tool Confirmation Display', () => {
    it('should display checkmark confirmation for add_task', () => {
      const toolCall: ToolCall = {
        tool: 'add_task',
        result: 'Buy groceries',
        status: 'executed',
      }

      // Tool display should show confirmation
      const message = formatToolResult(toolCall)
      expect(message).toContain('✓')
      expect(message).toContain('Buy groceries')
    })

    it('should display checkmark confirmation for delete_task', () => {
      const toolCall: ToolCall = {
        tool: 'delete_task',
        result: 'Task deleted successfully',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('✓')
      expect(message).toContain('Task deleted')
    })

    it('should display checkmark confirmation for update_task', () => {
      const toolCall: ToolCall = {
        tool: 'update_task',
        result: 'Task updated: Buy milk',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('✓')
      expect(message).toContain('updated')
    })

    it('should display checkmark confirmation for complete_task', () => {
      const toolCall: ToolCall = {
        tool: 'complete_task',
        result: 'Task marked complete',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('✓')
      expect(message).toContain('complete')
    })
  })

  describe('Search Tool Display', () => {
    it('should display search icon and result for found task', () => {
      const toolCall: ToolCall = {
        tool: 'find_task_by_name',
        result: 'Buy groceries - Pending',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('🔍')
      expect(message).toContain('Found')
      expect(message).toContain('Buy groceries')
    })

    it('should display search icon and not found message for no results', () => {
      const toolCall: ToolCall = {
        tool: 'find_task_by_name',
        result: '',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('🔍')
      expect(message.toLowerCase()).toContain('no tasks found')
    })
  })

  describe('List Tool Display', () => {
    it('should display list icon for list_tasks', () => {
      const toolCall: ToolCall = {
        tool: 'list_tasks',
        result: '✓ Buy groceries\n○ Call mom\n○ Do laundry',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('📋')
      expect(message.toLowerCase()).toContain('tasks')
    })

    it('should display list icon for empty task list', () => {
      const toolCall: ToolCall = {
        tool: 'list_tasks',
        result: '',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('📋')
    })
  })

  describe('Error Display', () => {
    it('should display error icon for failed operations', () => {
      const toolCall: ToolCall = {
        tool: 'add_task',
        result: 'Title is required',
        status: 'failed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('❌')
      expect(message).toContain('Error')
      expect(message.toLowerCase()).toContain('title')
    })

    it('should display error icon when error field is present', () => {
      const toolCall: ToolCall = {
        tool: 'delete_task',
        result: '',
        status: 'executed',
        error: 'Task not found',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('❌')
      expect(message).toContain('Error')
      expect(message).toContain('not found')
    })

    it('should display error for missing required fields', () => {
      const toolCall: ToolCall = {
        tool: 'update_task',
        result: '',
        status: 'failed',
        error: 'Task ID is required',
      }

      const message = formatToolResult(toolCall)
      expect(message).toContain('❌')
      expect(message).toContain('Error')
    })
  })

  describe('Multiple Tool Invocations', () => {
    it('should handle sequential tool calls with proper display', () => {
      const toolCalls: ToolCall[] = [
        {
          tool: 'add_task',
          result: 'Project planning',
          status: 'executed',
        },
        {
          tool: 'add_task',
          result: 'Review document',
          status: 'executed',
        },
        {
          tool: 'complete_task',
          result: 'Task marked complete',
          status: 'executed',
        },
      ]

      const messages = toolCalls.map(formatToolResult)

      // All confirmations should be present
      expect(messages[0]).toContain('✓')
      expect(messages[0]).toContain('Project planning')

      expect(messages[1]).toContain('✓')
      expect(messages[1]).toContain('Review document')

      expect(messages[2]).toContain('✓')
      expect(messages[2]).toContain('complete')
    })

    it('should handle mixed success and error tool calls', () => {
      const toolCalls: ToolCall[] = [
        {
          tool: 'add_task',
          result: 'Buy milk',
          status: 'executed',
        },
        {
          tool: 'delete_task',
          result: '',
          status: 'failed',
          error: 'Task not found',
        },
      ]

      const messages = toolCalls.map(formatToolResult)

      expect(messages[0]).toContain('✓') // Success
      expect(messages[1]).toContain('❌') // Error
    })
  })

  describe('Tool Widget Display', () => {
    it('should return widget for list_tasks', () => {
      const toolCall: ToolCall = {
        tool: 'list_tasks',
        result: '✓ Task 1\n○ Task 2',
        status: 'executed',
      }

      const widget = createTaskListWidget(toolCall)
      expect(widget).not.toBeNull()
      expect(widget?.type).toBe('widget')
    })

    it('should return null widget for empty task list', () => {
      const toolCall: ToolCall = {
        tool: 'list_tasks',
        result: '',
        status: 'executed',
      }

      const widget = createTaskListWidget(toolCall)
      expect(widget).toBeNull()
    })

    it('should parse task results from multiple formats', () => {
      const textFormatCall: ToolCall = {
        tool: 'list_tasks',
        result: '✓ Buy groceries\n○ Call mom',
        status: 'executed',
      }

      const widget1 = createTaskListWidget(textFormatCall)
      expect(widget1).not.toBeNull()

      const jsonFormatCall: ToolCall = {
        tool: 'list_tasks',
        result: JSON.stringify([
          { title: 'Buy groceries', completed: true },
          { title: 'Call mom', completed: false },
        ]),
        status: 'executed',
      }

      const widget2 = createTaskListWidget(jsonFormatCall)
      expect(widget2).not.toBeNull()
    })
  })

  describe('Unknown Tool Handling', () => {
    it('should display default message for unknown tool', () => {
      const toolCall: ToolCall = {
        tool: 'unknown_operation',
        result: 'Operation completed',
        status: 'executed',
      }

      const message = formatToolResult(toolCall)
      expect(message).toBeTruthy()
      expect(typeof message).toBe('string')
    })
  })
})

/**
 * Helper function to format tool results
 * Maps to backend _format_tool_result logic
 */
function formatToolResult(toolCall: ToolCall): string {
  const tool = toolCall.tool
  const result = toolCall.result || ''
  const status = toolCall.status
  const error = toolCall.error

  // Handle errors first
  if (error || status === 'failed') {
    const errorMsg = error || result || 'Operation failed'
    return `❌ Error: ${errorMsg}`
  }

  // Simple operations
  if (['add_task', 'delete_task', 'update_task', 'complete_task'].includes(tool)) {
    if (status === 'executed') {
      return `✓ ${result}`
    } else {
      return `⚠️ ${result}`
    }
  }

  // Find operations
  if (tool === 'find_task_by_name') {
    if (result) {
      return `🔍 Found: ${result}`
    } else {
      return `🔍 No tasks found matching search`
    }
  }

  // List operations
  if (tool === 'list_tasks') {
    return `📋 Tasks list ready`
  }

  // Default
  return result ? `✓ ${result}` : `✓ ${tool} completed`
}

/**
 * Helper function to create task list widget
 * Maps to backend _create_task_list_widget logic
 */
function createTaskListWidget(toolCall: ToolCall): MockWidgetItem | null {
  const result = toolCall.result || ''

  if (!result) {
    return null
  }

  // Parse task list from result
  const tasks = []

  try {
    // Try parsing as JSON first
    if (result.startsWith('[')) {
      tasks.push(...JSON.parse(result))
    } else {
      // Parse text format
      const lines = result.trim().split('\n')
      for (const line of lines) {
        if (line.strip()) {
          const completed = line.includes('✓') || line.toLowerCase().includes('(completed)')
          const title = line.replace(/^[✓○]\s*/, '').trim()
          if (title) {
            tasks.push({ title, completed })
          }
        }
      }
    }
  } catch (e) {
    // Fallback to text format
    return null
  }

  if (tasks.length === 0) {
    return null
  }

  // Return widget item
  return {
    type: 'widget',
    widget: {
      type: 'Card',
      title: `📋 Your Tasks (${tasks.length})`,
      tasks: tasks,
    },
  }
}

/**
 * String polyfill for trim (for compatibility)
 */
if (!String.prototype.strip) {
  // @ts-ignore
  String.prototype.strip = function () {
    return this.trim()
  }
}
