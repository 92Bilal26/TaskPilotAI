'use client'

import { ReactNode } from 'react'
import { Label } from '@/components/ui'
import { cn } from '@/lib/utils'

interface FormFieldProps {
  label?: string
  error?: string
  hint?: string
  required?: boolean
  children: ReactNode
  className?: string
}

/**
 * FormField - Reusable form field wrapper
 * Handles label, input, error message, and hint text
 */
export function FormField({
  label,
  error,
  hint,
  required = false,
  children,
  className,
}: FormFieldProps) {
  return (
    <div className={cn('space-y-2', className)}>
      {label && (
        <Label className={required ? "after:content-['*'] after:ml-0.5 after:text-error-600" : ''}>
          {label}
        </Label>
      )}
      {children}
      {error && (
        <p className="text-sm text-error-600 font-medium">{error}</p>
      )}
      {hint && !error && (
        <p className="text-sm text-gray-500">{hint}</p>
      )}
    </div>
  )
}
