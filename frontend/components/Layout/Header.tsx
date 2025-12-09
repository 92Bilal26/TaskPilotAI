'use client'

import { ReactNode } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui'
import { cn } from '@/lib/utils'

interface HeaderProps {
  title: string
  subtitle?: string
  action?: ReactNode
  className?: string
  showBackButton?: boolean
}

/**
 * Header - Reusable page header component
 * Displays title, subtitle, and optional action button
 */
export function Header({
  title,
  subtitle,
  action,
  className,
  showBackButton = false,
}: HeaderProps) {
  return (
    <header className={cn(
      'border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 sticky top-0 z-40',
      className
    )}>
      <div className="flex items-center justify-between px-6 py-4 gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-4">
            {showBackButton && (
              <Link href="/" className="text-gray-500 hover:text-gray-700">
                ←
              </Link>
            )}
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                {title}
              </h1>
              {subtitle && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {subtitle}
                </p>
              )}
            </div>
          </div>
        </div>
        {action && (
          <div className="flex-shrink-0">
            {action}
          </div>
        )}
      </div>
    </header>
  )
}
