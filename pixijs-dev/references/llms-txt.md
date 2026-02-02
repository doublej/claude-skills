# Pixi - Llms-Txt

**Pages:** 53

---

## FAQ

**URL:** llms-txt#faq

**Contents:**
- What is PixiJS for?
- Is PixiJS free?
- Where do I get it?
- How do I get started?
- Why should I use PixiJS?
- Is PixiJS a game engine?
- Who makes PixiJS?
- I found a bug. What should I do?
- Culler Plugin

## What is PixiJS for?

Everything! Pixi.js is a rendering library that will allow you to create rich,
interactive graphic experiences, cross-platform applications, and games without
having to dive into the WebGL API or grapple with the intricacies of browser and
device compatibility. Killer performance with a clean API, means not only will
your content be better - but also faster to build!

PixiJS is and always will be free and Open Source. That said, financial contributions
are what make it possible to push PixiJS further, faster. Contributions allow us to
commission the PixiJS developer community to accelerate feature development and create
more in-depth documentation. Support Us by making a contribution via Open Collective. Go on! It will be a massive help AND make you feel good about yourself, win win ;)

## Where do I get it?

Visit our GitHub page to download the very latest version of PixiJS. This is the most up-to-date resource for PixiJS and should always be your first port of call to make sure you are using the latest version. Just click the 'Download' link in the navigation.

## How do I get started?

Right here! Take a look through the Resources section for a wealth of information including documentation, forums, tutorials and the Goodboy blog.

## Why should I use PixiJS?

Because you care about speed. PixiJS' #1 mantra has always been speed. We really do feel the need! We do everything we can to make PixiJS as streamlined, efficient and fast as possible, whilst balancing it with offering as many crucial and valuable features as we can.

## Is PixiJS a game engine?

No. PixiJS is what we've come to think of as a "creation engine". Whilst it is extremely good for making games, the core essence of PixiJS is simply moving things around on screens as quickly and efficiently as possible. It does of course happen that it is absolutely brilliant for making games though!

PixiJS is maintained by three core developers who work on the project part-time:

- Mat Groves ([@GoodBoyDigital](https://github.com/GoodBoyDigital))
- Sean Burns ([@Zyie](https://github.com/Zyie))
- Matt Karl ([@bigtimebuddy](https://github.com/bigtimebuddy))

The project thrives thanks to our highly active community of contributors and sponsors. As part-time maintainers, your sponsorship directly supports our ability to improve PixiJS, fix bugs, and create better documentation. Consider supporting our work through [GitHub Sponsors](https://github.com/sponsors/pixijs) or [Open Collective](https://opencollective.com/pixijs).

## I found a bug. What should I do?

Two things - lets us know via the PixiJS GitHub community and even better yet, if you know how, post a fix! Our Community is stronger in numbers so we're always keen to welcome new contributors into the team to help us shape what PixiJS becomes next.

---

## Manifests & Bundles

**URL:** llms-txt#manifests-&-bundles

**Contents:**
- What Is a Manifest?
  - Initializing With a Manifest
- What Is a Bundle?
  - Adding a Bundle Dynamically
- Recommended Tool: AssetPack
  - Key Benefits
- Resolver

PixiJS has a structured and scalable approach to asset management through **Manifests** and **Bundles**. This is the recommended way to manage assets in your PixiJS applications, especially for larger projects or those that require dynamic loading of assets based on context or user interaction. This guide explains what they are, how to use them, and how to generate them efficiently using [AssetPack](https://github.com/pixijs/AssetPack) — a tool designed to automate manifest and bundle creation.

## What Is a Manifest?

A **Manifest** is a descriptor object that defines your asset loading strategy. It lists all bundles, each of which contains grouped assets by name and alias. This structure allows for lazy-loading assets based on application context (e.g. load screen assets, level-specific content, etc.).

### Initializing With a Manifest

To initialize PixiJS asset handling with a manifest:

Once initialized, you can load bundles by name:

It should be noted that you can still load assets directly without loading an entire bundle via their alias:

A **Bundle** is a group of assets that are identified by a shared name. While bundles can be pre-defined in a manifest, they can also be dynamically registered at runtime.

### Adding a Bundle Dynamically

This approach is helpful for scenarios where you want to define bundles on the fly:

## Recommended Tool: AssetPack

Managing manifests and bundles manually can be error-prone. [**AssetPack**](https://pixijs.io/assetpack) is a CLI tool that scans your assets folder and generates optimized manifests and bundles automatically.

- Organizes assets by directory or pattern
- Supports output in PixiJS manifest format
- Reduces boilerplate and risk of manual mistakes

You can integrate AssetPack into your build pipeline to generate the manifest file and load it using `Assets.init({ manifest })`.

**Examples:**

Example 1 (js):
```js
const manifest = {
  bundles: [
    {
      name: 'load-screen',
      assets: [
        { alias: 'background', src: 'sunset.png' },
        { alias: 'bar', src: 'load-bar.{png,webp}' },
      ],
    },
    {
      name: 'game-screen',
      assets: [
        { alias: 'character', src: 'robot.png' },
        { alias: 'enemy', src: 'bad-guy.png' },
      ],
    },
  ],
};
```

Example 2 (js):
```js
import { Assets } from 'pixi.js';

await Assets.init({ manifest });
```

Example 3 (js):
```js
const loadScreenAssets = await Assets.loadBundle('load-screen');
const gameScreenAssets = await Assets.loadBundle('game-screen');
```

Example 4 (js):
```js
await Assets.init({ manifest });
const background = await Assets.load('background');
const bar = await Assets.load('bar');
```

---

## Accessibility

**URL:** llms-txt#accessibility

**Contents:**
- **How It Works**
- Enabling the System
- **Configuration Options**
- **Creating Accessible Objects**
  - **Properties for Accessible Containers**
- **API Reference**
- Color

PixiJS includes built-in accessibility support through a DOM-based overlay system that integrates with screen readers, keyboard navigation, and other assistive technologies. It uses `` overlays to describe visual elements to screen readers

:::info
Accessibility is opt-in to reduce bundle size and must be explicitly enabled.
:::

PixiJS places DOM `` elements over your canvas, aligned to the bounds of accessible objects. These elements:

- Can receive focus via keyboard (`tabIndex`)
- Announce `accessibleTitle` or `accessibleHint` to screen readers
- Dispatch `click`, `mouseover`, `mouseout` events as Pixi pointer events
- Use `aria-live` and `aria-label` where appropriate

## Enabling the System

To enable accessibility, you must import the module before creating your renderer:

PixiJS automatically installs the `AccessibilitySystem` onto your renderer. You can configure how and when it's activated.

## **Configuration Options**

You can customize when and how the accessibility system activates by passing options to the `Application` constructor:

Or programmatically enable/disable the system:

## **Creating Accessible Objects**

To mark a display object as accessible and add it to the accessibility system, set the `accessible` property to `true`. This will create a `` overlay that screen readers can interact with.

### **Properties for Accessible Containers**

There are several properties you can set on accessible containers to customize their behavior:

| Property                  | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| `accessible`              | Enables accessibility for the object                             |
| `accessibleTitle`         | Sets the `title` for screen readers                              |
| `accessibleHint`          | Sets the `aria-label`                                            |
| `accessibleText`          | Alternative inner text for the div                               |
| `accessibleType`          | Tag name used for the shadow element (`'button'`, `'div'`, etc.) |
| `accessiblePointerEvents` | CSS `pointer-events` value (`'auto'`, `'none'`, etc.)            |
| `tabIndex`                | Allows focus with keyboard navigation                            |
| `accessibleChildren`      | Whether children of this container are accessible                |

- [Overview](https://pixijs.download/release/docs/accessibility.html)
- [AccessibilitySystem](https://pixijs.download/release/docs/accessibility.AccessibilitySystem.html)
- [AccessibleOptions](https://pixijs.download/release/docs/accessibility.AccessibleOptions.html)

**Examples:**

Example 1 (ts):
```ts
import 'pixi.js/accessibility';
import { Container } from 'pixi.js';

const button = new Container();
button.accessible = true;
```

Example 2 (ts):
```ts
import 'pixi.js/accessibility';
```

Example 3 (ts):
```ts
const app = new Application({
  accessibilityOptions: {
    enabledByDefault: true, // Enable on startup
    activateOnTab: false, // Disable auto-activation via tab
    deactivateOnMouseMove: false, // Keep system active with mouse use
    debug: true, // Show div overlays for debugging
  },
});
```

Example 4 (ts):
```ts
app.renderer.accessibility.setAccessibilityEnabled(true);
```

---

## Using PixiJS in Different Environments

**URL:** llms-txt#using-pixijs-in-different-environments

**Contents:**
- Running PixiJS in the Browser
  - Example:
- Running PixiJS in Web Workers
  - Example:
- Custom Environments
  - Example Custom Adapter:
- Garbage Collection

PixiJS is a highly adaptable library that can run in a variety of environments, including browsers, Web Workers, and custom execution contexts like Node.js. This guide explains how PixiJS handles different environments and how you can configure it to suit your application's needs.

## Running PixiJS in the Browser

For browser environments, PixiJS uses the `BrowserAdapter` by default, you should not need to configure anything

## Running PixiJS in Web Workers

Web Workers provide a parallel execution environment, ideal for offloading rendering tasks. PixiJS supports Web Workers using the `WebWorkerAdapter`:

## Custom Environments

For non-standard environments, you can create a custom adapter by implementing the `Adapter` interface. This allows PixiJS to function in environments like Node.js or headless testing setups.

### Example Custom Adapter:

## Garbage Collection

**Examples:**

Example 1 (typescript):
```typescript
import { Application } from 'pixi.js';

const app = new Application();

await app.init({
  width: 800,
  height: 600,
});

document.body.appendChild(app.canvas);
```

Example 2 (typescript):
```typescript
import { DOMAdapter, WebWorkerAdapter } from 'pixi.js';

// Must be set before creating anything in PixiJS
DOMAdapter.set(WebWorkerAdapter);

const app = new Application();

await app.init({
  width: 800,
  height: 600,
});

app.canvas; // OffscreenCanvas
```

Example 3 (typescript):
```typescript
import { DOMAdapter } from 'pixi.js';

const CustomAdapter = {
  createCanvas: (width, height) => {
    /* custom implementation */
  },
  getCanvasRenderingContext2D: () => {
    /* custom implementation */
  },
  getWebGLRenderingContext: () => {
    /* custom implementation */
  },
  getNavigator: () => ({ userAgent: 'Custom', gpu: null }),
  getBaseUrl: () => 'custom://',
  fetch: async (url, options) => {
    /* custom fetch */
  },
  parseXML: (xml) => {
    /* custom XML parser */
  },
};

DOMAdapter.set(CustomAdapter);
```

---

## Documentation for LLMs

**URL:** llms-txt#documentation-for-llms

**Contents:**
- Available Files

PixiJS supports the [`llms.txt`](https://llmstxt.org/) convention for making documentation accessible to large language models (LLMs) and the applications that utilize them.

We provide several documentation files at different compression levels to accommodate various context window sizes:

- [`/llms.txt`](https://pixijs.com/llms.txt) - An index of available documentation files
- [`/llms-full.txt`](https://pixijs.com/llms-full.txt) - Complete PixiJS API documentation including all classes, methods, and examples
- [`/llms-medium.txt`](https://pixijs.com/llms-medium.txt) - Compressed documentation optimized for medium context windows

These files are automatically generated and updated daily from our TypeScript definition files and documentation sources.

---

## Performance Tips

**URL:** llms-txt#performance-tips

**Contents:**
  - General
  - Sprites
  - Graphics
  - Texture
  - Text
  - Masks
  - Filters
  - BlendModes
  - Events
- Render Groups

- Only optimize when you need to! PixiJS can handle a fair amount of content off the bat
- Be mindful of the complexity of your scene. The more objects you add the slower things will end up
- Order can help, for example sprite / graphic / sprite / graphic is slower than sprite / sprite / graphic / graphic
- Some older mobile devices run things a little slower. Passing in the option `useContextAlpha: false` and `antialias: false` to the Renderer or Application can help with performance
- Culling is disabled by default as it's often better to do this at an application level or set objects to be `cullable = true`. If you are GPU-bound it will improve performance; if you are CPU-bound it will degrade performance

- Use Spritesheets where possible to minimize total textures
- Sprites can be batched with up to 16 different textures (dependent on hardware)
- This is the fastest way to render content
- On older devices use smaller low resolution textures
- Add the extention `@0.5x.png` to the 50% scale-down spritesheet so PixiJS will visually-double them automatically
- Draw order can be important

- Graphics objects are fastest when they are not modified constantly (not including the transform, alpha or tint!)
- Graphics objects are batched when under a certain size (100 points or smaller)
- Small Graphics objects are as fast as Sprites (rectangles, triangles)
- Using 100s of graphics complex objects can be slow, in this instance use sprites (you can create a texture)

- Textures are automatically managed by a Texture Garbage Collector
- You can also manage them yourself by using `texture.destroy()`
- If you plan to destroy more than one at once add a random delay to their destruction to remove freezing
- Delay texture destroy if you plan to delete a lot of textures yourself

- Avoid changing it on every frame as this can be expensive (each time it draws to a canvas and then uploads to GPU)
- Bitmap Text gives much better performance for dynamically changing text
- Text resolution matches the renderer resolution, decrease resolution yourself by setting the `resolution` property, which can consume less memory

- Masks can be expensive if too many are used: e.g., 100s of masks will really slow things down
- Axis-aligned Rectangle masks are the fastest (as they use scissor rect)
- Graphics masks are second fastest (as they use the stencil buffer)
- Sprite masks are the third fastest (they use filters). They are really expensive. Do not use too many in your scene!

- Release memory: `container.filters = null`
- If you know the size of them: `container.filterArea = new Rectangle(x,y,w,h)`. This can speed things up as it means the object does not need to be measured
- Filters are expensive, using too many will start to slow things down!

- Different blend modes will cause batches to break (de-optimize)
- ScreenSprite / NormalSprite / ScreenSprite / NormalSprite would be 4 draw calls
- ScreenSprite / ScreenSprite / NormalSprite / NormalSprite would be 2 draw calls

- If an object has no interactive children use `interactiveChildren = false`. The event system will then be able to avoid crawling through the object
- Setting `hitArea = new Rectangle(x,y,w,h)` as above should stop the event system from crawling through the object

---

## Scene Objects

**URL:** llms-txt#scene-objects

**Contents:**
- Containers vs. Leaf Nodes
  - Containers
  - Leaf Nodes
- Transforms
  - **Anchor vs Pivot**
- Measuring Bounds
  - Changing size
- Masking Scene Objects
  - Types of Masks
  - Inverse Masks

In PixiJS, scene objects are the building blocks of your application’s display hierarchy. They include **containers**, **sprites**, **text**, **graphics**, and other drawable entities that make up the **scene graph**—the tree-like structure that determines what gets rendered, how, and in what order.

## Containers vs. Leaf Nodes

Scene objects in PixiJS can be divided into **containers** and **leaf nodes**:

`Container` is the **base class** for all scene objects in v8 (replacing the old `DisplayObject`).

- Can have children.
- Commonly used to group objects and apply transformations (position, scale, rotation) to the group.
- Examples: `Application.stage`, user-defined groups.

Leaf nodes are renderable objects that should not have children. In v8, **only containers should have children**.

Examples of leaf nodes include:

- `Sprite`
- `Text`
- `Graphics`
- `Mesh`
- `TilingSprite`
- `HTMLText`

Attempting to add children to a leaf node will not result in a runtime error, however, you may run into unexpected rendering behavior. Therefore, If nesting is required, wrap leaf nodes in a `Container`.

**Before v8 (invalid in v8):**

All scene objects in PixiJS have several properties that control their position, rotation, scale, and alpha. These properties are inherited by child objects, allowing you to apply transformations to groups of objects easily.

You will often use these properties to position and animate objects in your scene.

| Property     | Description                                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **position** | X- and Y-position are given in pixels and change the position of the object relative to its parent, also available directly as `object.x` / `object.y`  |
| **rotation** | Rotation is specified in radians, and turns an object clockwise (0.0 - 2 \* Math.PI)                                                                    |
| **angle**    | Angle is an alias for rotation that is specified in degrees instead of radians (0.0 - 360.0)                                                            |
| **pivot**    | Point the object rotates around, in pixels - also sets origin for child objects                                                                         |
| **alpha**    | Opacity from 0.0 (fully transparent) to 1.0 (fully opaque), inherited by children                                                                       |
| **scale**    | Scale is specified as a percent with 1.0 being 100% or actual-size, and can be set independently for the x and y axis                                   |
| **skew**     | Skew transforms the object in x and y similar to the CSS skew() function, and is specified in radians                                                   |
| **anchor?**  | Anchor is a percentage-based offset for the sprite's position and rotation. This is different from the `pivot` property, which is a pixel-based offset. |

### **Anchor vs Pivot**

Some leaf nodes have an additional property called `anchor`, which is a percentage-based offset for the nodes position and rotation. This is different from the `pivot` property, which is a pixel-based offset. Understanding the difference between anchor and pivot is critical when positioning or rotating a node.

:::info
Setting either pivot or anchor visually moves the node. This differs from CSS where changing `transform-origin` does not affect the element's position.
:::

- Available only on `Sprite`
- Defined in normalized values `(0.0 to 1.0)`
- `(0, 0)` is the top-left, `(0.5, 0.5)` is the center
- Changes both position and rotation origin

- Available on all `Container`s
- Defined in **pixels**, not normalized

There are two types of bounds in PixiJS:

- **Local bounds** represent the object’s dimensions in its own coordinate space. Use `getLocalBounds()`.
- **Global bounds** represent the object's bounding box in world coordinates. Use `getBounds()`.

If performance is critical you can also provide a custom `boundsArea` to avoid per-child measurement entirely.

To change the size of a container, you can use the `width` and `height` properties. This will scale the container to fit the specified dimensions:

Setting the `width` and `height` individually can be an expensive operation, as it requires recalculating the bounds of the container and its children. To avoid this, you can use `setSize()` to set both properties at once:

This method is more efficient than setting `width` and `height` separately, as it only requires one bounds calculation.

## Masking Scene Objects

PixiJS supports **masking**, allowing you to restrict the visible area of a scene object based on another object's shape.
This is useful for creating effects like cropping, revealing, or hiding parts of your scene.

- **Graphics-based masks**: Use a `Graphics` object to define the shape.
- **Sprite-based masks**: Use a `Sprite` or other renderable object.

To create an inverse mask, you can use the `setMask` property and set its `inverse` option to `true`. This will render everything outside the mask.

- The mask is **not rendered**; it's used only to define the visible area. However, it must be added to the display list.
- Only one mask can be assigned per object.
- For advanced blending, use **alpha masks** or **filters** (covered in later guides).

Another common use for Container objects is as hosts for filtered content. Filters are an advanced, WebGL/WebGPU-only feature that allows PixiJS to perform per-pixel effects like blurring and displacements. By setting a filter on a Container, the area of the screen the Container encompasses will be processed by the filter after the Container's contents have been rendered.

:::info
Filters should be used somewhat sparingly. They can slow performance and increase memory usage if used too often in a scene.
:::

Below are list of filters available by default in PixiJS. There is, however, a community repository with [many more filters](https://github.com/pixijs/filters).

| Filter             | Description                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------- |
| AlphaFilter        | Similar to setting `alpha` property, but flattens the Container instead of applying to children individually. |
| BlurFilter         | Apply a blur effect                                                                                           |
| ColorMatrixFilter  | A color matrix is a flexible way to apply more complex tints or color transforms (e.g., sepia tone).          |
| DisplacementFilter | Displacement maps create visual offset pixels, for instance creating a wavy water effect.                     |
| NoiseFilter        | Create random noise (e.g., grain effect).                                                                     |

Under the hood, each Filter we offer out of the box is written in both glsl (for WebGL) and wgsl (for WebGPU). This means all filters should work on both renderers.

You can tint any scene object by setting the `tint` property. It modifies the color of the rendered pixels, similar to multiplying a tint color over the object.

The `tint` is inherited by child objects unless they specify their own. If only part of your scene should be tinted, place it in a separate container.

A value of `0xFFFFFF` disables tinting.

PixiJS supports a variety of color formats and you can find more information from the [Color documentation](../color.md).

Blend modes determine how colors of overlapping objects are combined. PixiJS supports a variety of blend modes, including:

- `normal`: Default blend mode.
- `add`: Adds the colors of the source and destination pixels.
- `multiply`: Multiplies the colors of the source and destination pixels.
- `screen`: Inverts the colors, multiplies them, and inverts again.

We also support may more advanced blend modes, such as `subtract`, `difference`, and `overlay`. You can find the full list of blend modes in the [Blend Modes documentation](../filters.md#advanced-blend-modes).

PixiJS provides a powerful interaction system that allows you to handle user input events like clicks/hovers. To enable interaction on a scene object, can be as simple as setting its `interactive` property to `true`.

We have a detailed guide on [Interaction](../events.md) that covers how to set up and manage interactions, including hit testing, pointer events, and more. We highly recommend checking it out.

The `onRender` callback allows you to run logic every frame when a scene object is rendered. This is useful for lightweight animation and update logic:

Note: In PixiJS v8, this replaces the common v7 pattern of overriding `updateTransform`, which no longer runs every frame. The `onRender` function is registered with the render group the container belongs to.

To remove the callback:

- [Overview](https://pixijs.download/release/docs/scene.html)
- [Container](https://pixijs.download/release/docs/scene.Container.html)
- [ParticleContainer](https://pixijs.download/release/docs/scene.ParticleContainer.html)
- [Sprite](https://pixijs.download/release/docs/scene.Sprite.html)
- [TilingSprite](https://pixijs.download/release/docs/scene.TilingSprite.html)
- [NineSliceSprite](https://pixijs.download/release/docs/scene.NineSliceSprite.html)
- [Graphics](https://pixijs.download/release/docs/scene.Graphics.html)
- [Mesh](https://pixijs.download/release/docs/scene.Mesh.html)
- [Text](https://pixijs.download/release/docs/scene.Text.html)
- [Bitmap Text](https://pixijs.download/release/docs/scene.BitmapText.html)
- [HTMLText](https://pixijs.download/release/docs/scene.HTMLText.html)

**Examples:**

Example 1 (ts):
```ts
const group = new Container();
group.addChild(spriteA);
group.addChild(spriteB);
```

Example 2 (ts):
```ts
const sprite = new Sprite();
sprite.addChild(anotherSprite); // ❌ Invalid in v8
```

Example 3 (ts):
```ts
const group = new Container();
group.addChild(sprite);
group.addChild(anotherSprite); // ✅ Valid
```

Example 4 (ts):
```ts
sprite.anchor.set(0.5); // center
sprite.rotation = Math.PI / 4; // Rotate 45 degrees around the center
```

---

## Render Layers

**URL:** llms-txt#render-layers

**Contents:**
  - **Key Concepts**
  - **Basic API Usage**
- ![alt text](render-layers/image-1.png)
  - **Complete Example**
  - **Gotchas and Things to Watch Out For**
  - **Best Practices**
- Render Loop

The PixiJS Layer API provides a powerful way to control the **rendering order** of objects independently of their **logical parent-child relationships** in the scene graph. With RenderLayers, you can decouple how objects are transformed (via their logical parent) from how they are visually drawn on the screen.

Using RenderLayers ensures these elements are visually prioritized while maintaining logical parent-child relationships. Examples include:

- A character with a health bar: Ensure the health bar always appears on top of the world, even if the character moves behind an object.

- UI elements like score counters or notifications: Keep them visible regardless of the game world’s complexity.

- Highlighting Elements in Tutorials: Imagine a tutorial where you need to push back most game elements while highlighting a specific object. RenderLayers can split these visually. The highlighted object can be placed in a foreground layer to be rendered above a push back layer.

This guide explains the key concepts, provides practical examples, and highlights common gotchas to help you use the Layer API effectively.

1. **Independent Rendering Order**:

- RenderLayers allow control of the draw order independently of the logical hierarchy, ensuring objects are rendered in the desired order.

2. **Logical Parenting Stays Intact**:

- Objects maintain transformations (e.g., position, scale, rotation) from their logical parent, even when attached to RenderLayers.

3. **Explicit Object Management**:

- Objects must be manually reassigned to a layer after being removed from the scene graph or layer, ensuring deliberate control over rendering.

4. **Dynamic Sorting**:

- Within layers, objects can be dynamically reordered using `zIndex` and `sortChildren` for fine-grained control of rendering order.

### **Basic API Usage**

First lets create two items that we want to render, red guy and blue guy.

![alt text](render-layers/image-1.png)

Now we know that red guy will be rendered first, then blue guy. Now in this simple example you could get away with just sorting the `zIndex` of the red guy and blue guy to help reorder.

But this is a guide about render layers, so lets create one of those.

Use `renderLayer.attach` to assign an object to a layer. This overrides the object’s default render order defined by its logical parent.

![alt text](render-layers/image-2.png)

So now our scene graph order is:

And our render order is:

This happens because the layer is now the last child in the stage. Since the red guy is attached to the layer, it will be rendered at the layer's position in the scene graph. However, it still logically remains in the same place in the scene hierarchy.

#### **3. Removing Objects from a Layer**

Now let's remove the red guy from the layer. To stop an object from being rendered in a layer, use `removeFromLayer`. Once removed from the layer, its still going to be in the scene graph, and will be rendered in its scene graph order.

![alt text](render-layers/image-1.png)

Removing an object from its logical parent (`removeChild`) automatically removes it from the layer.

![alt text](render-layers/image-3.png)

However, if you remove the red guy from the stage and then add it back to the stage, it will not be added to the layer again.

![alt text](render-layers/image-1.png)

You will need to reattach it to the layer yourself.

![alt text](render-layers/image-2.png)

This may seem like a pain, but it's actually a good thing. It means that you have full control over the render order of the object, and you can change it at any time. It also means you can't accidentally add an object to a container and have it automatically re-attach to a layer that may or may not still be around - it would be quite confusing and lead to some very hard to debug bugs!

#### **5. Layer Position in Scene Graph**

The layer’s position in the scene graph determines its render priority relative to other layers and objects.

## ![alt text](render-layers/image-1.png)

### **Complete Example**

Here’s a real-world example that shows how to use RenderLayers to set ap player ui on top of the world.

### **Gotchas and Things to Watch Out For**

1. **Manual Reassignment**:

- When an object is re-added to a logical parent, it does not automatically reassociate with its previous layer. Always reassign the object to the layer explicitly.

2. **Nested Children**:

- If you remove a parent container, all its children are automatically removed from layers. Be cautious with complex hierarchies.

3. **Sorting Within Layers**:

- Objects in a layer can be sorted dynamically using their `zIndex` property. This is useful for fine-grained control of render order.

4. **Layer Overlap**:
   - If multiple layers overlap, their order in the scene graph determines the render priority. Ensure the layering logic aligns with your desired visual output.

### **Best Practices**

1. **Group Strategically**: Minimize the number of layers to optimize performance.
2. **Use for Visual Clarity**: Reserve layers for objects that need explicit control over render order.
3. **Test Dynamic Changes**: Verify that adding, removing, or reassigning objects to layers behaves as expected in your specific scene setup.

By understanding and leveraging RenderLayers effectively, you can achieve precise control over your scene's visual presentation while maintaining a clean and logical hierarchy.

**Examples:**

Example 1 (typescript):
```typescript
const redGuy = new PIXI.Sprite('red guy');
redGuy.tint = 0xff0000;

const blueGuy = new PIXI.Sprite('blue guy');
blueGuy.tint = 0x0000ff;

stage.addChild(redGuy, blueGuy);
```

Example 2 (typescript):
```typescript
// a layer..
const layer = new RenderLayer();
stage.addChild(layer);
layer.attach(redGuy);
```

Example 3 (unknown):
```unknown
|- stage
    |-- redGuy
    |-- blueGuy
    |-- layer
```

Example 4 (unknown):
```unknown
|- stage
    |-- blueGuy
    |-- layer
        |-- redGuy
```

---

## Assets

**URL:** llms-txt#assets

**Contents:**
- Key Capabilities
- Supported File Types
- Getting started
  - Loading Assets
  - Repeated Loads Are Safe
  - Asset Aliases
  - Retrieving Loaded Assets
  - Unloading Assets
  - Customizing Asset Loading
- Advanced Usage

PixiJS has the `Assets` singleton which is used to streamline resource loading. It’s modern, Promise-based, cache-aware, and highly extensible—making it the one stop shop for all PixiJS resource management!

- **Asynchronous loading** of assets via Promises or async/await.
- **Caching** prevents redundant network requests.
- **Built-in support** for common media formats (images, video, fonts).
- **Custom parsers** and **resolvers** for flexibility.
- **Background loading, manifest-based bundles,** and **smart fallbacks**.

## Supported File Types

| Type                | Extensions                                                       | Loaders                           |
| ------------------- | ---------------------------------------------------------------- | --------------------------------- |
| Textures            | `.png`, `.jpg`, `.gif`, `.webp`, `.avif`, `.svg`                 | `loadTextures`, `loadSvg`         |
| Video Textures      | `.mp4`, `.m4v`, `.webm`, `.ogg`, `.ogv`, `.h264`, `.avi`, `.mov` | `loadVideoTextures`               |
| Sprite Sheets       | `.json`                                                          | `spritesheetAsset`                |
| Bitmap Fonts        | `.fnt`, `.xml`, `.txt`                                           | `loadBitmapFont`                  |
| Web Fonts           | `.ttf`, `.otf`, `.woff`, `.woff2`                                | `loadWebFont`                     |
| JSON                | `.json`                                                          | `loadJson`                        |
| Text                | `.txt`                                                           | `loadTxt`                         |
| Compressed Textures | `.basis`, `.dds`, `.ktx`, `.ktx2`                                | `loadBasis`, `loadDDS`, `loadKTX` |

> Need more? Add custom parsers!

Loading an asset with PixiJS is as simple as calling `Assets.load()` and passing in the asset’s URL. This function returns a `Promise` that resolves to the loaded resource—whether that’s a texture, font, JSON, or another supported format.

You can provide either an **absolute URL** (e.g. from a CDN):

Or a **relative path** within your project:

PixiJS will **_typically_** automatically determine how to load the asset based on its **file extension** and will cache the result to avoid redundant downloads.

### Repeated Loads Are Safe

`Assets` caches by URL or alias. Requests for the same resource return the **same texture**.

You can also use aliases to refer to assets instead of their full URLs. This provides a more convenient way to manage assets, especially when you have long or complex URLs.

All Asset APIs support aliases, including `Assets.load()`, `Assets.get()`, and `Assets.unload()`.

There is more complex ways of defining assets and you can read about them in the [Resolver](./resolver.md) section.

### Retrieving Loaded Assets

You can also retrieve assets that have already been loaded using `Assets.get()`:

This is useful for when you have preloaded your assets elsewhere in your code and want to access them later without having to pass round references from the initial load.

To unload an asset, you can use `Assets.unload()`. This will remove the asset from the cache and free up memory. Note that if you try to access the asset after unloading it, you will need to load it again.

### Customizing Asset Loading

You can customize the asset loading process by providing options to the `Assets.init()` method. This allows you to set preferences for how assets are loaded, specify a base path for assets, and more.

| Option                | Type                      | Description                                                   |
| --------------------- | ------------------------- | ------------------------------------------------------------- |
| `basePath`            | `string`                  | Prefix applied to all relative asset paths (e.g. for CDNs).   |
| `defaultSearchParams` | `string`                  | A default URL parameter string to append to all assets loaded |
| `skipDetections`      | `boolean`                 | Skip environment detection parsers for assets.                |
| `manifest`            | `Manifest`                | A descriptor of named asset bundles and their contents.       |
| `preferences`         | `AssetPreferences`        | Specifies preferences for each loader                         |
| `bundleIdentifier`    | `BundleIdentifierOptions` | **Advanced** - Override how bundlesIds are generated.         |

There are several advanced features available in the `Assets` API that can help you manage your assets more effectively.
You can read more about these features in the rest of the documentation:

- [Resolving Assets](./resolver.md)
- [Manifests & Bundles (Recommended)](./manifest.md)
- [Background Loading](./background-loader.md)
- [Compressed Textures](./compressed-textures.md)

- [Overview](https://pixijs.download/release/docs/assets.html)
- [Assets](https://pixijs.download/release/docs/assets.Assets.html)

## Manifests & Bundles

**Examples:**

Example 1 (ts):
```ts
import { Assets } from 'pixi.js';

await Assets.init({ ... });

const texture = await Assets.load('path/to/hero.png');
```

Example 2 (ts):
```ts
const texture = await Assets.load('https://example.com/assets/hero.png');
```

Example 3 (ts):
```ts
const texture = await Assets.load('assets/hero.png');
```

Example 4 (typescript):
```typescript
import { Application, Assets, Texture } from 'pixi.js';

const app = new Application();
// Application must be initialized before loading assets
await app.init({ backgroundColor: 0x1099bb });

// Load a single asset
const bunnyTexture = await Assets.load('path/to/bunny.png');
const sprite = new Sprite(bunnyTexture);

// Load multiple assets at once
const textures = await Assets.load(['path/to/bunny.png', 'path/to/cat.png']);
const bunnySprite = new Sprite(textures['path/to/bunny.png']);
const catSprite = new Sprite(textures['path/to/cat.png']);
```

---

## Quick Start

**URL:** llms-txt#quick-start

**Contents:**
- Try PixiJS Online
- Creating a New Project
- Usage
- Architecture

- To quickly get a taste of PixiJS, you can try it directly in our [PixiJS Playground](/8.x/playground).

## Creating a New Project

:::info[Prerequisites]

- Familiarity with the command line and a basic understanding of JavaScript.
- Install [Node.js](https://nodejs.org/en/) v20.0 or higher.
  :::

In this section, we will introduce how to scaffold a PixiJS application on your local machine. The created project will use a pre-configured build setup, allowing you to quickly get started with PixiJS development.

Make sure your current working directory is where you want to create your project. Run the following command in your terminal:

This command will install and execute the [PixiJS Create](https://pixijs.io/create-pixi/) CLI and begin scaffolding your project. You will be prompted to configure your project by selecting various options, including selecting a template type for setting up your project. There are two main types of templates to choose from:

#### Creation Templates (Recommended)

Creation templates are tailored for specific platforms and include additional configurations and dependencies to streamline development for a particular use case. These templates are more opinionated and are perfect for beginners or those looking for a ready-to-go setup.

#### Bundler Templates

Bundler templates are general templates designed to scaffold a PixiJS project with a specific bundler. They include the necessary configurations and dependencies but leave the project structure flexible, making them ideal for experienced developers who prefer more control.

We recommended using the Vite + PixiJS template for most projects when using bundler templates, as it provides a modern and fast setup for PixiJS applications with minimal configuration.

After selecting your desired template, the scaffolding tool will create a new project directory with the chosen configuration. Navigate to the project directory and install the dependencies:

You can also add PixiJS to an existing project:

Once you've set up your project, here's a simple example to get started with PixiJS:

:::warning
If using Vite you still need to wrap your code in an async function. There is an issue when using top level await with PixiJS when building for production.

This issue is known to affect Vite \<=6.0.6. Future versions of Vite may resolve this issue.
:::

**Examples:**

Example 1 (sh):
```sh
npm create pixi.js@latest
```

Example 2 (bash):
```bash
cd
npm install
npm run dev
```

Example 3 (bash):
```bash
npm install pixi.js
```

Example 4 (ts):
```ts
// description: This example demonstrates how to use a Container to group and manipulate multiple sprites
import { Application, Assets, Container, Sprite } from 'pixi.js';

(async () => {
  // Create a new application
  const app = new Application();

  // Initialize the application
  await app.init({ background: '#1099bb', resizeTo: window });

  // Append the application canvas to the document body
  document.body.appendChild(app.canvas);

  // Create and add a container to the stage
  const container = new Container();

  app.stage.addChild(container);

  // Load the bunny texture
  const texture = await Assets.load('https://pixijs.com/assets/bunny.png');

  // Create a 5x5 grid of bunnies in the container
  for (let i = 0; i < 25; i++) {
    const bunny = new Sprite(texture);

    bunny.x = (i % 5) * 40;
    bunny.y = Math.floor(i / 5) * 40;
    container.addChild(bunny);
  }

  // Move the container to the center
  container.x = app.screen.width / 2;
  container.y = app.screen.height / 2;

  // Center the bunny sprites in local container coordinates
  container.pivot.x = container.width / 2;
  container.pivot.y = container.height / 2;

  // Listen for animate update
  app.ticker.add((time) => {
    // Continuously rotate the container!
    // * use delta to create frame-independent transform *
    container.rotation -= 0.01 * time.deltaTime;
  });
})();
```

---

## Math

**URL:** llms-txt#math

**Contents:**
- Matrix
- Point and ObservablePoint
  - `Point`
  - `ObservablePoint`
- Shapes
  - `Rectangle`
  - `Circle`
  - `Ellipse`
  - `Polygon`
  - `RoundedRectangle`

PixiJS includes a several math utilities for 2D transformations, geometry, and shape manipulation. This guide introduces the most important classes and their use cases, including optional advanced methods enabled via `math-extras`.

The `Matrix` class represents a 2D affine transformation matrix. It is used extensively for transformations such as scaling, translation, and rotation.

## Point and ObservablePoint

The Point object represents a location in a two-dimensional coordinate system, where `x` represents the position on the horizontal axis and `y` represents the position on the vertical axis. Many Pixi functions accept the `PointData` type as an alternative to `Point`, which only requires `x` and `y` properties.

### `ObservablePoint`

Extends `Point` and triggers a callback when its values change. Used internally for reactive systems like position and scale updates.

PixiJS includes several 2D shapes, used for hit testing, rendering, and geometry computations.

Axis-aligned rectangle defined by `x`, `y`, `width`, and `height`.

Defined by `x`, `y` (center) and `radius`.

Similar to `Circle`, but supports different width and height (radii).

Defined by a list of points. Used for complex shapes and hit testing.

### `RoundedRectangle`

Rectangle with rounded corners, defined by a radius.

A convenience wrapper for defining triangles with three points.

## Optional: `math-extras`

Importing `pixi.js/math-extras` extends `Point` and `Rectangle` with additional vector and geometry utilities.

### Enhanced `Point` Methods

| Method                          | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| `add(other[, out])`             | Adds another point to this one.                              |
| `subtract(other[, out])`        | Subtracts another point from this one.                       |
| `multiply(other[, out])`        | Multiplies this point with another point component-wise.     |
| `multiplyScalar(scalar[, out])` | Multiplies the point by a scalar.                            |
| `dot(other)`                    | Computes the dot product of two vectors.                     |
| `cross(other)`                  | Computes the scalar z-component of the 3D cross product.     |
| `normalize([out])`              | Returns a normalized (unit-length) vector.                   |
| `magnitude()`                   | Returns the Euclidean length.                                |
| `magnitudeSquared()`            | Returns the squared length (more efficient for comparisons). |
| `project(onto[, out])`          | Projects this point onto another vector.                     |
| `reflect(normal[, out])`        | Reflects the point across a given normal.                    |

### Enhanced `Rectangle` Methods

| Method                       | Description                                           |
| ---------------------------- | ----------------------------------------------------- |
| `containsRect(other)`        | Returns true if this rectangle contains the other.    |
| `equals(other)`              | Checks if all properties are equal.                   |
| `intersection(other[, out])` | Returns a new rectangle representing the overlap.     |
| `union(other[, out])`        | Returns a rectangle that encompasses both rectangles. |

- [Overview](https://pixijs.download/release/docs/maths.html)
- [Matrix](https://pixijs.download/release/docs/maths.Matrix.html)
- [Point](https://pixijs.download/release/docs/maths.Point.html)
- [ObservablePoint](https://pixijs.download/release/docs/maths.ObservablePoint.html)
- [Rectangle](https://pixijs.download/release/docs/maths.Rectangle.html)
- [Circle](https://pixijs.download/release/docs/maths.Circle.html)
- [Ellipse](https://pixijs.download/release/docs/maths.Ellipse.html)
- [Polygon](https://pixijs.download/release/docs/maths.Polygon.html)
- [RoundedRectangle](https://pixijs.download/release/docs/maths.RoundedRectangle.html)
- [Triangle](https://pixijs.download/release/docs/maths.Triangle.html)

**Examples:**

Example 1 (ts):
```ts
import { Matrix, Point } from 'pixi.js';

const matrix = new Matrix();
matrix.translate(10, 20).scale(2, 2);

const point = new Point(5, 5);
const result = matrix.apply(point); // result is (20, 30)
```

Example 2 (ts):
```ts
import { Point } from 'pixi.js';
const point = new Point(5, 10);

point.set(20, 30); // set x and y
```

Example 3 (ts):
```ts
import { Point, ObservablePoint } from 'pixi.js';

const observer = {
  _onUpdate: (point) => {
    console.log(`Point updated to: (${point.x}, ${point.y})`);
  },
};
const reactive = new ObservablePoint(observer, 1, 2);
reactive.set(3, 4); // triggers call to _onUpdate
```

Example 4 (ts):
```ts
import { Rectangle } from 'pixi.js';

const rect = new Rectangle(10, 10, 100, 50);
rect.contains(20, 20); // true
```

---

## Resolver

**URL:** llms-txt#resolver

**Contents:**
- Resolver Lifecycle
- Using Unresolved Assets
- Examples
  - Loading a Single Asset
  - Loading with Explicit Parser and Loader Options
  - Using Wildcards for Responsive and Format-Aware Loading
- Related Tools and Features
- SVG's

In PixiJS, asset management centers around the concept of `UnresolvedAsset` and `ResolvedAsset`. This system is designed to support multi-format assets, conditional loading, and runtime optimization based on platform capabilities (e.g., WebP support, device resolution, or performance constraints).

Rather than specifying a fixed URL, developers describe what assets _could_ be loaded — and PixiJS selects the best option dynamically.

## Resolver Lifecycle

The resolution process involves four key steps:

1. **UnresolvedAsset Creation**
   Assets defined using a string or object are internally normalized into `UnresolvedAsset` instances. These include metadata such as aliases, wildcard paths, parser hints, and custom data.

2. **Source Expansion**
   The `src` field of an `UnresolvedAsset` can be a string or array of strings. PixiJS expands any wildcard patterns (e.g. `myAsset@{1,2}x.{png,webp}`) into a list of concrete candidate URLs.

3. **Best-Match Selection**
   PixiJS evaluates all candidate URLs and uses platform-aware heuristics to pick the most suitable source. Factors include supported formats (e.g. WebP vs PNG), device pixel ratio, and custom configuration such as preferred formats.

4. **ResolvedAsset Output**
   The result is a `ResolvedAsset` containing a specific URL and all required metadata, ready to be passed to the relevant parser and loaded into memory.

## Using Unresolved Assets

An `UnresolvedAsset` is the primary structure used to define assets in PixiJS. It allows you to specify the source URL(s), alias(es), and any additional data needed for loading. They are more complex, but are also more powerful.

| Field              | Type                 | Description                                                                  |
| ------------------ | -------------------- | ---------------------------------------------------------------------------- |
| `alias`            | `string \| string[]` | One or more aliases used to reference this asset later.                      |
| `src`              | `string \| string[]` | Path or paths to one or more asset candidates. Supports wildcards.           |
| `loadParser` (opt) | `string`             | A specific parser to handle the asset (e.g. `'loadTextures'`, `'loadJson'`). |
| `data` (opt)       | `any`                | Extra data to pass into the loader. This varies by parser type.              |

### Loading a Single Asset

### Loading with Explicit Parser and Loader Options

### Using Wildcards for Responsive and Format-Aware Loading

This pattern expands internally to:

PixiJS will select the best match depending on runtime capabilities (e.g. chooses WebP if supported, 2x if on a high-res display).

## Related Tools and Features

- **AssetPack**: If you're managing large asset sets, [AssetPack](https://pixijs.io/assetpack) can generate optimized manifests using glob patterns and output `UnresolvedAsset` structures automatically.
- **Asset Manifests & Bundles**: Use [manifests and bundles](./manifest.md) to predefine groups of unresolved assets and load them via `Assets.loadBundle`.

**Examples:**

Example 1 (ts):
```ts
import { Assets } from 'pixi.js';

await Assets.load({
  alias: 'bunny',
  src: 'images/bunny.png',
});
```

Example 2 (ts):
```ts
await Assets.load({
  alias: 'bunny',
  src: 'images/bunny.png',
  loadParser: 'loadTextures',
  data: {
    alphaMode: 'no-premultiply-alpha',
  },
});
```

Example 3 (ts):
```ts
await Assets.load({
  alias: 'bunny',
  src: 'images/bunny@{0.5,1,2}x.{png,webp}',
});
```

Example 4 (ts):
```ts
[
  'images/bunny@0.5x.png',
  'images/bunny@0.5x.webp',
  'images/bunny@1x.png',
  'images/bunny@1x.webp',
  'images/bunny@2x.png',
  'images/bunny@2x.webp',
];
```

---

## Graphics Fill

**URL:** llms-txt#graphics-fill

**Contents:**
- Basic Color Fills
  - Examples:
- Fill with a Style Object
- Fill with Textures
  - Local vs. Global Texture Space
  - Using Matrices with Textures
  - Texture Gotcha's
- Fill with Gradients
  - Linear Gradients
  - Radial Gradients

If you are new to graphics, please check out the [graphics guide](../graphics) here. This guide dives a bit deeper into a specific aspect of graphics: how to fill them! The `fill()` method in PixiJS is particularly powerful, enabling you to fill shapes with colors, textures, or gradients. Whether you're designing games, UI components, or creative tools, mastering the `fill()` method is essential for creating visually appealing and dynamic graphics. This guide explores the different ways to use the `fill()` method to achieve stunning visual effects.

:::info Note
The `fillStyles` discussed here can also be applied to Text objects!
:::

When creating a `Graphics` object, you can easily fill it with a color using the `fill()` method. Here's a simple example:

![alt text](/assets/guides/components/image.png)

This creates a red rectangle. PixiJS supports multiple color formats for the `fill()` method. Developers can choose a format based on their needs. For example, CSS color strings are user-friendly and readable, hexadecimal strings are compact and widely used in design tools, and numbers are efficient for programmatic use. Arrays and Color objects offer precise control, making them ideal for advanced graphics.

- CSS color strings (e.g., 'red', 'blue')
- Hexadecimal strings (e.g., '#ff0000')
- Numbers (e.g., `0xff0000`)
- Arrays (e.g., `[255, 0, 0]`)
- Color objects for precise color control

## Fill with a Style Object

For more advanced fills, you can use a `FillStyle` object. This allows for additional customization, such as setting opacity:

![alt text](/assets/guides/components/image-1.png)

## Fill with Textures

Filling shapes with textures is just as simple:

![alt text](/assets/guides/components/image-2.png)

### Local vs. Global Texture Space

Textures can be applied in two coordinate spaces:

- **Local Space** (Default): The texture coordinates are mapped relative to the shape's dimensions and position. The texture coordinates use a normalized coordinate system where (0,0) is the top-left and (1,1) is the bottom-right of the shape, regardless of its actual pixel dimensions. For example, if you have a 300x200 pixel texture filling a 100x100 shape, the texture will be scaled to fit exactly within those 100x100 pixels. The texture's top-left corner (0,0) will align with the shape's top-left corner, and the texture's bottom-right corner (1,1) will align with the shape's bottom-right corner, stretching or compressing the texture as needed.

![alt text](/assets/guides/components/image-13.png)

- **Global Space**: Set `textureSpace: 'global'` to make the texture position and scale relative to the Graphics object's coordinate system. Despite the name, this isn't truly "global" - the texture remains fixed relative to the Graphics object itself, maintaining its position even when the object moves or scales. See how the image goes across all the shapes (in the same graphics) below:

![alt text](/assets/guides/components/image-11.png)

### Using Matrices with Textures

To modify texture coordinates, you can apply a transformation matrix, which is a mathematical tool used to scale, rotate, or translate the texture. If you're unfamiliar with transformation matrices, they allow for precise control over how textures are rendered, and you can explore more about them [here](https://learnwebgl.brown37.net/10_surface_properties/texture_mapping_transforms.html#:~:text=Overview%C2%B6,by%2D4%20transformation%20matrix).

![alt text](/assets/guides/components/image-4.png)

1. **Sprite Sheets**: If using a texture from a sprite sheet, the entire source texture will be used. To use a specific frame, create a new texture:

2. **Power of Two Textures**: Textures should be power-of-two dimensions for proper tiling in WebGL1 (WebGL2 and WebGPU are fine).

## Fill with Gradients

PixiJS supports both linear and radial gradients, which can be created using the `FillGradient` class. Gradients are particularly useful for adding visual depth and dynamic styling to shapes and text.

Linear gradients create a smooth color transition along a straight line. Here is an example of a simple linear gradient:

![alt text](/assets/guides/components/image-5.png)

You can control the gradient direction with the following properties:

- `start {x, y}`: These define the starting point of the gradient. For example, in a linear gradient, this is where the first color stop is positioned. These values are typically expressed in relative coordinates (0 to 1), where `0` represents the left/top edge and `1` represents the right/bottom edge of the shape.

- `end {x, y}`: These define the ending point of the gradient. Similar to `start {x, y}`, these values specify where the last color stop is positioned in the shape's local coordinate system.

Using these properties, you can create various gradient effects, such as horizontal, vertical, or diagonal transitions. For example, setting `start` to `{x: 0, y: 0}` and `end` to `{x: 1, y: 1}` would result in a diagonal gradient from the top-left to the bottom-right of the shape.

![alt text](/assets/guides/components/image-6.png)

Radial gradients create a smooth color transition in a circular pattern. Unlike linear gradients, they blend colors from one circle to another. Here is an example of a simple radial gradient:

![alt text](/assets/guides/components/image-7.png)

You can control the gradient's shape and size using the following properties:

- `center {x, y}`: These define the center of the inner circle where the gradient starts. Typically, these values are expressed in relative coordinates (0 to 1), where `0.5` represents the center of the shape.

- `innerRadius`: The radius of the inner circle. This determines the size of the gradient's starting point.

- `outerCenter {x, y}`: These define the center of the outer circle where the gradient ends. Like `center {x, y}`, these values are also relative coordinates.

- `outerRadius`: The radius of the outer circle. This determines the size of the gradient's ending point.

By adjusting these properties, you can create a variety of effects, such as small, concentrated gradients or large, expansive ones. For example, setting a small `r0` and a larger `r1` will create a gradient that starts does not start to transition until the inner circle radius is reached.

![alt text](/assets/guides/components/image-8.png)

### Gradient Gotcha's

1. **Memory Management**: Use `fillGradient.destroy()` to free up resources when gradients are no longer needed.

2. **Animation**: Update existing gradients instead of creating new ones for better performance.

3. **Custom Shaders**: For complex animations, custom shaders may be more efficient.

4. **Texture and Matrix Limitations**: Under the hood, gradient fills set both the texture and matrix properties internally. This means you cannot use a texture fill or matrix transformation at the same time as a gradient fill.

### Combining Textures and Colors

You can combine a texture or gradients with a color tint and alpha to achieve more complex and visually appealing effects. This allows you to overlay a color on top of the texture or gradient, adjusting its transparency with the alpha value.

![alt text](/assets/guides/components/image-10.png)

![alt text](/assets/guides/components/image-9.png)

Hopefully, this guide has shown you how easy and powerful fills can be when working with graphics (and text!). By mastering the `fill()` method, you can unlock endless possibilities for creating visually dynamic and engaging graphics in PixiJS. Have fun!

## Graphics Pixel Line

import { Sandpack } from '@codesandbox/sandpack-react';
import { dracula } from '@codesandbox/sandpack-themes';

**Examples:**

Example 1 (ts):
```ts
const obj = new Graphics()
  .rect(0, 0, 200, 100) // Create a rectangle with dimensions 200x100
  .fill('red'); // Fill the rectangle with a red color
```

Example 2 (ts):
```ts
// Using a number
const obj1 = new Graphics().rect(0, 0, 100, 100).fill(0xff0000);

// Using a hex string
const obj2 = new Graphics().rect(0, 0, 100, 100).fill('#ff0000');

// Using an array
const obj3 = new Graphics().rect(0, 0, 100, 100).fill([255, 0, 0]);

// Using a Color object
const color = new Color();
const obj4 = new Graphics().rect(0, 0, 100, 100).fill(color);
```

Example 3 (ts):
```ts
const obj = new Graphics().rect(0, 0, 100, 100).fill({
  color: 'red',
  alpha: 0.5, // 50% opacity
});
```

Example 4 (ts):
```ts
const texture = await Assets.load('assets/image.png');
const obj = new Graphics().rect(0, 0, 100, 100).fill(texture);
```

---

## NineSlice Sprite

**URL:** llms-txt#nineslice-sprite

**Contents:**
- **How NineSlice Works**
- **Width and Height Behavior**
  - **Original Width and Height**
- **Dynamic Updates**
- **API Reference**
- Particle Container

`NineSliceSprite` is a specialized type of `Sprite` that allows textures to be resized while preserving the corners and edges. It is particularly useful for building scalable UI elements like buttons, panels, or windows with rounded or decorated borders.

You can also pass just a texture, and the slice values will fall back to defaults or be inferred from the texture’s `defaultBorders`.

## **How NineSlice Works**

Here’s how a nine-slice texture is divided:

This ensures that decorative corners are preserved and the center content can scale as needed.

## **Width and Height Behavior**

Setting `.width` and `.height` on a `NineSliceSprite` updates the **geometry vertices**, not the texture UVs. This allows the texture to repeat or stretch correctly based on the slice regions. This also means that the `width` and `height` properties are not the same as the `scale` properties.

### **Original Width and Height**

If you need to know the original size of the nine-slice, you can access it through the `originalWidth` and `originalHeight` properties. These values are set when the `NineSliceSprite` is created and represent the dimensions of the texture before any scaling or resizing is applied.

## **Dynamic Updates**

You can change slice dimensions or size at runtime:

Each setter triggers a geometry update to reflect the changes.

- [NineSliceSprite](https://pixijs.download/release/docs/scene.NineSliceSprite.html)

## Particle Container

**Examples:**

Example 1 (ts):
```ts
import { NineSliceSprite, Texture } from 'pixi.js';

const nineSlice = new NineSliceSprite({
  texture: Texture.from('button.png'),
  leftWidth: 15,
  topHeight: 15,
  rightWidth: 15,
  bottomHeight: 15,
  width: 200,
  height: 80,
});

app.stage.addChild(nineSlice);
```

Example 2 (js):
```js
A                          B
  +---+----------------------+---+
C | 1 |          2           | 3 |
  +---+----------------------+---+
  |   |                      |   |
  | 4 |          5           | 6 |
  |   |                      |   |
  +---+----------------------+---+
D | 7 |          8           | 9 |
  +---+----------------------+---+

Areas:
  - 1, 3, 7, 9: Corners (remain unscaled)
  - 2, 8: Top/Bottom center (stretched horizontally)
  - 4, 6: Left/Right center (stretched vertically)
  - 5: Center (stretched in both directions)
```

Example 3 (ts):
```ts
// The texture will stretch to fit the new dimensions
nineSlice.width = 300;
nineSlice.height = 100;

// The nine-slice will increase in size uniformly
nineSlice.scale.set(2); // Doubles the size
```

Example 4 (ts):
```ts
console.log(nineSlice.originalWidth);
console.log(nineSlice.originalHeight);
```

---

## Ticker Plugin

**URL:** llms-txt#ticker-plugin

**Contents:**
- Usage
  - Default Behavior
  - Manual Registration

The `TickerPlugin` provides a built-in update loop for your PixiJS `Application`. This loop calls `.render()` at a regular cadence—by default, once per animation frame—and integrates with PixiJS's `Ticker` system for precise control over frame-based updates.

PixiJS includes this plugin automatically when you initialize an `Application`, but you can also opt out and add it manually.

The `TickerPlugin` is included automatically unless disabled:

### Manual Registration

If you're managing extensions yourself:

**Examples:**

Example 1 (ts):
```ts
const app = new Application();

await app.init({
  sharedTicker: false,
  autoStart: true,
});

app.ticker.add((ticker) => {
  // Custom update logic here
  bunny.rotation += 1 * ticker.deltaTime;
});
```

Example 2 (ts):
```ts
const app = new Application();

await app.init({
  autoStart: true, // Automatically starts the render loop
  sharedTicker: false, // Use a dedicated ticker
});
```

Example 3 (ts):
```ts
import { extensions, TickerPlugin } from 'pixi.js';

extensions.add(TickerPlugin);
```

---

## Full API Reference

**URL:** llms-txt#full-api-reference

* interface EventTypes {
	 *   'event-with-parameters': any[]
	 *   'event-with-example-handler': (...args: any[]) => void
	 * }
	 * ts
 * // Full white (opaque)
 * const white: RgbaArray = [1, 1, 1, 1];
 *
 * // Semi-transparent red
 * const transparentRed: RgbaArray = [1, 0, 0, 0.5];
 * ts
 * // CSS Color Names
 * new Color('red');
 * new Color('blue');
 * new Color('green');
 *
 * // Hex Values
 * new Color(0xff0000);     // RGB integer
 * new Color('#ff0000');    // 6-digit hex
 * new Color('#f00');       // 3-digit hex
 * new Color('#ff0000ff');  // 8-digit hex (with alpha)
 * new Color('#f00f');      // 4-digit hex (with alpha)
 *
 * // RGB/RGBA Objects
 * new Color({ r: 255, g: 0, b: 0 });
 * new Color({ r: 255, g: 0, b: 0, a: 0.5 });
 *
 * // RGB/RGBA Strings
 * new Color('rgb(255, 0, 0)');
 * new Color('rgba(255, 0, 0, 0.5)');
 * new Color('rgb(100% 0% 0%)');
 * new Color('rgba(100% 0% 0% / 50%)');
 *
 * // Arrays (normalized 0-1)
 * new Color([1, 0, 0]);           // RGB
 * new Color([1, 0, 0, 0.5]);      // RGBA
 * new Color(new Float32Array([1, 0, 0, 0.5]));
 *
 * // Arrays (0-255)
 * new Color(new Uint8Array([255, 0, 0]));
 * new Color(new Uint8ClampedArray([255, 0, 0, 128]));
 *
 * // HSL/HSLA
 * new Color({ h: 0, s: 100, l: 50 });
 * new Color({ h: 0, s: 100, l: 50, a: 0.5 });
 * new Color('hsl(0, 100%, 50%)');
 * new Color('hsla(0deg 100% 50% / 50%)');
 *
 * // HSV/HSVA
 * new Color({ h: 0, s: 100, v: 100 });
 * new Color({ h: 0, s: 100, v: 100, a: 0.5 });
 * js
 * import { Color } from 'pixi.js';
 *
 * new Color('red').toArray(); // [1, 0, 0, 1]
 * new Color(0xff0000).toArray(); // [1, 0, 0, 1]
 * new Color('ff0000').toArray(); // [1, 0, 0, 1]
 * new Color('#f00').toArray(); // [1, 0, 0, 1]
 * new Color('0xff0000ff').toArray(); // [1, 0, 0, 1]
 * new Color('#f00f').toArray(); // [1, 0, 0, 1]
 * new Color({ r: 255, g: 0, b: 0, a: 0.5 }).toArray(); // [1, 0, 0, 0.5]
 * new Color('rgb(255, 0, 0, 0.5)').toArray(); // [1, 0, 0, 0.5]
 * new Color([1, 1, 1]).toArray(); // [1, 1, 1, 1]
 * new Color([1, 0, 0, 0.5]).toArray(); // [1, 0, 0, 0.5]
 * new Color(new Float32Array([1, 0, 0, 0.5])).toArray(); // [1, 0, 0, 0.5]
 * new Color(new Uint8Array([255, 0, 0, 255])).toArray(); // [1, 0, 0, 1]
 * new Color(new Uint8ClampedArray([255, 0, 0, 255])).toArray(); // [1, 0, 0, 1]
 * new Color({ h: 0, s: 100, l: 50, a: 0.5 }).toArray(); // [1, 0, 0, 0.5]
 * new Color('hsl(0, 100%, 50%, 50%)').toArray(); // [1, 0, 0, 0.5]
 * new Color({ h: 0, s: 100, v: 100, a: 0.5 }).toArray(); // [1, 0, 0, 0.5]
 *
 * // Convert between formats
 * const color = new Color('red');
 * color.toHex();        // "#ff0000"
 * color.toRgbString();  // "rgb(255,0,0,1)"
 * color.toNumber();     // 0xff0000
 *
 * // Access components
 * color.red;    // 1
 * color.green;  // 0
 * color.blue;   // 0
 * color.alpha;  // 1
 *
 * // Chain operations
 * color
 *   .setAlpha(0.5)
 *   .multiply([0.5, 0.5, 0.5])
 *   .premultiply(0.8);
 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Use shared instance for one-off color operations
	 * Color.shared.setValue(0xff0000);
	 * const redHex = Color.shared.toHex();     // "#ff0000"
	 * const redRgb = Color.shared.toRgbArray(); // [1, 0, 0]
	 *
	 * // Temporary color transformations
	 * const colorNumber = Color.shared
	 *     .setValue('#ff0000')     // Set to red
	 *     .setAlpha(0.5)          // Make semi-transparent
	 *     .premultiply(0.8)       // Apply premultiplication
	 *     .toNumber();            // Convert to number
	 *
	 * // Chain multiple operations
	 * const result = Color.shared
	 *     .setValue(someColor)
	 *     .multiply(tintColor)
	 *     .toPremultiplied(alpha);
	 * ts
	 * const color = new Color('red');
	 * console.log(color.red); // 1
	 *
	 * const green = new Color('#00ff00');
	 * console.log(green.red); // 0
	 * ts
	 * const color = new Color('lime');
	 * console.log(color.green); // 1
	 *
	 * const red = new Color('#ff0000');
	 * console.log(red.green); // 0
	 * ts
	 * const color = new Color('blue');
	 * console.log(color.blue); // 1
	 *
	 * const yellow = new Color('#ffff00');
	 * console.log(yellow.blue); // 0
	 * ts
	 * const color = new Color('red');
	 * console.log(color.alpha); // 1 (fully opaque)
	 *
	 * const transparent = new Color('rgba(255, 0, 0, 0.5)');
	 * console.log(transparent.alpha); // 0.5 (semi-transparent)
	 * ts
	 * // Basic usage
	 * const color = new Color();
	 * color.setValue('#ff0000')
	 *     .setAlpha(0.5)
	 *     .premultiply(0.8);
	 *
	 * // Different formats
	 * color.setValue(0xff0000);          // Hex number
	 * color.setValue('#ff0000');         // Hex string
	 * color.setValue([1, 0, 0]);         // RGB array
	 * color.setValue([1, 0, 0, 0.5]);    // RGBA array
	 * color.setValue({ r: 1, g: 0, b: 0 }); // RGB object
	 *
	 * // Copy from another color
	 * const red = new Color('red');
	 * color.setValue(red);
	 * ts
	 * // Setting different color formats
	 * const color = new Color();
	 *
	 * color.value = 0xff0000;         // Hex number
	 * color.value = '#ff0000';        // Hex string
	 * color.value = [1, 0, 0];        // RGB array
	 * color.value = [1, 0, 0, 0.5];   // RGBA array
	 * color.value = { r: 1, g: 0, b: 0 }; // RGB object
	 *
	 * // Copying from another color
	 * const red = new Color('red');
	 * color.value = red;  // Copies red's components
	 *
	 * // Getting the value
	 * console.log(color.value);  // Returns original format
	 *
	 * // After modifications
	 * color.multiply([0.5, 0.5, 0.5]);
	 * console.log(color.value);  // Returns null
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Convert colors to RGBA objects
	 * new Color('white').toRgba();     // returns { r: 1, g: 1, b: 1, a: 1 }
	 * new Color('#ff0000').toRgba();   // returns { r: 1, g: 0, b: 0, a: 1 }
	 *
	 * // With transparency
	 * new Color('rgba(255,0,0,0.5)').toRgba(); // returns { r: 1, g: 0, b: 0, a: 0.5 }
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Convert colors to RGB objects
	 * new Color('white').toRgb();     // returns { r: 1, g: 1, b: 1 }
	 * new Color('#ff0000').toRgb();   // returns { r: 1, g: 0, b: 0 }
	 *
	 * // Alpha is ignored
	 * new Color('rgba(255,0,0,0.5)').toRgb(); // returns { r: 1, g: 0, b: 0 }
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Convert colors to RGBA strings
	 * new Color('white').toRgbaString();     // returns "rgba(255,255,255,1)"
	 * new Color('#ff0000').toRgbaString();   // returns "rgba(255,0,0,1)"
	 *
	 * // With transparency
	 * new Color([1, 0, 0, 0.5]).toRgbaString(); // returns "rgba(255,0,0,0.5)"
	 * ts
	 * // Basic usage
	 * new Color('white').toUint8RgbArray(); // returns [255, 255, 255]
	 * new Color('#ff0000').toUint8RgbArray(); // returns [255, 0, 0]
	 *
	 * // Using custom output array
	 * const rgb = new Uint8Array(3);
	 * new Color('blue').toUint8RgbArray(rgb); // rgb is now [0, 0, 255]
	 *
	 * // Using different array types
	 * new Color('red').toUint8RgbArray(new Uint8ClampedArray(3)); // [255, 0, 0]
	 * new Color('red').toUint8RgbArray([]); // [255, 0, 0]
	 * ts
	 * // Basic usage
	 * new Color('white').toArray();  // returns [1, 1, 1, 1]
	 * new Color('red').toArray();    // returns [1, 0, 0, 1]
	 *
	 * // With alpha
	 * new Color('rgba(255,0,0,0.5)').toArray(); // returns [1, 0, 0, 0.5]
	 *
	 * // Using custom output array
	 * const rgba = new Float32Array(4);
	 * new Color('blue').toArray(rgba); // rgba is now [0, 0, 1, 1]
	 * ts
	 * // Basic usage
	 * new Color('white').toRgbArray(); // returns [1, 1, 1]
	 * new Color('red').toRgbArray();   // returns [1, 0, 0]
	 *
	 * // Using custom output array
	 * const rgb = new Float32Array(3);
	 * new Color('blue').toRgbArray(rgb); // rgb is now [0, 0, 1]
	 * ts
	 * // Basic usage
	 * new Color('white').toNumber(); // returns 0xffffff
	 * new Color('red').toNumber();   // returns 0xff0000
	 *
	 * // Store as hex
	 * const color = new Color('blue');
	 * const hex = color.toNumber(); // 0x0000ff
	 * ts
	 * // Convert RGB to BGR
	 * new Color(0xffcc99).toBgrNumber(); // returns 0x99ccff
	 *
	 * // Common use case: platform-specific color format
	 * const color = new Color('orange');
	 * const bgrColor = color.toBgrNumber(); // Color with swapped R/B channels
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Convert RGB color to little endian format
	 * new Color(0xffcc99).toLittleEndianNumber(); // returns 0x99ccff
	 *
	 * // Common use cases:
	 * const color = new Color('orange');
	 * const leColor = color.toLittleEndianNumber(); // Swaps byte order for LE systems
	 *
	 * // Multiple conversions
	 * const colors = {
	 *     normal: 0xffcc99,
	 *     littleEndian: new Color(0xffcc99).toLittleEndianNumber(), // 0x99ccff
	 *     backToNormal: new Color(0x99ccff).toLittleEndianNumber()  // 0xffcc99
	 * };
	 * ts
	 * // Basic multiplication
	 * const color = new Color('#ff0000');
	 * color.multiply(0x808080); // 50% darker red
	 *
	 * // With transparency
	 * color.multiply([1, 1, 1, 0.5]); // 50% transparent
	 *
	 * // Chain operations
	 * color
	 *     .multiply('#808080')
	 *     .multiply({ r: 1, g: 1, b: 1, a: 0.5 });
	 * ts
	 * // Basic premultiplication
	 * const color = new Color('red');
	 * color.premultiply(0.5); // 50% transparent red with premultiplied RGB
	 *
	 * // Alpha only (RGB unchanged)
	 * color.premultiply(0.5, false); // 50% transparent, original RGB
	 *
	 * // Chain with other operations
	 * color
	 *     .multiply(0x808080)
	 *     .premultiply(0.5)
	 *     .toNumber();
	 * ts
	 * // Convert to premultiplied format
	 * const color = new Color('red');
	 *
	 * // Full opacity (0xFFRRGGBB)
	 * color.toPremultiplied(1.0); // 0xFFFF0000
	 *
	 * // 50% transparency with premultiplied RGB
	 * color.toPremultiplied(0.5); // 0x7F7F0000
	 *
	 * // 50% transparency without RGB premultiplication
	 * color.toPremultiplied(0.5, false); // 0x7FFF0000
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Basic colors
	 * new Color('red').toHex();    // returns "#ff0000"
	 * new Color('white').toHex();  // returns "#ffffff"
	 * new Color('black').toHex();  // returns "#000000"
	 *
	 * // From different formats
	 * new Color(0xff0000).toHex(); // returns "#ff0000"
	 * new Color([1, 0, 0]).toHex(); // returns "#ff0000"
	 * new Color({ r: 1, g: 0, b: 0 }).toHex(); // returns "#ff0000"
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // Fully opaque colors
	 * new Color('red').toHexa();   // returns "#ff0000ff"
	 * new Color('white').toHexa(); // returns "#ffffffff"
	 *
	 * // With transparency
	 * new Color('rgba(255, 0, 0, 0.5)').toHexa(); // returns "#ff00007f"
	 * new Color([1, 0, 0, 0]).toHexa(); // returns "#ff000000"
	 * ts
	 * // Basic alpha setting
	 * const color = new Color('red');
	 * color.setAlpha(0.5);  // 50% transparent red
	 *
	 * // Chain with other operations
	 * color
	 *     .setValue('#ff0000')
	 *     .setAlpha(0.8)    // 80% opaque
	 *     .premultiply(0.5); // Further modify alpha
	 *
	 * // Reset to fully opaque
	 * color.setAlpha(1);
	 * ts
	 * import { Color } from 'pixi.js';
	 *
	 * // CSS colors and hex values
	 * Color.isColorLike('red');          // true
	 * Color.isColorLike('#ff0000');      // true
	 * Color.isColorLike(0xff0000);       // true
	 *
	 * // Arrays (RGB/RGBA)
	 * Color.isColorLike([1, 0, 0]);      // true
	 * Color.isColorLike([1, 0, 0, 0.5]); // true
	 *
	 * // TypedArrays
	 * Color.isColorLike(new Float32Array([1, 0, 0]));          // true
	 * Color.isColorLike(new Uint8Array([255, 0, 0]));          // true
	 * Color.isColorLike(new Uint8ClampedArray([255, 0, 0]));   // true
	 *
	 * // Object formats
	 * Color.isColorLike({ r: 1, g: 0, b: 0 });            // true (RGB)
	 * Color.isColorLike({ r: 1, g: 0, b: 0, a: 0.5 });    // true (RGBA)
	 * Color.isColorLike({ h: 0, s: 100, l: 50 });         // true (HSL)
	 * Color.isColorLike({ h: 0, s: 100, l: 50, a: 0.5 }); // true (HSLA)
	 * Color.isColorLike({ h: 0, s: 100, v: 100 });        // true (HSV)
	 * Color.isColorLike({ h: 0, s: 100, v: 100, a: 0.5 });// true (HSVA)
	 *
	 * // Color instances
	 * Color.isColorLike(new Color('red')); // true
	 *
	 * // Invalid values
	 * Color.isColorLike(null);           // false
	 * Color.isColorLike(undefined);      // false
	 * Color.isColorLike({});             // false
	 * Color.isColorLike([]);             // false
	 * Color.isColorLike('not-a-color');  // false
	 * ts
 * // Create an object implementing PointData
 * const point: PointData = { x: 100, y: 200 };
 *
 * // Use with matrix transformations
 * const matrix = new Matrix();
 * matrix.translate(50, 50).apply(point);
 *
 * // Mix with other point types
 * const observablePoint = new ObservablePoint(() => {}, null, 0, 0);
 * const regularPoint = new Point(0, 0);
 * // All are PointData compatible
 * ts
 * // Basic point manipulation
 * const point: PointLike = new Point(10, 20);
 * point.set(30, 40);
 *
 * // Copy between points
 * const other = new Point();
 * point.copyTo(other);
 *
 * // Compare points
 * const same = point.equals(other); // true
 * ts
	 * const point1: PointLike = new Point(10, 20);
	 * const point2: PointLike = new Point(30, 40);
	 * point1.copyFrom(point2);
	 * console.log(point1.x, point1.y); // 30, 40
	 * ts
	 * const point1: PointLike = new Point(10, 20);
	 * const point2: PointLike = new Point(0, 0);
	 * point1.copyTo(point2);
	 * console.log(point2.x, point2.y); // 10, 20
	 * ts
	 * const point1: PointLike = new Point(10, 20);
	 * const point2: PointLike = new Point(10, 20);
	 * const point3: PointLike = new Point(30, 40);
	 * console.log(point1.equals(point2)); // true
	 * console.log(point1.equals(point3)); // false
	 * ts
	 * const point: PointLike = new Point(10, 20);
	 * point.set(30, 40);
	 * console.log(point.x, point.y); // 30, 40
	 * point.set(50); // Sets both x and y to 50
	 * console.log(point.x, point.y); // 50, 50
	 * ts
 * // Basic point creation
 * const point = new Point(100, 200);
 *
 * // Using with transformations
 * const matrix = new Matrix();
 * matrix.translate(50, 50).apply(point);
 *
 * // Point arithmetic
 * const start = new Point(0, 0);
 * const end = new Point(100, 100);
 * const middle = new Point(
 *     (start.x + end.x) / 2,
 *     (start.y + end.y) / 2
 * );
 * ts
	 * // Set x position
	 * const point = new Point();
	 * point.x = 100;
	 *
	 * // Use in calculations
	 * const width = rightPoint.x - leftPoint.x;
	 * ts
	 * // Set y position
	 * const point = new Point();
	 * point.y = 200;
	 *
	 * // Use in calculations
	 * const height = bottomPoint.y - topPoint.y;
	 * ts
	 * // Basic point cloning
	 * const original = new Point(100, 200);
	 * const copy = original.clone();
	 *
	 * // Clone and modify
	 * const modified = original.clone();
	 * modified.set(300, 400);
	 *
	 * // Verify independence
	 * console.log(original); // Point(100, 200)
	 * console.log(modified); // Point(300, 400)
	 * ts
	 * // Basic copying
	 * const source = new Point(100, 200);
	 * const target = new Point();
	 * target.copyFrom(source);
	 *
	 * // Copy and chain operations
	 * const point = new Point()
	 *     .copyFrom(source)
	 *     .set(x + 50, y + 50);
	 *
	 * // Copy from any PointData
	 * const data = { x: 10, y: 20 };
	 * point.copyFrom(data);
	 * ts
	 * // Basic copying
	 * const source = new Point(100, 200);
	 * const target = new Point();
	 * source.copyTo(target);
	 * ts
	 * // Basic equality check
	 * const p1 = new Point(100, 200);
	 * const p2 = new Point(100, 200);
	 * console.log(p1.equals(p2)); // true
	 *
	 * // Compare with PointData
	 * const data = { x: 100, y: 200 };
	 * console.log(p1.equals(data)); // true
	 *
	 * // Check different points
	 * const p3 = new Point(200, 300);
	 * console.log(p1.equals(p3)); // false
	 * ts
	 * // Basic position setting
	 * const point = new Point();
	 * point.set(100, 200);
	 *
	 * // Set both x and y to same value
	 * point.set(50); // x=50, y=50
	 *
	 * // Chain with other operations
	 * point
	 *     .set(10, 20)
	 *     .copyTo(otherPoint);
	 * ts
	 * // Use for temporary calculations
	 * const tempPoint = Point.shared;
	 * tempPoint.set(100, 200);
	 * matrix.apply(tempPoint);
	 *
	 * // Will be reset to (0,0) on next access
	 * const fresh = Point.shared; // x=0, y=0
	 * js
 * | a  c  tx |
 * | b  d  ty |
 * | 0  0  1  |
 * ts
 * // Create identity matrix
 * const matrix = new Matrix();
 *
 * // Create matrix with custom values
 * const transform = new Matrix(2, 0, 0, 2, 100, 100); // Scale 2x, translate 100,100
 *
 * // Transform a point
 * const point = { x: 10, y: 20 };
 * const transformed = transform.apply(point);
 *
 * // Chain transformations
 * matrix
 *     .translate(100, 50)
 *     .rotate(Math.PI / 4)
 *     .scale(2, 2);
 * 
	 * > array[0] = a  (x scale)
	 * > array[1] = b  (y skew)
	 * > array[2] = tx (x translation)
	 * > array[3] = c  (x skew)
	 * > array[4] = d  (y scale)
	 * > array[5] = ty (y translation)
	 * > ts
	 * // Create matrix from array
	 * const matrix = new Matrix();
	 * matrix.fromArray([
	 *     2, 0,  100,  // a, b, tx
	 *     0, 2,  100   // c, d, ty
	 * ]);
	 *
	 * // Create matrix from typed array
	 * const float32Array = new Float32Array([
	 *     1, 0, 0,     // Scale x1, no skew
	 *     0, 1, 0      // No skew, scale x1
	 * ]);
	 * matrix.fromArray(float32Array);
	 * ts
	 * // Set to identity matrix
	 * matrix.set(1, 0, 0, 1, 0, 0);
	 *
	 * // Set to scale matrix
	 * matrix.set(2, 0, 0, 2, 0, 0); // Scale 2x
	 *
	 * // Set to translation matrix
	 * matrix.set(1, 0, 0, 1, 100, 50); // Move 100,50
	 * 
	 * > Non-transposed:
	 * > [a, c, tx,
	 * > b, d, ty,
	 * > 0, 0, 1]
	 * >
	 * > Transposed:
	 * > [a, b, 0,
	 * > c, d, 0,
	 * > tx,ty,1]
	 * > ts
	 * // Basic array conversion
	 * const matrix = new Matrix(2, 0, 0, 2, 100, 100);
	 * const array = matrix.toArray();
	 *
	 * // Using existing array
	 * const float32Array = new Float32Array(9);
	 * matrix.toArray(false, float32Array);
	 *
	 * // Get transposed array
	 * const transposed = matrix.toArray(true);
	 * ts
	 * // Basic point transformation
	 * const matrix = new Matrix().translate(100, 50).rotate(Math.PI / 4);
	 * const point = new Point(10, 20);
	 * const transformed = matrix.apply(point);
	 *
	 * // Reuse existing point
	 * const output = new Point();
	 * matrix.apply(point, output);
	 * ts
	 * // Basic inverse transformation
	 * const matrix = new Matrix().translate(100, 50).rotate(Math.PI / 4);
	 * const worldPoint = new Point(150, 100);
	 * const localPoint = matrix.applyInverse(worldPoint);
	 *
	 * // Reuse existing point
	 * const output = new Point();
	 * matrix.applyInverse(worldPoint, output);
	 *
	 * // Convert mouse position to local space
	 * const mousePoint = new Point(mouseX, mouseY);
	 * const localMouse = matrix.applyInverse(mousePoint);
	 * ts
	 * // Basic translation
	 * const matrix = new Matrix();
	 * matrix.translate(100, 50); // Move right 100, down 50
	 *
	 * // Chain with other transformations
	 * matrix
	 *     .scale(2, 2)
	 *     .translate(100, 0)
	 *     .rotate(Math.PI / 4);
	 * ts
	 * // Basic scaling
	 * const matrix = new Matrix();
	 * matrix.scale(2, 3); // Scale 2x horizontally, 3x vertically
	 *
	 * // Chain with other transformations
	 * matrix
	 *     .translate(100, 100)
	 *     .scale(2, 2)     // Scales after translation
	 *     .rotate(Math.PI / 4);
	 * ts
	 * // Basic rotation
	 * const matrix = new Matrix();
	 * matrix.rotate(Math.PI / 4); // Rotate 45 degrees
	 *
	 * // Chain with other transformations
	 * matrix
	 *     .translate(100, 100) // Move to rotation center
	 *     .rotate(Math.PI)     // Rotate 180 degrees
	 *     .scale(2, 2);        // Scale after rotation
	 *
	 * // Common angles
	 * matrix.rotate(Math.PI / 2);  // 90 degrees
	 * matrix.rotate(Math.PI);      // 180 degrees
	 * matrix.rotate(Math.PI * 2);  // 360 degrees
	 * ts
	 * // Basic matrix combination
	 * const matrix = new Matrix();
	 * const other = new Matrix().translate(100, 0).rotate(Math.PI / 4);
	 * matrix.append(other);
	 * ts
	 * // Basic matrix multiplication
	 * const result = new Matrix();
	 * const matrixA = new Matrix().scale(2, 2);
	 * const matrixB = new Matrix().rotate(Math.PI / 4);
	 * result.appendFrom(matrixA, matrixB);
	 * ts
	 * // Basic transform setup
	 * const matrix = new Matrix();
	 * matrix.setTransform(
	 *     100, 100,    // position
	 *     0, 0,        // pivot
	 *     2, 2,        // scale
	 *     Math.PI / 4, // rotation (45 degrees)
	 *     0, 0         // skew
	 * );
	 * ts
	 * // Basic matrix prepend
	 * const matrix = new Matrix().scale(2, 2);
	 * const other = new Matrix().translate(100, 0);
	 * matrix.prepend(other); // Translation happens before scaling
	 * ts
	 * // Basic decomposition
	 * const matrix = new Matrix()
	 *     .translate(100, 100)
	 *     .rotate(Math.PI / 4)
	 *     .scale(2, 2);
	 *
	 * const transform = {
	 *     position: new Point(),
	 *     scale: new Point(),
	 *     pivot: new Point(),
	 *     skew: new Point(),
	 *     rotation: 0
	 * };
	 *
	 * matrix.decompose(transform);
	 * console.log(transform.position); // Point(100, 100)
	 * console.log(transform.rotation); // ~0.785 (PI/4)
	 * console.log(transform.scale); // Point(2, 2)
	 * ts
	 * // Basic matrix inversion
	 * const matrix = new Matrix()
	 *     .translate(100, 50)
	 *     .scale(2, 2);
	 *
	 * matrix.invert(); // Now transforms in opposite direction
	 *
	 * // Verify inversion
	 * const point = new Point(50, 50);
	 * const transformed = matrix.apply(point);
	 * const original = matrix.invert().apply(transformed);
	 * // original ≈ point
	 * ts
	 * // Check if matrix is identity
	 * const matrix = new Matrix();
	 * console.log(matrix.isIdentity()); // true
	 *
	 * // Check after transformations
	 * matrix.translate(100, 0);
	 * console.log(matrix.isIdentity()); // false
	 *
	 * // Reset and verify
	 * matrix.identity();
	 * console.log(matrix.isIdentity()); // true
	 * ts
	 * // Reset transformed matrix
	 * const matrix = new Matrix()
	 *     .scale(2, 2)
	 *     .rotate(Math.PI / 4);
	 * matrix.identity(); // Back to default state
	 *
	 * // Chain after reset
	 * matrix
	 *     .identity()
	 *     .translate(100, 100)
	 *     .scale(2, 2);
	 *
	 * // Compare with identity constant
	 * const isDefault = matrix.equals(Matrix.IDENTITY);
	 * ts
	 * // Basic matrix cloning
	 * const matrix = new Matrix()
	 *     .translate(100, 100)
	 *     .rotate(Math.PI / 4);
	 * const copy = matrix.clone();
	 *
	 * // Clone and modify
	 * const modified = matrix.clone()
	 *     .scale(2, 2);
	 *
	 * // Compare matrices
	 * console.log(matrix.equals(copy));     // true
	 * console.log(matrix.equals(modified)); // false
	 * ts
	 * // Basic matrix copying
	 * const source = new Matrix()
	 *     .translate(100, 100)
	 *     .rotate(Math.PI / 4);
	 * const target = new Matrix();
	 * target.copyFrom(source);
	 * ts
	 * // Basic equality check
	 * const m1 = new Matrix();
	 * const m2 = new Matrix();
	 * console.log(m1.equals(m2)); // true
	 *
	 * // Compare transformed matrices
	 * const transform = new Matrix()
	 *     .translate(100, 100)
	 * const clone = new Matrix()
	 *     .scale(2, 2);
	 * console.log(transform.equals(clone)); // false
	 * ts
	 * // Get identity matrix reference
	 * const identity = Matrix.IDENTITY;
	 * console.log(identity.isIdentity()); // true
	 *
	 * // Compare with identity
	 * const matrix = new Matrix();
	 * console.log(matrix.equals(Matrix.IDENTITY)); // true
	 *
	 * // Create new matrix instead of modifying IDENTITY
	 * const transform = new Matrix()
	 *     .copyFrom(Matrix.IDENTITY)
	 *     .translate(100, 100);
	 * ts
	 * // Use for temporary calculations
	 * const tempMatrix = Matrix.shared;
	 * tempMatrix.translate(100, 100).rotate(Math.PI / 4);
	 * const point = tempMatrix.apply({ x: 10, y: 20 });
	 *
	 * // Will be reset to identity on next access
	 * const fresh = Matrix.shared; // Back to identity
	 * ts
 * // Basic observer implementation
 * const observer: Observer<ObservablePoint> = {
 *     _onUpdate: (point) => {
 *         console.log(`Point updated to (${point.x}, ${point.y})`);
 *     }
 * };
 *
 * // Create observable point with observer
 * const point = new ObservablePoint(observer, 100, 100);
 *
 * // Observer will be notified on changes
 * point.x = 200; // Logs: Point updated to (200, 100)
 * ts
 * // Basic observable point usage
 * const point = new ObservablePoint(
 *     { _onUpdate: (p) => console.log(`Updated to (${p.x}, ${p.y})`) },
 *     100, 100
 * );
 *
 * // Update triggers callback
 * point.x = 200; // Logs: Updated to (200, 100)
 * point.y = 300; // Logs: Updated to (200, 300)
 *
 * // Set both coordinates
 * point.set(50, 50); // Logs: Updated to (50, 50)
 * ts
	 * // Basic cloning
	 * const point = new ObservablePoint(observer, 100, 200);
	 * const copy = point.clone();
	 *
	 * // Clone with new observer
	 * const newObserver = {
	 *     _onUpdate: (p) => console.log(`Clone updated: (${p.x}, ${p.y})`)
	 * };
	 * const watched = point.clone(newObserver);
	 *
	 * // Verify independence
	 * watched.set(300, 400); // Only triggers new observer
	 * ts
	 * // Basic position setting
	 * const point = new ObservablePoint(observer);
	 * point.set(100, 200);
	 *
	 * // Set both x and y to same value
	 * point.set(50); // x=50, y=50
	 * ts
	 * // Basic copying
	 * const source = new ObservablePoint(observer, 100, 200);
	 * const target = new ObservablePoint();
	 * target.copyFrom(source);
	 *
	 * // Copy and chain operations
	 * const point = new ObservablePoint()
	 *     .copyFrom(source)
	 *     .set(x + 50, y + 50);
	 *
	 * // Copy from any PointData
	 * const data = { x: 10, y: 20 };
	 * point.copyFrom(data);
	 * ts
	 * // Basic copying
	 * const source = new ObservablePoint(100, 200);
	 * const target = new ObservablePoint();
	 * source.copyTo(target);
	 * ts
	 * // Basic equality check
	 * const p1 = new ObservablePoint(100, 200);
	 * const p2 = new ObservablePoint(100, 200);
	 * console.log(p1.equals(p2)); // true
	 *
	 * // Compare with PointData
	 * const data = { x: 100, y: 200 };
	 * console.log(p1.equals(data)); // true
	 *
	 * // Check different points
	 * const p3 = new ObservablePoint(200, 300);
	 * console.log(p1.equals(p3)); // false
	 * ts
	 * // Basic x position
	 * const point = new ObservablePoint(observer);
	 * point.x = 100; // Triggers observer
	 *
	 * // Use in calculations
	 * const width = rightPoint.x - leftPoint.x;
	 * ts
	 * // Basic y position
	 * const point = new ObservablePoint(observer);
	 * point.y = 200; // Triggers observer
	 *
	 * // Use in calculations
	 * const height = bottomPoint.y - topPoint.y;
	 * ts
 * // Create bounds data
 * const bounds: BoundsData = {
 *     minX: 0,
 *     minY: 0,
 *     maxX: 100,
 *     maxY: 100
 * };
 *
 * // Calculate dimensions
 * const width = bounds.maxX - bounds.minX;
 * const height = bounds.maxY - bounds.minY;
 *
 * // Check if point is inside
 * const isInside = (x: number, y: number) =>
 *     x >= bounds.minX && x <= bounds.maxX &&
 *     y >= bounds.minY && y <= bounds.maxY;
 * ts
 * // Create bounds
 * const bounds = new Bounds();
 *
 * // Add a rectangular frame
 * bounds.addFrame(0, 0, 100, 100);
 * console.log(bounds.width, bounds.height); // 100, 100
 *
 * // Transform bounds
 * const matrix = new Matrix()
 *     .translate(50, 50)
 *     .rotate(Math.PI / 4);
 * bounds.applyMatrix(matrix);
 *
 * // Check point intersection
 * if (bounds.containsPoint(75, 75)) {
 *     console.log('Point is inside bounds!');
 * }
 * ts
	 * const bounds = new Bounds();
	 * // Set left edge
	 * bounds.minX = 100;
	 * ts
	 * const bounds = new Bounds();
	 * // Set top edge
	 * bounds.minY = 100;
	 * ts
	 * const bounds = new Bounds();
	 * // Set right edge
	 * bounds.maxX = 200;
	 * // Get width
	 * const width = bounds.maxX - bounds.minX;
	 * ts
	 * const bounds = new Bounds();
	 * // Set bottom edge
	 * bounds.maxY = 200;
	 * // Get height
	 * const height = bounds.maxY - bounds.minY;
	 * ts
	 * const bounds = new Bounds();
	 *
	 * // Check if newly created bounds are empty
	 * console.log(bounds.isEmpty()); // true, default bounds are empty
	 *
	 * // Add frame and check again
	 * bounds.addFrame(0, 0, 100, 100);
	 * console.log(bounds.isEmpty()); // false, bounds now have area
	 *
	 * // Clear bounds
	 * bounds.clear();
	 * console.log(bounds.isEmpty()); // true, bounds are empty again
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 *
	 * // Get rectangle representation
	 * const rect = bounds.rectangle;
	 * console.log(rect.x, rect.y, rect.width, rect.height);
	 *
	 * // Use for hit testing
	 * if (bounds.rectangle.contains(mouseX, mouseY)) {
	 *     console.log('Mouse is inside bounds!');
	 * }
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * console.log(bounds.isEmpty()); // false
	 * // Clear the bounds
	 * bounds.clear();
	 * console.log(bounds.isEmpty()); // true
	 * ts
	 * const bounds = new Bounds();
	 * bounds.set(0, 0, 100, 100);
	 * ts
	 * const bounds = new Bounds();
	 * bounds.addFrame(0, 0, 100, 100);
	 *
	 * // Add transformed frame
	 * const matrix = new Matrix()
	 *     .translate(50, 50)
	 *     .rotate(Math.PI / 4);
	 * bounds.addFrame(0, 0, 100, 100, matrix);
	 * ts
	 * const bounds = new Bounds();
	 * // Add simple rectangle
	 * const rect = new Rectangle(0, 0, 100, 100);
	 * bounds.addRect(rect);
	 *
	 * // Add transformed rectangle
	 * const matrix = new Matrix()
	 *     .translate(50, 50)
	 *     .rotate(Math.PI / 4);
	 * bounds.addRect(rect, matrix);
	 * ts
	 * const bounds = new Bounds();
	 *
	 * // Add child bounds
	 * const childBounds = sprite.getBounds();
	 * bounds.addBounds(childBounds);
	 *
	 * // Add transformed bounds
	 * const matrix = new Matrix()
	 *     .scale(2, 2);
	 * bounds.addBounds(childBounds, matrix);
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Create mask bounds
	 * const mask = new Bounds();
	 * mask.addFrame(50, 50, 150, 150);
	 * // Apply mask - results in bounds of (50,50,100,100)
	 * bounds.addBoundsMask(mask);
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Apply translation
	 * const translateMatrix = new Matrix()
	 *     .translate(50, 50);
	 * bounds.applyMatrix(translateMatrix);
	 * ts
	 * const bounds = new Bounds(0, 0, 200, 200);
	 * // Fit within viewport
	 * const viewport = new Rectangle(50, 50, 100, 100);
	 * bounds.fit(viewport);
	 * // bounds are now (50, 50, 150, 150)
	 * ts
	 * const bounds = new Bounds(0, 0, 200, 200);
	 * // Fit to specific coordinates
	 * bounds.fitBounds(50, 150, 50, 150);
	 * // bounds are now (50, 50, 150, 150)
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 *
	 * // Add equal padding
	 * bounds.pad(10);
	 * // bounds are now (-10, -10, 110, 110)
	 *
	 * // Add different padding for x and y
	 * bounds.pad(20, 10);
	 * // bounds are now (-30, -20, 130, 120)
	 * ts
	 * const bounds = new Bounds();
	 * bounds.set(10.2, 10.9, 50.1, 50.8);
	 *
	 * // Round to whole pixels
	 * bounds.ceil();
	 * // bounds are now (10, 10, 51, 51)
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 *
	 * // Create a copy
	 * const copy = bounds.clone();
	 *
	 * // Original and copy are independent
	 * bounds.pad(10);
	 * console.log(copy.width === bounds.width); // false
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 *
	 * // Scale uniformly
	 * bounds.scale(2);
	 * // bounds are now (0, 0, 200, 200)
	 *
	 * // Scale non-uniformly
	 * bounds.scale(0.5, 2);
	 * // bounds are now (0, 0, 100, 400)
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Get x position
	 * console.log(bounds.x); // 0
	 *
	 * // Move bounds horizontally
	 * bounds.x = 50;
	 * console.log(bounds.minX, bounds.maxX); // 50, 150
	 *
	 * // Width stays the same
	 * console.log(bounds.width); // Still 100
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Get y position
	 * console.log(bounds.y); // 0
	 *
	 * // Move bounds vertically
	 * bounds.y = 50;
	 * console.log(bounds.minY, bounds.maxY); // 50, 150
	 *
	 * // Height stays the same
	 * console.log(bounds.height); // Still 100
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Get width
	 * console.log(bounds.width); // 100
	 * // Resize width
	 * bounds.width = 200;
	 * console.log(bounds.maxX - bounds.minX); // 200
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Get height
	 * console.log(bounds.height); // 100
	 * // Resize height
	 * bounds.height = 150;
	 * console.log(bounds.maxY - bounds.minY); // 150
	 * ts
	 * const bounds = new Bounds(50, 0, 150, 100);
	 * console.log(bounds.left); // 50
	 * console.log(bounds.left === bounds.minX); // true
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * console.log(bounds.right); // 100
	 * console.log(bounds.right === bounds.maxX); // true
	 * ts
	 * const bounds = new Bounds(0, 25, 100, 125);
	 * console.log(bounds.top); // 25
	 * console.log(bounds.top === bounds.minY); // true
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 200);
	 * console.log(bounds.bottom); // 200
	 * console.log(bounds.bottom === bounds.maxY); // true
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Check if bounds are positive
	 * console.log(bounds.isPositive); // true
	 *
	 * // Negative bounds
	 * bounds.maxX = bounds.minX;
	 * console.log(bounds.isPositive); // false, width is 0
	 * ts
	 * const bounds = new Bounds();
	 * console.log(bounds.isValid); // false, default state
	 *
	 * // Set valid bounds
	 * bounds.addFrame(0, 0, 100, 100);
	 * console.log(bounds.isValid); // true
	 * ts
	 * const bounds = new Bounds();
	 *
	 * // Add vertices from geometry
	 * const vertices = new Float32Array([
	 *     0, 0,    // Vertex 1
	 *     100, 0,  // Vertex 2
	 *     100, 100 // Vertex 3
	 * ]);
	 * bounds.addVertexData(vertices, 0, 6);
	 *
	 * // Add transformed vertices
	 * const matrix = new Matrix()
	 *     .translate(50, 50)
	 *     .rotate(Math.PI / 4);
	 * bounds.addVertexData(vertices, 0, 6, matrix);
	 *
	 * // Add subset of vertices
	 * bounds.addVertexData(vertices, 2, 4); // Only second vertex
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * // Basic point check
	 * console.log(bounds.containsPoint(50, 50)); // true
	 * console.log(bounds.containsPoint(150, 150)); // false
	 *
	 * // Check edges
	 * console.log(bounds.containsPoint(0, 0));   // true, includes edges
	 * console.log(bounds.containsPoint(100, 100)); // true, includes edges
	 * ts
	 * const bounds = new Bounds(0, 0, 100, 100);
	 * console.log(bounds.toString()); // "[pixi.js:Bounds minX=0 minY=0 maxX=100 maxY=100 width=100 height=100]"
	 * ts
	 * const sourceBounds = new Bounds(0, 0, 100, 100);
	 * // Copy bounds
	 * const targetBounds = new Bounds();
	 * targetBounds.copyFrom(sourceBounds);
	 * ts
 * // Basic rectangle creation
 * const rect = new Rectangle(100, 100, 200, 150);
 *
 * // Use as container bounds
 * container.hitArea = new Rectangle(0, 0, 100, 100);
 *
 * // Check point containment
 * const isInside = rect.contains(mouseX, mouseY);
 *
 * // Manipulate dimensions
 * rect.width *= 2;
 * rect.height += 50;
 * ts
	 * // Check shape type
	 * const shape = new Rectangle(0, 0, 100, 100);
	 * console.log(shape.type); // 'rectangle'
	 *
	 * // Use in type guards
	 * if (shape.type === 'rectangle') {
	 *     console.log(shape.width, shape.height);
	 * }
	 * ts
	 * // Basic x position
	 * const rect = new Rectangle();
	 * rect.x = 100;
	 * ts
	 * // Basic y position
	 * const rect = new Rectangle();
	 * rect.y = 100;
	 * ts
	 * // Basic width setting
	 * const rect = new Rectangle();
	 * rect.width = 200;
	 * ts
	 * // Basic height setting
	 * const rect = new Rectangle();
	 * rect.height = 150;
	 * ts
	 * // Get left edge position
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * console.log(rect.left); // 100
	 *
	 * // Use in alignment calculations
	 * sprite.x = rect.left + padding;
	 *
	 * // Compare positions
	 * if (point.x > rect.left) {
	 *     console.log('Point is right of rectangle');
	 * }
	 * ts
	 * // Get right edge position
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * console.log(rect.right); // 300
	 *
	 * // Align to right edge
	 * sprite.x = rect.right - sprite.width;
	 *
	 * // Check boundaries
	 * if (point.x < rect.right) {
	 *     console.log('Point is inside right bound');
	 * }
	 * ts
	 * // Get top edge position
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * console.log(rect.top); // 100
	 *
	 * // Position above rectangle
	 * sprite.y = rect.top - sprite.height;
	 *
	 * // Check vertical position
	 * if (point.y > rect.top) {
	 *     console.log('Point is below top edge');
	 * }
	 * ts
	 * // Get bottom edge position
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * console.log(rect.bottom); // 250
	 *
	 * // Stack below rectangle
	 * sprite.y = rect.bottom + margin;
	 *
	 * // Check vertical bounds
	 * if (point.y < rect.bottom) {
	 *     console.log('Point is above bottom edge');
	 * }
	 * ts
	 * // Check zero dimensions
	 * const rect = new Rectangle(100, 100, 0, 50);
	 * console.log(rect.isEmpty()); // true
	 * ts
	 * // Get fresh empty rectangle
	 * const empty = Rectangle.EMPTY;
	 * console.log(empty.isEmpty()); // true
	 * ts
	 * // Basic cloning
	 * const original = new Rectangle(100, 100, 200, 150);
	 * const copy = original.clone();
	 *
	 * // Clone and modify
	 * const modified = original.clone();
	 * modified.width *= 2;
	 * modified.height += 50;
	 *
	 * // Verify independence
	 * console.log(original.width);  // 200
	 * console.log(modified.width);  // 400
	 * ts
	 * // Convert bounds to rectangle
	 * const bounds = container.getBounds();
	 * const rect = new Rectangle().copyFromBounds(bounds);
	 * ts
	 * // Basic copying
	 * const source = new Rectangle(100, 100, 200, 150);
	 * const target = new Rectangle();
	 * target.copyFrom(source);
	 *
	 * // Chain with other operations
	 * const rect = new Rectangle()
	 *     .copyFrom(source)
	 *     .pad(10);
	 * ts
	 * // Basic copying
	 * const source = new Rectangle(100, 100, 200, 150);
	 * const target = new Rectangle();
	 * source.copyTo(target);
	 *
	 * // Chain with other operations
	 * const result = source
	 *     .copyTo(new Rectangle())
	 *     .getBounds();
	 * ts
	 * // Basic containment check
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * const isInside = rect.contains(150, 125); // true
	 * // Check edge cases
	 * console.log(rect.contains(100, 100)); // true (on edge)
	 * console.log(rect.contains(300, 250)); // false (outside)
	 * ts
	 * // Basic stroke check
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * const isOnStroke = rect.strokeContains(150, 100, 4); // 4px line width
	 *
	 * // Check with different alignments
	 * const innerStroke = rect.strokeContains(150, 100, 4, 1);   // Inside
	 * const centerStroke = rect.strokeContains(150, 100, 4, 0.5); // Centered
	 * const outerStroke = rect.strokeContains(150, 100, 4, 0);   // Outside
	 * ts
	 * // Basic intersection check
	 * const rect1 = new Rectangle(0, 0, 100, 100);
	 * const rect2 = new Rectangle(50, 50, 100, 100);
	 * console.log(rect1.intersects(rect2)); // true
	 *
	 * // With transformation matrix
	 * const matrix = new Matrix();
	 * matrix.rotate(Math.PI / 4); // 45 degrees
	 * console.log(rect1.intersects(rect2, matrix)); // Checks with rotation
	 *
	 * // Edge cases
	 * const zeroWidth = new Rectangle(0, 0, 0, 100);
	 * console.log(rect1.intersects(zeroWidth)); // false (no area)
	 * ts
	 * // Basic padding
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * rect.pad(10); // Adds 10px padding on all sides
	 *
	 * // Different horizontal and vertical padding
	 * const uiRect = new Rectangle(0, 0, 100, 50);
	 * uiRect.pad(20, 10); // 20px horizontal, 10px vertical
	 * ts
	 * // Basic fitting
	 * const container = new Rectangle(0, 0, 100, 100);
	 * const content = new Rectangle(25, 25, 200, 200);
	 * content.fit(container); // Clips to container bounds
	 * ts
	 * // Basic grid alignment
	 * const rect = new Rectangle(10.2, 10.6, 100.8, 100.4);
	 * rect.ceil(); // Aligns to whole pixels
	 *
	 * // Custom resolution grid
	 * const uiRect = new Rectangle(5.3, 5.7, 50.2, 50.8);
	 * uiRect.ceil(0.5); // Aligns to half pixels
	 *
	 * // Use with precision value
	 * const preciseRect = new Rectangle(20.001, 20.999, 100.001, 100.999);
	 * preciseRect.ceil(1, 0.01); // Handles small decimal variations
	 * ts
	 * const rect = new Rectangle(50, 50, 100, 100);
	 *
	 * // Scale uniformly
	 * rect.scale(0.5, 0.5);
	 * // rect is now: x=25, y=25, width=50, height=50
	 *
	 * // non-uniformly
	 * rect.scale(0.5, 1);
	 * // rect is now: x=25, y=50, width=50, height=100
	 * ts
	 * // Basic enlargement
	 * const rect = new Rectangle(50, 50, 100, 100);
	 * const other = new Rectangle(0, 0, 200, 75);
	 * rect.enlarge(other);
	 * // rect is now: x=0, y=0, width=200, height=150
	 *
	 * // Use for bounding box calculation
	 * const bounds = new Rectangle();
	 * objects.forEach((obj) => {
	 *     bounds.enlarge(obj.getBounds());
	 * });
	 * ts
	 * // Basic bounds retrieval
	 * const rect = new Rectangle(100, 100, 200, 150);
	 * const bounds = rect.getBounds();
	 *
	 * // Reuse existing rectangle
	 * const out = new Rectangle();
	 * rect.getBounds(out);
	 * ts
	 * // Check if one rectangle contains another
	 * const container = new Rectangle(0, 0, 100, 100);
	 * const inner = new Rectangle(25, 25, 50, 50);
	 *
	 * console.log(container.containsRect(inner)); // true
	 *
	 * // Check overlapping rectangles
	 * const partial = new Rectangle(75, 75, 50, 50);
	 * console.log(container.containsRect(partial)); // false
	 *
	 * // Zero-area rectangles
	 * const empty = new Rectangle(0, 0, 0, 100);
	 * console.log(container.containsRect(empty)); // false
	 * ts
	 * // Basic usage
	 * const rect = new Rectangle();
	 * rect.set(100, 100, 200, 150);
	 *
	 * // Chain with other operations
	 * const bounds = new Rectangle()
	 *     .set(0, 0, 100, 100)
	 *     .pad(10);
	 * ts
 * // Basic destruction - only this container
 * container.destroy({ children: false });
 *
 * // Deep destruction - container and all children
 * container.destroy({ children: true });
 *
 * // Cleanup pattern
 * function cleanupScene(scene: Container) {
 *     // Remove from parent first
 *     scene.parent?.removeChild(scene);
 *     // Then destroy with all children
 *     scene.destroy({ children: true });
 * }
 * js
	 * container.destroy({ children: true });
	 * ts
 * // Basic texture cleanup
 * sprite.destroy({
 *     texture: true
 * });
 *
 * // Complete texture cleanup
 * sprite.destroy({
 *     texture: true,
 *     textureSource: true
 * });
 * js
	 * texturedObject.destroy({ texture: true });
	 * js
	 * texturedObject.destroy({ textureSource: true });
	 * ts
 * // Basic context cleanup
 * graphics.destroy({
 *     context: true
 * });
 *
 * // Full graphics cleanup
 * graphics.destroy({
 *     context: true,
 *     texture: true,
 *     textureSource: true
 * });
 * js
	 * graphics.destroy({ context: true });
	 * ts
 * // Basic text cleanup
 * text.destroy({ style: false }); // Keep style for reuse
 * text.destroy({ style: true }); // Destroy style as well
 * ts
 * // Destroy the container and all its children, including textures and styles
 * container.destroy({
 *     children: true,
 *     texture: true,
 *     textureSource: true,
 *     context: true,
 *     style: true
 * });
 * ts
 * import { extensions, ExtensionType } from 'pixi.js';
 *
 * // Register a simple object extension
 * extensions.add({
 *   extension: {
 *       type: ExtensionType.LoadParser,
 *       name: 'my-loader',
 *       priority: 100, // Optional priority for ordering
 *   },
 *   // add load parser functions
 * });
 *
 * // Register a class-based extension
 * class MyRendererPlugin {
 *     static extension = {
 *         type: [ExtensionType.WebGLSystem, ExtensionType.WebGPUSystem],
 *         name: 'myRendererPlugin'
 *     };
 *
 *    // add renderer plugin methods
 * }
 * extensions.add(MyRendererPlugin);
 *
 * // Remove extensions
 * extensions.remove(MyRendererPlugin);
 * ts
	 * // Remove a single extension
	 * extensions.remove(MyRendererPlugin);
	 *
	 * // Remove multiple extensions
	 * extensions.remove(
	 *     MyRendererPlugin,
	 *     MySystemPlugin
	 * );
	 * ts
	 * // Register a simple extension
	 * extensions.add(MyRendererPlugin);
	 *
	 * // Register multiple extensions
	 * extensions.add(
	 *     MyRendererPlugin,
	 *     MySystemPlugin,
	 * });
	 * ts
	 * // Create a mixin with shared properties
	 * const moveable = {
	 *     x: 0,
	 *     y: 0,
	 *     move(x: number, y: number) {
	 *         this.x += x;
	 *         this.y += y;
	 *     }
	 * };
	 *
	 * // Create a mixin with computed properties
	 * const scalable = {
	 *     scale: 1,
	 *     get scaled() {
	 *         return this.scale > 1;
	 *     }
	 * };
	 *
	 * // Apply mixins to a class
	 * extensions.mixin(Sprite, moveable, scalable);
	 *
	 * // Use mixed-in properties
	 * const sprite = new Sprite();
	 * sprite.move(10, 20);
	 * console.log(sprite.x, sprite.y); // 10, 20
	 * js
 *
 * const texture = await Assets.load('assets/image.png');
 *
 * // once Assets has loaded the image it will be available via the from method
 * const sameTexture = Texture.from('assets/image.png');
 * // another way to access the texture once loaded
 * const sameAgainTexture = Assets.get('assets/image.png');
 *
 * const sprite1 = new Sprite(texture);
 *
 * js
 * import { Sprite, Texture } from 'pixi.js';
 *
 * const texture = await Assets.load('assets/image.png');
 * const sprite1 = new Sprite(texture);
 * const sprite2 = new Sprite(texture);
 * ts
 * import { Application, Sprite, Graphics } from 'pixi.js';
 *
 * const app = new Application();
 * await app.init();
 *
 * // Create a complex display object
 * const container = new Container();
 *
 * const graphics = new Graphics()
 *     .circle(0, 0, 50)
 *     .fill('red');
 *
 * const sprite = new Sprite(texture);
 * sprite.x = 100;
 *
 * container.addChild(graphics, sprite);
 *
 * // Generate a texture from the container
 * const generatedTexture = app.renderer.textureGenerator.generateTexture({
 *     target: container,
 *     resolution: 2,
 *     antialias: true
 * });
 *
 * // Use the generated texture
 * const newSprite = new Sprite(generatedTexture);
 * app.stage.addChild(newSprite);
 *
 * // Clean up when done
 * generatedTexture.destroy(true);
 * ts
	 * // Basic usage with a container
	 * const container = new Container();
	 * container.addChild(
	 *     new Graphics()
	 *         .circle(0, 0, 50)
	 *         .fill('red')
	 * );
	 *
	 * const texture = renderer.textureGenerator.generateTexture(container);
	 *
	 * // Advanced usage with options
	 * const texture = renderer.textureGenerator.generateTexture({
	 *     target: container,
	 *     frame: new Rectangle(0, 0, 100, 100), // Specific region
	 *     resolution: 2,                        // High DPI
	 *     clearColor: '#ff0000',               // Red background
	 *     antialias: true                      // Smooth edges
	 * });
	 *
	 * // Create a sprite from the generated texture
	 * const sprite = new Sprite(texture);
	 *
	 * // Clean up when done
	 * texture.destroy(true);
	 * ts
 * // Create a basic sprite with texture
 * const sprite = new Sprite({
 *     texture: Texture.from('sprite.png')
 * });
 *
 * // Create a centered sprite with rounded position
 * const centeredSprite = new Sprite({
 *     texture: Texture.from('centered.png'),
 *     anchor: 0.5,        // Center point
 *     roundPixels: true,  // Crisp rendering
 *     x: 100,            // Position from ViewContainerOptions
 *     y: 100
 * });
 *
 * // Create a sprite with specific anchor points
 * const anchoredSprite = new Sprite({
 *     texture: Texture.from('corner.png'),
 *     anchor: {
 *         x: 1,  // Right-aligned
 *         y: 0   // Top-aligned
 *     }
 * });
 * ts
	 * // Create a sprite with a texture
	 * const sprite = new Sprite({
	 *     texture: Texture.from('path/to/image.png')
	 * });
	 * // Update the texture later
	 * sprite.texture = Texture.from('path/to/another-image.png');
	 * ts
	 * // Centered anchor
	 * anchor: 0.5
	 * // Separate x/y anchor
	 * anchor: { x: 0.5, y: 0.5 }
	 * // Right-aligned anchor
	 * anchor: { x: 1, y: 0 }
	 * ts
	 * const sprite = new Sprite({
	 *     texture: Texture.from('sprite.png'),
	 *     roundPixels: true // Ensures crisp rendering
	 * });
	 * ts
 * // Create a sprite directly from an image path
 * const sprite = Sprite.from('assets/image.png');
 * sprite.position.set(100, 100);
 * app.stage.addChild(sprite);
 *
 * // Create from a spritesheet (more efficient)
 * const sheet = await Assets.load('assets/spritesheet.json');
 * const sprite = new Sprite(sheet.textures['image.png']);
 *
 * // Create with specific options
 * const configuredSprite = new Sprite({
 *     texture: Texture.from('sprite.png'),
 *     anchor: 0.5,           // Center anchor point
 *     position: { x: 100, y: 100 },
 *     scale: { x: 2, y: 2 }, // Double size
 *     rotation: Math.PI / 4   // 45 degrees
 * });
 *
 * // Animate sprite properties
 * app.ticker.add(() => {
 *     sprite.rotation += 0.1;      // Rotate
 *     sprite.scale.x = Math.sin(performance.now() / 1000) + 1; // Pulse scale
 * });
 * ts
	 * // Create from path or URL
	 * const sprite = Sprite.from('assets/image.png');
	 *
	 * // Create from existing texture
	 * const sprite = Sprite.from(texture);
	 *
	 * // Create from canvas
	 * const canvas = document.createElement('canvas');
	 * const sprite = Sprite.from(canvas, true); // Skip caching new texture
	 * ts
	 * // Create sprite with texture
	 * const sprite = new Sprite({
	 *     texture: Texture.from('sprite.png')
	 * });
	 *
	 * // Update texture
	 * sprite.texture = Texture.from('newSprite.png');
	 *
	 * // Use texture from spritesheet
	 * const sheet = await Assets.load('spritesheet.json');
	 * sprite.texture = sheet.textures['frame1.png'];
	 *
	 * // Reset to empty texture
	 * sprite.texture = Texture.EMPTY;
	 * ts
	 * const texture = new Texture({
	 *     source: new TextureSource({ width: 300, height: 300 }),
	 *     frame: new Rectangle(196, 66, 58, 56),
	 *     trim: new Rectangle(4, 4, 58, 56),
	 *     orig: new Rectangle(0, 0, 64, 64),
	 *     rotate: 2,
	 * });
	 * const sprite = new Sprite(texture);
	 * const visualBounds = sprite.visualBounds;
	 * // console.log(visualBounds); // { minX: -4, maxX: 62, minY: -4, maxY: 60 }
	 */
	get visualBounds(): BoundsData;
	/**
	 * Destroys this sprite renderable and optionally its texture.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * sprite.destroy();
	 * sprite.destroy(true);
	 * sprite.destroy({ texture: true, textureSource: true });
	 */
	destroy(options?: DestroyOptions): void;
	/**
	 * The anchor sets the origin point of the sprite. The default value is taken from the {@link Texture}
	 * and passed to the constructor.
	 *
	 * - The default is `(0,0)`, this means the sprite's origin is the top left.
	 * - Setting the anchor to `(0.5,0.5)` means the sprite's origin is centered.
	 * - Setting the anchor to `(1,1)` would mean the sprite's origin point will be the bottom right corner.
	 *
	 * If you pass only single parameter, it will set both x and y to the same value as shown in the example below.
	 * @example
	 * 
	 */
	get anchor(): ObservablePoint;
	set anchor(value: PointData | number);
	/**
	 * The width of the sprite, setting this will actually modify the scale to achieve the value set.
	 * @example
	 * 
	 */
	get width(): number;
	set width(value: number);
	/**
	 * The height of the sprite, setting this will actually modify the scale to achieve the value set.
	 * @example
	 * 
	 */
	get height(): number;
	set height(value: number);
	/**
	 * Retrieves the size of the Sprite as a [Size]{@link Size} object based on the texture dimensions and scale.
	 * This is faster than getting width and height separately as it only calculates the bounds once.
	 * @example
	 * 
	 * @param out - Optional object to store the size in, to avoid allocating a new object
	 * @returns The size of the Sprite
	 */
	getSize(out?: Size): Size;
	/**
	 * Sets the size of the Sprite to the specified width and height.
	 * This is faster than setting width and height separately as it only recalculates bounds once.
	 * @example
	 * 
	 * @param value - This can be either a number or a {@link Size} object
	 * @param height - The height to set. Defaults to the value of `width` if not provided
	 */
	setSize(value: number | Optional<Size, "height">, height?: number): void;
}
type OPTIONAL_SPACE = " " | "";
type FLOPS<T = UniformData> = T extends {
	value: infer V;
} ? V : never;
interface System$1 {
	extension: {
		name: string;
	};
	defaultOptions?: any;
	new (...args: any): any;
}
type SystemsWithExtensionList = System$1[];
type InstanceType$1<T extends new (...args: any) => any> = T extends new (...args: any) => infer R ? R : any;
type NameType<T extends SystemsWithExtensionList> = T[number]["extension"]["name"];
type NotUnknown<T> = T extends unknown ? keyof T extends never ? never : T : T;
type KnownProperties<T> = {
	[K in keyof T as NotUnknown<T[K]> extends never ? never : K]: T[K];
};
type FlattenOptions<T> = T extends {
	[K: string]: infer U;
} ? U : never;
type OptionsUnion<T extends SystemsWithExtensionList> = FlattenOptions<SeparateOptions<T>>;
type DefaultOptionsTypes<T extends SystemsWithExtensionList> = {
	[K in NameType<T>]: Extract<T[number], {
		extension: {
			name: K;
		};
	}>["defaultOptions"];
};
type SeparateOptions<T extends SystemsWithExtensionList> = KnownProperties<DefaultOptionsTypes<T>>;
type UnionToIntersection<U> = (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;
type MaskMode = "pushMaskBegin" | "pushMaskEnd" | "popMaskBegin" | "popMaskEnd";
declare class AlphaMaskEffect extends FilterEffect implements PoolItem {
	constructor();
	get sprite(): Sprite;
	set sprite(value: Sprite);
	get inverse(): boolean;
	set inverse(value: boolean);
	init: () => void;
}
interface MaskConversionTest {
	test: (item: any) => boolean;
	maskClass: new (item: any) => Effect & PoolItem;
}
type MaskMode$1 = "pushMaskBegin" | "pushMaskEnd" | "popMaskBegin" | "popMaskEnd";
interface EnsurePrecisionOptions {
	requestedVertexPrecision: PRECISION;
	requestedFragmentPrecision: PRECISION;
	maxSupportedVertexPrecision: PRECISION;
	maxSupportedFragmentPrecision: PRECISION;
}
interface AdvancedBlendInstruction extends Instruction {
	renderPipeId: "blendMode";
	blendMode: BLEND_MODES;
	activeBlend: Renderable[];
}
declare const imageTypes: {
	png: string;
	jpg: string;
	webp: string;
};
type Formats = keyof typeof imageTypes;
/**
 * System for exporting content from a renderer. It provides methods to extract content as images,
 * canvases, or raw pixel data. Available through `renderer.extract`.
 * @example
 * 
 *
 * Features:
 * - Extract as various formats (PNG, JPEG, WebP)
 * - Control output quality and resolution
 * - Extract specific regions
 * - Download extracted content
 * - Debug visualization
 *
 * Common Use Cases:
 * - Creating thumbnails
 * - Saving game screenshots
 * - Processing visual content
 * - Debugging renders
 * - Creating textures from rendered content
 *
 * Performance Considerations:
 * - Extraction operations are relatively expensive
 * - Consider caching results for frequently used content
 * - Be mindful of resolution and format choices
 * - Large extractions may impact performance
 */
export declare class ExtractSystem implements System {
	/**
	 * Default options for image extraction.
	 * @example
	 * 
	 */
	static defaultImageOptions: ImageOptions;
	/** @param renderer - The renderer this System works for. */
	constructor(renderer: Renderer);
	/**
	 * Creates an IImage from a display object or texture.
	 * @param options - Options for creating the image, or the target to extract
	 * @returns Promise that resolves with the generated IImage
	 * @example
	 * 
	 */
	image(options: ExtractImageOptions | Container | Texture): Promise<ImageLike>;
	/**
	 * Converts the target into a base64 encoded string.
	 *
	 * This method works by first creating
	 * a canvas using `Extract.canvas` and then converting it to a base64 string.
	 * @param options - The options for creating the base64 string, or the target to extract
	 * @returns Promise that resolves with the base64 encoded string
	 * @example
	 * 
	 * @throws Will throw an error if the platform doesn't support any of:
	 * - ICanvas.toDataURL
	 * - ICanvas.toBlob
	 * - ICanvas.convertToBlob
	 */
	base64(options: ExtractImageOptions | Container | Texture): Promise<string>;
	/**
	 * Creates a Canvas element, renders the target to it and returns it.
	 * This method is useful for creating static images or when you need direct canvas access.
	 * @param options - The options for creating the canvas, or the target to extract
	 * @returns A Canvas element with the texture rendered on
	 * @example
	 * 
	 */
	canvas(options: ExtractOptions | Container | Texture): ICanvas;
	/**
	 * Returns a one-dimensional array containing the pixel data of the entire texture in RGBA order,
	 * with integer values between 0 and 255 (inclusive).
	 * > [!NOE] The returned array is a flat Uint8Array where every 4 values represent RGBA
	 * @param options - The options for extracting the image, or the target to extract
	 * @returns One-dimensional Uint8Array containing the pixel data in RGBA format
	 * @example
	 * 
	 */
	pixels(options: ExtractOptions | Container | Texture): GetPixelsOutput;
	/**
	 * Creates a texture from a display object or existing texture.
	 *
	 * This is useful for creating
	 * reusable textures from rendered content or making copies of existing textures.
	 * > [!NOTE] The returned texture should be destroyed when no longer needed
	 * @param options - The options for creating the texture, or the target to extract
	 * @returns A new texture containing the extracted content
	 * @example
	 * 
	 */
	texture(options: ExtractOptions | Container | Texture): Texture;
	/**
	 * Extracts and downloads content from the renderer as an image file.
	 * This is a convenient way to save screenshots or export rendered content.
	 * > [!NOTE] The download will use PNG format regardless of the filename extension
	 * @param options - The options for downloading and extracting the image, or the target to extract
	 * @example
	 * 
	 */
	download(options: ExtractDownloadOptions | Container | Texture): void;
	destroy(): void;
}
interface UniformParserDefinition {
	type: UNIFORM_TYPES;
	test(data: UniformData): boolean;
	ubo?: string;
	uboWgsl?: string;
	uboStd40?: string;
	uniform?: string;
}
declare const DefaultWebGPUSystems: (typeof BackgroundSystem | typeof GlobalUniformSystem | typeof HelloSystem | typeof ViewSystem | typeof RenderGroupSystem | typeof TextureGCSystem | typeof GenerateTextureSystem | typeof ExtractSystem | typeof RendererInitHook | typeof RenderableGCSystem | typeof SchedulerSystem | typeof GpuUboSystem | typeof GpuEncoderSystem | typeof GpuDeviceSystem | typeof GpuLimitsSystem | typeof GpuBufferSystem | typeof GpuTextureSystem | typeof GpuRenderTargetSystem | typeof GpuShaderSystem | typeof GpuStateSystem | typeof PipelineSystem | typeof GpuColorMaskSystem | typeof GpuStencilSystem | typeof BindGroupSystem)[];
declare const DefaultWebGPUPipes: (typeof BlendModePipe | typeof BatcherPipe | typeof SpritePipe | typeof RenderGroupPipe | typeof AlphaMaskPipe | typeof StencilMaskPipe | typeof ColorMaskPipe | typeof CustomRenderPipe | typeof GpuUniformBatchPipe)[];
/**
 * The default WebGPU systems. These are the systems that are added by default to the WebGPURenderer.
 */
export type WebGPUSystems = ExtractSystemTypes<typeof DefaultWebGPUSystems> & PixiMixins.RendererSystems & PixiMixins.WebGPUSystems;
/**
 * Options for WebGPURenderer.
 */
export interface WebGPUOptions extends SharedRendererOptions, ExtractRendererOptions<typeof DefaultWebGPUSystems>, PixiMixins.WebGPUOptions {
}
export interface WebGPURenderer<T extends ICanvas = HTMLCanvasElement> extends AbstractRenderer<WebGPUPipes, WebGPUOptions, T>, WebGPUSystems {
}
/**
 * The WebGPU PixiJS Renderer. This renderer allows you to use the next-generation graphics API, WebGPU.
 * 
 *
 * You can use {@link autoDetectRenderer} to create a renderer that will automatically detect the best
 * renderer for the environment.
 * 
 *
 * The renderer is composed of systems that manage specific tasks. The following systems are added by default
 * whenever you create a WebGPU renderer:
 *
 * | WebGPU Core Systems                      | Systems that are specific to the WebGL renderer                               |
 * | ---------------------------------------- | ----------------------------------------------------------------------------- |
 * | {@link GpuUboSystem}           | This manages WebGPU uniform buffer objects feature for shaders                |
 * | {@link GpuEncoderSystem}       | This manages the WebGPU command encoder                                       |
 * | {@link GpuDeviceSystem}        | This manages the WebGPU Device and its extensions                             |
 * | {@link GpuBufferSystem}        | This manages buffers and their GPU resources, keeps everything in sync        |
 * | {@link GpuTextureSystem}       | This manages textures and their GPU resources, keeps everything in sync       |
 * | {@link GpuRenderTargetSystem}  | This manages what we render too. For example the screen, or another texture   |
 * | {@link GpuShaderSystem}        | This manages shaders, programs that run on the GPU to output lovely pixels    |
 * | {@link GpuStateSystem}         | This manages the state of the WebGPU Pipelines. eg the various flags that can be set blend modes / depthTesting etc |
 * | {@link PipelineSystem}         | This manages the WebGPU pipelines, used for rendering                         |
 * | {@link GpuColorMaskSystem}     | This manages the color mask. Used for color masking                           |
 * | {@link GpuStencilSystem}       | This manages the stencil buffer. Used primarily for masking                   |
 * | {@link BindGroupSystem}        | This manages the WebGPU bind groups. this is how data is bound to a shader when rendering |
 *
 * The breadth of the API surface provided by the renderer is contained within these systems.
 * @property {GpuUboSystem} ubo - UboSystem instance.
 * @property {GpuEncoderSystem} encoder - EncoderSystem instance.
 * @property {GpuDeviceSystem} device - DeviceSystem instance.
 * @property {GpuBufferSystem} buffer - BufferSystem instance.
 * @property {GpuTextureSystem} texture - TextureSystem instance.
 * @property {GpuRenderTargetSystem} renderTarget - RenderTargetSystem instance.
 * @property {GpuShaderSystem} shader - ShaderSystem instance.
 * @property {GpuStateSystem} state - StateSystem instance.
 * @property {PipelineSystem} pipeline - PipelineSystem instance.
 * @property {GpuColorMaskSystem} colorMask - ColorMaskSystem instance.
 * @property {GpuStencilSystem} stencil - StencilSystem instance.
 * @property {BindGroupSystem} bindGroup - BindGroupSystem instance.
 */
export declare class WebGPURenderer<T extends ICanvas = HTMLCanvasElement> extends AbstractRenderer<WebGPUPipes, WebGPUOptions, T> implements WebGPUSystems {
	/** The WebGPU Device. */
	gpu: GPU$1;
	constructor();
}
/**
 * Automatically determines the most appropriate renderer for the current environment.
 *
 * The function will prioritize the WebGL renderer as it is the most tested safe API to use.
 * In the near future as WebGPU becomes more stable and ubiquitous, it will be prioritized over WebGL.
 *
 * The selected renderer's code is then dynamically imported to optimize
 * performance and minimize the initial bundle size.
 *
 * To maximize the benefits of dynamic imports, it's recommended to use a modern bundler
 * that supports code splitting. This will place the renderer code in a separate chunk,
 * which is loaded only when needed.
 * @example
 *
 * // create a renderer
 * const renderer = await autoDetectRenderer({
 *   width: 800,
 *   height: 600,
 *   antialias: true,
 * });
 *
 * // custom for each renderer
 * const renderer = await autoDetectRenderer({
 *   width: 800,
 *   height: 600,
 *   webgpu:{
 *     antialias: true,
 *     backgroundColor: 'red'
 *   },
 *   webgl:{
 *     antialias: true,
 *     backgroundColor: 'green'
 *   }
 *  });
 * @param options - A partial configuration object based on the `AutoDetectOptions` type.
 * @returns A Promise that resolves to an instance of the selected renderer.
 */
export declare function autoDetectRenderer(options: Partial<AutoDetectOptions>): Promise<Renderer>;
/**
 * Application options supplied to the {@link Application#init} method.
 * These options configure how your PixiJS application behaves.
 * @example
 * 
 */
export interface ApplicationOptions extends AutoDetectOptions, PixiMixins.ApplicationOptions {
}
export interface Application extends PixiMixins.Application {
}
/**
 * Convenience class to create a new PixiJS application.
 *
 * The Application class is the main entry point for creating a PixiJS application. It handles the setup of all core
 * components needed to start rendering and managing your game or interactive experience.
 *
 * Key features:
 * - Automatically creates and manages the renderer
 * - Provides a stage (root container) for your display objects
 * - Handles canvas creation and management
 * - Supports plugins for extending functionality
 *   - {@link ResizePlugin} for automatic resizing
 *   - {@link TickerPlugin} for managing frame updates
 *   - {@link CullerPlugin} for culling off-screen objects
 * @example
 * 
 * > [!IMPORTANT] From PixiJS v8.0.0, the application must be initialized using the async `init()` method
 * > rather than passing options to the constructor.
 */
export declare class Application<R extends Renderer = Renderer> {
	/**
	 * The root display container for your application.
	 * All visual elements should be added to this container or its children.
	 * @example
	 * 
	 */
	stage: Container;
	/**
	 * The renderer instance that handles all drawing operations.
	 *
	 * Unless specified, it will automatically create a WebGL renderer if available.
	 * If WebGPU is available and the `preference` is set to `webgpu`, it will create a WebGPU renderer.
	 * @example
	 * 
	 */
	renderer: R;
	/** Create new Application instance */
	constructor();
	/** @deprecated since 8.0.0 */
	constructor(options?: Partial<ApplicationOptions>);
	/**
	 * Initializes the PixiJS application with the specified options.
	 *
	 * This method must be called after creating a new Application instance.
	 * @param options - Configuration options for the application and renderer
	 * @returns A promise that resolves when initialization is complete
	 * @example
	 * 
	 */
	init(options?: Partial<ApplicationOptions>): Promise<void>;
	/**
	 * Renders the current stage to the screen.
	 *
	 * When using the default setup with {@link TickerPlugin} (enabled by default), you typically don't need to call
	 * this method directly as rendering is handled automatically.
	 *
	 * Only use this method if you've disabled the {@link TickerPlugin} or need custom
	 * render timing control.
	 * @example
	 * 
	 */
	render(): void;
	/**
	 * Reference to the renderer's canvas element. This is the HTML element
	 * that displays your application's graphics.
	 * @type {HTMLCanvasElement}
	 * @example
	 * 
	 */
	get canvas(): R["canvas"];
	/**
	 * Reference to the renderer's canvas element.
	 * @type {HTMLCanvasElement}
	 * @deprecated since 8.0.0
	 */
	get view(): R["canvas"];
	/**
	 * Reference to the renderer's screen rectangle. This represents the visible area of your application.
	 *
	 * It's commonly used for:
	 * - Setting filter areas for full-screen effects
	 * - Defining hit areas for screen-wide interaction
	 * - Determining the visible bounds of your application
	 * @example
	 * 
	 */
	get screen(): Rectangle;
	/**
	 * Destroys the application and all of its resources.
	 *
	 * This method should be called when you want to completely
	 * clean up the application and free all associated memory.
	 * @param rendererDestroyOptions - Options for destroying the renderer:
	 *  - `false` or `undefined`: Preserves the canvas element (default)
	 *  - `true`: Removes the canvas element
	 *  - `{ removeView: boolean }`: Object with removeView property to control canvas removal
	 * @param options - Options for destroying the application:
	 *  - `false` or `undefined`: Basic cleanup (default)
	 *  - `true`: Complete cleanup including children
	 *  - Detailed options object:
	 *    - `children`: Remove children
	 *    - `texture`: Destroy textures
	 *    - `textureSource`: Destroy texture sources
	 *    - `context`: Destroy WebGL context
	 * @example
	 * 
	 * > [!WARNING] After calling destroy, the application instance should no longer be used.
	 * > All properties will be null and further operations will throw errors.
	 */
	destroy(rendererDestroyOptions?: RendererDestroyOptions, options?: DestroyOptions): void;
}
declare global {
	var __PIXI_APP_INIT__: undefined | ((arg: Application | Renderer, version: string) => void);
	var __PIXI_RENDERER_INIT__: undefined | ((arg: Application | Renderer, version: string) => void);
}
/**
 * The options for rendering a view.
 */
export interface RenderOptions extends ClearOptions {
	/** The container to render. */
	container: Container;
	/** the transform to apply to the container. */
	transform?: Matrix;
}
/**
 * Options for destroying the renderer.
 * This can be a boolean or an object.
 */
export type RendererDestroyOptions = TypeOrBool<ViewSystemDestroyOptions & {
	/** Whether to clean up global resource pools/caches */
	releaseGlobalResources?: boolean;
}>;
declare const defaultRunners: readonly [
	"init",
	"destroy",
	"contextChange",
	"resolutionChange",
	"resetState",
	"renderEnd",
	"renderStart",
	"render",
	"update",
	"postrender",
	"prerender"
];
type DefaultRunners = typeof defaultRunners[number];
type Runners = {
	[key in DefaultRunners]: SystemRunner;
} & {
	[K: ({} & string) | ({} & symbol)]: SystemRunner;
};
declare const DefaultWebGLSystems: (typeof BackgroundSystem | typeof GlobalUniformSystem | typeof HelloSystem | typeof ViewSystem | typeof RenderGroupSystem | typeof TextureGCSystem | typeof GenerateTextureSystem | typeof ExtractSystem | typeof RendererInitHook | typeof RenderableGCSystem | typeof SchedulerSystem | typeof GlUboSystem | typeof GlBackBufferSystem | typeof GlContextSystem | typeof GlLimitsSystem | typeof GlBufferSystem | typeof GlTextureSystem | typeof GlRenderTargetSystem | typeof GlGeometrySystem | typeof GlUniformGroupSystem | typeof GlShaderSystem | typeof GlEncoderSystem | typeof GlStateSystem | typeof GlStencilSystem | typeof GlColorMaskSystem)[];
declare const DefaultWebGLPipes: (typeof BlendModePipe | typeof BatcherPipe | typeof SpritePipe | typeof RenderGroupPipe | typeof AlphaMaskPipe | typeof StencilMaskPipe | typeof ColorMaskPipe | typeof CustomRenderPipe)[];
/**
 * The default WebGL renderer, uses WebGL2 contexts.
 */
export type WebGLSystems = ExtractSystemTypes<typeof DefaultWebGLSystems> & PixiMixins.RendererSystems & PixiMixins.WebGLSystems;
/**
 * Options for WebGLRenderer.
 */
export interface WebGLOptions extends SharedRendererOptions, ExtractRendererOptions<typeof DefaultWebGLSystems>, PixiMixins.WebGLOptions {
}
export interface WebGLRenderer<T extends ICanvas = HTMLCanvasElement> extends AbstractRenderer<WebGLPipes, WebGLOptions, T>, WebGLSystems {
}
/**
 * The WebGL PixiJS Renderer. This renderer allows you to use the most common graphics API, WebGL (and WebGL2).
 *
 * 
 *
 * You can use {@link autoDetectRenderer} to create a renderer that will automatically detect the best
 * renderer for the environment.
 *
 *
 * 
 *
 * The renderer is composed of systems that manage specific tasks. The following systems are added by default
 * whenever you create a WebGL renderer:
 *
 * | WebGL Core Systems                          | Systems that are specific to the WebGL renderer                               |
 * | ------------------------------------------- | ----------------------------------------------------------------------------- |
 * | {@link GlUboSystem}               | This manages WebGL2 uniform buffer objects feature for shaders                |
 * | {@link GlBackBufferSystem}        | manages the back buffer, used so that we can pixi can pixels from the screen  |
 * | {@link GlContextSystem}           | This manages the WebGL context and its extensions                             |
 * | {@link GlBufferSystem}            | This manages buffers and their GPU resources, keeps everything in sync        |
 * | {@link GlTextureSystem}           | This manages textures and their GPU resources, keeps everything in sync       |
 * | {@link GlRenderTargetSystem}      | This manages what we render too. For example the screen, or another texture   |
 * | {@link GlGeometrySystem}          | This manages geometry, used for drawing meshes via the GPU                    |
 * | {@link GlUniformGroupSystem}      | This manages uniform groups. Syncing shader properties with the GPU           |
 * | {@link GlShaderSystem}            | This manages shaders, programs that run on the GPU to output lovely pixels    |
 * | {@link GlEncoderSystem}           | This manages encoders, a WebGPU Paradigm, use it to draw a mesh + shader      |
 * | {@link GlStateSystem}             | This manages the state of the WebGL context. eg the various flags that can be set blend modes / depthTesting etc |
 * | {@link GlStencilSystem}           | This manages the stencil buffer. Used primarily for masking                   |
 * | {@link GlColorMaskSystem}         | This manages the color mask. Used for color masking                           |
 *
 * The breadth of the API surface provided by the renderer is contained within these systems.
 * @property {GlUboSystem} ubo - UboSystem instance.
 * @property {GlBackBufferSystem} backBuffer - BackBufferSystem instance.
 * @property {GlContextSystem} context - ContextSystem instance.
 * @property {GlBufferSystem} buffer - BufferSystem instance.
 * @property {GlTextureSystem} texture - TextureSystem instance.
 * @property {GlRenderTargetSystem} renderTarget - RenderTargetSystem instance.
 * @property {GlGeometrySystem} geometry - GeometrySystem instance.
 * @property {GlUniformGroupSystem} uniformGroup - UniformGroupSystem instance.
 * @property {GlShaderSystem} shader - ShaderSystem instance.
 * @property {GlEncoderSystem} encoder - EncoderSystem instance.
 * @property {GlStateSystem} state - StateSystem instance.
 * @property {GlStencilSystem} stencil - StencilSystem instance.
 * @property {GlColorMaskSystem} colorMask - ColorMaskSystem instance.
 */
export declare class WebGLRenderer<T extends ICanvas = HTMLCanvasElement> extends AbstractRenderer<WebGLPipes, WebGLOptions, T> implements WebGLSystems {
	gl: GlRenderingContext;
	constructor();
}
/**
 * A generic renderer that can be either a WebGL or WebGPU renderer.
 */
export type Renderer<T extends ICanvas = HTMLCanvasElement> = WebGLRenderer<T> | WebGPURenderer<T>;
/**
 * Options for the renderer.
 */
export interface RendererOptions extends WebGLOptions, WebGPUOptions {
}
export interface ViewContainer<GPU_DATA extends GPUData = any> extends PixiMixins.ViewContainer, Container {
	_gpuData: Record<number, GPU_DATA>;
}
/**
 * Options for configuring a RenderLayer. A RenderLayer allows control over rendering order
 * independent of the scene graph hierarchy.
 * @example
 * 
 */
export interface RenderLayerOptions {
	/**
	 * If true, the layer's children will be sorted by zIndex before rendering.
	 * If false, you can manually sort the children using sortRenderLayerChildren when needed.
	 * @default false
	 * @example
	 * 
	 */
	sortableChildren?: boolean;
	/**
	 * Custom sort function to sort layer children. Default sorts by zIndex.
	 * @param a - First container to compare
	 * @param b - Second container to compare
	 * @returns Negative if a should render before b, positive if b should render before a
	 * @example
	 * 
	 * @default (a, b) => a.zIndex - b.zIndex
	 */
	sortFunction?: (a: Container, b: Container) => number;
}
/**
 * The RenderLayer API provides a way to control the rendering order of objects independently
 * of their logical parent-child relationships in the scene graph.
 * This allows developers to decouple how objects are transformed
 * (via their logical parent) from how they are rendered on the screen.
 *
 * ### Key Concepts
 *
 * #### RenderLayers Control Rendering Order:
 * - RenderLayers define where in the render stack objects are drawn,
 * but they do not affect an object's transformations (e.g., position, scale, rotation) or logical hierarchy.
 * - RenderLayers can be added anywhere in the scene graph.
 *
 * #### Logical Parenting Remains Unchanged:
 * - Objects still have a logical parent for transformations via addChild.
 * - Assigning an object to a layer does not reparent it.
 *
 * #### Explicit Control:
 * - Developers assign objects to layers using renderLayer.add and remove them using renderLayer.remove.
 * ---
 * ### API Details
 *
 * #### 1. Creating a RenderLayer
 * A RenderLayer is a lightweight object responsible for controlling render order.
 * It has no children or transformations of its own
 * but can be inserted anywhere in the scene graph to define its render position.
 * 
 *
 * #### 2. Adding Objects to a Layer
 * Use renderLayer.add to assign an object to a layer.
 * This overrides the object's default render order defined by its logical parent.
 * 
 *
 * #### 3. Removing Objects from a Layer
 * To stop an object from being rendered in the layer, use remove.
 * 
 * When an object is removed from its logical parent (removeChild), it is automatically removed from the layer.
 *
 * #### 4. Re-Adding Objects to Layers
 * If an object is re-added to a logical parent, it does not automatically reassign itself to the layer.
 * Developers must explicitly reassign it.
 * 
 *
 * #### 5. Layer Position in Scene Graph
 * A layer's position in the scene graph determines its render priority relative to other layers and objects.
 * Layers can be inserted anywhere in the scene graph.
 * 
 * This is a new API and therefore considered experimental at this stage.
 * While the core is pretty robust, there are still a few tricky issues we need to tackle.
 * However, even with the known issues below, we believe this API is incredibly useful!
 *
 * Known issues:
 *  - Interaction may not work as expected since hit testing does not account for the visual render order created by layers.
 *    For example, if an object is visually moved to the front via a layer, hit testing will still use its original position.
 *  - RenderLayers and their children must all belong to the same renderGroup to work correctly
 */
export declare class RenderLayer extends Container {
	/**
	 * Default options for RenderLayer instances. These options control the sorting behavior
	 * of objects within the render layer.
	 * @example
	 * 
	 * @property {boolean} sortableChildren -
	 * @property {Function} sortFunction -
	 */
	static defaultOptions: RenderLayerOptions;
	/** Function used to sort layer children if sortableChildren is true */
	sortFunction: (a: Container, b: Container) => number;
	/**
	 * The list of objects that this layer is responsible for rendering. Objects in this list maintain
	 * their original parent in the scene graph but are rendered as part of this layer.
	 * @example
	 * 
	 */
	renderLayerChildren: Container[];
	/**
	 * Creates a new RenderLayer instance
	 * @param options - Configuration options for the RenderLayer
	 * @param {boolean} [options.sortableChildren=false] - If true, layer children will be automatically sorted each render
	 * @param {Function} [options.sortFunction] - Custom function to sort layer children. Default sorts by zIndex
	 */
	constructor(options?: RenderLayerOptions);
	/**
	 * Adds one or more Containers to this render layer. The Containers will be rendered as part of this layer
	 * while maintaining their original parent in the scene graph.
	 *
	 * If the Container already belongs to a layer, it will be removed from the old layer before being added to this one.
	 * @example
	 * 
	 * @param children - The Container(s) to add to this layer. Can be any Container or array of Containers.
	 * @returns The first child that was added, for method chaining
	 */
	attach<U extends Container[]>(...children: U): U[0];
	/**
	 * Removes one or more Containers from this render layer. The Containers will maintain their
	 * original parent in the scene graph but will no longer be rendered as part of this layer.
	 * @example
	 * 
	 * @param children - The Container(s) to remove from this layer
	 * @returns The first child that was removed, for method chaining
	 */
	detach<U extends Container[]>(...children: U): U[0];
	/**
	 * Removes all objects from this render layer. Objects will maintain their
	 * original parent in the scene graph but will no longer be rendered as part of this layer.
	 * @example
	 * 
	 * @returns The RenderLayer instance for method chaining
	 */
	detachAll(): void;
	/**
	 * Sort the layer's children using the defined sort function. This method allows manual sorting
	 * of layer children and is automatically called during rendering if sortableChildren is true.
	 * @example
	 * 
	 * @returns The RenderLayer instance for method chaining
	 */
	sortRenderLayerChildren(): void;
}
/**
 * The type of child that can be added to a {@link Container}.
 * This is a generic type that extends the {@link Container} class.
 */
export type ContainerChild = Container;
/**
 * Events that can be emitted by a Container. These events provide lifecycle hooks and notifications
 * for container state changes.
 * @example
 * 
 */
export interface ContainerEvents<C extends ContainerChild> extends PixiMixins.ContainerEvents {
	/**
	 * Emitted when this container is added to a new container.
	 * Useful for setting up parent-specific behaviors.
	 * @param container - The parent container this was added to
	 * @example
	 * 
	 */
	added: [
		container: Container
	];
	/**
	 * Emitted when a child is added to this container.
	 * Useful for tracking container composition changes.
	 * @param child - The child that was added
	 * @param container - The container the child was added to (this container)
	 * @param index - The index at which the child was added
	 * @example
	 * 
	 */
	childAdded: [
		child: C,
		container: Container,
		index: number
	];
	/**
	 * Emitted when this container is removed from its parent.
	 * Useful for cleanup and state management.
	 * @param container - The parent container this was removed from
	 * @example
	 * 
	 */
	removed: [
		container: Container
	];
	/**
	 * Emitted when a child is removed from this container.
	 * Useful for cleanup and maintaining container state.
	 * @param child - The child that was removed
	 * @param container - The container the child was removed from (this container)
	 * @param index - The index from which the child was removed
	 * @example
	 * 
	 */
	childRemoved: [
		child: C,
		container: Container,
		index: number
	];
	/**
	 * Emitted when the container is destroyed.
	 * Useful for final cleanup and resource management.
	 * @param container - The container that was destroyed
	 * @example
	 * 
	 */
	destroyed: [
		container: Container
	];
}
type AnyEvent = {
	[K: ({} & string) | ({} & symbol)]: any;
};
/**
 * Options for updating the transform of a container.
 */
export interface UpdateTransformOptions {
	x: number;
	y: number;
	scaleX: number;
	scaleY: number;
	rotation: number;
	skewX: number;
	skewY: number;
	pivotX: number;
	pivotY: number;
	originX: number;
	originY: number;
}
/**
 * Constructor options used for `Container` instances.
 * 
 */
export interface ContainerOptions<C extends ContainerChild = ContainerChild> extends PixiMixins.ContainerOptions {
	/** @see Container#isRenderGroup */
	isRenderGroup?: boolean;
	/**
	 * The blend mode to be applied to the sprite. Controls how pixels are blended when rendering.
	 *
	 * Setting to 'normal' will reset to default blending.
	 * > [!NOTE] More blend modes are available after importing the `pixi.js/advanced-blend-modes` sub-export.
	 * @example
	 * 
	 * @default 'normal'
	 */
	blendMode?: BLEND_MODES;
	/**
	 * The tint applied to the sprite.
	 *
	 * This can be any valid {@link ColorSource}.
	 * @example
	 * 
	 * @default 0xFFFFFF
	 */
	tint?: ColorSource;
	/**
	 * The opacity of the object relative to its parent's opacity.
	 * Value ranges from 0 (fully transparent) to 1 (fully opaque).
	 * @example
	 * 
	 * @default 1
	 */
	alpha?: number;
	/**
	 * The angle of the object in degrees.
	 *
	 * > [!NOTE] 'rotation' and 'angle' have the same effect on a display object;
	 * > rotation is in radians, angle is in degrees.
	 * @example
	 * 
	 */
	angle?: number;
	/**
	 * The array of children of this container. Each child must be a Container or extend from it.
	 *
	 * The array is read-only, but its contents can be modified using Container methods.
	 * @example
	 * 
	 */
	children?: C[];
	/**
	 * The display object container that contains this display object.
	 * This represents the parent-child relationship in the display tree.
	 */
	parent?: Container;
	/**
	 * Controls whether this object can be rendered. If false the object will not be drawn,
	 * but the transform will still be updated. This is different from visible, which skips
	 * transform updates.
	 * @example
	 * 
	 * @default true
	 */
	renderable?: boolean;
	/**
	 * The rotation of the object in radians.
	 *
	 * > [!NOTE] 'rotation' and 'angle' have the same effect on a display object;
	 * > rotation is in radians, angle is in degrees.
	 * @example
	 * 
	 */
	rotation?: number;
	/**
	 * The scale factors of this object along the local coordinate axes.
	 *
	 * The default scale is (1, 1).
	 * @example
	 * 
	 */
	scale?: PointData | number;
	/**
	 * The center of rotation, scaling, and skewing for this display object in its local space.
	 * The `position` is the projection of `pivot` in the parent's local space.
	 *
	 * By default, the pivot is the origin (0, 0).
	 * @example
	 * 
	 */
	pivot?: PointData | number;
	/**
	 * The origin point around which the container rotates and scales.
	 * Unlike pivot, changing origin will not move the container's position.
	 * @example
	 * 
	 */
	origin?: PointData | number;
	/**
	 * The coordinate of the object relative to the local coordinates of the parent.
	 * @example
	 * 
	 */
	position?: PointData;
	/**
	 * The skew factor for the object in radians. Skewing is a transformation that distorts
	 * the object by rotating it differently at each point, creating a non-uniform shape.
	 * @example
	 * 
	 * @default { x: 0, y: 0 }
	 */
	skew?: PointData;
	/**
	 * The visibility of the object. If false the object will not be drawn,
	 * and the transform will not be updated.
	 * @example
	 * 
	 * @default true
	 */
	visible?: boolean;
	/**
	 * The position of the container on the x axis relative to the local coordinates of the parent.
	 *
	 * An alias to position.x
	 * @example
	 * 
	 */
	x?: number;
	/**
	 * The position of the container on the y axis relative to the local coordinates of the parent.
	 *
	 * An alias to position.y
	 * @example
	 * 
	 */
	y?: number;
	/**
	 * An optional bounds area for this container. Setting this rectangle will stop the renderer
	 * from recursively measuring the bounds of each children and instead use this single boundArea.
	 *
	 * > [!IMPORTANT] This is great for optimisation! If for example you have a
	 * > 1000 spinning particles and you know they all sit within a specific bounds,
	 * > then setting it will mean the renderer will not need to measure the
	 * > 1000 children to find the bounds. Instead it will just use the bounds you set.
	 * @example
	 * 
	 */
	boundsArea?: Rectangle;
}
export interface Container<C extends ContainerChild> extends PixiMixins.Container<C>, EventEmitter<ContainerEvents<C> & AnyEvent> {
}
/**
 * Container is a general-purpose display object that holds children. It also adds built-in support for advanced
 * rendering features like masking and filtering.
 *
 * It is the base class of all display objects that act as a container for other objects, including Graphics
 * and Sprite.
 *
 * <details id="transforms">
 *
 * <summary>Transforms</summary>
 *
 * The [transform]{@link Container#localTransform} of a display object describes the projection from its
 * local coordinate space to its parent's local coordinate space. The following properties are derived
 * from the transform:
 *
 * <table>
 *   <thead>
 *     <tr>
 *       <th>Property</th>
 *       <th>Description</th>
 *     </tr>
 *   </thead>
 *   <tbody>
 *     <tr>
 *       <td>[pivot]{@link Container#pivot}</td>
 *       <td>
 *         Invariant under rotation, scaling, and skewing. The projection of into the parent's space of the pivot
 *         is equal to position, regardless of the other three transformations. In other words, It is the center of
 *         rotation, scaling, and skewing.
 *       </td>
 *     </tr>
 *     <tr>
 *       <td>[position]{@link Container#position}</td>
 *       <td>
 *         Translation. This is the position of the [pivot]{@link Container#pivot} in the parent's local
 *         space. The default value of the pivot is the origin (0,0). If the top-left corner of your display object
 *         is (0,0) in its local space, then the position will be its top-left corner in the parent's local space.
 *       </td>
 *     </tr>
 *     <tr>
 *       <td>[scale]{@link Container#scale}</td>
 *       <td>
 *         Scaling. This will stretch (or compress) the display object's projection. The scale factors are along the
 *         local coordinate axes. In other words, the display object is scaled before rotated or skewed. The center
 *         of scaling is the [pivot]{@link Container#pivot}.
 *       </td>
 *     </tr>
 *     <tr>
 *       <td>[rotation]{@link Container#rotation}</td>
 *       <td>
 *          Rotation. This will rotate the display object's projection by this angle (in radians).
 *       </td>
 *     </tr>
 *     <tr>
 *       <td>[skew]{@link Container#skew}</td>
 *       <td>
 *         <p>Skewing. This can be used to deform a rectangular display object into a parallelogram.</p>
 *         <p>
 *         In PixiJS, skew has a slightly different behaviour than the conventional meaning. It can be
 *         thought of the net rotation applied to the coordinate axes (separately). For example, if "skew.x" is
 *         ⍺ and "skew.y" is β, then the line x = 0 will be rotated by ⍺ (y = -x*cot⍺) and the line y = 0 will be
 *         rotated by β (y = x*tanβ). A line y = x*tanϴ (i.e. a line at angle ϴ to the x-axis in local-space) will
 *         be rotated by an angle between ⍺ and β.
 *         </p>
 *         <p>
 *         It can be observed that if skew is applied equally to both axes, then it will be equivalent to applying
 *         a rotation. Indeed, if "skew.x" = -ϴ and "skew.y" = ϴ, it will produce an equivalent of "rotation" = ϴ.
 *         </p>
 *         <p>
 *         Another quite interesting observation is that "skew.x", "skew.y", rotation are commutative operations. Indeed,
 *         because rotation is essentially a careful combination of the two.
 *         </p>
 *       </td>
 *     </tr>
 *     <tr>
 *       <td>[angle]{@link Container#angle}</td>
 *       <td>Rotation. This is an alias for [rotation]{@link Container#rotation}, but in degrees.</td>
 *     </tr>
 *     <tr>
 *       <td>[x]{@link Container#x}</td>
 *       <td>Translation. This is an alias for position.x!</td>
 *     </tr>
 *     <tr>
 *       <td>[y]{@link Container#y}</td>
 *       <td>Translation. This is an alias for position.y!</td>
 *     </tr>
 *     <tr>
 *       <td>[width]{@link Container#width}</td>
 *       <td>
 *         Implemented in [Container]{@link Container}. Scaling. The width property calculates scale.x by dividing
 *         the "requested" width by the local bounding box width. It is indirectly an abstraction over scale.x, and there
 *         is no concept of user-defined width.
 *       </td>
 *     </tr>
 *     <tr>
 *       <td>[height]{@link Container#height}</td>
 *       <td>
 *         Implemented in [Container]{@link Container}. Scaling. The height property calculates scale.y by dividing
 *         the "requested" height by the local bounding box height. It is indirectly an abstraction over scale.y, and there
 *         is no concept of user-defined height.
 *       </td>
 *     </tr>
 *   </tbody>
 * </table>
 * </details>
 *
 * <details id="alpha">
 * <summary>Alpha</summary>
 *
 * This alpha sets a display object's **relative opacity** w.r.t its parent. For example, if the alpha of a display
 * object is 0.5 and its parent's alpha is 0.5, then it will be rendered with 25% opacity (assuming alpha is not
 * applied on any ancestor further up the chain).
 * </details>
 *
 * <details id="visible">
 * <summary>Renderable vs Visible</summary>
 *
 * The `renderable` and `visible` properties can be used to prevent a display object from being rendered to the
 * screen. However, there is a subtle difference between the two. When using `renderable`, the transforms  of the display
 * object (and its children subtree) will continue to be calculated. When using `visible`, the transforms will not
 * be calculated.
 * 
 *
 * </details>
 *
 * <details id="renderGroup">
 * <summary>RenderGroup</summary>
 *
 * In PixiJS v8, containers can be set to operate in 'render group mode',
 * transforming them into entities akin to a stage in traditional rendering paradigms.
 * A render group is a root renderable entity, similar to a container,
 * but it's rendered in a separate pass with its own unique set of rendering instructions.
 * This approach enhances rendering efficiency and organization, particularly in complex scenes.
 *
 * You can enable render group mode on any container using container.enableRenderGroup()
 * or by initializing a new container with the render group property set to true (new Container({isRenderGroup: true})).
 *  The method you choose depends on your specific use case and setup requirements.
 *
 * An important aspect of PixiJS’s rendering process is the automatic treatment of rendered scenes as render groups.
 * This conversion streamlines the rendering process, but understanding when and how this happens is crucial
 * to fully leverage its benefits.
 *
 * One of the key advantages of using render groups is the performance efficiency in moving them. Since transformations
 *  are applied at the GPU level, moving a render group, even one with complex and numerous children,
 * doesn't require recalculating the rendering instructions or performing transformations on each child.
 * This makes operations like panning a large game world incredibly efficient.
 *
 * However, it's crucial to note that render groups do not batch together.
 * This means that turning every container into a render group could actually slow things down,
 * as each render group is processed separately. It's best to use render groups judiciously, at a broader level,
 * rather than on a per-child basis.
 * This approach ensures you get the performance benefits without overburdening the rendering process.
 *
 * RenderGroups maintain their own set of rendering instructions,
 * ensuring that changes or updates within a render group don't affect the rendering
 * instructions of its parent or other render groups.
 *  This isolation ensures more stable and predictable rendering behavior.
 *
 * Additionally, renderGroups can be nested, allowing for powerful options in organizing different aspects of your scene.
 * This feature is particularly beneficial for separating complex game graphics from UI elements,
 * enabling intricate and efficient scene management in complex applications.
 *
 * This means that Containers have 3 levels of matrix to be mindful of:
 *
 * 1. localTransform, this is the transform of the container based on its own properties
 * 2. groupTransform, this it the transform of the container relative to the renderGroup it belongs too
 * 3. worldTransform, this is the transform of the container relative to the Scene being rendered
 * </details>
 */
export declare class Container<C extends ContainerChild = ContainerChild> extends EventEmitter<ContainerEvents<C> & AnyEvent> {
	/**
	 * Mixes all enumerable properties and methods from a source object to Container.
	 * @param source - The source of properties and methods to mix in.
	 * @deprecated since 8.8.0
	 */
	static mixin(source: Dict<any>): void;
	/**
	 * The array of children of this container. Each child must be a Container or extend from it.
	 *
	 * The array is read-only, but its contents can be modified using Container methods.
	 * @example
	 * 
	 */
	children: C[];
	/**
	 * The display object container that contains this display object.
	 * This represents the parent-child relationship in the display tree.
	 * @example
	 * 
	 */
	parent: Container | null;
	/**
	 * Current transform of the object based on local factors: position, scale, other stuff.
	 * This matrix represents the local transformation without any parent influence.
	 * @example
	 * 
	 */
	localTransform: Matrix;
	/**
	 * Whether this object has been destroyed. If true, the object should no longer be used.
	 * After an object is destroyed, all of its functionality is disabled and references are removed.
	 * @example
	 * 
	 * @default false
	 */
	destroyed: boolean;
	/**
	 * An optional bounds area for this container. Setting this rectangle will stop the renderer
	 * from recursively measuring the bounds of each children and instead use this single boundArea.
	 *
	 * > [!IMPORTANT] This is great for optimisation! If for example you have a
	 * > 1000 spinning particles and you know they all sit within a specific bounds,
	 * > then setting it will mean the renderer will not need to measure the
	 * > 1000 children to find the bounds. Instead it will just use the bounds you set.
	 * @example
	 * 
	 */
	boundsArea: Rectangle;
	constructor(options?: ContainerOptions<C>);
	/**
	 * Adds one or more children to the container.
	 * The children will be rendered as part of this container's display list.
	 * @example
	 * 
	 * @param children - The Container(s) to add to the container
	 * @returns The first child that was added
	 */
	addChild<U extends C[]>(...children: U): U[0];
	/**
	 * Removes one or more children from the container.
	 * When removing multiple children, events will be triggered for each child in sequence.
	 * @example
	 * 
	 * @param children - The Container(s) to remove
	 * @returns The first child that was removed
	 */
	removeChild<U extends C[]>(...children: U): U[0];
	set isRenderGroup(value: boolean);
	/**
	 * Current transform of the object based on world (parent) factors.
	 *
	 * This matrix represents the absolute transformation in the scene graph.
	 * @example
	 * 
	 */
	get worldTransform(): Matrix;
	/**
	 * The position of the container on the x axis relative to the local coordinates of the parent.
	 *
	 * An alias to position.x
	 * @example
	 * 
	 */
	get x(): number;
	set x(value: number);
	/**
	 * The position of the container on the y axis relative to the local coordinates of the parent.
	 *
	 * An alias to position.y
	 * @example
	 * 
	 */
	get y(): number;
	set y(value: number);
	/**
	 * The coordinate of the object relative to the local coordinates of the parent.
	 * @example
	 * 
	 * @since 4.0.0
	 */
	get position(): ObservablePoint;
	set position(value: PointData);
	/**
	 * The rotation of the object in radians.
	 *
	 * > [!NOTE] 'rotation' and 'angle' have the same effect on a display object;
	 * > rotation is in radians, angle is in degrees.
	 * @example
	 * 
	 */
	get rotation(): number;
	set rotation(value: number);
	/**
	 * The angle of the object in degrees.
	 *
	 * > [!NOTE] 'rotation' and 'angle' have the same effect on a display object;
	 * > rotation is in radians, angle is in degrees.
	 * @example
	 * 
	 */
	get angle(): number;
	set angle(value: number);
	/**
	 * The center of rotation, scaling, and skewing for this display object in its local space.
	 * The `position` is the projection of `pivot` in the parent's local space.
	 *
	 * By default, the pivot is the origin (0, 0).
	 * @example
	 * 
	 * @since 4.0.0
	 */
	get pivot(): ObservablePoint;
	set pivot(value: PointData | number);
	/**
	 * The skew factor for the object in radians. Skewing is a transformation that distorts
	 * the object by rotating it differently at each point, creating a non-uniform shape.
	 * @example
	 * 
	 * @since 4.0.0
	 * @type {ObservablePoint} Point-like object with x/y properties in radians
	 * @default {x: 0, y: 0}
	 */
	get skew(): ObservablePoint;
	set skew(value: PointData);
	/**
	 * The scale factors of this object along the local coordinate axes.
	 *
	 * The default scale is (1, 1).
	 * @example
	 * 
	 * @since 4.0.0
	 */
	get scale(): ObservablePoint;
	set scale(value: PointData | number | string);
	/**
	 * @experimental
	 * The origin point around which the container rotates and scales without affecting its position.
	 * Unlike pivot, changing the origin will not move the container's position.
	 * @example
	 * 
	 */
	get origin(): ObservablePoint;
	set origin(value: PointData | number);
	/**
	 * The width of the Container, setting this will actually modify the scale to achieve the value set.
	 * > [!NOTE] Changing the width will adjust the scale.x property of the container while maintaining its aspect ratio.
	 * > [!NOTE] If you want to set both width and height at the same time, use {@link Container#setSize}
	 * as it is more optimized by not recalculating the local bounds twice.
	 * @example
	 * 
	 */
	get width(): number;
	set width(value: number);
	/**
	 * The height of the Container,
	 * > [!NOTE] Changing the height will adjust the scale.y property of the container while maintaining its aspect ratio.
	 * > [!NOTE] If you want to set both width and height at the same time, use {@link Container#setSize}
	 * as it is more optimized by not recalculating the local bounds twice.
	 * @example
	 * 
	 */
	get height(): number;
	set height(value: number);
	/**
	 * Retrieves the size of the container as a [Size]{@link Size} object.
	 *
	 * This is faster than get the width and height separately.
	 * @example
	 * 
	 * @param out - Optional object to store the size in.
	 * @returns The size of the container.
	 */
	getSize(out?: Size): Size;
	/**
	 * Sets the size of the container to the specified width and height.
	 * This is more efficient than setting width and height separately as it only recalculates bounds once.
	 * @example
	 * 
	 * @param value - This can be either a number or a [Size]{@link Size} object.
	 * @param height - The height to set. Defaults to the value of `width` if not provided.
	 */
	setSize(value: number | Optional<Size, "height">, height?: number): void;
	/**
	 * Updates the transform properties of the container.
	 * Allows partial updates of transform properties for optimized manipulation.
	 * @example
	 * 
	 * @param opts - Transform options to update
	 * @param opts.x - The x position
	 * @param opts.y - The y position
	 * @param opts.scaleX - The x-axis scale factor
	 * @param opts.scaleY - The y-axis scale factor
	 * @param opts.rotation - The rotation in radians
	 * @param opts.skewX - The x-axis skew factor
	 * @param opts.skewY - The y-axis skew factor
	 * @param opts.pivotX - The x-axis pivot point
	 * @param opts.pivotY - The y-axis pivot point
	 * @returns This container, for chaining
	 */
	updateTransform(opts: Partial<UpdateTransformOptions>): this;
	/**
	 * Updates the local transform properties by decomposing the given matrix.
	 * Extracts position, scale, rotation, and skew from a transformation matrix.
	 * @example
	 * 
	 * @param matrix - The matrix to use for updating the transform
	 */
	setFromMatrix(matrix: Matrix): void;
	/** Updates the local transform. */
	updateLocalTransform(): void;
	set alpha(value: number);
	/**
	 * The opacity of the object relative to its parent's opacity.
	 * Value ranges from 0 (fully transparent) to 1 (fully opaque).
	 * @example
	 * 
	 * @default 1
	 */
	get alpha(): number;
	set tint(value: ColorSource);
	/**
	 * The tint applied to the sprite.
	 *
	 * This can be any valid {@link ColorSource}.
	 * @example
	 * 
	 * @default 0xFFFFFF
	 */
	get tint(): number;
	set blendMode(value: BLEND_MODES);
	/**
	 * The blend mode to be applied to the sprite. Controls how pixels are blended when rendering.
	 *
	 * Setting to 'normal' will reset to default blending.
	 * > [!NOTE] More blend modes are available after importing the `pixi.js/advanced-blend-modes` sub-export.
	 * @example
	 * 
	 * @default 'normal'
	 */
	get blendMode(): BLEND_MODES;
	/**
	 * The visibility of the object. If false the object will not be drawn,
	 * and the transform will not be updated.
	 * @example
	 * 
	 * @default true
	 */
	get visible(): boolean;
	set visible(value: boolean);
	/**
	 * Controls whether this object can be rendered. If false the object will not be drawn,
	 * but the transform will still be updated. This is different from visible, which skips
	 * transform updates.
	 * @example
	 * 
	 * @default true
	 */
	get renderable(): boolean;
	set renderable(value: boolean);
	/**
	 * Removes all internal references and listeners as well as removes children from the display list.
	 * Do not use a Container after calling `destroy`.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * 
	 */
	destroy(options?: DestroyOptions): void;
}
/**
 * The type of the pointer event to listen for.
 */
export type PointerEvents = "auto" | "none" | "visiblePainted" | "visibleFill" | "visibleStroke" | "visible" | "painted" | "fill" | "stroke" | "all" | "inherit";
/**
 * When `accessible` is enabled on any display object, these properties will affect its accessibility.
 * @example
 * const container = new Container();
 * container.accessible = true;
 * container.accessibleTitle = 'My Container';
 * container.accessibleHint = 'This is a container';
 * container.tabIndex = 0;
 */
export interface AccessibleOptions {
	/**
	 * Flag for if the object is accessible. If true AccessibilityManager will overlay a
	 * shadow div with attributes set
	 * @default false
	 * @example
	 * 
	 */
	accessible: boolean;
	/**
	 * Sets the title attribute of the shadow div
	 * If accessibleTitle AND accessibleHint has not been this will default to 'container [tabIndex]'
	 * @type {string}
	 * @default null
	 * @example
	 * 
	 */
	accessibleTitle: string | null;
	/**
	 * Sets the tabIndex of the shadow div. You can use this to set the order of the
	 * elements when using the tab key to navigate.
	 * @default 0
	 * @example
	 * 
	 */
	tabIndex: number;
	/**
	 * Sets the text content of the shadow
	 * @default null
	 * @example
	 * 
	 */
	accessibleText: string | null;
	/**
	 * Setting to false will prevent any children inside this container to
	 * be accessible. Defaults to true.
	 * @default true
	 * @example
	 * 
	 */
	accessibleChildren: boolean;
}
/**
 * The result of the mobile device detection system.
 * Provides detailed information about device type and platform.
 * @example
 * 
 */
export type isMobileResult = {
	/**
	 * Apple device detection information.
	 * Provides detailed iOS device categorization.
	 * @example
	 * 
	 */
	apple: {
		/** Whether the device is an iPhone */
		phone: boolean;
		/** Whether the device is an iPod Touch */
		ipod: boolean;
		/** Whether the device is an iPad */
		tablet: boolean;
		/** Whether app is running in iOS universal mode */
		universal: boolean;
		/** Whether device is any Apple mobile device */
		device: boolean;
	};
	/**
	 * Amazon device detection information.
	 * Identifies Amazon Fire tablets and phones.
	 * @example
	 * 
	 */
	amazon: {
		/** Whether device is a Fire Phone */
		phone: boolean;
		/** Whether device is a Fire Tablet */
		tablet: boolean;
		/** Whether device is any Amazon mobile device */
		device: boolean;
	};
	/**
	 * Android device detection information.
	 * Categorizes Android phones and tablets.
	 * @example
	 * 
	 */
	android: {
		/** Whether device is an Android phone */
		phone: boolean;
		/** Whether device is an Android tablet */
		tablet: boolean;
		/** Whether device is any Android device */
		device: boolean;
	};
	/**
	 * Windows device detection information.
	 * Identifies Windows phones and tablets.
	 * @example
	 * 
	 */
	windows: {
		/** Whether device is a Windows Phone */
		phone: boolean;
		/** Whether device is a Windows tablet */
		tablet: boolean;
		/** Whether device is any Windows mobile device */
		device: boolean;
	};
	/**
	 * Other device detection information.
	 * Covers additional platforms and browsers.
	 * @example
	 * 
	 */
	other: {
		/** Whether device is a BlackBerry */
		blackberry: boolean;
		/** Whether device is a BlackBerry 10 */
		blackberry10: boolean;
		/** Whether browser is Opera Mobile */
		opera: boolean;
		/** Whether browser is Firefox Mobile */
		firefox: boolean;
		/** Whether browser is Chrome Mobile */
		chrome: boolean;
		/** Whether device is any other mobile device */
		device: boolean;
	};
	/**
	 * Whether the device is any type of phone.
	 * Combines detection across all platforms.
	 * @example
	 * 
	 */
	phone: boolean;
	/**
	 * Whether the device is any type of tablet.
	 * Combines detection across all platforms.
	 * @example
	 * 
	 */
	tablet: boolean;
	/**
	 * Whether the device is any type of mobile device.
	 * True if any mobile platform is detected.
	 * @example
	 * 
	 */
	any: boolean;
};
/**
 * Detects whether the device is mobile and what type of mobile device it is.
 * Provides a comprehensive detection system for mobile platforms and devices.
 * @example
 * 
 * @remarks
 * - Detects all major mobile platforms
 * - Distinguishes between phones and tablets
 * - Updates when navigator changes
 * - Common in responsive design
 */
export declare const isMobile: isMobileResult;
/**
 * The Accessibility system provides screen reader and keyboard navigation support for PixiJS content.
 * It creates an accessible DOM layer over the canvas that can be controlled programmatically or through user interaction.
 *
 * By default, the system activates when users press the tab key. This behavior can be customized through options:
 * 
 *
 * The system can also be controlled programmatically by accessing the `renderer.accessibility` property:
 * 
 *
 * To make individual containers accessible:
 * 
 * There are several properties that can be set on a Container to control its accessibility which can
 * be found here: {@link AccessibleOptions}.
 */
export declare class AccessibilitySystem implements System<AccessibilitySystemOptions> {
	/**
	 * The default options used by the system.
	 * You can set these before initializing the {@link Application} to change the default behavior.
	 * @example
	 * 
	 */
	static defaultOptions: AccessibilityOptions;
	/** Whether accessibility divs are visible for debugging */
	debug: boolean;
	/**
	 * @param {WebGLRenderer|WebGPURenderer} renderer - A reference to the current renderer
	 */
	constructor(renderer: Renderer, _mobileInfo?: isMobileResult);
	/**
	 * Value of `true` if accessibility is currently active and accessibility layers are showing.
	 * @type {boolean}
	 */
	get isActive(): boolean;
	/**
	 * Value of `true` if accessibility is enabled for touch devices.
	 * @type {boolean}
	 */
	get isMobileAccessibility(): boolean;
	/**
	 * Button element for handling touch hooks.
	 */
	get hookDiv(): HTMLElement;
	/**
	 * The DOM element that will sit over the PixiJS element. This is where the div overlays will go.
	 */
	get div(): HTMLElement;
	/**
	 * Destroys the accessibility system. Removes all elements and listeners.
	 * > [!IMPORTANT] This is typically called automatically when the {@link Application} is destroyed.
	 * > A typically user should not need to call this method directly.
	 */
	destroy(): void;
	/**
	 * Enables or disables the accessibility system.
	 * @param enabled - Whether to enable or disable accessibility.
	 * @example
	 * 
	 */
	setAccessibilityEnabled(enabled: boolean): void;
}
declare global {
	namespace PixiMixins {
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface Container extends Partial<AccessibleTarget> {
		}
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface ContainerOptions extends Partial<AccessibleOptions> {
		}
		interface RendererSystems {
			accessibility: AccessibilitySystem;
		}
	}
}
/**
 * A callback which can be added to a ticker.
 * The callback receives the Ticker instance as its parameter, providing access to timing properties.
 * @example
 * 
 */
export type TickerCallback<T> = (this: T, ticker: Ticker) => any;
/**
 * A Ticker class that runs an update loop that other objects listen to.
 * Used for managing animation frames and timing in a PixiJS application.
 *
 * It provides a way to add listeners that will be called on each frame,
 * allowing for smooth animations and updates.
 *
 * ## Time Units
 * - `deltaTime`: Dimensionless scalar (typically ~1.0 at 60 FPS) for frame-independent animations
 * - `deltaMS`: Milliseconds elapsed (capped and speed-scaled) for time-based calculations
 * - `elapsedMS`: Raw milliseconds elapsed (uncapped, unscaled) for measurements
 * - `lastTime`: Timestamp in milliseconds since epoch (performance.now() format)
 *
 * Animation frames are requested
 * only when necessary, e.g., when the ticker is started and the emitter has listeners.
 * @example
 * 
 */
export declare class Ticker {
	/**
	 * Target frame rate in frames per millisecond.
	 * Used for converting deltaTime to a scalar time delta.
	 * @example
	 * 
	 * @remarks
	 * - Default is 0.06 (equivalent to 60 FPS)
	 * - Used in deltaTime calculations
	 * - Affects all ticker instances
	 * @default 0.06
	 */
	static targetFPMS: number;
	/**
	 * Whether or not this ticker should invoke the method {@link Ticker#start|start}
	 * automatically when a listener is added.
	 * @example
	 * 
	 * @default false
	 */
	autoStart: boolean;
	/**
	 * Scalar representing the delta time factor.
	 * This is a dimensionless value representing the fraction of a frame at the target framerate.
	 * At 60 FPS, this value is typically around 1.0.
	 *
	 * This is NOT in milliseconds - it's a scalar multiplier for frame-independent animations.
	 * For actual milliseconds, use {@link Ticker#deltaMS}.
	 * @member {number}
	 * @example
	 * 
	 */
	deltaTime: number;
	/**
	 * Scalar time elapsed in milliseconds from last frame to this frame.
	 * Provides precise timing for animations and updates.
	 *
	 * This value is capped by setting {@link Ticker#minFPS|minFPS}
	 * and is scaled with {@link Ticker#speed|speed}.
	 *
	 * If the platform supports DOMHighResTimeStamp,
	 * this value will have a precision of 1 µs.
	 *
	 * Defaults to target frame time
	 *
	 * > [!NOTE] The cap may be exceeded by scaling.
	 * @example
	 * 
	 * @default 16.66
	 */
	deltaMS: number;
	/**
	 * Time elapsed in milliseconds from the last frame to this frame.
	 * This value is not capped or scaled and provides raw timing information.
	 *
	 * Unlike {@link Ticker#deltaMS}, this value is unmodified by speed scaling or FPS capping.
	 * @member {number}
	 * @example
	 * 
	 */
	elapsedMS: number;
	/**
	 * The last time update was invoked, in milliseconds since epoch.
	 * Similar to performance.now() timestamp format.
	 *
	 * Used internally for calculating time deltas between frames.
	 * @member {number}
	 * @example
	 * 
	 */
	lastTime: number;
	/**
	 * Factor of current {@link Ticker#deltaTime|deltaTime}.
	 * Used to scale time for slow motion or fast-forward effects.
	 * @example
	 * 
	 */
	speed: number;
	/**
	 * Whether or not this ticker has been started.
	 *
	 * `true` if {@link Ticker#start|start} has been called.
	 * `false` if {@link Ticker#stop|Stop} has been called.
	 *
	 * While `false`, this value may change to `true` in the
	 * event of {@link Ticker#autoStart|autoStart} being `true`
	 * and a listener is added.
	 * @example
	 * 
	 */
	started: boolean;
	constructor();
	/**
	 * Register a handler for tick events.
	 * @param fn - The listener function to add. Receives the Ticker instance as parameter
	 * @param context - The context for the listener
	 * @param priority - The priority of the listener
	 * @example
	 * 
	 */
	add<T = any>(fn: TickerCallback<T>, context?: T, priority?: number): this;
	/**
	 * Add a handler for the tick event which is only executed once on the next frame.
	 * @example
	 * 
	 * @param fn - The listener function to be added for one update
	 * @param context - The listener context
	 * @param priority - The priority for emitting (default: UPDATE_PRIORITY.NORMAL)
	 * @returns This instance of a ticker
	 */
	addOnce<T = any>(fn: TickerCallback<T>, context?: T, priority?: number): this;
	/**
	 * Removes any handlers matching the function and context parameters.
	 * If no handlers are left after removing, then it cancels the animation frame.
	 * @example
	 * 
	 * @param fn - The listener function to be removed
	 * @param context - The listener context to be removed
	 * @returns This instance of a ticker
	 */
	remove<T = any>(fn: TickerCallback<T>, context?: T): this;
	/**
	 * The number of listeners on this ticker, calculated by walking through linked list.
	 * @example
	 * 
	 */
	get count(): number;
	/**
	 * Starts the ticker. If the ticker has listeners a new animation frame is requested at this point.
	 * @example
	 * 
	 */
	start(): void;
	/**
	 * Stops the ticker. If the ticker has requested an animation frame it is canceled at this point.
	 * @example
	 * 
	 */
	stop(): void;
	/**
	 * Destroy the ticker and don't use after this. Calling this method removes all references to internal events.
	 * @example
	 * 
	 */
	destroy(): void;
	/**
	 * Triggers an update.
	 *
	 * An update entails setting the
	 * current {@link Ticker#elapsedMS|elapsedMS},
	 * the current {@link Ticker#deltaTime|deltaTime},
	 * invoking all listeners with current deltaTime,
	 * and then finally setting {@link Ticker#lastTime|lastTime}
	 * with the value of currentTime that was provided.
	 *
	 * This method will be called automatically by animation
	 * frame callbacks if the ticker instance has been started
	 * and listeners are added.
	 * @example
	 * 
	 * @param currentTime - The current time of execution (defaults to performance.now())
	 */
	update(currentTime?: number): void;
	/**
	 * The frames per second at which this ticker is running.
	 * The default is approximately 60 in most modern browsers.
	 * > [!NOTE] This does not factor in the value of
	 * > {@link Ticker#speed|speed}, which is specific
	 * > to scaling {@link Ticker#deltaTime|deltaTime}.
	 * @example
	 * 
	 */
	get FPS(): number;
	/**
	 * Manages the maximum amount of milliseconds allowed to
	 * elapse between invoking {@link Ticker#update|update}.
	 *
	 * This value is used to cap {@link Ticker#deltaTime|deltaTime},
	 * but does not effect the measured value of {@link Ticker#FPS|FPS}.
	 *
	 * When setting this property it is clamped to a value between
	 * `0` and `Ticker.targetFPMS * 1000`.
	 * @example
	 * 
	 * @default 10
	 */
	get minFPS(): number;
	set minFPS(fps: number);
	/**
	 * Manages the minimum amount of milliseconds required to
	 * elapse between invoking {@link Ticker#update|update}.
	 *
	 * This will effect the measured value of {@link Ticker#FPS|FPS}.
	 *
	 * If it is set to `0`, then there is no limit; PixiJS will render as many frames as it can.
	 * Otherwise it will be at least `minFPS`
	 * @example
	 * 
	 * @default 0
	 */
	get maxFPS(): number;
	set maxFPS(fps: number);
	/**
	 * The shared ticker instance used by {@link AnimatedSprite} and by
	 * {@link VideoSource} to update animation frames / video textures.
	 *
	 * It may also be used by {@link Application} if created with the `sharedTicker` option property set to true.
	 *
	 * The property {@link Ticker#autoStart|autoStart} is set to `true` for this instance.
	 * Please follow the examples for usage, including how to opt-out of auto-starting the shared ticker.
	 * @example
	 * import { Ticker } from 'pixi.js';
	 *
	 * const ticker = Ticker.shared;
	 * // Set this to prevent starting this ticker when listeners are added.
	 * // By default this is true only for the Ticker.shared instance.
	 * ticker.autoStart = false;
	 *
	 * // FYI, call this to ensure the ticker is stopped. It should be stopped
	 * // if you have not attempted to render anything yet.
	 * ticker.stop();
	 *
	 * // Call this when you are ready for a running shared ticker.
	 * ticker.start();
	 * @example
	 * import { autoDetectRenderer, Container } from 'pixi.js';
	 *
	 * // You may use the shared ticker to render...
	 * const renderer = autoDetectRenderer();
	 * const stage = new Container();
	 * document.body.appendChild(renderer.view);
	 * ticker.add((time) => renderer.render(stage));
	 *
	 * // Or you can just update it manually.
	 * ticker.autoStart = false;
	 * ticker.stop();
	 * const animate = (time) => {
	 *     ticker.update(time);
	 *     renderer.render(stage);
	 *     requestAnimationFrame(animate);
	 * };
	 * animate(performance.now());
	 * @type {Ticker}
	 */
	static get shared(): Ticker;
}
type ResizeableRenderer = Pick<Renderer, "resize">;
/**
 * Application options for the {@link ResizePlugin}.
 * These options control how your application handles window and element resizing.
 * @example
 * 
 */
export interface ResizePluginOptions {
	/**
	 * Element to automatically resize the renderer to.
	 * @example
	 * 
	 * @default null
	 */
	resizeTo?: Window | HTMLElement;
}
/**
 * Middleware for Application's resize functionality. This plugin handles automatic
 * and manual resizing of your PixiJS application.
 *
 * Adds the following features to {@link Application}:
 * - `resizeTo`: Set an element to automatically resize to
 * - `resize`: Manually trigger a resize
 * - `queueResize`: Queue a resize for the next animation frame
 * - `cancelResize`: Cancel a queued resize
 * @example
 * 
 */
export declare class ResizePlugin {
}
/**
 * Application options for the {@link TickerPlugin}.
 * These options control the animation loop and update cycle of your PixiJS application.
 * @example
 * 
 * @remarks
 * The ticker is the heart of your application's animation system. It:
 * - Manages the render loop
 * - Provides accurate timing information
 * - Handles frame-based updates
 * - Supports priority-based execution order
 */
export interface TickerPluginOptions {
	/**
	 * Controls whether the animation loop starts automatically after initialization.
	 * > [!IMPORTANT]
	 * > Setting this to `false` does NOT stop the shared ticker even if `sharedTicker` is `true`.
	 * > You must stop the shared ticker manually if needed.
	 * @example
	 * 
	 * @default true
	 */
	autoStart?: boolean;
	/**
	 * Controls whether to use the shared global ticker or create a new instance.
	 *
	 * The shared ticker is useful when you have multiple instances that should sync their updates.
	 * However, it has some limitations regarding update order control.
	 *
	 * Update Order:
	 * 1. System ticker (always runs first)
	 * 2. Shared ticker (if enabled)
	 * 3. App ticker (if using own ticker)
	 * @example
	 * 
	 * @default false
	 */
	sharedTicker?: boolean;
}
/**
 * Middleware for Application's {@link Ticker} functionality. This plugin manages the
 * animation loop and update cycle of your PixiJS application.
 *
 * Adds the following features to {@link Application}:
 * - `ticker`: Access to the application's ticker
 * - `start`: Start the animation loop
 * - `stop`: Stop the animation loop
 * @example
 * 
 */
export declare class TickerPlugin {
}
declare global {
	namespace PixiMixins {
		// Extend the Application interface with resize and ticker functionalities
		interface Application {
			/**
			 * Element to automatically resize the renderer to.
			 * @example
			 * 
			 * @default null
			 */
			resizeTo: Window | HTMLElement;
			/**
			 * Element to automatically resize the renderer to.
			 * > [!IMPORTANT]
			 * > You do not need to call this method manually in most cases.
			 * > A `resize` event will be dispatched automatically when the `resizeTo` element changes size.
			 * @remarks
			 * - Automatically resizes the renderer to match the size of the `resizeTo` element
			 * - If `resizeTo` is `null`, auto-resizing is disabled
			 * - If `resizeTo` is a `Window`, it resizes to the full window size
			 * - If `resizeTo` is an `HTMLElement`, it resizes to the element's bounding client rectangle
			 * @example
			 * 
			 * @default null
			 */
			resize(): void;
			/**
			 * Queue a resize operation for the next animation frame. This method is throttled
			 * and optimized for frequent calls.
			 * > [!IMPORTANT]
			 * > You do not need to call this method manually in most cases.
			 * > A `resize` event will be dispatched automatically when the `resizeTo` element changes size.
			 * @remarks
			 * - Safe to call multiple times per frame
			 * - Only one resize will occur on next frame
			 * - Cancels any previously queued resize
			 * @example
			 * 
			 */
			queueResize(): void;
			/**
			 * Cancel any pending resize operation that was queued with `queueResize()`.
			 * @remarks
			 * - Clears the resize operation queued for next frame
			 * @example
			 * 
			 */
			cancelResize(): void;
			/**
			 * The application's ticker instance that manages the update/render loop.
			 * @example
			 * 
			 */
			ticker: Ticker;
			/**
			 * Stops the render/update loop.
			 * @example
			 * 
			 */
			stop(): void;
			/**
			 * Starts the render/update loop.
			 * @example
			 * 
			 */
			start(): void;
		}
		// Combine ResizePluginOptions and TickerPluginOptions into ApplicationOptions
		interface ApplicationOptions extends ResizePluginOptions, TickerPluginOptions {
		}
	}
}
declare global {
	namespace PixiMixins {
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface AssetsPreferences {
		}
	}
}
/**
 * The CullingMixin interface provides properties and methods for managing culling behavior
 * of a display object. Culling is the process of determining whether an object should be rendered
 * based on its visibility within the current view or frame.
 *
 * Key Features:
 * - Custom culling areas for better performance
 * - Per-object culling control
 * - Child culling management
 * @example
 * 
 */
export interface CullingMixinConstructor {
	/**
	 * Custom shape used for culling calculations instead of object bounds.
	 * Defined in local space coordinates relative to the object.
	 * > [!NOTE]
	 * > Setting this to a custom Rectangle allows you to define a specific area for culling,
	 * > which can improve performance by avoiding expensive bounds calculations.
	 * @example
	 * 
	 * @remarks
	 * - Improves performance by avoiding bounds calculations
	 * - Useful for containers with many children
	 * - Set to null to use object bounds
	 * @default null
	 */
	cullArea: Rectangle;
	/**
	 * Controls whether this object should be culled when out of view.
	 * When true, the object will not be rendered if its bounds are outside the visible area.
	 * @example
	 * 
	 * @remarks
	 * - Does not affect transform updates
	 * - Applies to this object only
	 * - Children follow their own cullable setting
	 * @default false
	 */
	cullable: boolean;
	/**
	 * Controls whether children of this container can be culled.
	 * When false, skips recursive culling checks for better performance.
	 * @example
	 * 
	 * @remarks
	 * - Improves performance for static scenes
	 * - Useful when children are always within container bounds
	 * - Parent culling still applies
	 * @default true
	 */
	cullableChildren: boolean;
}
/**
 * Application options for the {@link CullerPlugin}.
 * These options control how your application handles culling of display objects.
 * @example
 * 
 */
export interface CullerPluginOptions {
	/**
	 * Options for the culler behavior.
	 * @example
	 * 
	 */
	culler?: {
		/**
		 * Update the transform of culled objects.
		 *
		 * > [!IMPORTANT] Keeping this as `false` can improve performance by avoiding unnecessary calculations,
		 * > however, the transform used for culling may not be up-to-date if the object has moved since the last render.
		 * @default true
		 * @example
		 * 
		 */
		updateTransform?: boolean;
	};
}
/**
 * An {@link Application} plugin that automatically culls (hides) display objects that are outside
 * the visible screen area. This improves performance by not rendering objects that aren't visible.
 *
 * Key Features:
 * - Automatic culling based on screen boundaries
 * - Configurable culling areas and behavior per container
 * - Can improve rendering performance
 * @example
 * 
 * @remarks
 * To enable culling, you must set the following properties on your containers:
 * - `cullable`: Set to `true` to enable culling for the container
 * - `cullableChildren`: Set to `true` to enable culling for children (default)
 * - `cullArea`: Optional custom Rectangle for culling bounds
 *
 * Performance Tips:
 * - Group objects that are spatially related
 * - Use `cullArea` for containers with many children to avoid bounds calculations
 * - Set `cullableChildren = false` for containers that are always fully visible
 */
export declare class CullerPlugin {
}
declare global {
	namespace PixiMixins {
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface Container extends Partial<CullingMixinConstructor> {
		}
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface ContainerOptions extends Partial<CullingMixinConstructor> {
		}
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface ApplicationOptions extends Partial<CullerPluginOptions> {
		}
	}
}
/**
 * Options for configuring a {@link DOMContainer}.
 * Controls how DOM elements are integrated into the PixiJS scene graph.
 * @example
 * 
 */
export interface DOMContainerOptions extends ViewContainerOptions {
	/**
	 * The DOM element to use for the container.
	 * Can be any HTML element like div, input, textarea, etc.
	 *
	 * If not provided, creates a new div element.
	 * @default document.createElement('div')
	 */
	element?: HTMLElement;
	/**
	 * The anchor point of the container.
	 * - Can be a single number to set both x and y
	 * - Can be a point-like object with x,y coordinates
	 * - (0,0) is top-left
	 * - (1,1) is bottom-right
	 * - (0.5,0.5) is center
	 * @default 0
	 */
	anchor?: PointData | number;
}
/**
 * The DOMContainer object is used to render DOM elements within the PixiJS scene graph.
 * It allows you to integrate HTML elements into your PixiJS application while maintaining
 * proper transform hierarchy and visibility.
 *
 * DOMContainer is especially useful for rendering standard DOM elements
 * that handle user input, such as `<input>` or `<textarea>`.
 * This is often simpler and more flexible than trying to implement text input
 * directly in PixiJS. For instance, if you need text fields or text areas,
 * you can embed them through this container for native browser text handling.
 *
 * --------- EXPERIMENTAL ---------
 *
 * This is a new API, things may change and it may not work as expected.
 * We want to hear your feedback as we go!
 *
 * --------------------------------
 * @example
 * @example
 * 
 */
export declare class DOMContainer extends ViewContainer<never> {
	/**
	 * @param options - The options for creating the DOM container.
	 */
	constructor(options?: DOMContainerOptions);
	/**
	 * The anchor sets the origin point of the container.
	 * Controls the relative positioning of the DOM element.
	 *
	 * The default is `(0,0)`, this means the container's origin is the top left.
	 * Setting the anchor to `(0.5,0.5)` means the container's origin is centered.
	 * Setting the anchor to `(1,1)` would mean the container's origin point will be the bottom right corner.
	 * @example
	 * 
	 */
	get anchor(): Point;
	/**
	 * Sets the anchor point of the container.
	 * @param value - New anchor value:
	 * - number: Sets both x and y to same value
	 * - PointData: Sets x and y separately
	 */
	set anchor(value: PointData | number);
	/**
	 * Sets the DOM element for this container.
	 * This will replace the current element and update the view.
	 * @param value - The new DOM element to use
	 * @example
	 * 
	 */
	set element(value: HTMLElement);
	/**
	 * The DOM element associated with this container.
	 * @example
	 * 
	 */
	get element(): HTMLElement;
	/**
	 * Destroys this DOM container.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that
	 * @example
	 * domContainer.destroy();
	 * domContainer.destroy(true);
	 */
	destroy(options?: boolean): void;
}
declare global {
	namespace PixiMixins {
		interface RendererPipes {
			dom: DOMPipe;
		}
	}
}
/**
 * A specialized event class for wheel/scroll interactions in PixiJS applications.
 * Extends {@link FederatedMouseEvent} to provide wheel-specific properties while
 * maintaining compatibility with the DOM WheelEvent interface.
 *
 * Key features:
 * - Provides scroll delta information
 * - Supports different scroll modes (pixel, line, page)
 * - Inherits mouse event properties
 * - Normalizes cross-browser wheel events
 * @example
 * 
 */
export declare class FederatedWheelEvent extends FederatedMouseEvent implements WheelEvent {
	/**
	 * The units of `deltaX`, `deltaY`, and `deltaZ`. This is one of `DOM_DELTA_LINE`,
	 * `DOM_DELTA_PAGE`, `DOM_DELTA_PIXEL`.
	 */
	deltaMode: number;
	/** Horizontal scroll amount */
	deltaX: number;
	/** Vertical scroll amount */
	deltaY: number;
	/** z-axis scroll amount. */
	deltaZ: number;
}
type EmitterListener = {
	fn(...args: any[]): any;
	context: any;
	once: boolean;
};
/**
 * The type of cursor to use when the mouse pointer is hovering over an interactive element.
 * Accepts any valid CSS cursor value.
 * @example
 * 
 *
 * Common cursor values:
 * - Basic: `auto`, `default`, `none`, `pointer`, `wait`
 * - Text: `text`, `vertical-text`
 * - Links: `alias`, `copy`, `move`
 * - Selection: `cell`, `crosshair`
 * - Drag: `grab`, `grabbing`
 * - Disabled: `not-allowed`, `no-drop`
 * - Resize: `n-resize`, `e-resize`, `s-resize`, `w-resize`
 * - Bidirectional: `ns-resize`, `ew-resize`, `nesw-resize`, `nwse-resize`
 * - Other: `help`, `progress`
 */
export type Cursor = "auto" | "default" | "none" | "context-menu" | "help" | "pointer" | "progress" | "wait" | "cell" | "crosshair" | "text" | "vertical-text" | "alias" | "copy" | "move" | "no-drop" | "not-allowed" | "e-resize" | "n-resize" | "ne-resize" | "nw-resize" | "s-resize" | "se-resize" | "sw-resize" | "w-resize" | "ns-resize" | "ew-resize" | "nesw-resize" | "col-resize" | "nwse-resize" | "row-resize" | "all-scroll" | "zoom-in" | "zoom-out" | "grab" | "grabbing";
/**
 * Interface defining a hit area for pointer interaction. The hit area specifies
 * the region in which pointer events should be captured by a display object.
 * @example
 * 
 * @remarks
 * - Hit areas override the default bounds-based hit testing
 * - Can improve performance by simplifying hit tests
 * - Useful for irregular shapes or precise interaction areas
 * - Common implementations include Rectangle, Circle, Polygon
 */
export interface IHitArea {
	/**
	 * Checks if the given coordinates are inside this hit area.
	 * @param {number} x - The x coordinate to check
	 * @param {number} y - The y coordinate to check
	 * @returns True if the coordinates are inside the hit area
	 */
	contains(x: number, y: number): boolean;
}
/**
 * The type of interaction behavior for a Container. This is set via the {@link Container#eventMode} property.
 * @example
 * 
 *
 * Available modes:
 * - `'none'`: Ignores all interaction events, even on its children
 * - `'passive'`: **(default)** Does not emit events and ignores hit testing on itself and non-interactive children.
 * Interactive children will still emit events.
 * - `'auto'`: Does not emit events but is hit tested if parent is interactive. Same as `interactive = false` in v7
 * - `'static'`: Emit events and is hit tested. Same as `interactive = true` in v7
 * - `'dynamic'`: Emits events and is hit tested but will also receive mock interaction events fired from
 * a ticker to allow for interaction when the mouse isn't moving
 *
 * Performance tips:
 * - Use `'none'` for pure visual elements
 * - Use `'passive'` for containers with some interactive children
 * - Use `'static'` for standard buttons/controls
 * - Use `'dynamic'` only for moving/animated interactive elements
 * @since 7.2.0
 */
export type EventMode = "none" | "passive" | "auto" | "static" | "dynamic";
/**
 * The properties available for any interactive object. This interface defines the core interaction
 * properties and event handlers that can be set on any Container in PixiJS.
 * @example
 * 
 *
 * Core Properties:
 * - `eventMode`: Controls how the object handles interaction events
 * - `cursor`: Sets the mouse cursor when hovering
 * - `hitArea`: Defines custom hit testing area
 * - `interactive`: Alias for `eventMode` to enable interaction with "static" or "passive" modes
 * - `interactiveChildren`: Controls hit testing on children
 *
 * Event Handlers:
 * - Mouse: click, mousedown, mouseup, mousemove, mouseenter, mouseleave
 * - Touch: touchstart, touchend, touchmove, tap
 * - Pointer: pointerdown, pointerup, pointermove, pointerover
 * - Global: globalpointermove, globalmousemove, globaltouchmove
 * > [!IMPORTANT] Global events are fired when the pointer moves even if it is outside the bounds of the Container.
 */
export interface FederatedOptions {
	/**
	 * The cursor style to display when the mouse pointer is hovering over the object.
	 * Accepts any valid CSS cursor value or custom cursor URL.
	 * @example
	 * 
	 * @type {Cursor | string}
	 * @default undefined
	 */
	cursor?: Cursor | (string & {});
	/**
	 * Enable interaction events for the Container. Touch, pointer and mouse events are supported.
	 * @example
	 * 
	 *
	 * Available modes:
	 *
	 * - `'none'`: Ignores all interaction events, even on its children. Best for pure visuals.
	 * - `'passive'`: **(default)** Does not emit events and ignores hit testing on itself and non-interactive
	 * children. Interactive children will still emit events.
	 * - `'auto'`: Does not emit events but is hit tested if parent is interactive. Same as `interactive = false` in v7.
	 * - `'static'`: Emit events and is hit tested. Same as `interactive = true` in v7. Best for buttons/UI.
	 * - `'dynamic'`: Like static but also receives synthetic events when pointer is idle. Best for moving objects.
	 *
	 * Performance tips:
	 * - Use `'none'` for pure visual elements
	 * - Use `'passive'` for containers with some interactive children
	 * - Use `'static'` for standard UI elements
	 * - Use `'dynamic'` only when needed for moving/animated elements
	 * @since 7.2.0
	 */
	eventMode?: EventMode;
	/**
	 * Whether this object should fire UI events. This is an alias for `eventMode` set to `'static'` or `'passive'`.
	 * Setting this to true will enable interaction events like `pointerdown`, `click`, etc.
	 * Setting it to false will disable all interaction events on this object.
	 * @example
	 * 
	 */
	interactive?: boolean;
	/**
	 * Controls whether children of this container can receive pointer events.
	 *
	 * Setting this to false allows PixiJS to skip hit testing on all children,
	 * improving performance for containers with many non-interactive children.
	 * @default true
	 * @example
	 * 
	 */
	interactiveChildren?: boolean;
	/**
	 * Defines a custom hit area for pointer interaction testing. When set, this shape will be used
	 * for hit testing instead of the container's standard bounds.
	 * @example
	 * 
	 * @remarks
	 * - Takes precedence over the container's bounds for hit testing
	 * - Can improve performance by simplifying collision checks
	 * - Useful for irregular shapes or precise click areas
	 */
	hitArea?: IHitArea | null;
	/**
	 * Property-based event handler for the `click` event.
	 * Fired when a pointer device (mouse, touch, etc.) completes a click action.
	 * @example
	 * 
	 * @default null
	 */
	onclick?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mousedown` event.
	 * Fired when a mouse button is pressed while the pointer is over the object.
	 * @example
	 * 
	 * @default null
	 */
	onmousedown?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mouseenter` event.
	 * Fired when the mouse pointer enters the bounds of the object. Does not bubble.
	 * @example
	 * 
	 * @default null
	 */
	onmouseenter?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mouseleave` event.
	 * Fired when the pointer leaves the bounds of the display object. Does not bubble.
	 * @example
	 * 
	 * @default null
	 */
	onmouseleave?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mousemove` event.
	 * Fired when the pointer moves while over the display object.
	 * @example
	 * 
	 * @default null
	 */
	onmousemove?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `globalmousemove` event.
	 *
	 * Fired when the mouse moves anywhere, regardless of whether the pointer is over this object.
	 * The object must have `eventMode` set to 'static' or 'dynamic' to receive this event.
	 * @example
	 * 
	 * @default null
	 * @remarks
	 * - Fires even when the mouse is outside the object's bounds
	 * - Useful for drag operations or global mouse tracking
	 * - Must have `eventMode` set appropriately to receive events
	 * - Part of the global move events family along with `globalpointermove` and `globaltouchmove`
	 */
	onglobalmousemove?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mouseout` event.
	 * Fired when the pointer moves out of the bounds of the display object.
	 * @example
	 * 
	 * @default null
	 */
	onmouseout?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mouseover` event.
	 * Fired when the pointer moves onto the bounds of the display object.
	 * @example
	 * 
	 * @default null
	 */
	onmouseover?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mouseup` event.
	 * Fired when a mouse button is released over the display object.
	 * @example
	 * 
	 * @default null
	 */
	onmouseup?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `mouseupoutside` event.
	 * Fired when a mouse button is released outside the display object that initially
	 * registered a mousedown.
	 * @example
	 * 
	 * @default null
	 */
	onmouseupoutside?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointercancel` event.
	 * Fired when a pointer device interaction is canceled or lost.
	 * @example
	 * 
	 * @default null
	 */
	onpointercancel?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerdown` event.
	 * Fired when a pointer device button (mouse, touch, pen, etc.) is pressed.
	 * @example
	 * 
	 * @default null
	 */
	onpointerdown?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerenter` event.
	 * Fired when a pointer device enters the bounds of the display object. Does not bubble.
	 * @example
	 * 
	 * @default null
	 */
	onpointerenter?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerleave` event.
	 * Fired when a pointer device leaves the bounds of the display object. Does not bubble.
	 * @example
	 * 
	 * @default null
	 */
	onpointerleave?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointermove` event.
	 * Fired when a pointer device moves while over the display object.
	 * @example
	 * 
	 * @default null
	 */
	onpointermove?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `globalpointermove` event.
	 *
	 * Fired when the pointer moves anywhere, regardless of whether the pointer is over this object.
	 * The object must have `eventMode` set to 'static' or 'dynamic' to receive this event.
	 * @example
	 * 
	 * @default null
	 * @remarks
	 * - Fires even when the mouse is outside the object's bounds
	 * - Useful for drag operations or global mouse tracking
	 * - Must have `eventMode` set appropriately to receive events
	 * - Part of the global move events family along with `globalpointermove` and `globaltouchmove`
	 */
	onglobalpointermove?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerout` event.
	 * Fired when the pointer moves out of the bounds of the display object.
	 * @example
	 * 
	 * @default null
	 */
	onpointerout?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerover` event.
	 * Fired when the pointer moves over the bounds of the display object.
	 * @example
	 * 
	 * @default null
	 */
	onpointerover?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointertap` event.
	 * Fired when a pointer device completes a tap action (e.g., touch or mouse click).
	 * @example
	 * 
	 * @default null
	 */
	onpointertap?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerup` event.
	 * Fired when a pointer device button (mouse, touch, pen, etc.) is released.
	 * @example
	 * 
	 * @default null
	 */
	onpointerup?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `pointerupoutside` event.
	 * Fired when a pointer device button is released outside the bounds of the display object
	 * that initially registered a pointerdown.
	 * @example
	 * 
	 * @default null
	 */
	onpointerupoutside?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `rightclick` event.
	 * Fired when a right-click (context menu) action is performed on the object.
	 * @example
	 * 
	 * @default null
	 */
	onrightclick?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `rightdown` event.
	 * Fired when a right mouse button is pressed down over the display object.
	 * @example
	 * 
	 * @default null
	 */
	onrightdown?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `rightup` event.
	 * Fired when a right mouse button is released over the display object.
	 * @example
	 * 
	 * @default null
	 */
	onrightup?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `rightupoutside` event.
	 * Fired when a right mouse button is released outside the bounds of the display object
	 * that initially registered a rightdown.
	 * @example
	 * 
	 * @default null
	 */
	onrightupoutside?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `tap` event.
	 * Fired when a tap action (touch) is completed on the object.
	 * @example
	 * 
	 * @default null
	 */
	ontap?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `touchcancel` event.
	 * Fired when a touch interaction is canceled, such as when the touch is interrupted.
	 * @example
	 * 
	 * @default null
	 */
	ontouchcancel?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `touchend` event.
	 * Fired when a touch interaction ends, such as when the finger is lifted from the screen.
	 * @example
	 * 
	 * @default null
	 */
	ontouchend?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `touchendoutside` event.
	 * Fired when a touch interaction ends outside the bounds of the display object
	 * that initially registered a touchstart.
	 * @example
	 * 
	 * @default null
	 */
	ontouchendoutside?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `touchmove` event.
	 * Fired when a touch interaction moves while over the display object.
	 * @example
	 * 
	 * @default null
	 */
	ontouchmove?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `globaltouchmove` event.
	 *
	 * Fired when a touch interaction moves anywhere, regardless of whether the pointer is over this object.
	 * The object must have `eventMode` set to 'static' or 'dynamic' to receive this event.
	 * @example
	 * 
	 * @default null
	 * @remarks
	 * - Fires even when the touch is outside the object's bounds
	 * - Useful for drag operations or global touch tracking
	 * - Must have `eventMode` set appropriately to receive events
	 * - Part of the global move events family along with `globalpointermove` and `globalmousemove`
	 */
	onglobaltouchmove?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `touchstart` event.
	 * Fired when a touch interaction starts, such as when a finger touches the screen.
	 * @example
	 * 
	 * @default null
	 */
	ontouchstart?: FederatedEventHandler | null;
	/**
	 * Property-based event handler for the `wheel` event.
	 * Fired when the mouse wheel is scrolled while over the display object.
	 * @example
	 * 
	 * @default null
	 */
	onwheel?: FederatedEventHandler<FederatedWheelEvent> | null;
}
/**
 * A PixiJS compatible touch event interface that extends the standard DOM Touch interface.
 * Provides additional properties to normalize touch input with mouse/pointer events.
 * @example
 * 
 */
export interface PixiTouch extends Touch {
	/** The button being pressed (0: left, 1: middle, 2: right) */
	button: number;
	/** Bitmap of currently pressed buttons */
	buttons: number;
	/** Whether this is the primary touch point */
	isPrimary: boolean;
	/** The width of the touch contact area */
	width: number;
	/** The height of the touch contact area */
	height: number;
	/** The angle of tilt along the x-axis (in degrees) */
	tiltX: number;
	/** The angle of tilt along the y-axis (in degrees) */
	tiltY: number;
	/** The type of pointer that triggered this event */
	pointerType: string;
	/** Unique identifier for this touch point */
	pointerId: number;
	/** The normalized pressure of the pointer (0 to 1) */
	pressure: number;
	/** The rotation angle of the pointer (e.g., pen) */
	twist: number;
	/** The normalized tangential pressure of the pointer */
	tangentialPressure: number;
	/** The x coordinate relative to the current layer */
	layerX: number;
	/** The y coordinate relative to the current layer */
	layerY: number;
	/** The x coordinate relative to the target's offset parent */
	offsetX: number;
	/** The y coordinate relative to the target's offset parent */
	offsetY: number;
	/** Whether the event was normalized by PixiJS */
	isNormalized: boolean;
	/** The type of touch event */
	type: string;
}
/**
 * A DOM-compatible synthetic event implementation for PixiJS's event system.
 * This class implements the standard DOM Event interface while providing additional
 * functionality specific to PixiJS events.
 * > [!NOTE] You wont receive an instance of this class directly, but rather a subclass
 * > of this class, such as {@link FederatedPointerEvent}, {@link FederatedMouseEvent}, or
 * > {@link FederatedWheelEvent}. This class is the base for all federated events.
 * @example
 * 
 * @typeParam N - The type of native event held. Can be either a UIEvent or PixiTouch.
 * @remarks
 * - Implements the standard DOM UIEvent interface
 * - Provides event bubbling and capturing phases
 * - Supports propagation control
 * - Manages event paths through display tree
 * - Normalizes native browser events
 */
export declare class FederatedEvent<N extends UIEvent | PixiTouch = UIEvent | PixiTouch> implements UIEvent {
	/** Flags whether this event bubbles. This will take effect only if it is set before propagation. */
	bubbles: boolean;
	/** @deprecated since 7.0.0 */
	cancelBubble: boolean;
	/**
	 * Flags whether this event can be canceled using {@link FederatedEvent.preventDefault}. This is always
	 * false (for now).
	 */
	readonly cancelable = false;
	/** The listeners of the event target that are being notified. */
	currentTarget: Container;
	/** Flags whether the default response of the user agent was prevent through this event. */
	defaultPrevented: boolean;
	/**
	 * The propagation phase.
	 * @default {@link FederatedEvent.NONE}
	 */
	eventPhase: number;
	/** Flags whether this is a user-trusted event */
	isTrusted: boolean;
	/** @deprecated since 7.0.0 */
	returnValue: boolean;
	/** @deprecated since 7.0.0 */
	srcElement: EventTarget;
	/** The event target that this will be dispatched to. */
	target: Container;
	/** The timestamp of when the event was created. */
	timeStamp: number;
	/** The type of event, e.g. `"mouseup"`. */
	type: string;
	/** The native event that caused the foremost original event. */
	nativeEvent: N;
	/** The original event that caused this event, if any. */
	originalEvent: FederatedEvent<N>;
	/** Flags whether propagation was stopped. */
	propagationStopped: boolean;
	/** Flags whether propagation was immediately stopped. */
	propagationImmediatelyStopped: boolean;
	/** The composed path of the event's propagation. The `target` is at the end. */
	path: Container[];
	/** The {@link EventBoundary} that manages this event. Null for root events. */
	readonly manager: EventBoundary;
	/** Event-specific detail */
	detail: number;
	/** The global Window object. */
	view: WindowProxy;
	/** The coordinates of the event relative to the nearest DOM layer. This is a non-standard property. */
	layer: Point;
	/** @readonly */
	get layerX(): number;
	/** @readonly */
	get layerY(): number;
	/** The coordinates of the event relative to the DOM document. This is a non-standard property. */
	page: Point;
	/** @readonly */
	get pageX(): number;
	/** @readonly */
	get pageY(): number;
	/**
	 * @param manager - The event boundary which manages this event. Propagation can only occur
	 *  within the boundary's jurisdiction.
	 */
	constructor(manager: EventBoundary);
	/**
	 * Fallback for the deprecated `InteractionEvent.data`.
	 * @deprecated since 7.0.0
	 */
	get data(): this;
	/**
	 * Prevent default behavior of both PixiJS and the user agent.
	 * @example
	 * 
	 * @remarks
	 * - Only works if the native event is cancelable
	 * - Does not stop event propagation
	 */
	preventDefault(): void;
	/**
	 * Stop this event from propagating to any additional listeners, including those
	 * on the current target and any following targets in the propagation path.
	 * @example
	 * 
	 * @remarks
	 * - Immediately stops all event propagation
	 * - Prevents other listeners on same target from being called
	 * - More aggressive than stopPropagation()
	 */
	stopImmediatePropagation(): void;
	/**
	 * Stop this event from propagating to the next target in the propagation path.
	 * The rest of the listeners on the current target will still be notified.
	 * @example
	 * 
	 * @remarks
	 * - Stops event bubbling to parent containers
	 * - Does not prevent other listeners on same target
	 * - Less aggressive than stopImmediatePropagation()
	 */
	stopPropagation(): void;
}
/**
 * A specialized event class for mouse interactions in PixiJS applications.
 * Extends {@link FederatedEvent} to provide mouse-specific properties and methods
 * while maintaining compatibility with the DOM MouseEvent interface.
 *
 * Key features:
 * - Tracks mouse button states
 * - Provides modifier key states
 * - Supports coordinate systems (client, screen, global)
 * - Enables precise position tracking
 * @example
 * 
 */
export declare class FederatedMouseEvent extends FederatedEvent<MouseEvent | PointerEvent | PixiTouch> implements MouseEvent {
	/** Whether the "alt" key was pressed when this mouse event occurred. */
	altKey: boolean;
	/** The specific button that was pressed in this mouse event. */
	button: number;
	/** The button depressed when this event occurred. */
	buttons: number;
	/** Whether the "control" key was pressed when this mouse event occurred. */
	ctrlKey: boolean;
	/** Whether the "meta" key was pressed when this mouse event occurred. */
	metaKey: boolean;
	/** This is currently not implemented in the Federated Events API. */
	relatedTarget: EventTarget;
	/** Whether the "shift" key was pressed when this mouse event occurred. */
	shiftKey: boolean;
	/** The coordinates of the mouse event relative to the canvas. */
	client: Point;
	/** @readonly */
	get clientX(): number;
	/** @readonly */
	get clientY(): number;
	/**
	 * Alias for {@link FederatedMouseEvent.clientX this.clientX}.
	 */
	get x(): number;
	/**
	 * Alias for {@link FederatedMouseEvent.clientY this.clientY}.
	 */
	get y(): number;
	/** This is the number of clicks that occurs in 200ms/click of each other. */
	detail: number;
	/** The movement in this pointer relative to the last `mousemove` event. */
	movement: Point;
	/** @readonly */
	get movementX(): number;
	/** @readonly */
	get movementY(): number;
	/** The offset of the pointer coordinates w.r.t. target Container in world space. This is not supported at the moment. */
	offset: Point;
	/** @readonly */
	get offsetX(): number;
	/** @readonly */
	get offsetY(): number;
	/** The pointer coordinates in world space. */
	global: Point;
	/** @readonly */
	get globalX(): number;
	/** @readonly */
	get globalY(): number;
	/**
	 * The pointer coordinates in the renderer's {@link AbstractRenderer.screen screen}. This has slightly
	 * different semantics than native PointerEvent screenX/screenY.
	 */
	screen: Point;
	/**
	 * The pointer coordinates in the renderer's screen. Alias for `screen.x`.
	 */
	get screenX(): number;
	/**
	 * The pointer coordinates in the renderer's screen. Alias for `screen.y`.
	 */
	get screenY(): number;
	/**
	 * Converts global coordinates into container-local coordinates.
	 *
	 * This method transforms coordinates from world space to a container's local space,
	 * useful for precise positioning and hit testing.
	 * @param container - The Container to get local coordinates for
	 * @param point - Optional Point object to store the result. If not provided, a new Point will be created
	 * @param globalPos - Optional custom global coordinates. If not provided, the event's global position is used
	 * @returns The local coordinates as a Point object
	 * @example
	 * 
	 */
	getLocalPosition<P extends PointData = Point>(container: Container, point?: P, globalPos?: PointData): P;
	/**
	 * Whether the modifier key was pressed when this event natively occurred.
	 * @param key - The modifier key.
	 */
	getModifierState(key: string): boolean;
}
/**
 * A specialized event class for pointer interactions in PixiJS applications.
 * Extends {@link FederatedMouseEvent} to provide advanced pointer-specific features
 * while maintaining compatibility with the DOM PointerEvent interface.
 *
 * Key features:
 * - Supports multi-touch interactions
 * - Provides pressure sensitivity
 * - Handles stylus input
 * - Tracks pointer dimensions
 * - Supports tilt detection
 * @example
 * 
 */
export declare class FederatedPointerEvent extends FederatedMouseEvent implements PointerEvent {
	/**
	 * The unique identifier of the pointer.
	 */
	pointerId: number;
	/**
	 * The width of the pointer's contact along the x-axis, measured in CSS pixels.
	 * radiusX of TouchEvents will be represented by this value.
	 */
	width: number;
	/**
	 * The angle in radians of a pointer or stylus measuring the vertical angle between
	 * the device's surface to the pointer or stylus.
	 * A stylus at 0 degrees would be directly parallel whereas at π/2 degrees it would be perpendicular.
	 */
	altitudeAngle: number;
	/**
	 * The angle in radians of a pointer or stylus measuring an arc from the X axis of the device to
	 * the pointer or stylus projected onto the screen's plane.
	 * A stylus at 0 degrees would be pointing to the "0 o'clock" whereas at π/2 degrees it would be pointing at "6 o'clock".
	 */
	azimuthAngle: number;
	/**
	 * The height of the pointer's contact along the y-axis, measured in CSS pixels.
	 * radiusY of TouchEvents will be represented by this value.
	 */
	height: number;
	/**
	 * Indicates whether or not the pointer device that created the event is the primary pointer.
	 */
	isPrimary: boolean;
	/**
	 * The type of pointer that triggered the event.
	 */
	pointerType: string;
	/**
	 * Pressure applied by the pointing device during the event.
	 *s
	 * A Touch's force property will be represented by this value.
	 */
	pressure: number;
	/**
	 * Barrel pressure on a stylus pointer.
	 */
	tangentialPressure: number;
	/**
	 * The angle, in degrees, between the pointer device and the screen.
	 */
	tiltX: number;
	/**
	 * The angle, in degrees, between the pointer device and the screen.
	 */
	tiltY: number;
	/**
	 * Twist of a stylus pointer.
	 */
	twist: number;
	/** This is the number of clicks that occurs in 200ms/click of each other. */
	detail: number;
}
/**
 * The system for handling UI events in PixiJS applications. This class manages mouse, touch, and pointer events,
 * normalizing them into a consistent event model.
 * @example
 * 
 *
 * Features:
 * - Normalizes browser events into consistent format
 * - Supports mouse, touch, and pointer events
 * - Handles event delegation and bubbling
 * - Provides cursor management
 * - Configurable event features
 */
export declare class EventSystem implements System<EventSystemOptions> {
	/**
	 * The event features that are enabled by the EventSystem
	 * @since 7.2.0
	 * @example
	 * 
	 */
	static defaultEventFeatures: EventSystemFeatures;
	/**
	 * The default interaction mode for all display objects.
	 * @type {EventMode}
	 * @since 7.2.0
	 */
	static get defaultEventMode(): EventMode;
	/**
	 * Indicates whether the current device supports touch events according to the W3C Touch Events spec.
	 * This is used to determine the appropriate event handling strategy.
	 * @default 'ontouchstart' in globalThis
	 */
	readonly supportsTouchEvents: boolean;
	/**
	 * Indicates whether the current device supports pointer events according to the W3C Pointer Events spec.
	 * Used to optimize event handling and provide more consistent cross-device interaction.
	 * @default !!globalThis.PointerEvent
	 */
	readonly supportsPointerEvents: boolean;
	/**
	 * Controls whether default browser actions are automatically prevented on pointer events.
	 * When true, prevents default browser actions from occurring on pointer events.
	 * @remarks
	 * - Does not apply to pointer events for backwards compatibility
	 * - preventDefault on pointer events stops mouse events from firing
	 * - For every pointer event, there will always be either a mouse or touch event alongside it
	 * - Setting this to false allows default browser actions (text selection, dragging images, etc.)
	 * @example
	 * 
	 * @default true
	 */
	autoPreventDefault: boolean;
	/**
	 * Dictionary of custom cursor styles that can be used across the application.
	 * Used to define how different cursor modes are handled when interacting with display objects.
	 * @example
	 * 
	 * @remarks
	 * - Strings are treated as CSS cursor values
	 * - Objects are applied as CSS styles to the DOM element
	 * - Functions are called directly for custom cursor handling
	 * - Default styles for 'default' and 'pointer' are provided
	 * @default
	 * 
	 */
	cursorStyles: Record<string, string | ((mode: string) => void) | CSSStyleDeclaration>;
	/**
	 * The DOM element to which the root event listeners are bound. This is automatically set to
	 * the renderer's {@link Renderer#view view}.
	 */
	domElement: HTMLElement;
	/** The resolution used to convert between the DOM client space into world space. */
	resolution: number;
	/** The renderer managing this {@link EventSystem}. */
	renderer: Renderer;
	/**
	 * The event features that are enabled by the EventSystem
	 * @since 7.2.0
	 * @example
	 * const app = new Application()
	 * app.renderer.events.features.globalMove = false
	 *
	 * // to override all features use Object.assign
	 * Object.assign(app.renderer.events.features, {
	 *  move: false,
	 *  globalMove: false,
	 *  click: false,
	 *  wheel: false,
	 * })
	 */
	readonly features: EventSystemFeatures;
	/**
	 * @param {Renderer} renderer
	 */
	constructor(renderer: Renderer);
	/** Destroys all event listeners and detaches the renderer. */
	destroy(): void;
	/**
	 * Sets the current cursor mode, handling any callbacks or CSS style changes.
	 * The cursor can be a CSS cursor string, a custom callback function, or a key from the cursorStyles dictionary.
	 * @param mode - Cursor mode to set. Can be:
	 * - A CSS cursor string (e.g., 'pointer', 'grab')
	 * - A key from the cursorStyles dictionary
	 * - null/undefined to reset to default
	 * @example
	 * 
	 * @remarks
	 * - Has no effect on OffscreenCanvas except for callback-based cursors
	 * - Caches current cursor to avoid unnecessary DOM updates
	 * - Supports CSS cursor values, style objects, and callback functions
	 */
	setCursor(mode: string): void;
	/**
	 * The global pointer event instance containing the most recent pointer state.
	 * This is useful for accessing pointer information without listening to events.
	 * @example
	 * 
	 * @since 7.2.0
	 */
	get pointer(): Readonly<FederatedPointerEvent>;
	/**
	 * Sets the {@link EventSystem#domElement domElement} and binds event listeners.
	 * This method manages the DOM event bindings for the event system, allowing you to
	 * change or remove the target element that receives input events.
	 * > [!IMPORTANT] This will default to the canvas element of the renderer, so you
	 * > should not need to call this unless you are using a custom element.
	 * @param element - The new DOM element to bind events to, or null to remove all event bindings
	 * @example
	 * 
	 * @remarks
	 * - Automatically removes event listeners from previous element
	 * - Required for the event system to function
	 * - Safe to call multiple times
	 */
	setTargetElement(element: HTMLElement): void;
	/**
	 * Maps coordinates from DOM/screen space into PixiJS normalized coordinates.
	 * This takes into account the current scale, position, and resolution of the DOM element.
	 * @param point - The point to store the mapped coordinates in
	 * @param x - The x coordinate in DOM/client space
	 * @param y - The y coordinate in DOM/client space
	 * @example
	 * 
	 * @remarks
	 * - Accounts for element scaling and positioning
	 * - Adjusts for device pixel ratio/resolution
	 */
	mapPositionToPoint(point: PointData, x: number, y: number): void;
}
declare global {
	namespace PixiMixins {
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface Container extends IFederatedContainer {
		}
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface ContainerOptions extends FederatedOptions {
		}
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface ContainerEvents extends FederatedEventEmitterTypes {
		}
		interface RendererOptions {
			/**
			 * The type of interaction behavior for a Container. This is set via the {@link Container#eventMode} property.
			 * @example
			 * 
			 *
			 * Available modes:
			 * - `'none'`: Ignores all interaction events, even on its children
			 * - `'passive'`: **(default)** Does not emit events and ignores hit testing on itself and
			 * non-interactive children. Interactive children will still emit events.
			 * - `'auto'`: Does not emit events but is hit tested if parent is interactive.
			 * Same as `interactive = false` in v7
			 * - `'static'`: Emit events and is hit tested. Same as `interactive = true` in v7
			 * - `'dynamic'`: Emits events and is hit tested but will also receive mock interaction events fired from
			 * a ticker to allow for interaction when the mouse isn't moving
			 *
			 * Performance tips:
			 * - Use `'none'` for pure visual elements
			 * - Use `'passive'` for containers with some interactive children
			 * - Use `'static'` for standard buttons/controls
			 * - Use `'dynamic'` only for moving/animated interactive elements
			 * @since 7.2.0
			 */
			eventMode?: EventMode;
			/**
			 * Configuration for enabling/disabling specific event features.
			 * Use this to optimize performance by turning off unused functionality.
			 * @example
			 * 
			 * @since 7.2.0
			 */
			eventFeatures?: EventSystemOptions["eventFeatures"];
		}
		interface RendererSystems {
			events: EventSystem;
		}
	}
}
declare global {
	namespace PixiMixins {
		interface RendererSystems {
			filter: FilterSystem;
		}
		interface RendererPipes {
			filter: FilterPipe;
		}
	}
}
declare global {
	namespace PixiMixins {
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface Point extends Vector2Math {
		}
		// eslint-disable-next-line @typescript-eslint/no-empty-object-type
		interface ObservablePoint extends Vector2Math {
		}
		interface Rectangle {
			/**
			 * Accepts `other` Rectangle and returns true if the given Rectangle is equal to `this` Rectangle.
			 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
			 * @example
			 * 
			 * @param {Rectangle} other - The Rectangle to compare with `this`
			 * @returns {boolean} Returns true if all `x`, `y`, `width`, and `height` are equal.
			 */
			equals(other: Rectangle): boolean;
			/**
			 * If the area of the intersection between the Rectangles `other` and `this` is not zero,
			 * returns the area of intersection as a Rectangle object. Otherwise, return an empty Rectangle
			 * with its properties set to zero.
			 *
			 * Rectangles without area (width or height equal to zero) can't intersect or be intersected
			 * and will always return an empty rectangle with its properties set to zero.
			 *
			 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
			 * @example
			 * 
			 * @param {Rectangle} other - The Rectangle to intersect with `this`.
			 * @param {Rectangle} [outRect] - A Rectangle object in which to store the value,
			 * optional (otherwise will create a new Rectangle).
			 * @returns {Rectangle} The intersection of `this` and `other`.
			 */
			intersection<T extends Rectangle = Rectangle>(other: Rectangle, outRect?: T): T;
			/**
			 * Adds `this` and `other` Rectangles together to create a new Rectangle object filling
			 * the horizontal and vertical space between the two rectangles.
			 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
			 * @example
			 * 
			 * @param {Rectangle} other - The Rectangle to unite with `this`
			 * @param {Rectangle} [outRect] - Optional Rectangle to store the result
			 * @returns The union of `this` and `other`
			 */
			union<T extends Rectangle = Rectangle>(other: Rectangle, outRect?: T): T;
		}
	}
	interface Vector2Math {
		/**
		 * Adds `other` to `this` point and outputs into `outPoint` or a new Point.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @param {PointData} other - The point to add to `this`
		 * @param {PointData} [outPoint] - Optional Point-like object to store result
		 * @returns The outPoint or a new Point with addition result
		 */
		add<T extends PointData = Point>(other: PointData, outPoint?: T): T;
		/**
		 * Subtracts `other` from `this` point and outputs into `outPoint` or a new Point.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @param {PointData} other - The point to subtract from `this`
		 * @param {PointData} [outPoint] - Optional Point-like object to store result
		 * @returns The outPoint or a new Point with subtraction result
		 */
		subtract<T extends PointData = Point>(other: PointData, outPoint?: T): T;
		/**
		 * Multiplies component-wise `other` and `this` points and outputs into `outPoint` or a new Point.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @param {PointData} other - The point to multiply with `this`
		 * @param {PointData} [outPoint] - Optional Point-like object to store result
		 * @returns The outPoint or a new Point with multiplication result
		 */
		multiply<T extends PointData = Point>(other: PointData, outPoint?: T): T;
		/**
		 * Multiplies each component of `this` point with the number `scalar` and outputs into `outPoint` or a new Point.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @param {number} scalar - The number to multiply both components with
		 * @param {PointData} [outPoint] - Optional Point-like object to store result
		 * @returns The outPoint or a new Point with multiplication result
		 */
		multiplyScalar<T extends PointData = Point>(scalar: number, outPoint?: T): T;
		/**
		 * Computes the dot product of `other` with `this` point.
		 * The dot product is the sum of the products of the corresponding components of two vectors.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @param {PointData} other - The other point to calculate the dot product with
		 * @returns The scalar result of the dot product
		 */
		dot(other: PointData): number;
		/**
		 * Computes the cross product of `other` with `this` point.
		 * Returns the z-component of the 3D cross product, assuming z=0 for both vectors.
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @remarks
		 * - Returns z-component only (x,y assumed in 2D plane)
		 * - Positive result means counter-clockwise angle from this to other
		 * - Magnitude equals area of parallelogram formed by vectors
		 * @param {PointData} other - The other point to calculate the cross product with
		 * @returns The z-component of the cross product
		 */
		cross(other: PointData): number;
		/**
		 * Computes a normalized version of `this` point.
		 *
		 * A normalized vector is a vector of magnitude (length) 1
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @param {PointData} outPoint - Optional Point-like object to store result
		 * @returns The normalized point
		 */
		normalize<T extends PointData = Point>(outPoint?: T): T;
		/**
		 * Computes the magnitude (length) of this point as Euclidean distance from origin.
		 *
		 * Defined as the square root of the sum of the squares of each component.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @returns The magnitude (length) of the vector
		 */
		magnitude(): number;
		/**
		 * Computes the squared magnitude of this point.
		 * More efficient than magnitude() for length comparisons.
		 *
		 * Defined as the sum of the squares of each component.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @returns The squared magnitude of the vector
		 */
		magnitudeSquared(): number;
		/**
		 * Computes vector projection of `this` on `onto`.
		 * Projects one vector onto another, creating a parallel vector with the length of the projection.
		 *
		 * Imagine a light source, parallel to `onto`, above `this`.
		 * The light would cast rays perpendicular to `onto`.
		 * `this.project(onto)` is the shadow cast by `this` on the line defined by `onto` .
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @remarks
		 * - Results in zero vector if projecting onto zero vector
		 * - Length depends on angle between vectors
		 * - Result is parallel to `onto` vector
		 * - Useful for physics and collision responses
		 * @param {PointData} onto - Vector to project onto (should be non-zero)
		 * @param {PointData} [outPoint] - Optional Point-like object to store result
		 * @returns The projection of `this` onto `onto`
		 */
		project<T extends PointData = Point>(onto: PointData, outPoint?: T): T;
		/**
		 * Reflects `this` vector off of a plane orthogonal to `normal`.
		 *
		 * Like a light ray bouncing off a mirror surface.
		 * `this` vector is the light and `normal` is a vector perpendicular to the mirror.
		 * `this.reflect(normal)` is the reflection of `this` on that mirror.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @remarks
		 * - Normal vector should be normalized for accurate results
		 * - Preserves vector magnitude
		 * - Useful for physics simulations
		 * - Common in light/particle effects
		 * @param {PointData} normal - The normal vector of the reflecting plane
		 * @param {PointData} outPoint - Optional Point-like object to store result
		 * @returns The reflection of `this` off the plane
		 */
		reflect<T extends PointData = Point>(normal: PointData, outPoint?: T): T;
		/**
		 * Rotates `this` vector.
		 *
		 * Like a light ray bouncing off a mirror surface.
		 * `this` vector is the light and `normal` is a vector perpendicular to the mirror.
		 * `this.reflect(normal)` is the reflection of `this` on that mirror.
		 *
		 * > [!IMPORTANT] Only available with **pixi.js/math-extras**.
		 * @example
		 * 
		 * @remarks
		 * convert degrees to radians with const radians = degrees * (Math.PI / 180)
		 * @param {PointData} radians - The rotation angle in radians
		 * @param {PointData} outPoint - Optional Point-like object to store result
		 * @returns The outPoint or a new Point with rotated result
		 */
		rotate<T extends PointData = Point>(radians: number, outPoint?: T): T;
	}
}
/**
 * Data structure for points with optional radius.
 */
export type RoundedPoint = PointData & {
	radius?: number;
};
/**
 * The line cap styles for strokes.
 *
 * It can be:
 * - `butt`: The ends of the stroke are squared off at the endpoints.
 * - `round`: The ends of the stroke are rounded.
 */
export type LineCap = "butt" | "round" | "square";
/**
 * The line join styles for strokes.
 *
 * It can be:
 * - `round`: The corners of the stroke are rounded.
 * - `bevel`: The corners of the stroke are squared off.
 * - `miter`: The corners of the stroke are extended to meet at a point.
 */
export type LineJoin = "round" | "bevel" | "miter";
/**
 * Defines the type of gradient to create.
 *
 * It can be:
 * - 'linear': A linear gradient that transitions colors along a straight line.
 * - 'radial': A radial gradient that transitions colors in a circular pattern from an inner circle to an outer circle.
 */
export type GradientType = "linear" | "radial";
/**
 * Represents the style options for a linear gradient fill.
 */
export interface BaseGradientOptions {
	/** The type of gradient */
	type?: GradientType;
	/** Array of colors stops to use in the gradient */
	colorStops?: {
		offset: number;
		color: ColorSource;
	}[];
	/** Whether coordinates are 'global' or 'local' */
	textureSpace?: TextureSpace;
	/**
	 * The size of the texture to use for the gradient - this is for advanced usage.
	 * The texture size does not need to match the size of the object being drawn.
	 * Due to GPU interpolation, gradient textures can be relatively small!
	 * Consider using a larger texture size if your gradient has a lot of very tight color steps
	 */
	textureSize?: number;
	/**
	 * The wrap mode of the gradient.
	 * This can be 'clamp-to-edge' or 'repeat'.
	 * @default 'clamp-to-edge'
	 */
	wrapMode?: WRAP_MODE;
}
/**
 * Options specific to linear gradients.
 * A linear gradient creates a smooth transition between colors along a straight line defined by start and end points.
 */
export interface LinearGradientOptions extends BaseGradientOptions {
	/** The type of gradient. Must be 'linear' for linear gradients. */
	type?: "linear";
	/**
	 * The start point of the gradient.
	 * This point defines where the gradient begins.
	 * It is represented as a PointData object containing x and y coordinates.
	 * The coordinates are in local space by default (0-1), but can be in global space if specified.
	 */
	start?: PointData;
	/**
	 * The end point of the gradient.
	 * This point defines where the gradient ends.
	 * It is represented as a PointData object containing x and y coordinates.
	 * The coordinates are in local space by default (0-1), but can be in global space if specified.
	 */
	end?: PointData;
}
/**
 * Options specific to radial gradients.
 * A radial gradient creates a smooth transition between colors that radiates outward in a circular pattern.
 * The gradient is defined by inner and outer circles, each with their own radius.
 */
export interface RadialGradientOptions extends BaseGradientOptions {
	/** The type of gradient. Must be 'radial' for radial gradients. */
	type?: "radial";
	/** The center point of the inner circle where the gradient begins. In local coordinates by default (0-1). */
	center?: PointData;
	/** The radius of the inner circle where the gradient begins. */
	innerRadius?: number;
	/** The center point of the outer circle where the gradient ends. In local coordinates by default (0-1). */
	outerCenter?: PointData;
	/** The radius of the outer circle where the gradient ends. */
	outerRadius?: number;
	/**
	 * The y scale of the gradient, use this to make the gradient elliptical.
	 * NOTE: Only applied to radial gradients used with Graphics.
	 */
	scale?: number;
	/**
	 * The rotation of the gradient in radians, useful for making the gradient elliptical.
	 * NOTE: Only applied to radial gradients used with Graphics.
	 */
	rotation?: number;
}
/**
 * Options for creating a gradient fill.
 */
export type GradientOptions = LinearGradientOptions | RadialGradientOptions;
/**
 * Class representing a gradient fill that can be used to fill shapes and text.
 * Supports both linear and radial gradients with multiple color stops.
 *
 * For linear gradients, color stops define colors and positions (0 to 1) along a line from start point (x0,y0)
 * to end point (x1,y1).
 *
 * For radial gradients, color stops define colors between two circles - an inner circle centered at (x0,y0) with radius r0,
 * and an outer circle centered at (x1,y1) with radius r1.
 * @example
 * 
 *
 * Internally this creates a  texture of the gradient then applies a
 * transform to it to give it the correct size and angle.
 *
 * This means that it's important to destroy a gradient when it is no longer needed
 * to avoid memory leaks.
 *
 * If you want to animate a gradient then it's best to modify and update an existing one
 * rather than creating a whole new one each time. That or use a custom shader.
 */
export declare class FillGradient implements CanvasGradient {
	/** Default options for creating a gradient fill */
	static readonly defaultLinearOptions: LinearGradientOptions;
	/** Default options for creating a radial gradient fill */
	static readonly defaultRadialOptions: RadialGradientOptions;
	/** Type of gradient - currently only supports 'linear' */
	readonly type: GradientType;
	/** Internal texture used to render the gradient */
	texture: Texture;
	/** Transform matrix for positioning the gradient */
	transform: Matrix;
	/** Array of color stops defining the gradient */
	colorStops: Array<{
		offset: number;
		color: string;
	}>;
	/** Whether gradient coordinates are in local or global space */
	textureSpace: TextureSpace;
	/** The start point of the linear gradient */
	start: PointData;
	/** The end point of the linear gradient */
	end: PointData;
	/** The center point of the inner circle of the radial gradient */
	center: PointData;
	/** The center point of the outer circle of the radial gradient */
	outerCenter: PointData;
	/** The radius of the inner circle of the radial gradient */
	innerRadius: number;
	/** The radius of the outer circle of the radial gradient */
	outerRadius: number;
	/** The scale of the radial gradient */
	scale: number;
	/** The rotation of the radial gradient */
	rotation: number;
	/**
	 * Creates a new gradient fill. The constructor behavior changes based on the gradient type.
	 * @param {GradientOptions} options - The options for the gradient
	 */
	constructor(options: GradientOptions);
	/**
	 * Adds a color stop to the gradient
	 * @param offset - Position of the stop (0-1)
	 * @param color - Color of the stop
	 * @returns This gradient instance for chaining
	 */
	addColorStop(offset: number, color: ColorSource): this;
	/** Destroys the gradient, releasing resources. This will also destroy the internal texture. */
	destroy(): void;
	/**
	 * Returns a unique key for this gradient instance.
	 * This key is used for caching and texture management.
	 * @returns {string} Unique key for the gradient
	 */
	get styleKey(): string;
}
/**
 * Defines the repetition modes for fill patterns.
 *
 * - `repeat`: The pattern repeats in both directions.
 * - `repeat-x`: The pattern repeats horizontally only.
 * - `repeat-y`: The pattern repeats vertically only.
 * - `no-repeat`: The pattern does not repeat.
 */
export type PatternRepetition = "repeat" | "repeat-x" | "repeat-y" | "no-repeat";
/**
 * A class that represents a fill pattern for use in Text and Graphics fills.
 * It allows for textures to be used as patterns, with optional repetition modes.
 * @example
 * const txt = await Assets.load('https://pixijs.com/assets/bg_scene_rotate.jpg');
 * const pat = new FillPattern(txt, 'repeat');
 *
 * const textPattern = new Text({
 *     text: 'PixiJS',
 *     style: {
 *         fontSize: 36,
 *         fill: 0xffffff,
 *         stroke: { fill: pat, width: 10 },
 *     },
 * });
 *
 * textPattern.y = (textGradient.height);
 */
export declare class FillPattern implements CanvasPattern {
	/** The transform matrix applied to the pattern */
	transform: Matrix;
	constructor(texture: Texture, repetition?: PatternRepetition);
	/**
	 * Sets the transform for the pattern
	 * @param transform - The transform matrix to apply to the pattern.
	 * If not provided, the pattern will use the default transform.
	 */
	setTransform(transform?: Matrix): void;
	/** Internal texture used to render the gradient */
	get texture(): Texture;
	set texture(value: Texture);
	/**
	 * Returns a unique key for this instance.
	 * This key is used for caching.
	 * @returns {string} Unique key for the instance
	 */
	get styleKey(): string;
	/** Destroys the fill pattern, releasing resources. This will also destroy the internal texture. */
	destroy(): void;
}
/**
 * Defines the style properties used for filling shapes in graphics and text operations.
 * This interface provides options for colors, textures, patterns, and gradients.
 * @example
 * 
 */
export interface FillStyle {
	/**
	 * The color to use for the fill.
	 * This can be any valid color source, such as a hex value, a Color object, or a string.
	 * @example
	 * 
	 */
	color?: ColorSource;
	/**
	 * The alpha value to use for the fill.
	 * This value should be between 0 (fully transparent) and 1 (fully opaque).
	 * @example
	 * 
	 * @default 1
	 */
	alpha?: number;
	/**
	 * The texture to use for the fill.
	 * @example
	 * 
	 */
	texture?: Texture | null;
	/**
	 * The transformation matrix to apply to the fill pattern or texture.
	 * Used to scale, rotate, translate, or skew the fill.
	 * @example
	 * 
	 * @default null
	 */
	matrix?: Matrix | null;
	/**
	 * The fill pattern or gradient to use. This can be either a FillPattern for
	 * repeating textures or a FillGradient for color transitions.
	 * @example
	 * 
	 */
	fill?: FillPattern | FillGradient | null;
	/**
	 * Determines how texture coordinates are calculated across shapes.
	 * - 'local': Texture coordinates are relative to each shape's bounds
	 * - 'global': Texture coordinates are in world space
	 * @example
	 * 
	 * @default 'local'
	 */
	textureSpace?: TextureSpace;
}
/**
 * A stroke attribute object that defines how lines and shape outlines are drawn.
 * Controls properties like width, alignment, line caps, joins, and more.
 * @example
 * 
 */
export interface StrokeAttributes {
	/**
	 * The width of the stroke in pixels.
	 * @example
	 * 
	 * @default 1
	 */
	width?: number;
	/**
	 * The alignment of the stroke relative to the path.
	 * - 1: Inside the shape
	 * - 0.5: Centered on the path (default)
	 * - 0: Outside the shape
	 * @example
	 * 
	 * @default 0.5
	 */
	alignment?: number;
	/**
	 * The style to use for the ends of open paths.
	 * - 'butt': Ends at path end
	 * - 'round': Rounds past path end
	 * - 'square': Squares past path end
	 * @example
	 * 
	 * @default 'butt'
	 */
	cap?: LineCap;
	/**
	 * The style to use where paths connect.
	 * - 'miter': Sharp corner
	 * - 'round': Rounded corner
	 * - 'bevel': Beveled corner
	 * @example
	 * 
	 * @default 'miter'
	 */
	join?: LineJoin;
	/**
	 * Controls how far miter joins can extend. Only applies when join is 'miter'.
	 * Higher values allow sharper corners.
	 * @example
	 * 
	 * @default 10
	 */
	miterLimit?: number;
	/**
	 * When true, ensures crisp 1px lines by aligning to pixel boundaries.
	 * > [!NOTE] Only available for Graphics fills.
	 * @example
	 * 
	 * @default false
	 */
	pixelLine?: boolean;
}
/**
 * A stroke style object that combines fill properties with stroke attributes to define
 * both the visual style and stroke behavior of lines, shape outlines, and text strokes.
 * @example
 * 
 */
export interface StrokeStyle extends FillStyle, StrokeAttributes {
}
/**
 * These can be directly used as a fill or a stroke
 * 
 */
export type FillInput = ColorSource | FillGradient | FillPattern | FillStyle | Texture;
/**
 * These can be directly used as a stroke
 * 
 */
export type StrokeInput = ColorSource | FillGradient | FillPattern | StrokeStyle;
/**
 * @deprecated since v8.1.6
 */
export type FillStyleInputs = ColorSource | FillGradient | FillPattern | FillStyle | ConvertedFillStyle | StrokeStyle | ConvertedStrokeStyle;
/**
 * The GraphicsContext class allows for the creation of lightweight objects that contain instructions for drawing shapes and paths.
 * It is used internally by the Graphics class to draw shapes and paths, and can be used directly and shared between Graphics objects,
 *
 * This sharing of a `GraphicsContext` means that the intensive task of converting graphics instructions into GPU-ready geometry is done once, and the results are reused,
 * much like sprites reusing textures.
 */
export declare class GraphicsContext extends EventEmitter<{
	update: GraphicsContext;
	destroy: GraphicsContext;
}> {
	/** The default fill style to use when none is provided. */
	static defaultFillStyle: ConvertedFillStyle;
	/** The default stroke style to use when none is provided. */
	static defaultStrokeStyle: ConvertedStrokeStyle;
	/** The batch mode for this graphics context. It can be 'auto', 'batch', or 'no-batch'. */
	batchMode: BatchMode;
	/**
	 * Creates a new GraphicsContext object that is a clone of this instance, copying all properties,
	 * including the current drawing state, transformations, styles, and instructions.
	 * @returns A new GraphicsContext instance with the same properties and state as this one.
	 */
	clone(): GraphicsContext;
	/**
	 * The current fill style of the graphics context. This can be a color, gradient, pattern, or a more complex style defined by a FillStyle object.
	 */
	get fillStyle(): ConvertedFillStyle;
	set fillStyle(value: FillInput);
	/**
	 * The current stroke style of the graphics context. Similar to fill styles, stroke styles can encompass colors, gradients, patterns, or more detailed configurations via a StrokeStyle object.
	 */
	get strokeStyle(): ConvertedStrokeStyle;
	set strokeStyle(value: FillInput);
	/**
	 * Sets the current fill style of the graphics context. The fill style can be a color, gradient,
	 * pattern, or a more complex style defined by a FillStyle object.
	 * @param style - The fill style to apply. This can be a simple color, a gradient or pattern object,
	 *                or a FillStyle or ConvertedFillStyle object.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	setFillStyle(style: FillInput): this;
	/**
	 * Sets the current stroke style of the graphics context. Similar to fill styles, stroke styles can
	 * encompass colors, gradients, patterns, or more detailed configurations via a StrokeStyle object.
	 * @param style - The stroke style to apply. Can be defined as a color, a gradient or pattern,
	 *                or a StrokeStyle or ConvertedStrokeStyle object.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	setStrokeStyle(style: StrokeInput): this;
	/**
	 * Adds a texture to the graphics context. This method supports multiple overloads for specifying the texture.
	 * If only a texture is provided, it uses the texture's width and height for drawing.
	 * @param texture - The Texture object to use.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	texture(texture: Texture): this;
	/**
	 * Adds a texture to the graphics context. This method supports multiple overloads for specifying the texture,
	 * tint, and dimensions. If only a texture is provided, it uses the texture's width and height for drawing.
	 * Additional parameters allow for specifying a tint color, and custom dimensions for the texture drawing area.
	 * @param texture - The Texture object to use.
	 * @param tint - (Optional) A ColorSource to tint the texture. If not provided, defaults to white (0xFFFFFF).
	 * @param dx - (Optional) The x-coordinate in the destination canvas at which to place the top-left corner of
	 * the source image.
	 * @param dy - (Optional) The y-coordinate in the destination canvas at which to place the top-left corner of
	 * the source image.
	 * @param dw - (Optional) The width of the rectangle within the source image to draw onto the destination canvas.
	 * If not provided, uses the texture's frame width.
	 * @param dh - (Optional) The height of the rectangle within the source image to draw onto the destination canvas.
	 * If not provided, uses the texture's frame height.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	texture(texture: Texture, tint?: ColorSource, dx?: number, dy?: number, dw?: number, dh?: number): this;
	/**
	 * Resets the current path. Any previous path and its commands are discarded and a new path is
	 * started. This is typically called before beginning a new shape or series of drawing commands.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	beginPath(): this;
	/**
	 * Fills the current or given path with the current fill style. This method can optionally take
	 * a color and alpha for a simple fill, or a more complex FillInput object for advanced fills.
	 * @param style - (Optional) The style to fill the path with. Can be a color, gradient, pattern, or a complex style object. If omitted, uses the current fill style.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	fill(style?: FillInput): this;
	/** @deprecated 8.0.0 */
	fill(color: ColorSource, alpha: number): this;
	/**
	 * Strokes the current path with the current stroke style. This method can take an optional
	 * FillInput parameter to define the stroke's appearance, including its color, width, and other properties.
	 * @param style - (Optional) The stroke style to apply. Can be defined as a simple color or a more complex style object. If omitted, uses the current stroke style.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	stroke(style?: StrokeInput): this;
	/**
	 * Applies a cutout to the last drawn shape. This is used to create holes or complex shapes by
	 * subtracting a path from the previously drawn path. If a hole is not completely in a shape, it will
	 * fail to cut correctly!
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	cut(): this;
	/**
	 * Adds an arc to the current path, which is centered at (x, y) with the specified radius,
	 * starting and ending angles, and direction.
	 * @param x - The x-coordinate of the arc's center.
	 * @param y - The y-coordinate of the arc's center.
	 * @param radius - The arc's radius.
	 * @param startAngle - The starting angle, in radians.
	 * @param endAngle - The ending angle, in radians.
	 * @param counterclockwise - (Optional) Specifies whether the arc is drawn counterclockwise (true) or clockwise (false). Defaults to false.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	arc(x: number, y: number, radius: number, startAngle: number, endAngle: number, counterclockwise?: boolean): this;
	/**
	 * Adds an arc to the current path with the given control points and radius, connected to the previous point
	 * by a straight line if necessary.
	 * @param x1 - The x-coordinate of the first control point.
	 * @param y1 - The y-coordinate of the first control point.
	 * @param x2 - The x-coordinate of the second control point.
	 * @param y2 - The y-coordinate of the second control point.
	 * @param radius - The arc's radius.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	arcTo(x1: number, y1: number, x2: number, y2: number, radius: number): this;
	/**
	 * Adds an SVG-style arc to the path, allowing for elliptical arcs based on the SVG spec.
	 * @param rx - The x-radius of the ellipse.
	 * @param ry - The y-radius of the ellipse.
	 * @param xAxisRotation - The rotation of the ellipse's x-axis relative
	 * to the x-axis of the coordinate system, in degrees.
	 * @param largeArcFlag - Determines if the arc should be greater than or less than 180 degrees.
	 * @param sweepFlag - Determines if the arc should be swept in a positive angle direction.
	 * @param x - The x-coordinate of the arc's end point.
	 * @param y - The y-coordinate of the arc's end point.
	 * @returns The instance of the current object for chaining.
	 */
	arcToSvg(rx: number, ry: number, xAxisRotation: number, largeArcFlag: number, sweepFlag: number, x: number, y: number): this;
	/**
	 * Adds a cubic Bezier curve to the path.
	 * It requires three points: the first two are control points and the third one is the end point.
	 * The starting point is the last point in the current path.
	 * @param cp1x - The x-coordinate of the first control point.
	 * @param cp1y - The y-coordinate of the first control point.
	 * @param cp2x - The x-coordinate of the second control point.
	 * @param cp2y - The y-coordinate of the second control point.
	 * @param x - The x-coordinate of the end point.
	 * @param y - The y-coordinate of the end point.
	 * @param smoothness - Optional parameter to adjust the smoothness of the curve.
	 * @returns The instance of the current object for chaining.
	 */
	bezierCurveTo(cp1x: number, cp1y: number, cp2x: number, cp2y: number, x: number, y: number, smoothness?: number): this;
	/**
	 * Closes the current path by drawing a straight line back to the start.
	 * If the shape is already closed or there are no points in the path, this method does nothing.
	 * @returns The instance of the current object for chaining.
	 */
	closePath(): this;
	/**
	 * Draws an ellipse at the specified location and with the given x and y radii.
	 * An optional transformation can be applied, allowing for rotation, scaling, and translation.
	 * @param x - The x-coordinate of the center of the ellipse.
	 * @param y - The y-coordinate of the center of the ellipse.
	 * @param radiusX - The horizontal radius of the ellipse.
	 * @param radiusY - The vertical radius of the ellipse.
	 * @returns The instance of the current object for chaining.
	 */
	ellipse(x: number, y: number, radiusX: number, radiusY: number): this;
	/**
	 * Draws a circle shape. This method adds a new circle path to the current drawing.
	 * @param x - The x-coordinate of the center of the circle.
	 * @param y - The y-coordinate of the center of the circle.
	 * @param radius - The radius of the circle.
	 * @returns The instance of the current object for chaining.
	 */
	circle(x: number, y: number, radius: number): this;
	/**
	 * Adds another `GraphicsPath` to this path, optionally applying a transformation.
	 * @param path - The `GraphicsPath` to add.
	 * @returns The instance of the current object for chaining.
	 */
	path(path: GraphicsPath): this;
	/**
	 * Connects the current point to a new point with a straight line. This method updates the current path.
	 * @param x - The x-coordinate of the new point to connect to.
	 * @param y - The y-coordinate of the new point to connect to.
	 * @returns The instance of the current object for chaining.
	 */
	lineTo(x: number, y: number): this;
	/**
	 * Sets the starting point for a new sub-path. Any subsequent drawing commands are considered part of this path.
	 * @param x - The x-coordinate for the starting point.
	 * @param y - The y-coordinate for the starting point.
	 * @returns The instance of the current object for chaining.
	 */
	moveTo(x: number, y: number): this;
	/**
	 * Adds a quadratic curve to the path. It requires two points: the control point and the end point.
	 * The starting point is the last point in the current path.
	 * @param cpx - The x-coordinate of the control point.
	 * @param cpy - The y-coordinate of the control point.
	 * @param x - The x-coordinate of the end point.
	 * @param y - The y-coordinate of the end point.
	 * @param smoothness - Optional parameter to adjust the smoothness of the curve.
	 * @returns The instance of the current object for chaining.
	 */
	quadraticCurveTo(cpx: number, cpy: number, x: number, y: number, smoothness?: number): this;
	/**
	 * Draws a rectangle shape. This method adds a new rectangle path to the current drawing.
	 * @param x - The x-coordinate of the top-left corner of the rectangle.
	 * @param y - The y-coordinate of the top-left corner of the rectangle.
	 * @param w - The width of the rectangle.
	 * @param h - The height of the rectangle.
	 * @returns The instance of the current object for chaining.
	 */
	rect(x: number, y: number, w: number, h: number): this;
	/**
	 * Draws a rectangle with rounded corners.
	 * The corner radius can be specified to determine how rounded the corners should be.
	 * An optional transformation can be applied, which allows for rotation, scaling, and translation of the rectangle.
	 * @param x - The x-coordinate of the top-left corner of the rectangle.
	 * @param y - The y-coordinate of the top-left corner of the rectangle.
	 * @param w - The width of the rectangle.
	 * @param h - The height of the rectangle.
	 * @param radius - The radius of the rectangle's corners. If not specified, corners will be sharp.
	 * @returns The instance of the current object for chaining.
	 */
	roundRect(x: number, y: number, w: number, h: number, radius?: number): this;
	/**
	 * Draws a polygon shape by specifying a sequence of points. This method allows for the creation of complex polygons,
	 * which can be both open and closed. An optional transformation can be applied, enabling the polygon to be scaled,
	 * rotated, or translated as needed.
	 * @param points - An array of numbers, or an array of PointData objects eg [{x,y}, {x,y}, {x,y}]
	 * representing the x and y coordinates, of the polygon's vertices, in sequence.
	 * @param close - A boolean indicating whether to close the polygon path. True by default.
	 */
	poly(points: number[] | PointData[], close?: boolean): this;
	/**
	 * Draws a regular polygon with a specified number of sides. All sides and angles are equal.
	 * @param x - The x-coordinate of the center of the polygon.
	 * @param y - The y-coordinate of the center of the polygon.
	 * @param radius - The radius of the circumscribed circle of the polygon.
	 * @param sides - The number of sides of the polygon. Must be 3 or more.
	 * @param rotation - The rotation angle of the polygon, in radians. Zero by default.
	 * @param transform - An optional `Matrix` object to apply a transformation to the polygon.
	 * @returns The instance of the current object for chaining.
	 */
	regularPoly(x: number, y: number, radius: number, sides: number, rotation?: number, transform?: Matrix): this;
	/**
	 * Draws a polygon with rounded corners.
	 * Similar to `regularPoly` but with the ability to round the corners of the polygon.
	 * @param x - The x-coordinate of the center of the polygon.
	 * @param y - The y-coordinate of the center of the polygon.
	 * @param radius - The radius of the circumscribed circle of the polygon.
	 * @param sides - The number of sides of the polygon. Must be 3 or more.
	 * @param corner - The radius of the rounding of the corners.
	 * @param rotation - The rotation angle of the polygon, in radians. Zero by default.
	 * @returns The instance of the current object for chaining.
	 */
	roundPoly(x: number, y: number, radius: number, sides: number, corner: number, rotation?: number): this;
	/**
	 * Draws a shape with rounded corners. This function supports custom radius for each corner of the shape.
	 * Optionally, corners can be rounded using a quadratic curve instead of an arc, providing a different aesthetic.
	 * @param points - An array of `RoundedPoint` representing the corners of the shape to draw.
	 * A minimum of 3 points is required.
	 * @param radius - The default radius for the corners.
	 * This radius is applied to all corners unless overridden in `points`.
	 * @param useQuadratic - If set to true, rounded corners are drawn using a quadraticCurve
	 *  method instead of an arc method. Defaults to false.
	 * @param smoothness - Specifies the smoothness of the curve when `useQuadratic` is true.
	 * Higher values make the curve smoother.
	 * @returns The instance of the current object for chaining.
	 */
	roundShape(points: RoundedPoint[], radius: number, useQuadratic?: boolean, smoothness?: number): this;
	/**
	 * Draw Rectangle with fillet corners. This is much like rounded rectangle
	 * however it support negative numbers as well for the corner radius.
	 * @param x - Upper left corner of rect
	 * @param y - Upper right corner of rect
	 * @param width - Width of rect
	 * @param height - Height of rect
	 * @param fillet - accept negative or positive values
	 */
	filletRect(x: number, y: number, width: number, height: number, fillet: number): this;
	/**
	 * Draw Rectangle with chamfer corners. These are angled corners.
	 * @param x - Upper left corner of rect
	 * @param y - Upper right corner of rect
	 * @param width - Width of rect
	 * @param height - Height of rect
	 * @param chamfer - non-zero real number, size of corner cutout
	 * @param transform
	 */
	chamferRect(x: number, y: number, width: number, height: number, chamfer: number, transform?: Matrix): this;
	/**
	 * Draws a star shape centered at a specified location. This method allows for the creation
	 *  of stars with a variable number of points, outer radius, optional inner radius, and rotation.
	 * The star is drawn as a closed polygon with alternating outer and inner vertices to create the star's points.
	 * An optional transformation can be applied to scale, rotate, or translate the star as needed.
	 * @param x - The x-coordinate of the center of the star.
	 * @param y - The y-coordinate of the center of the star.
	 * @param points - The number of points of the star.
	 * @param radius - The outer radius of the star (distance from the center to the outer points).
	 * @param innerRadius - Optional. The inner radius of the star
	 * (distance from the center to the inner points between the outer points).
	 * If not provided, defaults to half of the `radius`.
	 * @param rotation - Optional. The rotation of the star in radians, where 0 is aligned with the y-axis.
	 * Defaults to 0, meaning one point is directly upward.
	 * @returns The instance of the current object for chaining further drawing commands.
	 */
	star(x: number, y: number, points: number, radius: number, innerRadius?: number, rotation?: number): this;
	/**
	 * Parses and renders an SVG string into the graphics context. This allows for complex shapes and paths
	 * defined in SVG format to be drawn within the graphics context.
	 * @param svg - The SVG string to be parsed and rendered.
	 */
	svg(svg: string): this;
	/**
	 * Restores the most recently saved graphics state by popping the top of the graphics state stack.
	 * This includes transformations, fill styles, and stroke styles.
	 */
	restore(): this;
	/** Saves the current graphics state, including transformations, fill styles, and stroke styles, onto a stack. */
	save(): this;
	/**
	 * Returns the current transformation matrix of the graphics context.
	 * @returns The current transformation matrix.
	 */
	getTransform(): Matrix;
	/**
	 * Resets the current transformation matrix to the identity matrix, effectively removing any transformations (rotation, scaling, translation) previously applied.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	resetTransform(): this;
	/**
	 * Applies a rotation transformation to the graphics context around the current origin.
	 * @param angle - The angle of rotation in radians.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	rotate(angle: number): this;
	/**
	 * Applies a scaling transformation to the graphics context, scaling drawings by x horizontally and by y vertically.
	 * @param x - The scale factor in the horizontal direction.
	 * @param y - (Optional) The scale factor in the vertical direction. If not specified, the x value is used for both directions.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	scale(x: number, y?: number): this;
	/**
	 * Sets the current transformation matrix of the graphics context to the specified matrix or values.
	 * This replaces the current transformation matrix.
	 * @param transform - The matrix to set as the current transformation matrix.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	setTransform(transform: Matrix): this;
	/**
	 * Sets the current transformation matrix of the graphics context to the specified matrix or values.
	 * This replaces the current transformation matrix.
	 * @param a - The value for the a property of the matrix, or a Matrix object to use directly.
	 * @param b - The value for the b property of the matrix.
	 * @param c - The value for the c property of the matrix.
	 * @param d - The value for the d property of the matrix.
	 * @param dx - The value for the tx (translate x) property of the matrix.
	 * @param dy - The value for the ty (translate y) property of the matrix.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	setTransform(a: number, b: number, c: number, d: number, dx: number, dy: number): this;
	/**
	 * Applies the specified transformation matrix to the current graphics context by multiplying
	 * the current matrix with the specified matrix.
	 * @param transform - The matrix to apply to the current transformation.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	transform(transform: Matrix): this;
	/**
	 * Applies the specified transformation matrix to the current graphics context by multiplying
	 * the current matrix with the specified matrix.
	 * @param a - The value for the a property of the matrix, or a Matrix object to use directly.
	 * @param b - The value for the b property of the matrix.
	 * @param c - The value for the c property of the matrix.
	 * @param d - The value for the d property of the matrix.
	 * @param dx - The value for the tx (translate x) property of the matrix.
	 * @param dy - The value for the ty (translate y) property of the matrix.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	transform(a: number, b: number, c: number, d: number, dx: number, dy: number): this;
	/**
	 * Applies a translation transformation to the graphics context, moving the origin by the specified amounts.
	 * @param x - The amount to translate in the horizontal direction.
	 * @param y - (Optional) The amount to translate in the vertical direction. If not specified, the x value is used for both directions.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	translate(x: number, y?: number): this;
	/**
	 * Clears all drawing commands from the graphics context, effectively resetting it. This includes clearing the path,
	 * and optionally resetting transformations to the identity matrix.
	 * @returns The instance of the current GraphicsContext for method chaining.
	 */
	clear(): this;
	/** The bounds of the graphic shape. */
	get bounds(): Bounds;
	/**
	 * Check to see if a point is contained within this geometry.
	 * @param point - Point to check if it's contained.
	 * @returns {boolean} `true` if the point is contained within geometry.
	 */
	containsPoint(point: PointData): boolean;
	/**
	 * Destroys the GraphicsData object.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * context.destroy();
	 * context.destroy(true);
	 * context.destroy({ texture: true, textureSource: true });
	 */
	destroy(options?: TypeOrBool<TextureDestroyOptions>): void;
}
/**
 * The alignment of the text.
 *
 * - 'left': Aligns text to the left edge.
 * - 'center': Centers text horizontally.
 * - 'right': Aligns text to the right edge.
 * - 'justify': Justifies text, aligning both left and right edges.
 * @example
 * 
 */
export type TextStyleAlign = "left" | "center" | "right" | "justify";
/**
 * The fill style input for text styles.
 *
 * This can be:
 * - A color string like 'red', '#00FF00', or 'rgba(255,0,0,0.5)'
 * - A hex number like 0xff0000 for red
 * - A FillStyle object with properties like { color: 0xff0000, alpha: 0.5 }
 * - A FillGradient for gradient fills
 * - A FillPattern for pattern/texture fills
 * @example
 * 
 */
export type TextStyleFill = string | string[] | number | number[] | CanvasGradient | CanvasPattern;
/**
 * The font style input for text styles. Controls the slant or italicization of the text.
 * @example
 * 
 *
 * Supported values:
 * - 'normal': Regular upright text with no slant
 * - 'italic': True italics using specifically designed italic glyphs
 * - 'oblique': Slanted version of the regular glyphs
 * @remarks
 * - 'italic' uses specially designed glyphs with cursive characteristics
 * - 'oblique' is a mechanical slant of the normal glyphs
 * - Not all fonts include true italic designs; some may fall back to oblique
 */
export type TextStyleFontStyle = "normal" | "italic" | "oblique";
/**
 * The font variant input for text styles. Controls the capitalization and presentation of letters.
 * Used to enable special rendering like small caps.
 * @example
 * 
 *
 * Supported values:
 * - 'normal': Regular text rendering with standard capitalization
 * - 'small-caps': Renders lowercase letters as smaller versions of capital letters
 * @remarks
 * Small caps are only available if the font supports them.
 * Not all fonts include true small caps glyphs.
 */
export type TextStyleFontVariant = "normal" | "small-caps";
/**
 * The font weight input for text styles. Controls the thickness or boldness of the text.
 * @example
 * 
 *
 * Supported values:
 * - 'normal': Standard weight (equivalent to 400)
 * - 'bold': Bold weight (equivalent to 700)
 * - 'bolder': One weight darker than the parent element
 * - 'lighter': One weight lighter than the parent element
 * - '100': Thin (Hairline)
 * - '200': Extra Light (Ultra Light)
 * - '300': Light
 * - '400': Normal
 * - '500': Medium
 * - '600': Semi Bold (Demi Bold)
 * - '700': Bold
 * - '800': Extra Bold (Ultra Bold)
 * - '900': Heavy (Black)
 */
export type TextStyleFontWeight = "normal" | "bold" | "bolder" | "lighter" | "100" | "200" | "300" | "400" | "500" | "600" | "700" | "800" | "900";
/**
 * The line join style for text strokes. Determines how lines connect at corners.
 * @example
 * 
 * Available values:
 * - 'miter': Creates sharp corners by extending the outer edges until they meet
 * - 'round': Creates smooth, rounded corners using a circular arc
 * - 'bevel': Creates flattened corners by filling an additional triangle between the outer edges
 */
export type TextStyleLineJoin = "miter" | "round" | "bevel";
/**
 * The text baseline for text styles.
 *
 * This can be:
 * - 'alphabetic': The alphabetic baseline
 * - 'top': The top of the text
 * - 'hanging': The hanging baseline
 * - 'middle': The middle of the text
 * - 'ideographic': The ideographic baseline
 * - 'bottom': The bottom of the text
 */
export type TextStyleTextBaseline = "alphabetic" | "top" | "hanging" | "middle" | "ideographic" | "bottom";
/**
 * Controls how whitespace (spaces, tabs, and line breaks) is handled within the text.
 * This affects text wrapping and spacing behavior.
 * @example
 * 
 *
 * Supported values:
 * - 'normal': Collapses all whitespace (spaces, tabs, line breaks) into a single space
 * - 'pre': Preserves all whitespace characters exactly as written
 * - 'pre-line': Preserves line breaks but collapses multiple spaces into a single space
 * @remarks
 * - 'normal' is best for single-line text or when you want to ignore formatting
 * - 'pre' is useful for code blocks or when exact spacing is important
 * - 'pre-line' is good for formatted text where you want to keep line breaks but clean up spaces
 */
export type TextStyleWhiteSpace = "normal" | "pre" | "pre-line";
/**
 * Defines a drop shadow effect for text rendering.
 * Drop shadows add depth and emphasis to text by creating a shadow offset from the text.
 * @example
 * 
 */
export type TextDropShadow = {
	/**
	 * The opacity of the drop shadow.
	 * - Range: 0 to 1
	 * - 0 = fully transparent
	 * - 1 = fully opaque
	 * @example
	 * 
	 * @default 1
	 */
	alpha: number;
	/**
	 * The angle of the drop shadow in radians.
	 * - 0 = right
	 * - Math.PI/2 = down
	 * - Math.PI = left
	 * - Math.PI*1.5 = up
	 * @example
	 * 
	 * @default Math.PI/6 (30 degrees)
	 */
	angle: number;
	/**
	 * The blur radius of the shadow.
	 * - 0 = sharp shadow
	 * - Higher values = softer shadow
	 * @example
	 * 
	 * @default 0
	 */
	blur: number;
	/**
	 * The color of the drop shadow.
	 * Accepts any valid CSS color string, hex number, or RGB/RGBA values.
	 * @example '#000000', 'rgba(0,0,0,0.5)', 0x000000
	 * @default 'black'
	 */
	color: ColorSource;
	/**
	 * The distance of the drop shadow from the text.
	 * Measured in pixels.
	 * @example
	 * 
	 * @default 5
	 */
	distance: number;
};
/**
 * Constructor options used for `TextStyle` instances. Defines the visual appearance and layout of text.
 * @example
 * 
 */
export interface TextStyleOptions {
	/**
	 * Alignment for multiline text, does not affect single line text
	 * @default 'left'
	 */
	align?: TextStyleAlign;
	/**
	 * Whether to allow line breaks within words.
	 * Requires wordWrap to be true.
	 * @example
	 * 
	 * @default false
	 */
	breakWords?: boolean;
	/**
	 * Drop shadow configuration for the text.
	 * Can be boolean or a TextDropShadow object.
	 * @default null
	 */
	dropShadow?: boolean | Partial<TextDropShadow>;
	/**
	 * Fill style for the text.
	 * Can be a color, gradient, or pattern.
	 * @default 'black'
	 */
	fill?: FillInput;
	/**
	 * Font family or families to use.
	 * Can be single name or array of fallbacks.
	 * @example
	 * 
	 * @default 'Arial'
	 */
	fontFamily?: string | string[];
	/**
	 * Font size in pixels or as string.
	 *
	 * Equivalents are '26px','20pt','160%' or '1.6em')
	 * @example
	 * ts
 * // Create a basic text style
 * const style = new TextStyle({
 *     fontFamily: ['Helvetica', 'Arial', 'sans-serif'],
 *     fontSize: 36,
 *     fill: 0xff1010,
 *     align: 'center'
 * });
 *
 * // Create a rich text style with multiple features
 * const richStyle = new TextStyle({
 *     fontFamily: 'Arial',
 *     fontSize: 32,
 *     fill: 'white',
 *     stroke: {
 *         color: '#4a1850',
 *         width: 5
 *     },
 *     dropShadow: {
 *         color: '#000000',
 *         blur: 4,
 *         distance: 6,
 *         angle: Math.PI / 6
 *     },
 *     wordWrap: true,
 *     wordWrapWidth: 440,
 *     lineHeight: 40,
 *     align: 'center'
 * });
 *
 * // Share style between multiple text objects
 * const text1 = new Text({
 *     text: 'Hello',
 *     style: richStyle
 * });
 *
 * const text2 = new Text({
 *     text: 'World',
 *     style: richStyle
 * });
 *
 * // Update style dynamically - affects all text objects
 * richStyle.fontSize = 48;
 * richStyle.fill = 0x00ff00;
 * ts
	 * // Customize default settings globally
	 * TextStyle.defaultDropShadow.alpha = 0.5;    // 50% opacity for all shadows
	 * TextStyle.defaultDropShadow.blur = 2;       // 2px blur for all shadows
	 * TextStyle.defaultDropShadow.color = 'blue'; // Blue shadows by default
	 * ts
	 * // Customize default text style globally
	 * TextStyle.defaultTextStyle.fontSize = 16;
	 * TextStyle.defaultTextStyle.fill = 0x333333;
	 * TextStyle.defaultTextStyle.fontFamily = ['Arial', 'Helvetica', 'sans-serif'];
	 * ts
 * // Basic HTML text style
 * const text = new HTMLText({
 *     text: '<p>Hello World</p>',
 *     style: {
 *         fontSize: 24,
 *         fill: '#ff0000',
 *         fontFamily: 'Arial',
 *         align: 'center'
 *     }
 * });
 *
 * // Custom tag styling
 * const taggedText = new HTMLText({
 *     text: '<custom>Custom Tag</custom>',
 *     style: {
 *         fontSize: 16,
 *         tagStyles: {
 *             custom: {
 *                 fontSize: 32,
 *                 fill: '#00ff00',
 *                 fontStyle: 'italic'
 *             }
 *         }
 *     }
 * });
 * ts
	 * const text = new HTMLText({
	 *     text: `
	 *         <red>Main Title</red>
	 *         <grey>The subtitle</grey>
	 *         <blue>Regular content text</blue>
	 *     `,
	 *     style: {
	 *         tagStyles: {
	 *             red: {
	 *                 fill: '#ff0000',
	 *             },
	 *             grey: {
	 *                 fill: '#666666',
	 *             },
	 *             blue: {
	 *                 fill: 'blue',
	 *             }
	 *         }
	 *     }
	 * });
	 * ts
	 * // Create original style
	 * const originalStyle = new HTMLTextStyle({
	 *     fontSize: 24,
	 *     fill: '#ff0000',
	 *     tagStyles: {
	 *         header: { fontSize: 32, fill: '#00ff00' }
	 *     }
	 * });
	 *
	 * // Clone the style
	 * const clonedStyle = originalStyle.clone();
	 *
	 * // Modify cloned style independently
	 * clonedStyle.fontSize = 36;
	 * clonedStyle.fill = '#0000ff';
	 *
	 * // Original style remains unchanged
	 * console.log(originalStyle.fontSize); // Still 24
	 * console.log(originalStyle.fill); // Still '#ff0000'
	 * ts
	 * // Using hex colors
	 * const text = new HTMLText({
	 *     text: 'Colored Text',
	 *     style: {
	 *         fill: 0xff0000 // Red color
	 *     }
	 * });
	 *
	 * // Using CSS color strings
	 * text.style.fill = '#00ff00';     // Hex string (Green)
	 * text.style.fill = 'blue';        // Named color
	 * text.style.fill = 'rgb(255,0,0)' // RGB
	 * text.style.fill = '#f0f';        // Short hex
	 *
	 * // Invalid usage (will trigger warning in debug)
	 * text.style.fill = {
	 *     type: 'pattern',
	 *     texture: Texture.from('pattern.png')
	 * }; // Not supported, falls back to default
	 * ts
	 * // Using hex colors
	 * const text = new HTMLText({
	 *     text: 'Outlined Text',
	 *     style: {
	 *         stroke: 0xff0000 // Red outline
	 *     }
	 * });
	 *
	 * // Using CSS color strings
	 * text.style.stroke = '#00ff00';     // Hex string (Green)
	 * text.style.stroke = 'blue';        // Named color
	 * text.style.stroke = 'rgb(255,0,0)' // RGB
	 * text.style.stroke = '#f0f';        // Short hex
	 *
	 * // Using stroke width
	 * text.style = {
	 *     stroke: {
	 *         color: '#ff0000',
	 *         width: 2
	 *     }
	 * };
	 *
	 * // Remove stroke
	 * text.style.stroke = null;
	 *
	 * // Invalid usage (will trigger warning in debug)
	 * text.style.stroke = {
	 *     type: 'pattern',
	 *     texture: Texture.from('pattern.png')
	 * }; // Not supported, falls back to default
	 * ts
 * const text: TextString = 'Hello Pixi!';
 * const text2: TextString = 12345;
 * const text3: TextString = { toString: () => 'Hello Pixi!' };
 * ts
 * import { TextStyle, HTMLTextStyle } from 'pixi.js';
 * const style: AnyTextStyle = new TextStyle({ fontSize: 24 });
 * const htmlStyle: AnyTextStyle = new HTMLTextStyle({ fontSize: '24px' });
 * ts
 * import { TextStyleOptions, HTMLTextStyleOptions } from 'pixi.js';
 * const styleOptions: AnyTextStyleOptions = { fontSize: 24 } as TextStyleOptions;
 * const htmlStyleOptions: AnyTextStyleOptions = { fontSize: '24px' } as HTMLTextStyleOptions;
 * ts
 * // Create basic text with minimal options
 * const basicText = new Text({
 *     text: 'Hello Pixi!',
 *     style: {
 *         fontSize: 24,
 *         fill: 0xff1010
 *     }
 * });
 *
 * // Create text with advanced styling
 * const styledText = new Text({
 *     text: 'Styled Text',
 *     style: {
 *         fontFamily: 'Arial',
 *         fontSize: 32,
 *         fill: new FillGradient({
 *             end: { x: 1, y: 1 },
 *             stops: [
 *                 { color: 0xff0000, offset: 0 }, // Red at start
 *                 { color: 0x0000ff, offset: 1 }, // Blue at end
 *             ]
 *         }),
 *         stroke: { color: '#4a1850', width: 5 },
 *         dropShadow: {
 *             color: '#000000',
 *             blur: 4,
 *             distance: 6
 *         },
 *         align: 'center'
 *     },
 *     anchor: 0.5,
 *     resolution: window.devicePixelRatio
 * });
 *
 * // Create multiline text with word wrap
 * const wrappedText = new Text({
 *     text: 'This is a long piece of text that will wrap onto multiple lines',
 *     style: {
 *         fontSize: 20,
 *         wordWrap: true,
 *         wordWrapWidth: 200,
 *         lineHeight: 30
 *     },
 *     resolution: 2,
 *     roundPixels: true
 * });
 * ts
	 * // Set anchor to center
	 * const text = new Text({
	 *     text: 'Hello Pixi!',
	 *     anchor: 0.5 // Same as { x: 0.5, y: 0.5 }
	 * });
	 * // Set anchor to top-left
	 * const text2 = new Text({
	 *     text: 'Hello Pixi!',
	 *     anchor: { x: 0, y: 0 } // Top-left corner
	 * });
	 * // Set anchor to bottom-right
	 * const text3 = new Text({
	 *     text: 'Hello Pixi!',
	 *     anchor: { x: 1, y: 1 } // Bottom-right corner
	 * });
	 * ts
	 * const text = new Text({
	 *     text: 'Hello Pixi!',
	 * });
	 * const multilineText = new Text({
	 *     text: 'Line 1\nLine 2\nLine 3',
	 * });
	 * const numberText = new Text({
	 *     text: 12345, // Will be converted to '12345'
	 * });
	 * const objectText = new Text({
	 *     text: { toString: () => 'Object Text' }, // Custom toString
	 * });
	 * ts
	 * const text = new Text({
	 *     text: 'Hello Pixi!',
	 *     resolution: 2 // High DPI for sharper text
	 * });
	 * const autoResText = new Text({
	 *     text: 'Auto Resolution',
	 *     resolution: null // Use device's pixel ratio
	 * });
	 * ts
	 * const text = new Text({
	 *     text: 'Styled Text',
	 *     style: {
	 *         fontSize: 24,
	 *         fill: 0xff1010, // Red color
	 *         fontFamily: 'Arial',
	 *         align: 'center', // Center alignment
	 *         stroke: { color: '#4a1850', width: 5 }, // Purple stroke
	 *         dropShadow: {
	 *             color: '#000000', // Black shadow
	 *             blur: 4, // Shadow blur
	 *             distance: 6 // Shadow distance
	 *         }
	 *     }
	 * });
	 * const htmlText = new HTMLText({
	 *     text: 'HTML Styled Text',
	 *     style: {
	 *         fontSize: '20px',
	 *         fill: 'blue',
	 *         fontFamily: 'Verdana',
	 *     }
	 * });
	 * const bitmapText = new BitmapText({
	 *     text: 'Bitmap Styled Text',
	 *     style: {
	 *         fontName: 'Arial',
	 *         fontSize: 32,
	 *     }
	 * })
	 */
	style?: TEXT_STYLE | TEXT_STYLE_OPTIONS;
	/**
	 * Whether to round the x/y position to whole pixels.
	 * Enabling can prevent anti-aliasing of text edges but may cause slight position shifting.
	 * @example
	 * ts
 * // Create basic canvas text
 * const text = new Text({
 *     text: 'Hello Pixi!',
 *     style: {
 *         fontSize: 24,
 *         fill: 0xff1010,
 *     }
 * });
 *
 * // Create text with custom texture style
 * const customText = new Text({
 *     text: 'Custom Text',
 *     style: {
 *         fontSize: 32,
 *         fill: 0x4a4a4a
 *     },
 *     textureStyle: {
 *         scaleMode: 'nearest',
 *     }
 * });
 * ts
 * import { Text } from 'pixi.js';
 *
 * // Basic text creation
 * const basicText = new Text({
 *     text: 'Hello Pixi!',
 *     style: {
 *         fontFamily: 'Arial',
 *         fontSize: 24,
 *         fill: 0xff1010,
 *         align: 'center',
 *     }
 * });
 *
 * // Rich text with multiple styles
 * const richText = new Text({
 *     text: 'Styled\nMultiline\nText',
 *     style: {
 *         fontFamily: 'Arial',
 *         fontSize: 36,
 *         fill: 'red',
 *         stroke: { color: '#4a1850', width: 5 },
 *         align: 'center',
 *         lineHeight: 45,
 *         dropShadow: {
 *             color: '#000000',
 *             blur: 4,
 *             distance: 6,
 *         }
 *     },
 *     anchor: 0.5,
 * });
 *
 * // Text with custom texture settings
 * const crispText = new Text({
 *     text: 'High Quality Text',
 *     style: {
 *         fontSize: 24,
 *         fill: 0x4a4a4a,
 *     },
 *     textureStyle: {
 *         scaleMode: 'nearest',
 *     }
 * });
 *
 * // Word-wrapped text
 * const wrappedText = new Text({
 *     text: 'This is a long piece of text that will automatically wrap to multiple lines',
 *     style: {
 *         fontSize: 20,
 *         wordWrap: true,
 *         wordWrapWidth: 200,
 *         lineHeight: 30,
 *     }
 * });
 * ts
 * const graphics = new Graphics({
 *     roundPixels: true,
 *     position: { x: 100.5, y: 100.5 }
 * });
 *
 * // Reuse graphics context
 * const sharedContext = new GraphicsContext();
 * const graphics1 = new Graphics({ context: sharedContext });
 * const graphics2 = new Graphics({ context: sharedContext });
 * ts
	 * const sharedContext = new GraphicsContext();
	 * const graphics1 = new Graphics({ context: sharedContext });
	 * const graphics2 = new Graphics({ context: sharedContext });
	 * ts
	 * const graphics = new Graphics({ roundPixels: true });
	 * ts
 * // Create a new graphics object
 * const graphics = new Graphics();
 *
 * // Draw a filled rectangle with a stroke
 * graphics
 *     .rect(0, 0, 100, 100)
 *     .fill({ color: 0xff0000 }) // Fill with red
 *     .stroke({ width: 2, color: 0x000000 }); // Stroke with black
 *
 * // Draw a complex shape
 * graphics
 *     .moveTo(50, 50)
 *     .lineTo(100, 100)
 *     .arc(100, 100, 50, 0, Math.PI)
 *     .closePath()
 *     .fill({ color: 0x00ff00, alpha: 0.5 }); // Fill the shape
 *
 * // Use as a mask
 * sprite.mask = graphics;
 * ts
	 * // Create a shared context
	 * const sharedContext = new GraphicsContext();
	 *
	 * // Create graphics objects sharing the same context
	 * const graphics1 = new Graphics();
	 * const graphics2 = new Graphics();
	 *
	 * // Assign shared context
	 * graphics1.context = sharedContext;
	 * graphics2.context = sharedContext;
	 *
	 * // Both graphics will show the same shapes
	 * sharedContext
	 *     .rect(0, 0, 100, 100)
	 *     .fill({ color: 0xff0000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a shape
	 * graphics
	 *     .rect(0, 0, 100, 100)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Get bounds information
	 * const bounds = graphics.bounds;
	 * console.log(bounds.width);  // 100
	 * console.log(bounds.height); // 100
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a shape
	 * graphics
	 *     .rect(0, 0, 100, 100)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Check point intersection
	 * if (graphics.containsPoint({ x: 50, y: 50 })) {
	 *     console.log('Point is inside rectangle!');
	 * }
	 * ts
	 * // Destroy the graphics and its context
	 * graphics.destroy();
	 * graphics.destroy(true);
	 * graphics.destroy({ context: true, texture: true, textureSource: true });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic color fill
	 * graphics
	 *     .setFillStyle({ color: 0xff0000 }) // Red fill
	 *     .rect(0, 0, 100, 100)
	 *     .fill();
	 *
	 * // Gradient fill
	 * const gradient = new FillGradient({
	 *    end: { x: 1, y: 0 },
	 *    colorStops: [
	 *         { offset: 0, color: 0xff0000 }, // Red at start
	 *         { offset: 0.5, color: 0x00ff00 }, // Green at middle
	 *         { offset: 1, color: 0x0000ff }, // Blue at end
	 *    ],
	 * });
	 *
	 * graphics
	 *     .setFillStyle(gradient)
	 *     .circle(100, 100, 50)
	 *     .fill();
	 *
	 * // Pattern fill
	 * const pattern = new FillPattern(texture);
	 * graphics
	 *     .setFillStyle({
	 *         fill: pattern,
	 *         alpha: 0.5
	 *     })
	 *     .rect(0, 0, 200, 200)
	 *     .fill();
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic color stroke
	 * graphics
	 *     .setStrokeStyle({
	 *         width: 2,
	 *         color: 0x000000
	 *     })
	 *     .rect(0, 0, 100, 100)
	 *     .stroke();
	 *
	 * // Complex stroke style
	 * graphics
	 *     .setStrokeStyle({
	 *         width: 4,
	 *         color: 0xff0000,
	 *         alpha: 0.5,
	 *         join: 'round',
	 *         cap: 'round',
	 *         alignment: 0.5
	 *     })
	 *     .circle(100, 100, 50)
	 *     .stroke();
	 *
	 * // Gradient stroke
	 * const gradient = new FillGradient({
	 *    end: { x: 1, y: 0 },
	 *    colorStops: [
	 *         { offset: 0, color: 0xff0000 }, // Red at start
	 *         { offset: 0.5, color: 0x00ff00 }, // Green at middle
	 *         { offset: 1, color: 0x0000ff }, // Blue at end
	 *    ],
	 * });
	 *
	 * graphics
	 *     .setStrokeStyle({
	 *         width: 10,
	 *         fill: gradient
	 *     })
	 *     .poly([0,0, 100,50, 0,100])
	 *     .stroke();
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Fill with direct color
	 * graphics
	 *     .circle(50, 50, 25)
	 *     .fill('red'); // Red fill
	 *
	 * // Fill with texture
	 * graphics
	 *    .rect(0, 0, 100, 100)
	 *    .fill(myTexture); // Fill with texture
	 *
	 * // Fill with complex style
	 * graphics
	 *     .rect(0, 0, 100, 100)
	 *     .fill({
	 *         color: 0x00ff00,
	 *         alpha: 0.5,
	 *         texture: myTexture,
	 *         matrix: new Matrix()
	 *     });
	 *
	 * // Fill with gradient
	 * const gradient = new FillGradient({
	 *     end: { x: 1, y: 0 },
	 *     colorStops: [
	 *         { offset: 0, color: 0xff0000 },
	 *         { offset: 0.5, color: 0x00ff00 },
	 *         { offset: 1, color: 0x0000ff },
	 *     ],
	 * });
	 *
	 * graphics
	 *     .circle(100, 100, 50)
	 *     .fill(gradient);
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Stroke with direct color
	 * graphics
	 *     .circle(50, 50, 25)
	 *     .stroke({
	 *         width: 2,
	 *         color: 0xff0000
	 *     }); // 2px red stroke
	 *
	 * // Fill with texture
	 * graphics
	 *    .rect(0, 0, 100, 100)
	 *    .stroke(myTexture); // Fill with texture
	 *
	 * // Stroke with gradient
	 * const gradient = new FillGradient({
	 *     end: { x: 1, y: 0 },
	 *     colorStops: [
	 *         { offset: 0, color: 0xff0000 },
	 *         { offset: 0.5, color: 0x00ff00 },
	 *         { offset: 1, color: 0x0000ff },
	 *     ],
	 * });
	 *
	 * graphics
	 *     .rect(0, 0, 100, 100)
	 *     .stroke({
	 *         width: 4,
	 *         fill: gradient,
	 *         alignment: 0.5,
	 *         join: 'round'
	 *     });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic texture drawing
	 * graphics.texture(myTexture);
	 *
	 * // Tinted texture with position
	 * graphics.texture(myTexture, 0xff0000); // Red tint
	 *
	 * // Texture with custom position and dimensions
	 * graphics
	 *     .texture(
	 *         myTexture,    // texture
	 *         0xffffff,     // white tint
	 *         100, 100,     // position
	 *         200, 150      // dimensions
	 *     );
	 * ts
	 * const graphics = new Graphics();
	 * graphics
	 *     .circle(150, 150, 50)
	 *     .fill({ color: 0x00ff00 })
	 *     .beginPath() // Starts a new path
	 *     .circle(250, 150, 50)
	 *     .fill({ color: 0x0000ff });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw outer circle
	 * graphics
	 *     .circle(100, 100, 50)
	 *     .fill({ color: 0xff0000 });
	 *     .circle(100, 100, 25) // Inner circle
	 *     .cut() // Cuts out the inner circle from the outer circle
	 * ts
	 * // Draw a simple arc (quarter circle)
	 * const graphics = new Graphics();
	 * graphics
	 *     .arc(100, 100, 50, 0, Math.PI/2)
	 *     .stroke({ width: 2, color: 0xff0000 });
	 *
	 * // Draw a full circle using an arc
	 * graphics
	 *     .arc(200, 200, 30, 0, Math.PI * 2)
	 *     .stroke({ color: 0x00ff00 });
	 *
	 * // Draw a counterclockwise arc
	 * graphics
	 *     .arc(150, 150, 40, Math.PI, 0, true)
	 *     .stroke({ width: 2, color: 0x0000ff });
	 * ts
	 * // Draw a simple curved corner
	 * const graphics = new Graphics();
	 * graphics
	 *     .moveTo(50, 50)
	 *     .arcTo(100, 50, 100, 100, 20) // Rounded corner with 20px radius
	 *     .stroke({ width: 2, color: 0xff0000 });
	 *
	 * // Create a rounded rectangle using arcTo
	 * graphics
	 *     .moveTo(150, 150)
	 *     .arcTo(250, 150, 250, 250, 30) // Top right corner
	 *     .arcTo(250, 250, 150, 250, 30) // Bottom right corner
	 *     .arcTo(150, 250, 150, 150, 30) // Bottom left corner
	 *     .arcTo(150, 150, 250, 150, 30) // Top left corner
	 *     .fill({ color: 0x00ff00 });
	 * ts
	 * // Draw a simple elliptical arc
	 * const graphics = new Graphics();
	 * graphics
	 *     .moveTo(100, 100)
	 *     .arcToSvg(50, 30, 0, 0, 1, 200, 100)
	 *     .stroke({ width: 2, color: 0xff0000 });
	 *
	 * // Create a complex path with rotated elliptical arc
	 * graphics
	 *     .moveTo(150, 150)
	 *     .arcToSvg(
	 *         60,    // rx
	 *         30,    // ry
	 *         45,    // x-axis rotation (45 degrees)
	 *         1,     // large arc flag
	 *         0,     // sweep flag
	 *         250,   // end x
	 *         200    // end y
	 *     )
	 *     .stroke({ width: 4, color: 0x00ff00 });
	 *
	 * // Chain multiple arcs for complex shapes
	 * graphics
	 *     .moveTo(300, 100)
	 *     .arcToSvg(40, 20, 0, 0, 1, 350, 150)
	 *     .arcToSvg(40, 20, 0, 0, 1, 300, 200)
	 *     .fill({ color: 0x0000ff, alpha: 0.5 });
	 * ts
	 * // Draw a simple curved line
	 * const graphics = new Graphics();
	 * graphics
	 *     .moveTo(50, 50)
	 *     .bezierCurveTo(
	 *         100, 25,   // First control point
	 *         150, 75,   // Second control point
	 *         200, 50    // End point
	 *     )
	 *     .stroke({ width: 2, color: 0xff0000 });
	 *
	 * // Adjust curve smoothness
	 * graphics
	 *     .moveTo(50, 200)
	 *     .bezierCurveTo(
	 *         100, 150,
	 *         200, 250,
	 *         250, 200,
	 *         0.5         // Smoothness factor
	 *     )
	 *     .stroke({ width: 4, color: 0x0000ff });
	 * ts
	 * // Create a triangle with closed path
	 * const graphics = new Graphics();
	 * graphics
	 *     .moveTo(50, 50)
	 *     .lineTo(100, 100)
	 *     .lineTo(0, 100)
	 *     .closePath()
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a basic ellipse
	 * graphics
	 *     .ellipse(100, 100, 50, 30)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Draw an ellipse with stroke
	 * graphics
	 *     .ellipse(200, 100, 70, 40)
	 *     .stroke({ width: 2, color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a simple filled circle
	 * graphics
	 *     .circle(100, 100, 50)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Draw a circle with gradient fill
	 * const gradient = new FillGradient({
	 *     end: { x: 1, y: 0 },
	 *     colorStops: [
	 *           { offset: 0, color: 0xff0000 }, // Red at start
	 *           { offset: 0.5, color: 0x00ff00 }, // Green at middle
	 *           { offset: 1, color: 0x0000ff }, // Blue at end
	 *     ],
	 * });
	 *
	 * graphics
	 *     .circle(250, 100, 40)
	 *     .fill({ fill: gradient });
	 * ts
	 * const graphics = new Graphics();
	 * // Create a reusable path
	 * const heartPath = new GraphicsPath()
	 *     .moveTo(0, 0)
	 *     .bezierCurveTo(-50, -25, -50, -75, 0, -100)
	 *     .bezierCurveTo(50, -75, 50, -25, 0, 0);
	 *
	 * // Use the path multiple times
	 * graphics
	 *     .path(heartPath)
	 *     .fill({ color: 0xff0000 })
	 *     .translateTransform(200, 200)
	 *     .path(heartPath)
	 *     .fill({ color: 0xff0000, alpha: 0.5 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a triangle
	 * graphics
	 *     .moveTo(50, 50)
	 *     .lineTo(100, 100)
	 *     .lineTo(0, 100)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Create a complex shape with multiple lines
	 * graphics
	 *     .moveTo(200, 50)
	 *     .lineTo(250, 50)
	 *     .lineTo(250, 100)
	 *     .lineTo(200, 100)
	 *     .stroke({ width: 2, color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Create multiple separate lines
	 * graphics
	 *     .moveTo(50, 50)
	 *     .lineTo(100, 50)
	 *     .moveTo(50, 100)    // Start a new line
	 *     .lineTo(100, 100)
	 *     .stroke({ width: 2, color: 0xff0000 });
	 *
	 * // Create disconnected shapes
	 * graphics
	 *     .moveTo(150, 50)
	 *     .rect(150, 50, 50, 50)
	 *     .fill({ color: 0x00ff00 })
	 *     .moveTo(250, 50)    // Start a new shape
	 *     .circle(250, 75, 25)
	 *     .fill({ color: 0x0000ff });
	 *
	 * // Position before curved paths
	 * graphics
	 *     .moveTo(300, 50)
	 *     .bezierCurveTo(
	 *         350, 25,   // Control point 1
	 *         400, 75,   // Control point 2
	 *         450, 50    // End point
	 *     )
	 *     .stroke({ width: 3, color: 0xff00ff });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a simple curve
	 * graphics
	 *     .moveTo(50, 50)
	 *     .quadraticCurveTo(100, 25, 150, 50)
	 *     .stroke({ width: 2, color: 0xff0000 });
	 *
	 * // Adjust curve smoothness
	 * graphics
	 *     .moveTo(50, 200)
	 *     .quadraticCurveTo(
	 *         150, 150,   // Control point
	 *         250, 200,   // End point
	 *         0.5         // Smoothness factor
	 *     )
	 *     .stroke({
	 *         width: 4,
	 *         color: 0x0000ff,
	 *         alpha: 0.7
	 *     });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a simple filled rectangle
	 * graphics
	 *     .rect(50, 50, 100, 75)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Rectangle with stroke
	 * graphics
	 *     .rect(200, 50, 100, 75)
	 *     .stroke({ width: 2, color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic rounded rectangle
	 * graphics
	 *     .roundRect(50, 50, 100, 75, 15)
	 *     .fill({ color: 0xff0000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a triangle using array of numbers [x1,y1, x2,y2, x3,y3]
	 * graphics
	 *     .poly([50,50, 100,100, 0,100], true)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Draw a polygon using point objects
	 * graphics
	 *     .poly([
	 *         { x: 200, y: 50 },
	 *         { x: 250, y: 100 },
	 *         { x: 200, y: 150 },
	 *         { x: 150, y: 100 }
	 *     ])
	 *     .fill({ color: 0x00ff00 });
	 *
	 * // Draw an open polygon with stroke
	 * graphics
	 *     .poly([300,50, 350,50, 350,100, 300,100], false)
	 *     .stroke({
	 *         width: 2,
	 *         color: 0x0000ff,
	 *         join: 'round'
	 *     });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a simple triangle (3 sides)
	 * graphics
	 *     .regularPoly(100, 100, 50, 3)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Draw a hexagon (6 sides) with rotation
	 * graphics
	 *     .regularPoly(
	 *         250, 100,    // center position
	 *         40,          // radius
	 *         6,           // sides
	 *         Math.PI / 6  // rotation (30 degrees)
	 *     )
	 *     .fill({ color: 0x00ff00 })
	 *     .stroke({ width: 2, color: 0x000000 });
	 *
	 * // Draw an octagon (8 sides) with transform
	 * const transform = new Matrix()
	 *     .scale(1.5, 1)      // stretch horizontally
	 *     .rotate(Math.PI/4); // rotate 45 degrees
	 *
	 * graphics
	 *     .regularPoly(400, 100, 30, 8, 0, transform)
	 *     .fill({ color: 0x0000ff, alpha: 0.5 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a basic rounded triangle
	 * graphics
	 *     .roundPoly(100, 100, 50, 3, 10)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Draw a rounded hexagon with rotation
	 * graphics
	 *     .roundPoly(
	 *         250, 150,     // center position
	 *         40,           // radius
	 *         6,            // sides
	 *         8,            // corner radius
	 *         Math.PI / 6   // rotation (30 degrees)
	 *     )
	 *     .fill({ color: 0x00ff00 })
	 *     .stroke({ width: 2, color: 0x000000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a custom shape with rounded corners
	 * graphics
	 *     .roundShape([
	 *         { x: 100, y: 100, radius: 20 },
	 *         { x: 200, y: 100, radius: 10 },
	 *         { x: 200, y: 200, radius: 15 },
	 *         { x: 100, y: 200, radius: 5 }
	 *     ], 10)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Using quadratic curves for corners
	 * graphics
	 *     .roundShape([
	 *         { x: 250, y: 100 },
	 *         { x: 350, y: 100 },
	 *         { x: 350, y: 200 },
	 *         { x: 250, y: 200 }
	 *     ], 15, true, 0.5)
	 *     .fill({ color: 0x00ff00 })
	 *     .stroke({ width: 2, color: 0x000000 });
	 *
	 * // Shape with varying corner radii
	 * graphics
	 *     .roundShape([
	 *         { x: 400, y: 100, radius: 30 },
	 *         { x: 500, y: 100, radius: 5 },
	 *         { x: 450, y: 200, radius: 15 }
	 *     ], 10)
	 *     .fill({ color: 0x0000ff, alpha: 0.5 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a rectangle with internal fillets
	 * graphics
	 *     .filletRect(50, 50, 100, 80, 15)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Draw a rectangle with external fillets
	 * graphics
	 *     .filletRect(200, 50, 100, 80, -20)
	 *     .fill({ color: 0x00ff00 })
	 *     .stroke({ width: 2, color: 0x000000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a basic chamfered rectangle
	 * graphics
	 *     .chamferRect(50, 50, 100, 80, 15)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Add transform and stroke
	 * const transform = new Matrix()
	 *     .rotate(Math.PI / 4); // 45 degrees
	 *
	 * graphics
	 *     .chamferRect(200, 50, 100, 80, 20, transform)
	 *     .fill({ color: 0x00ff00 })
	 *     .stroke({ width: 2, color: 0x000000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw a basic 5-pointed star
	 * graphics
	 *     .star(100, 100, 5, 50)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Star with custom inner radius
	 * graphics
	 *     .star(250, 100, 6, 50, 20)
	 *     .fill({ color: 0x00ff00 })
	 *     .stroke({ width: 2, color: 0x000000 });
	 * ts
	 * const graphics = new Graphics();
	 * graphics
	 *     .svg(`
	 *         <path d="M 50,50 L 100,50 L 100,100 L 50,100 Z"
	 *               fill="blue" />
	 *         <circle cx="150" cy="75" r="25"
	 *               fill="green" />
	 *     `)
	 *     .stroke({ width: 2, color: 0x000000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Save current state
	 * graphics.save();
	 *
	 * // Make temporary changes
	 * graphics
	 *     .translateTransform(100, 100)
	 *     .setFillStyle({ color: 0xff0000 })
	 *     .circle(0, 0, 50)
	 *     .fill();
	 *
	 * // Restore to previous state
	 * graphics.restore();
	 *
	 * // Draw with original transform and styles
	 * graphics
	 *     .circle(50, 50, 30)
	 *     .fill();
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Save state before complex operations
	 * graphics.save();
	 *
	 * // Create transformed and styled shape
	 * graphics
	 *     .translateTransform(100, 100)
	 *     .rotateTransform(Math.PI / 4)
	 *     .setFillStyle({
	 *         color: 0xff0000,
	 *         alpha: 0.5
	 *     })
	 *     .rect(-25, -25, 50, 50)
	 *     .fill();
	 *
	 * // Restore to original state
	 * graphics.restore();
	 *
	 * // Continue drawing with previous state
	 * graphics
	 *     .circle(50, 50, 25)
	 *     .fill();
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Apply some transformations
	 * graphics
	 *     .translateTransform(100, 100)
	 *     .rotateTransform(Math.PI / 4);
	 *
	 * // Get the current transform matrix
	 * const matrix = graphics.getTransform();
	 * console.log(matrix.tx, matrix.ty); // 100, 100
	 *
	 * // Use the matrix for other operations
	 * graphics
	 *     .setTransform(matrix)
	 *     .circle(0, 0, 50)
	 *     .fill({ color: 0xff0000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Apply transformations
	 * graphics
	 *     .translateTransform(100, 100)
	 *     .scaleTransform(2, 2)
	 *     .circle(0, 0, 25)
	 *     .fill({ color: 0xff0000 });
	 * // Reset transform to default state
	 * graphics
	 *     .resetTransform()
	 *     .circle(50, 50, 25) // Will draw at actual coordinates
	 *     .fill({ color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Rotate 45 degrees clockwise
	 * graphics
	 *     .rotateTransform(Math.PI / 4)
	 *     .rect(-25, -25, 50, 50)
	 *     .fill({ color: 0xff0000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Uniform scaling
	 * graphics
	 *     .scaleTransform(2)  // Scale both dimensions by 2
	 *     .circle(0, 0, 25)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Non-uniform scaling
	 * graphics
	 *     .scaleTransform(0.5, 2)  // Half width, double height
	 *     .rect(100, 100, 50, 50)
	 *     .fill({ color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Using a Matrix object
	 * const matrix = new Matrix()
	 *     .translate(100, 100)
	 *     .rotate(Math.PI / 4);
	 *
	 * graphics
	 *     .setTransform(matrix)
	 *     .rect(0, 0, 50, 50)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Using individual transform values
	 * graphics
	 *     .setTransform(
	 *         2, 0,     // scale x by 2
	 *         0, 1,     // no skew
	 *         100, 100  // translate x,y by 100
	 *     )
	 *     .circle(0, 0, 25)
	 *     .fill({ color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Using a Matrix object
	 * const matrix = new Matrix()
	 *     .scale(2, 1)      // Scale horizontally
	 *     .rotate(Math.PI/6); // Rotate 30 degrees
	 *
	 * graphics
	 *     .transform(matrix)
	 *     .rect(0, 0, 50, 50)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Using individual transform values
	 * graphics
	 *     .transform(
	 *         1, 0.5,    // Skew horizontally
	 *         0, 1,      // No vertical skew
	 *         100, 100   // Translate
	 *     )
	 *     .circle(0, 0, 25)
	 *     .fill({ color: 0x00ff00 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic translation
	 * graphics
	 *     .translateTransform(100, 100)
	 *     .circle(0, 0, 25)
	 *     .fill({ color: 0xff0000 });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Draw some shapes
	 * graphics
	 *     .circle(100, 100, 50)
	 *     .fill({ color: 0xff0000 })
	 *     .rect(200, 100, 100, 50)
	 *     .fill({ color: 0x00ff00 });
	 *
	 * // Clear all graphics
	 * graphics.clear();
	 *
	 * // Start fresh with new shapes
	 * graphics
	 *     .circle(150, 150, 30)
	 *     .fill({ color: 0x0000ff });
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic color fill
	 * graphics.fillStyle = {
	 *     color: 0xff0000,  // Red
	 *     alpha: 1
	 * };
	 *
	 * // Using gradients
	 * const gradient = new FillGradient({
	 *     end: { x: 0, y: 1 }, // Vertical gradient
	 *     stops: [
	 *         { offset: 0, color: 0xff0000, alpha: 1 }, // Start color
	 *         { offset: 1, color: 0x0000ff, alpha: 1 }  // End color
	 *     ]
	 * });
	 *
	 * graphics.fillStyle = {
	 *     fill: gradient,
	 *     alpha: 0.8
	 * };
	 *
	 * // Using patterns
	 * graphics.fillStyle = {
	 *     texture: myTexture,
	 *     alpha: 1,
	 *     matrix: new Matrix()
	 *         .scale(0.5, 0.5)
	 *         .rotate(Math.PI / 4)
	 * };
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Basic stroke style
	 * graphics.strokeStyle = {
	 *     width: 2,
	 *     color: 0xff0000,
	 *     alpha: 1
	 * };
	 *
	 * // Using with gradients
	 * const gradient = new FillGradient({
	 *   end: { x: 0, y: 1 },
	 *   stops: [
	 *       { offset: 0, color: 0xff0000, alpha: 1 },
	 *       { offset: 1, color: 0x0000ff, alpha: 1 }
	 *   ]
	 * });
	 *
	 * graphics.strokeStyle = {
	 *     width: 4,
	 *     fill: gradient,
	 *     alignment: 0.5,
	 *     join: 'round',
	 *     cap: 'round'
	 * };
	 *
	 * // Complex stroke settings
	 * graphics.strokeStyle = {
	 *     width: 6,
	 *     color: 0x00ff00,
	 *     alpha: 0.5,
	 *     join: 'miter',
	 *     miterLimit: 10,
	 * };
	 * ts
	 * const graphics = new Graphics();
	 *
	 * // Create original graphics content
	 * graphics
	 *     .circle(100, 100, 50)
	 *     .fill({ color: 0xff0000 });
	 *
	 * // Create a shallow clone (shared context)
	 * const shallowClone = graphics.clone();
	 *
	 * // Changes to original affect the clone
	 * graphics
	 *     .circle(200, 100, 30)
	 *     .fill({ color: 0x00ff00 });
	 *
	 * // Create a deep clone (independent context)
	 * const deepClone = graphics.clone(true);
	 *
	 * // Modify deep clone independently
	 * deepClone
	 *     .translateTransform(100, 100)
	 *     .circle(0, 0, 40)
	 *     .fill({ color: 0x0000ff });
	 * ts
 * // Using a Container as a mask
 * const maskContainer: Mask = new Graphics();
 * // Using a mask ID
 * const maskId: Mask = 123;
 * // No mask applied
 * const noMask: Mask = null;
 * ts
 * // Basic mask inversion
 * sprite.setMask({
 *     mask: graphics,
 *     inverse: true
 * });
 * ts
	 * // Invert the mask
	 * sprite.setMask({
	 *     mask: graphics,
	 *     inverse: true
	 * });
	 * ts
 * sprite.setMask({
 *     mask: graphics,
 *     inverse: true,
 * });
 *
 * // Clear existing mask
 * sprite.setMask({
 *     mask: null,
 *     inverse: false,
 * });
 * ts
	 * // Set a mask
	 * sprite.setMask({
	 *     mask: graphics,
	 *     inverse: false,
	 * });
	 */
	mask: Mask;
}
/**
 * The Circle object represents a circle shape in a two-dimensional coordinate system.
 * Used for drawing graphics and specifying hit areas for containers.
 * @example
 * 
 * @remarks
 * - Defined by center (x,y) and radius
 * - Supports point containment tests
 * - Can check stroke intersections
 */
export declare class Circle implements ShapePrimitive {
	/**
	 * The X coordinate of the center of this circle
	 * @example
	 * 
	 * @default 0
	 */
	x: number;
	/**
	 * The Y coordinate of the center of this circle
	 * @example
	 * 
	 * @default 0
	 */
	y: number;
	/**
	 * The radius of the circle
	 * @example
	 * 
	 * @default 0
	 */
	radius: number;
	/**
	 * The type of the object, mainly used to avoid `instanceof` checks.
	 * @example
	 * 
	 * @remarks
	 * - Used for shape type checking
	 * - More efficient than instanceof
	 * - Read-only property
	 * @default 'circle'
	 */
	readonly type: SHAPE_PRIMITIVE;
	/**
	 * @param x - The X coordinate of the center of this circle
	 * @param y - The Y coordinate of the center of this circle
	 * @param radius - The radius of the circle
	 */
	constructor(x?: number, y?: number, radius?: number);
	/**
	 * Creates a clone of this Circle instance.
	 * @example
	 * 
	 * @returns A copy of the Circle
	 */
	clone(): Circle;
	/**
	 * Checks whether the x and y coordinates given are contained within this circle.
	 *
	 * Uses the distance formula to determine if a point is inside the circle's radius.
	 *
	 * Commonly used for hit testing in PixiJS events and graphics.
	 * @example
	 * 
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @returns Whether the x/y coordinates are within this Circle
	 */
	contains(x: number, y: number): boolean;
	/**
	 * Checks whether the x and y coordinates given are contained within this circle including the stroke.
	 * @example
	 * 
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @param width - The width of the line to check
	 * @param alignment - The alignment of the stroke, 0.5 by default
	 * @returns Whether the x/y coordinates are within this Circle's stroke
	 */
	strokeContains(x: number, y: number, width: number, alignment?: number): boolean;
	/**
	 * Returns the framing rectangle of the circle as a Rectangle object.
	 * @example
	 * 
	 * @param out - Optional Rectangle object to store the result
	 * @returns The framing rectangle
	 */
	getBounds(out?: Rectangle): Rectangle;
	/**
	 * Copies another circle to this one.
	 * @example
	 * 
	 * @param circle - The circle to copy from
	 * @returns Returns itself
	 */
	copyFrom(circle: Circle): this;
	/**
	 * Copies this circle to another one.
	 * @example
	 * 
	 * @param circle - The circle to copy to
	 * @returns Returns given parameter
	 */
	copyTo(circle: Circle): Circle;
	toString(): string;
}
/**
 * The Ellipse object is used to help draw graphics and can also be used to specify a hit area for containers.
 * @example
 * 
 * @remarks
 * - Defined by center (x,y) and half dimensions
 * - Total width = halfWidth * 2
 * - Total height = halfHeight * 2
 */
export declare class Ellipse implements ShapePrimitive {
	/**
	 * The X coordinate of the center of this ellipse
	 * @example
	 * 
	 * @default 0
	 */
	x: number;
	/**
	 * The Y coordinate of the center of this ellipse
	 * @example
	 * 
	 * @default 0
	 */
	y: number;
	/**
	 * The half width of this ellipse
	 * @example
	 * 
	 * @default 0
	 */
	halfWidth: number;
	/**
	 * The half height of this ellipse
	 * @example
	 * 
	 * @default 0
	 */
	halfHeight: number;
	/**
	 * The type of the object, mainly used to avoid `instanceof` checks
	 * @example
	 * 
	 * @default 'ellipse'
	 */
	readonly type = "ellipse";
	/**
	 * @param x - The X coordinate of the center of this ellipse
	 * @param y - The Y coordinate of the center of this ellipse
	 * @param halfWidth - The half width of this ellipse
	 * @param halfHeight - The half height of this ellipse
	 */
	constructor(x?: number, y?: number, halfWidth?: number, halfHeight?: number);
	/**
	 * Creates a clone of this Ellipse instance.
	 * @example
	 * 
	 * @returns A copy of the ellipse
	 */
	clone(): Ellipse;
	/**
	 * Checks whether the x and y coordinates given are contained within this ellipse.
	 * Uses normalized coordinates and the ellipse equation to determine containment.
	 * @example
	 * 
	 * @remarks
	 * - Uses ellipse equation (x²/a² + y²/b² ≤ 1)
	 * - Returns false if dimensions are 0 or negative
	 * - Normalized to center (0,0) for calculation
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @returns Whether the x/y coords are within this ellipse
	 */
	contains(x: number, y: number): boolean;
	/**
	 * Checks whether the x and y coordinates given are contained within this ellipse including stroke.
	 * @example
	 * 
	 * @remarks
	 * - Uses normalized ellipse equations
	 * - Considers stroke alignment
	 * - Returns false if dimensions are 0
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @param strokeWidth - The width of the line to check
	 * @param alignment - The alignment of the stroke (1 = inner, 0.5 = centered, 0 = outer)
	 * @returns Whether the x/y coords are within this ellipse's stroke
	 */
	strokeContains(x: number, y: number, strokeWidth: number, alignment?: number): boolean;
	/**
	 * Returns the framing rectangle of the ellipse as a Rectangle object.
	 * @example
	 * 
	 * @remarks
	 * - Creates Rectangle if none provided
	 * - Top-left is (x-halfWidth, y-halfHeight)
	 * - Width is halfWidth * 2
	 * - Height is halfHeight * 2
	 * @param out - Optional Rectangle object to store the result
	 * @returns The framing rectangle
	 */
	getBounds(out?: Rectangle): Rectangle;
	/**
	 * Copies another ellipse to this one.
	 * @example
	 * 
	 * @param ellipse - The ellipse to copy from
	 * @returns Returns itself
	 */
	copyFrom(ellipse: Ellipse): this;
	/**
	 * Copies this ellipse to another one.
	 * @example
	 * 
	 * @param ellipse - The ellipse to copy to
	 * @returns Returns given parameter
	 */
	copyTo(ellipse: Ellipse): Ellipse;
	toString(): string;
}
/**
 * The `RoundedRectangle` object represents a rectangle with rounded corners.
 * Defined by position, dimensions and corner radius.
 * @example
 * 
 * @remarks
 * - Position defined by top-left corner
 * - Radius clamped to half smallest dimension
 * - Common in UI elements
 */
export declare class RoundedRectangle implements ShapePrimitive {
	/**
	 * The X coordinate of the upper-left corner of the rounded rectangle
	 * @example
	 * 
	 * @default 0
	 */
	x: number;
	/**
	 * The Y coordinate of the upper-left corner of the rounded rectangle
	 * @example
	 * 
	 * @default 0
	 */
	y: number;
	/**
	 * The overall width of this rounded rectangle
	 * @example
	 * 
	 * @default 0
	 */
	width: number;
	/**
	 * The overall height of this rounded rectangle
	 * @example
	 * 
	 * @default 0
	 */
	height: number;
	/**
	 * Controls the radius of the rounded corners
	 * @example
	 * 
	 * @remarks
	 * - Automatically clamped to half of smallest dimension
	 * - Common values: 0-20 for UI elements
	 * - Higher values create more rounded corners
	 * @default 20
	 */
	radius: number;
	/**
	 * The type of the object, mainly used to avoid `instanceof` checks
	 * @example
	 * 
	 * @default 'roundedRectangle'
	 */
	readonly type: SHAPE_PRIMITIVE;
	/**
	 * @param x - The X coordinate of the upper-left corner of the rounded rectangle
	 * @param y - The Y coordinate of the upper-left corner of the rounded rectangle
	 * @param width - The overall width of this rounded rectangle
	 * @param height - The overall height of this rounded rectangle
	 * @param radius - Controls the radius of the rounded corners
	 */
	constructor(x?: number, y?: number, width?: number, height?: number, radius?: number);
	/**
	 * Returns the framing rectangle of the rounded rectangle as a Rectangle object
	 * @example
	 * 
	 * @remarks
	 * - Rectangle matches outer dimensions
	 * - Ignores corner radius
	 * @param out - Optional rectangle to store the result
	 * @returns The framing rectangle
	 */
	getBounds(out?: Rectangle): Rectangle;
	/**
	 * Creates a clone of this Rounded Rectangle.
	 * @example
	 * 
	 * @returns A copy of the rounded rectangle
	 */
	clone(): RoundedRectangle;
	/**
	 * Copies another rectangle to this one.
	 * @example
	 * 
	 * @param rectangle - The rectangle to copy from
	 * @returns Returns itself
	 */
	copyFrom(rectangle: RoundedRectangle): this;
	/**
	 * Copies this rectangle to another one.
	 * @example
	 * 
	 * @param rectangle - The rectangle to copy to
	 * @returns Returns given parameter
	 */
	copyTo(rectangle: RoundedRectangle): RoundedRectangle;
	/**
	 * Checks whether the x and y coordinates given are contained within this Rounded Rectangle
	 * @example
	 * 
	 * @remarks
	 * - Returns false if width/height is 0 or negative
	 * - Handles rounded corners with radius check
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @returns Whether the x/y coordinates are within this Rounded Rectangle
	 */
	contains(x: number, y: number): boolean;
	/**
	 * Checks whether the x and y coordinates given are contained within this rectangle including the stroke.
	 * @example
	 * 
	 * @param pX - The X coordinate of the point to test
	 * @param pY - The Y coordinate of the point to test
	 * @param strokeWidth - The width of the line to check
	 * @param alignment - The alignment of the stroke (1 = inner, 0.5 = centered, 0 = outer)
	 * @returns Whether the x/y coordinates are within this rectangle's stroke
	 */
	strokeContains(pX: number, pY: number, strokeWidth: number, alignment?: number): boolean;
	toString(): string;
}
type RoundedShape = Circle | Ellipse | RoundedRectangle;
/**
 * A class to define a shape via user defined coordinates.
 * Used for creating complex shapes and hit areas with custom points.
 * @example
 * 
 */
export declare class Polygon implements ShapePrimitive {
	/**
	 * An array of the points of this polygon stored as a flat array of numbers.
	 * @example
	 * 
	 * @remarks
	 * - Stored as [x1, y1, x2, y2, ...]
	 * - Each pair represents a vertex
	 * - Length is always even
	 * - Can be modified directly
	 */
	points: number[];
	/**
	 * Indicates if the polygon path is closed.
	 * @example
	 * 
	 * @remarks
	 * - True by default
	 * - False after moveTo
	 * - True after closePath
	 * @default true
	 */
	closePath: boolean;
	/**
	 * The type of the object, mainly used to avoid `instanceof` checks
	 * @example
	 * 
	 * @default 'polygon'
	 */
	readonly type: SHAPE_PRIMITIVE;
	constructor(points: PointData[] | number[]);
	constructor(...points: PointData[] | number[]);
	/**
	 * Determines whether the polygon's points are arranged in a clockwise direction.
	 * Uses the shoelace formula (surveyor's formula) to calculate the signed area.
	 *
	 * A positive area indicates clockwise winding, while negative indicates counter-clockwise.
	 *
	 * The formula sums up the cross products of adjacent vertices:
	 * For each pair of adjacent points (x1,y1) and (x2,y2), we calculate (x1*y2 - x2*y1)
	 * The final sum divided by 2 gives the signed area - positive for clockwise.
	 * @example
	 * 
	 * @returns `true` if the polygon's points are arranged clockwise, `false` if counter-clockwise
	 */
	isClockwise(): boolean;
	/**
	 * Checks if this polygon completely contains another polygon.
	 * Used for detecting holes in shapes, like when parsing SVG paths.
	 * @example
	 * 
	 * @remarks
	 * - Uses bounds check for quick rejection
	 * - Tests all points for containment
	 * @param polygon - The polygon to test for containment
	 * @returns True if this polygon completely contains the other polygon
	 */
	containsPolygon(polygon: Polygon): boolean;
	/**
	 * Creates a clone of this polygon.
	 * @example
	 * 
	 * @returns A copy of the polygon
	 */
	clone(): Polygon;
	/**
	 * Checks whether the x and y coordinates passed to this function are contained within this polygon.
	 * Uses raycasting algorithm for point-in-polygon testing.
	 * @example
	 * 
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @returns Whether the x/y coordinates are within this polygon
	 */
	contains(x: number, y: number): boolean;
	/**
	 * Checks whether the x and y coordinates given are contained within this polygon including the stroke.
	 * @example
	 * 
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @param strokeWidth - The width of the line to check
	 * @param alignment - The alignment of the stroke (1 = inner, 0.5 = centered, 0 = outer)
	 * @returns Whether the x/y coordinates are within this polygon's stroke
	 */
	strokeContains(x: number, y: number, strokeWidth: number, alignment?: number): boolean;
	/**
	 * Returns the framing rectangle of the polygon as a Rectangle object.
	 * @example
	 * 
	 * @param out - Optional rectangle to store the result
	 * @returns The framing rectangle
	 */
	getBounds(out?: Rectangle): Rectangle;
	/**
	 * Copies another polygon to this one.
	 * @example
	 * 
	 * @param polygon - The polygon to copy from
	 * @returns Returns itself
	 */
	copyFrom(polygon: Polygon): this;
	/**
	 * Copies this polygon to another one.
	 * @example
	 * 
	 * @param polygon - The polygon to copy to
	 * @returns Returns given parameter
	 */
	copyTo(polygon: Polygon): Polygon;
	toString(): string;
	/**
	 * Get the last X coordinate of the polygon.
	 * @example
	 * 
	 * @returns The x-coordinate of the last vertex
	 */
	get lastX(): number;
	/**
	 * Get the last Y coordinate of the polygon.
	 * @example
	 * 
	 * @returns The y-coordinate of the last vertex
	 */
	get lastY(): number;
	/**
	 * Get the last X coordinate of the polygon.
	 * @deprecated since 8.11.0, use {@link Polygon.lastX} instead.
	 */
	get x(): number;
	/**
	 * Get the last Y coordinate of the polygon.
	 * @deprecated since 8.11.0, use {@link Polygon.lastY} instead.
	 */
	get y(): number;
	/**
	 * Get the first X coordinate of the polygon.
	 * @example
	 * 
	 * @returns The x-coordinate of the first vertex
	 */
	get startX(): number;
	/**
	 * Get the first Y coordinate of the polygon.
	 * @example
	 * 
	 * @returns The y-coordinate of the first vertex
	 */
	get startY(): number;
}
/**
 * A class to define a shape of a triangle via user defined coordinates.
 *
 * Used for creating triangular shapes and hit areas with three points (x,y), (x2,y2), (x3,y3).
 * Points are stored in counter-clockwise order.
 * @example
 * 
 */
export declare class Triangle implements ShapePrimitive {
	/**
	 * The type of the object, mainly used to avoid `instanceof` checks
	 * @example
	 * 
	 * @default 'triangle'
	 */
	readonly type: SHAPE_PRIMITIVE;
	/**
	 * The X coordinate of the first point of the triangle.
	 * @example
	 * 
	 * @default 0
	 */
	x: number;
	/**
	 * The Y coordinate of the first point of the triangle.
	 * @example
	 * 
	 * @default 0
	 */
	y: number;
	/**
	 * The X coordinate of the second point of the triangle.
	 * @example
	 * 
	 * @default 0
	 */
	x2: number;
	/**
	 * The Y coordinate of the second point of the triangle.
	 * @example
	 * 
	 * @default 0
	 */
	y2: number;
	/**
	 * The X coordinate of the third point of the triangle.
	 * @example
	 * 
	 * @default 0
	 */
	x3: number;
	/**
	 * The Y coordinate of the third point of the triangle.
	 * @example
	 * 
	 * @default 0
	 */
	y3: number;
	/**
	 * @param x - The X coord of the first point.
	 * @param y - The Y coord of the first point.
	 * @param x2 - The X coord of the second point.
	 * @param y2 - The Y coord of the second point.
	 * @param x3 - The X coord of the third point.
	 * @param y3 - The Y coord of the third point.
	 */
	constructor(x?: number, y?: number, x2?: number, y2?: number, x3?: number, y3?: number);
	/**
	 * Checks whether the x and y coordinates given are contained within this triangle
	 * @example
	 * 
	 * @remarks
	 * - Uses barycentric coordinate system
	 * - Works with any triangle shape
	 * @param x - The X coordinate of the point to test
	 * @param y - The Y coordinate of the point to test
	 * @returns Whether the x/y coordinates are within this Triangle
	 */
	contains(x: number, y: number): boolean;
	/**
	 * Checks whether the x and y coordinates given are contained within this triangle including the stroke.
	 * @example
	 * 
	 * @param pointX - The X coordinate of the point to test
	 * @param pointY - The Y coordinate of the point to test
	 * @param strokeWidth - The width of the line to check
	 * @param _alignment - The alignment of the stroke (1 = inner, 0.5 = centered, 0 = outer)
	 * @returns Whether the x/y coordinates are within this triangle's stroke
	 */
	strokeContains(pointX: number, pointY: number, strokeWidth: number, _alignment?: number): boolean;
	/**
	 * Creates a clone of this Triangle
	 * @example
	 * 
	 * @returns A copy of the triangle
	 */
	clone(): Triangle;
	/**
	 * Copies another triangle to this one.
	 * @example
	 * 
	 * @param triangle - The triangle to copy from
	 * @returns Returns itself
	 */
	copyFrom(triangle: Triangle): this;
	/**
	 * Copies this triangle to another one.
	 * @example
	 * 
	 * @remarks
	 * - Updates target triangle values
	 * - Copies all point coordinates
	 * - Returns target for chaining
	 * - More efficient than clone()
	 * @param triangle - The triangle to copy to
	 * @returns Returns given parameter
	 */
	copyTo(triangle: Triangle): Triangle;
	/**
	 * Returns the framing rectangle of the triangle as a Rectangle object
	 * @example
	 * 
	 * @param out - Optional rectangle to store the result
	 * @returns The framing rectangle
	 */
	getBounds(out?: Rectangle): Rectangle;
}
/**
 * Constructor options used for `MeshPlane` instances. Defines how a texture is mapped
 * onto a plane with configurable vertex density.
 * @example
 * 
 */
export interface MeshPlaneOptions extends Omit<MeshOptions, "geometry"> {
	/** The texture to use on the plane. */
	texture: Texture;
	/**
	 * Number of vertices along the X axis. More vertices allow for more detailed deformations.
	 * @default 10
	 */
	verticesX?: number;
	/**
	 * Number of vertices along the Y axis. More vertices allow for more detailed deformations.
	 * @default 10
	 */
	verticesY?: number;
}
/**
 * A mesh that renders a texture mapped to a plane with configurable vertex density.
 * Useful for creating distortion effects, bent surfaces, and animated deformations.
 * @example
 * 
 */
export declare class MeshPlane extends Mesh {
	/**
	 * Controls whether the mesh geometry automatically updates when the texture dimensions change.
	 * When true, the mesh will resize to match any texture updates. When false, the mesh maintains
	 * its original dimensions regardless of texture changes.
	 * @example
	 * 
	 * @default true
	 */
	autoResize: boolean;
	/**
	 * @param options - Options to be applied to MeshPlane
	 */
	constructor(options: MeshPlaneOptions);
	set texture(value: Texture);
	/**
	 * The texture that the mesh plane uses for rendering. When changed, automatically updates
	 * geometry dimensions if autoResize is true and manages texture update event listeners.
	 * @example
	 * 
	 */
	get texture(): Texture;
	/**
	 * Destroys this sprite renderable and optionally its texture.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * meshPlane.destroy();
	 * meshPlane.destroy(true);
	 * meshPlane.destroy({ texture: true, textureSource: true });
	 */
	destroy(options?: DestroyOptions): void;
}
/**
 * Constructor options used for `PerspectiveMesh` instances. Defines the geometry and appearance
 * of a 2D mesh with perspective projection.
 * @example
 * 
 */
export interface PerspectivePlaneOptions extends MeshPlaneOptions {
	/** The x-coordinate of the top-left corner */
	x0?: number;
	/** The y-coordinate of the top-left corner */
	y0?: number;
	/** The x-coordinate of the top-right corner */
	x1?: number;
	/** The y-coordinate of the top-right corner */
	y1?: number;
	/** The x-coordinate of the bottom-right corner */
	x2?: number;
	/** The y-coordinate of the bottom-right corner */
	y2?: number;
	/** The x-coordinate of the bottom-left corner */
	x3?: number;
	/** The y-coordinate of the bottom-left corner */
	y3?: number;
}
/**
 * A perspective mesh that allows you to draw a 2d plane with perspective. Where ever you move the corners
 * the texture will be projected to look like it is in 3d space. Great for mapping a 2D mesh into a 3D scene.
 *
 * The calculations is done at the uv level. This means that the more vertices you have the more smooth
 * the perspective will be. If you have a low amount of vertices you may see the texture stretch. Too many vertices
 * could be slower. It is a balance between performance and quality! We leave that to you to decide.
 *
 * > [!IMPORTANT] This is not a full 3D mesh, it is a 2D mesh with a perspective projection applied to it.
 * @example
 * 
 */
export declare class PerspectiveMesh extends Mesh<PerspectivePlaneGeometry> {
	/**
	 * Default options for creating a PerspectiveMesh instance.
	 *
	 * Creates a 100x100 pixel square mesh
	 * with a white texture and 10x10 vertex grid for the perspective calculations.
	 * @example
	 * 
	 */
	static defaultOptions: PerspectivePlaneOptions;
	/**
	 * @param options - Options to be applied to PerspectiveMesh
	 */
	constructor(options: PerspectivePlaneOptions);
	set texture(value: Texture);
	/**
	 * The texture that the mesh uses for rendering. When changed, automatically updates
	 * the geometry to match the new texture dimensions.
	 * @example
	 * 
	 */
	get texture(): Texture;
	/**
	 * Sets the corners of the mesh to create a perspective transformation. The corners should be
	 * specified in clockwise order starting from the top-left.
	 *
	 * The mesh automatically recalculates the UV coordinates to create the perspective effect.
	 * @example
	 * 
	 * @param x0 - x-coordinate of the top-left corner
	 * @param y0 - y-coordinate of the top-left corner
	 * @param x1 - x-coordinate of the top-right corner
	 * @param y1 - y-coordinate of the top-right corner
	 * @param x2 - x-coordinate of the bottom-right corner
	 * @param y2 - y-coordinate of the bottom-right corner
	 * @param x3 - x-coordinate of the bottom-left corner
	 * @param y3 - y-coordinate of the bottom-left corner
	 * @returns The PerspectiveMesh instance for method chaining
	 */
	setCorners(x0: number, y0: number, x1: number, y1: number, x2: number, y2: number, x3: number, y3: number): void;
}
type Matrix3x3 = ArrayFixed<number, 9>;
/**
 * Constructor options used for `MeshRope` instances. Allows configuration of a rope-like mesh
 * that follows a series of points with a texture applied.
 * @example
 * 
 */
export interface MeshRopeOptions extends Omit<MeshOptions, "geometry"> {
	/** The texture to use on the rope */
	texture: Texture;
	/** An array of points that determine the rope's shape and path */
	points: PointData[];
	/**
	 * Controls how the texture is scaled along the rope.
	 * - If 0 (default), the texture stretches to fit between points
	 * - If > 0, texture repeats with preserved aspect ratio
	 * - Larger textures with textureScale < 1 can reduce artifacts
	 * @default 0
	 */
	textureScale?: number;
}
/**
 * A specialized mesh that renders a texture along a path defined by points. Perfect for
 * creating snake-like animations, chains, ropes, and other flowing objects.
 * @example
 * 
 */
export declare class MeshRope extends Mesh {
	/**
	 * Default options for creating a MeshRope instance. These values are used when specific
	 * options aren't provided in the constructor.
	 * @example
	 * 
	 * @property {number} textureScale - Controls texture scaling along the rope (0 = stretch)
	 */
	static defaultOptions: Partial<MeshRopeOptions>;
	/**
	 * Controls whether the rope's vertices are automatically recalculated each frame based on
	 * its points. When true, the rope will update to follow point movements. When false,
	 * manual updates are required.
	 * @example
	 * 
	 * @default true
	 */
	autoUpdate: boolean;
	/**
	 * Note: The wrap mode of the texture is set to REPEAT if `textureScale` is positive.
	 * @param options
	 * @param options.texture - The texture to use on the rope.
	 * @param options.points - An array of {@link math.Point} objects to construct this rope.
	 * @param {number} options.textureScale - Optional. Positive values scale rope texture
	 * keeping its aspect ratio. You can reduce alpha channel artifacts by providing a larger texture
	 * and downsampling here. If set to zero, texture will be stretched instead.
	 */
	constructor(options: MeshRopeOptions);
}
/**
 * Represents a particle with properties for position, scale, rotation, color, and texture.
 * Particles are lightweight alternatives to sprites, optimized for use in particle systems.
 * @example
 * 
 */
export interface IParticle {
	/** The x-coordinate of the particle position */
	x: number;
	/** The y-coordinate of the particle position */
	y: number;
	/**
	 * The horizontal scale factor of the particle
	 * @default 1
	 */
	scaleX: number;
	/**
	 * The vertical scale factor of the particle
	 * @default 1
	 */
	scaleY: number;
	/**
	 * The x-coordinate of the particle's anchor point (0-1 range)
	 * @default 0
	 */
	anchorX: number;
	/**
	 * The y-coordinate of the particle's anchor point (0-1 range)
	 * @default 0
	 */
	anchorY: number;
	/**
	 * The rotation of the particle in radians
	 * @default 0
	 */
	rotation: number;
	/**
	 * The color of the particle as a 32-bit RGBA value
	 * @default 0xffffffff
	 */
	color: number;
	/** The texture used to render this particle */
	texture: Texture;
}
/**
 * Configuration options for creating a new particle. All properties except texture are optional
 * and will use default values if not specified.
 * @example
 * 
 */
export type ParticleOptions = Omit<Partial<IParticle>, "color"> & {
	/** The texture used to render this particle */
	texture: Texture;
	/** The tint color as a hex number or CSS color string */
	tint?: ColorSource;
	/** The alpha transparency (0-1) */
	alpha?: number;
};
/**
 * Represents a single particle within a particle container. This class implements the IParticle interface,
 * providing properties and methods to manage the particle's position, scale, rotation, color, and texture.
 *
 * The reason we use a particle over a sprite is that these are much lighter weight and we can create a lot of them
 * without taking on the overhead of a full sprite.
 * @example
 * 
 */
export declare class Particle implements IParticle {
	/**
	 * Default options used when creating new particles. These values are applied when specific
	 * options aren't provided in the constructor.
	 * @example
	 * 
	 */
	static defaultOptions: Partial<ParticleOptions>;
	/**
	 * The x-coordinate of the anchor point (0-1).
	 * Controls the origin point for rotation and scaling.
	 * @example
	 * 
	 * @default 0
	 */
	anchorX: number;
	/**
	 * The y-coordinate of the anchor point (0-1).
	 * Controls the origin point for rotation and scaling.
	 * @example
	 * 
	 * @default 0
	 */
	anchorY: number;
	/**
	 * The x-coordinate of the particle in world space.
	 * @example
	 * 
	 * @default 0
	 */
	x: number;
	/**
	 * The y-coordinate of the particle in world space.
	 * @example
	 * 
	 * @default 0
	 */
	y: number;
	/**
	 * The horizontal scale factor of the particle.
	 * Values greater than 1 increase size, less than 1 decrease size.
	 * @example
	 * 
	 * @default 1
	 */
	scaleX: number;
	/**
	 * The vertical scale factor of the particle.
	 * Values greater than 1 increase size, less than 1 decrease size.
	 * @example
	 * 
	 * @default 1
	 */
	scaleY: number;
	/**
	 * The rotation of the particle in radians.
	 * Positive values rotate clockwise.
	 * @example
	 * 
	 * @default 0
	 */
	rotation: number;
	/**
	 * The color of the particle as a 32-bit RGBA value.
	 * Combines tint and alpha into a single value.
	 * @example
	 * 
	 * @default 0xffffffff
	 */
	color: number;
	/**
	 * The texture used to render this particle.
	 * All particles in a container should share the same base texture.
	 * @example
	 * 
	 */
	texture: Texture;
	constructor(options: Texture | ParticleOptions);
	/**
	 * The transparency of the particle. Values range from 0 (fully transparent)
	 * to 1 (fully opaque). Values outside this range are clamped.
	 * @example
	 * 
	 * @default 1
	 */
	get alpha(): number;
	set alpha(value: number);
	/**
	 * The tint color of the particle. Can be set using hex numbers or CSS color strings.
	 * The tint is multiplied with the texture color to create the final particle color.
	 * @example
	 * 
	 * @type {ColorSource} Hex number or CSS color string
	 * @default 0xffffff
	 */
	get tint(): number;
	set tint(value: ColorSource);
}
/**
 * Represents the properties of a particle that can be dynamically updated each frame.
 * These properties control which aspects of particles are recalculated during rendering.
 * Setting a property to true enables per-frame updates, while false only updates when manually triggered.
 * @example
 * 
 */
export interface ParticleProperties {
	/**
	 * When true, vertex positions are updated each frame.
	 * Useful for mesh deformation effects.
	 * @default false
	 */
	vertex?: boolean;
	/**
	 * When true, particle positions are updated each frame.
	 * Essential for moving particles.
	 * @default true
	 */
	position?: boolean;
	/**
	 * When true, rotation values are updated each frame.
	 * Needed for spinning particles.
	 * @default false
	 */
	rotation?: boolean;
	/**
	 * When true, texture coordinates are updated each frame.
	 * Required for texture animation.
	 * @default false
	 */
	uvs?: boolean;
	/**
	 * When true, color values are updated each frame.
	 * Enables color transitions and alpha changes.
	 * @default false
	 */
	color?: boolean;
}
/**
 * Options for configuring a ParticleContainer. Controls how particles are rendered, updated, and managed.
 * @example
 * 
 */
export interface ParticleContainerOptions extends PixiMixins.ParticleContainerOptions, Omit<ViewContainerOptions, "children"> {
	/**
	 * Specifies which particle properties should update each frame.
	 * Set properties to true for per-frame updates, false for static values.
	 * @default { position: true, rotation: false, vertex: false, uvs: false, color: false }
	 */
	dynamicProperties?: ParticleProperties & Record<string, boolean>;
	/**
	 * When true, particle positions are rounded to the nearest pixel.
	 * Helps achieve crisp rendering at the cost of smooth motion.
	 * @default false
	 */
	roundPixels?: boolean;
	/**
	 * The texture used for all particles in this container.
	 * If not provided, uses the texture of the first particle added.
	 */
	texture?: Texture;
	/** Initial array of particles to add to the container. All particles must share the same base texture. */
	particles?: IParticle[];
}
export interface ParticleContainer extends PixiMixins.ParticleContainer, ViewContainer<ParticleBuffer> {
}
/**
 * The ParticleContainer class is a highly optimized container that can render 1000s or particles at great speed.
 *
 * A ParticleContainer is specialized in that it can only contain and render particles. Particles are
 * lightweight objects that use minimal memory, which helps boost performance.
 *
 * It can render particles EXTREMELY fast!
 *
 * The tradeoff of using a ParticleContainer is that most advanced functionality is unavailable. Particles are simple
 * and cannot have children, filters, masks, etc. They possess only the basic properties: position, scale, rotation,
 * and color.
 *
 * All particles must share the same texture source (using something like a sprite sheet works well here).
 *
 * When creating a ParticleContainer, a developer can specify which of these properties are static and which are dynamic.
 * - Static properties are only updated when you add or remove a child, or when the `update` function is called.
 * - Dynamic properties are updated every frame.
 *
 * It is up to the developer to specify which properties are static and which are dynamic. Generally, the more static
 * properties you have (i.e., those that do not change per frame), the faster the rendering.
 *
 * If the developer modifies the children order or any static properties of the particle, they must call the `update` method.
 *
 * By default, only the `position` property is set to dynamic, which makes rendering very fast!
 *
 * Developers can also provide a custom shader to the particle container, allowing them to render particles in a custom way.
 *
 * To help with performance, the particle containers bounds are not calculated.
 * It's up to the developer to set the boundsArea property.
 *
 * It's extremely easy to use. Below is an example of rendering thousands of sprites at lightning speed.
 *
 * --------- EXPERIMENTAL ---------
 *
 * This is a new API, things may change and it may not work as expected.
 * We want to hear your feedback as we go!
 *
 * --------------------------------
 * @example
 * 
 */
export declare class ParticleContainer extends ViewContainer<ParticleBuffer> implements Instruction {
	/**
	 * Defines the default options for creating a ParticleContainer.
	 * @example
	 * 
	 * @property {Record<string, boolean>} dynamicProperties - Specifies which properties are dynamic.
	 * @property {boolean} roundPixels - Indicates if pixels should be  rounded.
	 */
	static defaultOptions: ParticleContainerOptions;
	/**
	 * An array of particles that are children of this ParticleContainer.
	 * This array can be modified directly for performance, but the 'update' method
	 * must be called afterwards to ensure the container is rendered correctly.
	 * @example
	 * 
	 */
	particleChildren: IParticle[];
	/**
	 * The texture used for rendering particles in this ParticleContainer. All particles
	 * must share the same base texture for optimal performance.
	 *
	 * > [!NOTE]
	 * > If not set, the texture of the first particle added to this container will be used.
	 * @example
	 * 
	 * @default null
	 */
	texture: Texture;
	/**
	 * @param options - The options for creating the sprite.
	 */
	constructor(options?: ParticleContainerOptions);
	/**
	 * Adds one or more particles to the container. The particles will be rendered using the container's shared texture
	 * and properties. When adding multiple particles, they must all share the same base texture.
	 * @example
	 * 
	 * @param children - The Particle(s) to add to the container
	 * @returns The first particle that was added, for method chaining
	 */
	addParticle(...children: IParticle[]): IParticle;
	/**
	 * Removes one or more particles from the container. The particles must already be children
	 * of this container to be removed.
	 * @example
	 * 
	 * @param children - The Particle(s) to remove from the container
	 * @returns The first particle that was removed, for method chaining
	 */
	removeParticle(...children: IParticle[]): IParticle;
	/**
	 * Updates the particle container's internal state. Call this method after manually modifying
	 * the particleChildren array or when changing static properties of particles.
	 * @example
	 * 
	 */
	update(): void;
	/**
	 * Returns a static empty bounds object since ParticleContainer does not calculate bounds automatically
	 * for performance reasons. Use the `boundsArea` property to manually set container bounds.
	 * @example
	 * 
	 * @returns {Bounds} An empty bounds object (0,0,0,0)
	 */
	get bounds(): Bounds;
	/**
	 * Destroys this sprite renderable and optionally its texture.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * particleContainer.destroy();
	 * particleContainer.destroy(true);
	 * particleContainer.destroy({ texture: true, textureSource: true, children: true });
	 */
	destroy(options?: DestroyOptions): void;
	/**
	 * Removes all particles from this container that are within the begin and end indexes.
	 * @param beginIndex - The beginning position.
	 * @param endIndex - The ending position. Default value is size of the container.
	 * @returns - List of removed particles
	 */
	removeParticles(beginIndex?: number, endIndex?: number): IParticle[];
	/**
	 * Removes a particle from the specified index position.
	 * @param index - The index to get the particle from
	 * @returns The particle that was removed.
	 */
	removeParticleAt<U extends IParticle>(index: number): U;
	/**
	 * Adds a particle to the container at a specified index. If the index is out of bounds an error will be thrown.
	 * If the particle is already in this container, it will be moved to the specified index.
	 * @param {Container} child - The particle to add.
	 * @param {number} index - The absolute index where the particle will be positioned at the end of the operation.
	 * @returns {Container} The particle that was added.
	 */
	addParticleAt<U extends IParticle>(child: U, index: number): U;
}
/**
 * A collection of textures or frame objects that can be used to create an `AnimatedSprite`.
 */
export type AnimatedSpriteFrames = Texture[] | FrameObject[];
/**
 * Constructor options used for `AnimatedSprite` instances. Allows configuration of animation
 * playback, speed, and texture frames.
 * @example
 * 
 */
export interface AnimatedSpriteOptions extends PixiMixins.AnimatedSpriteOptions, Omit<SpriteOptions, "texture"> {
	/**
	 * The speed that the AnimatedSprite will play at. Higher is faster, lower is slower.
	 * @example
	 * 
	 * @default 1
	 */
	animationSpeed?: number;
	/**
	 * Whether to start the animation immediately on creation.
	 * If set to `true`, the animation will start playing as soon as the
	 * `AnimatedSprite` is created.
	 * If set to `false`, you will need to call the `play` method to start the animation.
	 * @example
	 * 
	 * @default false
	 */
	autoPlay?: boolean;
	/**
	 * Whether to use Ticker.shared to auto update animation time.
	 * This is useful for animations that need to be updated every frame.
	 * If set to `false`, you will need to manually call the `update` method
	 * to update the animation.
	 * @example
	 * 
	 * @default true
	 */
	autoUpdate?: boolean;
	/**
	 * Whether or not the animation repeats after playing.
	 * @default true
	 */
	loop?: boolean;
	/**
	 * User-assigned function to call when an AnimatedSprite finishes playing.
	 * @example
	 * 
	 * @default null
	 */
	onComplete?: () => void;
	/**
	 * User-assigned function to call when an AnimatedSprite changes which texture is being rendered.
	 * @example
	 * 
	 * @default null
	 */
	onFrameChange?: (currentFrame: number) => void;
	/**
	 * User-assigned function to call when `loop` is true,
	 * and an AnimatedSprite is played and loops around to start again.
	 * @example
	 * 
	 * @default null
	 */
	onLoop?: () => void;
	/**
	 * An array of {@link Texture} or frame objects that make up the animation.
	 * @example
	 * 
	 */
	textures: AnimatedSpriteFrames;
	/**
	 * Update anchor to [Texture's defaultAnchor]{@link Texture#defaultAnchor} when frame changes.
	 *
	 * Useful with [sprite sheet animations]{@link Spritesheet#animations} created with tools.
	 * Changing anchor for each frame allows to pin sprite origin to certain moving feature
	 * of the frame (e.g. left foot).
	 * > [!NOTE] Enabling this will override any previously set `anchor` on each frame change.
	 * @example
	 * 
	 * @default false
	 */
	updateAnchor?: boolean;
}
export interface AnimatedSprite extends PixiMixins.AnimatedSprite, Sprite {
}
/**
 * An AnimatedSprite is a simple way to display an animation depicted by a list of textures.
 * @example
 * 
 *
 * The more efficient and simpler way to create an animated sprite is using a {@link Spritesheet}
 * containing the animation definitions:
 * @example
 * 
 */
export declare class AnimatedSprite extends Sprite {
	/**
	 * The speed that the AnimatedSprite will play at. Higher is faster, lower is slower.
	 * @example
	 * 
	 * @default 1
	 */
	animationSpeed: number;
	/**
	 * Whether or not the animation repeats after playing.
	 * When true, the animation will restart from the beginning after reaching the last frame.
	 * When false, the animation will stop on the last frame.
	 * @example
	 * 
	 * @default true
	 */
	loop: boolean;
	/**
	 * Update anchor to [Texture's defaultAnchor]{@link Texture#defaultAnchor} when frame changes.
	 *
	 * Useful with [sprite sheet animations]{@link Spritesheet#animations} created with tools.
	 * Changing anchor for each frame allows to pin sprite origin to certain moving feature
	 * of the frame (e.g. left foot).
	 *
	 * > [!NOTE] Enabling this will override any previously set `anchor` on each frame change.
	 * @default false
	 */
	updateAnchor: boolean;
	/**
	 * User-assigned function to call when an AnimatedSprite finishes playing.
	 *
	 * This function is called when the animation reaches the end and stops playing.
	 * If the animation is set to loop, this function will not be called.
	 * @example
	 * 
	 */
	onComplete?: () => void;
	/**
	 * User-assigned function to call when an AnimatedSprite changes which texture is being rendered.
	 *
	 * This function is called every time the current frame changes during playback.
	 * It receives the current frame index as an argument.
	 * @example
	 * animation.onFrameChange = () => {
	 *     // Updated!
	 * };
	 */
	onFrameChange?: (currentFrame: number) => void;
	/**
	 * User-assigned function to call when `loop` is true, and an AnimatedSprite is played and
	 * loops around to start again.
	 * @example
	 * animation.onLoop = () => {
	 *     // Looped!
	 * };
	 */
	onLoop?: () => void;
	/**
	 * @param frames - Collection of textures or frames to use.
	 * @param autoUpdate - Whether to use Ticker.shared to auto update animation time.
	 */
	constructor(frames: AnimatedSpriteFrames, autoUpdate?: boolean);
	/**
	 * @param options - The options for the AnimatedSprite.
	 */
	constructor(options: AnimatedSpriteOptions);
	/**
	 * Stops the animation playback and freezes the current frame.
	 * Does not reset the current frame or animation progress.
	 * @example
	 * 
	 */
	stop(): void;
	/**
	 * Starts or resumes the animation playback.
	 * If the animation was previously stopped, it will continue from where it left off.
	 * @example
	 * 
	 */
	play(): void;
	/**
	 * Stops the AnimatedSprite and sets it to a specific frame.
	 * @example
	 * 
	 * @param frameNumber - Frame index to stop at (0-based)
	 * @throws {Error} If frameNumber is out of bounds
	 */
	gotoAndStop(frameNumber: number): void;
	/**
	 * Goes to a specific frame and begins playing the AnimatedSprite from that point.
	 * Combines frame navigation and playback start in one operation.
	 * @example
	 * 
	 * @param frameNumber - Frame index to start playing from (0-based)
	 * @throws {Error} If frameNumber is out of bounds
	 */
	gotoAndPlay(frameNumber: number): void;
	/**
	 * Updates the object transform for rendering. This method handles animation timing, frame updates,
	 * and manages looping behavior.
	 * @example
	 * 
	 * @param ticker - The ticker to use for updating the animation timing
	 */
	update(ticker: Ticker): void;
	/**
	 * Stops the AnimatedSprite and destroys it.
	 * This method stops the animation playback, removes it from the ticker,
	 * and cleans up any resources associated with the sprite.
	 * @param options - Options for destroying the sprite, such as whether to remove from parent
	 * @example
	 * 
	 */
	destroy(options?: DestroyOptions): void;
	/**
	 * A short hand way of creating an AnimatedSprite from an array of frame ids.
	 * Uses texture frames from the cache to create an animation sequence.
	 * @example
	 * 
	 * @param frames - The array of frame ids to use for the animation
	 * @returns A new animated sprite using the frames
	 */
	static fromFrames(frames: string[]): AnimatedSprite;
	/**
	 * A short hand way of creating an AnimatedSprite from an array of image urls.
	 * Each image will be used as a frame in the animation.
	 * @example
	 * 
	 * @param images - The array of image urls to use as frames
	 * @returns A new animated sprite using the images as frames
	 */
	static fromImages(images: string[]): AnimatedSprite;
	/**
	 * The total number of frames in the AnimatedSprite. This is the same as number of textures
	 * assigned to the AnimatedSprite.
	 * @example
	 * 
	 * @returns {number} The total number of frames
	 */
	get totalFrames(): number;
	/**
	 * The array of textures or frame objects used for the animation sequence.
	 * Can be set to either an array of Textures or an array of FrameObjects with custom timing.
	 * @example
	 * 
	 * @type {AnimatedSpriteFrames}
	 */
	get textures(): AnimatedSpriteFrames;
	set textures(value: AnimatedSpriteFrames);
	/**
	 * Gets or sets the current frame index of the animation.
	 * When setting, the value will be clamped between 0 and totalFrames - 1.
	 * @example
	 * 
	 * @throws {Error} If attempting to set a frame index out of bounds
	 */
	get currentFrame(): number;
	set currentFrame(value: number);
	/**
	 * Indicates if the AnimatedSprite is currently playing.
	 * This is a read-only property that reflects the current playback state.
	 * @example
	 * 
	 * @returns {boolean} True if the animation is currently playing
	 */
	get playing(): boolean;
	/**
	 * Controls whether the animation automatically updates using the shared ticker.
	 * When enabled, the animation will update on each frame. When disabled, you must
	 * manually call update() to advance the animation.
	 * @example
	 * 
	 * @default true
	 */
	get autoUpdate(): boolean;
	set autoUpdate(value: boolean);
}
/**
 * Constructor options used for `NineSliceSprite` instances.
 * Defines how the sprite's texture is divided and scaled in nine sections.
 * <pre>
 *      A                          B
 *    +---+----------------------+---+
 *  C | 1 |          2           | 3 |
 *    +---+----------------------+---+
 *    |   |                      |   |
 *    | 4 |          5           | 6 |
 *    |   |                      |   |
 *    +---+----------------------+---+
 *  D | 7 |          8           | 9 |
 *    +---+----------------------+---+
 *  When changing this objects width and/or height:
 *     areas 1 3 7 and 9 will remain unscaled.
 *     areas 2 and 8 will be stretched horizontally
 *     areas 4 and 6 will be stretched vertically
 *     area 5 will be stretched both horizontally and vertically
 * </pre>
 * @example
 * 
 */
export interface NineSliceSpriteOptions extends PixiMixins.NineSliceSpriteOptions, ViewContainerOptions {
	/**
	 * The texture to use on the NineSliceSprite.
	 * 
	 * @default Texture.EMPTY
	 */
	texture: Texture;
	/**
	 * Width of the left vertical bar (A).
	 * Controls the size of the left edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	leftWidth?: number;
	/**
	 * Height of the top horizontal bar (C).
	 * Controls the size of the top edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	topHeight?: number;
	/**
	 * Width of the right vertical bar (B).
	 * Controls the size of the right edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	rightWidth?: number;
	/**
	 * Height of the bottom horizontal bar (D).
	 * Controls the size of the bottom edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	bottomHeight?: number;
	/**
	 * Width of the NineSliceSprite.
	 * Modifies the vertices directly rather than UV coordinates
	 * @example
	 * 
	 * @default 100
	 */
	width?: number;
	/**
	 * Height of the NineSliceSprite.
	 * Modifies the vertices directly rather than UV coordinates
	 * @example
	 * 
	 * @default 100
	 */
	height?: number;
	/**
	 * Whether to round the x/y position to whole pixels
	 * @example
	 * 
	 * @default false
	 */
	roundPixels?: boolean;
	/**
	 * The anchor point of the NineSliceSprite (0-1 range)
	 *
	 * Controls the origin point for rotation, scaling, and positioning.
	 * Can be a number for uniform anchor or a PointData for separate x/y values.
	 * @default 0
	 * @example
	 * 
	 */
	anchor?: PointData | number;
}
export interface NineSliceSprite extends PixiMixins.NineSliceSprite, ViewContainer<NineSliceSpriteGpuData> {
}
/**
 * The NineSliceSprite allows you to stretch a texture using 9-slice scaling. The corners will remain unscaled (useful
 * for buttons with rounded corners for example) and the other areas will be scaled horizontally and or vertically
 *
 * <pre>
 *      A                          B
 *    +---+----------------------+---+
 *  C | 1 |          2           | 3 |
 *    +---+----------------------+---+
 *    |   |                      |   |
 *    | 4 |          5           | 6 |
 *    |   |                      |   |
 *    +---+----------------------+---+
 *  D | 7 |          8           | 9 |
 *    +---+----------------------+---+
 *  When changing this objects width and/or height:
 *     areas 1 3 7 and 9 will remain unscaled.
 *     areas 2 and 8 will be stretched horizontally
 *     areas 4 and 6 will be stretched vertically
 *     area 5 will be stretched both horizontally and vertically
 * </pre>
 * @example
 * 
 */
export declare class NineSliceSprite extends ViewContainer<NineSliceSpriteGpuData> implements View {
	/**
	 * The default options used to override initial values of any options passed in the constructor.
	 * These values are used as fallbacks when specific options are not provided.
	 * @example
	 * 
	 * @type {NineSliceSpriteOptions}
	 */
	static defaultOptions: NineSliceSpriteOptions;
	constructor(options: NineSliceSpriteOptions | Texture);
	/**
	 * The anchor sets the origin point of the sprite. The default value is taken from the {@link Texture}
	 * and passed to the constructor.
	 *
	 * - The default is `(0,0)`, this means the sprite's origin is the top left.
	 * - Setting the anchor to `(0.5,0.5)` means the sprite's origin is centered.
	 * - Setting the anchor to `(1,1)` would mean the sprite's origin point will be the bottom right corner.
	 *
	 * If you pass only single parameter, it will set both x and y to the same value as shown in the example below.
	 * @example
	 * 
	 */
	get anchor(): ObservablePoint;
	set anchor(value: PointData | number);
	/**
	 * The width of the NineSliceSprite, setting this will actually modify the vertices and UV's of this plane.
	 * The width affects how the middle sections are scaled.
	 * @example
	 * 
	 */
	get width(): number;
	set width(value: number);
	/**
	 * The height of the NineSliceSprite, setting this will actually modify the vertices and UV's of this plane.
	 * The height affects how the middle sections are scaled.
	 * @example
	 * 
	 */
	get height(): number;
	set height(value: number);
	/**
	 * Sets the size of the NineSliceSprite to the specified width and height.
	 * This method directly modifies the vertices and UV coordinates of the sprite.
	 *
	 * Using this is more efficient than setting width and height separately as it only triggers one update.
	 * @example
	 * 
	 * @param value - This can be either a number or a Size object with width/height properties
	 * @param height - The height to set. Defaults to the value of `width` if not provided
	 */
	setSize(value: number | Optional<Size, "height">, height?: number): void;
	/**
	 * Retrieves the size of the NineSliceSprite as a [Size]{@link Size} object.
	 * This method is more efficient than getting width and height separately.
	 * @example
	 * 
	 * @param out - Optional object to store the size in, to avoid allocating a new object
	 * @returns The size of the NineSliceSprite
	 */
	getSize(out?: Size): Size;
	/**
	 * Width of the left vertical bar (A).
	 * Controls the size of the left edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	get leftWidth(): number;
	set leftWidth(value: number);
	/**
	 * Height of the top horizontal bar (C).
	 * Controls the size of the top edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	get topHeight(): number;
	set topHeight(value: number);
	/**
	 * Width of the right vertical bar (B).
	 * Controls the size of the right edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	get rightWidth(): number;
	set rightWidth(value: number);
	/**
	 * Height of the bottom horizontal bar (D).
	 * Controls the size of the bottom edge that remains unscaled
	 * @example
	 * 
	 * @default 10
	 */
	get bottomHeight(): number;
	set bottomHeight(value: number);
	/**
	 * The texture to use on the NineSliceSprite.
	 * 
	 * @default Texture.EMPTY
	 */
	get texture(): Texture;
	set texture(value: Texture);
	/**
	 * The original width of the texture before any nine-slice scaling.
	 * This is the width of the source texture used to create the nine-slice sprite.
	 * @example
	 * 
	 * @returns The original width of the texture
	 */
	get originalWidth(): number;
	/**
	 * The original height of the texture before any nine-slice scaling.
	 * This is the height of the source texture used to create the nine-slice sprite.
	 * @example
	 * 
	 * @returns The original height of the texture
	 */
	get originalHeight(): number;
	/**
	 * Destroys this sprite renderable and optionally its texture.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * nineSliceSprite.destroy();
	 * nineSliceSprite.destroy(true);
	 * nineSliceSprite.destroy({ texture: true, textureSource: true });
	 */
	destroy(options?: DestroyOptions): void;
}
/**
 * Please use the {@link NineSliceSprite} class instead.
 * The NineSlicePlane is deprecated and will be removed in future versions.
 * @deprecated since 8.0.0
 */
export declare class NineSlicePlane extends NineSliceSprite {
	constructor(options: NineSliceSpriteOptions | Texture);
	/** @deprecated since 8.0.0 */
	constructor(texture: Texture, leftWidth: number, topHeight: number, rightWidth: number, bottomHeight: number);
}
/**
 * The Transform class facilitates the manipulation of a 2D transformation matrix through
 * user-friendly properties: position, scale, rotation, skew, and pivot.
 * @example
 * 
 * @remarks
 * - Manages 2D transformation properties
 * - Auto-updates matrix on changes
 * - Supports observable changes
 * - Common in display objects
 */
export declare class Transform {
	/**
	 * The coordinate of the object relative to the local coordinates of the parent.
	 * @example
	 * 
	 */
	position: ObservablePoint;
	/**
	 * The scale factor of the object.
	 * @example
	 * 
	 */
	scale: ObservablePoint;
	/**
	 * The pivot point of the container that it rotates around.
	 * @example
	 * 
	 */
	pivot: ObservablePoint;
	/**
	 * The skew amount, on the x and y axis.
	 * @example
	 * 
	 */
	skew: ObservablePoint;
	/**
	 * @param options - Options for the transform.
	 * @param options.matrix - The matrix to use.
	 * @param options.observer - The observer to use.
	 */
	constructor({ matrix, observer }?: TransformOptions);
	/**
	 * The transformation matrix computed from the transform's properties.
	 * Combines position, scale, rotation, skew, and pivot into a single matrix.
	 * @example
	 * 
	 */
	get matrix(): Matrix;
	toString(): string;
	/**
	 * Decomposes a matrix and sets the transforms properties based on it.
	 * @example
	 * 
	 * @param matrix - The matrix to decompose
	 */
	setFromMatrix(matrix: Matrix): void;
	/**
	 * The rotation of the object in radians.
	 * @example
	 * 
	 */
	get rotation(): number;
	set rotation(value: number);
}
/**
 * Constructor options used for creating a TilingSprite instance.
 * Defines the texture, tiling behavior, and rendering properties of the sprite.
 * @example
 * 
 */
export interface TilingSpriteOptions extends PixiMixins.TilingSpriteOptions, ViewContainerOptions {
	/**
	 * The anchor point of the TilingSprite (0-1 range)
	 *
	 * Controls the origin point for rotation, scaling, and positioning.
	 * Can be a number for uniform anchor or a PointData for separate x/y values.
	 * @example
	 * 
	 * @default 0
	 */
	anchor?: PointData | number;
	/**
	 * The offset of the tiling texture.
	 * Used to scroll or position the repeated pattern.
	 * @example
	 * 
	 * @default {x: 0, y: 0}
	 */
	tilePosition?: PointData;
	/**
	 * Scale of the tiling texture.
	 * Affects the size of each repeated instance of the texture.
	 * @example
	 * 
	 * @default {x: 1, y: 1}
	 */
	tileScale?: PointData;
	/**
	 * Rotation of the tiling texture in radians.
	 * This controls the rotation applied to the texture before tiling.
	 * @example
	 * 
	 * @default 0
	 */
	tileRotation?: number;
	/**
	 * The texture to use for tiling.
	 * This is the image that will be repeated across the sprite.
	 * @example
	 * 
	 * @default Texture.WHITE
	 */
	texture?: Texture;
	/**
	 * The width of the tiling area.
	 * This defines how wide the tiling sprite will be.
	 * @example
	 * 
	 * @default 256
	 */
	width?: number;
	/**
	 * The height of the tiling area.
	 * This defines how tall the tiling sprite will be.
	 * @example
	 * 
	 * @default 256
	 */
	height?: number;
	/**
	 * Whether the tiling pattern should originate from the anchor point.
	 * When true, tiling starts from the origin instead of top-left.
	 *
	 * This will make the texture coordinates assigned to each vertex dependent on the value of the anchor. Without
	 * this, the top-left corner always gets the (0, 0) texture coordinate.
	 * @example
	 * 
	 * @default false
	 */
	applyAnchorToTexture?: boolean;
	/**
	 * Whether to round the sprite's position to whole pixels.
	 * This can help with crisp rendering, especially for pixel art.
	 * When true, the sprite's position will be rounded to the nearest pixel.
	 * @example
	 * 
	 * @default false
	 */
	roundPixels?: boolean;
}
export interface TilingSprite extends PixiMixins.TilingSprite, ViewContainer<TilingSpriteGpuData> {
}
/**
 * A TilingSprite is a fast and efficient way to render a repeating texture across a given area.
 * The texture can be scrolled, scaled, and rotated independently of the sprite itself.
 * @example
 * 
 */
export declare class TilingSprite extends ViewContainer<TilingSpriteGpuData> implements View, Instruction {
	/**
	 * Creates a new tiling sprite based on a source texture or image path.
	 * This is a convenience method that automatically creates and manages textures.
	 * @example
	 * 
	 * @param source - The source to create the sprite from. Can be a path to an image or a texture
	 * @param options - Additional options for the tiling sprite
	 * @returns A new tiling sprite based on the source
	 */
	static from(source: Texture | string, options?: TilingSpriteOptions): TilingSprite;
	/**
	 * Default options used when creating a TilingSprite instance.
	 * These values are used as fallbacks when specific options are not provided.
	 * @example
	 * 
	 * @type {TilingSpriteOptions}
	 */
	static defaultOptions: TilingSpriteOptions;
	/**
	 * Flags whether the tiling pattern should originate from the origin instead of the top-left corner in
	 * local space.
	 *
	 * This will make the texture coordinates assigned to each vertex dependent on the value of the anchor. Without
	 * this, the top-left corner always gets the (0, 0) texture coordinate.
	 * @example
	 * 
	 * @default false
	 */
	applyAnchorToTexture: boolean;
	/**
	 * @param {Texture | TilingSpriteOptions} options - The options for creating the tiling sprite.
	 */
	constructor(options?: Texture | TilingSpriteOptions);
	/** @deprecated since 8.0.0 */
	constructor(texture: Texture, width: number, height: number);
	/**
	 * The anchor sets the origin point of the sprite. The default value is taken from the {@link Texture}
	 * and passed to the constructor.
	 *
	 * - The default is `(0,0)`, this means the sprite's origin is the top left.
	 * - Setting the anchor to `(0.5,0.5)` means the sprite's origin is centered.
	 * - Setting the anchor to `(1,1)` would mean the sprite's origin point will be the bottom right corner.
	 *
	 * If you pass only single parameter, it will set both x and y to the same value as shown in the example below.
	 * @example
	 * 
	 */
	get anchor(): ObservablePoint;
	set anchor(value: PointData | number);
	/**
	 * The offset of the tiling texture.
	 * Used to scroll or position the repeated pattern.
	 * @example
	 * 
	 * @default {x: 0, y: 0}
	 */
	get tilePosition(): ObservablePoint;
	set tilePosition(value: PointData);
	/**
	 * Scale of the tiling texture.
	 * Affects the size of each repeated instance of the texture.
	 * @example
	 * 
	 * @default {x: 1, y: 1}
	 */
	get tileScale(): ObservablePoint;
	set tileScale(value: PointData | number);
	set tileRotation(value: number);
	/**
	 * Rotation of the tiling texture in radians.
	 * This controls the rotation applied to the texture before tiling.
	 * @example
	 * 
	 * @default 0
	 */
	get tileRotation(): number;
	set texture(value: Texture);
	/**
	 * The texture to use for tiling.
	 * This is the image that will be repeated across the sprite.
	 * @example
	 * 
	 * @default Texture.WHITE
	 */
	get texture(): Texture;
	/**
	 * The width of the tiling area. This defines how wide the area is that the texture will be tiled across.
	 * @example
	 * 
	 */
	set width(value: number);
	get width(): number;
	set height(value: number);
	/**
	 * The height of the tiling area. This defines how tall the area is that the texture will be tiled across.
	 * @example
	 * 
	 */
	get height(): number;
	/**
	 * Sets the size of the TilingSprite to the specified width and height.
	 * This is faster than setting width and height separately as it only triggers one update.
	 * @example
	 * 
	 * @param value - This can be either a number for uniform sizing or a Size object with width/height properties
	 * @param height - The height to set. Defaults to the value of `width` if not provided
	 */
	setSize(value: number | Optional<Size, "height">, height?: number): void;
	/**
	 * Retrieves the size of the TilingSprite as a {@link Size} object.
	 * This method is more efficient than getting width and height separately as it only allocates one object.
	 * @example
	 * 
	 * @param out - Optional object to store the size in, to avoid allocating a new object
	 * @returns The size of the TilingSprite
	 */
	getSize(out?: Size): Size;
	/**
	 * Checks if the object contains the given point in local coordinates.
	 * Takes into account the anchor offset when determining boundaries.
	 * @example
	 * 
	 * @param point - The point to check in local coordinates
	 * @returns True if the point is within the sprite's bounds
	 */
	containsPoint(point: PointData): boolean;
	/**
	 * Destroys this sprite renderable and optionally its texture.
	 * @param options - Options parameter. A boolean will act as if all options
	 *  have been set to that value
	 * @example
	 * tilingSprite.destroy();
	 * tilingSprite.destroy(true);
	 * tilingSprite.destroy({ texture: true, textureSource: true });
	 */
	destroy(options?: DestroyOptions): void;
}
interface BitmapFontEvents<Type> {
	destroy: [
		Type
	];
}
/**
 * A fully resolved asset, with all the information needed to load it.
 * This represents an asset that has been processed by the resolver and is ready to be loaded.
 * @example
 * 
 */
export interface ResolvedAsset<T = any> {
	/** Array of alternative names for this asset. Used for looking up the same asset by different keys. */
	alias?: string[];
	/** The URL or relative path to the asset. This is the final, resolved path that will be used for loading. */
	src?: string;
	/**
	 * Optional data passed to the asset loader.
	 * Can include texture settings, parser options, or other asset-specific data.
	 */
	data?: T;
	/** File format of the asset, usually the file extension. Used to determine which loader parser to use. */
	format?: string;
	/**
	 * @deprecated Use `parser` instead.
	 */
	loadParser?: LoadParserName;
	/** Override to specify which parser should load this asset. Useful when file extensions don't match the content type. */
	parser?: AssetParser;
	/**
	 * The amount of progress an asset will contribute to the onProgress event when loading.
	 * This can be any arbitrary value but typically represents the file size.
	 * @default 1
	 */
	progressSize?: number;
}
/**
 * A valid asset source specification. This can be a URL string, a {@link ResolvedSrc},
 * or an array of either. The source defines where and how to load an asset.
 * @example
 * 
 * @remarks
 * When specifying multiple formats:
 * - The format that is selected will depend on {@link AssetInitOptions.texturePreference}
 * - Resolution is parsed from file names
 * - Custom data can be passed to loaders
 */
export type AssetSrc = ArrayOr<string> | (ArrayOr<ResolvedSrc> & {
	[key: string]: any;
});
/**
 * An asset that has not been resolved yet. This is the initial format used when adding assets
 * to the Assets system before they are processed into a {@link ResolvedAsset}.
 * @example
 * 
 * @remarks
 * - Used as input format when adding assets to the system
 * - Can specify multiple aliases for the same asset
 * - Supports format patterns for browser compatibility
 * - Can include loader-specific data and options
 */
export type UnresolvedAsset<T = any> = Pick<ResolvedAsset<T>, "data" | "format" | "loadParser" | "parser"> & {
	/** Aliases associated with asset */
	alias?: ArrayOr<string>;
	/** The URL or relative path to the asset */
	src?: AssetSrc;
	[key: string]: any;
};
/**
 * Structure of a bundle found in a {@link AssetsManifest} file. Bundles allow you to
 * group related assets together for easier management and loading.
 * @example
 * 
 */
export interface AssetsBundle {
	/** Unique identifier for the bundle */
	name: string;
	/** Assets contained in the bundle. Can be an array of assets or a record mapping aliases to sources. */
	assets: UnresolvedAsset[] | Record<string, ArrayOr<string> | UnresolvedAsset>;
}
/**
 * The manifest format for defining all assets in your application. Manifests provide a
 * structured way to organize and manage your assets through bundles.
 * @example
 * 
 */
export interface AssetsManifest {
	/** Array of asset bundles that make up the manifest */
	bundles: AssetsBundle[];
}
declare class CacheClass {
	/** Clear all entries. */
	reset(): void;
	/**
	 * Check if the key exists
	 * @param key - The key to check
	 */
	has(key: any): boolean;
	/**
	 * Fetch entry by key
	 * @param key - The key of the entry to get
	 */
	get<T = any>(key: any): T;
	/**
	 * Set a value by key or keys name
	 * @param key - The key or keys to set
	 * @param value - The value to store in the cache or from which cacheable assets will be derived.
	 */
	set<T = any>(key: any | any[], value: T): void;
	/**
	 * Remove entry by key
	 *
	 * This function will also remove any associated alias from the cache also.
	 * @param key - The key of the entry to remove
	 */
	remove(key: any): void;
}
/**
 * A prefer order lets the resolver know which assets to prefer depending on the various parameters passed to it.
 */
export interface PreferOrder {
	/** the importance order of the params */
	priority?: string[];
	params: {
		[key: string]: any;
	};
}
/**
 * Callback function for tracking asset loading progress. The function is called repeatedly
 * during the loading process with a progress value between 0.0 and 1.0.
 * @param progress - The loading progress from 0.0 (started) to 1.0 (complete)
 * @returns void
 * @example
 * 
 * > [!IMPORTANT] Do not rely on the progress callback to determine when all assets are loaded.
 * > Use the returned promise from `Assets.load()` or `Assets.loadBundle()` to know when loading is complete.
 */
export type ProgressCallback = (progress: number) => void;
/**
 * Options for initializing the Assets class. These options configure how assets are loaded,
 * resolved, and managed in your PixiJS application.
 */
export interface AssetInitOptions {
	/**
	 * Base path prepended to all asset URLs. Useful for CDN hosting.
	 * @example
	 * 
	 */
	basePath?: string;
	/**
	 * A manifest defining all your application's assets.
	 * Can be a URL to a JSON file or a manifest object.
	 * @example
	 * 
	 */
	manifest?: string | AssetsManifest;
	/**
	 * Configure texture loading preferences.
	 * Useful for optimizing asset delivery based on device capabilities.
	 * @example
	 * 
	 */
	texturePreference?: {
		/** Preferred texture resolution(s). Can be a single number or array of resolutions in order of preference. */
		resolution?: number | number[];
		/** Preferred texture formats in order of preference. Default: ['avif', 'webp', 'png', 'jpg', 'jpeg'] */
		format?: ArrayOr<string>;
	};
	/**
	 * Optional preferences for asset loading behavior.
	 * @example
	 * 
	 */
	preferences?: Partial<AssetsPreferences>;
	/**
	 * Options for defining the loading behavior of assets.
	 * @example
	 * 
	 * @remarks
	 * - `onProgress` callback receives values from 0.0 to 1.0
	 * - `onError` callback is invoked for individual asset load failures
	 * - `strategy` can be 'throw' (default), 'retry', or 'skip'
	 * - `retryCount` sets how many times to retry failed assets (default 3)
	 * - `retryDelay` sets the delay between retries in milliseconds (default 250ms)
	 */
	loadOptions?: Partial<LoadOptions>;
}
/**
 * The global Assets class is a singleton that manages loading, caching, and unloading of all resources
 * in your PixiJS application.
 *
 * Key responsibilities:
 * - **URL Resolution**: Maps URLs/keys to browser-compatible resources
 * - **Resource Loading**: Handles loading and transformation of assets
 * - **Asset Caching**: Manages a global cache to prevent duplicate loads
 * - **Memory Management**: Provides unloading capabilities to free memory
 *
 * Advanced Features:
 * - **Asset Bundles**: Group and manage related assets together
 * - **Background Loading**: Load assets before they're needed over time
 * - **Format Detection**: Automatically select optimal asset formats
 *
 * Supported Asset Types:
 * | Type                | Extensions                                                       | Loaders                                                               |
 * | ------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------- |
 * | Textures            | `.png`, `.jpg`, `.gif`, `.webp`, `.avif`, `.svg`                 | {@link loadTextures}, {@link loadSvg}                                 |
 * | Video Textures      | `.mp4`, `.m4v`, `.webm`, `.ogg`, `.ogv`, `.h264`, `.avi`, `.mov` | {@link loadVideoTextures}                                             |
 * | Sprite Sheets       | `.json`                                                          | {@link spritesheetAsset}                                              |
 * | Bitmap Fonts        | `.fnt`, `.xml`, `.txt`                                           | {@link loadBitmapFont}                                                |
 * | Web Fonts           | `.ttf`, `.otf`, `.woff`, `.woff2`                                | {@link loadWebFont}                                                   |
 * | JSON                | `.json`                                                          | {@link loadJson}                                                      |
 * | Text                | `.txt`                                                           | {@link loadTxt}                                                       |
 * | Compressed Textures | `.basis`, `.dds`, `.ktx`, `.ktx2`                                | {@link loadBasis}, {@link loadDDS}, {@link loadKTX}, {@link loadKTX2} |
 * > [!NOTE] Some loaders allow for custom configuration, please refer to the specific loader documentation for details.
 * @example
 * 
 * @remarks
 * - Assets are cached automatically and only loaded once
 * - Background loading helps eliminate loading screens
 * - Format detection ensures optimal asset delivery
 * - Bundle management simplifies resource organization
 *
 * > [!IMPORTANT]
 * > When unloading assets, ensure they aren't being used elsewhere
 * > in your application to prevent missing texture references.
 */
export declare const Assets: AssetsClass;
/**
 * Options for loading assets with the Loader
 * @example
 * 
 */
export interface LoadOptions {
	/**
	 * Callback for progress updates during loading
	 * @param progress - A number between 0 and 1 indicating the load progress
	 * @example
	 * 
	 */
	onProgress?: (progress: number) => void;
	/**
	 * Callback for handling errors during loading
	 * @param error - The error that occurred
	 * @param url - The URL of the asset that failed to load
	 * @example
	 * 
	 */
	onError?: (error: Error, url: string | ResolvedAsset) => void;
	/**
	 * Strategy to handle load failures
	 * - 'throw': Immediately throw an error and stop loading (default)
	 * - 'skip': Skip the failed asset and continue loading others
	 * - 'retry': Retry loading the asset a specified number of times
	 * @default 'throw'
	 * @example
	 * 
	 */
	strategy?: "throw" | "skip" | "retry";
	/**
	 * Number of retry attempts if strategy is 'retry'
	 * @default 3
	 * @example
	 * 
	 */
	retryCount?: number;
	/**
	 * Delay in milliseconds between retry attempts
	 * @default 250
	 * @example
	 * 
	 */
	retryDelay?: number;
}
/**
 * The options for installing a new BitmapFont. Once installed, the font will be available
 * for use in BitmapText objects through the fontFamily property of TextStyle.
 * @example
 * 
 */
export interface BitmapFontInstallOptions {
	/**
	 * The name of the font. This will be used as the fontFamily in text styles to access this font.
	 * Must be unique across all installed bitmap fonts.
	 * @example
	 * 
	 */
	name?: string;
	/**
	 * Characters included in the font set. You can specify individual characters or ranges.
	 * Don't forget to include spaces ' ' in your character set!
	 * @default BitmapFont.ALPHANUMERIC
	 * @example
	 * 
	 */
	chars?: string | (string | string[])[];
	/**
	 * Render resolution for glyphs. Higher values create sharper text at the cost of memory.
	 * Useful for supporting high-DPI displays.
	 * @default 1
	 * @example
	 * 
	 */
	resolution?: number;
	/**
	 * Padding between glyphs on texture atlas. Balances visual quality with texture space.
	 * - Lower values: More compact, but may have visual artifacts
	 * - Higher values: Better quality, but uses more texture space
	 * @default 4
	 * @example
	 * 
	 */
	padding?: number;
	/**
	 * Skip generation of kerning information for the BitmapFont.
	 * - true: Faster generation, but text may have inconsistent spacing
	 * - false: Better text appearance, but slower generation
	 * @default false
	 * @example
	 * 
	 */
	skipKerning?: boolean;
	/**
	 * Style options to render the BitmapFont with.
	 * Supports all TextStyle properties including fill, stroke, and shadow effects.
	 * @example
	 * 
	 */
	style?: TextStyle | TextStyleOptions;
	/**
	 * Optional texture style to use when creating the font textures.
	 * Controls how the font textures are rendered and filtered.
	 * @example
	 * 
	 */
	textureStyle?: TextureStyle | TextureStyleOptions;
	/**
	 * Whether to allow overriding the fill color with a tint at runtime.
	 *
	 * When enabled, the font can be dynamically tinted using the `tint` property of BitmapText,
	 * allowing a single font to display multiple colors without creating separate font textures.
	 * This is memory efficient but requires the font to be rendered with white fill color.
	 *
	 * When disabled, the fill color is permanently baked into the font texture. This allows
	 * any fill color but prevents runtime tinting - each color variation requires a separate font.
	 * @default false (automatically determined based on style)
	 *
	 * **Requirements for tinting:**
	 * - Fill color must be white (`0xFFFFFF` or `'#ffffff'`)
	 * - No stroke effects
	 * - No drop shadows (or only black shadows)
	 * - No gradient or pattern fills
	 *
	 * **Performance considerations:**
	 * - ✅ Enabled: One font texture, multiple colors via tinting (memory efficient)
	 * - ❌ Disabled: Separate font texture per color (higher memory usage)
	 * @example
	 * 
	 * @example
	 * 
	 * @example
	 * 
	 */
	dynamicFill?: boolean;
}
declare class BitmapFontManagerClass {
	/**
	 * This character set includes all the letters in the alphabet (both lower- and upper- case).
	 * @type {string[][]}
	 * @example
	 * BitmapFont.from('ExampleFont', style, { chars: BitmapFont.ALPHA })
	 */
	readonly ALPHA: (string | string[])[];
	/**
	 * This character set includes all decimal digits (from 0 to 9).
	 * @type {string[][]}
	 * @example
	 * BitmapFont.from('ExampleFont', style, { chars: BitmapFont.NUMERIC })
	 */
	readonly NUMERIC: string[][];
	/**
	 * This character set is the union of `BitmapFont.ALPHA` and `BitmapFont.NUMERIC`.
	 * @type {string[][]}
	 */
	readonly ALPHANUMERIC: (string | string[])[];
	/**
	 * This character set consists of all the ASCII table.
	 * @type {string[][]}
	 */
	readonly ASCII: string[][];
	/** Default options for installing a new BitmapFont. */
	defaultOptions: Omit<BitmapFontInstallOptions, "style">;
	/** Cache for measured text layouts to avoid recalculating them multiple times. */
	readonly measureCache: import("tiny-lru").LRU<BitmapTextLayoutData>;
	/**
	 * Get a font for the specified text and style.
	 * @param text - The text to get the font for
	 * @param style - The style to use
	 */
	getFont(text: string, style: TextStyle): BitmapFont;
	/**
	 * Get the layout of a text for the specified style.
	 * @param text - The text to get the layout for
	 * @param style - The style to use
	 * @param trimEnd - Whether to ignore whitespaces at the end of each line
	 */
	getLayout(text: string, style: TextStyle, trimEnd?: boolean): BitmapTextLayoutData;
	/**
	 * Measure the text using the specified style.
	 * @param text - The text to measure
	 * @param style - The style to use
	 * @param trimEnd - Whether to ignore whitespaces at the end of each line
	 */
	measureText(text: string, style: TextStyle, trimEnd?: boolean): {
		width: number;
		height: number;
		scale: number;
		offsetY: number;
	};
	/**
	 * Generates a bitmap-font for the given style and character set
	 * @param options - Setup options for font generation.
	 * @returns Font generated by style options.
	 * @example
	 * import { BitmapFontManager, BitmapText } from 'pixi.js';
	 *
	 * BitmapFontManager.install('TitleFont', {
	 *     fontFamily: 'Arial',
	 *     fontSize: 12,
	 *     strokeThickness: 2,
	 *     fill: 'purple',
	 * });
	 *
	 * const title = new BitmapText({ text: 'This is the title', fontFamily: 'TitleFont' });
	 */
	install(options: BitmapFontInstallOptions): BitmapFont;
	/** @deprecated since 7.0.0 */
	install(name: string, style?: TextStyle | TextStyleOptions, options?: BitmapFontInstallOptions): BitmapFont;
	/**
	 * Uninstalls a bitmap font from the cache.
	 * @param {string} name - The name of the bitmap font to uninstall.
	 */
	uninstall(name: string): void;
}
/**
 * Options for creating a BitmapFont. Used when loading or creating bitmap fonts from existing textures and data.
 * @example
 * 
 */
export interface BitmapFontOptions {
	/**
	 * The bitmap font data containing character metrics, layout information,
	 * and font properties. This includes character positions, dimensions,
	 * kerning data, and general font settings.
	 */
	data: BitmapFontData;
	/**
	 * Array of textures containing the font glyphs. Each texture corresponds
	 * to a page in the font data. For simple fonts this is typically just
	 * one texture, but complex fonts may split glyphs across multiple textures.
	 */
	textures: Texture[];
}
/**
 * A BitmapFont object represents a particular font face, size, and style.
 * This class handles both pre-loaded bitmap fonts and dynamically generated ones.
 * @example
 * 
 */
export declare class BitmapFont extends AbstractBitmapFont<BitmapFont> {
	/**
	 * The URL from which the font was loaded, if applicable.
	 * This is useful for tracking font sources and reloading.
	 * @example
	 * 
	 */
	url?: string;
	constructor(options: BitmapFontOptions, url?: string);
	/** Destroys the BitmapFont object. */
	destroy(): void;
	/**
	 * Generates and installs a bitmap font with the specified options.
	 * The font will be cached and available for use in BitmapText objects.
	 * @param options - Setup options for font generation
	 * @returns Installed font instance
	 * @example
	 * 
	 */
	static install(options: BitmapFontInstallOptions): void;
	/**
	 * Uninstalls a bitmap font from the cache.
	 * This frees up memory and resources associated with the font.
	 * @param name - The name of the bitmap font to uninstall
	 * @example
	 * 
	 */
	static uninstall(name: string): void;
}
export interface BitmapText extends PixiMixins.BitmapText, AbstractText<TextStyle, TextStyleOptions, TextOptions, BitmapTextGraphics> {
}
/**
 * A BitmapText object creates text using pre-rendered bitmap fonts.
 * It supports both loaded bitmap fonts (XML/FNT) and dynamically generated ones.
 *
 * To split a line you can use '\n' in your text string, or use the `wordWrap` and
 * `wordWrapWidth` style properties.
 *
 * Key Features:
 * - High-performance text rendering using pre-generated textures
 * - Support for both pre-loaded and dynamic bitmap fonts
 * - Compatible with MSDF/SDF fonts for crisp scaling
 * - Automatic font reuse and optimization
 *
 * Performance Benefits:
 * - Faster rendering compared to Canvas/HTML text
 * - Lower memory usage for repeated characters
 * - More efficient text changes
 * - Better batching capabilities
 *
 * Limitations:
 * - Full character set support is impractical due to the number of chars (mainly affects CJK languages)
 * - Initial font generation/loading overhead
 * - Less flexible styling compared to Canvas/HTML text
 * @example
 * 
 *
 * Font Types:
 * 1. Pre-loaded Bitmap Fonts:
 *    - Load via Asset Manager (XML/FNT formats)
 *    - Support for MSDF/SDF fonts
 *    - Create using tools like https://msdf-bmfont.donmccurdy.com/
 *
 * 2. Dynamic Bitmap Fonts:
 *    - Generated at runtime from system fonts
 *    - Automatic font reuse and optimization
 *    - Smart scaling for similar font sizes
 *
 * Font Management:
 * - Automatic font generation when needed
 * - Manual pre-installation via `BitmapFont.install`
 * - Smart font reuse to optimize memory
 * - Scale existing fonts instead of generating new ones when possible
 */
export declare class BitmapText extends AbstractText<TextStyle, TextStyleOptions, TextOptions, BitmapTextGraphics> implements View {
	/**
	 * **Note:** Our docs parser struggles to properly understand the constructor signature.
	 * This is the correct signature.
	 * 
	 * @param { TextOptions } options - The options of the bitmap text.
	 */
	constructor(options?: TextOptions);
	/** @deprecated since 8.0.0 */
	constructor(text?: TextString, options?: Partial<TextStyle>);
	/**
	 * The resolution / device pixel ratio for text rendering.
	 * Unlike other text types, BitmapText resolution is managed by the BitmapFont.
	 * Individual resolution changes are not supported.
	 * @example
	 * 
	 * @default 1
	 * @throws {Warning} When attempting to change resolution directly
	 */
	set resolution(value: number);
	get resolution(): number;
}
/**
 * Contains the output elements from a text split operation.
 * Provides access to the hierarchical structure of split text elements.
 * @example
 * 
 */
export interface TextSplitOutput<T extends SplitableTextObject> {
	/** Array of individual character Text objects */
	chars: T[];
	/** Array of word containers, each containing character objects */
	words: Container[];
	/** Array of line containers, each containing word containers */
	lines: Container[];
}
/**
 * Configuration options for text splitting.
 */
export interface AbstractSplitOptions {
	/** Text content to be split */
	text: string;
	/** Text styling - accepts TextStyle instance or style object */
	style: TextStyle | Partial<TextStyleOptions>;
	/**
	 * Enables automatic splitting on text/style changes
	 * @default true
	 */
	autoSplit?: boolean;
	/**
	 * Transform origin for line segments. Range: [0-1]
	 * @example
	 * 
	 * @default 0
	 */
	lineAnchor?: number | PointData;
	/**
	 * Transform origin for word segments. Range: [0-1]
	 * @example
	 * 
	 * @default 0
	 */
	wordAnchor?: number | PointData;
	/**
	 * Transform origin for character segments. Range: [0-1]
	 * @example
	 * 
	 * @default 0
	 */
	charAnchor?: number | PointData;
}
/**
 * Configuration options for SplitText, combining container properties with text splitting settings.
 * @example Basic Usage
 * 
 * @example Advanced Configuration
 * 
 *
 * Properties:
 * - Container options from {@link ContainerOptions}
 * - Text split options from {@link AbstractSplitOptions}
 */
export interface AbstractSplitTextOptions extends ContainerOptions, AbstractSplitOptions {
}
/**
 * @experimental
 * A container that splits text into individually manipulatable segments (lines, words, and characters)
 * for advanced text effects and animations.
 * @example Basic Usage
 * 
 *
 * Features:
 * - Hierarchical text splitting (lines → words → characters)
 * - Independent transformation origins for each segment level
 * - Automatic or manual segment updates
 * - Support for both canvas text and bitmap text
 * @example Animation Example
 * 
 *
 * Configuration Options:
 * - `text`: The string to render and segment
 * - `style`: TextStyle instance or configuration object
 * - `autoSplit`: Automatically update segments on changes (default: true)
 * - `lineAnchor`: Transform origin for lines (default: 0)
 * - `wordAnchor`: Transform origin for words (default: 0)
 * - `charAnchor`: Transform origin for characters (default: 0)
 *
 * > [!NOTE] Anchor points are normalized (0-1):
 * > - 0,0: Top-left
 * > - 0.5,0.5: Center
 * > - 1,1: Bottom-right
 *
 * > [!WARNING] Limitations
 * > - Character spacing may differ slightly from standard text due to browser
 * >   kerning being lost when characters are separated
 */
export declare abstract class AbstractSplitText<T extends SplitableTextObject> extends Container {
	/**
	 * Individual character segments of the text.
	 * @example
	 * 
	 */
	chars: T[];
	/**
	 * Word segments of the text, each containing one or more characters.
	 * @example
	 * 
	 */
	words: Container[];
	/**
	 * Line segments of the text, each containing one or more words.
	 * @example
	 * 
	 */
	lines: Container[];
	constructor(config: AbstractSplitTextOptions);
	/**
	 * Splits the text into lines, words, and characters.
	 * Call this manually when autoSplit is false.
	 * @example Manual Splitting
	 * 
	 */
	split(): void;
	get text(): string;
	/**
	 * Gets or sets the text content.
	 * Setting new text triggers splitting if autoSplit is true.
	 * > [!NOTE] Setting this frequently can have a performance impact, especially with large texts and canvas text.
	 * @example Dynamic Text Updates
	 * 
	 */
	set text(value: string);
	/**
	 * Gets or sets the transform anchor for line segments.
	 * The anchor point determines the center of rotation and scaling for each line.
	 * @example Setting Line Anchors
	 * 
	 */
	get lineAnchor(): number | PointData;
	set lineAnchor(value: number | PointData);
	/**
	 * Gets or sets the transform anchor for word segments.
	 * The anchor point determines the center of rotation and scaling for each word.
	 * @example
	 * 
	 */
	get wordAnchor(): number | PointData;
	set wordAnchor(value: number | PointData);
	/**
	 * Gets or sets the transform anchor for character segments.
	 * The anchor point determines the center of rotation and scaling for each character.
	 * @example Setting Character Anchors
	 * 
	 * @example Animation with Anchors
	 * 
	 */
	get charAnchor(): number | PointData;
	set charAnchor(value: number | PointData);
	get style(): TextStyle;
	/**
	 * The style configuration for the text.
	 * Can be a TextStyle instance or a configuration object.
	 * @example
	 * ts
	 * // Clean up everything
	 * text.destroy({ children: true, texture: true, style: true });
	 *
	 * // Remove from parent but keep style
	 * text.destroy({ children: true, style: false });
	 * ts
 * const options: SplitTextOptions = {
 *   text: 'Hello World',
 *   style: { fontSize: 32, fill: 0xffffff },
 *   // Transform origins
 *   lineAnchor: 0.5,                // Center each line
 *   wordAnchor: { x: 0, y: 0.5 },  // Left-center each word
 *   charAnchor: { x: 0.5, y: 1 },  // Bottom-center each char
 * };
 * ts
 * const options: SplitTextOptions = {
 *   // Text content and style
 *   text: 'Multi\nLine Text',
 *   style: new TextStyle({
 *     fontSize: 24,
 *     fill: 'white',
 *     strokeThickness: 2,
 *   }),
 *
 *   // Container properties
 *   x: 100,
 *   y: 100,
 *   alpha: 0.8,
 *
 *   // Splitting settings
 *   autoSplit: true,
 *
 *   // Transform origins (normalized 0-1)
 *   lineAnchor: { x: 1, y: 0 },    // Top-right
 *   wordAnchor: 0.5,               // Center
 *   charAnchor: { x: 0, y: 1 },    // Bottom-left
 * };
 * ts
 * const text = new SplitText({
 *   text: "Hello World",
 *   style: { fontSize: 24 },
 *   // Origin points for transformations (0-1 range)
 *   lineAnchor: 0.5,  // Center of each line
 *   wordAnchor: { x: 0, y: 0.5 },  // Left-center of each word
 *   charAnchor: { x: 0.5, y: 1 },  // Bottom-center of each character
 *   autoSplit: true  // Auto-update segments on text/style changes
 * });
 * ts
 * // Character fade-in sequence
 * text.chars.forEach((char, i) => {
 *   gsap.from(char, {
 *     alpha: 0,
 *     delay: i * 0.1
 *   });
 * });
 *
 * // Word scale animation
 * text.words.forEach((word, i) => {
 *   gsap.to(word.scale, {
 *     x: 1.2, y: 1.2,
 *     yoyo: true,
 *     repeat: -1,
 *     delay: i * 0.2
 *   });
 * });
 *
 * // Line slide-in effect
 * text.lines.forEach((line, i) => {
 *   gsap.from(line, {
 *     x: -200,
 *     delay: i * 0.3
 *   });
 * });
 * ts
	 * // Override defaults globally
	 * SplitText.defaultOptions = {
	 *   autoSplit: false,
	 *   lineAnchor: 0.5,  // Center alignment
	 *   wordAnchor: { x: 0, y: 0.5 },  // Left-center
	 *   charAnchor: { x: 0.5, y: 1 }   // Bottom-center
	 * };
	 * ts
	 * const text = new Text({
	 *   text: 'Bitmap Text',
	 *   style: { fontFamily: 'Arial' }
	 * });
	 *
	 * const segmented = SplitText.from(text);
	 *
	 * // with additional options
	 * const segmentedWithOptions = SplitText.from(text, {
	 *   autoSplit: false,
	 *   lineAnchor: 0.5,
	 *   wordAnchor: { x: 0, y: 0.5 },
	 * })
	 * ts
 * // Basic HTML text
 * const basicText = new HTMLText({
 *     text: '<b>Bold</b> and <i>Italic</i> text',
 *     style: {
 *         fontSize: 24,
 *         fill: 0xff1010
 *     }
 * });
 *
 * // Rich HTML text with styling
 * const richText = new HTMLText({
 *     text: '<custom>Custom Tag</custom>',
 *     style: {
 *         fontFamily: 'Arial',
 *         fontSize: 32,
 *         fill: 0x4a4a4a,
 *         align: 'center',
 *         tagStyles: {
 *             custom: {
 *                 fontSize: 32,
 *                 fill: '#00ff00',
 *                 fontStyle: 'italic'
 *             }
 *         }
 *     }
 *     textureStyle: {
 *         scaleMode: 'linear',
 *     }
 * });
 * ts
 * import { HTMLText } from 'pixi.js';
 *
 * // Basic HTML text with tags
 * const text = new HTMLText({
 *     text: '<h1>Title</h1><p>This is a <strong>bold</strong> and <em>italic</em> text.</p>',
 *     style: {
 *         fontFamily: 'Arial',
 *         fontSize: 24,
 *         fill: 0xff1010,
 *         align: 'center',
 *     }
 * });
 *
 * // Rich HTML text with custom styling
 * const richText = new HTMLText({
 *     text: `
 *         <div class="title">Welcome</div>
 *         <div class="content">
 *             This text supports:
 *             <ul>
 *                 <li>✨ Emojis</li>
 *                 <li>🎨 Custom CSS</li>
 *                 <li>📏 Auto-sizing</li>
 *             </ul>
 *         </div>
 *     `,
 *     style: {
 *         fontSize: 24,
 *         fill: '#334455',
 *         cssOverrides: [
 *             '.title { font-size: 32px; color: red; }',
 *             '.content { line-height: 1.5; }'
 *         ],
 *         wordWrap: true,
 *         wordWrapWidth: 300,
 *     }
 * });
 *
 * // Text with custom texture settings
 * const crispText = new HTMLText({
 *     text: '<div style="padding: 10px">High Quality Text</div>',
 *     style: {
 *         fontSize: 24,
 *         fill: '#4a4a4a',
 *     },
 *     textureStyle: {
 *         scaleMode: 'nearest',
 *     }
 * });
 * ts
	 * const text = new HTMLText({
	 *     text: 'Hello Pixi!',
	 * });
	 * const multilineText = new HTMLText({
	 *     text: 'Line 1\nLine 2\nLine 3',
	 * });
	 * const numberText = new HTMLText({
	 *     text: 12345, // Will be converted to '12345'
	 * });
	 * const objectText = new HTMLText({
	 *     text: { toString: () => 'Object Text' }, // Custom toString
	 * });
	 *
	 * // Update text dynamically
	 * text.text = 'Updated Text'; // Re-renders with new text
	 * text.text = 67890; // Updates to '67890'
	 * text.text = { toString: () => 'Dynamic Text' }; // Uses custom toString method
	 * // Clear text
	 * text.text = ''; // Clears the text
	 * ts
 * const options: SplitBitmapTextOptions = {
 *   text: 'Hello World',
 *   style: { fontSize: 32, fill: 0xffffff },
 *   // Transform origins
 *   lineAnchor: 0.5,                // Center each line
 *   wordAnchor: { x: 0, y: 0.5 },  // Left-center each word
 *   charAnchor: { x: 0.5, y: 1 },  // Bottom-center each char
 * };
 * ts
 * const options: SplitBitmapTextOptions = {
 *   // Text content and style
 *   text: 'Multi\nLine Text',
 *   style: new TextStyle({
 *     fontSize: 24,
 *     fill: 'white',
 *     strokeThickness: 2,
 *   }),
 *
 *   // Container properties
 *   x: 100,
 *   y: 100,
 *   alpha: 0.8,
 *
 *   // Splitting settings
 *   autoSplit: true,
 *
 *   // Transform origins (normalized 0-1)
 *   lineAnchor: { x: 1, y: 0 },    // Top-right
 *   wordAnchor: 0.5,               // Center
 *   charAnchor: { x: 0, y: 1 },    // Bottom-left
 * };
 * ts
 * const text = new SplitBitmapText({
 *   text: "Hello World",
 *   style: { fontSize: 24 },
 *   // Origin points for transformations (0-1 range)
 *   lineAnchor: 0.5,  // Center of each line
 *   wordAnchor: { x: 0, y: 0.5 },  // Left-center of each word
 *   charAnchor: { x: 0.5, y: 1 },  // Bottom-center of each character
 *   autoSplit: true  // Auto-update segments on text/style changes
 * });
 * ts
 * // Character fade-in sequence
 * text.chars.forEach((char, i) => {
 *   gsap.from(char, {
 *     alpha: 0,
 *     delay: i * 0.1
 *   });
 * });
 *
 * // Word scale animation
 * text.words.forEach((word, i) => {
 *   gsap.to(word.scale, {
 *     x: 1.2, y: 1.2,
 *     yoyo: true,
 *     repeat: -1,
 *     delay: i * 0.2
 *   });
 * });
 *
 * // Line slide-in effect
 * text.lines.forEach((line, i) => {
 *   gsap.from(line, {
 *     x: -200,
 *     delay: i * 0.3
 *   });
 * });
 * ts
	 * // Override defaults globally
	 * SplitBitmapText.defaultOptions = {
	 *   autoSplit: false,
	 *   lineAnchor: 0.5,  // Center alignment
	 *   wordAnchor: { x: 0, y: 0.5 },  // Left-center
	 *   charAnchor: { x: 0.5, y: 1 }   // Bottom-center
	 * };
	 * ts
	 * const bitmapText = new BitmapText({
	 *   text: 'Bitmap Text',
	 *   style: { fontFamily: 'Arial' }
	 * });
	 *
	 * const segmented = SplitBitmapText.from(bitmapText);
	 *
	 * // with additional options
	 * const segmentedWithOptions = SplitBitmapText.from(bitmapText, {
	 *   autoSplit: false,
	 *   lineAnchor: 0.5,
	 *   wordAnchor: { x: 0, y: 0.5 },
	 * })
	 * typescript
	 * const bitmap = await WorkerManager.loadImageBitmap('image.png');
	 * const bitmapWithOptions = await WorkerManager.loadImageBitmap('image.png', asset);
	 * typescript
	 * // Clean up when shutting down
	 * WorkerManager.reset();
	 * ts
 * import { Culler, Container, Rectangle } from 'pixi.js';
 *
 * // Create a culler and container
 * const culler = new Culler();
 * const stage = new Container();
 *
 * // Set up container with culling
 * stage.cullable = true;
 * stage.cullArea = new Rectangle(0, 0, 800, 600);
 *
 * // Add some sprites that will be culled
 * for (let i = 0; i < 1000; i++) {
 *     const sprite = Sprite.from('texture.png');
 *     sprite.x = Math.random() * 2000;
 *     sprite.y = Math.random() * 2000;
 *     sprite.cullable = true;
 *     stage.addChild(sprite);
 * }
 *
 * // Cull objects outside view
 * culler.cull(stage, {
 *     x: 0,
 *     y: 0,
 *     width: 800,
 *     height: 600
 * });
 *
 * // Only visible objects will be rendered
 * renderer.render(stage);
 * ts
	 * // Basic culling with view bounds
	 * const culler = new Culler();
	 * culler.cull(stage, {
	 *     x: 0,
	 *     y: 0,
	 *     width: 800,
	 *     height: 600
	 * });
	 *
	 * // Culling to renderer screen
	 * culler.cull(stage, renderer.screen, false);
	 * ts
	 * // Use the shared instance instead of creating a new one
	 * Culler.shared.cull(stage, {
	 *     x: 0,
	 *     y: 0,
	 *     width: 800,
	 *     height: 600
	 * });
	 * ts
	 * AlphaFilter.defaultOptions = {
	 *     alpha: 0.5, // Default alpha value
	 * };
	 * // Use default options
	 * const filter = new AlphaFilter(); // Uses default alpha of 0.5
	 * ts
	 * // Create filter with initial alpha
	 * const filter = new AlphaFilter({ alpha: 0.5 });
	 *
	 * // Update alpha value dynamically
	 * filter.alpha = 0.8;
	 * ts
 * // Basic blur with default values
 * const filter = new BlurFilter();
 *
 * // Custom blur configuration
 * const filter = new BlurFilter({
 *     strength: 8,        // Overall blur strength
 *     quality: 4,         // Higher quality = better blur
 *     kernelSize: 5      // Size of blur kernel
 * });
 *
 * // Different horizontal/vertical blur
 * const filter = new BlurFilter({
 *     strengthX: 4,      // Horizontal blur only
 *     strengthY: 12,     // Stronger vertical blur
 *     quality: 2         // Lower quality for better performance
 * });
 * ts
 * import { BlurFilter } from 'pixi.js';
 *
 * // Create with default settings
 * const filter = new BlurFilter();
 *
 * // Create with custom settings
 * const filter = new BlurFilter({
 *     strength: 8,      // Overall blur strength
 *     quality: 4,       // Blur quality (higher = better but slower)
 *     kernelSize: 5     // Size of blur kernel matrix
 * });
 *
 * // Apply to a display object
 * sprite.filters = [filter];
 *
 * // Update properties
 * filter.strength = 10;          // Set both X and Y blur
 * filter.strengthX = 5;          // Set only horizontal blur
 * filter.strengthY = 15;         // Set only vertical blur
 * filter.quality = 2;            // Adjust quality
 *
 * // Enable edge pixel clamping
 * filter.repeatEdgePixels = true;
 * ts
	 * // Set default options for all BlurFilters
	 * BlurFilter.defaultOptions = {
	 *     strength: 10,       // Default blur strength
	 *     quality: 2,        // Default blur quality
	 *     kernelSize: 7      // Default kernel size
	 * };
	 * // Create a filter with these defaults
	 * const filter = new BlurFilter(); // Uses default options
	 * ts
	 * // Set equal blur strength for both axes
	 * filter.strength = 8;
	 *
	 * // Will throw error if X and Y are different
	 * filter.strengthX = 4;
	 * filter.strengthY = 8;
	 * filter.strength; // Error: BlurFilter's strengthX and strengthY are different
	 * ts
	 * // High quality blur (slower)
	 * filter.quality = 8;
	 *
	 * // Low quality blur (faster)
	 * filter.quality = 2;
	 * ts
	 * // Apply horizontal-only blur
	 * filter.strengthX = 8;
	 * filter.strengthY = 0;
	 *
	 * // Create motion blur effect
	 * filter.strengthX = 16;
	 * filter.strengthY = 2;
	 * ts
	 * // Apply vertical-only blur
	 * filter.strengthX = 0;
	 * filter.strengthY = 8;
	 *
	 * // Create radial blur effect
	 * filter.strengthX = 8;
	 * filter.strengthY = 8;
	 * js
 * import { ColorMatrixFilter } from 'pixi.js';
 *
 * // Create a new color matrix filter
 * const colorMatrix = new ColorMatrixFilter();
 *
 * // Apply it to a container
 * container.filters = [colorMatrix];
 *
 * // Adjust contrast
 * colorMatrix.contrast(2);
 *
 * // Chain multiple effects
 * colorMatrix
 *     .saturate(0.5)     // 50% saturation
 *     .brightness(1.2)    // 20% brighter
 *     .hue(90);          // 90 degree hue rotation
 * ts
	 * // Create a new color matrix filter
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Darken the image to 50% brightness
	 * colorMatrix.brightness(0.5, false);
	 *
	 * // Chain with other effects by using multiply
	 * colorMatrix
	 *     .brightness(1.2, true)  // Brighten by 20%
	 *     .saturate(1.1, true);   // Increase saturation by 10%
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply a red tint
	 * colorMatrix.tint(0xff0000);
	 *
	 * // Layer a green tint on top of existing effects
	 * colorMatrix.tint('green', true);
	 *
	 * // Chain with other color adjustments
	 * colorMatrix
	 *     .tint('blue')       // Blue tint
	 *     .brightness(1.2, true) // Increase brightness
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Convert to 50% grey
	 * colorMatrix.greyscale(0.5, false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .greyscale(0.6, true)    // Add grey tint
	 *     .brightness(1.2, true);   // Brighten the result
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Convert to 50% grey
	 * colorMatrix.grayscale(0.5, false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .grayscale(0.6, true)    // Add grey tint
	 *     .brightness(1.2, true);   // Brighten the result
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Convert to black and white
	 * colorMatrix.blackAndWhite(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .blackAndWhite(true)     // Apply B&W effect
	 *     .brightness(1.2, true);   // Then increase brightness
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Rotate hue by 90 degrees
	 * colorMatrix.hue(90, false);
	 *
	 * // Chain multiple color adjustments
	 * colorMatrix
	 *     .hue(45, true)          // Rotate colors by 45°
	 *     .saturate(1.2, true)    // Increase saturation
	 *     .brightness(1.1, true); // Slightly brighten
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Increase contrast by 50%
	 * colorMatrix.contrast(0.75, false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .contrast(0.6, true)     // Boost contrast
	 *     .brightness(1.1, true)   // Slightly brighten
	 *     .saturate(1.2, true);    // Increase color intensity
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Double the saturation
	 * colorMatrix.saturate(1, false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .saturate(0.5, true)     // Increase saturation by 50%
	 *     .brightness(1.1, true)    // Slightly brighten
	 *     .contrast(0.8, true);     // Reduce contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Convert image to grayscale
	 * colorMatrix.desaturate();
	 *
	 * // Can be chained with other effects
	 * colorMatrix
	 *     .desaturate()         // Remove all color
	 *     .brightness(1.2);     // Then increase brightness
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Create negative effect
	 * colorMatrix.negative(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .negative(true)       // Apply negative effect
	 *     .brightness(1.2, true) // Increase brightness
	 *     .contrast(0.8, true);  // Reduce contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply sepia effect
	 * colorMatrix.sepia(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .sepia(true)           // Add sepia tone
	 *     .brightness(1.1, true)  // Slightly brighten
	 *     .contrast(0.9, true);   // Reduce contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply Technicolor effect
	 * colorMatrix.technicolor(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .technicolor(true)      // Add Technicolor effect
	 *     .contrast(1.1, true)    // Boost contrast
	 *     .brightness(0.9, true); // Slightly darken
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply Polaroid effect
	 * colorMatrix.polaroid(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .polaroid(true)         // Add Polaroid effect
	 *     .brightness(1.1, true)  // Slightly brighten
	 *     .contrast(1.1, true);   // Boost contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Swap red and blue channels
	 * colorMatrix.toBGR(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .toBGR(true)           // Swap R and B channels
	 *     .brightness(1.1, true)  // Slightly brighten
	 *     .contrast(0.9, true);   // Reduce contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply Kodachrome effect
	 * colorMatrix.kodachrome(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .kodachrome(true)       // Add Kodachrome effect
	 *     .contrast(1.1, true)    // Boost contrast
	 *     .brightness(0.9, true); // Slightly darken
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply browni effect
	 * colorMatrix.browni(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .browni(true)          // Add brown tint
	 *     .brightness(1.1, true)  // Slightly brighten
	 *     .contrast(1.2, true);   // Boost contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply vintage effect
	 * colorMatrix.vintage(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .vintage(true)          // Add vintage look
	 *     .brightness(0.9, true)  // Slightly darken
	 *     .contrast(1.1, true);   // Boost contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Create sepia-like effect with custom colors
	 * colorMatrix.colorTone(
	 *     0.3,        // Moderate desaturation
	 *     0.2,        // Moderate toning
	 *     0xFFE580,   // Warm highlight color
	 *     0x338000,   // Dark green shadows
	 *     false
	 * );
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .colorTone(0.2, 0.15, 0xFFE580, 0x338000, true)
	 *     .brightness(1.1, true);  // Slightly brighten
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply night vision effect
	 * colorMatrix.night(0.3, false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .night(0.2, true)        // Add night vision
	 *     .brightness(1.1, true)    // Slightly brighten
	 *     .contrast(1.2, true);     // Boost contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply thermal vision effect
	 * colorMatrix.predator(0.5, false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .predator(0.3, true)      // Add thermal effect
	 *     .contrast(1.2, true)      // Boost contrast
	 *     .brightness(1.1, true);   // Slightly brighten
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply psychedelic effect
	 * colorMatrix.lsd(false);
	 *
	 * // Chain with other effects
	 * colorMatrix
	 *     .lsd(true)             // Add color distortion
	 *     .brightness(0.9, true)  // Slightly darken
	 *     .contrast(1.2, true);   // Boost contrast
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 *
	 * // Apply some effects
	 * colorMatrix
	 *     .sepia(true)
	 *     .brightness(1.2, true);
	 *
	 * // Reset back to original colors
	 * colorMatrix.reset();
	 * ts
	 * const colorMatrix = new ColorMatrixFilter();
	 * // Get the current color matrix
	 * const currentMatrix = colorMatrix.matrix;
	 * // Modify the matrix
	 * colorMatrix.matrix = [
	 *     1, 0, 0, 0, 0,
	 *     0, 1, 0, 0, 0,
	 *     0, 0, 1, 0, 0,
	 *     0, 0, 0, 1, 0
	 * ];
	 */
	get matrix(): ColorMatrix;
	set matrix(value: ColorMatrix);
	/**
	 * The opacity value used to blend between the original and transformed colors.
	 *
	 * This value controls how much of the color transformation is applied:
	 * - 0 = Original color only (no effect)
	 * - 0.5 = 50% blend of original and transformed colors
	 * - 1 = Fully transformed color (default)
	 * @default 1
	 * @example
	 * 
	 */
	get alpha(): number;
	set alpha(value: number);
}
/**
 * Configuration options for the DisplacementFilter.
 *
 * A displacement filter uses a sprite's texture as a displacement map,
 * moving pixels of the target based on the color values of corresponding
 * pixels in the displacement sprite.
 * @example
 * 
 */
export interface DisplacementFilterOptions extends FilterOptions {
	/**
	 * The sprite whose texture will be used as the displacement map.
	 * Red channel = horizontal displacement
	 * Green channel = vertical displacement
	 * @example
	 * 
	 */
	sprite: Sprite;
	/**
	 * The scale of the displacement effect. Can be a single number for uniform
	 * scaling or a point-like object for separate x/y scaling.
	 * @default 20
	 * @example
	 * 
	 */
	scale?: number | PointData;
}
/**
 * A filter that applies a displacement map effect using a sprite's texture.
 *
 * The DisplacementFilter uses another texture (from a sprite) as a displacement map,
 * where the red and green channels of each pixel in the map determine how the corresponding
 * pixel in the filtered object should be offset:
 * - Red channel controls horizontal displacement
 * - Green channel controls vertical displacement
 *
 * Common use cases:
 * - Creating ripple or wave effects
 * - Distorting images dynamically
 * - Implementing heat haze effects
 * - Creating transition effects
 * @example
 * 
 */
export declare class DisplacementFilter extends Filter {
	/**
	 * @param {Sprite | DisplacementFilterOptions} options - The sprite or options object.
	 * @param {Sprite} options.sprite - The texture used for the displacement map.
	 * @param {number | PointData} options.scale - The scale of the displacement.
	 */
	constructor(options: Sprite | DisplacementFilterOptions);
	/** @deprecated since 8.0.0 */
	constructor(sprite: Sprite, scale?: number | PointData);
	/**
	 * The scale of the displacement effect.
	 *
	 * Gets the current x and y scaling values used for the displacement mapping.
	 * - x: Horizontal displacement scale
	 * - y: Vertical displacement scale
	 * @returns {Point} The current scale as a Point object
	 * @example
	 * 
	 */
	get scale(): Point;
}
/**
 * Configuration options for the NoiseFilter.
 *
 * The NoiseFilter adds random noise to the rendered content. The noise effect can be
 * controlled through the noise intensity and an optional seed value for reproducible results.
 * @example
 * 
 */
export interface NoiseFilterOptions extends FilterOptions {
	/**
	 * The amount of noise to apply. Should be in range (0, 1]:
	 * - 0.1 = subtle noise
	 * - 0.5 = moderate noise (default)
	 * - 1.0 = maximum noise
	 * @default 0.5
	 * @example
	 * 
	 */
	noise?: number;
	/**
	 * A seed value to apply to the random noise generation.
	 * Using the same seed will generate the same noise pattern.
	 * @default Math.random()
	 * @example
	 * 
	 */
	seed?: number;
}
/**
 * A filter that adds configurable random noise to rendered content.
 *
 * This filter generates pixel noise based on a noise intensity value and an optional seed.
 * It can be used to create various effects like film grain, static, or texture variation.
 *
 * Based on: https://github.com/evanw/glfx.js/blob/master/src/filters/adjust/noise.js
 * @example
 * 
 */
export declare class NoiseFilter extends Filter {
	/**
	 * The default configuration options for the NoiseFilter.
	 *
	 * These values will be used when no specific options are provided to the constructor.
	 * You can override any of these values by passing your own options object.
	 * @example
	 * 
	 */
	static defaultOptions: NoiseFilterOptions;
	/**
	 * @param options - The options of the noise filter.
	 */
	constructor(options?: NoiseFilterOptions);
	/**
	 * The amount of noise to apply to the filtered content.
	 *
	 * This value controls the intensity of the random noise effect:
	 * - Values close to 0 produce subtle noise
	 * - Values around 0.5 produce moderate noise
	 * - Values close to 1 produce strong noise
	 * @default 0.5
	 * @example
	 * 
	 */
	get noise(): number;
	set noise(value: number);
	/**
	 * The seed value used for random noise generation.
	 *
	 * This value determines the noise pattern:
	 * - Using the same seed will generate identical noise patterns
	 * - Different seeds produce different but consistent patterns
	 * - `Math.random()` can be used for random patterns
	 * @default Math.random()
	 * @example
	 * 
	 */
	get seed(): number;
	set seed(value: number);
}
type GD8Symmetry = number;
/**
 * Utility class for maintaining reference to a collection
 * of Textures on a single Spritesheet.
 *
 * To access a sprite sheet from your code you may pass its JSON data file to Pixi's loader:
 *
 * 
 *
 * Alternately, you may circumvent the loader by instantiating the Spritesheet directly:
 *
 * 
 *
 * With the `sheet.textures` you can create Sprite objects, and `sheet.animations` can be used to create an AnimatedSprite.
 *
 * Here's an example of a sprite sheet JSON data file:
 * 
 * Sprite sheets can be packed using tools like {@link https://codeandweb.com/texturepacker|TexturePacker},
 * {@link https://renderhjs.net/shoebox/|Shoebox} or {@link https://github.com/krzysztof-o/spritesheet.js|Spritesheet.js}.
 * Default anchor points (see {@link Texture#defaultAnchor}), default 9-slice borders
 * (see {@link Texture#defaultBorders}) and grouping of animation sprites are currently only
 * supported by TexturePacker.
 *
 * Alternative ways for loading spritesheet image if you need more control:
 *
 * 
 *
 * or:
 *
 * 
 */
export declare class Spritesheet<S extends SpritesheetData = SpritesheetData> {
	/** For multi-packed spritesheets, this contains a reference to all the other spritesheets it depends on. */
	linkedSheets: Spritesheet<S>[];
	/** Reference to the source texture. */
	textureSource: TextureSource;
	/**
	 * A map containing all textures of the sprite sheet.
	 * Can be used to create a {@link Sprite}:
	 * @example
	 * import { Sprite } from 'pixi.js';
	 *
	 * new Sprite(sheet.textures['image.png']);
	 */
	textures: Record<keyof S["frames"], Texture>;
	/**
	 * A map containing the textures for each animation.
	 * Can be used to create an {@link AnimatedSprite}:
	 * @example
	 * import { AnimatedSprite } from 'pixi.js';
	 *
	 * new AnimatedSprite(sheet.animations['anim_name']);
	 */
	animations: Record<keyof NonNullable<S["animations"]>, Texture[]>;
	/**
	 * Reference to the original JSON data.
	 * @type {object}
	 */
	data: S;
	/** The resolution of the spritesheet. */
	resolution: number;
	/** Prefix string to add to global cache */
	readonly cachePrefix: string;
	/**
	 * @param options - Options to use when constructing a new Spritesheet.
	 */
	constructor(options: SpritesheetOptions<S>);
	/**
	 * @param texture - Reference to the source BaseTexture object.
	 * @param {object} data - Spritesheet image data.
	 */
	constructor(texture: BindableTexture, data: S);
	/**
	 * Parser spritesheet from loaded data. This is done asynchronously
	 * to prevent creating too many Texture within a single process.
	 */
	parse(): Promise<Record<string, Texture>>;
	/**
	 * Destroy Spritesheet and don't use after this.
	 * @param {boolean} [destroyBase=false] - Whether to destroy the base texture as well
	 */
	destroy(destroyBase?: boolean): void;
}
/**
 * Represents the update priorities used by internal Pixi classes when registered with
 * the {@link Ticker} object. Higher priority items are updated first and lower
 * priority items, such as render, should go later.
 * @enum {number}
 */
export declare enum UPDATE_PRIORITY {
	/**
	 * Highest priority used for interaction events in {@link EventSystem}
	 * @default 50
	 */
	INTERACTION = 50,
	/**
	 * High priority updating, used by {@link AnimatedSprite}
	 * @default 25
	 */
	HIGH = 25,
	/**
	 * Default priority for ticker events, see {@link Ticker#add}.
	 * @default 0
	 */
	NORMAL = 0,
	/**
	 * Low priority used for {@link Application} rendering.
	 * @default -25
	 */
	LOW = -25,
	/**
	 * Lowest priority used for {@link PrepareBase} utility.
	 * @default -50
	 */
	UTILITY = -50
}
/**
 * Helper for checking for WebGL support in the current environment.
 *
 * Results are cached after first call for better performance.
 * @example
 * 
 * @param failIfMajorPerformanceCaveat - Whether to fail if there is a major performance caveat
 * @returns True if WebGL is supported
 */
export declare function isWebGLSupported(failIfMajorPerformanceCaveat?: boolean): boolean;
/**
 * Helper for checking for WebGPU support in the current environment.
 * Results are cached after first call for better performance.
 * @example
 * 
 * @param options - The options for requesting a GPU adapter
 * @returns Promise that resolves to true if WebGPU is supported
 */
export declare function isWebGPUSupported(options?: GPURequestAdapterOptions): Promise<boolean>;
interface DeprecationOptions {
	/**
	 * When set to true, all deprecation warning messages will be hidden.
	 * Use this if you want to silence deprecation notifications.
	 * @default false
	 */
	quiet: boolean;
	/**
	 * When set to true, deprecation messages will be displayed as plain text without color formatting.
	 * Use this if you want to disable colored console output for deprecation warnings.
	 * @default false
	 */
	noColor: boolean;
}
/**
 * Path utilities for working with URLs and file paths in a cross-platform way.
 * All paths that are passed in will become normalized to have posix separators.
 * @example
 * 
 * @remarks
 * - Normalizes to POSIX separators (forward slashes)
 * - Handles URLs, data URLs, and file paths
 * - Supports path composition and decomposition
 * - Common in asset loading and URL management
 */
export declare const path: Path;
interface Cleanable {
	clear(): void;
}

export {
	Buffer$1 as Buffer,
	Cache$1 as Cache,
	EXT_texture_compression_bptc$1 as EXT_texture_compression_bptc,
	EXT_texture_compression_rgtc$1 as EXT_texture_compression_rgtc,
	ExtensionFormat as ExtensionFormatLoose,
	GPU$1 as GPU,
	PredefinedColorSpace$1 as PredefinedColorSpace,
	RenderingContext$1 as RenderingContext,
	StrictExtensionFormat as ExtensionFormat,
	Text$1 as Text,
	WEBGL_compressed_texture_etc$1 as WEBGL_compressed_texture_etc,
	WEBGL_compressed_texture_etc1$1 as WEBGL_compressed_texture_etc1,
	WEBGL_compressed_texture_pvrtc$1 as WEBGL_compressed_texture_pvrtc,
	earcut$1 as earcut,
};

export as namespace PIXI;

**Examples:**

Example 1 (typescript):
```typescript
// Generated by dts-bundle-generator v9.5.1

/**
 * Minimal `EventEmitter` interface that is molded against the Node.js
 * `EventEmitter` interface.
 */
export declare class EventEmitter<EventTypes extends EventEmitter.ValidEventTypes = string | symbol, Context extends any = any> {
	static prefixed: string | boolean;
	/**
	 * Return an array listing the events for which the emitter has registered
	 * listeners.
	 */
	eventNames(): Array<EventEmitter.EventNames<EventTypes>>;
	/**
	 * Return the listeners registered for a given event.
	 */
	listeners<T extends EventEmitter.EventNames<EventTypes>>(event: T): Array<EventEmitter.EventListener<EventTypes, T>>;
	/**
	 * Return the number of listeners listening to a given event.
	 */
	listenerCount(event: EventEmitter.EventNames<EventTypes>): number;
	/**
	 * Calls each of the listeners registered for a given event.
	 */
	emit<T extends EventEmitter.EventNames<EventTypes>>(event: T, ...args: EventEmitter.EventArgs<EventTypes, T>): boolean;
	/**
	 * Add a listener for a given event.
	 */
	on<T extends EventEmitter.EventNames<EventTypes>>(event: T, fn: EventEmitter.EventListener<EventTypes, T>, context?: Context): this;
	addListener<T extends EventEmitter.EventNames<EventTypes>>(event: T, fn: EventEmitter.EventListener<EventTypes, T>, context?: Context): this;
	/**
	 * Add a one-time listener for a given event.
	 */
	once<T extends EventEmitter.EventNames<EventTypes>>(event: T, fn: EventEmitter.EventListener<EventTypes, T>, context?: Context): this;
	/**
	 * Remove the listeners of a given event.
	 */
	removeListener<T extends EventEmitter.EventNames<EventTypes>>(event: T, fn?: EventEmitter.EventListener<EventTypes, T>, context?: Context, once?: boolean): this;
	off<T extends EventEmitter.EventNames<EventTypes>>(event: T, fn?: EventEmitter.EventListener<EventTypes, T>, context?: Context, once?: boolean): this;
	/**
	 * Remove all listeners, or those of the specified event.
	 */
	removeAllListeners(event?: EventEmitter.EventNames<EventTypes>): this;
}
export declare namespace EventEmitter {
	export interface ListenerFn<Args extends any[] = any[]> {
		(...args: Args): void;
	}
	export interface EventEmitterStatic {
		new <EventTypes extends ValidEventTypes = string | symbol, Context = any>(): EventEmitter<EventTypes, Context>;
	}
	/**
	 * `object` should be in either of the following forms:
	 *
```

Example 2 (unknown):
```unknown
*/
	export type ValidEventTypes = string | symbol | object;
	export type EventNames<T extends ValidEventTypes> = T extends string | symbol ? T : keyof T;
	export type ArgumentMap<T extends object> = {
		[K in keyof T]: T[K] extends (...args: any[]) => void ? Parameters<T[K]> : T[K] extends any[] ? T[K] : any[];
	};
	export type EventListener<T extends ValidEventTypes, K extends EventNames<T>> = T extends string | symbol ? (...args: any[]) => void : (...args: ArgumentMap<Exclude<T, string | symbol>>[Extract<K, keyof T>]) => void;
	export type EventArgs<T extends ValidEventTypes, K extends EventNames<T>> = Parameters<EventListener<T, K>>;
	export const EventEmitter: EventEmitterStatic;
}
declare type RgbColor = {
	r: number;
	g: number;
	b: number;
};
declare type HslColor = {
	h: number;
	s: number;
	l: number;
};
declare type HsvColor = {
	h: number;
	s: number;
	v: number;
};
declare type WithAlpha<O> = O & {
	a: number;
};
declare type RgbaColor = WithAlpha<RgbColor>;
declare type HslaColor = WithAlpha<HslColor>;
declare type HsvaColor = WithAlpha<HsvColor>;
/**
 * Array of RGBA color components, where each component is a number between 0 and 1.
 * The array must contain exactly 4 numbers in the order: red, green, blue, alpha.
 * @example
 *
```

Example 3 (unknown):
```unknown
* @remarks
 * - All components must be between 0 and 1
 * - Array must contain exactly 4 values
 * - Order is [red, green, blue, alpha]
 */
export type RgbaArray = [
	number,
	number,
	number,
	number
];
/**
 * Valid color formats supported by PixiJS. These types extend from [colord](https://www.npmjs.com/package/colord)
 * with additional PixiJS-specific formats.
 *
 * Common Formats:
 *
```

Example 4 (unknown):
```unknown
* @remarks
 * - All color values are normalized internally to 0-1 range
 * - Alpha is always between 0-1
 * - Invalid colors will throw an error
 * - Original format is preserved when possible
 * @since 7.2.0
 */
export type ColorSource = string | number | number[] | Float32Array | Uint8Array | Uint8ClampedArray | HslColor | HslaColor | HsvColor | HsvaColor | RgbColor | RgbaColor | Color | number;
/**
 * Color utility class for managing colors in various formats. Provides a unified way to work
 * with colors across your PixiJS application.
 *
 * Features:
 * - Accepts multiple color formats (hex, RGB, HSL, etc.)
 * - Automatic format conversion
 * - Color manipulation methods
 * - Component access (r,g,b,a)
 * - Chainable operations
 * @example
 *
```

---

## Architecture

**URL:** llms-txt#architecture

**Contents:**
  - Major Components
- Extensions
- Extension Types
  - Assets
  - Renderer (WebGL, WebGPU, Canvas)
  - Application
  - Environment
  - Other (Primarily Internal Use)
- Creating Extensions
- Environments

Here's a list of the major components that make up PixiJS. Note that this list isn't exhaustive. Additionally, don't worry too much about how each component works. The goal here is to give you a feel for what's under the hood as we start exploring the engine.

| Component         | Description                                                                                                                                                                                                       |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Renderer**      | The core of the PixiJS system is the renderer, which displays the scene graph and draws it to the screen. PixiJS will automatically determine whether to provide you the WebGPU or WebGL renderer under the hood. |
| **Container**     | Main scene object which creates a scene graph: the tree of renderable objects to be displayed, such as sprites, graphics and text. See [Scene Graph](scene-graph) for more details.                               |
| **Assets**        | The Asset system provides tools for asynchronously loading resources such as images and audio files.                                                                                                              |
| **Ticker**        | Tickers provide periodic callbacks based on a clock. Your game update logic will generally be run in response to a tick once per frame. You can have multiple tickers in use at one time.                         |
| **Application**   | The Application is a simple helper that wraps a Loader, Ticker and Renderer into a single, convenient easy-to-use object. Great for getting started quickly, prototyping and building simple projects.            |
| **Events**        | PixiJS supports pointer-based interaction - making objects clickable, firing hover events, etc.                                                                                                                   |
| **Accessibility** | Woven through our display system is a rich set of tools for enabling keyboard and screen-reader accessibility.                                                                                                    |
| **Filters**       | PixiJS supports a variety of filters, including custom shaders, to apply effects to your renderable objects.                                                                                                      |

PixiJS v8 is built entirely around the concept of extensions. Every system in PixiJS is implemented as a modular extension. This allows PixiJS to remain lightweight, flexible, and easy to extend.

:::info
In most cases, you won’t need to interact with the extension system directly unless you are developing a third-party library or contributing to the PixiJS ecosystem itself.
:::

PixiJS supports a wide range of extension types, each serving a unique role in the architecture:

- `ExtensionType.Asset`: Groups together loaders, resolvers, cache and detection extensions into one convenient object instead of having to register each one separately.
- `ExtensionType.LoadParser`: Loads resources like images, JSON, videos.
- `ExtensionType.ResolveParser`: Converts asset URLs into a format that can be used by the loader.
- `ExtensionType.CacheParser`: Determines caching behavior for a particular asset.
- `ExtensionType.DetectionParser`: Identifies asset format support on the current platform.

### Renderer (WebGL, WebGPU, Canvas)

- `ExtensionType.WebGLSystem`, `ExtensionType.WebGPUSystem`, `ExtensionType.CanvasSystem`: Add systems to their respective renderers. These systems can vary widely in functionality, from managing textures to accessibility features.
- `ExtensionType.WebGLPipes`, `ExtensionType.WebGPUPipes`, `ExtensionType.CanvasPipes`: Add a new rendering pipe. RenderPipes are specifically used to render Renderables like a Mesh
- `ExtensionType.WebGLPipesAdaptor`, `ExtensionType.WebGPUPipesAdaptor`, `ExtensionType.CanvasPipesAdaptor`: Adapt rendering pipes for the respective renderers.

- `ExtensionType.Application`: Used for plugins that extend the `Application` lifecycle.
  For example the `TickerPlugin` and `ResizePlugin` are both application extensions.

- `ExtensionType.Environment`: Used to detect and configure platform-specific behavior. This can be useful for configuring PixiJS to work in environments like Node.js, Web Workers, or the browser.

### Other (Primarily Internal Use)

These extension types are mainly used internally and are typically not required in most user-facing applications:

- `ExtensionType.MaskEffect`: Used by MaskEffectManager for custom masking behaviors.
- `ExtensionType.BlendMode`: A type of extension for creating a new advanced blend mode.
- `ExtensionType.TextureSource`: A type of extension that will be used to auto detect a resource type E.g `VideoSource`
- `ExtensionType.ShapeBuilder`: A type of extension for building and triangulating custom shapes used in graphics.
- `ExtensionType.Batcher`: A type of extension for creating custom batchers used in rendering.

## Creating Extensions

The `extensions` object in PixiJS is a global registry for managing extensions. Extensions must declare an `extension` field with metadata, and are registered via `extensions.add(...)`.

**Examples:**

Example 1 (ts):
```ts
import { extensions, ExtensionType } from 'pixi.js';

const myLoader = {
  extension: {
    type: ExtensionType.LoadParser,
    name: 'my-loader',
  },
  test(url) {
    /* logic */
  },
  load(url) {
    /* logic */
  },
};

extensions.add(myLoader);
```

---

## Color

**URL:** llms-txt#color

**Contents:**
- Using `Color` and `ColorSource`
- API Reference
- Events / Interaction

The `Color` class in PixiJS is a flexible utility for representing colors. It is used throughout the rendering pipeline for things like tints, fills, strokes, gradients, and more.

## Using `Color` and `ColorSource`

PixiJS supports many color formats through the `ColorSource` type:

- Color names: `'red'`, `'white'`, `'blue'`, etc.
- Hex integers: `0xffcc00`
- Hex strings: `'ffcc00'`, `'#f00'`, `'0xffcc00ff'`
- RGB(A) objects: `{ r: 255, g: 0, b: 0 }`, `{ r: 255, g: 0, b: 0, a: 0.5 }`
- RGB(A) strings: `'rgb(255,0,0)'`, `'rgba(255,0,0,0.5)'`
- RGB(A) arrays: `[1, 0, 0]`, `[1, 0, 0, 0.5]`
- Typed arrays: `Uint8Array`, `Float32Array`
- HSL/HSV objects and strings
- `Color` instances

Whenever you see a color-related property (e.g., `fill`, `tint`, `stroke`), you can use any of these formats. The library will automatically convert them to the appropriate format internally.

- [Color](https://pixijs.download/release/docs/color.Color.html)

## Events / Interaction

**Examples:**

Example 1 (ts):
```ts
import { Color, Sprite, Texture, Graphics } from 'pixi.js';

const red = new Color('red'); // Named color
const green = new Color(0x00ff00); // Hex
const blue = new Color('#0000ff'); // Hex string
const rgba = new Color({ r: 255, g: 0, b: 0, a: 0.5 }); // RGBA object

console.log(red.toArray()); // [1, 0, 0, 1]
console.log(green.toHex()); // "#00ff00"

const sprite = new Sprite(Texture.WHITE);
sprite.tint = red; // Works directly with a Color instance
```

Example 2 (ts):
```ts
import { Graphics, Sprite, Texture } from 'pixi.js';

const sprite = new Sprite(Texture.WHITE);
sprite.tint = 'red'; // converted internally

const graphics = new Graphics();
graphics.fill({ color: '#00ff00' }); // Also converted internally
```

---

## Mesh

**URL:** llms-txt#mesh

**Contents:**
- **What Is a Mesh?**
- **MeshGeometry**
- Built-in Mesh Types
  - MeshSimple
  - MeshRope
  - MeshPlane
  - PerspectiveMesh
- **API Reference**
- NineSlice Sprite

PixiJS v8 offers a powerful `Mesh` system that provides full control over geometry, UVs, indices, shaders, and WebGL/WebGPU state. Meshes are ideal for custom rendering effects, advanced distortion, perspective manipulation, or performance-tuned rendering pipelines.

## **What Is a Mesh?**

A mesh is a low-level rendering primitive composed of:

- **Geometry**: Vertex positions, UVs, indices, and other attributes
- **Shader**: A GPU program that defines how the geometry is rendered
- **State**: GPU state configuration (e.g. blending, depth, stencil)

With these elements, you can build anything from simple quads to curved surfaces and procedural effects.

All meshes in PixiJS are built using the `MeshGeometry` class. This class allows you to define the vertex positions, UV coordinates, and indices that describe the mesh's shape and texture mapping.

You can access and modify buffers directly:

## Built-in Mesh Types

A minimal wrapper over `Mesh` that accepts vertex, UV, and index arrays directly. Suitable for fast static or dynamic meshes.

- Use `autoUpdate = true` to update geometry per frame.
- Access `mesh.vertices` to read/write data.

Bends a texture along a series of control points, often used for trails, snakes, and animated ribbons.

- `textureScale > 0` repeats texture; `0` stretches it.
- `autoUpdate = true` re-evaluates geometry each frame.

A flexible subdivided quad mesh, suitable for distortion or grid-based warping.

- Automatically resizes on texture update when `autoResize = true`.

A special subclass of `MeshPlane` that applies perspective correction by transforming the UVs.

- Set corner coordinates via `setCorners(...)`.
- Ideal for emulating 3D projection in 2D.

- [Mesh](https://pixijs.download/release/docs/scene.Mesh.html)
- [MeshGeometry](https://pixijs.download/release/docs/scene.MeshGeometry.html)
- [MeshSimple](https://pixijs.download/release/docs/scene.MeshSimple.html)
- [MeshRope](https://pixijs.download/release/docs/scene.MeshRope.html)
- [MeshPlane](https://pixijs.download/release/docs/scene.MeshPlane.html)
- [PerspectiveMesh](https://pixijs.download/release/docs/scene.PerspectiveMesh.html)
- [Shader](https://pixijs.download/release/docs/rendering.Shader.html)
- [Texture](https://pixijs.download/release/docs/rendering.Texture.html)

**Examples:**

Example 1 (ts):
```ts
import { Texture, Mesh, MeshGeometry, Shader } from 'pixi.js';

const geometry = new MeshGeometry({
  positions: new Float32Array([0, 0, 100, 0, 100, 100, 0, 100]),
  uvs: new Float32Array([0, 0, 1, 0, 1, 1, 0, 1]),
  indices: new Uint32Array([0, 1, 2, 0, 2, 3]),
});

const shader = Shader.from({
  gl: {
    vertex: `
            attribute vec2 aPosition;
            attribute vec2 aUV;
            varying vec2 vUV;
            void main() {
                gl_Position = vec4(aPosition / 100.0 - 1.0, 0.0, 1.0);
                vUV = aUV;
            }
        `,
    fragment: `
            precision mediump float;
            varying vec2 vUV;
            uniform sampler2D uSampler;
            void main() {
                gl_FragColor = texture2D(uSampler, vUV);
            }
        `,
  },
  resources: {
    uSampler: Texture.from('image.png').source,
  },
});

const mesh = new Mesh({ geometry, shader });
app.stage.addChild(mesh);
```

Example 2 (ts):
```ts
const geometry = new MeshGeometry({
  positions: Float32Array, // 2 floats per vertex
  uvs: Float32Array, // matching number of floats
  indices: Uint32Array, // 3 indices per triangle
  topology: 'triangle-list',
});
```

Example 3 (ts):
```ts
geometry.positions[0] = 50;
geometry.uvs[0] = 0.5;
geometry.indices[0] = 1;
```

Example 4 (ts):
```ts
const mesh = new MeshSimple({
  texture: Texture.from('image.png'),
  vertices: new Float32Array([0, 0, 100, 0, 100, 100, 0, 100]),
  uvs: new Float32Array([0, 0, 1, 0, 1, 1, 0, 1]),
  indices: new Uint32Array([0, 1, 2, 0, 2, 3]),
});
```

---

## Sprite

**URL:** llms-txt#sprite

**Contents:**
- Updating the Texture
- **Scale vs Width/Height**
- API Reference
- Bitmap Text

Sprites are the foundational visual elements in PixiJS. They represent a single image to be displayed on the screen. Each [Sprite](https://pixijs.download/release/docs/scene.Sprite.html) contains a [Texture](https://pixijs.download/release/docs/rendering.Texture.html) to be drawn, along with all the transformation and display state required to function in the scene graph.

## Updating the Texture

If you change the texture of a sprite, it will automatically:

- Rebind listeners for texture updates
- Recalculate width/height if set so that the visual size remains the same
- Trigger a visual update

## **Scale vs Width/Height**

Sprites inherit `scale` from `Container`, allowing for percentage-based resizing:

Sprites also have `width` and `height` properties that act as _convenience setters_ for `scale`, based on the texture’s dimensions:

- [Sprite](https://pixijs.download/release/docs/scene.Sprite.html)
- [Texture](https://pixijs.download/release/docs/rendering.Texture.html)
- [Assets](https://pixijs.download/release/docs/assets.Assets.html)

**Examples:**

Example 1 (ts):
```ts
import { Assets, Sprite } from 'pixi.js';

const texture = await Assets.load('path/to/image.png');
const sprite = new Sprite(texture);

sprite.anchor.set(0.5);
sprite.position.set(100, 100);
sprite.scale.set(2);
sprite.rotation = Math.PI / 4; // Rotate 45 degrees
```

Example 2 (ts):
```ts
const texture = Assets.get('path/to/image.png');
sprite.texture = texture;
```

Example 3 (ts):
```ts
sprite.scale.set(2); // Double the size
```

Example 4 (ts):
```ts
sprite.width = 100; // Automatically updates scale.x
// sets: sprite.scale.x = 100 / sprite.texture.orig.width;
```

---

## Renderers

**URL:** llms-txt#renderers

**Contents:**
- Renderer Types
- Creating a Renderer
- Rendering a Scene
- Resizing the Renderer
- Generating Textures
- Resetting State
- API Reference
- Cache As Texture

PixiJS renderers are responsible for drawing your scene to a canvas using either **WebGL/WebGL2** or **WebGPU**. These renderers are high-performance GPU-accelerated engines and are composed of modular systems that manage everything from texture uploads to rendering pipelines.

All PixiJS renderers inherit from a common base, which provides consistent methods such as `.render()`, `.resize()`, and `.clear()` as well as shared systems for managing the canvas, texture GC, events, and more.

| Renderer         | Description                                                        | Status          |
| ---------------- | ------------------------------------------------------------------ | --------------- |
| `WebGLRenderer`  | Default renderer using WebGL/WebGL2. Well supported and stable.    | ✅ Recommended  |
| `WebGPURenderer` | Modern GPU renderer using WebGPU. More performant, still maturing. | 🚧 Experimental |
| `CanvasRenderer` | Fallback renderer using 2D canvas.                                 | ❌ Coming-soon  |

:::info
The WebGPU renderer is feature complete, however, inconsistencies in browser implementations may lead to unexpected behavior. It is recommended to use the WebGL renderer for production applications.
:::

## Creating a Renderer

You can use `autoDetectRenderer()` to create the best renderer for the environment:

Or construct one explicitly:

To render a scene, you can use the `render()` method. This will draw the specified container to the screen or a texture:

## Resizing the Renderer

To resize the renderer, use the `resize()` method. This will adjust the canvas size and update the resolution:

## Generating Textures

You can generate textures from containers using the `generateTexture()` method. This is useful for creating textures from dynamic content:

To reset the renderer's state, use the `resetState()` method. This is useful when mixing PixiJS with other libraries like Three.js:

See our full guide on [mixing PixiJS with Three.js](../../third-party/mixing-three-and-pixi.mdx) for more details.

- [Overview](https://pixijs.download/release/docs/rendering.html)
- [AbstractRenderer](https://pixijs.download/release/docs/rendering.AbstractRenderer.html)
- [WebGLRenderer](https://pixijs.download/release/docs/rendering.WebGLRenderer.html)
- [WebGPURenderer](https://pixijs.download/release/docs/rendering.WebGPURenderer.html)
- [AutoDetectRenderer](https://pixijs.download/release/docs/rendering.html#autoDetectRenderer)

**Examples:**

Example 1 (ts):
```ts
import { autoDetectRenderer } from 'pixi.js';

const renderer = await autoDetectRenderer({
  preference: 'webgpu', // or 'webgl'
});
```

Example 2 (ts):
```ts
import { WebGLRenderer, WebGPURenderer } from 'pixi.js';

const renderer = new WebGLRenderer();
await renderer.init(options);
```

Example 3 (ts):
```ts
import { Container } from 'pixi.js';

const container = new Container();
renderer.render(container);

// or provide a complete set of options
renderer.render({
  target: container,
  clear: true, // clear the screen before rendering
  transform: new Matrix(), // optional transform to apply to the container
});
```

Example 4 (ts):
```ts
renderer.resize(window.innerWidth, window.innerHeight);
```

---

## Render Loop

**URL:** llms-txt#render-loop

**Contents:**
- Overview
- Step 1: Running Ticker Callbacks
  - Example
- Step 2: Updating the Scene Graph
- Step 3: Rendering the Scene
- Full Frame Lifecycle Diagram
- Scene Graph

At the core of PixiJS lies its **render loop**, a repeating cycle that updates and redraws your scene every frame. Unlike traditional web development where rendering is event-based (e.g. on user input), PixiJS uses a continuous animation loop that provides full control over real-time rendering.

This guide provides a deep dive into how PixiJS structures this loop internally, from the moment a frame begins to when it is rendered to the screen. Understanding this will help you write more performant, well-structured applications.

Each frame, PixiJS performs the following sequence:

1. **Tickers are executed** (user logic)
2. **Scene graph is updated** (transforms and culling)
3. **Rendering occurs** (GPU draw calls)

This cycle repeats as long as your application is running and its ticker is active.

## Step 1: Running Ticker Callbacks

The render loop is driven by the `Ticker` class, which uses `requestAnimationFrame` to schedule work. Each tick:

- Measures elapsed time since the previous frame
- Caps it based on `minFPS` and `maxFPS`
- Calls every listener registered with `ticker.add()` or `app.ticker.add()`

Every callback receives the current `Ticker` instance. You can access `ticker.deltaTime` (scaled frame delta) and `ticker.elapsedMS` (unscaled delta in ms) to time animations.

## Step 2: Updating the Scene Graph

PixiJS uses a hierarchical **scene graph** to represent all visual objects. Before rendering, the graph needs to be traversed to:

- Recalculate transforms (world matrix updates)
- Apply custom logic via `onRender` handlers
- Apply culling if enabled

## Step 3: Rendering the Scene

Once the scene graph is ready, the renderer walks the display list starting at `app.stage`:

1. Applies global and local transformations
2. Batches draw calls when possible
3. Uploads geometry, textures, and uniforms
4. Issues GPU commands

All rendering is **retained mode**: objects persist across frames unless explicitly removed.

Rendering is done via either WebGL or WebGPU, depending on your environment. The renderer abstracts away the differences behind a common API.

## Full Frame Lifecycle Diagram

**Examples:**

Example 1 (ts):
```ts
app.ticker.add((ticker) => {
  bunny.rotation += ticker.deltaTime * 0.1;
});
```

Example 2 (plaintext):
```plaintext
requestAnimationFrame
        │
    [Ticker._tick()]
        │
    ├─ Compute elapsed time
    ├─ Call user listeners
    │   └─ sprite.onRender
    ├─ Cull display objects (if enabled)
    ├─ Update world transforms
    └─ Render stage
            ├─ Traverse display list
            ├─ Upload data to GPU
            └─ Draw
```

---

## Filters / Blend Modes

**URL:** llms-txt#filters-/-blend-modes

**Contents:**
- Applying Filters
- Advanced Blend Modes
- Built-In Filters Overview
- Creating a Custom Filter
- API Reference
- Math

PixiJS filters allow you to apply post-processing visual effects to any scene object and its children. Filters can be used for effects such as blurring, color adjustments, noise, or custom shader-based operations.

Applying filters is straightforward. You can assign a filter instance to the `filters` property of any scene object, such as `Sprite`, `Container`, or `Graphics`.
You can apply multiple filters by passing an array of filter instances.

:::info
Order matters — filters are applied in sequence.
:::

## Advanced Blend Modes

PixiJS v8 introduces advanced blend modes for filters, allowing for more complex compositing effects. These blend modes can be used to create unique visual styles and effects.
To use advanced modes like `HARD_LIGHT`, you must manually import the advanced blend mode extension:

## Built-In Filters Overview

PixiJS v8 provides a variety of filters out of the box:

| Filter Class         | Description                                 |
| -------------------- | ------------------------------------------- |
| `AlphaFilter`        | Applies transparency to an object.          |
| `BlurFilter`         | Gaussian blur.                              |
| `ColorMatrixFilter`  | Applies color transformations via a matrix. |
| `DisplacementFilter` | Distorts an object using another texture.   |
| `NoiseFilter`        | Adds random noise for a grainy effect.      |

:::info
To explore more community filters, see [pixi-filters](https://pixijs.io/filters/docs/).
:::

**Blend Filters**: Used for custom compositing modes

| Filter Class       | Description                                        |
| ------------------ | -------------------------------------------------- |
| `ColorBurnBlend`   | Darkens the base color to reflect the blend color. |
| `ColorDodgeBlend`  | Brightens the base color.                          |
| `DarkenBlend`      | Retains the darkest color components.              |
| `DivideBlend`      | Divides the base color by the blend color.         |
| `HardMixBlend`     | High-contrast blend.                               |
| `LinearBurnBlend`  | Darkens using linear formula.                      |
| `LinearDodgeBlend` | Lightens using linear formula.                     |
| `LinearLightBlend` | Combination of linear dodge and burn.              |
| `PinLightBlend`    | Selective replacement of colors.                   |
| `SubtractBlend`    | Subtracts the blend color from base.               |

## Creating a Custom Filter

To define a custom filter in PixiJS v8, you use `Filter.from()` with shader programs and GPU resources.

:::info **Tip**
Shaders must be WebGL- or WebGPU-compatible. For dual-renderer support, include a `gpuProgram`.
:::

- [Overview](https://pixijs.download/release/docs/filters.html)
- [Filter](https://pixijs.download/release/docs/filters.Filter.html)

**Examples:**

Example 1 (ts):
```ts
import { Sprite, BlurFilter } from 'pixi.js';

// Apply the filter
sprite.filters = [new BlurFilter({ strength: 8 })];
```

Example 2 (ts):
```ts
import { BlurFilter, NoiseFilter } from 'pixi.js';

sprite.filters = new BlurFilter({ strength: 5 });

sprite.filters = [
  new BlurFilter({ strength: 4 }),
  new NoiseFilter({ noise: 0.2 }),
];
```

Example 3 (ts):
```ts
import 'pixi.js/advanced-blend-modes';
import { HardMixBlend } from 'pixi.js';

sprite.filters = [new HardMixBlend()];
```

Example 4 (ts):
```ts
import { Filter, GlProgram, Texture } from 'pixi.js';

const vertex = `
  in vec2 aPosition;
  out vec2 vTextureCoord;

  uniform vec4 uInputSize;
  uniform vec4 uOutputFrame;
  uniform vec4 uOutputTexture;

  vec4 filterVertexPosition( void )
  {
      vec2 position = aPosition * uOutputFrame.zw + uOutputFrame.xy;

      position.x = position.x * (2.0 / uOutputTexture.x) - 1.0;
      position.y = position.y * (2.0*uOutputTexture.z / uOutputTexture.y) - uOutputTexture.z;

      return vec4(position, 0.0, 1.0);
  }

  vec2 filterTextureCoord( void )
  {
      return aPosition * (uOutputFrame.zw * uInputSize.zw);
  }

  void main(void)
  {
      gl_Position = filterVertexPosition();
      vTextureCoord = filterTextureCoord();
  }
`;

const fragment = `
  in vec2 vTextureCoord;
  in vec4 vColor;

  uniform sampler2D uTexture;
  uniform float uTime;

  void main(void)
  {
      vec2 uvs = vTextureCoord.xy;

      vec4 fg = texture2D(uTexture, vTextureCoord);

      fg.r = uvs.y + sin(uTime);

      gl_FragColor = fg;

  }
`;

const customFilter = new Filter({
  glProgram: new GlProgram({
    fragment,
    vertex,
  }),
  resources: {
    timeUniforms: {
      uTime: { value: 0.0, type: 'f32' },
    },
  },
});

// Apply the filter
sprite.filters = [customFilter];

// Update uniform
app.ticker.add((ticker) => {
  filter.resources.timeUniforms.uniforms.uTime += 0.04 * ticker.deltaTime;
});
```

---

## Particle Container

**URL:** llms-txt#particle-container

**Contents:**
- **Why Use ParticleContainer?**
  - **Performance Tip: Static vs. Dynamic**
- **Limitations and API Differences**
  - ❌ Not Available:
  - ✅ Use Instead:
- **Creating a Particle**
  - **Particle Example**
- **API Reference**
- Sprite

PixiJS v8 introduces a high-performance particle system via the `ParticleContainer` and `Particle` classes. Designed for rendering vast numbers of lightweight visuals—like sparks, bubbles, bunnies, or explosions—this system provides raw speed by stripping away all non-essential overhead.

:::warning **Experimental API Notice**
The Particle API is stable but **experimental**. Its interface may evolve in future PixiJS versions. We welcome feedback to help guide its development.
:::

## **Why Use ParticleContainer?**

- **Extreme performance**: Render hundreds of thousands or even millions of particles with high FPS.
- **Lightweight design**: Particles are more efficient than `Sprite`, lacking extra features like children, events, or filters.
- **Fine-grained control**: Optimize rendering by declaring which properties are dynamic (updated every frame) or static (set once).

### **Performance Tip: Static vs. Dynamic**

- **Dynamic properties** are uploaded to the GPU every frame.
- **Static properties** are uploaded only when `update()` is called.

Declare your needs explicitly:

If you later modify a static property or the particle list, you must call:

## **Limitations and API Differences**

`ParticleContainer` is designed for speed and simplicity. As such, it doesn't support the full `Container` API:

- `addChild()`, `removeChild()`
- `getChildAt()`, `setChildIndex()`
- `swapChildren()`, `reparentChild()`

- `addParticle(particle)`
- `removeParticle(particle)`
- `removeParticles(beginIndex, endIndex)`
- `addParticleAt(particle, index)`
- `removeParticleAt(index)`

These methods operate on the `.particleChildren` array and maintain the internal GPU buffers correctly.

## **Creating a Particle**

A `Particle` supports key display properties, and is far more efficient than `Sprite`.

### **Particle Example**

You can also use the shorthand:

- [ParticleContainer](https://pixijs.download/release/docs/scene.ParticleContainer.html)
- [Particle](https://pixijs.download/release/docs/scene.Particle.html)

**Examples:**

Example 1 (ts):
```ts
import { ParticleContainer, Particle, Texture } from 'pixi.js';

const texture = Texture.from('bunny.png');

const container = new ParticleContainer({
  dynamicProperties: {
    position: true, // default
    vertex: false,
    rotation: false,
    color: false,
  },
});

for (let i = 0; i < 100000; i++) {
  const particle = new Particle({
    texture,
    x: Math.random() * 800,
    y: Math.random() * 600,
  });

  container.addParticle(particle);
}

app.stage.addChild(container);
```

Example 2 (ts):
```ts
const container = new ParticleContainer({
  dynamicProperties: {
    position: true,
    rotation: true,
    vertex: false,
    color: false,
  },
});
```

Example 3 (ts):
```ts
container.update();
```

Example 4 (ts):
```ts
const particle = new Particle({
  texture: Texture.from('spark.png'),
  x: 200,
  y: 100,
  scaleX: 0.8,
  scaleY: 0.8,
  rotation: Math.PI / 4,
  tint: 0xff0000,
  alpha: 0.5,
});
```

---

## Ticker

**URL:** llms-txt#ticker

**Contents:**
- Adding and Removing Listeners
- Controlling the Ticker
- Prioritizing Listeners
- Configuring FPS
  - `minFPS`
  - `maxFPS`
- API Reference
- Mixing PixiJS and Three.js

The `Ticker` class in PixiJS provides a powerful and flexible mechanism for executing callbacks on every animation frame. It's useful for managing game loops, animations, and any time-based updates.

## Adding and Removing Listeners

The `Ticker` class allows you to add multiple listeners that will be called on every frame. You can also specify a context for the callback, which is useful for maintaining the correct `this` reference.

## Controlling the Ticker

To automatically start the ticker when a listener is added, enable `autoStart`:

## Prioritizing Listeners

Listeners can be assigned a priority. Higher values run earlier.

Available constants include:

- `UPDATE_PRIORITY.HIGH = 50`
- `UPDATE_PRIORITY.NORMAL = 0`
- `UPDATE_PRIORITY.LOW = -50`

Tickers allows FPS limits to control the update rate.

Caps how _slow_ frames are allowed to be. Used to clamp `deltaTime`:

Limits how _fast_ the ticker runs. Useful for conserving CPU/GPU:

Set to `0` to allow unlimited framerate:

- [Ticker](https://pixijs.download/release/docs/ticker.Ticker.html)
- [Application](https://pixijs.download/release/docs/app.Application.html)

## Mixing PixiJS and Three.js

**Examples:**

Example 1 (ts):
```ts
import { Ticker } from 'pixi.js';

const ticker = new Ticker();

ticker.add((ticker) => {
  console.log(`Delta Time: ${ticker.deltaTime}`);
});

// Start the ticker
ticker.start();
```

Example 2 (ts):
```ts
ticker.add(myFunction, myContext);
ticker.addOnce(myFunction, myContext);
ticker.remove(myFunction, myContext);
```

Example 3 (ts):
```ts
ticker.start(); // Begin calling listeners every frame
ticker.stop(); // Pause the ticker and cancel the animation frame
```

Example 4 (ts):
```ts
ticker.autoStart = true;
```

---

## Scene Graph

**URL:** llms-txt#scene-graph

**Contents:**
- The Scene Graph Is a Tree
- Parents and Children
- Render Order
- RenderGroups
- Culling
- Local vs Global Coordinates
- Global vs Screen Coordinates
- Accessibility

Every frame, PixiJS is updating and then rendering the scene graph. Let's talk about what's in the scene graph, and how it impacts how you develop your project. If you've built games before, this should all sound very familiar, but if you're coming from HTML and the DOM, it's worth understanding before we get into specific types of objects you can render.

## The Scene Graph Is a Tree

The scene graph's root node is a container maintained by the application, and referenced with `app.stage`. When you add a sprite or other renderable object as a child to the stage, it's added to the scene graph and will be rendered and interactable. PixiJS `Containers` can also have children, and so as you build more complex scenes, you will end up with a tree of parent-child relationships, rooted at the app's stage.

(A helpful tool for exploring your project is the [Pixi.js devtools plugin](https://chrome.google.com/webstore/detail/pixijs-devtools/aamddddknhcagpehecnhphigffljadon) for Chrome, which allows you to view and manipulate the scene graph in real time as it's running!)

## Parents and Children

When a parent moves, its children move as well. When a parent is rotated, its children are rotated too. Hide a parent, and the children will also be hidden. If you have a game object that's made up of multiple sprites, you can collect them under a container to treat them as a single object in the world, moving and rotating as one.

Each frame, PixiJS runs through the scene graph from the root down through all the children to the leaves to calculate each object's final position, rotation, visibility, transparency, etc. If a parent's alpha is set to 0.5 (making it 50% transparent), all its children will start at 50% transparent as well. If a child is then set to 0.5 alpha, it won't be 50% transparent, it will be 0.5 x 0.5 = 0.25 alpha, or 75% transparent. Similarly, an object's position is relative to its parent, so if a parent is set to an x position of 50 pixels, and the child is set to an x position of 100 pixels, it will be drawn at a screen offset of 150 pixels, or 50 + 100.

Here's an example. We'll create three sprites, each a child of the last, and animate their position, rotation, scale and alpha. Even though each sprite's properties are set to the same values, the parent-child chain amplifies each change:

The cumulative translation, rotation, scale and skew of any given node in the scene graph is stored in the object's
`worldTransform` property. Similarly, the cumulative alpha value is stored in the `worldAlpha` property.

So we have a tree of things to draw. Who gets drawn first?

PixiJS renders the tree from the root down. At each level, the current object is rendered, then each child is rendered in order of insertion. So the second child is rendered on top of the first child, and the third over the second.

Check out this example, with two parent objects A & D, and two children B & C under A:

If you'd like to re-order a child object, you can use `setChildIndex()`. To add a child at a given point in a parent's list, use `addChildAt()`. Finally, you can enable automatic sorting of an object's children using the `sortableChildren` option combined with setting the `zIndex` property on each child.

As you delve deeper into PixiJS, you'll encounter a powerful feature known as Render Groups. Think of Render Groups as specialized containers within your scene graph that act like mini scene graphs themselves. Here's what you need to know to effectively use Render Groups in your projects. For more info check out the [RenderGroups overview](./render-groups.md)

If you're building a project where a large proportion of your scene objects are off-screen (say, a side-scrolling game), you will want to _cull_ those objects. Culling is the process of evaluating if an object (or its children!) is on the screen, and if not, turning off rendering for it. If you don't cull off-screen objects, the renderer will still draw them, even though none of their pixels end up on the screen.

PixiJS provides built-in support for viewport culling. To enable culling, set `cullable = true` on your objects. You can also set `cullableChildren` to `false` to allow PixiJS to bypass the recursive culling function, which can improve performance. Additionally, you can set `cullArea` to further optimize performance by defining the area to be culled.

## Local vs Global Coordinates

If you add a sprite to the stage, by default it will show up in the top left corner of the screen. That's the origin of the global coordinate space used by PixiJS. If all your objects were children of the stage, that's the only coordinates you'd need to worry about. But once you introduce containers and children, things get more complicated. A child object at [50, 100] is 50 pixels right and 100 pixels down _from its parent_.

We call these two coordinate systems "global" and "local" coordinates. When you use `position.set(x, y)` on an object, you're always working in local coordinates, relative to the object's parent.

The problem is, there are many times when you want to know the global position of an object. For example, if you want to cull offscreen objects to save render time, you need to know if a given child is outside the view rectangle.

To convert from local to global coordinates, you use the `toGlobal()` function. Here's a sample usage:

This snippet will set `globalPos` to be the global coordinates for the child object, relative to [0, 0] in the global coordinate system.

## Global vs Screen Coordinates

When your project is working with the host operating system or browser, there is a third coordinate system that comes into play - "screen" coordinates (aka "viewport" coordinates). Screen coordinates represent position relative to the top-left of the canvas element that PixiJS is rendering into. Things like the DOM and native mouse click events work in screen space.

Now, in many cases, screen space is equivalent to world space. This is the case if the size of the canvas is the same as the size of the render view specified when you create you `Application`. By default, this will be the case - you'll create for example an 800x600 application window and add it to your HTML page, and it will stay that size. 100 pixels in world coordinates will equal 100 pixels in screen space. BUT! It is common to stretch the rendered view to have it fill the screen, or to render at a lower resolution and up-scale for speed. In that case, the screen size of the canvas element will change (e.g. via CSS), but the underlying render view will _not_, resulting in a mis-match between world coordinates and screen coordinates.

**Examples:**

Example 1 (ts):
```ts
import { Application, Assets, Container, Sprite } from 'pixi.js';

(async () => {
  // Create the application helper and add its render target to the page
  const app = new Application();

  await app.init({ resizeTo: window });
  document.body.appendChild(app.canvas);

  // Add a container to center our sprite stack on the page
  const container = new Container({
    x: app.screen.width / 2,
    y: app.screen.height / 2,
  });

  app.stage.addChild(container);

  // load the texture
  const tex = await Assets.load('https://pixijs.com/assets/bunny.png');

  // Create the 3 sprites, each a child of the last
  const sprites = [];
  let parent = container;

  for (let i = 0; i < 3; i++) {
    const wrapper = new Container();
    const sprite = Sprite.from(tex);

    sprite.anchor.set(0.5);
    wrapper.addChild(sprite);
    parent.addChild(wrapper);
    sprites.push(wrapper);
    parent = wrapper;
  }

  // Set all sprite's properties to the same value, animated over time
  let elapsed = 0.0;

  app.ticker.add((delta) => {
    elapsed += delta.deltaTime / 60;
    const amount = Math.sin(elapsed);
    const scale = 1.0 + 0.25 * amount;
    const alpha = 0.75 + 0.25 * amount;
    const angle = 40 * amount;
    const x = 75 * amount;

    for (let i = 0; i < sprites.length; i++) {
      const sprite = sprites[i];

      sprite.scale.set(scale);
      sprite.alpha = alpha;
      sprite.angle = angle;
      sprite.x = x;
    }
  });
})();
```

Example 2 (ts):
```ts
import { Application, Container, Sprite, Text, Texture } from 'pixi.js';

(async () => {
  // Create the application helper and add its render target to the page
  const app = new Application();

  await app.init({ resizeTo: window });
  document.body.appendChild(app.canvas);

  // Label showing scene graph hierarchy
  const label = new Text({
    text: 'Scene Graph:\n\napp.stage\n  ┗ A\n     ┗ B\n     ┗ C\n  ┗ D',
    style: { fill: '#ffffff' },
    position: { x: 300, y: 100 },
  });

  app.stage.addChild(label);

  // Helper function to create a block of color with a letter
  const letters = [];

  function addLetter(letter, parent, color, pos) {
    const bg = new Sprite(Texture.WHITE);

    bg.width = 100;
    bg.height = 100;
    bg.tint = color;

    const text = new Text({
      text: letter,
      style: { fill: '#ffffff' },
    });

    text.anchor.set(0.5);
    text.position = { x: 50, y: 50 };

    const container = new Container();

    container.position = pos;
    container.visible = false;
    container.addChild(bg, text);
    parent.addChild(container);

    letters.push(container);

    return container;
  }

  // Define 4 letters
  const a = addLetter('A', app.stage, 0xff0000, { x: 100, y: 100 });
  const b = addLetter('B', a, 0x00ff00, { x: 20, y: 20 });
  const c = addLetter('C', a, 0x0000ff, { x: 20, y: 40 });
  const d = addLetter('D', app.stage, 0xff8800, { x: 140, y: 100 });

  // Display them over time, in order
  let elapsed = 0.0;

  app.ticker.add((ticker) => {
    elapsed += ticker.deltaTime / 60.0;
    if (elapsed >= letters.length) {
      elapsed = 0.0;
    }
    for (let i = 0; i < letters.length; i++) {
      letters[i].visible = elapsed >= i;
    }
  });
})();
```

Example 3 (javascript):
```javascript
// Get the global position of an object, relative to the top-left of the screen
let globalPos = obj.toGlobal(new Point(0, 0));
```

---

## Managing Garbage Collection in PixiJS

**URL:** llms-txt#managing-garbage-collection-in-pixijs

**Contents:**
- Explicit Resource Management with `destroy`
- Managing Textures with `texture.unload`
- Automatic Texture Garbage Collection with `TextureGCSystem`
  - Customizing `TextureGCSystem`
- Best Practices for Garbage Collection in PixiJS
- Performance Tips

Efficient resource management is crucial for maintaining optimal performance in any PixiJS application. This guide explores how PixiJS handles garbage collection, the tools it provides, and best practices for managing GPU resources effectively.

## Explicit Resource Management with `destroy`

PixiJS objects, such as textures, meshes, and other GPU-backed data, hold references that consume memory. To explicitly release these resources, call the `destroy` method on objects you no longer need. For example:

Calling `destroy` ensures that the object’s GPU resources are freed immediately, reducing the likelihood of memory leaks and improving performance.

## Managing Textures with `texture.unload`

In cases where PixiJS’s automatic texture garbage collection is insufficient, you can manually unload textures from the GPU using `texture.unload()`:

This is particularly useful for applications that dynamically load large numbers of textures and require precise memory control.

## Automatic Texture Garbage Collection with `TextureGCSystem`

PixiJS also includes the `TextureGCSystem`, a system that manages GPU texture memory. By default:

- **Removes textures unused for 3600 frames** (approximately 1 minute at 60 FPS).
- **Checks every 600 frames** for unused textures.

### Customizing `TextureGCSystem`

You can adjust the behavior of `TextureGCSystem` to suit your application:

- **`textureGCActive`**: Enable or disable garbage collection. Default: `true`.
- **`textureGCMaxIdle`**: Maximum idle frames before texture cleanup. Default: `3600` frames.
- **`textureGCCheckCountMax`**: Frequency of garbage collection checks (in frames). Default: `600` frames.

Example configuration:

## Best Practices for Garbage Collection in PixiJS

1. **Explicitly Destroy Objects:** Always call `destroy` on objects you no longer need to ensure GPU resources are promptly released.
2. **Use Pooling:** Reuse objects with a pooling system to reduce allocation and deallocation overhead.
3. **Proactively Manage Textures:** Use `texture.unload()` for manual memory management when necessary.

By following these practices and understanding PixiJS’s garbage collection mechanisms, you can create high-performance applications that efficiently utilize system resources.

**Examples:**

Example 1 (javascript):
```javascript
import { Sprite } from 'pixi.js';

const sprite = new Sprite(texture);
// Use the sprite in your application

// When no longer needed
sprite.destroy();
```

Example 2 (javascript):
```javascript
import { Texture } from 'pixi.js';

const texture = Texture.from('image.png');

// Use the texture

// When no longer needed
texture.unload();
```

Example 3 (javascript):
```javascript
import { Application } from 'pixi.js';

const app = new Application();

await app.init({
  textureGCActive: true, // Enable texture garbage collection
  textureGCMaxIdle: 7200, // 2 hours idle time
  textureGCCheckCountMax: 1200, // Check every 20 seconds at 60 FPS
});
```

---

## Resize Plugin

**URL:** llms-txt#resize-plugin

**Contents:**
- Usage
  - Default Behavior
  - Manual Registration
  - Custom Resize Target
- API Reference
- Ticker Plugin

The `ResizePlugin` provides automatic resizing functionality for PixiJS applications. When enabled, it listens to window or element resize events and resizes the application's renderer accordingly.

- Making the canvas responsive to the browser window
- Maintaining aspect ratio or fitting to containers
- Handling layout changes without manual resize calls

By default, PixiJS adds this plugin when initializing an `Application`, but you can also register it manually if you're using a custom setup.

- When using `Application.init()` with no overrides, the `ResizePlugin` is installed automatically:
- When `resizeTo` is set, the renderer automatically adjusts to match the dimensions of the target (`window` or `HTMLElement`).
- Resizing is throttled using `requestAnimationFrame` to prevent performance issues during rapid resize events.
- You can trigger a resize manually with `app.resize()` or cancel a scheduled resize with `app.cancelResize()`.

### Manual Registration

If you're managing extensions manually:

### Custom Resize Target

You can specify a custom target for resizing. This is useful if you want to resize the canvas to fit a specific element rather than the entire window.

- [`ResizePlugin`](https://pixijs.download/release/docs/app.ResizePlugin.html)

**Examples:**

Example 1 (ts):
```ts
import { Application } from 'pixi.js';

const app = new Application();

await app.init({
  width: 800,
  height: 600,
  resizeTo: window,
});
```

Example 2 (ts):
```ts
import { extensions, ResizePlugin } from 'pixi.js';

extensions.add(ResizePlugin);
```

Example 3 (ts):
```ts
await app.init({
  resizeTo: document.getElementById('game-container'),
});
```

---

## Compressed Textures

**URL:** llms-txt#compressed-textures

**Contents:**
- Supported Compressed Texture Formats
- Registering Loaders
- Using Compressed Textures in Assets
- Integration with AssetPack
  - Example
- Assets

Compressed textures significantly reduce memory usage and GPU upload time, especially on mobile devices or lower-end hardware. PixiJS supports multiple compressed texture formats, but **you must configure the appropriate loaders** before using them.

## Supported Compressed Texture Formats

PixiJS provides built-in support for several widely-used compressed texture formats:

| Format    | File Extension | Description                                                             |
| --------- | -------------- | ----------------------------------------------------------------------- |
| **DDS**   | `.dds`         | DirectDraw Surface format, supports DXT variants (S3TC)                 |
| **KTX**   | `.ktx`         | Khronos format, supports ETC and other schemes                          |
| **KTX2**  | `.ktx2`        | Modern container supporting Basis Universal and Supercompressed formats |
| **Basis** | `.basis`       | Highly compressed format that can transcode to multiple GPU formats     |

## Registering Loaders

PixiJS does **not automatically include compressed texture support**. To use these formats, you must explicitly import the necessary loaders before loading any assets:

:::info
You only need to import the loaders for the formats you're using. These imports must run **before** any call to `Assets.load`.
:::

## Using Compressed Textures in Assets

Once loaders are registered, you can load compressed textures just like any other asset:

PixiJS will parse and upload the texture using the correct loader and GPU-compatible transcoding path based on the user's device.

## Integration with AssetPack

[**AssetPack**](https://pixijs.io/assetpack) supports automatic generation of compressed texture variants during the build step. You can:

- Convert `.png` or `.jpg` files into `.basis`, `.ktx2`, or `.dds` formats.
- Reference compressed files in your manifest using the same aliases or wildcard patterns.
- Use the **same manifest and loading workflow** — PixiJS will resolve and load the best available variant based on the device.

Your manifest might include:

PixiJS will try to load `bg.ktx2` or `bg.basis` first if the device supports it, falling back to `bg.png` as needed.

**Examples:**

Example 1 (ts):
```ts
import 'pixi.js/dds';
import 'pixi.js/ktx';
import 'pixi.js/ktx2';
import 'pixi.js/basis';
```

Example 2 (ts):
```ts
import 'pixi.js/ktx2'; // Import the KTX2 loader
import { Assets } from 'pixi.js';

await Assets.load('textures/background.ktx2');
```

Example 3 (json):
```json
{
  "bundles": [
    {
      "name": "scene",
      "assets": [
        {
          "alias": "bg",
          "src": ["assets/bg.ktx2", "assets/bg.basis", "assets/bg.png"]
        }
      ]
    }
  ]
}
```

---

## SplitText & SplitBitmapText

**URL:** llms-txt#splittext-&-splitbitmaptext

**Contents:**
- What Are SplitText & SplitBitmapText?
- Basic Usage
  - SplitText Example
  - SplitBitmapText Example
- Accessing Segments
- Anchor Points Explained
- Animation Example (with GSAP)
- Creating from Existing Text
- Configuration Options
- Global Defaults

The `SplitText` and `SplitBitmapText` classes let you break a string into individual lines, words, and characters—each as its own display object—unlocking rich, per-segment animations and advanced text layout effects.

These classes work just like regular `Text` or `BitmapText`, but provide fine-grained control over every part of your text.

:::warning
**Experimental:** These features are new and may evolve in future versions.
:::

## What Are SplitText & SplitBitmapText?

Both `SplitText` and `SplitBitmapText` extend PixiJS containers, generating nested display objects for each line, word, and character of your string.

The difference is in the underlying text rendering:

| Class             | Base Type    | Best For                      |
| ----------------- | ------------ | ----------------------------- |
| `SplitText`       | `Text`       | Richly styled text            |
| `SplitBitmapText` | `BitmapText` | High-performance dynamic text |

- Per-character or per-word animations
- Line-based entrance or exit effects
- Interactive text elements
- Complex animated typography

### SplitText Example

### SplitBitmapText Example

## Accessing Segments

Both classes provide convenient segment arrays:

Each line contains its words, and each word contains its characters.

## Anchor Points Explained

Segment anchors control the origin for transformations like rotation or scaling.

Normalized range: `0` (start) to `1` (end)

| Anchor    | Meaning      |
| --------- | ------------ |
| `0,0`     | Top-left     |
| `0.5,0.5` | Center       |
| `1,1`     | Bottom-right |

## Animation Example (with GSAP)

## Creating from Existing Text

Convert existing text objects into segmented versions:

## Configuration Options

Shared options for both classes:

| Option       | Description                                         | Default    |
| ------------ | --------------------------------------------------- | ---------- |
| `text`       | String content to render and split                  | _Required_ |
| `style`      | Text style configuration (varies by text type)      | `{}`       |
| `autoSplit`  | Auto-update segments when text or style changes     | `true`     |
| `lineAnchor` | Anchor for line containers (`number` or `{x, y}`)   | `0`        |
| `wordAnchor` | Anchor for word containers (`number` or `{x, y}`)   | `0`        |
| `charAnchor` | Anchor for character objects (`number` or `{x, y}`) | `0`        |

Change global defaults for each class:

⚠️ **Character Spacing:**
Splitting text into individual objects removes browser or font kerning. Expect slight differences in spacing compared to standard `Text`.

Splitting text creates additional display objects. For simple static text, a regular `Text` object is more efficient. Use `SplitText` when you need:

- Per-segment animations
- Interactive or responsive text effects
- Complex layouts

The same performance limitations outlined [here](./index.md) apply for these classes as well.

- [Text](https://pixijs.download/release/docs/scene.Text.html)
- [TextStyle](https://pixijs.download/release/docs/text.TextStyle.html)
- [BitmapFont](https://pixijs.download/release/docs/text.BitmapFont.html)
- [SplitText](https://pixijs.download/release/docs/text.SplitText.html)
- [SplitBitmapText](https://pixijs.download/release/docs/text.SplitBitmapText.html)

**Examples:**

Example 1 (ts):
```ts
import { SplitText } from 'pixi.js';

const text = new SplitText({
  text: 'Hello World',
  style: { fontSize: 32, fill: 0xffffff },

  // Optional: Anchor points (0-1 range)
  lineAnchor: 0.5, // Center lines
  wordAnchor: { x: 0, y: 0.5 }, // Left-center words
  charAnchor: { x: 0.5, y: 1 }, // Bottom-center characters
  autoSplit: true,
});

app.stage.addChild(text);
```

Example 2 (ts):
```ts
import { SplitBitmapText, BitmapFont } from 'pixi.js';

// Ensure your bitmap font is installed
BitmapFont.install({
  name: 'Game Font',
  style: { fontFamily: 'Arial', fontSize: 32 },
});

const text = new SplitBitmapText({
  text: 'High Performance',
  style: { fontFamily: 'Game Font', fontSize: 32 },
  autoSplit: true,
});

app.stage.addChild(text);
```

Example 3 (ts):
```ts
console.log(text.lines); // Array of line containers
console.log(text.words); // Array of word containers
console.log(text.chars); // Array of character display objects
```

Example 4 (ts):
```ts
const text = new SplitText({
  text: 'Animate Me',
  lineAnchor: { x: 1, y: 0 }, // Top-right lines
  wordAnchor: 0.5, // Center words
  charAnchor: { x: 0, y: 1 }, // Bottom-left characters
});
```

---

## Textures

**URL:** llms-txt#textures

**Contents:**
- Texture Lifecycle
  - Lifecycle Flow
  - Loading Textures
  - Preparing Textures
- Texture vs. TextureSource
- Texture Creation
- Destroying Textures
- Unload Texture from GPU
- Texture Types
- Common Texture Properties

Textures are one of the most essential components in the PixiJS rendering pipeline. They define the visual content used by Sprites, Meshes, and other renderable objects. This guide covers how textures are loaded, created, and used, along with the various types of data sources PixiJS supports.

The texture system is built around two major classes:

- **`TextureSource`**: Represents a pixel source, such as an image, canvas, or video.
- **`Texture`**: Defines a view into a `TextureSource`, including sub-rectangles, trims, and transformations.

Textures can be loaded asynchronously using the `Assets` system:

### Preparing Textures

Even after you've loaded your textures, the images still need to be pushed to the GPU and decoded. Doing this for a large number of source images can be slow and cause lag spikes when your project first loads. To solve this, you can use the [Prepare](https://pixijs.download/release/docs/rendering.PrepareSystem.html) plugin, which allows you to pre-load textures in a final step before displaying your project.

## Texture vs. TextureSource

The `TextureSource` handles the raw pixel data and GPU upload. A `Texture` is a lightweight view on that source, with metadata such as trimming, frame rectangle, UV mapping, etc. Multiple `Texture` instances can share a single `TextureSource`, such as in a sprite sheet.

You can manually create textures using the constructor:

Set `dynamic: true` in the `Texture` options if you plan to modify its `frame`, `trim`, or `source` at runtime.

## Destroying Textures

Once you're done with a Texture, you may wish to free up the memory (both WebGL-managed buffers and browser-based) that it uses. To do so, you should call `Assets.unload('texture.png')`, or `texture.destroy()` if you have created the texture outside of Assets.

This is a particularly good idea for short-lived imagery like cut-scenes that are large and will only be used once. If a texture is destroyed that was loaded via `Assets` then the assets class will automatically remove it from the cache for you.

## Unload Texture from GPU

If you want to unload a texture from the GPU but keep it in memory, you can call `texture.source.unload()`. This will remove the texture from the GPU but keep the source in memory.

PixiJS supports multiple `TextureSource` types, depending on the kind of input data:

| Texture Type          | Description                                                       |
| --------------------- | ----------------------------------------------------------------- |
| **ImageSource**       | HTMLImageElement, ImageBitmap, SVG's, VideoFrame, etc.            |
| **CanvasSource**      | HTMLCanvasElement or OffscreenCanvas                              |
| **VideoSource**       | HTMLVideoElement with optional auto-play and update FPS           |
| **BufferImageSource** | TypedArray or ArrayBuffer with explicit width, height, and format |
| **CompressedSource**  | Array of compressed mipmaps (Uint8Array\[])                       |

## Common Texture Properties

Here are some important properties of the `Texture` class:

- `frame`: Rectangle defining the visible portion within the source.
- `orig`: Original untrimmed dimensions.
- `trim`: Defines trimmed regions to exclude transparent space.
- `uvs`: UV coordinates generated from `frame` and `rotate`.
- `rotate`: GroupD8 rotation value for atlas compatibility.
- `defaultAnchor`: Default anchor when used in Sprites.
- `defaultBorders`: Used for 9-slice scaling.
- `source`: The `TextureSource` instance.

## Common TextureSource Properties

Here are some important properties of the `TextureSource` class:

- `resolution`: Affects render size relative to actual pixel size.
- `format`: Texture format (e.g., `rgba8unorm`, `bgra8unorm`, etc.)
- `alphaMode`: Controls how alpha is interpreted on upload.
- `wrapMode` / `scaleMode`: Controls how texture is sampled outside of bounds or when scaled.
- `autoGenerateMipmaps`: Whether to generate mipmaps on upload.

You can set these properties when creating a `TextureSource`:

- [Texture](https://pixijs.download/release/docs/rendering.Texture.html)
- [TextureSource](https://pixijs.download/release/docs/rendering.TextureSource.html)
- [TextureStyle](https://pixijs.download/release/docs/rendering.TextureStyle.html)
- [RenderTexture](https://pixijs.download/release/docs/rendering.RenderTexture.html)

**Examples:**

Example 1 (unknown):
```unknown
Source File/Image -> TextureSource -> Texture -> Sprite (or other display object)
```

Example 2 (ts):
```ts
const texture = await Assets.load('myTexture.png');

const sprite = new Sprite(texture);
```

Example 3 (ts):
```ts
const sheet = await Assets.load('spritesheet.json');
const heroTexture = sheet.textures['hero.png'];
```

Example 4 (ts):
```ts
const mySource = new TextureSource({ resource: myImage });
const texture = new Texture({ source: mySource });
```

---

## PixiJS Documentation for LLMs

**URL:** llms-txt#pixijs-documentation-for-llms

**Contents:**
- Ecosystem
- Core Ecosystem Libraries
  - [DevTools](https://pixijs.io/devtools/)
  - [React Integration](https:/react.pixijs.io/)
  - [Layout](https://layout.pixijs.io/)
  - [Spine Integration](https://esotericsoftware.com/spine-pixi)
  - [Filters](https://github.com/pixijs/filters)
  - [Sound](https://github.com/pixijs/sound)
  - [UI](https://github.com/pixijs/ui)
  - [AssetPack](https://pixijs.io/assetpack/)

> PixiJS is the fastest, most lightweight 2D library available for the web, working across all devices and allowing you to create rich, interactive graphics and cross-platform applications using WebGL and WebGPU.

This file contains all documentation content in a single document following the llmtxt.org standard.

PixiJS itself is just a rendering engine. However, there is a foundation of a robust ecosystem of libraries and tools that enhance and expand its capabilities. These tools integrate seamlessly with PixiJS, empowering developers to create richer, more interactive applications with ease.

## Core Ecosystem Libraries

### [DevTools](https://pixijs.io/devtools/)

Optimize and debug your PixiJS projects with DevTools. This browser extension offers real-time insights into application performance, rendering hierarchies, and texture management, ensuring your projects run smoothly.

### [React Integration](https:/react.pixijs.io/)

:::info
PixiJS React requires React 19 or higher.
:::

Simplify the use of PixiJS in React applications with the Pixi-React library. This library provides bindings that allow you to manage PixiJS components as React elements, making it easy to incorporate powerful graphics into React's declarative framework.

### [Layout](https://layout.pixijs.io/)

Add flexbox-style layouting to PixiJS with the PixiJS Layout library, which is powered by Facebook’s [Yoga](https://www.yogalayout.dev/) engine. It introduces a declarative way to control positioning, alignment, and sizing of PixiJS display objects using familiar CSS-like rules.

Key features include:

- Built on Yoga for standardized, reliable layouts
- Fully opt-in: apply layout only where you need it
- Any PixiJS object can now be layout-aware
- Supports PixiJS React
- New web-style features: objectFit, objectPosition, and overflow scrolling

### [Spine Integration](https://esotericsoftware.com/spine-pixi)

Bring animations to life with Spine-Pixi. This integration combines the power of PixiJS and Spine, a leading animation tool, to create smooth, skeletal-based animations for games and interactive content.

### [Filters](https://github.com/pixijs/filters)

Transform your visuals with PixiJS Filters. This extensive collection of high-performance effects includes options like blur, glow, and color adjustments, giving you the tools to create visually stunning graphics.

### [Sound](https://github.com/pixijs/sound)

Add audio to your projects with PixiJS Sound a WebAudio API playback library, with filters.

### [UI](https://github.com/pixijs/ui)

Streamline the creation of user interfaces with PixiJS UI. This library offers pre-built components:

- Buttons
- Sliders
- Progress bars
- Lists
- Scrollbox
- Radio Groups
- Checkboxes
- Switches

All the essentials for building interactive interfaces in PixiJS.

### [AssetPack](https://pixijs.io/assetpack/)

Simplify asset management with AssetPack. This tool organizes, packages, and loads assets efficiently, reducing load times and improving resource handling for your projects.

## [PixiJS Userland](https://github.com/pixijs-userland) - Community-Driven Repositories

PixiJS Userland is a dedicated space for hosting community-driven repositories. This organization allows developers to collaborate on PixiJS-related projects and share their work with the wider community.

If you have an idea for a new library or tool, you can request access to PixiJS Userland to create and maintain a repository within the organization. This is a great opportunity to contribute to the growing PixiJS ecosystem and engage with like-minded developers.

Note that userland repositories are community-driven and may not be up to date with the latest PixiJS releases. However, they offer a wealth of resources and inspiration for developers looking to enhance their PixiJS projects.

## Getting Started with the Ecosystem

To explore these libraries, visit their respective documentation and GitHub repositories for installation instructions and usage guides. Additionally, PixiJS offers [**Creation Templates**](https://pixijs.io/create-pixi/docs/guide/creations/intro/) through the [PixiJS Create CLI](https://pixijs.io/create-pixi/) that combine many of these libraries into pre-configured setups, ideal for specific use cases and platforms.

For inspiration, you can also check out the [open-games repository](https://github.com/pixijs/open-games), which showcases a variety of games built with PixiJS and its ecosystem libraries.

---

## Cache As Texture

**URL:** llms-txt#cache-as-texture

**Contents:**
  - Using `cacheAsTexture` in PixiJS
  - What Is `cacheAsTexture`?
  - Basic Usage
  - Advanced Usage
  - Benefits of `cacheAsTexture`
  - Advanced Details
  - How It Works Internally
  - Best Practices
  - Gotchas
- Container

### Using `cacheAsTexture` in PixiJS

The `cacheAsTexture` function in PixiJS is a powerful tool for optimizing rendering in your applications. By rendering a container and its children to a texture, `cacheAsTexture` can significantly improve performance for static or infrequently updated containers. Let's explore how to use it effectively, along with its benefits and considerations.

:::info[Note]
`cacheAsTexture` is PixiJS v8's equivalent of the previous `cacheAsBitmap` functionality. If you're migrating from v7 or earlier, simply replace `cacheAsBitmap` with `cacheAsTexture` in your code.
:::

### What Is `cacheAsTexture`?

When you set `container.cacheAsTexture()`, the container is rendered to a texture. Subsequent renders reuse this texture instead of rendering all the individual children of the container. This approach is particularly useful for containers with many static elements, as it reduces the rendering workload.

To update the texture after making changes to the container, call:

and to turn it off, call:

Here's an example that demonstrates how to use `cacheAsTexture`:

In this example, the `container` and its children are rendered to a single texture, reducing the rendering overhead when the scene is drawn.

Instead of enabling cacheAsTexture with true, you can pass a configuration object which is very similar to texture source options.

- `resolution` is the resolution of the texture. By default this is the same as you renderer or application.
- `antialias` is the antialias mode to use for the texture. Much like the resolution this defaults to the renderer or application antialias mode.

### Benefits of `cacheAsTexture`

- **Performance Boost**: Rendering a complex container as a single texture avoids the need to process each child element individually during each frame.
- **Optimized for Static Content**: Ideal for containers with static or rarely updated children.

- **Memory Tradeoff**: Each cached texture requires GPU memory. Using `cacheAsTexture` trades rendering speed for increased memory usage.
- **GPU Limitations**: If your container is too large (e.g., over 4096x4096 pixels), the texture may fail to cache, depending on GPU limitations.

### How It Works Internally

Under the hood, `cacheAsTexture` converts the container into a render group and renders it to a texture. It uses the same texture cache mechanism as filters:

Once the texture is cached, updating it via `updateCacheTexture()` is efficient and incurs minimal overhead. Its as fast as rendering the container normally.

- **Use for Static Content**: Apply `cacheAsTexture` to containers with elements that don't change frequently, such as a UI panel with static decorations.
- **Leverage for Performance**: Use `cacheAsTexture` to render complex containers as a single texture, reducing the overhead of processing each child element individually every frame. This is especially useful for containers that contain expensive effects eg filters.
- **Switch of Antialiasing**: setting antialiasing to false can give a small performance boost, but the texture may look a bit more pixelated around its children's edges.
- **Resolution**: Do adjust the resolution based on your situation, if something is scaled down, you can use a lower resolution.If something is scaled up, you may want to use a higher resolution. But be aware that the higher the resolution the larger the texture and memory footprint.

- **Apply to Very Large Containers**: Avoid using `cacheAsTexture` on containers that are too large (e.g., over 4096x4096 pixels), as they may fail to cache due to GPU limitations. Instead, split them into smaller containers.
- **Overuse for Dynamic Content**: Flick `cacheAsTexture` on / off frequently on containers, as this results in constant re-caching, negating its benefits. Its better to Cache as texture when you once, and then use `updateCacheTexture` to update it.
- **Apply to Sparse Content**: Do not use `cacheAsTexture` for containers with very few elements or sparse content, as the performance improvement will be negligible.
- **Ignore Memory Impact**: Be cautious of GPU memory usage. Each cached texture consumes memory, so overusing `cacheAsTexture` can lead to resource constraints.

- **Rendering Depends on Scene Visibility**: The cache updates only when the containing scene is rendered. Modifying the layout after setting `cacheAsTexture` but before rendering your scene will be reflected in the cache.

- **Containers are rendered with no transform**: Cached items are rendered at their actual size, ignoring transforms like scaling. For instance, an item scaled down by 50%, its texture will be cached at 100% size and then scaled down by the scene.

- **Caching and Filters**: Filters may not behave as expected with `cacheAsTexture`. To cache the filter effect, wrap the item in a parent container and apply `cacheAsTexture` to the parent.

- **Reusing the texture**: If you want to create a new texture based on the container, its better to use `const texture = renderer.generateTexture(container)` and share that amongst you objects!

By understanding and applying `cacheAsTexture` strategically, you can significantly enhance the rendering performance of your PixiJS projects. Happy coding!

**Examples:**

Example 1 (javascript):
```javascript
container.updateCacheTexture();
```

Example 2 (javascript):
```javascript
container.cacheAsTexture(false);
```

Example 3 (javascript):
```javascript
import * as PIXI from 'pixi.js';

(async () => {
  // Create a new application
  const app = new Application();

  // Initialize the application
  await app.init({ background: '#1099bb', resizeTo: window });

  // Append the application canvas to the document body
  document.body.appendChild(app.canvas);

  // load sprite sheet..
  await Assets.load('https://pixijs.com/assets/spritesheet/monsters.json');

  // holder to store aliens
  const aliens = [];
  const alienFrames = [
    'eggHead.png',
    'flowerTop.png',
    'helmlok.png',
    'skully.png',
  ];

  let count = 0;

  // create an empty container
  const alienContainer = new Container();

  alienContainer.x = 400;
  alienContainer.y = 300;

  app.stage.addChild(alienContainer);

  // add a bunch of aliens with textures from image paths
  for (let i = 0; i < 100; i++) {
    const frameName = alienFrames[i % 4];

    // create an alien using the frame name..
    const alien = Sprite.from(frameName);

    alien.tint = Math.random() * 0xffffff;

    alien.x = Math.random() * 800 - 400;
    alien.y = Math.random() * 600 - 300;
    alien.anchor.x = 0.5;
    alien.anchor.y = 0.5;
    aliens.push(alien);
    alienContainer.addChild(alien);
  }

  // this will cache the container and its children as a single texture
  // so instead of drawing 100 sprites, it will draw a single texture!
  alienContainer.cacheAsTexture();
})();
```

Example 4 (typescript):
```typescript
container.cacheAsTexture({
  resolution: 2,
  antialias: true,
});
```

---

## Container

**URL:** llms-txt#container

**Contents:**
- What Is a Container?
- Managing Children
  - Events
  - Finding Children
  - Sorting Children
- Optimizing with Render Groups
- Cache as Texture
- API Reference
- Graphics Fill

The `Container` class is the foundation of PixiJS's scene graph system. Containers act as groups of scene objects, allowing you to build complex hierarchies, organize rendering layers, and apply transforms or effects to groups of objects.

## What Is a Container?

A `Container` is a general-purpose node that can hold other display objects, **including other containers**. It is used to structure your scene, apply transformations, and manage rendering and interaction.

Containers are **not** rendered directly. Instead, they delegate rendering to their children.

PixiJS provides a robust API for adding, removing, reordering, and swapping children in a container:

You can also remove a child by index or remove all children within a range:

To keep a child’s world transform while moving it to another container, use `reparentChild` or `reparentChildAt`:

Containers emit events when children are added or removed:

Containers support searching children by `label` using helper methods:

Set `deep = true` to search recursively through all descendants.

Use `zIndex` and `sortableChildren` to control render order within a container:

Call `sortChildren()` to manually re-sort if needed:

:::info
Use this feature sparingly, as sorting can be expensive for large numbers of children.
:::

## Optimizing with Render Groups

Containers can be promoted to **render groups** by setting `isRenderGroup = true` or calling `enableRenderGroup()`.

Use render groups for UI layers, particle systems, or large moving subtrees.
See the [Render Groups guide](../../../concepts/render-groups.md) for more details.

The `cacheAsTexture` function in PixiJS is a powerful tool for optimizing rendering in your applications. By rendering a container and its children to a texture, `cacheAsTexture` can significantly improve performance for static or infrequently updated containers.

When you set `container.cacheAsTexture()`, the container is rendered to a texture. Subsequent renders reuse this texture instead of rendering all the individual children of the container. This approach is particularly useful for containers with many static elements, as it reduces the rendering workload.

:::info[Note]
`cacheAsTexture` is PixiJS v8's equivalent of the previous `cacheAsBitmap` functionality. If you're migrating from v7 or earlier, simply replace `cacheAsBitmap` with `cacheAsTexture` in your code.
:::

For more advanced usage, including setting cache options and handling dynamic content, refer to the [Cache as Texture guide](./cache-as-texture.md).

- [Container](https://pixijs.download/release/docs/scene.Container.html)
- [ContainerOptions](https://pixijs.download/release/docs/scene.ContainerOptions.html)
- [RenderContainer](https://pixijs.download/release/docs/scene.RenderContainer.html)

**Examples:**

Example 1 (ts):
```ts
import { Container, Sprite } from 'pixi.js';

const group = new Container();
const sprite = Sprite.from('bunny.png');

group.addChild(sprite);
```

Example 2 (ts):
```ts
const container = new Container();
const child1 = new Container();
const child2 = new Container();

container.addChild(child1, child2);
container.removeChild(child1);
container.addChildAt(child1, 0);
container.swapChildren(child1, child2);
```

Example 3 (ts):
```ts
container.removeChildAt(0);
container.removeChildren(0, 2);
```

Example 4 (ts):
```ts
otherContainer.reparentChild(child);
```

---

## Text (Canvas)

**URL:** llms-txt#text-(canvas)

**Contents:**
- Text Styling
- **Changing Text Dynamically**
- Text Resolution
- Font Loading
- API Reference
- HTML Text

The `Text` class in PixiJS allows you to render styled, dynamic strings as display objects in your scene. Under the hood, PixiJS rasterizes the text using the browser’s canvas text API, then converts that into a texture. This makes `Text` objects behave like sprites: they can be moved, rotated, scaled, masked, and rendered efficiently.

The `TextStyle` class allows you to customize the appearance of your text. You can set properties like:

- `fontFamily`
- `fontSize`
- `fontWeight`
- `fill` (color)
- `align`
- `stroke` (outline)

See the guide on [TextStyle](./style.md) for more details.

## **Changing Text Dynamically**

You can update the text string or its style at runtime:

:::warning
Changing text or style re-rasterizes the object. Avoid doing this every frame unless necessary.
:::

The `resolution` property of the `Text` class determines the pixel density of the rendered text. By default, it uses the resolution of the renderer.

However, you can set text resolution independently from the renderer for sharper text, especially on high-DPI displays.

PixiJS supports loading custom fonts via the `Assets` API. It supports many of the common font formats:

- `woff`
- `woff2`
- `ttf`
- `otf`

It is recommended to use `woff2` for the best performance and compression.

Below is a list of properties you can pass in the `data` object when loading a font:

| Property            | Description                                             |
| ------------------- | ------------------------------------------------------- |
| **family**          | The font family name.                                   |
| **display**         | The display property of the FontFace interface.         |
| **featureSettings** | The featureSettings property of the FontFace interface. |
| **stretch**         | The stretch property of the FontFace interface.         |
| **style**           | The style property of the FontFace interface.           |
| **unicodeRange**    | The unicodeRange property of the FontFace interface.    |
| **variant**         | The variant property of the FontFace interface.         |
| **weights**         | The weights property of the FontFace interface.         |

- [Text](https://pixijs.download/release/docs/scene.Text.html)
- [TextStyle](https://pixijs.download/release/docs/text.TextStyle.html)
- [FillStyle](https://pixijs.download/release/docs/scene.FillStyle.html)
- [StrokeStyle](https://pixijs.download/release/docs/scene.StrokeStyle.html)

**Examples:**

Example 1 (ts):
```ts
import { Text, TextStyle, Assets } from 'pixi.js';

// Load font before use
await Assets.load({
    src: 'my-font.woff2',
    data: {
        family: 'MyFont', // optional
    }
});

const myText = new Text({
    text: 'Hello PixiJS!',
    style: {
      fill: '#ffffff',
      fontSize: 36,
      fontFamily: 'MyFont',
    }
    anchor: 0.5
});

app.stage.addChild(myText);
```

Example 2 (ts):
```ts
text.text = 'Updated!';
text.style.fontSize = 40; // Triggers re-render
```

Example 3 (ts):
```ts
const myText = new Text('Hello', {
  resolution: 2, // Higher resolution for sharper text
});

// change resolution
myText.resolution = 1; // Reset to default
```

Example 4 (js):
```js
await Assets.load({
  src: 'my-font.woff2',
  data: {},
});
```

---

## SVG's

**URL:** llms-txt#svg's

**Contents:**
  - Overview
  - Why Use SVGs?
  - Ways to Render SVGs in PixiJS
- 1. Rendering SVGs as Textures
  - Overview
  - Example
  - Scaling Textures
  - Pros & Cons
  - Best Use Cases
- 2. Rendering SVGs as Graphics

PixiJS provides powerful support for rendering SVGs, allowing developers to integrate scalable vector graphics seamlessly into their projects. This guide explores different ways to use SVGs in PixiJS, covering real-time rendering, performance optimizations, and potential pitfalls.

SVGs have several advantages over raster images like PNGs:

- ✅ **Smaller File Sizes** – SVGs can be significantly smaller than PNGs, especially for large but simple shapes. A high-resolution PNG may be several megabytes, while an equivalent SVG could be just a few kilobytes.
- ✅ **Scalability** – SVGs scale without losing quality, making them perfect for responsive applications and UI elements.
- ✅ **Editable After Rendering** – Unlike textures, SVGs rendered via Graphics can be modified dynamically (e.g., changing stroke colors, modifying shapes).
- ✅ **Efficient for Simple Graphics** – If the graphic consists of basic shapes and paths, SVGs can be rendered efficiently as vector graphics.

However, SVGs can also be computationally expensive to parse, particularly for intricate illustrations with many paths or effects.

### Ways to Render SVGs in PixiJS

PixiJS offers two primary ways to render SVGs:

1. **As a Texture** – Converts the SVG into a texture for rendering as a sprite.
2. **As a Graphics Object** – Parses the SVG and renders it as vector geometry.

Each method has its advantages and use cases, which we will explore below.

## 1. Rendering SVGs as Textures

SVGs can be loaded as textures and used within Sprites. This method is efficient but does not retain the scalability of vector graphics.

You can specify a resolution when loading an SVG as a texture to control its size:
This does increase memory usage, but it be of a higher fidelity.

This ensures the texture appears at the correct size and resolution.

- ✅ **Fast to render** (rendered as a quad, not geometry)
- ✅ **Good for static images**
- ✅ **Supports resolution scaling for precise sizing**
- ✅ **Ideal for complex SVGs that do not need crisp vector scaling** (e.g., UI components with fixed dimensions)
- ❌ **Does not scale cleanly** (scaling may result in pixelation)
- ❌ **Less flexibility** (cannot modify the shape dynamically)
- ❌ **Texture Size Limit** A texture can only be up to 4096x4096 pixels, so if you need to render a larger SVG, you will need to use the Graphics method.

- Background images
- Decorative elements
- Performance-critical applications where scaling isn’t needed
- Complex SVGs that do not require crisp vector scaling (e.g., fixed-size UI components)

## 2. Rendering SVGs as Graphics

PixiJS can render SVGs as real scalable vector graphics using the `Graphics` class.

If you want to use the same SVG multiple times, you can use `GraphicsContext` to share the parsed SVG data across multiple graphics objects, improving performance by parsing it once and reusing it.

### Loading SVGs as Graphics

Instead of passing an SVG string directly, you can load an SVG file using PixiJS’s `Assets.load` method. This will return a `GraphicsContext` object, which can be used to create multiple `Graphics` objects efficiently.

Since it's loaded via `Assets.load`, it will be cached and reused, much like a texture.

- ✅ **Retains vector scalability** (no pixelation when zooming)
- ✅ **Modifiable after rendering** (change colors, strokes, etc.)
- ✅ **Efficient for simple graphics**
- ✅ **fast rendering if SVG structure does not change** (no need to reparse)
- ❌ **More expensive to parse** (complex SVGs can be slow to render)
- ❌ **Not ideal for static images**

- Icons and UI elements that need resizing
- A game world that needs to remain crisp as a player zooms in
- Interactive graphics where modifying the SVG dynamically is necessary

## SVG Rendering Considerations

### Supported Features

PixiJS supports most SVG features that can be rendered in a Canvas 2D context. Below is a list of common SVG features and their compatibility:

| Feature                                 | Supported |
| --------------------------------------- | --------- |
| Basic Shapes (rect, circle, path, etc.) | ✅        |
| Gradients                               | ✅        |
| Stroke & Fill Styles                    | ✅        |
| Text Elements                           | ❌        |
| Filters (Blur, Drop Shadow, etc.)       | ❌        |
| Clipping Paths                          | ✅        |
| Patterns                                | ❌        |
| Complex Paths & Curves                  | ✅        |

### Performance Considerations

- **Complex SVGs:** Large or intricate SVGs can slow down rendering start up due to high parsing costs. Use `GraphicsContext` to cache and reuse parsed data.
- **Vector vs. Texture:** If performance is a concern, consider using SVGs as textures instead of rendering them as geometry. However, keep in mind that textures take up more memory.
- **Real-Time Rendering:** Avoid rendering complex SVGs dynamically. Preload and reuse them wherever possible.

## Best Practices & Gotchas

- ✅ **Use Graphics for scalable and dynamic SVGs**
- ✅ **Use Textures for performance-sensitive applications**
- ✅ **Use `GraphicsContext` to avoid redundant parsing**
- ✅ **Consider `resolution` when using textures to balance quality and memory**

- ⚠ **Large SVGs can be slow to parse** – Optimize SVGs before using them in PixiJS.
- ⚠ **Texture-based SVGs do not scale cleanly** – Use higher resolution if necessary.
- ⚠ **Not all SVG features are supported** – Complex filters and text elements may not work as expected.

By understanding how PixiJS processes SVGs, developers can make informed decisions on when to use `Graphics.svg()`, `GraphicsContext`, or SVG textures, balancing quality and performance for their specific use case.

**Examples:**

Example 1 (ts):
```ts
const svgTexture = await Assets.load('tiger.svg');
const mySprite = new Sprite(svgTexture);
```

Example 2 (ts):
```ts
// description: This example demonstrates loading and displaying SVG graphics using the Graphics class
import { Application, Assets, Graphics } from 'pixi.js';

(async () => {
  // Create a new application
  const app = new Application();

  // Initialize the application
  await app.init({ antialias: true, resizeTo: window });

  // Append the application canvas to the document body
  document.body.appendChild(app.canvas);

  const tigerSvg = await Assets.load({
    src: 'https://pixijs.com/assets/tiger.svg',
    data: {
      parseAsGraphicsContext: true,
    },
  });

  const graphics = new Graphics(tigerSvg);

  // line it up as this svg is not centered
  const bounds = graphics.getLocalBounds();

  graphics.pivot.set(
    (bounds.x + bounds.width) / 2,
    (bounds.y + bounds.height) / 2,
  );

  graphics.position.set(app.screen.width / 2, app.screen.height / 2);

  app.stage.addChild(graphics);

  app.ticker.add(() => {
    graphics.rotation += 0.01;
    graphics.scale.set(2 + Math.sin(graphics.rotation));
  });
})();
```

Example 3 (ts):
```ts
// description: This example demonstrates how to create and display SVG graphics using the Graphics class
import { Application, Graphics } from 'pixi.js';

(async () => {
  // Create a new application
  const app = new Application();

  // Initialize the application
  await app.init({
    antialias: true,
    backgroundColor: 'white',
    resizeTo: window,
  });

  // Append the application canvas to the document body
  document.body.appendChild(app.canvas);

  const graphics = new Graphics().svg(`
            <svg height="400" width="450" xmlns="http://www.w3.org/2000/svg">
                <!-- Draw the paths -->
                <path id="lineAB" d="M 100 350 l 150 -300" stroke="red" stroke-width="4"/>
                <path id="lineBC" d="M 250 50 l 150 300" stroke="red" stroke-width="4"/>
                <path id="lineMID" d="M 175 200 l 150 0" stroke="green" stroke-width="4"/>
                <path id="lineAC" d="M 100 350 q 150 -300 300 0" stroke="blue" fill="none" stroke-width="4"/>

                <!-- Mark relevant points -->
                <g stroke="black" stroke-width="3" fill="black">
                    <circle id="pointA" cx="100" cy="350" r="4" />
                    <circle id="pointB" cx="250" cy="50" r="4" />
                    <circle id="pointC" cx="400" cy="350" r="4" />
                </g>
            </svg>
        `);

  app.stage.addChild(graphics);
})();
```

Example 4 (ts):
```ts
// description: This example demonstrates loading a large SVG texture and displaying it as a sprite
import { Application, Assets, Sprite } from 'pixi.js';

(async () => {
  // Create a new application
  const app = new Application();

  // Initialize the application
  await app.init({ antialias: true, resizeTo: window });

  // Append the application canvas to the document body
  document.body.appendChild(app.canvas);

  const tigerTexture = await Assets.load({
    src: 'https://pixijs.com/assets/tiger.svg',
  });

  const sprite = new Sprite(tigerTexture);

  // line it up as this svg is not centered
  const bounds = sprite.getLocalBounds();

  sprite.pivot.set(
    (bounds.x + bounds.width) / 2,
    (bounds.y + bounds.height) / 2,
  );

  sprite.position.set(app.screen.width / 2, app.screen.height / 2);

  app.stage.addChild(sprite);

  app.ticker.add(() => {
    sprite.rotation += 0.01;
    sprite.scale.set(2 + Math.sin(sprite.rotation));
  });
})();
```

---

## Text

**URL:** llms-txt#text

**Contents:**
- `Text`: Rich Dynamic Text with Styles
- `BitmapText`: High-Performance Glyph Rendering
- `HTMLText`: Styled HTML Inside the Scene
- Next Steps
- API Reference
- SplitText & SplitBitmapText

Text is essential in games and applications, and PixiJS provides three different systems to cover different needs:

- **`Text`**: High-quality, styled raster text
- **`BitmapText`**: Ultra-fast, GPU-optimized bitmap fonts
- **`HTMLText`**: Richly formatted HTML inside the Pixi scene

Each approach has tradeoffs in fidelity, speed, and flexibility. Let’s look at when and how to use each one.

## `Text`: Rich Dynamic Text with Styles

The `Text` class renders using the browser's native text engine, and then converts the result into a texture. This allows for:

- Full CSS-like font control
- Drop shadows, gradients, and alignment
- Support for dynamic content and layout

- You need detailed font control
- Text changes occasionally
- Fidelity is more important than speed

- You're changing text every frame
- You need to render hundreds of instances

## `BitmapText`: High-Performance Glyph Rendering

`BitmapText` uses a pre-baked bitmap font image for glyphs, bypassing font rasterization entirely. This gives:

- High rendering speed
- Ideal for thousands of changing labels
- Low memory usage

- You need to render lots of dynamic text
- You prioritize performance over styling
- You predefine the characters and styles

- You need fine-grained style control
- You change fonts or font sizes frequently

To use `BitmapText`, you must first register a bitmap font via:

- `BitmapFont.from(...)` to create on the fly, or
- `Assets.load(...)` if using a 3rd-party BMFont or AngelCode export

## `HTMLText`: Styled HTML Inside the Scene

`HTMLText` lets you render actual HTML markup in your PixiJS scene. This allows:

- `, `, `` style formatting
- Fine layout and text flow
- Emoji, RTL, links, and more

- You want complex HTML-style markup
- Static or semi-dynamic content
- Your users expect "document-like" layout

- You need pixel-perfect performance
- You're rendering hundreds of text blocks
- You need GPU text effects

Each text type has a corresponding guide that covers setup, font loading, style options, and limitations in more detail:

- [Text Guide →](./canvas.md)
- [BitmapText Guide →](./bitmap.md)
- [HTMLText Guide →](./html.md)

- [Text](https://pixijs.download/release/docs/scene.Text.html)
- [BitmapText](https://pixijs.download/release/docs/scene.BitmapText.html)
- [HTMLText](https://pixijs.download/release/docs/scene.HTMLText.html)
- [TextStyle](https://pixijs.download/release/docs/text.TextStyle.html)
- [BitmapFont](https://pixijs.download/release/docs/text.BitmapFont.html)
- [FillStyle](https://pixijs.download/release/docs/scene.FillStyle.html)
- [StrokeStyle](https://pixijs.download/release/docs/scene.StrokeStyle.html)

## SplitText & SplitBitmapText

---

## Render Groups

**URL:** llms-txt#render-groups

**Contents:**
- Understanding RenderGroups in PixiJS
  - What Are Render Groups?
  - Why Use Render Groups?
  - Examples
  - Best Practices
- Render Layers

## Understanding RenderGroups in PixiJS

As you delve deeper into PixiJS, especially with version 8, you'll encounter a powerful feature known as RenderGroups. Think of RenderGroups as specialized containers within your scene graph that act like mini scene graphs themselves. Here's what you need to know to effectively use Render Groups in your projects:

### What Are Render Groups?

Render Groups are essentially containers that PixiJS treats as self-contained scene graphs. When you assign parts of your scene to a Render Group, you're telling PixiJS to manage these objects together as a unit. This management includes monitoring for changes and preparing a set of render instructions specifically for the group. This is a powerful tool for optimizing your rendering process.

### Why Use Render Groups?

The main advantage of using Render Groups lies in their optimization capabilities. They allow for certain calculations, like transformations (position, scale, rotation), tint, and alpha adjustments, to be offloaded to the GPU. This means that operations like moving or adjusting the Render Group can be done with minimal CPU impact, making your application more performance-efficient.

In practice, you're utilizing Render Groups even without explicit awareness. The root element you pass to the render function in PixiJS is automatically converted into a RenderGroup as this is where its render instructions will be stored. Though you also have the option to explicitly create additional RenderGroups as needed to further optimize your project.

This feature is particularly beneficial for:

- **Static Content:** For content that doesn't change often, a Render Group can significantly reduce the computational load on the CPU. In this case static refers to the scene graph structure, not that actual values of the PixiJS elements inside it (eg position, scale of things).
- **Distinct Scene Parts:** You can separate your scene into logical parts, such as the game world and the HUD (Heads-Up Display). Each part can be optimized individually, leading to overall better performance.

Check out the [container example](/8.x/examples/?example=container_transform_pivot_basic).

- **Don't Overuse:** While Render Groups are powerful, using too many can actually degrade performance. The goal is to find a balance that optimizes rendering without overwhelming the system with too many separate groups. Make sure to profile when using them. The majority of the time you won't need to use them at all!
- **Strategic Grouping:** Consider what parts of your scene change together and which parts remain static. Grouping dynamic elements separately from static elements can lead to performance gains.

By understanding and utilizing Render Groups, you can take full advantage of PixiJS's rendering capabilities, making your applications smoother and more efficient. This feature represents a powerful tool in the optimization toolkit offered by PixiJS, enabling developers to create rich, interactive scenes that run smoothly across different devices.

**Examples:**

Example 1 (ts):
```ts
const myGameWorld = new Container({
  isRenderGroup: true,
});

const myHud = new Container({
  isRenderGroup: true,
});

scene.addChild(myGameWorld, myHud);

renderer.render(scene); // this action will actually convert the scene to a render group under the hood
```

---

## HTML Text

**URL:** llms-txt#html-text

**Contents:**
- **Why Use `HTMLText`?**
- **Async Rendering Behavior**
- **Styling HTMLText**
  - **CSS Overrides**
- **API Reference**
- Text

`HTMLText` enables styled, formatted HTML strings to be rendered as part of the PixiJS scene graph. It uses an SVG `` to embed browser-native HTML inside your WebGL canvas.

This makes it ideal for rendering complex typography, inline formatting, emojis, and layout effects that are hard to replicate using traditional canvas-rendered text.

## **Why Use `HTMLText`?**

- ✅ Supports inline tags like `, `, ``, etc.
- ✅ Compatible with emojis, Unicode, and RTL text
- ✅ Fine-grained layout control via CSS
- ✅ Tag-based style overrides (`, `, etc.)

## **Async Rendering Behavior**

HTML text uses SVG `` to draw HTML inside the canvas. As a result:

- Rendering occurs **asynchronously**. Typically after the next frame.
- Text content is not immediately visible after instantiation.

## **Styling HTMLText**

`HTMLTextStyle` extends `TextStyle` and adds:

- **HTML-aware tag-based styles** via `tagStyles`
- **CSS override support** via `cssOverrides`

### **CSS Overrides**

You can apply CSS styles to the text using the `cssOverrides` property. This allows you to set properties like `text-shadow`, `text-decoration`, and more.

- [HTMLText](https://pixijs.download/release/docs/scene.HTMLText.html)
- [HTMLTextStyle](https://pixijs.download/release/docs/text.HTMLTextStyle.html)

**Examples:**

Example 1 (ts):
```ts
import { HTMLText } from 'pixi.js';

const html = new HTMLText({
  text: 'Hello PixiJS!',
  style: {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: '#ff1010',
    align: 'center',
  },
});

app.stage.addChild(html);
```

Example 2 (ts):
```ts
const fancy = new HTMLText({
  text: 'Red, Blue',
  style: {
    fontFamily: 'DM Sans',
    fontSize: 32,
    fill: '#ffffff',
    tagStyles: {
      red: { fill: 'red' },
      blue: { fill: 'blue' },
    },
  },
});
```

Example 3 (ts):
```ts
fancy.style.addOverride('text-shadow: 2px 2px 4px rgba(0,0,0,0.5)');
```

---

## Bitmap Text

**URL:** llms-txt#bitmap-text

**Contents:**
- **Why Use `BitmapText`?**
- **How to Load and Use Bitmap Fonts**
  - Font Loading
  - MSDF and SDF Fonts

`BitmapText` is a high-performance text rendering solution in PixiJS. Unlike the `Text` class, which rasterizes each string into a new texture, `BitmapText` draws characters from a pre-generated texture atlas. This design allows you to render tens of thousands of text objects with minimal overhead.

## **Why Use `BitmapText`?**

- ✅ **Fast rendering**: Perfect for HUDs, score counters, timers, etc.
- ✅ **No per-frame rasterization**: Text changes are cheap.
- ✅ **Efficient memory usage**: Shares glyph textures across all instances.
- ✅ **Supports MSDF/SDF fonts**: Crisp scaling without blurring.

- Frequently updating text
- Large numbers of text instances
- High-performance or mobile projects

## **How to Load and Use Bitmap Fonts**

PixiJS supports AngelCode BMFont format and MSDF-compatible `.fnt` and `.xml` files. You can load these files using the `Assets` API.

Once loaded, you can create a `BitmapText` instance with the loaded font using the `fontFamily` property.

### MSDF and SDF Fonts

PixiJS supports **MSDF** (multi-channel signed distance field) and **SDF** formats for crisp, resolution-independent text. These fonts remain sharp at any size and scale.

You can generate MSDF/SDF fonts using tools like [AssetPack](https://pixijs.io/assetpack/) which can take a `.ttf` or `.otf` font and generate a bitmap font atlas with MSDF/SDF support.

Using MSDF/SDF fonts is similar to using regular bitmap fonts and just requires you to load the appropriate font file:

**Examples:**

Example 1 (ts):
```ts
import { Assets, BitmapText } from 'pixi.js';

await Assets.load('fonts/MyFont.fnt');

const text = new BitmapText({
  text: 'Loaded font!',
  style: {
    fontFamily: 'MyFont',
    fontSize: 32,
    fill: '#ffcc00',
  },
});
```

Example 2 (ts):
```ts
import { Assets, BitmapText } from 'pixi.js';

await Assets.load('fonts/MyFont.fnt');

const text = new BitmapText({
  text: 'Loaded font!',
  style: {
    fontFamily: 'MyFont',
    fontSize: 32,
    fill: '#ffcc00',
  },
});
```

Example 3 (ts):
```ts
import { Assets, BitmapText } from 'pixi.js';

await Assets.load('fonts/MyMSDFFont.fnt');

const text = new BitmapText({
  text: 'Loaded MSDF font!',
  style: {
    fontFamily: 'MyMSDFFont',
  },
});
```

---

## **Limitations and Caveats**

**URL:** llms-txt#**limitations-and-caveats**

**Contents:**
  - ❌ Cannot Update Resolution
  - ⚠️ Large Character Sets Not Practical
- **API Reference**
- Text (Canvas)

### ❌ Cannot Update Resolution

`BitmapText.resolution` is not mutable. It must be handled by the `BitmapFont`

### ⚠️ Large Character Sets Not Practical

Bitmap fonts are limited by texture size. CJK or emoji-rich sets may require too much memory. Use `Text` or `HTMLText` for dynamic internationalization or emoji support.

- [BitmapText](https://pixijs.download/release/docs/scene.BitmapText.html)
- [BitmapFont](https://pixijs.download/release/docs/text.BitmapFont.html)
- [Assets](https://pixijs.download/release/docs/assets.Assets.html)
- [TextStyle](https://pixijs.download/release/docs/text.TextStyle.html)
- [FillStyle](https://pixijs.download/release/docs/scene.FillStyle.html)
- [StrokeStyle](https://pixijs.download/release/docs/scene.StrokeStyle.html)

**Examples:**

Example 1 (ts):
```ts
text.resolution = 2;
// ⚠️ [BitmapText] dynamically updating the resolution is not supported.
```

---

## Tiling Sprite

**URL:** llms-txt#tiling-sprite

**Contents:**
- What is a TilingSprite?
- Key Properties
  - Width & Height vs Scale
  - Anchor and applyAnchorToTexture
- API Reference
- Documentation for LLMs

A `TilingSprite` is a high-performance way to render a repeating texture across a rectangular area. Instead of stretching the texture, it repeats (tiles) it to fill the given space, making it ideal for backgrounds, parallax effects, terrain, and UI panels.

## What is a TilingSprite?

- It draws a texture repeatedly across a defined area.
- The texture is not scaled by default unless you adjust `tileScale`.
- The sprite's overall `width` and `height` determine how much area the tiles fill, independent of the texture's native size.
- The pattern's offset, scale, and rotation can be controlled independently of the object's transform.

| Property               | Description                                                            |
| ---------------------- | ---------------------------------------------------------------------- |
| `texture`              | The texture being repeated                                             |
| `tilePosition`         | `ObservablePoint` controlling offset of the tiling pattern             |
| `tileScale`            | `ObservablePoint` controlling scaling of each tile                     |
| `tileRotation`         | Number controlling the rotation of the tile pattern                    |
| `width` / `height`     | The size of the area to be filled by tiles                             |
| `anchor`               | Adjusts origin point of the TilingSprite                               |
| `applyAnchorToTexture` | If `true`, the anchor affects the starting point of the tiling pattern |
| `clampMargin`          | Margin adjustment to avoid edge artifacts (default: `0.5`)             |

### Width & Height vs Scale

Unlike `Sprite`, setting `width` and `height` in a `TilingSprite` directly changes the visible tiling area. It **does not affect the scale** of the tiles.

To scale the tile pattern itself, use `tileScale`:

### Anchor and applyAnchorToTexture

- `anchor` sets the pivot/origin point for positioning the TilingSprite.
- If `applyAnchorToTexture` is `true`, the anchor also affects where the tile pattern begins.
- By default, the tile pattern starts at (0, 0) in local space regardless of anchor.

- [TilingSprite](https://pixijs.download/release/docs/scene.TilingSprite.html)
- [Texture](https://pixijs.download/release/docs/rendering.Texture.html)

## Documentation for LLMs

**Examples:**

Example 1 (ts):
```ts
import { TilingSprite, Texture } from 'pixi.js';

const tilingSprite = new TilingSprite({
  texture: Texture.from('assets/tile.png'),
  width: 400,
  height: 300,
});

app.stage.addChild(tilingSprite);
```

Example 2 (ts):
```ts
// Makes the tiling area bigger
tilingSprite.width = 800;
tilingSprite.height = 600;

// Keeps tiles the same size, just tiles more of them
```

Example 3 (ts):
```ts
// Makes each tile appear larger
tilingSprite.tileScale.set(2, 2);
```

---

## Application

**URL:** llms-txt#application

**Contents:**
- Creating an Application
  - ApplicationOptions Reference
  - Customizing Application Options Per Renderer Type
- Built-In Plugins
- Creating a Custom Application Plugin
  - Adding Types
- API Reference
- Resize Plugin

The `Application` class provides a modern, extensible entry point to set up rendering in PixiJS. It abstracts common tasks like renderer setup and ticker updates, and is designed to support both WebGL and WebGPU via async initialization.

## Creating an Application

Creating an application requires two steps: constructing an instance, then initializing it asynchronously using `.init()`:

### ApplicationOptions Reference

The `.init()` method of `Application` accepts a `Partial` object with the following configuration options:

| Option                   | Type                                | Default     | Description                                                                                                                              |
| ------------------------ | ----------------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `autoStart`              | `boolean`                           | `true`      | Whether to start rendering immediately after initialization. Setting to `false` will not stop the shared ticker if it's already running. |
| `resizeTo`               | `Window \| HTMLElement`             | —           | Element to auto-resize the renderer to match.                                                                                            |
| `sharedTicker`           | `boolean`                           | `false`     | Use the shared ticker instance if `true`; otherwise, a private ticker is created.                                                        |
| `preference`             | `'webgl' \| 'webgpu'`               | `webgl`     | Preferred renderer type.                                                                                                                 |
| `useBackBuffer`          | `boolean`                           | `false`     | _(WebGL only)_ Use the back buffer when required.                                                                                        |
| `forceFallbackAdapter`   | `boolean`                           | `false`     | _(WebGPU only)_ Force usage of fallback adapter.                                                                                         |
| `powerPreference`        | `'high-performance' \| 'low-power'` | `undefined` | Hint for GPU power preference (WebGL & WebGPU).                                                                                          |
| `antialias`              | `boolean`                           | —           | Enables anti-aliasing. May impact performance.                                                                                           |
| `autoDensity`            | `boolean`                           | —           | Adjusts canvas size based on `resolution`. Applies only to `HTMLCanvasElement`.                                                          |
| `background`             | `ColorSource`                       | —           | Alias for `backgroundColor`.                                                                                                             |
| `backgroundAlpha`        | `number`                            | `1`         | Alpha transparency for background (0 = transparent, 1 = opaque).                                                                         |
| `backgroundColor`        | `ColorSource`                       | `'black'`   | Color used to clear the canvas. Accepts hex, CSS color, or array.                                                                        |
| `canvas`                 | `ICanvas`                           | —           | A custom canvas instance (optional).                                                                                                     |
| `clearBeforeRender`      | `boolean`                           | `true`      | Whether the renderer should clear the canvas each frame.                                                                                 |
| `context`                | `WebGL2RenderingContext \| null`    | `null`      | User-supplied rendering context (WebGL).                                                                                                 |
| `depth`                  | `boolean`                           | —           | Enable a depth buffer in the main view. Always `true` for WebGL.                                                                         |
| `height`                 | `number`                            | `600`       | Initial height of the renderer (in pixels).                                                                                              |
| `width`                  | `number`                            | `800`       | Initial width of the renderer (in pixels).                                                                                               |
| `hello`                  | `boolean`                           | `false`     | Log renderer info and version to the console.                                                                                            |
| `multiView`              | `boolean`                           | `false`     | Enable multi-canvas rendering.                                                                                                           |
| `preferWebGLVersion`     | `1 \| 2`                            | `2`         | Preferred WebGL version.                                                                                                                 |
| `premultipliedAlpha`     | `boolean`                           | `true`      | Assume alpha is premultiplied in color buffers.                                                                                          |
| `preserveDrawingBuffer`  | `boolean`                           | `false`     | Preserve buffer between frames. Needed for `toDataURL`.                                                                                  |
| `resolution`             | `number`                            | 1           | The resolution of the renderer.                                                                                                          |
| `skipExtensionImports`   | `boolean`                           | `false`     | Prevent automatic import of default PixiJS extensions.                                                                                   |
| `textureGCActive`        | `boolean`                           | `true`      | Enable garbage collection for GPU textures.                                                                                              |
| `textureGCCheckCountMax` | `number`                            | `600`       | Frame interval between GC runs (textures).                                                                                               |
| `textureGCMaxIdle`       | `number`                            | `3600`      | Max idle frames before destroying a texture.                                                                                             |
| `textureGCAMaxIdle`      | `number`                            | —           | (Appears undocumented; placeholder for internal GC controls.)                                                                            |

### Customizing Application Options Per Renderer Type

You can also override properties based on the renderer type by using the `WebGLOptions` or `WebGPUOptions` interfaces. For example:

- ✅ **Ticker Plugin** — Updates every frame → [Guide](./ticker-plugin.md)
- ✅ **Resize Plugin** — Resizes renderer/canvas → [Guide](./resize-plugin.md)
- ➕ **Optional: Culler Plugin** - Culls objects that are out of frame → [Guide](./culler-plugin.md)

## Creating a Custom Application Plugin

You can create custom plugins for the `Application` class. A plugin must implement the `ApplicationPlugin` interface, which includes `init()` and `destroy()` methods. You can also specify the `extension` type, which is `ExtensionType.Application` for application plugins.

Both functions are called with `this` set as the `Application` instance e.g `this.renderer` or `this.stage` is available.

The `init()` method is called when the application is initialized and passes the options from the `application.init` call, and the `destroy()` method is called when the application is destroyed.

If you are using TypeScript, or are providing a plugin for others to use, you can extend the `ApplicationOptions` interface to include your custom plugins options.

- [Overview](https://pixijs.download/release/docs/app.html)
- [Application](https://pixijs.download/release/docs/app.Application.html)
- [ApplicationOptions](https://pixijs.download/release/docs/app.ApplicationOptions.html)
  - [AutoDetectOptions](https://pixijs.download/release/docs/rendering.AutoDetectOptions.html)
  - [WebGLOptions](https://pixijs.download/release/docs/rendering.WebGLOptions.html)
  - [WebGPUOptions](https://pixijs.download/release/docs/rendering.WebGPUOptions.html)
  - [SharedRendererOptions](https://pixijs.download/release/docs/rendering.SharedRendererOptions.html)
- [TickerPlugin](https://pixijs.download/release/docs/app.TickerPlugin.html)
- [ResizePlugin](https://pixijs.download/release/docs/app.ResizePlugin.html)
- [CullerPlugin](https://pixijs.download/release/docs/app.CullerPlugin.html)

**Examples:**

Example 1 (ts):
```ts
import { Application } from 'pixi.js';

const app = new Application();

await app.init({
  width: 800,
  height: 600,
  backgroundColor: 0x1099bb,
});

document.body.appendChild(app.canvas);
```

Example 2 (ts):
```ts
import { Application } from 'pixi.js';

const app = new Application();
await app.init({
  width: 800,
  height: 600,
  backgroundColor: 0x1099bb,
  webgl: {
    antialias: true,
  },
  webgpu: {
    antialias: false,
  },
});
document.body.appendChild(app.canvas);
```

Example 3 (ts):
```ts
import type { ApplicationOptions, ApplicationPlugin, ExtensionType } from 'pixi.js';

const myPlugin: ApplicationPlugin = {
    extension: ExtensionType.Application;
    init(options: ApplicationOptions) {
        console.log('Custom plugin init:', this, options);
    },
    destroy() {
        console.log('Custom plugin destroy');
    },
};
```

Example 4 (ts):
```ts
import { extensions } from 'pixi.js';
extensions.add(myPlugin);
```

---

## Culler Plugin

**URL:** llms-txt#culler-plugin

**Contents:**
- When Should You Use It?
- Usage
  - Enabling the Culler Plugin
  - Configuring Containers for Culling
  - Optional: Define a Custom Cull Area
- Manual Culling with `Culler`
- API Reference
- Application

The `CullerPlugin` automatically skips rendering for offscreen objects in your scene. It does this by using the renderer's screen bounds to determine whether containers (and optionally their children) intersect the view. If they don't, they are **culled**, reducing rendering and update overhead.

PixiJS does not enable this plugin by default. You must manually register it using the `extensions` system.

## When Should You Use It?

Culling is ideal for:

- Large scenes with many offscreen elements
- Scrollable or camera-driven environments (e.g. tilemaps, world views)
- Optimizing render performance without restructuring your scene graph

### Enabling the Culler Plugin

To enable automatic culling in your application:

This will override the default `render()` method on your `Application` instance to call `Culler.shared.cull()` before rendering:

### Configuring Containers for Culling

By default, containers are **not culled**. To enable culling for a container, set the following properties:

### Optional: Define a Custom Cull Area

You can define a `cullArea` to override the default bounds check (which uses global bounds):

This is useful for containers with many children where bounding box calculations are expensive or inaccurate.

## Manual Culling with `Culler`

If you’re not using the plugin but want to manually cull before rendering:

- [CullerPlugin](https://pixijs.download/release/docs/app.CullerPlugin.html)

**Examples:**

Example 1 (ts):
```ts
const app = new Application();

await app.init({
  width: 800,
  height: 600,
  backgroundColor: 0x222222,
});

extensions.add(CullerPlugin);

const world = new Container();
world.cullable = true;
world.cullableChildren = true;

const sprite = new Sprite.from('path/to/image.png');
sprite.cullable = true; // Enable culling for this sprite
world.addChild(sprite);

app.stage.addChild(world);
```

Example 2 (ts):
```ts
import { extensions, CullerPlugin } from 'pixi.js';

extensions.add(CullerPlugin);
```

Example 3 (ts):
```ts
// Internally replaces:
app.renderer.render({ container: app.stage });
// With:
Culler.shared.cull(app.stage, app.renderer.screen);
app.renderer.render({ container: app.stage });
```

Example 4 (ts):
```ts
container.cullable = true; // Enables culling for this container
container.cullableChildren = true; // Enables recursive culling for children
```

---

## v8 Migration Guide

**URL:** llms-txt#v8-migration-guide

**Contents:**
- Table of Contents
- 1. Introduction {#introduction}
- 2. Breaking Changes {#breaking-changes}
  - Should I Upgrade?
  - **New Package Structure**
  - **Async Initialisation**
  - ** Texture adjustments **
  - **Graphics API Overhaul**
  - Shader changes
  - Filters

Welcome to the PixiJS v8 Migration Guide! This document is designed to help you smoothly transition your projects from PixiJS v7 to the latest and greatest PixiJS v8. Please follow these steps to ensure a successful migration.

1. [Introduction](#introduction)
2. [Breaking Changes](#breaking-changes)
3. [Deprecated Features](#deprecated-features)
4. [Resources](#resources)

## 1. Introduction {#introduction}

PixiJS v8 introduces several exciting changes and improvements that dramatically enhance the performance of the renderer. While we've made efforts to keep the migration process as smooth as possible, some breaking changes are inevitable. This guide will walk you through the necessary steps to migrate your PixiJS v7 project to PixiJS v8.

## 2. Breaking Changes {#breaking-changes}

Before diving into the migration process, let's review the breaking changes introduced in PixiJS v8. Make sure to pay close attention to these changes as they may impact your existing codebase.

### Should I Upgrade?

Generally, the answer is yes! But currently, there may be reasons that suggest it's best not to upgrade just yet. Ask yourself the following question:

- **Does your project leverage existing Pixi libraries that have not yet been migrated to v8?**
  We are working hard to migrate our key libraries to v8 but did not want this to be a blocker for those who are using pure Pixi. This means some libraries will not have a v8 counterpart just yet. It's best to hold off on migration if this is the case for you.

- Filters
- Sound
- Gif
- Storybook
- UI
- Open Games

**Migrating Right Now:**

- React
- Spine (esoteric version)

- Pixi layers (rather than migrating this, we will likely incorporate it directly into PixiJS v8 as a feature)

### **New Package Structure**

Since version 5, PixiJS has utilized individual sub-packages to organize its codebase into smaller units. However, this approach led to issues, such as conflicting installations of different PixiJS versions, causing complications with internal caches.

In v8, PixiJS has reverted to a single-package structure. While you can still import specific parts of PixiJS, you only need to install the main package.

PixiJS uses an "extensions" system to add renderer functionality. By default, PixiJS includes many extensions for a comprehensive out-of-the-box experience. However, for full control over features and bundle size, you can manually import specific PixiJS components.

When initializing the application, you can disable the auto-import feature, preventing PixiJS from importing any extensions automatically. You'll need to import them manually, as demonstrated above.

It should also be noted that the `pixi.js/text-bitmap`, also add `Assets` loading functionality.
Therefore if you want to load bitmap fonts **BEFORE** initialising the renderer, you will need to import this extension.

### **Async Initialisation**

PixiJS will now need to be initialised asynchronously. With the introduction of the WebGPU renderer PixiJS will now need to be awaited before being used

With this change it also means that the `ApplicationOptions` object can now be passed into the `init` function instead of the constructor.

### ** Texture adjustments **

Textures structures have been modified to simplify what was becoming quite a mess behind the scenes in v7.
Textures no longer know or manage loading of resources. This needs to be done upfront by you or the assets manager. Textures expect full loaded resources only. This makes things so much easier to manage as the validation of a texture can essentially be done at construction time and left at that!
BaseTexture no longer exists. In stead we now have a variety of TextureSources available. A texture source combines the settings of a texture with how to upload and use that texture. In v8 there are the following texture sources:

TextureSource - a vanilla texture that you can render too or upload however you wish. (used mainly by render textures)
ImageSource - a texture source that contains an image resource of some kind (eg ImageBitmap or html image)
CanvasSource - a canvas source that contains a canvas. Used mainly for rendering canvases or rendering to a canvas (webGPU)
VideoSource - a texture source that contains a video. Takes care of updating the texture on the GPU to ensure that they stay in sync.
BufferSource - a texture source that contains a buffer. What ever you want really! make sure your buffer type and format are compatible!
CompressedSource - a texture source that handles compressed textures. Used by the GPU compressed texture formats.

Whilst the majority of the time `Assets` will return Textures you may want to make you own! More power to ya!

To create a texture source the signature differs from baseTexture. example:

### **Graphics API Overhaul**

There are a few key changes to the Graphics API. In fact this is probably the most changed part of v8. We have added deprecations where possible but below is the rundown of changes:

- Instead of beginning a fill or a stroke and then building a shape, v8 asks you to build your shape and then stroke / fill it. The terminology of `Line` has been replaced with the terminology of `Stroke`

- Shape functions have been renamed. Each drawing function has been simplified into a shorter version of its name. They have the same parameters though:

| v7 API Call        | v8 API Equivalent |
| ------------------ | ----------------- |
| drawChamferRect    | chamferRect       |
| drawCircle         | circle            |
| drawEllipse        | ellipse           |
| drawFilletRect     | filletRect        |
| drawPolygon        | poly              |
| drawRect           | rect              |
| drawRegularPolygon | regularPoly       |
| drawRoundedPolygon | roundPoly         |
| drawRoundedRect    | roundRect         |
| drawRoundedShape   | roundShape        |
| drawStar           | star              |

- fills functions expect `FillStyle` options or a color, rather than a string of parameters. This also replaces `beginTextureFill`

- stokes functions expect `StrokeStyle` options or a color, rather than a string of parameters. This also replaces `lineTextureStyle`
  **Old:**

- holes now make use of a new `cut` function. As with `stroke` and `fill`, `cut` acts on the previous shape.
  **Old:**

- `GraphicsGeometry` has been replaced with `GraphicsContext` this allows for sharing of `Graphics` data more efficiently.

As we now need to accommodate both WebGL and WebGPU shaders, the way they are constructed has been tweaked to take this into account. The main differences you will notice (this is for shaders in general) is that Textures are no longer considered uniforms (as in they cannot be included in a uniform group). Instead we have the concept of resources. A resource can be a few things including:

- TextureSource - A source texture `myTexture.source`
- TextureStyle - A texture style `myTexture.style`
- UniformGroup - A collection of number based uniforms `myUniforms = new UniformGroup({})`
- BufferResource - A buffer that is treated as a uniform group (advanced)

creating a webgl only shader now looks like this:

Uniforms are also constructed in a slightly different way. When creating them, you now provide the type of variable you want it to be.

The best way to play and fully and get to know this new setup please check out the Mesh and Shader examples:

**old**: [v7 example](https://pixijs.com/7.x/examples/mesh-and-shaders/triangle-color)
**new**: [v8 example](https://pixijs.com/8.x/examples/mesh-and-shaders/triangle-color)

Filters work almost exactly the same, unless you are constructing a custom one. If this is the case, the shader changes mentioned above need to taken into account.

**old**: [v7 example](https://pixijs.com/7.x/examples/filters-advanced/custom)
**new**: [v8 example](https://pixijs.com/8.x/examples/filters-advanced/custom)

If you're using the [community filters](https://github.com/pixijs/filters), note that the `@pixi/filter-*` packages are no-longer maintained for v8, however, you can import directly from the `pixi-filters` package as sub-modules.

### ParticleContainer

`ParticleContainer` has been reworked in v8 to allow for far more particles than before. There are a few key changes you should be aware of:

A `ParticleContainer` no longer accepts sprites as its children. Instead, it requires a `Particle` class (or an object that implements the `IParticle` interface), which follows this interface:

The reason for this change is that sprites come with many extra properties and events that are generally unnecessary when dealing with large numbers of particles. This approach explicitly removes any ambiguity we had in v7, such as "Why doesn't my sprite work with filters?" or "Why can't I nest children in my sprites?" It’s a bit more predictable. Additionally, due to the lightweight nature of particles, this means we can render far more of them!

So, no functionality is lost—just an API tweak with a massive performance boost!

Particles are also not stored in the `children` array of the `ParticleContainer`, as particles are not technically part of the scene graph (for performance reasons). Instead, they are stored in a flat list called `particleChildren`, which is part of the `ParticleContainer` class. You can modify this array directly for extra speed, or you can use the `addParticle` and `removeParticle` methods to manage your particles.

Another optimization is that `ParticleContainer` does not calculate its own bounds, as doing so would negate the performance gains we've created! Instead, it's up to you to provide a `boundsArea` when initializing the `ParticleContainer`.

The act of adding and removing the event when a sprite's texture was changed led to an unacceptable performance drop, especially when swapping many textures (imagine shooting games with lots of keyframe textures swapping). This is why we now leave that responsibility to the user.

- New Container culling approach

With this version of PixiJS we have changed how the `cullable` property works on containers. Previously culling was done for you automatically during the render loop. However, we have moved this logic out and provided users the ability to control when culling happens themselves.

With this change we have added a couple of new properties:

- `cullable` - Whether or not the container can be culled
  - `cullArea` - A cull area that will be used instead of the bounds of the container
  - `cullableChildren` - Whether or not the containers children can be culled. This can help optimise large scenes

There is also a `CullerPlugin` that can be used to automatically call `Culler.shared.cull` every frame if you want to simulate the old behaviour.

- Renamed several mesh classes

- renamed `SimpleMesh` -> `MeshSimple`
  - renamed `SimplePlane` -> `MeshPlane`
  - renamed `SimpleRope` -> `MeshRope`

- Deprecations for `Assets` removed

- `settings` object has been removed

- Adapter and Web Worker Changes

- `settings.ADAPTER` has been removed and replaced with `DOMAdapter`

- `DOMAdapter` is a static class that can be used to set the adapter for the entire application
    - PixiJS has two adapters built in `BrowserAdapter` and `WebWorkerAdapter`
      - `BrowserAdapter` is the default adapter and is used when running in the browser
      - `WebWorkerAdapter` is used when running in a web worker

- Application type now accepts Renderer instead of view by @Zyie in https://github.com/pixijs/pixijs/pull/9740

This is to allow `app.renderer` to be typed correctly

* `Texture.from` no longer will load a texture from a URL.

When using `Texture.from` you will need to pass in a source such as `CanvasSource`/`ImageSource`/`VideoSource` or a resource such as `HTMLImageElement`/`HTMLCanvasElement`/`HTMLVideoElement` or a string that has been loaded through `Assets.load`

- The `Ticker`'s callback will now pass the `Ticker` instance instead of the delta time.
  This is to allow for more control over what unit of time is used.

- Text parsers have been renamed

- `TextFormat` -> `bitmapFontTextParser`
  - `XMLStringFormat` -> `bitmapFontXMLStringParser`
  - `XMLFormat` -> `bitmapFontXMLParser`

- The default `eventMode` is now `passive` instead of `auto`

- `utils` has been removed. All the functions are available as direct imports.

- `container.getBounds()` now returns a [`Bounds`](https://pixijs.download/release/docs/rendering.Bounds.html) object instead of a [`Rectangle`](https://pixijs.download/release/docs/maths.Rectangle.html) object. You can access the rectangle by using `container.getBounds().rectangle` instead.

- `container.cacheAsBitmap` has been replaced with `container.cacheAsTexture()`. They do the same things, except we changed the name `cacheAsTexture` as the Bitmap terminology is not really relevant to PixiJS.

## 3. Deprecated Features {#deprecated-features}

Certain features from PixiJS v7 have been deprecated in v8. While they will still work, it's recommended to update your code to use the new alternatives. Refer to the deprecated features section for details on what to replace them with.

- Leaf nodes no longer allow children

Only `Containers` can have children. This means that `Sprite`, `Mesh`, `Graphics` etc can no longer have children.

To replicate the old behaviour you can create a `Container` and add the leaf nodes to it.

- `Application.view` replaced with `Application.canvas`

- `NineSlicePlane` renamed to `NineSliceSprite`

- `SCALE_MODES` replaced with `ScaleMode` strings

- `SCALE_MODES.NEAREST` -> `'nearest'`,
  - `SCALE_MODES.LINEAR` -> `'linear'`,

- `WRAP_MODES` replaced with `WrapMode` strings

- `WRAP_MODES.CLAMP` -> `'clamp-to-edge'`,
  - `WRAP_MODES.REPEAT` -> `'repeat'`,
  - `WRAP_MODES.MIRRORED_REPEAT` -> `'mirror-repeat'`,

- `DRAW_MODES` replaced with `Topology` strings

- `DRAW_MODES.POINTS` -> `'point-list'`,
  - `DRAW_MODES.LINES` -> `'line-list'`,
  - `DRAW_MODES.LINE_STRIP` -> `'line-strip'`,
  - `DRAW_MODES.TRIANGLES` -> `'triangle-list'`,
  - `DRAW_MODES.TRIANGLE_STRIP` -> `'triangle-strip'`,

- Constructors have largely been changed to accept objects instead of multiple arguments

- `container.name` is now `container.label`

## 4. Resources {#resources}

- [PixiJS v8 Release Notes](https://github.com/pixijs/pixijs/releases?q=v8.0.0&expanded=true)
- [PixiJS Discord](https://discord.gg/CPTjeb28nH)
- [PixiJS Issues](https://github.com/pixijs/pixijs/issues)

## Bug Bounty Program

**Examples:**

Example 1 (ts):
```ts
import { Application } from '@pixi/app';
import { Sprite } from '@pixi/sprite';
```

Example 2 (ts):
```ts
import { Application, Sprite } from 'pixi.js';
```

Example 3 (ts):
```ts
// imported by default
import 'pixi.js/accessibility';
import 'pixi.js/app';
import 'pixi.js/events';
import 'pixi.js/filters';
import 'pixi.js/sprite-tiling';
import 'pixi.js/text';
import 'pixi.js/text-bitmap';
import 'pixi.js/text-html';
import 'pixi.js/graphics';
import 'pixi.js/mesh';
import 'pixi.js/sprite-nine-slice';

// not added by default, everyone needs to import these manually
import 'pixi.js/advanced-blend-modes';
import 'pixi.js/unsafe-eval';
import 'pixi.js/prepare';
import 'pixi.js/math-extras';
import 'pixi.js/dds';
import 'pixi.js/ktx';
import 'pixi.js/ktx2';
import 'pixi.js/basis';

import { Application } from 'pixi.js';

const app = new Application();

await app.init({
  manageImports: false, // disable importing the above extensions
});
```

Example 4 (ts):
```ts
import 'pixi.js/text-bitmap';
import { Assets, Application } from 'pixi.js';

await Assets.load('my-font.fnt'); // If 'pixi.js/text-bitmap' is not imported, this will not load
await new Application().init();
```

---

## Text Style

**URL:** llms-txt#text-style

**Contents:**
- Fill and Stroke
- Drop Shadow
- **API Reference**
- Tiling Sprite

The `TextStyle` class encapsulates all visual styling properties for text. You can define colors, font families, stroke, shadows, alignment, line spacing, word wrapping, and more.

A `TextStyle` instance can be reused across multiple `Text` objects, making your code cleaner and improving memory efficiency.

Using fills and strokes are identical to that of the `Graphics` class. You can find more details about them in the [Graphics Fills](../graphics/graphics-fill.md) section.

In v8 `dropShadow` and its properties are now objects. To update a drop shadow, you can set the properties directly on the `dropShadow` object.

- [TextStyle](https://pixijs.download/release/docs/text.TextStyle.html)
- [Text](https://pixijs.download/release/docs/scene.Text.html)
- [BitmapText](https://pixijs.download/release/docs/scene.BitmapText.html)
- [HTMLText](https://pixijs.download/release/docs/scene.HTMLText.html)
- [FillStyle](https://pixijs.download/release/docs/scene.FillStyle.html)
- [StrokeStyle](https://pixijs.download/release/docs/scene.StrokeStyle.html)

**Examples:**

Example 1 (ts):
```ts
import { TextStyle } from 'pixi.js';

const style = new TextStyle({
  fontFamily: 'Arial',
  fontSize: 30,
  fill: '#ffffff',
  stroke: '#000000',
  strokeThickness: 3,
  dropShadow: {
    color: '#000000',
    blur: 5,
    distance: 4,
    angle: Math.PI / 4,
    alpha: 0.5,
  },
});

const label = new Text({
  text: 'Score: 1234',
  style,
});
```

Example 2 (ts):
```ts
// Using a number
const fill = 0xff0000;

// Using a hex string
const fill = '#ff0000';

// Using an array
const fill = [255, 0, 0];

// Using a Color object
const color = new Color();
const obj4 = color;

// Using a gradient
const fill = new FillGradient({
  type: 'linear',
  colorStops: [
    { offset: 0, color: 'yellow' },
    { offset: 1, color: 'green' },
  ],
});

// Using a pattern
const txt = await Assets.load('https://pixijs.com/assets/bg_scene_rotate.jpg');
const fill = new FillPattern(txt, 'repeat');

// Use the fill in a TextStyle
const style = new TextStyle({
  fontSize: 48,
  fill: fill,
  stroke: {
    fill,
    width: 4,
  },
});
```

Example 3 (ts):
```ts
const style = new TextStyle({
  dropShadow: {
    color: '#000000',
    alpha: 0.5,
    angle: Math.PI / 4,
    blur: 5,
    distance: 4,
  },
});

style.dropShadow.color = '#ff0000'; // Change shadow color
```

---

## Bug Bounty Program

**URL:** llms-txt#bug-bounty-program

**Contents:**
- How It Works
- Terms & Conditions
- Sponsoring Bounties
- **Finding Bounty Issues**
- Why We're Doing This
- Questions?
- FAQ

PixiJS is committed to delivering a reliable, high-performance rendering engine for the web. To support that mission, we’re launching a **Bug Bounty Program** to reward contributors who help make PixiJS more stable and robust.

1. **Bounty Tag Assignment**
   The PixiJS team will identify eligible issues and apply the **`bounty`** label along with a specific **dollar amount**.

Only issues labeled with the `bounty` tag and a dollar amount are eligible for this program.

You can find all current bounty-tagged issues [here](https://github.com/pixijs/pixijs/issues?q=is%3Aissue%20state%3Aopen%20label%3A%F0%9F%92%B0Bounty).

2. **Submission Requirements**
   To claim a bounty, you must:

- Submit a **Pull Request (PR)** that fixes the issue.
   - Link the issue in your PR description.
   - Include a clear **example or test case** demonstrating that the bug is resolved.
   - Follow our standard [contribution guidelines](https://github.com/pixijs/pixijs/blob/dev/.github/CONTRIBUTING.md).

3. **Approval Process**

- The PixiJS team will review your PR.
   - If your fix is accepted and merged into the main branch, your bounty is approved.

4. **Requesting Payment**
   Once your PR is merged:

- You can submit a payout request via our [Open Collective](https://opencollective.com/pixijs) page.
   - Include a link to the merged PR and the bounty issue in your request.
   - Payments will be processed through Open Collective.

## Terms & Conditions

- Only issues **pre-approved** with a `bounty` tag and dollar amount are eligible.
- Bounties are awarded **at the PixiJS team's discretion**. We reserve the right to reject fixes that are incomplete, introduce regressions, or do not meet project standards.
- You may submit fixes for issues without a bounty tag, but they will not be eligible for financial rewards.
- Multiple contributors can submit PRs for the same bounty, but only the PR that gets merged is eligible for payment.
- The bounty amount is fixed and non-negotiable.
- Abuse, spamming, or low-quality submissions may result in exclusion from the program.

## Sponsoring Bounties

If you are a developer or company working on a project and would like to sponsor a one-off bounty, please contact **Matt Karl** [@bigtimebuddy](https://github.com/bigtimebuddy) at **[hello@mattkarl.com](mailto:hello@mattkarl.com)** to arrange the details.

Sponsors can make one-time donations directly to our [Open Collective](https://opencollective.com/pixijs) to fund the bounty.

We kindly request that sponsors add an additional **10%** to the bounty amount to cover Open Collective's processing fees.

## **Finding Bounty Issues**

You can easily find [eligible bounty issues](https://github.com/pixijs/pixijs/issues?q=is%3Aissue%20state%3Aopen%20label%3A%F0%9F%92%B0Bounty) on our GitHub repository.

This allows you to focus your contributions on tasks that have a financial reward.

## Why We're Doing This

We believe in the power of open source and community collaboration. Our bug bounty program is designed to:

- Encourage contributors to tackle important, impactful issues.
- Recognize the hard work involved in debugging and fixing complex problems.
- Acknowledge that the PixiJS core team is small and often focused on other critical tasks, your contributions help get issues resolved faster.
- Make PixiJS even better for everyone.

Feel free to ask questions on our [GitHub Discussions](https://github.com/pixijs/pixijs/discussions) or join our [community Discord](https://discord.gg/QrnxmQUPGV).

---

## Events / Interaction

**URL:** llms-txt#events-/-interaction

**Contents:**
- Event Modes
- Event Types
  - Pointer Events (Recommended for general use)
  - Mouse Events (Used for mouse-specific input)
  - Touch Events
  - Global Events
- How Hit Testing Works
  - Custom Hit Area
- Listening to Events
  - Using `on()` (from EventEmitter)

PixiJS is primarily a rendering library, but it provides a flexible and performant event system designed for both mouse and touch input. This system replaces the legacy `InteractionManager` from previous versions with a unified, DOM-like federated event model.

To use the event system, set the `eventMode` of a `Container` (or its subclasses like `Sprite`) and subscribe to event listeners.

The `eventMode` property controls how an object interacts with the event system:

| Mode      | Description                                                                                                              |
| --------- | ------------------------------------------------------------------------------------------------------------------------ |
| `none`    | Ignores all interaction events, including children. Optimized for non-interactive elements.                              |
| `passive` | _(default)_ Ignores self-hit testing and does not emit events, but interactive children still receive events.            |
| `auto`    | Participates in hit testing only if a parent is interactive. Does not emit events.                                       |
| `static`  | Emits events and is hit tested. Suitable for non-moving interactive elements like buttons.                               |
| `dynamic` | Same as `static`, but also receives synthetic events when the pointer is idle. Suitable for animating or moving targets. |

PixiJS supports a rich set of DOM-like event types across mouse, touch, and pointer input. Below is a categorized list.

### Pointer Events (Recommended for general use)

| Event Type          | Description                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| `pointerdown`       | Fired when a pointer (mouse, pen, or touch) is pressed on a display object.        |
| `pointerup`         | Fired when the pointer is released over the display object.                        |
| `pointerupoutside`  | Fired when the pointer is released outside the object that received `pointerdown`. |
| `pointermove`       | Fired when the pointer moves over the display object.                              |
| `pointerover`       | Fired when the pointer enters the boundary of the display object.                  |
| `pointerout`        | Fired when the pointer leaves the boundary of the display object.                  |
| `pointerenter`      | Fired when the pointer enters the display object (does not bubble).                |
| `pointerleave`      | Fired when the pointer leaves the display object (does not bubble).                |
| `pointercancel`     | Fired when the pointer interaction is canceled (e.g. touch lost).                  |
| `pointertap`        | Fired when a pointer performs a quick tap.                                         |
| `globalpointermove` | Fired on every pointer move, regardless of whether any display object is hit.      |

### Mouse Events (Used for mouse-specific input)

| Event Type        | Description                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------- |
| `mousedown`       | Fired when a mouse button is pressed on a display object.                                   |
| `mouseup`         | Fired when a mouse button is released over the object.                                      |
| `mouseupoutside`  | Fired when a mouse button is released outside the object that received `mousedown`.         |
| `mousemove`       | Fired when the mouse moves over the display object.                                         |
| `mouseover`       | Fired when the mouse enters the display object.                                             |
| `mouseout`        | Fired when the mouse leaves the display object.                                             |
| `mouseenter`      | Fired when the mouse enters the object, does not bubble.                                    |
| `mouseleave`      | Fired when the mouse leaves the object, does not bubble.                                    |
| `click`           | Fired when a mouse click (press and release) occurs on the object.                          |
| `rightdown`       | Fired when the right mouse button is pressed on the display object.                         |
| `rightup`         | Fired when the right mouse button is released over the object.                              |
| `rightupoutside`  | Fired when the right mouse button is released outside the object that received `rightdown`. |
| `rightclick`      | Fired when a right mouse click (press and release) occurs on the object.                    |
| `globalmousemove` | Fired on every mouse move, regardless of display object hit.                                |
| `wheel`           | Fired when the mouse wheel is scrolled while over the display object.                       |

| Event Type        | Description                                                                           |
| ----------------- | ------------------------------------------------------------------------------------- |
| `touchstart`      | Fired when a new touch point is placed on a display object.                           |
| `touchend`        | Fired when a touch point is lifted from the display object.                           |
| `touchendoutside` | Fired when a touch point ends outside the object that received `touchstart`.          |
| `touchmove`       | Fired when a touch point moves across the display object.                             |
| `touchcancel`     | Fired when a touch interaction is canceled (e.g. device gesture).                     |
| `tap`             | Fired when a touch point taps the display object.                                     |
| `globaltouchmove` | Fired on every touch move, regardless of whether a display object is under the touch. |

In previous versions of PixiJS, events such as `pointermove`, `mousemove`, and `touchmove` were fired when any move event was captured by the canvas, even if the pointer was not over a display object. This behavior changed in v8 and now these events are fired only when the pointer is over a display object.

To maintain the old behavior, you can use the `globalpointermove`, `globalmousemove`, and `globaltouchmove` events. These events are fired on every pointer/touch move, regardless of whether any display object is hit.

## How Hit Testing Works

When an input event occurs (mouse move, click, etc.), PixiJS walks the display tree to find the top-most interactive element under the pointer:

- If `interactiveChildren` is `false` on a `Container`, its children will be skipped.
- If a `hitArea` is set, it overrides bounds-based hit testing.
- If `eventMode` is `'none'`, the element and its children are skipped.

Once the top-most interactive element is found, the event is dispatched to it. If the event bubbles, it will propagate up the display tree.
If the event is not handled, it will continue to bubble up to parent containers until it reaches the root.

Custom hit areas can be defined using the `hitArea` property. This property can be set on any scene object, including `Sprite`, `Container`, and `Graphics`.

Using a custom hit area allows you to define a specific area for interaction, which can be different from the object's bounding box. It also can improve performance by reducing the number of objects that need to be checked for interaction.

## Listening to Events

PixiJS supports both `on()`/`off()` and `addEventListener()`/`removeEventListener()` and event callbacks (`onclick: ()=> {}`) for adding and removing event listeners. The `on()` method is recommended for most use cases as it provides a more consistent API across different event types used throughout PixiJS.

### Using `on()` (from EventEmitter)

### Using DOM-style Events

## Checking for Interactivity

You can check if a `Sprite` or `Container` is interactive by using the `isInteractive()` method. This method returns `true` if the object is interactive and can receive events.

PixiJS allows you to set a custom cursor for interactive objects using the `cursor` property. This property accepts a string representing the CSS cursor type.

### Default Custom Cursors

You can also set default values to be used for all interactive objects.

- [Overview](https://pixijs.download/release/docs/events.html)
- [EventSystem](https://pixijs.download/release/docs/events.EventSystem.html)
- [Cursor](https://pixijs.download/release/docs/events.html#Cursor)
- [EventMode](https://pixijs.download/release/docs/events.html#EventMode)
- [Container](https://pixijs.download/release/docs/scene.Container.html)
- [FederatedEvent](https://pixijs.download/release/docs/events.FederatedEvent.html)
- [FederatedMouseEvent](https://pixijs.download/release/docs/events.FederatedMouseEvent.html)
- [FederatedWheelEvent](https://pixijs.download/release/docs/events.FederatedWheelEvent.html)
- [FederatedPointerEvent](https://pixijs.download/release/docs/events.FederatedPointerEvent.html)

## Filters / Blend Modes

**Examples:**

Example 1 (ts):
```ts
const sprite = new Sprite(texture);
sprite.eventMode = 'static';
sprite.on('pointerdown', () => {
  console.log('Sprite clicked!');
});
```

Example 2 (ts):
```ts
const sprite = new Sprite(texture);
sprite.eventMode = 'static';
sprite.on('globalpointermove', (event) => {
  console.log('Pointer moved globally!', event);
});
```

Example 3 (ts):
```ts
import { Rectangle, Sprite } from 'pixi.js';

const sprite = new Sprite(texture);
sprite.hitArea = new Rectangle(0, 0, 100, 100);
sprite.eventMode = 'static';
```

Example 4 (ts):
```ts
const eventFn = (e) => console.log('clicked');
sprite.on('pointerdown', eventFn);
sprite.once('pointerdown', eventFn);
sprite.off('pointerdown', eventFn);
```

---

## Mixing PixiJS and Three.js

**URL:** llms-txt#mixing-pixijs-and-three.js

**Contents:**
  - What You’ll Learn
  - Setting Up
  - Rendering Loop
  - Example: Combining 3D and 2D Elements
  - Gotchas
  - Conclusion
- v8 Migration Guide

In many projects, developers aim to harness the strengths of both 3D and 2D graphics. Combining the advanced 3D rendering capabilities of Three.js with the speed and versatility of PixiJS for 2D can result in a powerful, seamless experience. Together, these technologies create opportunities for dynamic and visually compelling applications. Lets see how to do this.

:::info NOTE
This guide assumes PixiJS will be used as the top layer to deliver UI over a 3D scene rendered by Three.js. However, developers can render either in any order, as many times as needed. This flexibility allows for creative and dynamic applications.
:::

### What You’ll Learn

- Setting up PixiJS and Three.js to share a single WebGL context.
- Using `resetState` to manage renderer states.
- Avoiding common pitfalls when working with multiple renderers.

#### Step 1: Initialize Three.js Renderer and Scene

Three.js will handle the 3D rendering the creation of the dom element and context.

:::info NOTE
We used the dom element and context created by the three.js renderer to pass to the pixijs renderer.
This was the simplest way to ensure that the two renderers were using the same WebGL context. You could have done it the other way round
if you wanted to.
:::

#### Step 2: Initialize PixiJS Renderer and Stage

PixiJS will handle the 2D overlay.

To ensure smooth transitions between the renderers, reset their states before each render:

### Example: Combining 3D and 2D Elements

Here’s the complete example integrating PixiJS and Three.js:

- **Enable Stencil Buffers:**

- When creating the Three.js renderer, ensure `stencil` is set to `true`. This allows PixiJS masks to work correctly.

- **Keep Dimensions in Sync:**

- Ensure both renderers use the same `width` and `height` to avoid visual mismatches—so be careful when resizing one, you need to resize the other!

- **Pass the WebGL Context:**

- Pass the WebGL context from Three.js to PixiJS during initialization using `pixiRenderer.init({ context: threeRenderer.getContext() });`.

- **Disable Clear Before Render:**

- Set `clearBeforeRender: false` when initializing the PixiJS renderer. This prevents PixiJS from clearing the Three.js content that was rendered before it.
  - Alternatively you can set `clear: false` in the `pixiRenderer.render()` call. eg `pixiRenderer.render({ container: stage, clear: false });`.

- **Manage Render Order:**

- In this example, Three.js is rendered first, followed by PixiJS for UI layers. However, this order is flexible. You can render pixi -> three -> pixi is you want, just make sure you reset the state when switching renderer.

- **Separate Resources:**

- Remember that resources like textures are not shared between PixiJS and Three.js. A PixiJS texture cannot be directly used as a Three.js texture and vice versa.

Mixing PixiJS and Three.js can be a powerful way to create dynamic and visually appealing applications. By carefully managing the rendering loop and states, you can achieve seamless transitions between 3D and 2D layers. This approach allows you to leverage the strengths of both technologies, creating applications that are both visually stunning and performant.

This technique can be used with other renderers too - as long as they have their own way of resetting their state (which the main ones do) you can mix them. Popular 3D engines like Babylon.js and PlayCanvas both support state management through their respective APIs, making them compatible with this mixing approach. This gives you the flexibility to choose the 3D engine that best suits your needs while still leveraging PixiJS's powerful 2D capabilities.

## v8 Migration Guide

**Examples:**

Example 1 (javascript):
```javascript
const WIDTH = window.innerWidth;
const HEIGHT = window.innerHeight;

const threeRenderer = new THREE.WebGLRenderer({
  antialias: true,
  stencil: true, // so masks work in pixijs
});

threeRenderer.setSize(WIDTH, HEIGHT);
threeRenderer.setClearColor(0xdddddd, 1);
document.body.appendChild(threeRenderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, WIDTH / HEIGHT);
camera.position.z = 50;
scene.add(camera);

const boxGeometry = new THREE.BoxGeometry(10, 10, 10);
const basicMaterial = new THREE.MeshBasicMaterial({ color: 0x0095dd });
const cube = new THREE.Mesh(boxGeometry, basicMaterial);
cube.rotation.set(0.4, 0.2, 0);
scene.add(cube);
```

Example 2 (javascript):
```javascript
const pixiRenderer = new PIXI.WebGLRenderer();

await pixiRenderer.init({
  context: threeRenderer.getContext(),
  width: WIDTH,
  height: HEIGHT,
  clearBeforeRender: false, // Prevent PixiJS from clearing the Three.js render
});

const stage = new PIXI.Container();
const amazingUI = new PIXI.Graphics()
  .roundRect(20, 80, 100, 100, 5)
  .roundRect(220, 80, 100, 100, 5)
  .fill(0xffff00);

stage.addChild(amazingUI);
```

Example 3 (javascript):
```javascript
function render() {
  // Render the Three.js scene
  threeRenderer.resetState();
  threeRenderer.render(scene, camera);

  // Render the PixiJS stage
  pixiRenderer.resetState();
  pixiRenderer.render({ container: stage });

  requestAnimationFrame(render);
}

requestAnimationFrame(render);
```

Example 4 (ts):
```ts
// dependencies: { "three": "latest", "pixi.js": "latest" }
// description: A basic integration of PixiJS and Three.js sharing the same WebGL context
// Import required classes from PixiJS and Three.js
import { Container, Graphics, Text, WebGLRenderer } from 'pixi.js';
import * as THREE from 'three';

// Self-executing async function to set up the demo
(async () => {
  // Initialize window dimensions
  let WIDTH = window.innerWidth;
  let HEIGHT = window.innerHeight;

  // === THREE.JS SETUP ===
  // Create Three.js WebGL renderer with antialiasing and stencil buffer
  const threeRenderer = new THREE.WebGLRenderer({
    antialias: true,
    stencil: true,
  });

  // Configure Three.js renderer size and background color
  threeRenderer.setSize(WIDTH, HEIGHT);
  threeRenderer.setClearColor(0xdddddd, 1); // Light gray background
  document.body.appendChild(threeRenderer.domElement);

  // Create Three.js scene
  const scene = new THREE.Scene();

  // Set up perspective camera with 70° FOV
  const threeCamera = new THREE.PerspectiveCamera(70, WIDTH / HEIGHT);

  threeCamera.position.z = 50; // Move camera back to see the scene
  scene.add(threeCamera);

  // Create a simple cube mesh
  const boxGeometry = new THREE.BoxGeometry(30, 30, 30);
  const basicMaterial = new THREE.MeshBasicMaterial({ color: 0x0095dd }); // Blue color
  const cube = new THREE.Mesh(boxGeometry, basicMaterial);

  scene.add(cube);

  // === PIXI.JS SETUP ===
  // Create PixiJS renderer that shares the WebGL context with Three.js
  const pixiRenderer = new WebGLRenderer();

  // Initialize PixiJS renderer with shared context
  await pixiRenderer.init({
    context: threeRenderer.getContext(),
    width: WIDTH,
    height: HEIGHT,
    clearBeforeRender: false, // Don't clear the canvas as Three.js will handle that
  });

  // Create PixiJS scene graph
  const stage = new Container();

  // Create a yellow rounded rectangle UI element
  const uiLayer = new Graphics().roundRect(20, 80, 300, 300, 20).fill(0xffff00);

  // Add text overlay
  const text = new Text({
    text: 'Pixi and Three.js',
    style: { fontFamily: 'Arial', fontSize: 24, fill: 'black' },
  });

  uiLayer.addChild(text);
  stage.addChild(uiLayer);

  // Animation loop
  function loop() {
    // Rotate cube continuously
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    // Animate UI layer position using sine wave
    uiLayer.y = ((Math.sin(Date.now() * 0.001) + 1) * 0.5 * WIDTH) / 2;

    // Render Three.js scene
    threeRenderer.resetState();
    threeRenderer.render(scene, threeCamera);

    // Render PixiJS scene
    pixiRenderer.resetState();
    pixiRenderer.render({ container: stage });

    // Continue animation loop
    requestAnimationFrame(loop);
  }

  // Start animation loop
  requestAnimationFrame(loop);

  // Handle window resizing
  window.addEventListener('resize', () => {
    WIDTH = window.innerWidth;
    HEIGHT = window.innerHeight;

    // Update Three.js renderer
    threeRenderer.setSize(WIDTH, HEIGHT);
    // Update Three.js camera aspect ratio so it renders correctly
    threeCamera.aspect = WIDTH / HEIGHT;
    threeCamera.updateProjectionMatrix();

    // Update PixiJS renderer
    pixiRenderer.resize(WIDTH, HEIGHT);
  });
})();
```

---

## Shared vs Custom Ticker

**URL:** llms-txt#shared-vs-custom-ticker

**Contents:**
  - Behavior Differences
- Lifecycle Control
- API Reference
- Background Loader

The plugin supports two modes:

| Option                | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| `sharedTicker: true`  | Uses `Ticker.shared`, shared across all applications.        |
| `sharedTicker: false` | Creates a private ticker instance scoped to the application. |

### Behavior Differences

- If using a **shared ticker**, other code may also be registering updates, so the order of execution can vary.
- If using a **custom ticker**, you get complete control over timing and update order.

You can manually stop and start the ticker:

- Pausing the game or animation
- Performance throttling on inactive tabs
- Managing visibility events

- [TickerPlugin](https://pixijs.download/release/docs/app.TickerPlugin.html)
- [Ticker](https://pixijs.download/release/docs/ticker.Ticker.html)

**Examples:**

Example 1 (ts):
```ts
app.stop(); // Stop automatic rendering
app.start(); // Resume
```

---

## Background Loader

**URL:** llms-txt#background-loader

**Contents:**
- Loading Bundles
- Loading Individual Assets
- API Reference
- Compressed Textures

PixiJS provides a **background loader** that allows you to load assets in the background while your application is running. This is useful for loading large assets or multiple assets without blocking the main thread. This can help improve the responsiveness of your application, reduce the initial loading time, and potentially void showing multiple loading screens to the user.

The most effective way to use the background loader is to load bundles of assets. Bundles are groups of assets that are related to each other in some way, such as all the assets for a specific screen or level in your game. By loading bundles in the background, you can ensure that the assets are available when you need them without blocking the main thread.

## Loading Individual Assets

You can also load individual assets in the background using the `Assets.backgroundLoad()` method. This is useful for loading assets that are not part of a bundle or for loading additional assets after the initial load.

- [Assets](https://pixijs.download/release/docs/assets.Assets.html)
- [BackgroundLoader](https://pixijs.download/release/docs/assets.BackgroundLoader.html)

## Compressed Textures

**Examples:**

Example 1 (ts):
```ts
const manifest = {
  bundles: [
    {
      name: 'home-screen',
      assets: [
        { alias: 'flowerTop', src: 'https://pixijs.com/assets/flowerTop.png' },
      ],
    },
    {
      name: 'game-screen',
      assets: [
        { alias: 'eggHead', src: 'https://pixijs.com/assets/eggHead.png' },
      ],
    },
  ],
};

// Initialize the asset system with a manifest
await Assets.init({ manifest });

// Start loading both bundles in the background
Assets.backgroundLoadBundle(['game-screen']);

// Load only the first screen assets immediately
const resources = await Assets.loadBundle('home-screen');
```

Example 2 (ts):
```ts
// Load an individual asset in the background
Assets.backgroundLoad({
  alias: 'flowerTop',
  src: 'https://pixijs.com/assets/flowerTop.png',
});

// Load another asset in the background
Assets.backgroundLoad({
  alias: 'eggHead',
  src: 'https://pixijs.com/assets/eggHead.png',
});
```

---

## Graphics Pixel Line

**URL:** llms-txt#graphics-pixel-line

**Contents:**
- How to use `pixelLine`?
- Why Use `pixelLine`?
  - 1. **Retro or Pixel Art Games**
  - 2. **UI and HUD Elements**
  - 3. **Debugging and Prototyping**
- How it works
- Caveats and Gotchas
  - 1. **Its 1px thick, thats it!**
  - 2. **Hardware may render differently**
  - 4. **Scaling Behavior**

The `pixelLine` property is a neat feature of the PixiJS Graphics API that allows you to create lines that remain 1 pixel thick, regardless of scaling or zoom level. As part of the Graphics API, it gives developers all the power PixiJS provides for building and stroking shapes. This feature is especially useful for achieving crisp, pixel-perfect visuals, particularly in retro-style or grid-based games, technical drawing, or UI rendering.

In this guide, we'll dive into how this property works, its use cases, and the caveats you should be aware of when using it.

## How to use `pixelLine`?

Here’s a simple example:

In this example, no matter how you transform or zoom the `Graphics` object, the red line will always appear 1 pixel thick on the screen.

## Why Use `pixelLine`?

Pixel-perfect lines can be incredibly useful in a variety of scenarios. Here are some common use cases:

### 1. **Retro or Pixel Art Games**

- Pixel art games rely heavily on maintaining sharp, precise visuals. The `pixelLine` property ensures that lines do not blur or scale inconsistently with other pixel elements.
- Example: Drawing pixel-perfect grids for tile-based maps.

### 2. **UI and HUD Elements**

- For UI elements such as borders, separators, or underlines, a consistent 1-pixel thickness provides a professional, clean look.
- Example: Drawing a separator line in a menu or a progress bar border.

### 3. **Debugging and Prototyping**

- Use pixel-perfect lines to debug layouts, collision boxes, or grids. Since the lines don’t scale, they offer a consistent reference point during development.
- Example: Displaying collision boundaries in a physics-based game.

This is achieved under the hood using WebGL or WebGPU's native line rendering methods when `pixelLine` is set to `true`.

Fun fact its actually faster to draw a pixel line than a regular line. This is because of two main factors:

1. **Simpler Drawing Process**: Regular lines in PixiJS (when `pixelLine` is `false`) need extra steps to be drawn. PixiJS has to figure out the thickness of the line and create a shape that looks like a line but is actually made up of triangles.

2. **Direct Line Drawing**: When using `pixelLine`, we can tell the graphics card "just draw a line from point A to point B" and it knows exactly what to do. This is much simpler and faster than creating and filling shapes.

Think of it like drawing a line on paper - `pixelLine` is like using a pen to draw a straight line, while regular lines are like having to carefully color in a thin rectangle. The pen method is naturally faster and simpler!

## Caveats and Gotchas

While the `pixelLine` property is incredibly useful, there are some limitations and things to keep in mind:

### 1. **Its 1px thick, thats it!**

- The line is always 1px thick, there is no way to change this as its using the GPU to draw the line.

### 2. **Hardware may render differently**

- Different GPUs and graphics hardware may render the line slightly differently due to variations in how they handle line rasterization. For example, some GPUs may position the line slightly differently or apply different anti-aliasing techniques. This is an inherent limitation of GPU line rendering and is beyond PixiJS's control.

### 4. **Scaling Behavior**

- While the line thickness remains constant, other properties (e.g., position or start/end points) are still affected by scaling. This can sometimes create unexpected results if combined with other scaled objects. This is a feature not a bug :)

### Example: Box with Pixel-Perfect Stroke

Here's an example of a filled box with a pixel-perfect stroke. The box itself scales and grows, but the stroke remains 1 pixel wide:

In this example, the blue box grows as it scales, but the red stroke remains at 1 pixel thickness, providing a crisp outline regardless of the scaling.

## When to Avoid Using `pixelLine`

- **You want a line that is not 1px thick:** Don't use `pixelLine`.
- **You want the line to scale:** Don't use `pixelLine`

The `pixelLine` property is a super useful to have in the PixiJS toolbox for developers looking to create sharp, pixel-perfect lines that remain consistent under transformation. By understanding its strengths and limitations, you can incorporate it into your projects for clean, professional results in both visual and functional elements.

**Examples:**

Example 1 (ts):
```ts
import { Application, Container, Graphics, Text } from 'pixi.js';

/**
 * Creates a grid pattern using Graphics lines
 * @param graphics - The Graphics object to draw on
 * @returns The Graphics object with the grid drawn
 */
function buildGrid(graphics) {
  // Draw 10 vertical lines spaced 10 pixels apart
  for (let i = 0; i < 11; i++) {
    // Move to top of each line (x = i*10, y = 0)
    graphics
      .moveTo(i * 10, 0)
      // Draw down to bottom (x = i*10, y = 100)
      .lineTo(i * 10, 100);
  }

  // Draw 10 horizontal lines spaced 10 pixels apart
  for (let i = 0; i < 11; i++) {
    // Move to start of each line (x = 0, y = i*10)
    graphics
      .moveTo(0, i * 10)
      // Draw across to end (x = 100, y = i*10)
      .lineTo(100, i * 10);
  }

  return graphics;
}

(async () => {
  // Create and initialize a new PixiJS application
  const app = new Application();

  await app.init({ antialias: true, resizeTo: window });
  document.body.appendChild(app.canvas);

  // Create two grids - one with pixel-perfect lines and one without
  const gridPixel = buildGrid(new Graphics()).stroke({
    color: 0xffffff,
    pixelLine: true,
    width: 1,
  });

  const grid = buildGrid(new Graphics()).stroke({
    color: 0xffffff,
    pixelLine: false,
  });

  // Position the grids side by side
  grid.x = -100;
  grid.y = -50;
  gridPixel.y = -50;

  // Create a container to hold both grids
  const container = new Container();

  container.addChild(grid, gridPixel);

  // Center the container on screen
  container.x = app.screen.width / 2;
  container.y = app.screen.height / 2;
  app.stage.addChild(container);

  // Animation variables
  let count = 0;

  // Add animation to scale the grids over time
  app.ticker.add(() => {
    count += 0.01;
    container.scale = 1 + (Math.sin(count) + 1) * 2;
  });

  // Add descriptive label
  const label = new Text({
    text: 'Grid Comparison: Standard Lines (Left) vs Pixel-Perfect Lines (Right)',
    style: { fill: 0xffffff },
  });

  // Position label in top-left corner
  label.position.set(20, 20);
  label.width = app.screen.width - 40;
  label.scale.y = label.scale.x;
  app.stage.addChild(label);
})();
```

Example 2 (ts):
```ts
// Create a Graphics object and draw a pixel-perfect line
let graphics = new Graphics()
  .moveTo(0, 0)
  .lineTo(100, 100)
  .stroke({ color: 0xff0000, pixelLine: true });

// Add it to the stage
app.stage.addChild(graphics);

// Even if we scale the Graphics object, the line remains 1 pixel wide
graphics.scale.set(2);
```

Example 3 (ts):
```ts
// Create a grid of vertical and horizontal lines
const grid = new Graphics();

// Draw 10 vertical lines spaced 10 pixels apart
// Draw vertical lines
for (let i = 0; i < 10; i++) {
  // Move to top of each line (x = i*10, y = 0)
  grid
    .moveTo(i * 10, 0)
    // Draw down to bottom (x = i*10, y = 100)
    .lineTo(i * 10, 100);
}

// Draw horizontal lines
for (let i = 0; i < 10; i++) {
  // Move to start of each line (x = 0, y = i*10)
  grid
    .moveTo(0, i * 10)
    // Draw across to end (x = 100, y = i*10)
    .lineTo(100, i * 10);
}

// Stroke all lines in white with pixel-perfect width
grid.stroke({ color: 0xffffff, pixelLine: true });
```

Example 4 (ts):
```ts
// Create a separator line that will always be 1 pixel thick
const separator = new Graphics()
  // Start at x=0, y=50
  .moveTo(0, 50)
  // Draw a horizontal line 200 pixels to the right
  .lineTo(200, 50)
  // Stroke in green with pixel-perfect 1px width
  .stroke({ color: 0x00ff00, pixelLine: true });
```

---

## Graphics

**URL:** llms-txt#graphics

**Contents:**
- **Available Shapes**
  - Basic Primitives
  - Advanced Primitives
  - SVG Support
- **GraphicsContext**
  - Destroying a GraphicsContext
- **Creating Holes**
- **Graphics Is About Building, Not Drawing**
- **Performance Best Practices**
- **Caveats and Gotchas**

[Graphics](https://pixijs.download/release/docs/scene.Graphics.html) is a powerful and flexible tool for rendering shapes such as rectangles, circles, stars, and custom polygons. It can also be used to create complex shapes by combining multiple primitives, and it supports advanced features like gradients, textures, and masks.

## **Available Shapes**

PixiJS v8 supports a variety of shape primitives:

- Line
- Rectangle
- Rounded Rectangle
- Circle
- Ellipse
- Arc
- Bezier / Quadratic Curves

### Advanced Primitives

- Chamfer Rect
- Fillet Rect
- Regular Polygon
- Star
- Rounded Polygon
- Rounded Shape

You can also load SVG path data, although complex hole geometries may render inaccurately due to Pixi's performance-optimized triangulation system.

## **GraphicsContext**

The `GraphicsContext` class is the core of PixiJS's new graphics model. It holds all the drawing commands and styles, allowing the same shape data to be reused by multiple `Graphics` instances:

This pattern is particularly effective when rendering repeated or animated shapes, such as frame-based SVG swaps:

:::info
If you don't explicitly pass a `GraphicsContext` when creating a `Graphics` object, then internally, it will have its own context, accessible via `myGraphics.context`.
:::

### Destroying a GraphicsContext

When you destroy a `GraphicsContext`, all `Graphics` instances that share it will also be destroyed. This is a crucial point to remember, as it can lead to unexpected behavior if you're not careful.

## **Creating Holes**

Use `.cut()` to remove a shape from the previous one:

Ensure the hole is fully enclosed within the shape to avoid triangulation errors.

## **Graphics Is About Building, Not Drawing**

Despite the terminology of functions like `.rect()` or `.circle()`, `Graphics` does not immediately draw anything. Instead, each method builds up a list of geometry primitives stored inside a `GraphicsContext`. These are then rendered when the object is drawn to the screen or used in another context, such as a mask.

You can think of `Graphics` as a blueprint builder: it defines what to draw, but not when to draw it. This is why `Graphics` objects can be reused, cloned, masked, and transformed without incurring extra computation until they're actually rendered.

## **Performance Best Practices**

- **Do not clear and rebuild graphics every frame**. If your content is dynamic, prefer swapping prebuilt `GraphicsContext` objects instead of recreating them.
- **Use `Graphics.destroy()`** to clean up when done. Shared contexts are not auto-destroyed.
- **Use many simple `Graphics` objects** over one complex one to maintain GPU batching.
- **Avoid transparent overlap** unless you understand blend modes; overlapping semi-transparent primitives will interact per primitive, not post-composition.

## **Caveats and Gotchas**

- **Memory Leaks**: Call `.destroy()` when no longer needed.
- **SVG and Holes**: Not all SVG hole paths triangulate correctly.
- **Changing Geometry**: Use `.clear()` sparingly. Prefer swapping contexts.
- **Transparency and Blend Modes**: These apply per primitive. Use `RenderTexture` if you want to flatten effects.

- [Graphics](https://pixijs.download/release/docs/scene.Graphics.html)
- [GraphicsContext](https://pixijs.download/release/docs/scene.GraphicsContext.html)
- [FillStyle](https://pixijs.download/release/docs/scene.FillStyle.html)
- [StrokeStyle](https://pixijs.download/release/docs/scene.StrokeStyle.html)

**Examples:**

Example 1 (ts):
```ts
import { Graphics } from 'pixi.js';

const graphics = new Graphics().rect(50, 50, 100, 100).fill(0xff0000);
```

Example 2 (ts):
```ts
const graphics = new Graphics()
  .rect(50, 50, 100, 100)
  .fill(0xff0000)
  .circle(200, 200, 50)
  .stroke(0x00ff00)
  .lineStyle(5)
  .moveTo(300, 300)
  .lineTo(400, 400);
```

Example 3 (ts):
```ts
let shape = new Graphics().svg(`
  
    
  
`);
```

Example 4 (ts):
```ts
const context = new GraphicsContext().circle(100, 100, 50).fill('red');

const shapeA = new Graphics(context);
const shapeB = new Graphics(context); // Shares the same geometry
```

---
