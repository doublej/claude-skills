---
name: pixijs-dev
description: Build 2D graphics and games with PixiJS. Use when working with PixiJS applications, sprites, textures, animations, or the PixiJS API.
---

# PixiJS Development

Build 2D graphics, games, and interactive applications with PixiJS.

## When to Use

- Building PixiJS applications
- Working with sprites, textures, containers
- Implementing animations and interactions
- Debugging PixiJS rendering issues

## Example Patterns

```js
import { Assets } from 'pixi.js';
await Assets.init({ manifest });
```

```ts
import 'pixi.js/accessibility';
import { Container } from 'pixi.js';

const button = new Container();
button.accessible = true;
```

## Reference Files

See `references/` for comprehensive documentation.
