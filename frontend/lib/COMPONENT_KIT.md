# Component Kit - UI Component Library

A collection of production-ready UI components built with Tailwind CSS and the design system tokens defined in this project.

## Components Included

### 1. **Button** (`components/ui/button.tsx`)
A versatile button component with multiple variants and sizes.

**Variants:**
- `default` - Primary action button (blue)
- `secondary` - Secondary action button (gray)
- `destructive` - Destructive action button (red)
- `outline` - Outlined button
- `ghost` - Transparent button
- `link` - Link-style button

**Sizes:**
- `sm` - Small (h-9, text-xs)
- `default` - Default (h-10, text-sm)
- `lg` - Large (h-11, text-base)
- `icon` - Icon button (h-10, w-10)

**Usage:**
```tsx
import { Button } from "@/components/ui"

export function MyComponent() {
  return (
    <>
      <Button>Default Button</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Delete</Button>
      <Button size="lg">Large Button</Button>
    </>
  )
}
```

### 2. **Input** (`components/ui/input.tsx`)
Text input field with focus states and disabled support.

**Features:**
- Border and ring focus states
- Placeholder support
- Disabled state styling
- Full width by default

**Usage:**
```tsx
import { Input } from "@/components/ui"

export function LoginForm() {
  return (
    <Input
      type="email"
      placeholder="Enter your email"
      disabled={false}
    />
  )
}
```

### 3. **Card** (`components/ui/card.tsx`)
Container component with optional header, content, and footer.

**Subcomponents:**
- `Card` - Root container
- `CardHeader` - Header section (p-6)
- `CardTitle` - Title heading (text-2xl font-bold)
- `CardDescription` - Subtitle (text-sm text-gray-600)
- `CardContent` - Main content area (p-6 pt-0)
- `CardFooter` - Footer section (flex items-center p-6 pt-0)

**Usage:**
```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui"

export function UserCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>User Profile</CardTitle>
      </CardHeader>
      <CardContent>
        <p>User information goes here</p>
      </CardContent>
    </Card>
  )
}
```

### 4. **Label** (`components/ui/label-simple.tsx`)
Form label component with accessibility support.

**Usage:**
```tsx
import { Label, Input } from "@/components/ui"

export function FormField() {
  return (
    <>
      <Label htmlFor="email">Email Address</Label>
      <Input id="email" type="email" />
    </>
  )
}
```

### 5. **Alert** (`components/ui/alert.tsx`)
Message alert component with multiple variants.

**Variants:**
- `default` - Default alert
- `success` - Success message (green)
- `destructive` - Error message (red)
- `warning` - Warning message (amber)

**Subcomponents:**
- `Alert` - Root alert
- `AlertTitle` - Alert title
- `AlertDescription` - Alert description

**Usage:**
```tsx
import { Alert, AlertTitle, AlertDescription } from "@/components/ui"

export function MyAlert() {
  return (
    <Alert variant="success">
      <AlertTitle>Success</AlertTitle>
      <AlertDescription>Your changes have been saved.</AlertDescription>
    </Alert>
  )
}
```

### 6. **Badge** (`components/ui/badge.tsx`)
Small label component for tags and statuses.

**Variants:**
- `default` - Default badge (primary)
- `secondary` - Secondary badge (gray)
- `success` - Success badge (green)
- `destructive` - Destructive badge (red)
- `outline` - Outlined badge

**Usage:**
```tsx
import { Badge } from "@/components/ui"

export function TaskItem() {
  return (
    <>
      <h3>Task Title</h3>
      <Badge variant="success">Completed</Badge>
    </>
  )
}
```

### 7. **Checkbox** (`components/ui/checkbox.tsx`)
Checkbox input with accessible styling.

**Usage:**
```tsx
import { Checkbox, Label } from "@/components/ui"

export function RememberMe() {
  return (
    <div className="flex items-center gap-2">
      <Checkbox id="remember" />
      <Label htmlFor="remember">Remember me</Label>
    </div>
  )
}
```

### 8. **Select** (`components/ui/select.tsx`)
Dropdown select component.

