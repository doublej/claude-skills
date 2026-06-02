# eframe — the app framework

eframe (`egui` framework) runs the same egui code on native (Win/Mac/Linux/Android) and web/WASM. It owns the window, input, and renderer; you implement the `App` trait.

## The `App` trait (egui 0.34.x)

```rust
pub trait App {
    // REQUIRED — called every frame you need to repaint. You get a Ui directly.
    fn ui(&mut self, ui: &mut egui::Ui, frame: &mut eframe::Frame);

    // provided, override-able:
    fn logic(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame) { /* default drives ui() */ }
    #[deprecated = "Use Self::ui instead"]
    fn update(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame) {}
    fn save(&mut self, storage: &mut dyn eframe::Storage) {}
    fn on_exit(&mut self, gl: Option<&eframe::glow::Context>) {}
    fn auto_save_interval(&self) -> std::time::Duration { /* 30s */ }
    fn clear_color(&self, visuals: &egui::Visuals) -> [f32; 4] { /* window bg */ }
    fn persist_egui_memory(&self) -> bool { true }
    fn raw_input_hook(&mut self, ctx: &egui::Context, raw_input: &mut egui::RawInput) {}
}
```

**Version note (≤0.33):** the per-frame method was `fn update(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame)` and you'd open a panel with `egui::CentralPanel::default().show(ctx, |ui| ...)`. On 0.34+, prefer `ui(&mut self, ui, ...)` with `.show_inside(ui, ...)`. Match whatever version `Cargo.toml` pins. If you need a `&Context` inside the new `ui()` method, it's `ui.ctx()`.

## Launching (native)

```rust
fn main() -> eframe::Result {
    env_logger::init();
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([900.0, 600.0])
            .with_min_inner_size([400.0, 300.0])
            .with_title("My App")
            .with_icon(/* egui::IconData */ Default::default()),
        ..Default::default()
    };
    eframe::run_native("my_app", options, Box::new(|cc| {
        // cc: &CreationContext — set up here (fonts, visuals, loaders, restore state)
        setup_custom_fonts(&cc.egui_ctx);
        Ok(Box::new(MyApp::new(cc)))
    }))
}
```

`CreationContext` (`cc`) fields you use most: `cc.egui_ctx` (the `egui::Context`), `cc.storage` (`Option<&dyn Storage>` — read persisted state on startup), `cc.gl` / wgpu render state (for custom GPU painting callbacks).

`NativeOptions` notables: `viewport` (see `ViewportBuilder` below), `vsync`, `multisampling`, `depth_buffer`, `renderer` (`Wgpu` | `Glow`), `persist_window`, `centered`.

`ViewportBuilder` chain: `.with_inner_size([w,h])`, `.with_min_inner_size`, `.with_resizable(bool)`, `.with_decorations(bool)`, `.with_transparent(bool)`, `.with_always_on_top()`, `.with_maximized`, `.with_fullscreen`, `.with_title`, `.with_icon`, `.with_app_id` (Linux/Wayland + persistence key).

## Persistence

1. Enable the feature: `eframe = { version = "0.34", features = ["persistence"] }`.
2. Derive `serde` on your app state and gate with the `serde` feature.
3. Restore in the creator, save in `save()`:

```rust
impl MyApp {
    fn new(cc: &eframe::CreationContext<'_>) -> Self {
        if let Some(storage) = cc.storage {
            return eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default();
        }
        Self::default()
    }
}
impl eframe::App for MyApp {
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        eframe::set_value(storage, eframe::APP_KEY, self);
    }
    fn ui(&mut self, ui: &mut egui::Ui, _f: &mut eframe::Frame) { /* ... */ }
}
```

egui memory (window positions, collapsed state) persists automatically when `persist_egui_memory()` is true. `auto_save_interval()` controls cadence; `save()` also runs on exit.

## Web / WASM deploy

Same `App`, different entry point. On 0.34.x `WebRunner::start` takes a **`web_sys::HtmlCanvasElement`** (older templates passed a canvas-id `&str` — that's outdated).

`Cargo.toml`:
```toml
[lib]
crate-type = ["cdylib", "rlib"]
[dependencies]
eframe = "0.34"
wasm-bindgen-futures = "0.4"
web-sys = { version = "0.3", features = ["HtmlCanvasElement"] }
log = "0.4"
```

```rust
#[cfg(target_arch = "wasm32")]
fn main() {
    use eframe::wasm_bindgen::JsCast as _;
    eframe::WebLogger::init(log::LevelFilter::Debug).ok();
    let web_options = eframe::WebOptions::default();

    wasm_bindgen_futures::spawn_local(async {
        let document = web_sys::window().unwrap().document().unwrap();
        let canvas = document
            .get_element_by_id("the_canvas_id").unwrap()
            .dyn_into::<web_sys::HtmlCanvasElement>().unwrap();

        eframe::WebRunner::new()
            .start(canvas, web_options, Box::new(|cc| Ok(Box::new(MyApp::new(cc)))))
            .await
            .expect("failed to start eframe");
    });
}
```

`index.html` needs `<canvas id="the_canvas_id"></canvas>`. Build & serve with **Trunk** (`trunk serve` / `trunk build --release`) which runs `wasm-bindgen`. Start from `https://github.com/emilk/eframe_template` (note: bump its deps to 0.34 and migrate `update`→`ui` + the canvas-element signature). Web uses the WebGPU/WebGL backend automatically; eframe 0.34 added a WebGL fallback for the wgpu backend.

## Backends: wgpu vs glow

- **wgpu** (default `eframe = "0.34"` ships it): modern, WebGPU + Vulkan/Metal/DX, best for custom GPU paint callbacks (`egui_wgpu::CallbackFn`). 0.34 hardened `Surface` lifecycle (fixed random hangs).
- **glow** (`features = ["glow"]`): OpenGL/WebGL, lighter deps, broad old-GPU support; custom paint via `egui_glow::CallbackFn`. `App::on_exit` hands you the `glow::Context` for cleanup.

Pick wgpu unless you specifically need GL interop or minimal deps.

## Multi-viewport (multiple OS windows)

```rust
ctx.show_viewport_immediate(
    egui::ViewportId::from_hash_of("settings"),
    egui::ViewportBuilder::default().with_title("Settings").with_inner_size([300.0, 200.0]),
    |ctx, _class| {
        egui::CentralPanel::default().show(ctx, |ui| ui.label("hi"));
        if ctx.input(|i| i.viewport().close_requested()) { /* set your flag */ }
    },
);
```

`show_viewport_immediate` renders inline (needs a backend that supports viewports — eframe native does); `show_viewport_deferred` takes an owning closure for cross-thread cases. Not supported on web (single canvas).
