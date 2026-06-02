# Widgets, layout & styling

All calls are on a `&mut egui::Ui`. Widgets return a `Response`; layout containers take a closure `|ui| ...` and return `InnerResponse`.

## Widget catalog (bind each to your own state)

| Call | Notes |
|---|---|
| `ui.label("text")` / `ui.heading(..)` / `ui.monospace(..)` / `ui.small(..)` | text; `RichText` for styling: `ui.label(egui::RichText::new("x").strong().color(egui::Color32::RED))` |
| `ui.button("x")` / `ui.small_button` | `.clicked()`, `.secondary_clicked()`, `.middle_clicked()` |
| `ui.checkbox(&mut self.on, "Enabled")` | bool |
| `ui.radio_value(&mut self.choice, Enum::A, "A")` | one per variant |
| `ui.selectable_value(&mut self.choice, Enum::A, "A")` | toggle-button style; `selectable_label(bool, "x")` for manual |
| `ui.add(egui::Slider::new(&mut self.v, 0.0..=1.0).text("gain").logarithmic(true))` | numeric |
| `ui.add(egui::DragValue::new(&mut self.n).speed(0.1).range(0..=100))` | drag-to-edit number |
| `ui.text_edit_singleline(&mut self.s)` / `ui.text_edit_multiline(&mut self.s)` | `String`; for richer config `ui.add(egui::TextEdit::singleline(&mut self.s).hint_text("…").password(true))` |
| `ui.hyperlink("https://…")` / `ui.hyperlink_to("label", url)` | |
| `ui.image(egui::include_image!("path.png"))` / `ui.image("file://…" or URL)` | needs `egui_extras::install_image_loaders` (see ecosystem.md) |
| `ui.spinner()` / `ui.add(egui::ProgressBar::new(frac).show_percentage())` | progress |
| `egui::ComboBox::from_label("Pick").selected_text(cur).show_ui(ui, \|ui\| { ui.selectable_value(&mut self.x, A, "A"); })` | dropdown |
| `ui.color_edit_button_srgba(&mut color)` | color picker |
| `ui.separator()` / `ui.add_space(8.0)` | spacing |

`ui.add(widget)` / `ui.add_enabled(bool, widget)` / `ui.add_sized([w,h], widget)` / `ui.add_visible` are the generic escape hatches for any `Widget`.

## Response & Sense

```rust
let r = ui.button("Click");
if r.clicked()  { /* ... */ }
if r.changed()  { /* value widgets: fired when the bound value changed */ }
if r.hovered()  { r.on_hover_text("tooltip"); }
if r.double_clicked() {}
if r.dragged()  { let delta = r.drag_delta(); }
r.context_menu(|ui| { if ui.button("Delete").clicked() { /* */ } }); // right-click menu
let rect = r.rect; // where it was drawn
```

`Sense` controls what a custom/interactive area detects: `egui::Sense::click()`, `::drag()`, `::click_and_drag()`, `::hover()`. Combine `Response`s with `r1 | r2`.

## Layout containers

```rust
ui.horizontal(|ui| { ui.label("a"); ui.label("b"); });
ui.horizontal_wrapped(|ui| { /* wraps to next line */ });
ui.vertical(|ui| { /* ... */ });
ui.vertical_centered(|ui| { /* ... */ });
ui.columns(3, |cols| { cols[0].label("c0"); cols[1].label("c1"); cols[2].label("c2"); });
ui.group(|ui| { /* framed box */ });
ui.indent("id", |ui| { /* indented block */ });
ui.collapsing("Advanced", |ui| { /* CollapsingHeader */ });
egui::CollapsingHeader::new("Section").default_open(true).show(ui, |ui| { /* */ });

// Explicit layout direction/alignment:
ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
    if ui.button("OK").clicked() {}   // lays out from the right
});
```

