---
name: ui-ux-pro-max
description: >
  Generates professional, production-ready UI/UX across web and mobile platforms
  using an AI-powered design intelligence engine. Selects the optimal design
  system (style, color palette, typography, layout pattern, effects) based on
  the product type and industry. Use when building landing pages, dashboards,
  components, mobile screens, or full interfaces from scratch or by request.
  Do NOT use for backend logic, API design, database schemas, pure refactors
  with no visual output, or explaining existing UI without changing it.
tags: [ui, ux, design-system, frontend, landing-page, dashboard, mobile, accessibility]
version: 2.0.0
---

# UI UX Pro Max

Design intelligence skill for building beautiful, production-ready interfaces
across web and mobile — powered by a reasoning engine with 100 industry-specific
rules, 67 UI styles, 96 color palettes, 57 font pairings, and 99 UX guidelines.

---

## Use this skill when
- User says "build", "create", "design", "make", "implement" + any UI element or page
- User shares a Figma link, screenshot, or design description to implement
- User says "landing page", "dashboard", "component", "form", "mobile app UI"
- User asks to "improve", "redesign", or "make this look better"
- User mentions a product type (SaaS, e-commerce, healthcare, fintech, etc.)
- User says "make it look professional / modern / clean / minimal"

## Do NOT use when
- User is asking for backend, API, database, or server logic with no UI output
- User wants an explanation of existing code without visual changes
- User is doing a pure refactor (performance, code quality) with no design impact
- User asks about design theory or concepts without wanting code generated

---

## Step 1 — Parse the request

Before generating anything, extract:

1. **Product type** — What is this? (SaaS, spa, e-commerce, portfolio, fintech, etc.)
2. **Page or component type** — Landing page, dashboard, form, card, nav, modal, etc.
3. **Tech stack** — React, Next.js, Vue, Nuxt, Svelte, Astro, SwiftUI, Flutter, HTML+Tailwind (default if not specified)
4. **Explicit style preferences** — Did the user mention minimalist, dark, glassmorphism, colorful, etc.?
5. **Functional requirements** — CTA goals, data to display, user flows

If the product type or page type is unclear, make a reasonable assumption and state it.
Do not ask clarifying questions for short tasks — infer and build.

---

## Step 2 — Run the Design System Reasoning Engine

Match the product type against the 100 industry reasoning rules.
Each rule outputs a complete design system recommendation across 7 dimensions:

### 2.1 — Select Landing Pattern

Choose from the 24 conversion-optimized patterns:

| # | Pattern | Best For |
|---|---|---|
| 1 | Hero-Centric + Social Proof | Products with strong visuals + testimonials |
| 2 | Feature-Rich Showcase | SaaS, complex multi-feature products |
| 3 | Conversion-Optimized Funnel | Lead gen, sales pages, product launches |
| 4 | Minimal & Direct | Simple apps, tools, utilities |
| 5 | Video-First Hero | Storytelling brands, consumer products |
| 6 | Interactive Product Demo | Software, dev tools, dashboards |
| 7 | Trust & Authority | B2B enterprise, legal, consulting |
| 8 | Storytelling-Driven | Agencies, nonprofits, brand sites |
| 9 | Pricing-Forward | Subscription products, SaaS |
| 10 | Community-First | Dev communities, forums, marketplaces |
| 11 | Before/After | Beauty, health, fitness, coaching |
| 12 | Data-Driven Proof | Analytics tools, growth platforms |
| 13 | Waitlist / Coming Soon | Early-stage products, pre-launch |
| 14 | Portfolio Showcase | Creatives, designers, photographers |

### 2.2 — Select UI Style

Choose from 67 styles. Key selections by product type:

**General Styles (select 1 primary):**
- **Glassmorphism** → Modern SaaS, fintech dashboards (frosted glass, backdrop blur)
- **Neumorphism** → Health/wellness, meditation apps (soft extruded shadows)
- **Minimalism / Swiss Style** → Enterprise, documentation, B2B tools
- **Claymorphism** → Educational apps, children's, consumer SaaS
- **Neubrutalism** → Gen Z brands, startups, Figma-style tools
- **Aurora UI** → Creative agencies, modern SaaS, AI products
- **AI-Native UI** → AI products, chatbots, copilot interfaces
- **Soft UI Evolution** → Wellness, beauty, premium services
- **Dark Mode (OLED)** → Dev tools, coding platforms, gaming
- **Brutalism** → Design portfolios, art projects
- **Bento Box Grid** → Product pages, dashboards, personal sites
- **Organic Biophilic** → Wellness, sustainability, health brands
- **Cyberpunk UI** → Gaming, crypto, tech hardware
- **Vibrant & Block-based** → Startups, creative agencies
- **3D & Hyperrealism** → Gaming, product showcase
- **Motion-Driven** → Portfolio sites, brand storytelling

