# Ecosystem: extras, plot, docking, engines, testing

All add-on crates version-lockstep with egui (use the **same minor**, e.g. all `0.34`).

## egui_extras — tables, images, dates

`egui_extras = { version = "0.34", features = ["all_loaders"] }` (loaders pull in `image`/`resvg` for PNG/JPEG/SVG; trim features in prod).

### Tables (`TableBuilder`)
```rust
use egui_extras::{Column, TableBuilder};

TableBuilder::new(ui)
    .striped(true)
    .resizable(true)
    .cell_layout(egui::Layout::left_to_right(egui::Align::Center))
    .column(Column::auto())                 // size to content
    .column(Column::initial(120.0).range(60.0..=300.0).clip(true))
    .column(Column::remainder())            // takes leftover width
    .header(20.0, |mut header| {
        header.col(|ui| { ui.strong("Name"); });
        header.col(|ui| { ui.strong("Size"); });
        header.col(|ui| { ui.strong("Path"); });
    })
    .body(|mut body| {
        // Fixed-height virtualized rows — preferred for large data:
        body.rows(18.0, self.files.len(), |mut row| {
            let f = &self.files[row.index()];
            row.col(|ui| { ui.label(&f.name); });
            row.col(|ui| { ui.label(f.size.to_string()); });
            row.col(|ui| { ui.label(&f.path); });
        });
        // Or per-row when heights vary: body.row(h, |mut row| { row.col(..) });
    });
```
`Column` variants: `auto()`, `initial(w)`, `exact(w)`, `remainder()`; modifiers `.at_least`/`.at_most`/`.range`/`.clip`/`.resizable`. Use `body.rows(..)` (not a manual loop) for big tables — it virtualizes.

### Images
```rust
egui_extras::install_image_loaders(&cc.egui_ctx); // once, in the creator
ui.image(egui::include_image!("../assets/logo.png")); // bytes baked in
ui.image("https://example.com/pic.png");              // http loader
ui.add(egui::Image::new("file://./icon.svg").fit_to_exact_size(egui::vec2(32.0, 32.0)));
```

### DatePicker
`ui.add(egui_extras::DatePickerButton::new(&mut self.date));` (needs the `datepicker` feature + `chrono`).

## egui_plot — 2D plots

`egui_plot = "0.34"`.
```rust
use egui_plot::{Line, Plot, PlotPoints};
let pts: PlotPoints = (0..1000).map(|i| { let x = i as f64 * 0.01; [x, x.sin()] }).collect();
Plot::new("sine").view_aspect(2.0).legend(egui_plot::Legend::default())
    .show(ui, |plot_ui| { plot_ui.line(Line::new("sin", pts)); });
```
Also `Points`, `Bar`/`BarChart`, `BoxPlot`, `HLine`/`VLine`, `Polygon`, `Text`. Plot handles pan/zoom and auto-bounds.

## Docking / tiling

- **egui_tiles** — flexible tiling with drag-and-drop, splits, tabs. You implement `tiles::Behavior<Pane>` (defines `tab_title_for_pane`, `pane_ui`) and drive a `tiles::Tree<Pane>` via `tree.ui(&mut behavior, ui)`.
- **egui_dock** — VSCode/IDE-style docking. Hold a `DockState<Tab>`, implement `TabViewer` (`title`, `ui`), render with `DockArea::new(&mut dock_state).show(ctx, &mut viewer)`.

Pick `egui_dock` for IDE tab/dock UX, `egui_tiles` for free-form resizable tiling.

## Game engines / embedding

### Bevy (`bevy_egui`)
```rust
app.add_plugins(bevy_egui::EguiPlugin { enable_multipass_for_primary_context: true });
fn ui_system(mut contexts: bevy_egui::EguiContexts) {
    egui::Window::new("Debug").show(contexts.ctx_mut(), |ui| { ui.label("hello from bevy"); });
}
// add ui_system to Update. Recent bevy_egui attaches EguiContext to cameras — ensure a camera exists.
```
For entity/resource inspectors use `bevy-inspector-egui`. (bevy_egui's API tracks Bevy releases closely — verify against the Bevy version in `Cargo.toml`.)

### Custom wgpu/winit loop
Use `egui-winit` (input/window) + `egui-wgpu` (render) directly when you own the event loop:
1. `let mut state = egui_winit::State::new(ctx.clone(), viewport_id, &window, None, None, None);`
2. Per window event: `let _ = state.on_window_event(&window, &event);`
3. Per frame: `let raw = state.take_egui_input(&window); let out = ctx.run(raw, |ctx| build_ui(ctx)); state.handle_platform_output(&window, out.platform_output);`
4. Tessellate + render: `let prims = ctx.tessellate(out.shapes, out.pixels_per_point);` then feed `prims` + `out.textures_delta` to `egui_wgpu::Renderer` (`update_texture`/`update_buffers`/`render`).

`three-d`, `miniquad`, SDL2, and others have community integrations — see the egui wiki "3rd party integrations".

## Accessibility (AccessKit)

egui exposes a UI tree to screen readers via **AccessKit**, behind the `accesskit` feature (off by default; eframe enables it on supported platforms). Set semantic info with `Response::on_hover_text`, proper labels, and `ui.label(..).labelled_by(widget.id)` to associate labels with inputs.

## Testing (`egui_kittest`)

`egui_kittest` drives a headless egui app via the AccessKit tree (kittest = Testing-Library-style queries) and supports screenshot regression tests.
```rust
use egui_kittest::Harness;
let mut h = Harness::new_ui(|ui| { if ui.button("Increment").clicked() { /* */ } });
h.get_by_label("Increment").click();
h.run();                          // step a frame
// h.snapshot("increment");       // image regression (feature-gated, e.g. "wgpu"/"snapshot")
```
Query by `get_by_label`/`get_by_role`, simulate `click`/`type_text`/key events, then `run()` to advance frames and assert on resulting state.
