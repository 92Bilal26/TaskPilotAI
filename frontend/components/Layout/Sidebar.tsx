'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

interface NavItem {
  label: string
  href: string
  icon?: string
  badge?: number | string | null
  active?: boolean
}

interface SidebarProps {
  items: NavItem[]
  title?: string
  onLogout?: () => void
  collapsed?: boolean
  onCollapsedChange?: (collapsed: boolean) => void
}

/**
 * Sidebar - Reusable sidebar navigation component
 * Displays navigation items with active state indication
 */
export function Sidebar({ items, title = 'TaskPilotAI', onLogout, collapsed: externalCollapsed, onCollapsedChange }: SidebarProps) {
  const pathname = usePathname()
  const [internalCollapsed, setInternalCollapsed] = useState(false)
  const collapsed = externalCollapsed !== undefined ? externalCollapsed : internalCollapsed

  const handleCollapsedChange = (newState: boolean) => {
    setInternalCollapsed(newState)
    if (onCollapsedChange) {
      onCollapsedChange(newState)
    }
  }

  return (
    <aside className={cn(
      'border-r border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800 transition-all duration-normal',
      'fixed md:relative bottom-0 left-0 right-0 md:bottom-auto md:left-auto md:right-auto z-40',
      'h-20 md:h-screen flex flex-row-reverse md:flex-col',
      collapsed ? 'md:w-20' : 'md:w-64',
      'w-full'
    )}>
      <div className="flex flex-col md:h-screen h-full w-full md:w-auto">
        {/* Logo - Hidden on Mobile */}
        <div className={cn(
          'hidden md:flex items-center gap-3 px-6 py-4 border-b border-gray-200 dark:border-gray-700',
          collapsed && 'justify-center px-2'
        )}>
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center text-white font-bold">
            T
          </div>
          {!collapsed && (
            <div className="min-w-0 flex-1">
              <h2 className="text-sm font-bold text-gray-900 dark:text-white truncate">
                {title}
              </h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">Task Manager</p>
            </div>
          )}
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 overflow-x-auto md:overflow-y-auto px-2 md:px-3 py-2 md:py-4 space-x-1 md:space-x-0 md:space-y-2 flex md:flex-col">
          {items.map((item) => {
            const isActive = pathname === item.href || pathname.startsWith(item.href + '/')

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'flex items-center gap-3 px-2 md:px-3 py-2 md:py-2.5 rounded-lg text-sm font-medium transition-colors duration-fast whitespace-nowrap md:whitespace-normal flex-shrink-0 md:flex-shrink',
                  'h-10 md:h-auto',
                  isActive
                    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-200'
                    : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                )}
                title={item.label}
              >
                {item.icon && <span className="text-lg">{item.icon}</span>}
                {!collapsed && (
                  <div className="hidden md:flex md:flex-1 md:items-center md:gap-2">
                    <span className="flex-1 truncate">{item.label}</span>
                    {item.badge !== undefined && item.badge !== null && item.badge !== "" && (
                      <span className="bg-error-600 text-white text-xs px-2 py-0.5 rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </div>
                )}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className={cn(
          'border-t border-gray-200 dark:border-gray-700 p-3 space-y-2',
          collapsed && 'flex flex-col items-center'
        )}>
          <button
            onClick={() => handleCollapsedChange(!collapsed)}
            className={cn(
              'w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
              'transition-colors duration-fast'
            )}
            title={collapsed ? 'Expand' : 'Collapse'}
          >
            {collapsed ? '→' : '←'}
            {!collapsed && <span>Collapse</span>}
          </button>
          {onLogout && !collapsed && (
            <button
              onClick={onLogout}
              className="w-full flex items-center gap-2 px-3 py-2.5 rounded-lg text-sm font-medium text-error-600 hover:bg-error-50 dark:hover:bg-error-900 transition-colors duration-fast"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </aside>
  )
}
