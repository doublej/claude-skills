# Go Terminal UX

## Libraries

| Library | Use case | Install |
|---------|----------|---------|
| **Bubble Tea** | Full-screen TUI (Elm architecture) | `go get github.com/charmbracelet/bubbletea` |
| **lipgloss** | Styling/layout for terminal | `go get github.com/charmbracelet/lipgloss` |
| **bubbles** | Pre-built components (spinner, progress, list, table) | `go get github.com/charmbracelet/bubbles` |
| **cobra** | CLI framework (commands, flags, help) | `go get github.com/spf13/cobra` |
| **huh** | Interactive forms/prompts (Charm stack) | `go get github.com/charmbracelet/huh` |

## Bubble Tea: TUI with Elm architecture

### Model-Update-View pattern
```go
package main

import (
    "fmt"
    tea "github.com/charmbracelet/bubbletea"
)

type model struct {
    choices  []string
    cursor   int
    selected map[int]struct{}
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        case "up", "k":
            if m.cursor > 0 { m.cursor-- }
        case "down", "j":
            if m.cursor < len(m.choices)-1 { m.cursor++ }
        case "enter", " ":
            if _, ok := m.selected[m.cursor]; ok {
                delete(m.selected, m.cursor)
            } else {
                m.selected[m.cursor] = struct{}{}
            }
        }
    }
    return m, nil
}

func (m model) View() string {
    s := "Pick items:\n\n"
    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i { cursor = ">" }
        checked := " "
        if _, ok := m.selected[i]; ok { checked = "x" }
        s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
    }
    s += "\nq to quit\n"
    return s
}

func main() {
    m := model{choices: []string{"Build", "Test", "Deploy"}, selected: make(map[int]struct{})}
    tea.NewProgram(m).Run()
}
```

### Spinner component
```go
import "github.com/charmbracelet/bubbles/spinner"

type model struct {
    spinner spinner.Model
    done    bool
}

func (m model) Init() tea.Cmd {
    return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    m.spinner, cmd = m.spinner.Update(msg)
    return m, cmd
}

func (m model) View() string {
    if m.done { return "Done!\n" }
    return m.spinner.View() + " Loading...\n"
}
```

### Progress bar
```go
import "github.com/charmbracelet/bubbles/progress"

type model struct {
    progress progress.Model
    percent  float64
}

func (m model) View() string {
    return m.progress.ViewAs(m.percent)
}
```

## lipgloss: Styling

```go
import "github.com/charmbracelet/lipgloss"

var (
    titleStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("212")).
        PaddingLeft(1)

    successStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("42"))

    errorStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)
)

fmt.Println(titleStyle.Render("My App"))
fmt.Println(successStyle.Render("✓ Done"))
```

## Key patterns
- Bubble Tea uses Elm architecture: `Init`, `Update`, `View`
- `Cmd` for side effects (timers, IO); never do IO in `View`
- Compose models: embed sub-models (spinner, progress) in parent
- Use `tea.WithAltScreen()` for full-screen, `tea.WithOutput(os.Stderr)` for non-fullscreen
- `huh` forms integrate with Bubble Tea via `huh.NewForm().RunWithContext()`
