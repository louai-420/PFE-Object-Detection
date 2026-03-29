---
name: web-performance-optimization
description: >
  Measures, diagnoses, and fixes web performance issues to improve Core Web
  Vitals (LCP, INP, CLS), SEO rankings, and conversion rates. Covers INP
  optimization (replaced FID March 2024), bundle analysis, image pipelines,
  caching, resource hints, Speculation Rules API, HTTP/3, and Real User
  Monitoring. Use when a site is slow, CWV scores are poor, or a performance
  audit is needed. Do NOT use for backend infrastructure unrelated to
  web delivery, database optimization, or mobile native apps.
tags: [performance, core-web-vitals, seo, lighthouse, cwv, INP, LCP, CLS]
version: 2.0.0
---

# Web Performance Optimization

> "Performance is not a feature — it's the baseline.
> A 100ms improvement in INP can lift mobile conversions by ~10%." — SpeedCurve Research

Performance directly drives SEO rankings, bounce rate, and revenue.
Google has confirmed: Page Experience is a ranking factor.
Core Web Vitals are central to that — sites meeting benchmarks tend to outrank
those that don't, and poor scores drop visibility especially on mobile-first indexing.

---

## Use this skill when
- A site or app is loading slowly or feels sluggish to interact with
- Core Web Vitals (LCP, INP, CLS) scores are in "needs improvement" or "poor"
- Reducing JavaScript bundle size or Time to Interactive (TTI)
- Optimizing images, fonts, or static assets
- Implementing caching strategies or CDN configuration
- Preparing for a performance audit or Lighthouse CI integration
- Debugging why a specific page is slow

## Do NOT use when
- The task is pure backend / database optimization with no web delivery impact
- User wants mobile native app performance (iOS/Android), not web
- Task is DevOps infrastructure unrelated to HTTP delivery
- User only wants to explain what a metric means (answer directly, no audit needed)

---

## ⚠️ CRITICAL — FID IS DEAD. Use INP.

The original metric **First Input Delay (FID) was officially deprecated and
removed** as a Core Web Vital on **March 12, 2024**.

INP officially became a Core Web Vital and replaced FID on March 12, 2024.
FID is no longer a Core Web Vital and has been deprecated.

**Never optimize for FID in 2025+. Always optimize for INP.**

| Metric | Old (Deprecated) | New (Current) |
|--------|-----------------|---------------|
| Responsiveness | FID — first interaction only | INP — ALL interactions, 98th percentile |
| Good threshold | < 100ms | < 200ms |
| Poor threshold | > 300ms | > 500ms |
| What it misses | ❌ All interactions after first | ✅ Captures full session responsiveness |

---

## The 2025 Core Web Vitals

The three Core Web Vitals measure LCP, INP, and CLS — loading performance,
interactivity, and visual stability respectively.

### LCP — Largest Contentful Paint (Loading)
Measures when the largest visible element finishes rendering.

| Score | Threshold | Action |
|-------|-----------|--------|
| ✅ Good | < 2.5s | Maintain |
| ⚠️ Needs Work | 2.5s – 4s | Prioritize |
| ❌ Poor | > 4s | Critical fix |

**Top LCP culprits:** Unoptimized hero images, render-blocking CSS/JS, slow TTFB,
no `fetchpriority="high"` on the LCP element, missing CDN.

### INP — Interaction to Next Paint (Responsiveness) ← NEW
Unlike FID, which only measured the first interaction, INP evaluates all
interactions on the page and reports the slowest response time. This metric
gives a more accurate picture of how users experience your site.

INP measures the complete cycle: **input delay → processing time → presentation delay**.
Google measures this at the 75th percentile of all interactions during a page visit.

| Score | Threshold |
|-------|-----------|
| ✅ Good | < 200ms |
| ⚠️ Needs Work | 200ms – 500ms |
| ❌ Poor | > 500ms |

**Top INP culprits:** Long JavaScript tasks blocking the main thread, heavy
event handlers, layout thrashing during interactions, large React re-renders,
third-party scripts executing during interactions.

### CLS — Cumulative Layout Shift (Visual Stability)
Measures unexpected layout movement during the page's lifetime.

| Score | Threshold |
|-------|-----------|
| ✅ Good | < 0.1 |
| ⚠️ Needs Work | 0.1 – 0.25 |
| ❌ Poor | > 0.25 |

