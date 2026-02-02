# Avoiding UI Freeze in Blender

Patterns for long-running operations without freezing Blender.

**Rule of thumb:** Don't block main thread > 16ms (60fps)

## 1. Modal Operator with Timer (Recommended for <10s work)

Break operations into small chunks per frame:

```python
import bpy

class MODAL_OT_process_data(bpy.types.Operator):
    bl_idname = "wm.modal_process"
    bl_label = "Process Data"

    _timer = None
    _index = 0
    _items = list(range(1000))

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._index < len(self._items):
                # Process small batch per frame
                batch_size = 10
                for i in range(batch_size):
                    if self._index < len(self._items):
                        self.process_item(self._items[self._index])
                        self._index += 1
                return {'RUNNING_MODAL'}
            else:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                return {'FINISHED'}

        elif event.type == 'ESC':
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def process_item(self, item):
        pass  # Do work here

# Run it
bpy.ops.wm.modal_process('INVOKE_DEFAULT')
```

## 2. Frame Change Handler (For <5s animations)

Let Blender's frame loop drive work:

```python
import bpy

class ProcessState:
    def __init__(self, items):
        self.index = 0
        self.items = items

    def process_frame(self, scene):
        if self.index < len(self.items):
            self.process_item(self.items[self.index])
            self.index += 1
            print(f"Progress: {self.index}/{len(self.items)}")
        else:
            bpy.app.handlers.frame_change_post.remove(self.process_frame)

    def process_item(self, item):
        pass

# Set up
state = ProcessState(list(range(1000)))
bpy.app.handlers.frame_change_post.append(state.process_frame)

# Trigger by playing animation
bpy.ops.screen.animation_play()
```

## 3. Background Thread (For CPU-heavy, no Blender data modifications)

```python
import bpy
import threading
from queue import Queue

result_queue = Queue()

def background_compute(items):
    """Runs in background - don't modify Blender here!"""
    for item in items:
        result = expensive_calculation(item)
        result_queue.put(result)

# Start background thread
thread = threading.Thread(target=background_compute, args=(items,))
thread.daemon = True
thread.start()

# Collect results in modal operator (safe in main thread)
class MODAL_OT_collect(bpy.types.Operator):
    bl_idname = "wm.collect_results"
    bl_label = "Collect Results"
    _timer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            while not result_queue.empty():
                result = result_queue.get()
                self.apply_result(result)

            if not thread.is_alive() and result_queue.empty():
                wm = context.window_manager
                wm.event_timer_remove(self._timer)
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def apply_result(self, result):
        # Modify Blender here (safe in main thread)
        pass
```

## 4. Disable Updates During Batch Operations

```python
import bpy

# Disable viewport updates
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'SOLID'
                space.overlay.show_wireframes = False

# Batch without undo (faster)
with bpy.context.temp_override(use_undo=False):
    for i in range(1000):
        create_object(i)

# Force viewport redraw
for area in bpy.context.screen.areas:
    if area.type in ['VIEW_3D', 'PROPERTIES']:
        area.tag_redraw()
```

## Quick Selection Guide

| Time | Method | Use Case |
|------|--------|----------|
| < 100ms | Direct execution | Simple operations |
| 100ms-1s | Modal operator + timer | Batch object creation |
| 1-10s | Modal + frame handler | Complex mesh operations |
| 10s+ | Background thread + queue | Simulation, rendering prep |
