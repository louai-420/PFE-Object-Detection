# Parallelize Independent Async Operations (async-parallel)

Eliminate waterfalls by starting independent asynchronous operations in parallel using `Promise.all()`.

## Why it matters
Waterfalls happen when you `await` multiple independent operations sequentially. This means the second operation doesn't start until the first one finishes, doubling the total wait time for the user. Parallelizing them allows them to run concurrently, reducing the total duration to the time of the slowest operation.

## Incorrect Example
```tsx
// ❌ This creates a waterfall: fetchUserData must finish before fetchPosts starts
async function UserProfile({ id }) {
  const user = await fetchUserData(id); // 500ms
  const posts = await fetchPosts(id);   // 500ms
  // Total time: 1000ms
  return <Layout user={user} posts={posts} />;
}
```

## Correct Example
```tsx
// ✅ Independent operations start in parallel
async function UserProfile({ id }) {
  const [user, posts] = await Promise.all([
    fetchUserData(id),
    fetchPosts(id)
  ]);
  // Total time: 500ms
  return <Layout user={user} posts={posts} />;
}
```

## Additional Context
- Use `Promise.allSettled()` if you want to allow some operations to fail without rejecting the entire set.
- For Next.js Server Components, this pattern is critical for reducing Time to First Byte (TTFB) and improving streaming performance.
