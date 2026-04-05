# OpenXR Session Lifecycle Details

## State Machine (Complete)

```
                    xrCreateSession
                          |
                          v
                      +------+
                      | IDLE |
                      +------+
                          |
                          v
                      +-------+      xrBeginSession
                      | READY | ─────────────────────┐
                      +-------+                      |
                          ^                          v
                          |                  +--------------+
                          |                  | SYNCHRONIZED |
                          |                  +--------------+
                          |                          |
                          |                          v
                          |                   +---------+
                          |                   | VISIBLE |
                          |                   +---------+
                          |                          |
                          |                          v
                          |                   +---------+
                          |                   | FOCUSED |
                          |                   +---------+
                          |                          |
                      +----------+                   |
                      | STOPPING | <─────────────────┘
                      +----------+   (from any running state)
                          |
                   xrEndSession
                          |
              ┌───────────┴───────────┐
              v                       v
          +--------+             +---------+
          | EXITING|             |  IDLE   |
          +--------+             +---------+
              |                  (re-enter loop)
              v
         App exits
```

Additionally, `LOSS_PENDING` can occur from any state -- the session/instance is being lost.

## State Transitions & Required Actions

| From State | To State | App Must |
|-----------|----------|----------|
| UNKNOWN | IDLE | Wait for event |
| IDLE | READY | Call `xrBeginSession` |
| READY | SYNCHRONIZED | Start frame loop, submit empty frames |
| SYNCHRONIZED | VISIBLE | Render content (no input) |
| VISIBLE | FOCUSED | Full rendering + input active |
| FOCUSED | VISIBLE | Stop reading input, keep rendering |
| VISIBLE | SYNCHRONIZED | Keep submitting frames (empty OK) |
| SYNCHRONIZED | STOPPING | N/A (runtime-driven) |
| any | STOPPING | Call `xrEndSession`, stop frame loop |
| STOPPING | IDLE | Optionally recreate session or exit |
| STOPPING | EXITING | Clean up, destroy session |
| any | LOSS_PENDING | Destroy session, possibly re-init instance |

## Event Polling Pattern

```c
XrEventDataBuffer event = {XR_TYPE_EVENT_DATA_BUFFER};
while (xrPollEvent(instance, &event) == XR_SUCCESS) {
    switch (((XrEventDataBaseHeader*)&event)->type) {
    case XR_TYPE_EVENT_DATA_SESSION_STATE_CHANGED: {
        XrEventDataSessionStateChanged* stateEvent =
            (XrEventDataSessionStateChanged*)&event;
        currentState = stateEvent->state;
        handleSessionState(stateEvent->state);
        break;
    }
    case XR_TYPE_EVENT_DATA_INSTANCE_LOSS_PENDING:
        // Must destroy instance within event's lossTime
        shouldQuit = true;
        break;
    case XR_TYPE_EVENT_DATA_REFERENCE_SPACE_CHANGE_PENDING: {
        XrEventDataReferenceSpaceChangePending* spaceEvent =
            (XrEventDataReferenceSpaceChangePending*)&event;
        // Recreate reference space to get new origin
        recreateReferenceSpace(spaceEvent->referenceSpaceType);
        break;
    }
    case XR_TYPE_EVENT_DATA_INTERACTION_PROFILE_CHANGED:
        // Re-query current interaction profile
        updateInteractionProfile();
        break;
    case XR_TYPE_EVENT_DATA_EVENTS_LOST: {
        XrEventDataEventsLost* lostEvent = (XrEventDataEventsLost*)&event;
        log("Lost %d events", lostEvent->lostEventCount);
        break;
    }
    }
    // Reset for next poll
    event = (XrEventDataBuffer){XR_TYPE_EVENT_DATA_BUFFER};
}
```

**Critical:** Reset `event.type` before each `xrPollEvent` call. The runtime overwrites the buffer but the type field must be `XR_TYPE_EVENT_DATA_BUFFER`.

## Error Recovery

### Session Loss

