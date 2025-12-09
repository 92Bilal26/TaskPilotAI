'use client'

import { useState, useCallback } from 'react'
import { Input } from '@/components/ui'
import { cn } from '@/lib/utils'

interface SearchBarProps {
  placeholder?: string
  onSearch: (query: string) => void
  onClear?: () => void
  debounceMs?: number
  className?: string
}

/**
 * SearchBar - Reusable search input component
 * Debounced search with clear functionality
 */
export function SearchBar({
  placeholder = 'Search tasks...',
  onSearch,
  onClear,
  debounceMs = 300,
  className,
}: SearchBarProps) {
  const [query, setQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)

  // Debounce search
  const handleSearch = useCallback(
    ((value: string) => {
      setQuery(value)
      setIsSearching(true)

      const timer = setTimeout(() => {
        onSearch(value)
        setIsSearching(false)
      }, debounceMs)

      return () => clearTimeout(timer)
    }) as (value: string) => void,
    [onSearch, debounceMs]
  )

  const handleClear = () => {
    setQuery('')
    onClear?.()
    onSearch('')
  }

  return (
    <div className={cn('relative', className)}>
      <Input
        type="search"
        placeholder={placeholder}
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        className="pr-10"
      />
      {query && (
        <button
          onClick={handleClear}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          aria-label="Clear search"
        >
          ×
        </button>
      )}
      {isSearching && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      )}
    </div>
  )
}
