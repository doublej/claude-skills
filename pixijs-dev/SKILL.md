---
name: pixijs-dev
description: Build 2D graphics and games with PixiJS. Use when working with PixiJS applications, sprites, textures, animations, or the PixiJS API.
---

# PixiJS Development

Build 2D graphics, games, and interactive applications with PixiJS.

<when_to_use>
- Building PixiJS applications
- Working with sprites, textures, containers
- Implementing animations and interactions
- Debugging PixiJS rendering issues
</when_to_use>

<examples>
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
</examples>

## Reference Files

See `references/` for comprehensive documentation.
