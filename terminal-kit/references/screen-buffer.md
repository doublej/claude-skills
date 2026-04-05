# Terminal-Kit ScreenBuffer Reference

ScreenBuffer is a buffer for a rectangular area. Each cell has: character, 8-bit fg/bg colors, style flags, blending mask.

## Two kinds of ScreenBuffers
1. Writing directly to terminal
2. Writing to another ScreenBuffer (for compositing)

Optimized drawing: with `delta: true`, only changed cells are redrawn.

## Constructor

```js
const { ScreenBuffer } = require('terminal-kit');

const screen = new ScreenBuffer({
    width: 80,
    height: 24,
    dst: term,     // Terminal or another ScreenBuffer
    x: 1, y: 1,   // position in dst
    blending: false,
    wrap: false,
    noFill: false
});
```

## Static Methods
- `ScreenBuffer.createFromString(options, str)` — create from string with attrs
- `ScreenBuffer.loadImage(url, [options], callback)` — load image as ScreenBufferHD
- `ScreenBuffer.attr2object(flags)` / `ScreenBuffer.object2attr(obj)` — convert between formats
- `ScreenBuffer.loadSync(filepath)` — load saved buffer

## Properties
- `.dst` — destination Terminal or ScreenBuffer
- `.x`, `.y` — position in dst
- `.blending` — default blending state

## Methods

### .fill( [options] )
- `attr`: attribute object or bit flags
- `char`: fill character (default: space)
- `region`: Rect for partial fill

### .clear()
Fill with defaults (space, default colors).

### .put( options, text )
- `x`, `y`: position
- `markup`: boolean or 'ansi'
- `attr`: attributes
- `wrap`: boolean
- `newLine`: boolean (handle \r\n)
- `direction`: 'right' | 'left' | 'up' | 'down' | 'none'
- `clip`: `{ x, y, width, height }` clipping area

```js
screen.put({ x: 0, y: 0, attr: { color: 'red', bold: true } }, 'Hello');
screen.put({ x: 0, y: 1, markup: true }, '^gGreen text^:');
```

### .get( [options] )
Returns `{ char, attr }` at cursor or `{ x, y }`.

### .resize( fromRect )
Resize with `{ width, height, x, y }` or `{ xmin, xmax, ymin, ymax }`.

### .draw( [options] )
Draw to destination. Options:
- `dst`, `x`, `y` — override defaults
- `delta: true` — only redraw changed cells (performance!)
- `blending: true` — enable transparency compositing
- `wrap`: 'x' | 'y' | true | false
- `tile: true` — tile the source

### .drawCursor( [options] )
Move dst cursor to match buffer cursor position.

### .moveTo( x, y )
Move buffer's internal cursor.

### .vScroll( lineOffset, [attr], [ymin], [ymax], [scrollTerminal] )
Vertical scroll content. With `scrollTerminal: true`, also scrolls terminal.

### .saveSync( filepath ) / ScreenBuffer.loadSync( filepath )
Persist/restore buffers.

## Attribute Object
```js
{
    color: 'red',        // or 0-255 integer
    bgColor: 'blue',
    defaultColor: true,  // use terminal default
    bold: true,
    dim: false,
    italic: false,
    underline: true,
    blink: false,
    inverse: false,
    hidden: false,
    strike: false,
    // Transparency (for compositing)
    transparency: false,      // all transparencies
    fgTransparency: false,
    bgTransparency: false,
    styleTransparency: false,
    charTransparency: false
}
```

## Common Pattern: Full-Screen App

```js
const term = require('terminal-kit').terminal;
const { ScreenBuffer } = require('terminal-kit');

const screen = new ScreenBuffer({ dst: term });
const widget = new ScreenBuffer({ dst: screen, width: 20, height: 5, x: 5, y: 3 });

widget.fill({ attr: { color: 'white', bgColor: 'blue' } });
widget.put({ x: 1, y: 1, attr: { color: 'brightWhite', bold: true } }, 'Widget');

widget.draw();    // draw widget to screen buffer
screen.draw({ delta: true });  // draw screen to terminal (optimized)
```
