---
name: rust-systems
description: "Systems programming for real-time media/VR: FFI, lock-free, unsafe, NDK, cargo"
---

# Rust Systems Programming

## Before Writing Code

1. **Detect project setup**:
   - Edition: check `Cargo.toml` (`edition = "2021"` or `"2024"`)
   - Workspace: single crate or `[workspace]` with members?
   - Target: native, Android NDK, WASM, embedded?
   - Existing unsafe patterns: `grep -rn "unsafe" src/`

2. **Identify hot path vs cold path**:
   - Hot: frame loops, audio callbacks, packet handlers — no allocations, no locks, no panics
   - Cold: startup, config loading, UI — normal Rust idioms fine

3. **Check existing error strategy**:
   - `anyhow`/`eyre` for applications
   - `thiserror` for libraries
   - Raw `Result` types in hot paths

## Core Rules

### Unsafe Discipline

Every `unsafe` block MUST have a `// SAFETY:` comment explaining the invariant:

```rust
// SAFETY: `ptr` is non-null, aligned, and points to initialized `Frame`.
// Lifetime bounded by the scope of `process_frame` — caller guarantees
// the buffer outlives this reference.
let frame = unsafe { &*ptr };
```

**Audit checklist for unsafe code:**
- No aliasing `&mut` references (Rust's #1 UB source)
- Raw pointers validated before dereference (null, alignment, provenance)
- FFI types have correct layout (`#[repr(C)]`)
- No `mem::transmute` unless layout is identical and documented
- `Send`/`Sync` impls justified (the type is truly thread-safe)

### Hot Path Contract

Code on frame-deadline paths MUST NOT:

| Banned | Why | Alternative |
|--------|-----|-------------|
| `Box::new`, `Vec::push` (growing) | Heap allocation | Pre-allocate, arena, `ArrayVec` |
| `Mutex::lock` | Blocks on contention | Atomics, lock-free queues |
| `panic!`, `unwrap()`, `expect()` | Aborts pipeline | `.unwrap_or()`, match, `if let` |
| `println!`, `log::info!` | I/O syscall | Ring buffer logger, atomic counter |
| `String::format!` | Allocates | Pre-formatted, `write!` to buffer |
| `HashMap` lookup | Hashing cost | `FxHashMap`, array lookup, perfect hash |
| `thread::sleep` | Blocks thread | Spin-wait or yield for RT |

### Error Handling by Path

```rust
// Cold path — use anyhow/eyre, readable errors
fn load_config(path: &Path) -> anyhow::Result<Config> {
    let data = std::fs::read_to_string(path)
        .context("failed to read config")?;
    toml::from_str(&data).context("invalid config")
}

// Hot path — lightweight enum, no allocations
#[derive(Debug, Clone, Copy)]
enum FrameError {
    Dropped,
    DecodeFailed,
    BufferFull,
}

fn process_frame(frame: &Frame) -> Result<(), FrameError> {
    if frame.is_empty() { return Err(FrameError::Dropped); }
    // ...
    Ok(())
}
```

### Channel Architecture

Use bounded channels for backpressure. Unbounded = OOM under load.

| Crate | When |
|-------|------|
| `crossbeam-channel` | Multi-producer, multi-consumer, `select!` macro |
| `flume` | Lighter than crossbeam, async + sync, good default |
| `tokio::sync::mpsc` | Already in tokio runtime |
| `ringbuf` | SPSC lock-free ring buffer (audio/video frames) |

```rust
use crossbeam_channel::{bounded, select, Sender, Receiver};

// Bounded channel — drops frames under pressure instead of OOM
let (tx, rx): (Sender<Frame>, Receiver<Frame>) = bounded(4);

// Producer: try_send to avoid blocking
match tx.try_send(frame) {
    Ok(()) => {}
    Err(TrySendError::Full(_)) => stats.dropped += 1, // graceful degradation
    Err(TrySendError::Disconnected(_)) => return,
}

// Consumer: select across multiple channels
select! {
    recv(video_rx) -> frame => handle_video(frame?),
    recv(audio_rx) -> chunk => handle_audio(chunk?),
    recv(control_rx) -> cmd => handle_control(cmd?),
}
```

### Async vs Threads

| Use | For |
|-----|-----|
| **Raw threads** | Frame loops, audio callbacks, anything with a deadline |
| **tokio** | Network I/O, HTTP, WebSocket, file I/O |
| **rayon** | CPU-parallel batch processing (not real-time) |

**Never use async for frame-deadline work.** Tokio's executor is cooperative — a slow `.await` stalls the entire task. Frame loops need deterministic timing.

```rust
// WRONG: async for frame processing
async fn render_loop() {
    loop {
        process_frame().await; // executor may not poll in time
        tokio::time::sleep(Duration::from_millis(11)).await; // drift
    }
}

// RIGHT: dedicated thread with spin/yield
std::thread::Builder::new()
    .name("render".into())
    .spawn(move || {
        loop {
            let deadline = Instant::now() + FRAME_BUDGET;
            process_frame(&mut state);
            spin_until(deadline); // busy-wait for sub-ms precision
        }
    })?;
```

## FFI Patterns

### bindgen Setup

```toml
# Cargo.toml
[build-dependencies]
bindgen = "0.71"
cc = "1"  # if compiling C source

[dependencies]
libc = "0.2"
```

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=wrapper.h");
    println!("cargo:rustc-link-lib=mylib");

    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .allowlist_function("mylib_.*")
        .allowlist_type("MyLib.*")
        .generate()
        .expect("bindgen failed");

    let out = std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap());
    bindings.write_to_file(out.join("bindings.rs")).unwrap();
}
```

### Safe Wrapper Pattern

```rust
// Raw FFI (generated or manual)
mod ffi {
    include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
}