```c
case XR_SESSION_STATE_LOSS_PENDING:
    // Clean up current session
    xrDestroySession(session);
    // May try to create a new session
    // If instance loss is also pending, destroy instance too
    break;
```

### Instance Loss

```c
case XR_TYPE_EVENT_DATA_INSTANCE_LOSS_PENDING:
    // Must destroy everything within lossTime
    xrDestroySession(session);
    xrDestroyInstance(instance);
    // May attempt xrCreateInstance again
    break;
```

### Runtime Errors During Frame Submission

```c
XrResult result = xrEndFrame(session, &endInfo);
if (result == XR_ERROR_TIME_INVALID) {
    // Display time was invalid -- use predicted time from xrWaitFrame
    // Fall back to submitting with the frameState.predictedDisplayTime
}
if (result == XR_ERROR_LAYER_INVALID) {
    // Layer configuration wrong -- submit empty frame to recover
    endInfo.layerCount = 0;
    xrEndFrame(session, &endInfo);
}
```

ALVR handles this by falling back to the original `predictedDisplayTime` from `xrWaitFrame` when a custom display time fails:

```rust
if let Err(e) = xr_frame_stream.end(custom_time, blend_mode, layers) {
    error!("End frame failed: {e}");
    // Fall back to predicted time with empty layers
    xr_frame_stream.end(frame_state.predicted_display_time, blend_mode, &[]).unwrap();
}
```

## Multi-Session Patterns

### Lobby + Stream (ALVR Pattern)

ALVR maintains two rendering contexts that share a session:

```
Session created
    |
    v
Lobby active (simple environment, HUD messages)
    |
    ├── StreamingStarted event -> Switch to Stream rendering
    |       |
    |       └── StreamingStopped event -> Switch back to Lobby
    |
    └── Frame loop selects active renderer per frame
```

Both use the same session, swapchains are per-mode. The interaction context is shared via `Arc<RwLock<InteractionContext>>`.

### Session Restart

When a session ends (EXITING/LOSS_PENDING), you may want to restart:

```rust
'session_loop: loop {
    let system = instance.system(FormFactor::HEAD_MOUNTED_DISPLAY)?;
    let (session, waiter, stream) = create_session(&instance, system, &graphics);

    'render_loop: loop {
        // ... poll events, render frames ...
        match event.state() {
            EXITING | LOSS_PENDING => break 'render_loop,
            _ => {}
        }
    }
    // Session destroyed, loop back to create new one
}
```

## Platform-Specific Session Notes

### Android

- Must call `xr_entry.initialize_android_loader()` before anything else
- Session runs on a dedicated rendering thread (not the Android main thread)
- Handle `AndroidApp` lifecycle events separately from OpenXR events
- `libopenxr_loader.so` may have vendor-specific variants (Quest, Pico, YVR)

### Desktop (SteamVR/Monado/WMR)

- Loader discovers runtime via `XR_RUNTIME_JSON` env var or registry
- Multiple runtimes may be installed; only one active at a time
- API layers configured via `XR_API_LAYER_PATH` or registry

### Quest-Specific

- `LOCAL_FLOOR_EXT` not available on Quest 1 -- use `STAGE` as fallback
- Foveation via `XR_FB_foveation` + `XR_FB_foveation_configuration`
- Display refresh rates: 72, 80, 90, 120 Hz (model-dependent)
- Android permissions required: `org.khronos.openxr.permission.OPENXR`

## Timing Diagram

```
        xrWaitFrame         xrBeginFrame        xrEndFrame
Frame N: |----block----|--------|---GPU render---|--------->
                                                            |
Frame N+1:              |----block----|--------|---GPU------|-->
                                                               |
Display:                                    [N shown]     [N+1 shown]
```

`xrWaitFrame` blocks until the runtime signals it's time to start the next frame. This paces the application to the display refresh rate and provides the predicted display time for pose queries.

The gap between `xrEndFrame` and the actual display is where the runtime does reprojection/timewarp using the submitted poses and images.
