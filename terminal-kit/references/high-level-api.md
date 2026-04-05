# Terminal-Kit High-Level API Reference

## .fullscreen( options )
- `options`: true/false/object. `{ noAlternate: true }` to skip alternate screen buffer.

## .processExit( code )
Use instead of `process.exit()` to cleanly restore terminal state.

## .grabInput( options , [safeCallback] )
- `options`: false/true/Object
  - `mouse`: 'button' | 'drag' | 'motion'
  - `focus`: boolean
- `safe` boolean: returns promise when turning off, avoiding junk echo

```js
term.grabInput({ mouse: 'button' });
term.on('key', (name, matches, data) => { /* ... */ });
term.on('mouse', (name, data) => { /* data: { x, y, ctrl, alt, shift } */ });
```

## .getCursorLocation( [callback] )
Returns promise resolving `{ x, y }`. Or callback `(error, x, y)`.

## .getColor( register ) / .setColor( register, r, g, b )
Get/set RGB values for color register (0-255).

## .getPalette() / .setPalette( palette )
Get/set 16-color palette. Built-in palettes: default, gnome, konsole, linux, solarized, vga, xterm.

## .wrapColumn( [options] ) / .wrapColumn( [x], width )
Configure word-wrapping behavior for `.wrap` modifier.
- `width`, `x`, `continue`, `offset`

```js
term.wrapColumn({ x: 10, width: 25 });
term.wrap.green('Long text here...');
```

## .table( tableCells, [options] )
- `tableCells`: array of arrays of strings
- Key options: `hasBorder`, `contentHasMarkup`, `borderChars` ('lightRounded', etc), `borderAttr`, `textAttr`, `firstRowTextAttr`, `firstColumnTextAttr`, `width`, `fit`

```js
term.table([
    ['header 1', 'header 2', 'header 3'],
    ['row 1', 'cell', 'cell'],
], { hasBorder: true, borderChars: 'lightRounded', borderAttr: { color: 'blue' }, width: 60, fit: true });
```

## .yesOrNo( [options] , [callback] )
- `yes`/`no`: key codes (string or array). `echoYes`/`echoNo`: display text.
- Returns object with `.promise` and `.abort()`.

```js
const result = await term.yesOrNo({ yes: ['y', 'ENTER'], no: ['n'] }).promise;
```

## .inputField( [options] , [callback] )
Key options:
- `echo`, `echoChar` (true for dot), `default`, `cancelable`, `style`, `hintStyle`
- `maxLength`, `minLength`, `history` (array), `cursorPosition`
- `autoComplete` (array or async function), `autoCompleteMenu` (boolean/object), `autoCompleteHint`
- `keyBindings`, `tokenHook` (for syntax highlighting), `tokenRegExp`
- `x`, `y` position

Returns EventEmitter with: `.promise`, `.abort()`, `.stop()`, `.getInput()`, `.getPosition()`, `.getCursorPosition()`, `.setCursorPosition(offset)`, `.redraw()`, `.hide()`, `.show()`, `.rebase([x],[y])`

Actions: submit, cancel, backDelete, delete, deleteAllBefore, deleteAllAfter, backward, forward, previousWord, nextWord, historyPrevious, historyNext, startOfInput, endOfInput, autoComplete

```js
const input = await term.inputField({
    history: ['prev1', 'prev2'],
    autoComplete: ['option1', 'option2'],
    autoCompleteMenu: true,
    autoCompleteHint: true
}).promise;
```

Custom async auto-completer:
```js
const autoCompleter = async (inputString) => {
    const files = await fs.promises.readdir(__dirname);
    return termkit.autoComplete(files, inputString, true);
};
```

## .fileInput( [options] , [callback] )
Variant of inputField with file path auto-completion.
- `baseDir` (default: process.cwd()) + all inputField options.

```js
const file = await term.fileInput({ baseDir: '../' }).promise;
```

## .singleLineMenu( menuItems, [options], [callback] )
- `menuItems`: array of strings
- Options: `y`, `separator` (' '), `nextPageHint`, `previousPageHint`, `style`, `selectedStyle`, `selectedIndex`, `align`, `fillIn`, `cancelable`, `exitOnUnexpectedKey`, `keyBindings`
- Response: `{ selectedIndex, selectedText, x, y, canceled, unexpectedKey }`

```js
const response = await term.singleLineMenu(['File', 'Edit', 'View', 'Help'], {
    y: 1, style: term.inverse, selectedStyle: term.dim.blue.bgGreen
}).promise;
```

## .singleColumnMenu( menuItems, [options], [callback] )
Options: `y`, `style`, `selectedStyle`, `submittedStyle`, `leftPadding`, `selectedLeftPadding`, `submittedLeftPadding`, `extraLines`, `oneLineItem`, `itemMaxWidth`, `continueOnSubmit`, `selectedIndex`, `cancelable`, `exitOnUnexpectedKey`, `keyBindings`

```js
const response = await term.singleColumnMenu(['Option A', 'Option B', 'Option C']).promise;
```

## .gridMenu( menuItems, [options], [callback] )
Options: `y`, `x`, `width`, `style`, `selectedStyle`, `leftPadding`, `selectedLeftPadding`, `rightPadding`, `selectedRightPadding`, `itemMaxWidth`, `exitOnUnexpectedKey`, `keyBindings`

```js
const items = fs.readdirSync(process.cwd());
const response = await term.gridMenu(items).promise;
```

## .spinner( [options] ) / .spinner( animation )
- `animation`: string name or custom array. Built-in: 'line', 'dotSpinner', 'unboxing-color', etc.
- Must `await` before writing text after it.

```js
const spinner = await term.spinner('unboxing-color');
term(' Loading...');
```

## .progressBar( [options] )
Options: `width`, `percent`, `eta`, `items`, `title`, `barStyle`, `barBracketStyle`, `percentStyle`, `etaStyle`, `itemStyle`, `titleStyle`, `itemSize`, `titleSize`, `barChar`, `barHeadChar`, `maxRefreshTime`, `minRefreshTime`, `inline`, `syncMode`, `x`, `y`

Controller: `.update(progress)`, `.startItem(name)`, `.itemDone(name)`, `.stop()`, `.resume()`, `.reset()`

```js
const bar = term.progressBar({ width: 80, title: 'Processing:', eta: true, percent: true });
bar.update(0.5);  // 50%
bar.update({ progress: 0.75, title: 'Almost done' });

// Item mode:
const bar2 = term.progressBar({ width: 80, title: 'Tasks:', eta: true, percent: true, items: 5 });
bar2.startItem('task1');
bar2.itemDone('task1');
```

## .bar( value, [options] )
Simple inline bar. `value`: 0-1, `options.innerSize` (default 10), `options.barStyle`.

## .slowTyping( str, [options], [callback] )
Old-fashioned typing effect.
- `style`, `flashStyle`, `delay` (150ms), `flashDelay` (100ms)

```js
await term.slowTyping('Hello world!\n', { flashStyle: term.brightWhite });
```

## .drawImage( url, [options], [callback] )
Draw PNG/JPEG/GIF in terminal. Supports filepath only by default (install `get-pixels` for URLs).
- `shrink: { width, height }` - recommended: `{ width: term.width, height: term.height * 2 }`

```js
await term.drawImage('./image.png', { shrink: { width: term.width, height: term.height * 2 } });
```