// Safe wrapper
pub struct Decoder {
    ptr: *mut ffi::decoder_t,
}

// SAFETY: decoder_t is internally synchronized (mutex-protected state).
// All methods take &self or &mut self, preventing concurrent mutation.
unsafe impl Send for Decoder {}

impl Decoder {
    pub fn new(config: &Config) -> Result<Self, DecoderError> {
        let ptr = unsafe { ffi::decoder_create(config.as_raw()) };
        if ptr.is_null() {
            return Err(DecoderError::InitFailed);
        }
        Ok(Self { ptr })
    }

    pub fn decode(&mut self, input: &[u8]) -> Result<Frame, DecoderError> {
        let ret = unsafe {
            ffi::decoder_decode(self.ptr, input.as_ptr(), input.len())
        };
        if ret < 0 { return Err(DecoderError::from_code(ret)); }
        // ...
        Ok(frame)
    }
}

impl Drop for Decoder {
    fn drop(&mut self) {
        if !self.ptr.is_null() {
            unsafe { ffi::decoder_destroy(self.ptr); }
        }
    }
}
```

### Callbacks from C

```rust
// C expects: void (*callback)(void* user_data, int event, const char* msg)

extern "C" fn on_event(user_data: *mut c_void, event: c_int, msg: *const c_char) {
    // SAFETY: user_data was created from Box::into_raw in register_callback
    let handler = unsafe { &mut *(user_data as *mut EventHandler) };
    let msg = unsafe { CStr::from_ptr(msg) }.to_string_lossy();
    handler.handle(event, &msg);
}

fn register_callback(handler: Box<EventHandler>) {
    let user_data = Box::into_raw(handler) as *mut c_void;
    unsafe { ffi::set_callback(on_event, user_data); }
    // Must call Box::from_raw(user_data) later to free!
}
```

## Memory Patterns for Media

### Arena Allocator (bumpalo)

```rust
use bumpalo::Bump;

fn process_batch(frames: &[RawFrame]) -> Vec<ProcessedFrame> {
    let arena = Bump::with_capacity(frames.len() * FRAME_SIZE);

    let intermediates: Vec<&[u8]> = frames.iter()
        .map(|f| arena.alloc_slice_copy(&f.data))
        .collect();

    // All arena memory freed here when `arena` drops — one dealloc total
    process_intermediates(&intermediates)
}
```

### Zero-Copy with Shared Memory

```rust
use memmap2::MmapMut;

// Shared memory ring buffer for IPC (e.g., between encoder/decoder processes)
let file = OpenOptions::new()
    .read(true).write(true).create(true)
    .open("/dev/shm/video_buffer")?;
file.set_len(RING_SIZE as u64)?;

let mut mmap = unsafe { MmapMut::map_mut(&file)? };
let ring = RingBuffer::from_raw(&mut mmap[..]);
```

### Pre-allocated Frame Pool

```rust
struct FramePool {
    frames: Vec<Frame>,
    free: crossbeam_queue::ArrayQueue<usize>,
}

impl FramePool {
    fn new(count: usize, frame_size: usize) -> Self {
        let frames: Vec<Frame> = (0..count)
            .map(|_| Frame::with_capacity(frame_size))
            .collect();
        let free = ArrayQueue::new(count);
        for i in 0..count { let _ = free.push(i); }
        Self { frames, free }
    }

    fn acquire(&self) -> Option<&mut Frame> {
        let idx = self.free.pop()?;
        // SAFETY: index valid, single consumer per slot
        Some(unsafe { &mut *(&self.frames[idx] as *const Frame as *mut Frame) })
    }

    fn release(&self, idx: usize) {
        let _ = self.free.push(idx);
    }
}
```

## Cargo Workspace Patterns

### Multi-Crate Layout (ALVR-style)

```
project/
├── Cargo.toml          # [workspace] members
├── crates/
│   ├── common/         # Shared types, no unsafe
│   ├── protocol/       # Wire format, serialization
│   ├── server/         # Platform-specific, unsafe FFI
│   ├── client/         # Platform-specific, unsafe FFI
│   └── xtask/          # Build automation (cargo xtask)
```

```toml
# Root Cargo.toml
[workspace]
members = ["crates/*"]
resolver = "2"  # REQUIRED for edition 2021+

