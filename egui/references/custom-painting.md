# Custom widgets, painting, animation, IDs & state store

## Reusable widget: implement `Widget`

A widget is just a function `self -> Response`. Implement `egui::Widget` so it works with `ui.add(...)`:

```rust
struct Toggle<'a>(&'a mut bool);

impl egui::Widget for Toggle<'_> {
    fn ui(self, ui: &mut egui::Ui) -> egui::Response {
        let desired = ui.spacing().interact_size.y * egui::vec2(2.0, 1.0);
        let (rect, mut resp) = ui.allocate_exact_size(desired, egui::Sense::click());
        if resp.clicked() { *self.0 = !*self.0; resp.mark_changed(); }

        if ui.is_rect_visible(rect) {
            let how_on = ui.ctx().animate_bool(resp.id, *self.0); // 0..1 eased
            let visuals = ui.style().interact_selectable(&resp, *self.0);
            let radius = 0.5 * rect.height();
            ui.painter().rect(rect, radius, visuals.bg_fill, visuals.bg_stroke, egui::StrokeKind::Inside);
            let cx = egui::lerp((rect.left() + radius)..=(rect.right() - radius), how_on);
            ui.painter().circle(egui::pos2(cx, rect.center().y), 0.75 * radius,
                                visuals.bg_fill, visuals.fg_stroke);
        }
        resp
    }
}
// usage: ui.add(Toggle(&mut self.enabled));
```

Pattern: **allocate space → sense input → mutate state (`mark_changed`) → paint**. For a simple helper that doesn't need `ui.add`, just write `fn my_widget(ui: &mut egui::Ui, ...) -> egui::Response`.

`ui.allocate_*` family: `allocate_exact_size(size, sense)`, `allocate_at_least(size, sense)`, `allocate_space(size)` (no sense), `allocate_response(size, sense)`. To make an already-drawn rect interactive: `let resp = ui.interact(rect, ui.id().with("tag"), egui::Sense::drag());`.

## Painting with `Painter` / `epaint`

`let p = ui.painter();` (clipped to the `Ui`) or `ui.painter_at(rect)`.

```rust
use egui::{Color32, Stroke, pos2, vec2, Rect, Align2, FontId};
p.rect_filled(rect, 6.0, Color32::from_rgb(30, 30, 40));         // (rect, corner_radius, fill)
p.rect_stroke(rect, 6.0, Stroke::new(1.0, Color32::GRAY), egui::StrokeKind::Inside);
p.circle_filled(center, 20.0, Color32::RED);
p.line_segment([a, b], Stroke::new(2.0, Color32::WHITE));
p.text(rect.center(), Align2::CENTER_CENTER, "hi", FontId::proportional(14.0), Color32::WHITE);
let galley = p.layout_no_wrap("measured".into(), FontId::monospace(12.0), Color32::WHITE);
p.galley(top_left, galley, Color32::WHITE);
```

Coordinates are points (logical px), origin top-left. `Rect::from_min_size`, `Rect::from_center_size`, `Pos2`, `Vec2` from `emath`. For polylines/shapes push `egui::Shape` variants or use `epaint::PathShape`/`CircleShape`. GPU-accelerated custom 3D goes through a backend paint callback (`egui_wgpu`/`egui_glow` `CallbackFn`), not the 2D painter.

**Version note:** signatures for `rect`/`rect_stroke`/`circle` shifted across versions — the `StrokeKind` arg and `corner_radius` vs `Rounding` naming are version-sensitive. Confirm against docs.rs for the pinned egui version.

## Animation

egui eases values between frames for you (and auto-requests repaints while animating):
```rust
let t  = ui.ctx().animate_bool(id, condition);                 // 0.0 → 1.0
let t2 = ui.ctx().animate_bool_with_time(id, condition, 0.4);  // custom duration
let v  = ui.ctx().animate_value_with_time(id, target, 0.25);   // smooth toward target
```
For continuous animation driven by your own clock, call `ctx.request_repaint()` each frame (or `request_repaint_after(dur)`), and read `ui.input(|i| i.time)` / `i.stable_dt`.

## IDs

Auto-generated from call-site + label. Manage them only when you create the same widget repeatedly or need a stable handle:
```rust
for (i, item) in self.items.iter().enumerate() {
    ui.push_id(i, |ui| {                       // disambiguate identical widgets in a loop
        egui::CollapsingHeader::new(&item.name).show(ui, |ui| { /* … */ });
    });
}
let id = egui::Id::new("my_thing").with(extra);   // build an explicit, stable Id
```
"Id clash" warnings at runtime mean two widgets share an Id — wrap one in `push_id` or give it a unique label.

## Transient & persisted state store

For widget-local state you don't want in your `App` struct (drag offsets, open/closed, scratch values), use egui's per-`Id` memory:
```rust
// transient (cleared on restart):
let mut count = ui.data_mut(|d| d.get_temp::<i32>(id).unwrap_or(0));
count += 1;
ui.data_mut(|d| d.insert_temp(id, count));

// persisted across runs (needs serde + persistence; survives save()):
ui.data_mut(|d| d.insert_persisted(id, value));
let v = ui.data_mut(|d| d.get_persisted::<T>(id));
```
Prefer your own `App` fields for real app state; use the data store only for incidental UI state tied to a widget `Id`. `ui.memory_mut(|m| ...)` exposes lower-level things (focus, open popups).
