# Rule Sections Index

Overview of all performance optimization categories for React and Next.js applications.

## Summary Table

| Category                   | Impact       | Description                                                                 |
|----------------------------|--------------|-----------------------------------------------------------------------------|
| Eliminating Waterfalls     | **CRITICAL** | Remove serial await traps and use Promise-based concurrent fetching pattern |
| Bundle Size Optimization   | **CRITICAL** | Minimize JavaScript weight by using direct imports and dynamic loading       |
| Server-Side Performance    | **HIGH**     | Optimize per-request and cross-request caching and data flows               |
| Client-Side Data Fetching  | **MEDIUM**   | Deduplicate requests and manage global state changes efficiently            |
| Re-render Optimization     | **MEDIUM**   | Minimize unnecessary UI updates with stability hooks and memoization        |
| Rendering Performance      | **MEDIUM**   | Focus on browser-level performance like SVG and DOM structure               |
| JavaScript Performance      | **LOW**      | Standardize data structures and efficient loop management                   |
| Advanced Patterns          | **LOW**      | Specialized patterns using stable refs for callback stability               |

## Active Rules
- `async-parallel.md`: Concurrent fetching with `Promise.all()`
- `bundle-barrel-imports.md`: Minimizing import surface area

## Future Rules
*The additional 40+ rules specified in the SKILL manifest will be expanded into individual files.*