**Top CLS culprits:** Images without dimensions, dynamically injected content
above existing content, web fonts causing FOIT/FOUT, ads without reserved space.

### Supporting Metrics (not CWV but important)

| Metric | Good | Description |
|--------|------|-------------|
| TTFB | < 600ms | Time to First Byte — server response speed |
| FCP | < 1.8s | First Contentful Paint — first pixel rendered |
| TTI | < 3.8s | Time to Interactive — fully interactive |
| TBT | < 200ms | Total Blocking Time — main thread block sum |
| Speed Index | < 3.4s | Visual progress speed |

---

## Step 1 — Establish Baseline

**Never optimize without measuring first.** Always get before/after data.

### Tool Stack

| Tool | Type | Best For |
|------|------|----------|
| **Google Search Console** | Field (real users) | Official CWV for SEO — what Google uses |
| **PageSpeed Insights** | Field + Lab | CrUX field data + Lighthouse lab data |
| **Lighthouse (DevTools)** | Lab | Reproducible audits, CI integration |
| **WebPageTest** | Lab | Deep waterfall, filmstrip, real devices |
| **CrUX Dashboard** | Field | Historical 28-day CWV trends |
| **web-vitals.js** | RUM | Custom Real User Monitoring in production |
| **DebugBear / Calibre** | RUM | Continuous monitoring with regression alerts |
| **Chrome DevTools → Performance** | Lab | Frame-level profiling, long task detection |
| **Chrome DevTools → Network** | Lab | Waterfall, request size, caching |

```bash
# Run Lighthouse from CLI (for CI integration)
npm install -g lighthouse
lighthouse https://yoursite.com --output html --output-path ./report.html

# Run with mobile throttling (matches Google's conditions)
lighthouse https://yoursite.com \
  --throttling.cpuSlowdownMultiplier=4 \
  --throttling.downloadThroughputKbps=1638 \
  --form-factor=mobile \
  --output html
```

### Baseline Template

```markdown
## Performance Baseline — [Site Name] — [Date]

### Field Data (CrUX / Search Console)
- LCP:  ___s  [ ✅ < 2.5 | ⚠️ 2.5-4 | ❌ > 4 ]
- INP:  ___ms [ ✅ < 200 | ⚠️ 200-500 | ❌ > 500 ]
- CLS:  ___   [ ✅ < 0.1 | ⚠️ 0.1-0.25 | ❌ > 0.25 ]
- TTFB: ___ms [ ✅ < 600 | ❌ > 600 ]

### Lab Data (Lighthouse)
- Performance Score: ___/100
- FCP: ___s | TBT: ___ms | Speed Index: ___s

### Bundle
- Total JS (gzipped): ___KB  [ ✅ < 150 | ⚠️ 150-300 | ❌ > 300 ]
- Total CSS (gzipped): ___KB [ ✅ < 50  | ⚠️ 50-100  | ❌ > 100 ]
- Total Images: ___MB

### Device / Network Context
- Tested on: [ Desktop | Mobile ]
- Network: [ Fast 3G | Slow 4G | Cable ]
```

---

## Step 2 — Diagnose by Metric

### LCP Diagnosis Checklist

```bash
# 1. Identify the LCP element
# Open Chrome DevTools → Performance → Record → Look for "LCP" annotation
# Or: document.querySelector('[loading]') won't help — use Lighthouse

# 2. Check if LCP image is preloaded
# Look for: <link rel="preload" as="image" href="/hero.avif" fetchpriority="high">
# Missing this is the #1 LCP issue on image-heavy pages

# 3. Check TTFB (server response)
# In DevTools Network tab: time to first green bar
# TTFB > 600ms = server/CDN issue, not front-end
```

### INP Diagnosis

```javascript
// Install web-vitals and log INP in production
import { onINP } from 'web-vitals/attribution';

onINP(({ value, attribution }) => {
  console.log('INP:', value, 'ms');
  console.log('Slow interaction element:', attribution.interactionTarget);
  console.log('Event type:', attribution.interactionType);
  // This tells you EXACTLY which element is slow
});
```

```bash
# Find long tasks in DevTools
# Performance tab → look for red triangles on tasks > 50ms
# These are your INP killers — break them up with scheduler.yield()
```

### CLS Diagnosis

```javascript
// Log all layout shifts to find the source
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      console.log('CLS source:', entry.sources, 'value:', entry.value);
    }
  }
}).observe({ type: 'layout-shift', buffered: true });
```

---

## Step 3 — Fix by Priority

### 🔴 P1 — LCP Fixes

#### Hero Image Optimization (most impactful LCP fix)

```html
<!-- ❌ BEFORE: Unoptimized, no priority hints -->
<img src="/hero.jpg" alt="Hero">

<!-- ✅ AFTER: Modern formats, priority hints, dimensions -->
<link rel="preload" as="image" href="/hero.avif"
      imagesrcset="/hero-400.avif 400w, /hero-800.avif 800w, /hero-1200.avif 1200w"
      imagesizes="100vw"
      fetchpriority="high">

<picture>
  <source
    srcset="/hero-400.avif 400w, /hero-800.avif 800w, /hero-1200.avif 1200w"
    sizes="(max-width: 768px) 100vw, 50vw"
    type="image/avif">
  <source
    srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
    sizes="(max-width: 768px) 100vw, 50vw"
    type="image/webp">
  <img
    src="/hero-800.jpg"
    alt="Hero description"
    width="1200"
    height="600"
    loading="eager"
    fetchpriority="high"
    decoding="async">
</picture>
```

#### Reduce TTFB with Early Hints (HTTP 103)

Early Hints is one of the most effective modern performance optimizations
available. By using HTTP 103, you can virtually eliminate the latency gap
between server processing and browser action, leading to faster LCP scores.

```nginx
# Nginx: Send 103 Early Hints before the full response
location / {
  http2_push_preload on;
  add_header Link "</critical.css>; rel=preload; as=style";
  add_header Link "</hero.avif>; rel=preload; as=image; fetchpriority=high";
  # Browser starts loading these while server processes the request
}
```

```javascript
// Cloudflare Workers: Programmatic Early Hints
export default {
  async fetch(request) {
    const earlyHints = new Response(null, {
      status: 103,
      headers: {
        'Link': [
          '</critical.css>; rel=preload; as=style',
          '</hero.avif>; rel=preload; as=image',
        ].join(', ')
      }
    });
    // Send 103 immediately, then process the full response
    return fetch(request);
  }
}
```

#### Inline Critical CSS

```javascript
// postcss-critical-css or critical npm package
// Inline above-the-fold CSS directly in <head>
// Defer the rest
```

```html
<head>
  <!-- Critical CSS inlined — renders above fold without network roundtrip -->
  <style>
    /* Only above-the-fold styles */
    body { margin: 0; font-family: 'Inter', sans-serif; }
    .hero { min-height: 100vh; background: #1a1a2e; }
  </style>

  <!-- Non-critical CSS deferred -->
  <link rel="preload" href="/styles.css" as="style" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/styles.css"></noscript>
</head>
```

---

### 🔴 P1 — INP Fixes (Most important 2025 metric)

#### Break Up Long Tasks

```javascript
// ❌ BAD — 200ms synchronous task blocks all interactions
function processLargeDataset(data) {
  return data.map(expensiveTransform); // Blocks main thread
}

// ✅ GOOD — yield to browser between chunks using scheduler.yield()
async function processLargeDataset(data) {
  const results = [];
  const CHUNK_SIZE = 50;

  for (let i = 0; i < data.length; i += CHUNK_SIZE) {
    const chunk = data.slice(i, i + CHUNK_SIZE);
    results.push(...chunk.map(expensiveTransform));

    // Yield to browser — allows it to process pending interactions
    if ('scheduler' in window && 'yield' in scheduler) {
      await scheduler.yield(); // Chrome 129+ — best option
    } else {
      await new Promise(resolve => setTimeout(resolve, 0)); // Fallback
    }
  }
  return results;
}
```

#### Optimize Event Handlers

```javascript
// ❌ BAD — heavy synchronous handler delays visual feedback
button.addEventListener('click', (e) => {
  const result = heavyComputation(); // Blocks paint
  updateUI(result);
});

// ✅ GOOD — update UI immediately, defer heavy work
button.addEventListener('click', async (e) => {
  // 1. Provide immediate visual feedback first
  button.textContent = 'Processing...';
  button.disabled = true;

  // 2. Yield to let the browser paint the feedback
  await scheduler.yield();

  // 3. Now do the heavy work
  const result = await heavyComputation();
  updateUI(result);
  button.textContent = 'Done';
  button.disabled = false;
});
```

#### Reduce React Re-render Scope (INP in React SPAs)

```tsx
// ❌ BAD — entire parent re-renders on every keystroke
function SearchPage() {
  const [query, setQuery] = useState('');
  const results = expensiveFilter(allData, query); // Runs on every keystroke

  return (
    <div>
      <input onChange={e => setQuery(e.target.value)} />
      <ResultsList results={results} />  {/* Re-renders with parent */}
    </div>
  );
}

// ✅ GOOD — memoize expensive computation, isolate re-render
const ResultsList = memo(({ results }) => (
  <ul>{results.map(r => <li key={r.id}>{r.name}</li>)}</ul>
));

function SearchPage() {
  const [query, setQuery] = useState('');
  const results = useMemo(
    () => expensiveFilter(allData, query),
    [query] // Only recomputes when query changes
  );

  return (
    <div>
      <input onChange={e => setQuery(e.target.value)} />
      <ResultsList results={results} />
    </div>
  );
}
```

#### Defer Third-Party Scripts (Major INP killer)

```html
<!-- ❌ BAD — third-party scripts block interactions on load -->
<script src="https://analytics.com/tracker.js"></script>
<script src="https://support-chat.com/widget.js"></script>

<!-- ✅ GOOD — load after page is interactive -->
<script>
  // Wait for page to be interactive before loading any third party
  window.addEventListener('load', () => {
    // Further delay — load on first user interaction
    const loadThirdParty = () => {
      ['https://analytics.com/tracker.js',
       'https://support-chat.com/widget.js'].forEach(src => {
        const s = document.createElement('script');
        s.src = src;
        s.async = true;
        document.body.appendChild(s);
      });
      // Remove listeners after first load
      ['click', 'scroll', 'keydown'].forEach(e =>
        document.removeEventListener(e, loadThirdParty)
      );
    };

    ['click', 'scroll', 'keydown'].forEach(e =>
      document.addEventListener(e, loadThirdParty, { once: true, passive: true })
    );
  });
</script>
```

---

### 🔴 P1 — CLS Fixes

```html
<!-- Always specify dimensions on images -->
<img src="/product.jpg" alt="Product" width="400" height="300">

<!-- Or use CSS aspect-ratio for responsive images -->
<style>
img { aspect-ratio: 4 / 3; width: 100%; height: auto; }
</style>
```

```css
/* Reserve space for dynamically loaded content */
.ad-container    { min-height: 250px; }
.comment-section { min-height: 400px; }

/* Font display swap prevents FOUT-related CLS */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: optional; /* Best for CLS — no FOUT fallback swap */
}
```

---

### 🟠 P2 — Bundle Size Optimization

```bash
# Analyze bundle composition
npx webpack-bundle-analyzer dist/stats.json
# Or for Vite:
npx vite-bundle-visualizer

# Check a package's size before installing
npx bundlephobia <package-name>
```

```javascript
// Replace heavy libraries with lighter alternatives
// moment.js (67KB) → date-fns (tree-shakeable, 12KB for what you use)
import { format, addDays } from 'date-fns';

// lodash (72KB full) → lodash/individual OR native JS
import uniq from 'lodash/uniq';                    // 5KB vs 72KB
const unique = [...new Set(array)];                 // Native — 0KB

// axios (13KB) → native fetch (0KB)
const data = await fetch('/api').then(r => r.json());
```

```javascript
// Code splitting — lazy load routes and heavy components
// Next.js
import dynamic from 'next/dynamic';
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <div className="skeleton h-64" />,
  ssr: false  // Client-only heavy components
});

// React (Vite / CRA)
const AdminPanel = lazy(() => import('./AdminPanel'));
// Wrap in Suspense at the route level
```

```javascript
// webpack.config.js — enable tree shaking and chunk splitting
module.exports = {
  mode: 'production',
  optimization: {
    usedExports: true,
    sideEffects: false,
    splitChunks: {
      chunks: 'all',
      maxSize: 244000,          // Max 244KB per chunk
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
        }
      }
    }
  }
};
```

**Bundle size targets:**

| Asset | Excellent | Good | Warning |
|-------|-----------|------|---------|
| Total JS (gzipped) | < 100KB | < 200KB | > 300KB |
| Main bundle (gzipped) | < 70KB | < 150KB | > 200KB |
| Total CSS (gzipped) | < 30KB | < 50KB | > 100KB |
| Individual chunk | — | < 244KB | > 500KB |

---

### 🟠 P2 — Image Pipeline

```bash
# Full optimization pipeline with sharp
npm install sharp

# Batch convert all images to WebP + AVIF
node -e "
const sharp = require('sharp');
const fs = require('fs');
const files = fs.readdirSync('./public/images').filter(f => /\.(jpg|jpeg|png)$/i.test(f));
files.forEach(file => {
  const base = file.replace(/\.[^.]+$/, '');
  sharp('./public/images/' + file)
    .webp({ quality: 80 }).toFile('./public/images/' + base + '.webp');
  sharp('./public/images/' + file)
    .avif({ quality: 65 }).toFile('./public/images/' + base + '.avif');
});
"
```

**Size targets by image role:**

| Role | Max Size | Format |
|------|----------|--------|
| Hero / LCP image | < 200KB | AVIF → WebP → JPEG |
| Product images | < 100KB | AVIF → WebP → JPEG |
| Thumbnails | < 30KB | AVIF → WebP |
| Icons / logos | SVG preferred | SVG / WebP |
| Background texture | < 50KB | WebP |

---

### 🟠 P2 — Caching Strategy

```nginx
# Nginx cache headers — fingerprinted static assets (forever cache)
location ~* \.(js|css|woff2|jpg|webp|avif|png|svg)$ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}

# HTML — revalidate every visit
location / {
  add_header Cache-Control "no-cache";  # Revalidate always
}

# API responses — short cache
location /api/ {
  add_header Cache-Control "public, max-age=60, stale-while-revalidate=300";
}
```

```javascript
// Service Worker — cache-first for static, network-first for API
self.addEventListener('fetch', (event) => {
  const { request } = event;

  if (request.url.includes('/api/')) {
    // Network-first for API
    event.respondWith(
      fetch(request).catch(() => caches.match(request))
    );
  } else {
    // Cache-first for static assets
    event.respondWith(
      caches.match(request).then(cached =>
        cached || fetch(request).then(response => {
          const clone = response.clone();
          caches.open('v1').then(cache => cache.put(request, clone));
          return response;
        })
      )
    );
  }
});
```

---

### 🟡 P3 — Modern Navigation Speed

#### Speculation Rules API (Instant page navigation — 2025)

The Speculation Rules API is a new browser feature that allows developers
to hint to the browser which pages to proactively download in the background.
If a page has been downloaded in the background, it can be instantly displayed
to the user when they navigate to it.

```html
<!-- Add to pages where you know the user's next destination -->
<script type="speculationrules">
{
  "prerender": [{
    "where": { "href_matches": "/checkout" },
    "eagerness": "moderate"
  }],
  "prefetch": [{
    "where": { "selector_matches": "a[href^='/products/']" },
    "eagerness": "conservative"
  }]
}
</script>
```

**Eagerness levels:**

| Level | When it triggers | Cost | Best for |
|-------|-----------------|------|---------|
| `immediate` | As soon as page loads | Highest | Near-certain next pages |
| `eager` | On link visible in viewport | High | High-confidence predictions |
| `moderate` | On 10ms hover (desktop) or viewport scroll stop (mobile) | Medium | Likely-but-not-certain |
| `conservative` | On mousedown / touchstart | Lowest | Safe default for most sites |

> ⚠️ Use `prerender` sparingly — it consumes ~100MB RAM per page.
> Use `prefetch` broadly — much cheaper, still significant speed gain.
> Never prerender pages with user-specific content or payment flows.

#### Resource Hints (Critical for LCP + TTFB)

```html
<head>
  <!-- 1. dns-prefetch: Resolve DNS for third-party origins early (cheapest) -->
  <link rel="dns-prefetch" href="https://fonts.googleapis.com">
  <link rel="dns-prefetch" href="https://analytics.com">

  <!-- 2. preconnect: Full TCP + TLS for critical third parties (costlier) -->
  <!-- Use only for 2-3 most critical external origins -->
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- 3. preload: Fetch critical current-page resources immediately -->
  <!-- Use for: LCP image, critical web font, critical JS/CSS -->
  <link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/hero.avif" as="image" fetchpriority="high">

  <!-- 4. prefetch: Fetch NEXT page's resources at low priority -->
  <link rel="prefetch" href="/next-article.html">
</head>
```

---

### 🟡 P3 — HTTP Protocol Upgrade

HTTP/3 (QUIC) is now emerging as the next standard — it runs over UDP
with encryption and offers even faster connection setup. Major CDN providers
report over 60% of their traffic now utilizes the protocol.

```nginx
# Enable HTTP/3 + HTTP/2 with Nginx
server {
  listen 443 ssl;
  listen 443 quic reuseport;           # HTTP/3 (QUIC)
  http2 on;                            # HTTP/2

  ssl_certificate     /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;

  add_header Alt-Svc 'h3=":443"; ma=86400';  # Advertise HTTP/3 support

  # Enable Brotli compression (better than gzip for text)
  brotli on;
  brotli_comp_level 6;
  brotli_types text/html text/css application/javascript application/json;
}
```

**Protocol performance comparison:**

| Protocol | Connection | Multiplexing | Head-of-Line Blocking | Best for |
|---------|------------|--------------|----------------------|---------|
| HTTP/1.1 | 6 connections/origin | ❌ No | ❌ Severe | Legacy only |
| HTTP/2 | 1 connection | ✅ Yes | ⚠️ TCP level | Current standard |
| HTTP/3 | 1 QUIC connection | ✅ Yes | ✅ None | Mobile / lossy networks |

---

## Step 4 — Real User Monitoring (RUM)

Lab data (Lighthouse) is not what Google uses for rankings.
**CrUX field data from real users is the official ranking signal.**

```javascript
// Install web-vitals.js — Google's official library
npm install web-vitals

// Track all Core Web Vitals with attribution
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals/attribution';

function sendToAnalytics({ name, value, rating, attribution }) {
  // Send to your analytics endpoint
  fetch('/api/vitals', {
    method: 'POST',
    body: JSON.stringify({ name, value, rating, page: location.pathname }),
    keepalive: true  // Ensures data is sent even if page is closing
  });
}

onLCP(sendToAnalytics);   // Largest Contentful Paint
onINP(sendToAnalytics);   // Interaction to Next Paint ← most important in 2025
onCLS(sendToAnalytics);   // Cumulative Layout Shift
onFCP(sendToAnalytics);   // First Contentful Paint
onTTFB(sendToAnalytics);  // Time to First Byte
```

**RUM tools comparison:**

| Tool | Free | INP Support | CWV Dashboard |
|------|------|-------------|---------------|
| Google Search Console | ✅ Free | ✅ Yes | ✅ Built-in |
| PageSpeed Insights | ✅ Free | ✅ Yes | Per-URL |
| web-vitals.js + custom | ✅ Free | ✅ Yes | DIY |
| DebugBear | 💰 Paid | ✅ Yes | ✅ Regression alerts |
| Calibre | 💰 Paid | ✅ Yes | ✅ Team dashboards |
| SpeedCurve | 💰 Paid | ✅ Yes | ✅ Film strips |

---

## Step 5 — Performance Budget

A performance budget makes performance a first-class team constraint.
Define it early; enforce it in CI.

```javascript
// lighthouserc.js — fail CI if budgets exceeded
module.exports = {
  ci: {
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 200 }],
        'uses-optimized-images': 'error',
        'uses-webp-images': 'warn',
        'uses-responsive-images': 'error',
      }
    }
  }
};
```

```json
// webpack performance budgets
// webpack.config.js
"performance": {
  "maxAssetSize": 244000,
  "maxEntrypointSize": 244000,
  "hints": "error"
}
```

---

## Anti-Patterns

### ❌ Still Optimizing for FID in 2025
FID was deprecated March 2024. Optimizing for "first input" only misses all
subsequent interactions. Audit for INP — it's a fundamentally harder metric.

### ❌ Lighthouse Score ≠ Real User Experience
Lab scores run on a throttled emulated device — not your users' devices.
A 95 Lighthouse score on a page with heavy React interactions can still have
a poor INP in the field. Always validate with CrUX / Search Console field data.

### ❌ Prerendering Everything with Speculation Rules
Prerendering uses ~100MB RAM per page. Prerendering 10 links on every page = 1GB.
Use `conservative` eagerness and limit prerender to highest-confidence next pages.

### ❌ Over-Using `rel="preconnect"`
Each preconnect opens a TCP+TLS connection that must be maintained. More than
3-4 preconnect hints creates connection overhead that can slow the page.
Use `dns-prefetch` for lower-priority third parties.

