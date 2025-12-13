'use client'

import { Task } from '@/types'
import { Card, CardContent, CardHeader, CardTitle, Badge, Button, Checkbox } from '@/components/ui'
import { cn } from '@/lib/utils'

interface TaskCardProps {
  task: Task
  onComplete?: (id: string) => void
  onDelete?: (id: string) => void
  onEdit?: (task: Task) => void
}

/**
 * TaskCard - Reusable task display component
 * Shows task title, description, status badge, and actions
 */
export function TaskCard({
  task,
  onComplete,
  onDelete,
  onEdit,
}: TaskCardProps) {
  const createdDate = new Date(task.created_at).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })

  return (
    <Card className={cn(
      'transition-all duration-normal hover:shadow-lg animate-slide-in-up',
      task.completed && 'opacity-75'
    )}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3 flex-1">
            <Checkbox
              checked={task.completed}
              onChange={() => onComplete?.(task.id)}
              className="mt-1"
            />
            <div className="flex-1 min-w-0">
              <CardTitle className={cn(
                'text-lg',
                task.completed && 'line-through text-gray-500'
              )}>
                {task.title}
              </CardTitle>
              {task.description && (
                <p className={cn(
                  'text-sm text-gray-600 mt-1 line-clamp-2',
                  task.completed && 'text-gray-400'
                )}>
                  {task.description}
                </p>
              )}
            </div>
          </div>
          <Badge variant={task.completed ? 'secondary' : 'success'}>
            {task.completed ? 'Done' : 'Pending'}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Created {createdDate}</span>
          {task.updated_at && new Date(task.updated_at).getTime() !== new Date(task.created_at).getTime() && (
            <span>Modified</span>
          )}
        </div>

        <div className="flex gap-2 pt-2 border-t border-gray-200">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onEdit?.(task)}
            className="flex-1"
          >
            Edit
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onDelete?.(task.id)}
            className="flex-1 text-error-600 hover:text-error-700 hover:bg-error-50"
          >
            Delete
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