**Dashboard-Specific Styles (when building analytics/admin):**
- Data-Dense Dashboard, Heat Map, Executive Dashboard, Real-Time Monitoring,
  Drill-Down Analytics, Comparative Analysis, Predictive Analytics, Financial Dashboard

### 2.3 — Select Color Palette

Output format for every color system:

```
PRIMARY:     <hex> (<name>) — main brand interactions, CTAs
SECONDARY:   <hex> (<name>) — supporting elements, hover states
CTA:         <hex> (<name>) — buttons, conversion actions
BACKGROUND:  <hex> (<name>) — page/surface background
TEXT:        <hex> (<name>) — body text (must pass 4.5:1 contrast on Background)
BORDER:      <hex> (<name>) — dividers, card outlines, inputs
```

**Industry palette mapping (representative examples):**

| Industry | Primary | CTA | Mood |
|---|---|---|---|
| SaaS / Tech | #6366F1 Indigo | #8B5CF6 Violet | Confident, modern |
| Fintech / Banking | #1E3A5F Navy | #0EA5E9 Sky | Trust, stability |
| Healthcare / Medical | #0F766E Teal | #16A34A Green | Clean, healing |
| Beauty / Spa | #E8B4B8 Soft Pink | #D4AF37 Gold | Calming, luxurious |
| E-commerce | #DC2626 Red | #F97316 Orange | Energy, urgency |
| Luxury / Premium | #1C1917 Charcoal | #D4AF37 Gold | Exclusive, refined |
| Education | #7C3AED Violet | #06B6D4 Cyan | Inspiring, vibrant |
| Sustainability | #166534 Forest | #84CC16 Lime | Organic, natural |
| Gaming / Entertainment | #4C1D95 Dark Purple | #EC4899 Hot Pink | Immersive, energetic |
| Legal / Consulting | #1E293B Slate | #0EA5E9 Sky | Authority, clarity |

**Anti-patterns for color (always avoid):**
- Banking / Finance: neon colors, AI purple/pink gradients, cartoon palettes
- Healthcare: aggressive reds, neon greens, dark heavy themes
- Wellness / Spa: harsh contrasts, bright neons, dark mode
- Kids / Education: muted desaturated palettes, corporate blues

### 2.4 — Select Typography Pairing

Format for every typography selection:

```
HEADING:  <Font Name> — <mood description>
BODY:     <Font Name> — <readability note>
ACCENT:   <Font Name> (optional) — <use case>
IMPORT:   <Google Fonts URL or @import>
TAILWIND: fontFamily config object
```

**Key pairings by style:**

| Style | Heading | Body | Mood |
|---|---|---|---|
| SaaS / Tech | Space Grotesk | Inter | Technical, modern |
| Fintech | Sora | DM Sans | Precise, trustworthy |
| Healthcare | Nunito | Open Sans | Friendly, approachable |
| Luxury / Beauty | Cormorant Garamond | Montserrat | Elegant, sophisticated |
| Editorial / Blog | Playfair Display | Source Serif | Classic, editorial |
| AI / Futuristic | Syne | Rajdhani | Forward-looking |
| Creative Agency | Clash Display | Satoshi | Bold, expressive |
| Kids / Fun | Fredoka One | Nunito | Playful, warm |
| Minimal Swiss | DM Serif | DM Sans | Clean, structured |
| Gaming | Exo 2 | Barlow | Strong, dynamic |

### 2.5 — Define Effects & Animations

Specify which effects are appropriate. Format:

```
TRANSITIONS:  <duration range> — <easing>
HOVER:        <effect description>
SHADOWS:      <type and intensity>
BORDER-RADIUS: <range for cards/buttons/inputs>
SPECIAL:      <any signature effects for the style>
AVOID:        <animation anti-patterns for this style>
```