**Usage:**
```tsx
import { Select, Label } from "@/components/ui"

export function StatusFilter() {
  return (
    <>
      <Label htmlFor="status">Status</Label>
      <Select id="status">
        <option>All</option>
        <option>Pending</option>
        <option>Completed</option>
      </Select>
    </>
  )
}
```

### 9. **Textarea** (`components/ui/textarea.tsx`)
Multi-line text input field.

**Features:**
- Minimum height (min-h-[80px])
- No resize by default (resize-none)
- Same focus styling as Input

**Usage:**
```tsx
import { Textarea, Label } from "@/components/ui"

export function CommentForm() {
  return (
    <>
      <Label htmlFor="comment">Comment</Label>
      <Textarea id="comment" placeholder="Enter your comment..." />
    </>
  )
}
```

### 10. **Spinner** (`components/ui/spinner.tsx`)
Loading spinner component.

**Sizes:**
- `sm` - Small (w-4, h-4)
- `md` - Medium (w-6, h-6)
- `lg` - Large (w-8, h-8)

**Usage:**
```tsx
import { Spinner } from "@/components/ui"
import { Button } from "@/components/ui"

export function LoadingButton() {
  const [loading, setLoading] = useState(false)

  return (
    <Button disabled={loading}>
      {loading ? <Spinner size="sm" /> : "Submit"}
    </Button>
  )
}
```

## Utility Functions

### `cn()` (`lib/utils.ts`)
Combines class names with Tailwind merge support.

**Features:**
- Merges Tailwind classes intelligently
- Prevents class conflicts
- Supports conditional classes with clsx

**Usage:**
```tsx
import { cn } from "@/lib/utils"

export function CustomComponent({ className }) {
  return (
    <div className={cn(
      "base-class",
      active && "active-class",
      className
    )}>
      Content
    </div>
  )
}
```

## Design System Integration

All components use design tokens from:

### **Colors** (`lib/colors.ts`)
- Primary (blue): #0EA5E9
- Secondary (indigo): #6366F1
- Success (emerald): #22C55E
- Warning (amber): #F59E0B
- Error (red): #EF4444
- Neutral (gray): Gray scale

### **Typography** (`lib/typography.ts`)
- Primary font: Inter (sans-serif)
- Secondary font: Playfair Display (serif)
- Sizes: display, h1-h3, body, small, xsmall
- Weights: regular, medium, semibold, bold

### **Tailwind Config** (`tailwind.config.ts`)
- Spacing: 8px baseline
- Border radius: 4px to full
- Shadows: subtle to elevated
- Transitions: fast (150ms), normal (300ms), slow (500ms)
- Dark mode: Enabled (class strategy)

## Best Practices

1. **Always use the component library** - Don't create custom styles
2. **Leverage variants** - Use component variants instead of custom className overrides
3. **Use semantic HTML** - Components maintain accessibility
4. **Respect the design system** - Colors, spacing, typography are defined globally
5. **Test in dark mode** - All components support dark mode with `dark:` classes
6. **Keep it simple** - Use composition for complex layouts

## Future Enhancements

- [ ] Add Radix UI Dialog/Modal components
- [ ] Add Tabs, Accordion components
- [ ] Add Popover, Tooltip components
- [ ] Add Toast/Notification system
- [ ] Add Form wrapper with validation
- [ ] Add Data Table component
- [ ] Storybook integration and documentation
- [ ] Component test suite
- [ ] Accessibility audit (WCAG 2.1 AA)

## File Structure

```
components/ui/
├── button.tsx              # Button component with variants
├── input.tsx              # Text input component
├── card.tsx               # Card container component
├── label-simple.tsx       # Form label component
├── alert.tsx              # Alert component with variants
├── badge.tsx              # Badge/tag component
├── checkbox.tsx           # Checkbox input
├── select.tsx             # Dropdown select
├── textarea.tsx           # Multi-line textarea
├── spinner.tsx            # Loading spinner
└── index.ts              # Component exports
```

---

**Last Updated:** 2025-12-09
**Version:** 1.0.0
**Status:** Production Ready
