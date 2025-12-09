import * as React from "react"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "success" | "destructive" | "outline"
}

const getBadgeClasses = (variant: string) => {
  const variants: Record<string, string> = {
    default: "bg-primary-100 text-primary-800 border border-primary-200",
    secondary: "bg-gray-100 text-gray-800 border border-gray-200",
    success: "bg-success-100 text-success-800 border border-success-200",
    destructive: "bg-error-100 text-error-800 border border-error-200",
    outline: "text-gray-800 border border-gray-200 bg-transparent",
  }
  return variants[variant] || variants.default
}

const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className = "", variant = "default", ...props }, ref) => {
    const baseClasses = "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors"
    const variantClasses = getBadgeClasses(variant)
    const finalClassName = `${baseClasses} ${variantClasses} ${className}`

    return (
      <div
        ref={ref}
        className={finalClassName}
        {...props}
      />
    )
  }
)
Badge.displayName = "Badge"

export { Badge }
