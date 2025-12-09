# Design Recommendations for TaskPilotAI

## 🎯 Visual Design Direction

### Color Palette

#### Primary Colors
```
Blue (Primary Action)
- Light: #E0F2FE    (blue-100)
- Main:  #0EA5E9    (blue-500)
- Dark:  #0284C7    (blue-600)
- Darker: #0c4a6e   (blue-900)

Usage: CTAs, links, navigation, focused states
```

#### Status Colors
```
Success (Completed Tasks)
- Light: #D1FAE5    (emerald-100)
- Main:  #10B981    (emerald-500)
- Dark:  #059669    (emerald-600)

Warning (Pending Tasks)
- Light: #FEF3C7    (amber-100)
- Main:  #F59E0B    (amber-500)
- Dark:  #D97706    (amber-600)

Error (Errors, Destructive)
- Light: #FEE2E2    (red-100)
- Main:  #EF4444    (red-500)
- Dark:  #DC2626    (red-600)

Info (Notifications)
- Light: #E0E7FF    (indigo-100)
- Main:  #6366F1    (indigo-500)
- Dark:  #4F46E5    (indigo-600)
```

#### Neutral Colors
```
Gray Scale (for text, borders, backgrounds)
- 50:  #F9FAFB     (lightest - subtle backgrounds)
- 100: #F3F4F6     (light backgrounds)
- 200: #E5E7EB     (subtle borders)
- 300: #D1D5DB     (active borders)
- 400: #9CA3AF     (muted text)
- 500: #6B7280     (secondary text)
- 600: #4B5563     (primary text)
- 700: #374151     (dark text)
- 800: #1F2937     (darker text)
- 900: #111827     (darkest - dark mode bg)
```

### Typography Scale

```typescript
// Font Stack
Font Family: 'Inter', 'Segoe UI', system-ui, sans-serif
Font Smoothing: Antialiased

// Sizes & Weights
Display:    3.5rem  (56px)  - Bold    - Hero text
H1:         2.25rem (36px)  - Bold    - Page title
H2:         1.5rem  (24px)  - Semibold- Section title
H3:         1.25rem (20px)  - Semibold- Card title
Body:       1rem    (16px)  - Regular - Paragraph
Label:      0.875rem(14px)  - Medium  - Form labels
Small:      0.75rem (12px)  - Regular - Captions

// Line Heights
Headings:   120% (tight, conveying hierarchy)
Body:       150% (comfortable reading)
Labels:     140% (balanced form readability)
```

### Spacing Scale

```
8px baseline system:
xs:   4px   (very tight spacing)
sm:   8px   (tight, between elements)
md:  16px   (default, card padding)
lg:  24px   (section padding)
xl:  32px   (large gaps)
2xl: 48px   (major sections)
3xl: 64px   (hero sections)
```

### Border Radius

```
sm:   4px    (small form inputs)
md:   8px    (standard inputs, small cards)
lg:  12px    (cards, containers)
xl:  16px    (large modals)
full: 9999px (pills, avatars)
```

### Shadow System

```
subtle:  0 1px 2px 0 rgba(0,0,0,0.05)
         (Used on: cards, slight elevation)

medium:  0 4px 6px -1px rgba(0,0,0,0.1)
         (Used on: dropdowns, hover states)

large:   0 10px 15px -3px rgba(0,0,0,0.1)
         (Used on: modals, floating elements)

elevated: 0 20px 25px -5px rgba(0,0,0,0.1)
          (Used on: top-level overlays)
```

---

## 📐 Layout Patterns

### Desktop Layout (1280px+)
```
┌─────────────────────────────────────┐
│  Header (Sticky)                    │
├──────────┬──────────────────────────┤
│          │                          │
│ Sidebar  │  Main Content            │
│ (256px)  │  (auto)                  │
│          │                          │
│          │                          │
└──────────┴──────────────────────────┘
```

### Tablet Layout (768px - 1024px)
```
┌──────────────────────────────┐
│  Header (Sticky)             │
├──────────────────────────────┤
│  Sidebar Toggle ┌─────────┐  │
│  Main Content   │Sidebar? │  │
│                 └─────────┘  │
└──────────────────────────────┘
```

### Mobile Layout (<768px)
```
┌──────────────────┐
│ Header (Sticky)  │
├──────────────────┤
│ Main Content     │
│ (Full width)     │
│                  │
│ Sidebar: Drawer  │
└──────────────────┘
```

---

## 🎨 Component Design

### Button Variants

#### Primary Button
```
Background: Blue-600
Text: White
Padding: 10px 16px
Border Radius: 8px
Font: Medium 14px
Hover: Blue-700 + shadow
Active: Scale 95%
Disabled: Opacity 50%
```

#### Secondary Button
```
Background: Gray-100
Text: Gray-900
Padding: 10px 16px
Border: 1px Gray-300
Border Radius: 8px
Font: Medium 14px
Hover: Gray-200
Active: Scale 95%
Disabled: Opacity 50%
```

#### Danger Button
```
Background: Red-50
Text: Red-600
Border: 1px Red-200
Padding: 10px 16px
Hover: Red-100
Active: Scale 95%
```

#### Ghost Button
```
Background: Transparent
Text: Blue-600
Padding: 10px 16px
Hover: Blue-50
Active: Blue-100
```

### Form Input Design

```
Default State:
├─ Background: White
├─ Border: 1px Gray-300
├─ Padding: 10px 12px
├─ Border Radius: 8px
├─ Font: 14px Regular
└─ Height: 40px (48px for mobile)

Focus State:
├─ Background: White
├─ Border: 2px Blue-500
├─ Ring: 2px Blue-200
├─ Shadow: subtle
└─ Transition: 150ms

Error State:
├─ Background: White
├─ Border: 2px Red-500
├─ Ring: 2px Red-100
└─ Error Message: Red-600 14px

Disabled State:
├─ Background: Gray-50
├─ Border: 1px Gray-200
├─ Cursor: not-allowed
└─ Opacity: 60%
```

### Card Design

```
Standard Card:
├─ Background: White (Light) / Gray-800 (Dark)
├─ Border: 1px Gray-200 (Light) / Gray-700 (Dark)
├─ Border Radius: 12px
├─ Padding: 24px
├─ Shadow: subtle
└─ Hover: shadow increased

Card Header:
├─ Border Bottom: 1px Gray-200
├─ Padding Bottom: 16px
├─ Font Weight: Semibold
└─ Color: Gray-900 (Light) / White (Dark)

Card Content:
├─ Padding: 16px 0
└─ Color: Gray-600 (Light) / Gray-300 (Dark)

Card Footer:
├─ Border Top: 1px Gray-200
├─ Padding Top: 16px
└─ Display: flex justify-end gap-2
```

---

## 🔄 Interaction Patterns

### Hover Effects

```
Buttons:
├─ Color: Slightly darker
├─ Shadow: Increased
├─ Scale: 102%
└─ Duration: 150ms

Cards:
├─ Shadow: Increased (medium)
├─ Background: Slightly lighter
└─ Duration: 200ms

Links:
├─ Color: Slightly darker
├─ Underline: Appears
└─ Duration: 150ms
```

### Loading States

```
Button Loading:
├─ Show spinner: Inline
├─ Text: "Loading..." or "Saving..."
├─ Disabled: true
└─ Cursor: not-allowed

Content Loading:
├─ Show skeleton: Matches content shape
├─ Background: Gray-200 animated pulse
├─ Duration: Fade in/out 2s
└─ Repeat: Multiple times

Page Transition:
├─ Fade out: 100ms opacity 1 → 0
├─ Fade in: 300ms opacity 0 → 1
└─ Stagger children: 50ms delay
```

### Error States

```
Form Error:
├─ Border: Red-500
├─ Ring: Red-200
├─ Message: Below input, Red-600
├─ Icon: ⚠️ or ✕
└─ Animation: Shake (if severe)

Alert Error:
├─ Background: Red-50
├─ Border: Red-200
├─ Text: Red-800
├─ Icon: ⚠️
└─ Action: Close or Retry
```

### Success States

```
Success Message:
├─ Background: Green-50
├─ Border: Green-200
├─ Text: Green-800
├─ Icon: ✓
└─ Duration: Auto-close 3-4s

Toast Notification:
├─ Position: Bottom-right
├─ Slide in: From bottom, 300ms
├─ Stay: 4 seconds
├─ Slide out: 200ms
└─ Z-index: Top layer
```

---

## 🌙 Dark Mode Color Mapping

```
Light Mode → Dark Mode

White (#FFFFFF)           → Gray-900 (#111827)
Gray-50 (#F9FAFB)        → Gray-800 (#1F2937)
Gray-100 (#F3F4F6)       → Gray-700 (#374151)
Gray-200 (#E5E7EB)       → Gray-600 (#4B5563)
Gray-600 (#4B5563)       → Gray-300 (#D1D5DB)
Gray-900 (#111827)       → White (#FFFFFF)

Text: Dark → Light
Background: Light → Dark
Border: Lighter → Darker
Shadow: Darker → Lighter

Accent colors remain same (Blue, Green, Red, etc.)
But backgrounds adjusted for contrast
```

---

## 📱 Responsive Breakpoints

### Mobile First Approach

```
Mobile (< 640px)
├─ 1 column layout
├─ Full width cards
├─ Stacked navigation
├─ Large buttons (48px height)
└─ Padding: 16px

Tablet (640px - 1024px)
├─ 2 column layout
├─ Sidebar navigation
├─ Medium buttons (40px height)
└─ Padding: 24px

Desktop (1024px - 1280px)
├─ 3 column layout
├─ Full sidebar
├─ Standard buttons (40px height)
└─ Padding: 32px

Large Desktop (> 1280px)
├─ 3-4 column layout
├─ Max-width container (1280px)
├─ Standard buttons
└─ Padding: 32px
```

---

## ✨ Animation Specifications

### Timing Functions

```
swift:        cubic-bezier(0.25, 0.46, 0.45, 0.94)  [Fast]
smooth:       cubic-bezier(0.4, 0, 0.2, 1)          [Smooth]
gentle:       cubic-bezier(0.33, 0.66, 0.66, 1)    [Gentle]
```

### Duration Guidelines

```
Fast:         100-150ms  (button clicks, hovers)
Normal:       200-300ms  (transitions, page changes)
Slow:         500-1000ms (modals, overlays)
Very Slow:    1000-2000ms (loading indicators)
```

### Animation Types

```
Fade:      Opacity 0% → 100%        [300ms smooth]
Slide:     Transform X/Y             [200ms swift]
Scale:     Transform scale()          [150ms smooth]
Rotate:    Transform rotate()         [200ms swift]
Bounce:    Spring-like movement       [500ms gentle]
```

---

## 🎯 Page-Specific Design

### Sign-In Page

```
Layout: Split screen (left: brand, right: form)

Left Side (50%):
├─ Background: Blue gradient
├─ Logo: Large, white
├─ Tagline: White text, centered
└─ Spacing: Centered vertically

Right Side (50%):
├─ Background: White
├─ Card: 400px wide, centered
├─ Title: "Welcome Back" (28px)
├─ Form: 300px wide
├─ Inputs: Full width
├─ Button: Full width (40px height)
├─ Links: Centered below button
└─ OAuth: Below divider

Mobile:
├─ Stack vertically (hide brand)
├─ Full width form
└─ Padding: 16px all sides
```

### Dashboard Page

```
Header (56px, sticky):
├─ Logo: 24px (left)
├─ Search: 300px (center)
├─ Icons: Notification, Theme (right)
└─ Profile: Avatar dropdown (right)

Sidebar (256px, fixed on desktop):
├─ Logo: 32px
├─ Nav Items: 12px padding each
├─ Active: Blue-600 background
├─ Collapsed: Hidden on mobile
└─ Bottom: Sign out button

Main Content:
├─ Metrics Grid:
│  ├─ Desktop: 4 columns
│  ├─ Tablet: 2 columns
│  └─ Mobile: 1 column
│
├─ Create Task Section:
│  ├─ Button: "+ Add Task"
│  └─ Modal on click
│
└─ Task List:
   ├─ Filters: All / Active / Completed
   ├─ Search: Full width
   ├─ Cards: Full width
   ├─ Empty State: Centered
   └─ Pagination: Bottom, centered
```

### Settings Page

```
Layout: Two column (left: sidebar nav, right: content)

Left Sidebar (200px):
├─ Nav Items:
│  ├─ Profile
│  ├─ Preferences
│  ├─ Security
│  ├─ Data
│  └─ Help
└─ Active: Blue highlight

Right Content:
├─ Section Header: 24px bold
├─ Subsections: 18px semibold
├─ Form Groups: 24px spacing
├─ Cards: Padded sections
└─ Buttons: Primary/Secondary pair

Mobile:
├─ Stack navigation
├─ Tabs instead of sidebar
└─ Full width content
```

---

## 🔍 Accessibility Specifications

### Color Contrast

```
Normal Text:
├─ Minimum: 4.5:1 (WCAG AA)
├─ Target: 7:1 (WCAG AAA)
└─ Tested: On light & dark backgrounds

Large Text (18pt+):
├─ Minimum: 3:1 (WCAG AA)
└─ Target: 4.5:1 (WCAG AAA)

UI Components (buttons, inputs):
├─ Minimum: 3:1 (WCAG AA)
└─ Tested: All states (default, hover, focus)
```

### Focus Indicators

```
Focus Ring:
├─ Width: 2px
├─ Color: Blue-500 (light) / Blue-400 (dark)
├─ Offset: 2px from element
└─ Visible: All interactive elements

Keyboard Navigation:
├─ Tab: Forward through focusable elements
├─ Shift+Tab: Backward
├─ Enter/Space: Activate button
├─ Arrow Keys: Menu navigation
└─ Escape: Close modals
```

### Screen Reader Support

```
Forms:
├─ Labels: Explicitly associated <label> tags
├─ Errors: aria-describedby with error ID
├─ Hints: aria-describedby with hint ID
└─ Required: aria-required="true"

Images/Icons:
├─ Alt text: Descriptive for content
├─ Decorative: Empty alt or role="presentation"
└─ Icons in buttons: aria-label or title

Lists:
├─ Role: list/listitem properly nested
├─ Empty: aria-label="No items"
└─ Loading: aria-live="polite" for updates
```

---

## 📊 Design Token Variables

### CSS Custom Properties

```css
:root {
  /* Colors */
  --color-primary: #0EA5E9;
  --color-primary-light: #E0F2FE;
  --color-primary-dark: #0284C7;

  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;

  --color-text: #111827;
  --color-text-secondary: #6B7280;
  --color-background: #FFFFFF;

  /* Typography */
  --font-family: 'Inter', system-ui, sans-serif;
  --font-size-base: 16px;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);

  /* Transitions */
  --transition-fast: 150ms;
  --transition-normal: 300ms;
  --transition-slow: 500ms;

  /* Z-Index Scale */
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-modal-backdrop: 300;
  --z-modal: 310;
  --z-tooltip: 320;
}
```

---

## 📋 Implementation Checklist

### Phase 1 Deliverables
- [ ] Tailwind config with custom colors
- [ ] CSS custom properties defined
- [ ] Typography scale configured
- [ ] Spacing scale established
- [ ] Shadow system defined
- [ ] Border radius system defined

### Phase 2 Deliverables
- [ ] shadcn/ui components installed
- [ ] Button variants created
- [ ] Form components created
- [ ] Card components created
- [ ] Modal components created

### Phase 3+ Verification
- [ ] Colors match specification
- [ ] Typography follows scale
- [ ] Spacing consistent throughout
- [ ] Shadows applied correctly
- [ ] Animations at specified durations
- [ ] Hover/focus states visible
- [ ] Dark mode colors accurate
- [ ] Responsive breakpoints work
- [ ] Accessibility standards met
- [ ] Performance metrics green

---

## 📸 Visual Examples

### Before & After

#### Current Sign-In
```
Basic card
Blue gradient background
Simple form
No visual hierarchy
```

#### New Sign-In
```
Split screen layout
Brand on left
Form on right
Clear visual hierarchy
Social login buttons
Password show/hide
Error messaging
Dark mode support
```

#### Current Dashboard
```
3-column stat cards
Inline create form
Basic task list
Limited navigation
```

#### New Dashboard
```
Header with search
Sidebar navigation
4-column metrics
Modal for create task
Multiple task views
Filters & search
Empty states
Loading skeletons
Dark mode support
```

---

## 🚀 Next Steps

1. **Review this document** - Confirm colors, spacing, typography
2. **Create design tokens** - Implement in Tailwind config
3. **Build component library** - shadcn/ui + custom components
4. **Redesign pages** - Apply new design system
5. **User testing** - Gather feedback
6. **Iterate** - Refine based on feedback
7. **Launch** - Deploy to production

---

**Document Created**: December 9, 2025
**Status**: ⏳ Ready for Implementation
**Questions?** Review the accompanying detailed plan and research summary

