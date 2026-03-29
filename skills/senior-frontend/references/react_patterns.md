# React Patterns & Best Practices (2025 Edition)

This guide covers modern React (v18/v19) patterns, focusing on the App Router ecosystem, Server Components, and functional design patterns.

## 1. Component Architecture

### React Server Components (RSC) vs Client Components
By default in modern React frameworks (like Next.js App Router), all components are **Server Components**.

**Server Components (Default):**
- Cannot use hooks (`useState`, `useEffect`, context).
- Cannot have interactivity (onClick, onChange).
- Can use `async/await` directly in the component body to fetch data.
- Do not add to the client-side JavaScript bundle.

**Client Components (`'use client'`):**
- Use only when interactivity or client state is required.
- Render on both the server (for initial HTML) and the client (for hydration).
- Push them as far down the tree as possible to minimize the client bundle size.

*Pattern: Pass Server Components as children to Client Components.*
```javascript
// ClientComponent.jsx
'use client';
import { useState } from 'react';

export default function ExpandableSection({ title, children }) {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>{title}</button>
      {isOpen && <div>{children}</div>}
    </div>
  );
}

// ServerComponent.jsx (Parent)
import ExpandableSection from './ClientComponent';
import HeavyServerModule from './HeavyServerModule'; // Stays on server!

export default function Page() {
  return (
    <ExpandableSection title="Show Details">
      <HeavyServerModule /> 
    </ExpandableSection>
  );
}
```

## 2. Forms and Mutations

### React 19 Actions
React 19 introduces native support for actions, replacing `useState` + `onSubmit` + `e.preventDefault()` boilerplate for forms.

```javascript
// Client Component utilizing useActionState
'use client';
import { useActionState } from 'react';
import { updateProfile } from './actions';

export default function ProfileForm() {
  const [state, formAction, isPending] = useActionState(updateProfile, null);

  return (
    <form action={formAction}>
      <input type="text" name="username" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Saving...' : 'Save'}
      </button>
      {state?.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

## 3. Performance & Memoization

### The React Compiler
With the release of the React Compiler (React 19), manual memoization (`useMemo`, `useCallback`, `React.memo`) is largely obsolete. The compiler automatically determines what needs to be cached.

*Rule: Stop writing `useMemo` and let the compiler handle it. Write simple, declarative code.*

### Optimistic UI
For immediate user feedback during slow mutations, use the `useOptimistic` hook.

```javascript
'use client';
import { useOptimistic } from 'react';
import { addMessage } from './actions';

export default function Chat({ messages }) {
  const [optimisticMessages, addOptimisticMessage] = useOptimistic(
    messages,
    (state, newMessage) => [...state, { text: newMessage, sending: true }]
  );

  async function handleSubmit(formData) {
    const text = formData.get('message');
    addOptimisticMessage(text); // Immediate UI update
    await addMessage(text);     // Background server request
  }

  return (
    <div>
      {optimisticMessages.map(m => (
        <div key={m.id} style={{ opacity: m.sending ? 0.5 : 1 }}>
          {m.text}
        </div>
      ))}
      <form action={handleSubmit}>
        <input name="message" />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## 4. State Management

- **Local State:** Use `useState` and `useReducer`.
- **URL State:** Prefer the URL (query parameters) for easily shareable, filterable state (e.g., search queries, pagination, active tabs). This keeps RSCs capable of reading the state without passing props down.
- **Global State:** Zustand is preferred over Redux for its simplicity and lack of boilerplate. React Context is fine for low-frequency updates, but avoids Context for rapidly changing data to prevent unnecessary re-renders.

## 5. Clean Code Practices in React

- **Return early:** Handle error/loading states at the top of the component.
- **Destructure props:** Destructure directly in the function signature `function User({ name, age })`.
- **Boolean props:** Pass `isTrue` instead of `isTrue={true}`.
- **Conditional Rendering:** Use `&&` cautiously. Avoid `items.length && <List />` (renders `0`). Use `items.length > 0 && <List />` or ternary `items.length ? <List /> : <Empty />`.