**Examples by style:**
- Glassmorphism: `backdrop-filter: blur(20px)`, `background: rgba(255,255,255,0.1)`, border glow
- Neumorphism: `box-shadow: 6px 6px 12px #b8b9be, -6px -6px 12px #ffffff`, no harsh borders
- Neubrutalism: solid 2-3px black borders, hard drop shadows, zero border-radius
- Claymorphism: large border-radius (24-32px), thick shadows, saturated fill colors
- Minimalism: no shadows or ultra-subtle, generous whitespace, 0-4px radius

### 2.6 — Identify Anti-Patterns to Avoid

Every design system output must include a "AVOID" block:

```
AVOID:
- <industry-specific anti-pattern 1>
- <generic UI anti-pattern 2>
- <accessibility anti-pattern 3>
```

**Universal anti-patterns (always include):**
- Emojis as icons — use SVG (Heroicons, Lucide, Phosphor)
- Missing `cursor-pointer` on interactive elements
- Hover states without smooth transitions (always 150-300ms ease)
- Text contrast below 4.5:1 (WCAG AA)
- Auto-playing media without user consent
- Hamburger menus on desktop
- Walls of text without visual hierarchy
- Missing focus states for keyboard navigation

---

## Step 3 — Output the Design System Block

Before writing any code, always output the complete design system as a readable summary:

