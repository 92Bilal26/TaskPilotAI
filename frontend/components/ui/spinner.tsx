import * as React from "react"
import { cn } from "@/lib/utils"

export interface SpinnerProps
  extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg"
}

const Spinner = React.forwardRef<HTMLDivElement, SpinnerProps>(
  ({ className, size = "md", ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "inline-block border-2 border-current border-t-transparent rounded-full animate-spin",
        {
          "w-4 h-4": size === "sm",
          "w-6 h-6": size === "md",
          "w-8 h-8": size === "lg",
        },
        className
      )}
      {...props}
    />
  )
)
Spinner.displayName = "Spinner"

export { Spinner }