### Grid (aligned columns)
```rust
egui::Grid::new("settings_grid").num_columns(2).striped(true).show(ui, |ui| {
    ui.label("Name");  ui.text_edit_singleline(&mut self.name);  ui.end_row();
    ui.label("Age");   ui.add(egui::DragValue::new(&mut self.age)); ui.end_row();
});
```
`end_row()` after each row is mandatory. Grid remembers column widths from the previous frame.

### ScrollArea + virtualization
```rust
egui::ScrollArea::vertical().auto_shrink([false, false]).show(ui, |ui| { /* content */ });

// Virtualize huge lists — only lays out visible rows:
let row_h = ui.text_style_height(&egui::TextStyle::Body);
egui::ScrollArea::vertical().show_rows(ui, row_h, self.items.len(), |ui, range| {
    for i in range { ui.label(&self.items[i]); }
});
```
`.stick_to_bottom(true)` for logs/chat. Use `show_rows` (or `egui_extras::TableBuilder::body(.rows)`) whenever the list can be large — full re-layout each frame is the main perf trap.

## Panels (top-level regions)

```rust
egui::TopBottomPanel::top("menu").show(ctx, |ui| { egui::menu::bar(ui, |ui| { /* … */ }); });
egui::SidePanel::left("nav").resizable(true).default_width(200.0).show(ctx, |ui| { /* … */ });
egui::TopBottomPanel::bottom("status").show(ctx, |ui| { ui.label("ready"); });
egui::CentralPanel::default().show(ctx, |ui| { /* MAIN — add LAST so it fills the remainder */ });
```
Order matters: side/top/bottom panels claim their edge first; `CentralPanel` takes what's left. Inside the new 0.34 `ui()` method use `.show_inside(ui, |ui| ...)` instead of `.show(ctx, ...)`.

## Windows
```rust
egui::Window::new("Inspector")
    .open(&mut self.show_inspector)      // adds a close button bound to your bool
    .resizable(true).default_pos([20.0, 20.0]).collapsible(true)
    .show(ctx, |ui| { /* … */ });
```

## Atoms (0.32+)
`Atom`/`AtomLayout` are the layout primitive behind buttons and labels, letting you mix text + images/icons inline with consistent spacing — e.g. `egui::Button::new((egui::Atom::from(icon_image), "Save"))`. API is newer and evolving; check docs.rs for the pinned version before relying on details.

## Styling, theme, fonts, scaling

```rust
ctx.set_visuals(egui::Visuals::dark());           // or ::light(); whole-app theme
ctx.set_theme(egui::Theme::Dark);                 // follow/set light-dark (recent versions)
ctx.set_pixels_per_point(1.25);                   // global UI scale (DPI/zoom)

// Tweak spacing/visuals globally:
ctx.style_mut(|s| {
    s.spacing.item_spacing = egui::vec2(8.0, 6.0);
    s.spacing.button_padding = egui::vec2(10.0, 4.0);
    s.visuals.widgets.inactive.rounding = 6.0.into(); // see version note below
});

// Local override for a subtree:
ui.style_mut().visuals.override_text_color = Some(egui::Color32::LIGHT_GREEN);
```

**Version note on corner radius:** older egui used `Rounding`; recent versions renamed it to `CornerRadius`. Field/type names like `widgets.inactive.rounding` vs `.corner_radius` differ across versions — check docs.rs for the pinned version. `Color32`, `Stroke`, `Vec2`, `Pos2`, `Rect` are stable.

### Custom fonts
```rust
fn setup_custom_fonts(ctx: &egui::Context) {
    let mut fonts = egui::FontDefinitions::default();
    fonts.font_data.insert("my".to_owned(),
        std::sync::Arc::new(egui::FontData::from_static(include_bytes!("../assets/Inter.ttf"))));
    fonts.families.entry(egui::FontFamily::Proportional).or_default().insert(0, "my".to_owned());
    ctx.set_fonts(fonts);
}
```
(`FontData::from_static` is wrapped in `Arc` in recent versions.) Adjust per-`TextStyle` sizes via `ctx.style_mut(|s| s.text_styles = ...)`.
