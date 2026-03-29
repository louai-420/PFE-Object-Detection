# Frontend Best Practices (2025 Edition)

This guide covers modern tools, architecture, code quality patterns, and Core Web Vitals targets for Senior Frontend Engineers.

## 1. Tooling and Stack Selection

- **Build Tools:** Vite is the standard for non-SSR React apps, replacing CRA and legacy Webpack due to the speed of esbuild/Rollup. Next.js is standard for full-stack and SSR/SSG apps.
- **Styling:** Tailwind CSS remains the industry default for utility-first styling. CSS Modules form the fallback for isolated styled components.
- **Formatting:** Prettier ensures consistent code formatting format-on-save. ESLint catches structural code errors.
- **Testing:** ViTest has replaced Jest for most React / frontend codebases. React Testing Library focuses on testing behavior over implementation details. Playwright is overwhelmingly preferred over Cypress for End-to-End (E2E) testing.

## 2. Core Web Vitals

Google's ranking algorithm focuses heavily on these three metrics. You must test these using real field data (CrUX) and Lighthouse.

- **Largest Contentful Paint (LCP): < 2.5s.** Measures loading speed. The largest element (usually a hero image or H1) must paint quickly. Add `priority={true}` to large `next/image` tags above the fold. 
- **Interaction to Next Paint (INP): < 200ms.** Replaced FID in March 2024. Measures total UI responsiveness against ALL user interactions. Mitigate INP by wrapping heavy JS tasks in `scheduler.yield()` or Web Workers, keeping the main thread clear.
- **Cumulative Layout Shift (CLS): < 0.1.** Measures visual stability. Always reserve space for images and ads by providing `width` and `height`, and configure `display: 'swap'` on web fonts to prevent shifting text.

## 3. Project Architecture

Structure large front-end applications by feature (domain-driven design), rather than by type, to decouple massive monolithic applications.

```
src/
  features/
    authentication/
      components/
      hooks/
      api/
    dashboard/
      components/
      hooks/
      utils/
  components/      // Generic UI elements (Button, Input)
  lib/             // 3rd party configurations (Axios, Supabase)
  utils/           // Pure helper functions (formatDate)
```

## 4. Accessibility (a11y)

Accessibility is a non-negotiable requirement of Senior Frontend Engineering.

- **Semantic HTML:** Always use `<button>` instead of `<div onClick>`. Use `<nav>`, `<article>`, `<aside>`, and `<dialog>`. 
- **Keyboard Navigation:** Forms must be navigable via Tab/Shift+Tab. Test outlines using keyboard only.
- **ARIA Attributes:** Use `aria-expanded`, `aria-hidden`, and `aria-label` when visual context doesn't exist for screen readers.
- **Color Contrast:** Keep foreground-to-background contrast ratios above 4.5:1 for normal text (WCAG AA). 

```javascript
// Poor Accessibility
<div className="btn" onClick={submit}>Submit</div>

// Senior Accessibility
<button 
  type="submit" 
  className="btn" 
  aria-busy={isLoading}
  disabled={isLoading}
>
  {isLoading ? 'Submitting...' : 'Submit'}
</button>
```

## 5. Clean Context and Prop Drilling

Context API solves localized prop drilling but isn't built for high-frequency updates across an entire application.

- Keep Context boundaries as small as possible (e.g., ThemeProvider wrapping the root, but ModalProvider wrapping just the Dashboard).
- Create custom hooks to consume Context rather than forcing developers to import `useContext` and the Context object manually.

```javascript
// Local Context Hook Pattern
export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
```
