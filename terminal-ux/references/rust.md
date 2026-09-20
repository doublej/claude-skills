# Rust Terminal UX

## Libraries

| Crate | Use case | Add |
|-------|----------|-----|
| **ratatui** | Full-screen TUI (immediate mode) | `cargo add ratatui crossterm` |
| **indicatif** | Spinners, progress bars, multi-progress | `cargo add indicatif` |
| **clap** | CLI framework (derive or builder) | `cargo add clap --features derive` |
| **console** | Colours, styles, TTY detection | `cargo add console` |

## indicatif: Spinners & progress (CLI)

### Spinner
```rust
use indicatif::{ProgressBar, ProgressStyle};
use std::time::Duration;

let pb = ProgressBar::new_spinner();
pb.set_style(ProgressStyle::default_spinner()
    .template("{spinner:.green} {msg}")
    .unwrap());
pb.set_message("Loading...");
pb.enable_steady_tick(Duration::from_millis(80));

// do work...
pb.finish_with_message("Done!");
```

### Progress bar
```rust
use indicatif::ProgressBar;

let pb = ProgressBar::new(total);
pb.set_style(ProgressStyle::default_bar()
    .template("{bar:40.cyan/blue} {pos}/{len} {msg}")
    .unwrap());

for item in items {
    process(&item);
    pb.inc(1);
    pb.set_message(format!("Processing {}", item.name));
}
pb.finish_with_message("Complete");
```

### Multi-progress (concurrent tasks)
```rust
use indicatif::{MultiProgress, ProgressBar, ProgressStyle};

let mp = MultiProgress::new();
let style = ProgressStyle::default_bar()
    .template("{prefix:.bold} {bar:30} {pos}/{len}")
    .unwrap();

let pb1 = mp.add(ProgressBar::new(100));
pb1.set_style(style.clone());
pb1.set_prefix("Download");

let pb2 = mp.add(ProgressBar::new(50));
pb2.set_style(style);
pb2.set_prefix("Process ");

// spawn threads, each advancing its own ProgressBar
// MultiProgress handles rendering
```

### Non-TTY: use hidden or println fallback
```rust
use indicatif::ProgressBar;
use console::Term;

let pb = if Term::stderr().is_term() {
    ProgressBar::new(total)
} else {
    ProgressBar::hidden()  // no-op, no output
};
```

## Ratatui: Full-screen TUI

### Minimal app structure
```rust
use ratatui::{
    crossterm::event::{self, Event, KeyCode},
    DefaultTerminal, Frame,
};

fn main() -> color_eyre::Result<()> {
    let terminal = ratatui::init();
    let result = run(terminal);
    ratatui::restore();
    result
}

fn run(mut terminal: DefaultTerminal) -> color_eyre::Result<()> {
    loop {
        terminal.draw(|frame| ui(frame))?;
        if let Event::Key(key) = event::read()? {
            if key.code == KeyCode::Char('q') { break; }
        }
    }
    Ok(())
}

fn ui(frame: &mut Frame) {
    use ratatui::widgets::{Block, Paragraph};
    let block = Block::bordered().title("My App");
    let text = Paragraph::new("Hello, TUI!").block(block);
    frame.render_widget(text, frame.area());
}
```

### Layout
```rust
use ratatui::layout::{Layout, Constraint, Direction};

let chunks = Layout::default()
    .direction(Direction::Vertical)
    .constraints([
        Constraint::Length(3),   // header
        Constraint::Min(0),     // main
        Constraint::Length(1),  // footer
    ])
    .split(frame.area());
```

### Common widgets
- `Paragraph` - text display
- `List` - selectable list
- `Table` - tabular data
- `Gauge` - progress bar
- `Block` - borders/titles (wraps other widgets)
- `Tabs` - tab bar

### Key patterns
- Immediate mode: redraw every frame via `terminal.draw(|f| ...)`
- Separate state struct from rendering
- Use `crossterm` for event handling and raw mode
- Always restore terminal on exit (use `ratatui::restore()` or a drop guard)
- For async: use `tokio` with `crossterm::event::EventStream`
