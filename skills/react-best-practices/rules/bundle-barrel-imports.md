# Direct Imports Over Barrel Files (bundle-barrel-imports)

Import components directly from their source files instead of through a single `index.js` barrel file.

## Why it matters
Barrel files (files that export everything from a directory) can prevent effective tree-shaking in many build systems. When you import a single component through a barrel file, the bundler may include *everything* exported by that file in the bundle, bloating the final output even if only one small component is used. Direct imports allow the bundler to only include what is actually needed.

## Incorrect Example
```tsx
// ❌ Barrel import - may include all UI components (Button, Input, Modal, etc.)
import { Button } from '@/components/ui';

export function LoginButton() {
  return <Button>Login</Button>;
}
```

## Correct Example
```tsx
// ✅ Direct import - only the Button component is bundled
import { Button } from '@/components/ui/button';

export function LoginButton() {
  return <Button>Login</Button>;
}
```

## Additional Context
- In Next.js, this is particularly important for reducing the first load JavaScript size.
- Tooling like `eslint-plugin-no-barrel-files` or Next.js `optimizePackageImports` can help automate this, but direct imports are the most reliable way to ensure minimal bundle sizes.
