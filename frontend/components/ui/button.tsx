import * as React from "react"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "destructive" | "outline" | "ghost" | "link"
  size?: "default" | "sm" | "lg" | "icon"
}

const getVariantClasses = (variant: string) => {
  const variants: Record<string, string> = {
    default: "bg-primary-600 text-white hover:bg-primary-700 hover:shadow-lg active:scale-95 transition-all duration-fast",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 hover:shadow-md active:scale-95 transition-all duration-fast",
    destructive: "bg-error-50 text-error-600 hover:bg-error-100 hover:shadow-md active:scale-95 transition-all duration-fast",
    outline: "border-2 border-gray-300 bg-white text-gray-900 hover:bg-gray-50 hover:shadow-sm active:scale-95 transition-all duration-fast",
    ghost: "bg-transparent text-primary-600 hover:bg-primary-50 active:scale-95 transition-all duration-fast",
    link: "text-primary-600 underline-offset-4 hover:underline transition-colors duration-fast",
  }
  return variants[variant] || variants.default
}

const getSizeClasses = (size: string) => {
  const sizes: Record<string, string> = {
    default: "h-10 px-4 py-2.5 text-sm",
    sm: "h-9 rounded-md px-3 text-xs",
    lg: "h-11 rounded-lg px-8 text-base",
    icon: "h-10 w-10",
  }
  return sizes[size] || sizes.default
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = "", variant = "default", size = "default", ...props }, ref) => {
    const baseClasses = "inline-flex items-center justify-center gap-2 rounded-lg font-semibold transition-all duration-200 whitespace-nowrap focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
    const variantClasses = getVariantClasses(variant)
    const sizeClasses = getSizeClasses(size)
    const finalClassName = `${baseClasses} ${variantClasses} ${sizeClasses} ${className}`

    return (
      <button
        className={finalClassName}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