### ❌ Lazy Loading Above-the-Fold Images
`loading="lazy"` on LCP images is one of the most common LCP regressions.
Always use `loading="eager"` + `fetchpriority="high"` for the LCP element.

### ❌ Ignoring Mobile Performance
Google uses mobile-first indexing, which means your mobile scores are what
count for rankings. Poor mobile performance is literally costing you customers.
Always test on throttled mobile in Chrome DevTools (CPU 4x slowdown, Slow 4G).

### ❌ Third-Party Scripts in `<head>` Without Defer
Analytics, chat widgets, and marketing pixels in `<head>` without `defer`
or `async` block the entire page render. They also fire during user
interactions and directly tank INP.

---

## Constraints

- **Always measure before optimizing** — never guess where the bottleneck is
- **Always check field data (CrUX/Search Console)** before trusting lab data
- **Never use FID as a target metric** — it's deprecated, optimize for INP
- **Never apply `loading="lazy"` to LCP images** — it delays the most important paint
- **Never prerender more than 2-3 pages** with Speculation Rules — memory cost is real
- **Always test on mobile** with CPU throttling — desktop scores are misleading
- **Always set image dimensions** (width + height) on all `<img>` elements — CLS prevention
- **Never block the main thread** with synchronous tasks > 50ms — breaks INP

---

## Complete 2025 Checklist

### 🔴 Core Web Vitals (Blocking — fix before launch)
- [ ] LCP < 2.5s (check in Search Console field data)
- [ ] INP < 200ms (NOT FID — check with web-vitals.js attribution)
- [ ] CLS < 0.1 (all images have width/height; no dynamic injection above content)
- [ ] TTFB < 600ms (check server, CDN, caching)

### 🔴 Images (Blocking)
- [ ] LCP image: `loading="eager"`, `fetchpriority="high"`, preloaded
- [ ] All images: AVIF/WebP format, responsive srcset, width+height specified
- [ ] Non-LCP images: `loading="lazy"`
- [ ] All images: < 200KB (hero), < 100KB (product), < 30KB (thumb)

### 🔴 JavaScript (Blocking)
- [ ] Total JS gzipped < 200KB
- [ ] Code splitting implemented — no single bundle > 244KB
- [ ] No synchronous tasks > 50ms on main thread
- [ ] Third-party scripts deferred until after interaction

### 🟠 Performance Architecture
- [ ] HTTP/2 or HTTP/3 enabled on server/CDN
- [ ] Brotli compression enabled (better than gzip)
- [ ] Static assets: `Cache-Control: public, max-age=31536000, immutable`
- [ ] Critical CSS inlined; non-critical CSS deferred
- [ ] Web fonts: `font-display: optional` or `swap` with size-adjust fallback
- [ ] Resource hints: `preconnect` for critical origins, `dns-prefetch` for others
- [ ] Early Hints (HTTP 103) configured if server supports it

### 🟠 INP Specific
- [ ] Long tasks (> 50ms) broken up with `scheduler.yield()`
- [ ] Event handlers provide immediate visual feedback before heavy processing
- [ ] React/Vue: Memoization applied to expensive computations
- [ ] No layout thrashing in interaction handlers
- [ ] INP monitored in production with web-vitals.js attribution

### 🟡 Advanced
- [ ] Speculation Rules API implemented for likely next pages
- [ ] Service Worker caching strategy for return visitors
- [ ] Performance budget enforced in CI (Lighthouse CI)
- [ ] Real User Monitoring (RUM) sending CWV data to analytics
- [ ] Performance regression alerts configured

---

## Output Format

```
## Performance Audit — <page/site name>

### Current Scores (Field Data — CrUX)
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| LCP | ___s | < 2.5s | ✅/⚠️/❌ |
| INP | ___ms | < 200ms | ✅/⚠️/❌ |
| CLS | ___ | < 0.1 | ✅/⚠️/❌ |
| TTFB | ___ms | < 600ms | ✅/⚠️/❌ |

### Priority Fixes

🔴 P1 — Blockers (highest ROI)
1. [Fix] → [Expected improvement] → [Code]

🟠 P2 — High Impact
2. [Fix] → [Expected improvement]

🟡 P3 — Optimizations
3. [Fix] → [Expected improvement]

### Expected Results After Fixes
- LCP: ___s → ___s (___% improvement)
- INP: ___ms → ___ms
- CLS: ___ → ___
- Lighthouse: ___/100 → ___/100
```