import * as React from "react"

interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "destructive" | "warning"
}

const getAlertClasses = (variant: string) => {
  const variants: Record<string, string> = {
    default: "bg-white text-gray-900 border-gray-200",
    success: "bg-success-50 text-success-900 border-success-200",
    destructive: "bg-error-50 text-error-900 border-error-200",
    warning: "bg-warning-50 text-warning-900 border-warning-200",
  }
  return variants[variant] || variants.default
}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className = "", variant = "default", ...props }, ref) => {
    const baseClasses = "relative w-full rounded-lg border p-4"
    const variantClasses = getAlertClasses(variant)
    const finalClassName = `${baseClasses} ${variantClasses} ${className}`

    return (
      <div
        ref={ref}
        role="alert"
        className={finalClassName}
        {...props}
      />
    )
  }
)
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className = "", ...props }, ref) => (
  <h5
    ref={ref}
    className={`mb-1 font-medium leading-tight tracking-tight ${className}`}
    {...props}
  />
))
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className = "", ...props }, ref) => (
  <div
    ref={ref}
    className={`text-sm leading-relaxed ${className}`}
    {...props}
  />
))
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }
