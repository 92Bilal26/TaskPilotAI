/**
 * Typography System - Design Tokens & Constants
 *
 * This file defines all typography settings used throughout the application.
 * Built on Inter (sans-serif) for body text and Playfair Display (serif) for headings.
 *
 * Base size: 16px (1rem)
 * Scale ratio: 1.125 (major third) - balanced, professional progression
 */

/**
 * FONT FAMILIES
 * CSS variables are injected by next/font/google in layout.tsx
 */
export const FONT_FAMILIES = {
  base: 'var(--font-inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif)',
  sans: 'var(--font-inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif)',
  serif: 'var(--font-playfair, Georgia, serif)',
  mono: '"Menlo", "Monaco", "Courier New", monospace',
} as const;

/**
 * FONT WEIGHTS
 * Defined weights available in our font family
 */
export const FONT_WEIGHTS = {
  thin: 100,
  extralight: 200,
  light: 300,
  normal: 400,
  regular: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
  extrabold: 800,
  black: 900,
} as const;

/**
 * FONT SIZES & LINE HEIGHTS
 * Responsive typography scale (mobile-first)
 *
 * Format: [fontSize, { lineHeight: "...", fontWeight: ... }]
 * Uses rem units for accessibility (respects user's base font size)
 */
export const FONT_SIZES = {
  // Display - for page hero sections
  display: {
    mobile: "2rem",      // 32px
    tablet: "2.5rem",    // 40px
    desktop: "3.5rem",   // 56px
    lineHeight: "1.2",
    fontWeight: FONT_WEIGHTS.bold,
    family: FONT_FAMILIES.serif,
  },

  // Heading 1 - main page titles
  h1: {
    mobile: "1.75rem",   // 28px
    tablet: "2rem",      // 32px
    desktop: "2.25rem",  // 36px
    lineHeight: "1.2",
    fontWeight: FONT_WEIGHTS.bold,
    family: FONT_FAMILIES.serif,
  },

  // Heading 2 - section titles
  h2: {
    mobile: "1.5rem",    // 24px
    tablet: "1.75rem",   // 28px
    desktop: "1.5rem",   // 24px
    lineHeight: "1.3",
    fontWeight: FONT_WEIGHTS.semibold,
    family: FONT_FAMILIES.serif,
  },

  // Heading 3 - subsection titles
  h3: {
    mobile: "1.25rem",   // 20px
    tablet: "1.25rem",   // 20px
    desktop: "1.25rem",  // 20px
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.semibold,
    family: FONT_FAMILIES.serif,
  },

  // Body - main content, default text
  body: {
    mobile: "1rem",      // 16px (base)
    tablet: "1rem",      // 16px
    desktop: "1rem",     // 16px
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.normal,
    family: FONT_FAMILIES.base,
  },

  // Small - secondary info, labels, hints
  small: {
    mobile: "0.875rem",  // 14px
    tablet: "0.875rem",  // 14px
    desktop: "0.875rem", // 14px
    lineHeight: "1.25",
    fontWeight: FONT_WEIGHTS.normal,
    family: FONT_FAMILIES.base,
  },

  // Extra Small - captions, metadata, badges
  xsmall: {
    mobile: "0.75rem",   // 12px
    tablet: "0.75rem",   // 12px
    desktop: "0.75rem",  // 12px
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.normal,
    family: FONT_FAMILIES.base,
  },

  // Extra Extra Small - helper text, icons
  xxsmall: {
    mobile: "0.625rem",  // 10px
    tablet: "0.625rem",  // 10px
    desktop: "0.625rem", // 10px
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.normal,
    family: FONT_FAMILIES.base,
  },
} as const;

/**
 * TYPOGRAPHY PRESETS
 * Common typography combinations for quick application
 */
export const TYPOGRAPHY_PRESETS = {
  // Display styles
  displayLarge: {
    fontSize: "3.5rem",
    lineHeight: "1.2",
    fontWeight: FONT_WEIGHTS.bold,
    fontFamily: FONT_FAMILIES.serif,
  },
  displayMedium: {
    fontSize: "2.75rem",
    lineHeight: "1.2",
    fontWeight: FONT_WEIGHTS.bold,
    fontFamily: FONT_FAMILIES.serif,
  },

  // Heading styles
  headingXL: {
    fontSize: "2.25rem",
    lineHeight: "1.2",
    fontWeight: FONT_WEIGHTS.bold,
    fontFamily: FONT_FAMILIES.serif,
  },
  headingLarge: {
    fontSize: "1.875rem",
    lineHeight: "1.3",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.serif,
  },
  headingMedium: {
    fontSize: "1.5rem",
    lineHeight: "1.3",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.serif,
  },
  headingSmall: {
    fontSize: "1.25rem",
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.serif,
  },

  // Body styles
  bodyLarge: {
    fontSize: "1.125rem",
    lineHeight: "1.6",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.base,
  },
  bodyRegular: {
    fontSize: "1rem",
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.base,
  },
  bodySmall: {
    fontSize: "0.875rem",
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.base,
  },

  // Label styles (form labels, badges)
  labelLarge: {
    fontSize: "1rem",
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.base,
  },
  labelMedium: {
    fontSize: "0.875rem",
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.base,
  },
  labelSmall: {
    fontSize: "0.75rem",
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.base,
  },

  // Caption styles (metadata, hints)
  captionLarge: {
    fontSize: "0.875rem",
    lineHeight: "1.25",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.base,
  },
  captionSmall: {
    fontSize: "0.75rem",
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.base,
  },

  // Button text
  button: {
    fontSize: "1rem",
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.base,
    textTransform: "none",
  },
  buttonSmall: {
    fontSize: "0.875rem",
    lineHeight: "1.25",
    fontWeight: FONT_WEIGHTS.semibold,
    fontFamily: FONT_FAMILIES.base,
  },

  // Code/Monospace
  code: {
    fontSize: "0.875rem",
    lineHeight: "1.5",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.mono,
  },
  codeSmall: {
    fontSize: "0.75rem",
    lineHeight: "1.4",
    fontWeight: FONT_WEIGHTS.normal,
    fontFamily: FONT_FAMILIES.mono,
  },
} as const;

/**
 * RESPONSIVE TYPOGRAPHY MAPPING
 * Maps breakpoints to appropriate font sizes
 */
export const RESPONSIVE_TYPOGRAPHY = {
  headings: {
    h1: {
      mobile: "1.75rem",
      tablet: "2rem",
      desktop: "2.25rem",
    },
    h2: {
      mobile: "1.5rem",
      tablet: "1.75rem",
      desktop: "1.5rem",
    },
    h3: {
      mobile: "1.25rem",
      tablet: "1.25rem",
      desktop: "1.25rem",
    },
  },
  body: {
    mobile: "1rem",
    tablet: "1rem",
    desktop: "1rem",
  },
} as const;

/**
 * LETTER SPACING
 * For specific typographic effects
 */
export const LETTER_SPACING = {
  tighter: "-0.025em",   // -0.4px at 16px
  tight: "-0.0125em",    // -0.2px at 16px
  normal: "0em",         // 0px (default)
  wide: "0.025em",       // 0.4px at 16px
  wider: "0.05em",       // 0.8px at 16px
  widest: "0.1em",       // 1.6px at 16px
} as const;

/**
 * TEXT TRANSFORM
 * Common text transformation utilities
 */
export const TEXT_TRANSFORM = {
  uppercase: "uppercase",
  lowercase: "lowercase",
  capitalize: "capitalize",
  normal: "none",
} as const;

/**
 * TYPOGRAPHY SCALE INFORMATION
 * Reference for understanding the typographic hierarchy
 *
 * DISPLAY SIZES (Hero/Impact):
 * - 56px: For page hero, main headlines
 *
 * HEADING SIZES (Hierarchy):
 * - H1: 36px - Main page title
 * - H2: 24px - Section titles
 * - H3: 20px - Subsection titles
 *
 * BODY TEXT (Readability):
 * - Body: 16px (1rem) - Primary content
 * - Small: 14px - Secondary info
 * - XSmall: 12px - Captions, badges
 *
 * LINE HEIGHT GUIDELINES:
 * - Headings: 1.2-1.4 (tighter, more compact)
 * - Body: 1.5-1.6 (optimal readability)
 * - Captions: 1.4 (compact, but readable)
 *
 * FONT WEIGHT USAGE:
 * - Regular (400): Body text, normal content
 * - Semibold (600): Labels, buttons, subheadings
 * - Bold (700): Headings, emphasis, H1
 *
 * RESPONSIVE STRATEGY:
 * - Mobile: Smaller headings (28px-20px)
 * - Tablet: Medium headings (32px-20px)
 * - Desktop: Larger headings (36px-20px)
 * - Body stays consistent at 16px across all breakpoints
 *
 * ACCESSIBILITY CONSIDERATIONS:
 * - Minimum 16px for body text (prevent zoom on iOS)
 * - Line height ≥1.5 for improved readability
 * - Sufficient contrast with WCAG AA (4.5:1) minimum
 * - Max line length ~60-70 characters for optimal reading
 */

/**
 * Helper function to get CSS properties for a typography preset
 * Usage: getTyoographyCSS('headingMedium')
 */
export function getTypographyCSS(
  preset: keyof typeof TYPOGRAPHY_PRESETS
): Record<string, string | number> {
  return TYPOGRAPHY_PRESETS[preset];
}

/**
 * Helper function to get responsive font size
 * Usage: getResponsiveFontSize('h1')
 */
export function getResponsiveFontSize(
  heading: keyof typeof RESPONSIVE_TYPOGRAPHY.headings
): Record<string, string> {
  return RESPONSIVE_TYPOGRAPHY.headings[heading];
}
