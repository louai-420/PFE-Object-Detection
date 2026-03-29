# Next.js Optimization Guide (2025 Edition)

This guide focuses on optimizing Next.js applications using the App Router architecture.

## 1. Data Fetching Strategies

Next.js fundamentally changed data fetching with the App Router. The `getServerSideProps` and `getStaticProps` patterns are deprecated in favor of native `fetch`.

### Standard API Routes
- **RSC Fetching:** Server Components run directly on the backend. `fetch` requests inside an RSC happen with Zero Cilent Latency.
- **Cache Control:** Native `fetch` is extended with a caching API.

```javascript
// ISR Configuration: Revalidates every 60 seconds
const res = await fetch('https://api.com/data', { 
  next: { revalidate: 60 } 
});

// Avoid caching dynamic dashboard data
const res = await fetch('https://api.com/user', { 
  cache: 'no-store' 
});
```

### Server Actions
Use Server Actions for mutations (POST/PUT/DELETE). They allow client components to call asynchronous server functions without creating an API endpoint.

```javascript
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData) {
  const content = formData.get('content')
  await db.posts.insert({ content })
  revalidatePath('/posts') // Flush cache
  redirect('/posts')       // Redirect client
}
```

## 2. Streaming and Partial Hydration

To prevent slow server-side queries from blocking the entire page render, wrap components in React Suspense. This sends the shell of the page immediately, and streams the heavy component when it resolves.

```javascript
import { Suspense } from 'react'
import { Skeleton } from '@/components/ui'
import HeavyAnalyticsComponent from './Analytics'

export default function Dashboard() {
  return (
    <main>
      <h1>DashboardOverview</h1>
      <Suspense fallback={<Skeleton className="h-40 w-full" />}>
         <HeavyAnalyticsComponent />
      </Suspense>
    </main>
  )
}
```

Use `loading.js` for entire-page loading barriers at the route level.

## 3. Asset Optimization

### Images
Always use `next/image` (`next/legacy/image` shouldn't be used).

```javascript
import Image from 'next/image'

// For LCP (Largest Contentful Paint) images above the fold
<Image 
  src="/hero.webp" 
  alt="Hero" 
  priority // Prevents lazy loading, preloads the image
  width={1200}
  height={600}
/>

// Remote images require defining remotePatterns in next.config.js
```

### Fonts
Avoid external render-blocking font requests. `next/font` downloads and hosts the font locally at build time.

```javascript
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Prevents FOUT (Flash of Unstyled Text)
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

## 4. Metadata and SEO

Use the built-in Metadata API inside your `page.jsx` or `layout.jsx`. Use `generateMetadata` for dynamic data.

```javascript
export async function generateMetadata({ params }) {
  const product = await fetchProduct(params.id)
  return {
    title: product.name,
    description: product.summary,
    openGraph: {
      images: [product.image],
    },
  }
}
```

## 5. Third Party Scripts

Script loading drastically affects TTFB and INP. Use `next/script`.

```javascript
import Script from 'next/script'

// For analytics (loads in the background after page is interactive)
<Script src="https://analytics.com/script.js" strategy="lazyOnload" />

// For critical scripts that must execute before the page is interactive
<Script src="https://api.stripe.com/v3" strategy="beforeInteractive" />
```