```
╔══════════════════════════════════════════════════════════════╗
║  DESIGN SYSTEM — <Project Name>                             ║
╠══════════════════════════════════════════════════════════════╣
║  INDUSTRY:    <detected type>                               ║
║  PATTERN:     <selected landing/dashboard pattern>          ║
║  STYLE:       <primary style name>                          ║
╠══════════════════════════════════════════════════════════════╣
║  COLORS                                                      ║
║    Primary:    <hex> (<name>)                               ║
║    Secondary:  <hex> (<name>)                               ║
║    CTA:        <hex> (<name>)                               ║
║    Background: <hex> (<name>)                               ║
║    Text:       <hex> (<name>)                               ║
║    Border:     <hex> (<name>)                               ║
╠══════════════════════════════════════════════════════════════╣
║  TYPOGRAPHY                                                  ║
║    Heading: <font> — <mood>                                 ║
║    Body:    <font> — <note>                                 ║
║    Import:  <Google Fonts URL>                              ║
╠══════════════════════════════════════════════════════════════╣
║  EFFECTS                                                     ║
║    Transitions: <value>                                     ║
║    Hover:       <description>                               ║
║    Shadows:     <description>                               ║
║    Radius:      <range>                                     ║
╠══════════════════════════════════════════════════════════════╣
║  AVOID                                                       ║
║    ✗ <anti-pattern 1>                                       ║
║    ✗ <anti-pattern 2>                                       ║
║    ✗ <anti-pattern 3>                                       ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Step 4 — Generate the Code

Write production-ready code using the design system. Apply stack-specific rules:

### React / Next.js
- Use Tailwind utility classes for all styling; no inline style unless dynamic
- Components in PascalCase, files in kebab-case
- Use `cn()` (clsx + tailwind-merge) for conditional classes
- All interactive elements need `hover:`, `focus:`, `active:` states
- Use `next/image` for all images; never raw `<img>` in Next.js
- Typed with TypeScript; export interfaces for all props

### HTML + Tailwind (default)
- Semantic HTML5: `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`, `<article>`
- CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Google Fonts via `<link>` in `<head>`
- All interactive elements keyboard-accessible

### Vue / Nuxt
- `<script setup>` + Composition API
- `defineProps` with TypeScript generics
- Use `NuxtLink` instead of `<a>` for internal links in Nuxt
- Pinia for state if needed; no Vuex

### Svelte / SvelteKit
- Prefer `$state` runes (Svelte 5) over stores when possible
- `{#each}` and `{#if}` for template logic
- `on:click` handlers with proper event types

### SwiftUI
- Use `VStack`, `HStack`, `ZStack` for layout
- Apply design tokens as `Color` extensions
- Support `@Environment(\.colorScheme)` for dark mode

### Flutter
- `ThemeData` for design tokens, not hard-coded values
- Use `const` constructors wherever possible
- `MediaQuery` for responsive breakpoints

---

## Step 5 — Stack-Specific UX Guidelines

Apply the relevant guidelines from the 99 UX rules based on what is being built:

### Animation Rules
- Loading states: skeleton screens > spinners for content-heavy pages
- Page transitions: 200-400ms, ease-out curves
- Micro-interactions: 100-150ms, spring/bounce for delight
- Never animate more than 2-3 properties simultaneously
- Always respect `prefers-reduced-motion`: wrap all animations in `@media (prefers-reduced-motion: no-preference)`

### Accessibility Rules (WCAG 2.2 AA minimum)
- Text contrast: 4.5:1 for normal text, 3:1 for large text (18px+ or 14px bold)
- Focus rings: `outline: 2px solid <primary>; outline-offset: 2px` on all interactive elements
- All images need `alt` text; decorative images use `alt=""`
- Form inputs need `<label>` elements, not just placeholders
- Modals trap focus and close on Escape
- Skip links for keyboard users: `<a href="#main-content" class="sr-only focus:not-sr-only">Skip to content</a>`

### Responsive Breakpoints (Tailwind defaults)
```
Mobile:   375px  → base (no prefix)
Tablet:   768px  → md:
Laptop:   1024px → lg:
Desktop:  1280px → xl:
Wide:     1440px → 2xl:
```
Always build mobile-first. Test at all 5 breakpoints before finalizing.

### Form UX Rules
- Show validation inline on blur, not on submit only
- Never disable the submit button — show errors instead
- Success states need visual confirmation (color + icon + text)
- Input labels always visible (not just placeholder as label)
- Error messages must say what went wrong and how to fix it

### Icon Rules
- NEVER use emojis as functional icons
- Use SVG icon libraries: Heroicons, Lucide, Phosphor, or Radix Icons
- Icon + label preferred over icon-only (unless obvious like search/close)
- Icon-only buttons must have `aria-label`

### Z-Index Scale (use consistently)
```
Base content:    0-9
Dropdowns:       100-199
Sticky headers:  200-299
Modals/overlays: 300-399
Tooltips:        400-499
Toasts/alerts:   500-599
```

---

## Step 6 — Pre-Delivery Checklist

Run every output through this checklist before presenting to the user:

### Visual Quality
- [ ] Design system applied consistently (no off-palette colors)
- [ ] Typography hierarchy clear (heading > subheading > body > caption)
- [ ] Spacing consistent (use Tailwind's 4px scale: 4, 8, 12, 16, 24, 32, 48, 64)
- [ ] All interactive elements have hover + active states
- [ ] Shadows and effects match the selected style
- [ ] No emojis used as icons — SVG only

### Accessibility
- [ ] All text passes 4.5:1 contrast ratio on its background
- [ ] All `<img>` have `alt` attributes
- [ ] All form inputs have visible `<label>` elements
- [ ] Focus states visible on all interactive elements
- [ ] `prefers-reduced-motion` respected for animations
- [ ] Semantic HTML used (not div-soup)

### Responsiveness
- [ ] Layout tested mentally at 375px, 768px, 1024px, 1440px
- [ ] No fixed pixel widths that break on mobile
- [ ] Images use responsive sizing (not fixed width/height)
- [ ] Touch targets minimum 44x44px on mobile

### Performance (flag for user if relevant)
- [ ] Images use modern formats (WebP/AVIF) or CDN URLs
- [ ] Fonts loaded with `display=swap`
- [ ] No render-blocking scripts in `<head>` without `defer`/`async`

---

## Step 7 — Persist Design System (when multi-page project)

When the user is building a multi-page or multi-session project, offer to persist
the design system using the Master + Overrides pattern:

```
design-system/
├── MASTER.md           ← Global source of truth
│   Contains: colors, typography, spacing, component styles, effects
└── pages/
    ├── landing.md      ← Page-specific overrides only
    ├── dashboard.md
    └── checkout.md
```

**Retrieval instruction for future sessions:**
> "Read `design-system/MASTER.md`. If `design-system/pages/<page>.md` exists,
> its rules override the Master for this page only. Apply all rules before
> generating any code."

---

## Examples

### Example 1 — SaaS Landing Page (hero request)
**Input:** "Build a landing page for my project management SaaS tool"

**Step 1 output:**
- Product: SaaS / Productivity tool
- Page: Landing page
- Stack: Not specified → default HTML + Tailwind
- Style preference: None stated → reason from product type

**Step 2 Design System:**
- Pattern: Feature-Rich Showcase
- Style: Glassmorphism
- Colors: Indigo primary, Violet CTA, white background
- Fonts: Space Grotesk / Inter
- Effects: Subtle glass cards, smooth hover transitions 200ms
- Avoid: Cartoon elements, bright neons, heavy dark backgrounds

**Expected output:** Full HTML page with semantic structure, hero + features + CTA sections, glassmorphism card components, proper font import, responsive layout.

---

### Example 2 — Healthcare Dashboard
**Input:** "Create a healthcare analytics dashboard with charts"

**Step 1 output:**
- Product: Healthcare / Medical
- Page: Dashboard / Analytics
- Stack: React (inferred from "dashboard" + modern context)
- Style preference: None → reason to clean, accessible

**Step 2 Design System:**
- Style: Accessible & Ethical + Data-Dense Dashboard
- Colors: Teal primary, Green CTA, white background, high-contrast text
- Fonts: Nunito / Open Sans
- Chart types: Line (trends), Bar (comparisons), Donut (distribution), KPI cards
- Avoid: Aggressive reds, dark theme, low-contrast data labels

**Expected output:** React component with responsive grid layout, KPI cards, chart placeholders with Recharts/Chart.js wiring, proper ARIA labels on all data elements.

---

### Example 3 — Mobile Beauty App UI
**Input:** "Design a mobile UI for a beauty booking app"

**Step 1 output:**
- Product: Beauty / Spa / Wellness
- Page: Mobile app screens
- Stack: React Native (inferred from "mobile app")
- Style: Soft UI Evolution

**Step 2 Design System:**
- Colors: Soft Pink primary, Gold CTA, Warm White background
- Fonts: Cormorant Garamond / Montserrat
- Effects: Gentle shadows, rounded cards (24px radius), subtle gradients
- Avoid: Neon accents, dark mode, harsh animations

**Expected output:** React Native components for home screen, booking card, and CTA button with proper TouchableOpacity, safe area handling, and platform-specific spacing.

---

## Constraints

- **Never use emojis as icons** — always SVG. This is the #1 most common UI anti-pattern.
- **Never output a design without running Step 6 checklist** — even mentally.
- **Never hardcode colors outside the design system palette** — if a new color is needed, extend the system.
- **Never ignore the tech stack** — output must match the user's framework. No React in HTML projects, no raw JS in TypeScript projects.
- **Never skip the Design System Block** (Step 3) for any full page or component request — the user needs to see the reasoning.
- **Always use semantic HTML** — `<button>` for buttons, `<a>` for links, `<nav>` for navigation. Never use `<div>` for interactive elements.
- **Do not invent UI patterns** without basis in the 100 industry rules — always trace back to a known pattern.

---

## Output Format

Every response must follow this structure:

```
1. ╔══ DESIGN SYSTEM BLOCK ══╗ (Step 3 output)

2. [Code — fully implemented, production-ready]

3. Pre-Delivery Notes (only flag actual issues found in Step 6)
   - Any checklist items that need user attention
   - Any assumptions made about stack/style

4. Optional: "To persist this design system, run..." (Step 7, only for multi-page projects)
```

---

## Safety

- If the user's design request targets a sensitive industry (healthcare, legal, financial),
  always ensure accessibility and trust signals are prioritized in the design system selection.
- Never generate UI that manipulates users through dark patterns:
  - Hidden unsubscribe options
  - Pre-ticked consent boxes
  - False urgency timers
  - Misleading CTA button labels
- If a design request would result in WCAG failures (e.g. user insists on low-contrast colors),
  flag it clearly and offer a compliant alternative while still implementing their request.

---

## Directory Structure

```
skills/
└── ui-ux/
    ├── SKILL.md                    ← This file
    ├── scripts/
    │   └── search.py               ← Design database search engine
    ├── data/
    │   ├── styles.csv              ← 67 UI styles
    │   ├── colors.csv              ← 96 color palettes
    │   ├── typography.csv          ← 57 font pairings
    │   ├── charts.csv              ← 25 chart types
    │   ├── patterns.csv            ← 24 landing patterns
    │   ├── ux-guidelines.csv       ← 99 UX rules
    │   └── reasoning-rules.json    ← 100 industry rules
    └── resources/
        └── design-system-template.md  ← Master.md template
```

**Using the search script directly:**
```bash
# Generate design system for a product
python3 scripts/search.py "beauty spa wellness" --design-system -p "Project Name"

# Search specific domain
python3 scripts/search.py "glassmorphism" --domain style
python3 scripts/search.py "dashboard" --domain chart
python3 scripts/search.py "elegant serif" --domain typography

# Persist design system
python3 scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp"
python3 scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp" --page "dashboard"
```