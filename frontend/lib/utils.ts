/**
 * Utility function to merge class names
 * Simple implementation without external dependencies
 */
export function cn(...inputs: (string | undefined | null | boolean | Record<string, boolean>)[]): string {
  const classes: string[] = []

  for (const input of inputs) {
    if (!input || typeof input === "boolean") continue

    if (typeof input === "string") {
      classes.push(input)
    } else if (typeof input === "object") {
      for (const [key, value] of Object.entries(input)) {
        if (value) classes.push(key)
      }
    }
  }

  return classes.join(" ")
}
