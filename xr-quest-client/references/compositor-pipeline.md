# Compositor Pipeline

## Frame Timing Deep Dive

The Quest compositor runs on a dedicated thread, independent of the app's render thread. The frame lifecycle:

```
App Thread                          Compositor Thread
─────────                           ─────────────────
xrWaitFrame() ─── blocks ───┐
                             │      [compositor displays previous frame]
         ◄── returns ────────┘      [provides predictedDisplayTime]
xrBeginFrame()
  query poses at predictedDisplayTime
  acquire swapchain image
  wait for swapchain image
  RENDER
  release swapchain image
xrEndFrame() ──── submits ──┐
                             │      [compositor picks up frame]
                             └────► [ATW reprojection at vsync]
                                    [display scanout]
```

### Vsync Alignment

The compositor targets vsync intervals. At 90Hz, vsync occurs every 11.1ms. If the app misses the deadline:

1. **ATW kicks in**: reprojects the previous frame with updated head orientation
2. **Frame appears 1 vsync late**: user sees stale content with correct rotation
3. **Consistent misses**: perceived as judder, especially during translational movement

### predictedDisplayTime

`xrWaitFrame` returns `predictedDisplayTime` -- the exact XrTime when the frame will appear on the display. This accounts for:
- Render time estimate
- Compositor processing time
- Display scanout latency

Always use this time for `xrLocateSpace` and `xrLocateViews`. Using any other time source (system clock, previous frame time) causes incorrect pose prediction.

```cpp
XrFrameState frameState{XR_TYPE_FRAME_STATE};
xrWaitFrame(session, nullptr, &frameState);

if (!frameState.shouldRender) {
    xrBeginFrame(session, nullptr);
    xrEndFrame(session, &endInfo);  // submit empty frame
    return;
}

// Query views at the predicted display time
XrViewLocateInfo viewLocateInfo{XR_TYPE_VIEW_LOCATE_INFO};
viewLocateInfo.viewConfigurationType = XR_VIEW_CONFIGURATION_TYPE_PRIMARY_STEREO;
viewLocateInfo.displayTime = frameState.predictedDisplayTime;
viewLocateInfo.space = appSpace;

XrViewState viewState{XR_TYPE_VIEW_STATE};
uint32_t viewCount;
xrLocateViews(session, &viewLocateInfo, &viewState, 2, &viewCount, views);
```

### shouldRender Flag

`frameState.shouldRender` can be `false` when:
- The app is not focused (guardian menu, system UI overlay)
- The headset is in standby (proximity sensor)
- Session state is not `FOCUSED`

When `shouldRender` is false, still call `xrBeginFrame` + `xrEndFrame` (with 0 layers) to maintain frame pacing. Never busy-loop or skip the frame lifecycle.

## Layer Ordering

Layers are composited back-to-front in the order submitted to `xrEndFrame`. The compositor blends them according to each layer's flags.

```
Layer 0: Passthrough          (XrCompositionLayerPassthroughFB)
Layer 1: Scene projection     (XrCompositionLayerProjection)
Layer 2: UI quad overlay      (XrCompositionLayerQuad)
```

### Passthrough Layer Setup

```cpp
// 1. Create passthrough feature
XrPassthroughCreateInfoFB ptCreateInfo{XR_TYPE_PASSTHROUGH_CREATE_INFO_FB};
ptCreateInfo.flags = XR_PASSTHROUGH_IS_RUNNING_AT_CREATION_BIT_FB;
XrPassthroughFB passthrough;
pfnCreatePassthroughFB(session, &ptCreateInfo, &passthrough);

// 2. Create reconstruction layer
XrPassthroughLayerCreateInfoFB layerCreateInfo{XR_TYPE_PASSTHROUGH_LAYER_CREATE_INFO_FB};
layerCreateInfo.passthrough = passthrough;
layerCreateInfo.purpose = XR_PASSTHROUGH_LAYER_PURPOSE_RECONSTRUCTION_FB;
layerCreateInfo.flags = XR_PASSTHROUGH_IS_RUNNING_AT_CREATION_BIT_FB;
XrPassthroughLayerFB ptLayer;
pfnCreatePassthroughLayerFB(session, &layerCreateInfo, &ptLayer);

// 3. Submit as first layer (behind everything)
XrCompositionLayerPassthroughFB ptCompLayer{XR_TYPE_COMPOSITION_LAYER_PASSTHROUGH_FB};
ptCompLayer.layerHandle = ptLayer;
ptCompLayer.flags = XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT;
ptCompLayer.space = XR_NULL_HANDLE;

// 4. Set blend mode in frame end
XrFrameEndInfo endInfo{XR_TYPE_FRAME_END_INFO};
endInfo.environmentBlendMode = XR_ENVIRONMENT_BLEND_MODE_ALPHA_BLEND;
endInfo.layerCount = layerCount;
endInfo.layers = layers;  // passthrough first, then projection
```

