# Python Terminal UX

## Libraries

| Library | Use case | Install |
|---------|----------|---------|
| **Rich** | Spinners, progress, tables, panels, logging | `pip install rich` |
| **Textual** | Full-screen TUI (built on Rich) | `pip install textual` |
| **click** | CLI framework (args, help, groups) | `pip install click` |
| **typer** | CLI framework (type-hint based, uses Rich) | `pip install typer[all]` |

## Rich: CLI with rich status

### Spinner
```python
from rich.console import Console

console = Console(stderr=True)

with console.status("Processing...") as status:
    for item in items:
        status.update(f"Processing {item.name}...")
        process(item)
console.print("[green]Done![/green]")
```

### Multi-task progress
```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("{task.completed}/{task.total}"),
    console=Console(stderr=True),
) as progress:
    task1 = progress.add_task("Downloading", total=100)
    task2 = progress.add_task("Processing", total=None)  # indeterminate

    while not progress.finished:
        progress.advance(task1, 1)
```

### Task tree pattern
```python
from rich.tree import Tree
from rich.console import Console

tree = Tree("Deploy")
tree.add("[green]Build[/green] - done")
tree.add("[yellow]Test[/yellow] - running")
tree.add("[dim]Deploy[/dim] - pending")
Console(stderr=True).print(tree)
```

### Live display (updating panel)
```python
from rich.live import Live
from rich.table import Table

def make_table(data):
    table = Table()
    table.add_column("Task")
    table.add_column("Status")
    for name, status in data.items():
        table.add_row(name, status)
    return table

with Live(make_table(data), console=Console(stderr=True), refresh_per_second=4):
    # update data dict, Live auto-refreshes
    pass
```

## Textual: Full-screen TUI

### Minimal app
```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class MyApp(App):
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello, TUI!")
        yield Footer()

if __name__ == "__main__":
    MyApp().run()
```

### Background worker (non-blocking IO)
```python
from textual.app import App
from textual.worker import Worker

class MyApp(App):
    def on_mount(self):
        self.run_worker(self.fetch_data)

    async def fetch_data(self) -> None:
        # long-running work here
        result = await some_api_call()
        self.query_one("#output").update(str(result))
```

### Key patterns
- Use `compose()` for layout, not `__init__`
- Use `CSS` property or `.tcss` files for styling
- Use `reactive` for state that triggers UI updates
- Use `Worker` for async/background tasks (never block the event loop)

## TTY-aware output module template
```python
import sys
from rich.console import Console

_stderr = Console(stderr=True, force_terminal=None)  # auto-detect
_stdout = Console(file=sys.stdout, no_color=True, highlight=False)

def status(msg: str): _stderr.print(f"[dim]{msg}[/dim]")
def info(msg: str): _stderr.print(msg)
def data(obj): _stdout.print_json(data=obj)
def error(msg: str): _stderr.print(f"[red]error:[/red] {msg}")
```
