# Server Actions

## Basics

Server Actions are async functions that run on the server, triggered from client or server code.

```tsx
// app/actions.ts — shared actions file
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  await db.posts.create({ data: { title } });
  revalidatePath('/posts');
}
```

### File Naming Convention

- `action.ts` — single action, colocated with route
- `actions.ts` — multiple related actions, shared across routes
- Match existing project patterns

## Form Patterns

### Basic Form (No Feedback)

```tsx
// page.tsx (Server Component)
import { createPost } from './actions';

export default function Page() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

**Rule**: `<form action={fn}>` expects the function to return `void`. No return statement.

### Form with Feedback (useActionState)

```tsx
// actions.ts
'use server';

type State = { error?: string; success?: boolean } | null;

export async function createPost(prevState: State, formData: FormData): Promise<State> {
  const title = formData.get('title') as string;
  if (!title || title.length < 3) return { error: 'Title must be at least 3 characters' };

  await db.posts.create({ data: { title } });
  revalidatePath('/posts');
  return { success: true };
}
```

```tsx
// CreatePostForm.tsx
'use client';
import { useActionState } from 'react';
import { createPost } from './actions';

export function CreatePostForm() {
  const [state, action, pending] = useActionState(createPost, null);

  return (
    <form action={action}>
      <input name="title" required />
      <button type="submit" disabled={pending}>
        {pending ? 'Creating...' : 'Create'}
      </button>
      {state?.error && <p className="text-red-500">{state.error}</p>}
      {state?.success && <p className="text-green-500">Created!</p>}
    </form>
  );
}
```

### Progressive Enhancement

Forms work without JavaScript when using `<form action={...}>`:

```tsx
// Works with JS disabled — form submits as standard POST
<form action={createPost}>
  <input name="title" />
  <button type="submit">Create</button>
</form>
```

## Security

Server Actions are **public HTTP endpoints**. Always validate and authorize:

```tsx
'use server';
import { cookies } from 'next/headers';
import { z } from 'zod';

const schema = z.object({
  title: z.string().min(3).max(100),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  // 1. Authenticate
  const session = await getSession(await cookies());
  if (!session) throw new Error('Unauthorized');

  // 2. Validate input
  const parsed = schema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });
  if (!parsed.success) throw new Error('Invalid input');

  // 3. Authorize
  if (!session.user.canCreatePosts) throw new Error('Forbidden');

  // 4. Mutate
  await db.posts.create({ data: { ...parsed.data, authorId: session.user.id } });
  revalidatePath('/posts');
}
```

## Revalidation After Mutations

```tsx
'use server';
import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';

export async function updatePost(id: string, formData: FormData) {
  await db.posts.update({ where: { id }, data: { title: formData.get('title') } });

  revalidateTag('posts');        // Invalidate tagged caches
  revalidatePath('/posts');      // Revalidate specific path
  revalidatePath('/posts/[slug]', 'page'); // Revalidate dynamic pages
  redirect('/posts');            // Redirect after mutation
}
```

## Non-Form Usage

Server Actions can be called directly from client code:

```tsx
'use client';
import { deletePost } from './actions';

export function DeleteButton({ id }: { id: string }) {
  return (
    <button onClick={() => deletePost(id)}>
      Delete
    </button>
  );
}
```

## Optimistic Updates

```tsx
'use client';
import { useOptimistic } from 'react';
import { addTodo } from './actions';

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: string) => [...state, { id: 'temp', title: newTodo }]
  );

  return (
    <form action={async (formData) => {
      const title = formData.get('title') as string;
      addOptimistic(title);
      await addTodo(formData);
    }}>
      <input name="title" />
      <button type="submit">Add</button>
      <ul>
        {optimisticTodos.map(t => <li key={t.id}>{t.title}</li>)}
      </ul>
    </form>
  );
}
```
