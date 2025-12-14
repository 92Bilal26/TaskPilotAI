'use client'

import { useState, useEffect } from 'react'
import { Task } from '@/types'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface TaskEditModalProps {
  task: Task | null
  onClose: () => void
  onSave: (updates: { title: string; description: string }) => Promise<void>
  isLoading?: boolean
}

export function TaskEditModal({ task, onClose, onSave, isLoading = false }: TaskEditModalProps) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  // Update form values when task changes
  useEffect(() => {
    if (task) {
      setTitle(task.title || '')
      setDescription(task.description || '')
    }
  }, [task])
  const [isSaving, setIsSaving] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSaving(true)
    try {
      await onSave({ title, description })
      onClose()
    } finally {
      setIsSaving(false)
    }
  }

  if (!task) return null

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 animate-fade-in">
      <Card className="w-full max-w-md animate-slide-in-up">
        <CardHeader>
          <CardTitle>Edit Task</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Title</label>
              <Input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Task title..."
                required
                disabled={isSaving || isLoading}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
              <Textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Task description (optional)..."
                disabled={isSaving || isLoading}
              />
            </div>

            <div className="flex gap-2 pt-4">
              <Button
                type="button"
                variant="ghost"
                onClick={onClose}
                disabled={isSaving || isLoading}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={isSaving || isLoading}
                className="flex-1"
              >
                {isSaving ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="animate-spin h-4 w-4 rounded-full border-2 border-white border-t-transparent"></div>
                    Saving...
                  </span>
                ) : (
                  'Save Changes'
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