[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
anyhow = "1"
log = "0.4"
```

```toml
# crates/server/Cargo.toml
[dependencies]
common = { path = "../common" }
serde.workspace = true
anyhow.workspace = true
```

### Feature Flag Discipline

```toml
[features]
default = []
# Keep features additive — never subtract functionality
cuda = ["dep:cust"]
vulkan = ["dep:ash"]
tracy = ["dep:tracy-client"]

# Feature gates for platform-specific code
[target.'cfg(target_os = "linux")'.dependencies]
v4l2 = { version = "0.1", optional = true }
```

**Common pitfalls:**
- Features must be **additive** — `feature_a` + `feature_b` must compile
- `default-features = false` on workspace deps propagates — check `cargo tree -e features`
- Conflicting features from different workspace members cause silent bugs

## Cross-Compilation

### Android NDK Setup

```toml
# .cargo/config.toml
[target.aarch64-linux-android]
linker = "aarch64-linux-android34-clang"

[target.x86_64-linux-android]
linker = "x86_64-linux-android34-clang"
```

```bash
# Install targets
rustup target add aarch64-linux-android x86_64-linux-android

# Set NDK path
export ANDROID_NDK_HOME=/path/to/ndk
export PATH="$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/darwin-x86_64/bin:$PATH"

# Build
cargo build --target aarch64-linux-android --release
```

**Common issues:**
- Missing `libclang` for bindgen: set `LIBCLANG_PATH` to NDK's clang
- C library linking: use `cc` crate with `.target()` in build.rs
- OpenSSL: use `rustls` instead, or `openssl = { features = ["vendored"] }`

## Profiling

| Tool | Use Case | Integration |
|------|----------|-------------|
| `cargo flamegraph` | CPU hotspots | `cargo install flamegraph` |
| `perf` (Linux) | System-level profiling | `perf record --call-graph dwarf` |
| Tracy | Frame-level real-time profiling | `tracy-client` crate |
| `DHAT` | Heap profiling | `dhat` crate, `#[global_allocator]` |
| `cargo-bloat` | Binary size analysis | `cargo install cargo-bloat` |

### Tracy Integration

```toml
[dependencies]
tracy-client = { version = "0.17", optional = true }

[features]
tracy = ["dep:tracy-client"]
```

```rust
#[cfg(feature = "tracy")]
use tracy_client::{span, Client};

fn process_frame(frame: &Frame) {
    #[cfg(feature = "tracy")]
    let _span = span!("process_frame");

    decode(frame);
    transform(frame);
    encode(frame);
}
```

### Release Profile for Media

```toml
[profile.release]
lto = "thin"        # full LTO too slow for large projects
codegen-units = 1   # better optimization, slower compile
panic = "abort"     # smaller binary, no unwinding in RT
strip = true        # remove debug symbols from release
opt-level = 3       # max optimization

[profile.release.package.codec-crate]
opt-level = 3       # ensure hot crate is fully optimized

[profile.dev]
opt-level = 1       # faster dev builds with some optimization
```

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| `impl Send for Wrapper<*mut T>` without justification | Audit thread safety, add `// SAFETY:` |
| `transmute` between non-`#[repr(C)]` types | Use `bytemuck` or manual field copy |
| `Vec` in audio callback | `ArrayVec`, `heapless::Vec`, or pre-allocated slice |
| `Mutex` in render loop | `AtomicU64` for counters, lock-free queue for data |
| `String` in error enum | `Copy` enum variants, error codes |
| `unwrap()` on channel recv in hot path | `match` or `if let Ok(v)` |
| Forgetting `#[repr(C)]` on FFI structs | Always `#[repr(C)]` for types crossing FFI |
| Using `std::time::Instant` for frame timing on all platforms | Use `mach_absolute_time` on macOS, `clock_gettime(MONOTONIC_RAW)` on Linux |
| `Box::into_raw` without matching `Box::from_raw` | Track ownership, free in `Drop` |
| Feature flags that aren't additive | Test `--all-features` in CI |

## Quality Gates

- [ ] `cargo clippy --all-targets --all-features -- -D warnings`
- [ ] `cargo test` (cold path tests)
- [ ] `cargo build --release` (catch LTO/optimization issues)
- [ ] No `unwrap()`/`expect()` in hot path code
- [ ] All `unsafe` blocks have `// SAFETY:` comments
- [ ] Cross-compile targets build: `cargo build --target aarch64-linux-android`

## Deep Reference

Load on demand from `references/`:

| Reference | Use When |
|-----------|----------|
| `ffi-patterns.md` | Complex bindgen configs, opaque types, callback lifetimes, vendoring C libs |
| `realtime-patterns.md` | Lock-free data structures, SPSC queues, atomics ordering, thread pinning, scheduling |
