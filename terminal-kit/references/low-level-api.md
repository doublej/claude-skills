# Terminal-Kit Low-Level API Reference

## Properties
- `.width` / `.height`: terminal dimensions (auto-updated on resize)

## Chainable Style System
All styles are chainable and accept strings with printf-style formatting:
```js
term.bold.underline.red('styled text');
term.red("Name: %s, Age: %d\n", 'Jack', 32);
term.moveTo.cyan(1, 1, "Positioned and styled");
```

Boolean toggle: `term.red(true)` starts red, `term.red(false)` stops.
String shorthand: `term.red('text')` turns on, outputs, turns off.

## Foreground Colors
`.defaultColor()`, `.black()`, `.red()`, `.green()`, `.yellow()`, `.blue()`, `.magenta()`, `.cyan()`, `.white()`
`.brightBlack()` / `.gray()` / `.grey()`, `.brightRed()`, `.brightGreen()`, `.brightYellow()`, `.brightBlue()`, `.brightMagenta()`, `.brightCyan()`, `.brightWhite()`
`.color(register)` (0-15 or name), `.color256(register)` (0-255)
`.colorRgb(r,g,b)`, `.colorRgbHex('#ef1234')`, `.colorGrayscale(l)` (0-255)

## Background Colors
Same as foreground with `bg` prefix: `.bgRed()`, `.bgColor256(register)`, `.bgColorRgb(r,g,b)`, `.bgColorRgbHex('#ef1234')`, etc.

## Styles
`.styleReset()`, `.bold()`, `.dim()`, `.italic()`, `.underline()`, `.blink()`, `.inverse()`, `.hidden()`, `.strike()`

## Cursor Movement
`.saveCursor()` / `.restoreCursor()`
`.up(n)`, `.down(n)`, `.right(n)`, `.left(n)`
`.nextLine(n)`, `.previousLine(n)`, `.column(x)`
`.moveTo(x, y)` (1,1 = upper-left), `.move(x, y)` (relative)
`.hideCursor()` / `.hideCursor(false)`
`.scrollUp(n)`, `.scrollDown(n)`
`.scrollingRegion(top, bottom)`, `.resetScrollingRegion()`

## Screen Editing
`.clear()`, `.eraseDisplay()`, `.eraseDisplayBelow()`, `.eraseDisplayAbove()`
`.eraseLine()`, `.eraseLineAfter()`, `.eraseLineBefore()`
`.eraseArea(x, y, [width], [height])`
`.insertLine(n)`, `.deleteLine(n)`, `.insert(n)`, `.delete(n)`, `.erase(n)`
`.backDelete()`, `.alternateScreenBuffer()`

## Modifiers
- `.error()`: write to STDERR — `term.error.red('Error: %E', myError)`
- `.str()`: return string instead of outputting — `const s = term.str.blue('BLUE')`
- `.noFormat(str)`: disable printf formatting and markup
- `.markupOnly(str)`: disable printf but keep ^ markup
- `.wrap(str)`: enable word-wrapping (configure with `.wrapColumn()`)
- `.bindArgs(...)`: replacement for `.bind()` on chainable functions

## Operating System
`.windowTitle(str)`, `.iconName(str)`, `.cwd(uri)`, `.notify(title, text)` (gnome-terminal)

## Misc
`.reset()`, `.bell()`
`.setCursorColor(register)`, `.setCursorColorRgb(r,g,b)`, `.resetCursorColorRgb()`
`.setDefaultColorRgb(r,g,b)`, `.resetDefaultColorRgb()`
`.setDefaultBgColorRgb(r,g,b)`, `.resetDefaultBgColorRgb()`

## Style Markup (caret `^` syntax)
Colors: `^r`red `^g`green `^b`blue `^y`yellow `^m`magenta `^c`cyan `^w`white `^k`black
Bright: `^R` `^G` `^B` `^Y` `^M` `^C` `^W` `^K`(gray)
Styles: `^+`bold `^-`dim `^_`underline `^/`italic `^!`inverse
Reset: `^:` or `^ ` (with space)
Background: `^#` then color char, e.g. `^#r` = red background
Escape caret: `^^`
Complex: `^[red]`, `^[fg:red]`, `^[bg:blue]`, `^[#aa5577]`

```js
term("^rRed text^ normal ^+^_bold underline^:\n");
term("^[bg:blue]Blue background^:\n");
```

## Events (after .grabInput())

### 'key' ( name, matches, data )
- `name`: char or special key (ENTER, ESCAPE, UP, DOWN, LEFT, RIGHT, etc.)
- `data`: `{ isCharacter, codepoint, code }`
- Special keys: ESCAPE, ENTER, BACKSPACE, TAB, SHIFT_TAB, arrows, INSERT, DELETE, HOME, END, PAGE_UP, PAGE_DOWN, F1-F12, CTRL_A-Z, ALT_A-Z, etc.

### 'mouse' ( name, data )
- `name`: MOUSE_LEFT_BUTTON_PRESSED, MOUSE_LEFT_BUTTON_RELEASED, MOUSE_RIGHT_BUTTON_PRESSED, MOUSE_WHEEL_UP, MOUSE_WHEEL_DOWN, MOUSE_MOTION, MOUSE_DRAG, etc.
- `data`: `{ x, y, ctrl, alt, shift }` (+ `left, right, xFrom, yFrom` for MOUSE_DRAG)

### 'resize' ( width, height )
### 'terminal' ( name, data )
- CURSOR_LOCATION, FOCUS_IN, FOCUS_OUT

## Global API (termkit module)
```js
const termkit = require('terminal-kit');
const term = termkit.terminal;
```
- `termkit.terminal`: default terminal instance
- `termkit.realTerminal`: bypass pipes, access real terminal
- `termkit.createTerminal(options)`: custom terminal instance
- `termkit.autoComplete(array, startString, returnAlternatives, prefix, postfix)`: auto-complete helper
- `termkit.stripEscapeSequences(str)`: remove escape sequences
- `termkit.stringWidth(str)`: terminal-aware string width
- `termkit.truncateString(str, maxWidth)`: terminal-aware truncation
