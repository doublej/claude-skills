# Node/TypeScript Terminal UX

## Libraries

| Library | Use case | Install |
|---------|----------|---------|
| **ora** | Spinners (stderr-friendly) | `npm i ora` |
| **listr2** | Task list runner (multi-status) | `npm i listr2` |
| **Ink** | React-style full-screen TUI | `npm i ink react` |
| **chalk** | Colour/styling | `npm i chalk` |
| **@inquirer/prompts** | Interactive prompts | `npm i @inquirer/prompts` |

## ora: Spinners

```typescript
import ora from 'ora';

const spinner = ora({ text: 'Loading...', stream: process.stderr }).start();
// update
spinner.text = 'Still loading...';
// done
spinner.succeed('Loaded 42 items');
// or
spinner.fail('Connection refused');
```

### Concurrent spinners (use with caution)
```typescript
const s1 = ora({ text: 'Task A', prefixText: ' ', stream: process.stderr }).start();
const s2 = ora({ text: 'Task B', prefixText: ' ', stream: process.stderr }).start();
// Better: use listr2 for concurrent task display
```

## listr2: Task lists (best for multi-status CLI)

```typescript
import { Listr } from 'listr2';

const tasks = new Listr([
  {
    title: 'Install dependencies',
    task: async (ctx, task) => {
      task.output = 'Running npm install...';
      await exec('npm install');
    },
  },
  {
    title: 'Build project',
    task: async (ctx, task) => {
      // nested subtasks
      return task.newListr([
        { title: 'Compile TypeScript', task: () => exec('tsc') },
        { title: 'Bundle', task: () => exec('esbuild ...') },
      ], { concurrent: true });
    },
  },
  {
    title: 'Run tests',
    task: async (ctx, task) => {
      task.title = 'Running tests (42 suites)';
      await exec('vitest run');
    },
  },
], {
  rendererOptions: { collapseSubtasks: false },
  exitOnError: false,
});

await tasks.run();
```

### Conditional + skip
```typescript
{
  title: 'Deploy',
  enabled: (ctx) => ctx.deploy === true,
  skip: (ctx) => ctx.dryRun ? 'Dry run, skipping deploy' : false,
  task: async () => { /* ... */ },
}
```

### Non-TTY fallback
```typescript
new Listr(tasks, {
  renderer: process.stderr.isTTY ? 'default' : 'simple',
});
```

## Ink: React-style TUI

### Minimal app
```tsx
import React from 'react';
import { render, Text, Box } from 'ink';

function App() {
  return (
    <Box flexDirection="column" padding={1}>
      <Text bold>My TUI App</Text>
      <Text color="green">Ready</Text>
    </Box>
  );
}

render(<App />);
```

### Spinner component
```tsx
import React from 'react';
import { Text } from 'ink';
import Spinner from 'ink-spinner';

function LoadingStep({ label, done }: { label: string; done: boolean }) {
  return (
    <Text>
      {done ? <Text color="green">✓</Text> : <Spinner type="dots" />}
      {' '}{label}
    </Text>
  );
}
```

### useInput for keybindings
```tsx
import { useInput } from 'ink';

useInput((input, key) => {
  if (input === 'q') process.exit(0);
  if (key.upArrow) moveCursor(-1);
  if (key.downArrow) moveCursor(1);
});
```

### Key patterns
- Use `<Box>` for layout (flexbox model)
- Use `useApp().exit()` for clean shutdown
- Use `ink-text-input` for text fields, `ink-select-input` for lists
- String width: use `string-width` for correct emoji/CJK handling

## TTY-aware output module template
```typescript
import chalk from 'chalk';

const isTTY = process.stderr.isTTY ?? false;

export const log = {
  info: (msg: string) => process.stderr.write(`${msg}\n`),
  status: (msg: string) => isTTY && process.stderr.write(`${chalk.dim(msg)}\n`),
  error: (msg: string) => process.stderr.write(`${chalk.red('error:')} ${msg}\n`),
  data: (obj: unknown) => process.stdout.write(JSON.stringify(obj) + '\n'),
};
```
