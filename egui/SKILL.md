---
name: egui
description: "Build native + web GUIs in Rust with egui (immediate-mode) and eframe. Covers the App trait (ui/update), widgets, layout/panels, state ownership, styling/Visuals, egui_extras tables/images, egui_plot, docking (tiles/dock), bevy_egui, custom painting, WASM/web deploy, and egui_kittest testing. Pinned to egui 0.34.x (Rust 1.92+). Trigger on egui, eframe, egui_extras, 'Rust GUI'/'Rust desktop app', immediate-mode GUI, CentralPanel/SidePanel/TopBottomPanel, ui.button/ui.label, ViewportBuilder, run_native, or compiling a Rust UI to web/wasm."
---

# egui

<mental_model>
egui is an **immediate-mode** GUI: you re-describe the whole UI every frame from your own state. Widgets are throwaway builders — egui stores almost nothing for you.

- **You own the state.** Your `App` struct fields are the single source of truth. Each frame you read them to draw and mutate them on interaction.
- **No retained widget tree, no callbacks.** Interaction is a return value: `if ui.button("Save").clicked() { save(); }`.
- **IDs are auto-generated** from call-site + label. Duplicate labels are fine (unlike Dear ImGui). You only manage `Id` for stateful/looped widgets (see [push_id](#) in references/custom-painting.md).
- **egui is backend-agnostic** — it lays out and emits triangles; an *integration* (eframe, bevy_egui, custom wgpu/winit) collects input and renders. Default app path is **eframe**.
</mental_model>

<version>
Pinned to **egui / eframe 0.34.x** (latest 0.34.3, 2026-05), **MSRV Rust 1.92+**. egui versions move fast and break APIs — before writing code, confirm the project's pinned version in `Cargo.toml` and check docs.rs for that exact version. Key recent shifts:
- **0.34**: required `App` method is now `ui(&mut self, ui, frame)`; `update(ctx, frame)` is **deprecated**. Font backend → `skrifa` + `vello_cpu` (hinting). `content_rect`/`viewport_rect` for safe areas.
- **0.32**: `Atom` layout primitives; popups/tooltips/menus rewritten; better SVG.
- **0.33**: `egui::Plugin` trait; `Rounding` renamed to `CornerRadius`.

**Common 0.33→0.34 renames** (old names still compile but emit deprecation warnings — except `rect_filled`, which is a hard type error):
- `SidePanel` / `TopBottomPanel` → unified `Panel`: `Panel::left(id)` / `Panel::right(id)` / `Panel::top(id)` / `Panel::bottom(id)`.
- `Panel::default_width` / `exact_width` (and the `_height` variants) → `Panel::default_size` / `exact_size`.
- `ctx.style()` → `ctx.global_style()`; `ctx.set_style()` → `ctx.set_global_style()` (and `style_mut` → `global_style_mut`) — avoids confusion with `ui.style()`.
- `Painter::rect_filled` corner-radius arg is now `CornerRadius` (`u8`-based, since 0.33's `Rounding`→`CornerRadius`), **not** `f32` — pass `CornerRadius::same(3)`, not `3.0`.

If the project is on ≤0.33, use the `update(&mut self, ctx, frame)` method instead of `ui` (see references/eframe-app.md).
</version>

<when_to_use>
- **eframe** (this skill's default): standalone desktop (Win/Mac/Linux), Android, or web/WASM app, same source. → references/eframe-app.md
- **Embed** in an existing renderer (your own wgpu/winit loop) or a **game engine** (bevy_egui). → references/ecosystem.md
- Not the right tool for: pixel-perfect designer-driven layouts, heavy retained-mode form apps, or native-look platform widgets. egui is best for tools, debug UIs, dashboards, and apps where dev speed + portability beat platform fidelity.
</when_to_use>

<quickstart>
Minimal eframe app (egui 0.34.x). `Cargo.toml`: `eframe = "0.34"`, `egui_extras = { version = "0.34", features = ["all_loaders"] }` (only if loading images), `env_logger = "0.11"`.

```rust
use eframe::egui;

fn main() -> eframe::Result {
    env_logger::init(); // RUST_LOG=debug for egui logs
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([320.0, 240.0]),
        ..Default::default()
    };
    eframe::run_native(
        "My egui App",
        options,
        Box::new(|cc| {
            egui_extras::install_image_loaders(&cc.egui_ctx); // optional: image support
            Ok(Box::<MyApp>::default())
        }),
    )
}

struct MyApp { name: String, age: u32 }
impl Default for MyApp {
    fn default() -> Self { Self { name: "Arthur".to_owned(), age: 42 } }
}

impl eframe::App for MyApp {
    // 0.34+: the per-frame method is `ui`, and you receive a `&mut Ui` directly.
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show_inside(ui, |ui| {
            ui.heading("My egui Application");
            ui.horizontal(|ui| {
                let label = ui.label("Your name: ");
                ui.text_edit_singleline(&mut self.name).labelled_by(label.id);
            });
            ui.add(egui::Slider::new(&mut self.age, 0..=120).text("age"));
            if ui.button("Increment").clicked() {
                self.age += 1;
            }
            ui.label(format!("Hello '{}', age {}", self.name, self.age));
        });
    }
}
```

Note: inside `ui()` you already hold a `Ui`, so panels use `.show_inside(ui, |ui| ...)`. When you only have a `&Context` (e.g. the deprecated `update`, or `Window`), use `.show(ctx, |ui| ...)` instead.
</quickstart>

<core_idioms>
- **Widgets read & mutate your state by `&mut`:** `ui.checkbox(&mut self.on, "Enabled")`, `ui.add(egui::Slider::new(&mut self.v, 0.0..=1.0))`, `ui.text_edit_singleline(&mut self.s)`, `ui.selectable_value(&mut self.choice, Variant::A, "A")`.
- **Interaction is a `Response`:** `let r = ui.button("x"); if r.clicked() {} if r.changed() {} if r.hovered() {} r.on_hover_text("tip")`.
- **Layout is nested closures:** `ui.horizontal(|ui| {...})`, `ui.vertical(|ui| {...})`, `ui.columns(2, |c| { c[0]...; c[1]... })`, `egui::Grid::new("g").show(ui, |ui| { ...; ui.end_row(); })`.
- **Panels & windows:** `SidePanel`, `TopBottomPanel`, `CentralPanel` (add central LAST), `egui::Window::new("t").open(&mut self.show).show(ctx, |ui| ...)`.
- **Repaint is input-driven.** For animation or background events, call `ctx.request_repaint()` (or `request_repaint_after(dur)`); egui is otherwise idle.
- Full detail + widget catalog: references/widgets-layout.md.
</core_idioms>

<pitfalls>
- **"My value resets every frame."** You didn't store it. egui doesn't keep widget values — bind every widget to a field you own.
- **Single-pass layout lag.** Size is known only *after* a frame; egui reuses last-frame sizes (Window/Grid/Table). Symptoms: first-frame jitter; a resizable panel that "snaps back" because content auto-shrinks. Pin sizes (`exact_width`, `Column::initial`) when you need stability.
- **Big scroll areas are the #1 CPU sink** — everything is laid out every frame. Virtualize: `ScrollArea::vertical().show_rows(ui, row_h, n, |ui, range| ...)` or `egui_extras::TableBuilder` with `body.rows(...)`. See references/widgets-layout.md.
- **Same `Id` collisions in loops** (e.g. a `CollapsingHeader`/`Grid` per item with identical labels) → wrap each iteration in `ui.push_id(i, |ui| {...})`.
- **Borrow-checker fights** from mutating `self` inside a `ui.xxx(|ui| ...)` closure that also borrows `self`. Collect actions into a local (e.g. `let mut clicked = None;`), apply after the closure.
- **Don't do heavy work in the frame loop.** Offload to threads/async and feed results into state + `request_repaint()`; the `ui`/`update` method must stay fast.
</pitfalls>

<debugging>
- `ctx.set_debug_on_hover(true)` — outlines widgets and shows their `Id`/size on hover.
- `egui::Window::new("🔧 Settings").show(ctx, |ui| ctx.settings_ui(ui))` and `ctx.inspection_ui(ui)` / `ctx.memory_ui(ui)` for live introspection.
- Run with `RUST_LOG=debug` (with `env_logger`) to surface egui/eframe warnings.
- The official live demo (`https://www.egui.rs/`) doubles as a searchable widget gallery — its source is `egui_demo_lib`.
</debugging>

<references>
Load on demand:
- **references/eframe-app.md** — `App` trait (all methods, `ui` vs deprecated `update`), `run_native` + `NativeOptions`/`ViewportBuilder`, **web/WASM deploy** (`WebRunner`, canvas, trunk/wasm-bindgen), persistence/`save`, multi-viewport, wgpu vs glow backends.
- **references/widgets-layout.md** — full widget catalog, `Response`/`Sense`, all layout containers, panels, `ScrollArea` + virtualization, `Grid`, `ComboBox`, `Atom`s, styling/`Visuals`/`Style`, fonts, scaling.
- **references/ecosystem.md** — `egui_extras` (`TableBuilder`, image loaders, datepicker), `egui_plot`, docking (`egui_tiles`/`egui_dock`), `bevy_egui`, embedding in a custom wgpu/winit loop, accessibility (AccessKit), testing with `egui_kittest`.
- **references/custom-painting.md** — implementing the `Widget` trait, `ui.allocate_response` + `Sense`, `epaint`/`Painter` shapes & text, animations (`ctx.animate_*`), `Id` management (`push_id`), the transient data store (`ctx.data_mut`).
</references>