### Depth-Based Composition

Extension: `XR_KHR_composition_layer_depth`. Submitting depth alongside color enables:
- Correct hand occlusion (system-rendered hands appear behind/in front of app objects)
- Improved ATW reprojection (positional, not just rotational)

```cpp
XrCompositionLayerDepthInfoKHR depthInfo{XR_TYPE_COMPOSITION_LAYER_DEPTH_INFO_KHR};
depthInfo.subImage.swapchain = depthSwapchain;
depthInfo.subImage.imageArrayIndex = eye;
depthInfo.subImage.imageRect = {{0, 0}, {width, height}};
depthInfo.minDepth = 0.0f;
depthInfo.maxDepth = 1.0f;
depthInfo.nearZ = nearPlane;
depthInfo.farZ = farPlane;

// Chain to projection view
projectionViews[eye].next = &depthInfo;
```

**Pitfall**: `nearZ` and `farZ` must match the projection matrix used during rendering. Mismatched values cause incorrect occlusion.

## Quad Layers

For UI panels, HUD elements, or video surfaces. Rendered by the compositor at display resolution (sharper than rendering to eye buffer).

```cpp
XrCompositionLayerQuad quadLayer{XR_TYPE_COMPOSITION_LAYER_QUAD};
quadLayer.space = appSpace;
quadLayer.eyeVisibility = XR_EYE_VISIBILITY_BOTH;
quadLayer.subImage.swapchain = uiSwapchain;
quadLayer.subImage.imageRect = {{0, 0}, {uiWidth, uiHeight}};
quadLayer.pose = uiPanelPose;           // position + orientation in space
quadLayer.size = {1.0f, 0.75f};         // meters in world space
quadLayer.layerFlags = XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT;
```

## Cylinder Layers

For curved UI panels (e.g., settings menus, media players):

```cpp
XrCompositionLayerCylinderKHR cylLayer{XR_TYPE_COMPOSITION_LAYER_CYLINDER_KHR};
cylLayer.space = appSpace;
cylLayer.subImage.swapchain = uiSwapchain;
cylLayer.pose = panelPose;
cylLayer.radius = 2.0f;                 // cylinder radius in meters
cylLayer.centralAngle = 1.0f;           // arc in radians
cylLayer.aspectRatio = 16.0f / 9.0f;
```

## Display Refresh Rate

Extension: `XR_FB_display_refresh_rate`.

```cpp
// Query available rates
uint32_t rateCount;
xrEnumerateDisplayRefreshRatesFB(session, 0, &rateCount, nullptr);
std::vector<float> rates(rateCount);
xrEnumerateDisplayRefreshRatesFB(session, rateCount, &rateCount, rates.data());

// Request 90Hz
xrRequestDisplayRefreshRateFB(session, 90.0f);

// Get current rate
float currentRate;
xrGetDisplayRefreshRateFB(session, &currentRate);
```

**Trade-offs**:
- 72Hz: easiest to hit, longest frame budget (13.9ms), best battery life
- 90Hz: good balance for most apps (11.1ms budget)
- 120Hz: smoothest but hardest to sustain (8.3ms), thermal risk

## Session Lifecycle

```
IDLE -> READY -> SYNCHRONIZED -> VISIBLE -> FOCUSED
                                    |          |
                                    v          v
                                STOPPING -> IDLE (or LOSS_PENDING -> EXITING)
```

Critical state handling:
- `READY`: call `xrBeginSession`
- `SYNCHRONIZED`: session running but not rendering (submit empty frames)
- `VISIBLE`: app visible but not focused (render, no input)
- `FOCUSED`: full rendering + input
- `STOPPING`: call `xrEndSession`, release resources
- `EXITING`: destroy session and instance

```cpp
XrEventDataBuffer event{XR_TYPE_EVENT_DATA_BUFFER};
while (xrPollEvent(instance, &event) == XR_SUCCESS) {
    if (event.type == XR_TYPE_EVENT_DATA_SESSION_STATE_CHANGED) {
        auto* stateEvent = (XrEventDataSessionStateChanged*)&event;
        switch (stateEvent->state) {
            case XR_SESSION_STATE_READY: {
                XrSessionBeginInfo beginInfo{XR_TYPE_SESSION_BEGIN_INFO};
                beginInfo.primaryViewConfigurationType =
                    XR_VIEW_CONFIGURATION_TYPE_PRIMARY_STEREO;
                xrBeginSession(session, &beginInfo);
                break;
            }
            case XR_SESSION_STATE_STOPPING:
                xrEndSession(session);
                break;
            case XR_SESSION_STATE_EXITING:
            case XR_SESSION_STATE_LOSS_PENDING:
                // Clean up and exit
                break;
        }
    }
    event = {XR_TYPE_EVENT_DATA_BUFFER};
}
```
