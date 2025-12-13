import * as React from "react"
import { cn } from "@/lib/utils"

export interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, ...props }, ref) => (
    <select
      className={cn(
        "flex h-10 w-full rounded-lg border-2 border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 transition-all duration-fast appearance-none cursor-pointer focus-visible:outline-none focus-visible:border-primary-500 focus-visible:ring-2 focus-visible:ring-primary-200 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:border-gray-200 disabled:text-gray-500",
        className
      )}
      ref={ref}
      {...props}
    />
  )
)
Select.displayName = "Select"

export { Select }
