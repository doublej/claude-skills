# Real-Time Patterns — Deep Reference

## Atomic Operations & Ordering

### Ordering Quick Reference

| Ordering | Use | Cost |
|----------|-----|------|
| `Relaxed` | Counters, stats, flags (no synchronization needed) | Cheapest |
| `Acquire` | Reading shared state (pairs with `Release` store) | Load fence |
| `Release` | Publishing shared state (pairs with `Acquire` load) | Store fence |
| `AcqRel` | Read-modify-write on shared data | Both fences |
| `SeqCst` | When in doubt (full sequential consistency) | Most expensive |

### Common Atomic Patterns

```rust
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};

// Shutdown flag — writer: Release, reader: Acquire
static RUNNING: AtomicBool = AtomicBool::new(true);

fn signal_shutdown() {
    RUNNING.store(false, Ordering::Release);
}

fn render_loop() {
    while RUNNING.load(Ordering::Acquire) {
        process_frame();
    }
}

// Frame counter — Relaxed is fine (no data depends on the count)
static FRAME_COUNT: AtomicU64 = AtomicU64::new(0);

fn tick() {
    FRAME_COUNT.fetch_add(1, Ordering::Relaxed);
}

// Double-buffer swap index
static BUFFER_IDX: AtomicUsize = AtomicUsize::new(0);

fn swap_buffers() -> usize {
    BUFFER_IDX.fetch_xor(1, Ordering::AcqRel)
}
```

## Lock-Free Data Structures

### SPSC Ring Buffer (Audio/Video)

For single-producer, single-consumer — the most common real-time pattern:

```rust
use ringbuf::{HeapRb, traits::*};

// Audio: producer on capture thread, consumer on process thread
let rb = HeapRb::<f32>::new(4096);
let (mut producer, mut consumer) = rb.split();

// Producer thread (audio capture)
std::thread::spawn(move || {
    let mut capture_buf = [0f32; 256];
    loop {
        capture_audio(&mut capture_buf);
        // Push what fits, drop the rest (never block)
        let written = producer.push_slice(&capture_buf);
        if written < capture_buf.len() {
            stats_dropped.fetch_add(1, Ordering::Relaxed);
        }
    }
});

// Consumer thread (audio processing)
std::thread::spawn(move || {
    let mut process_buf = [0f32; 256];
    loop {
        let read = consumer.pop_slice(&mut process_buf);
        if read > 0 {
            process_audio(&process_buf[..read]);
        } else {
            std::hint::spin_loop(); // no data yet
        }
    }
});
```

### MPMC Queue (crossbeam)

```rust
use crossbeam_queue::ArrayQueue;
use std::sync::Arc;

// Fixed-capacity, lock-free, multi-producer multi-consumer
let queue = Arc::new(ArrayQueue::new(64));

// Multiple producers
let q = queue.clone();
std::thread::spawn(move || {
    for frame in frames {
        match q.push(frame) {
            Ok(()) => {}
            Err(frame) => drop(frame), // queue full, drop oldest strategy
        }
    }
});

// Consumer
while let Some(frame) = queue.pop() {
    process(frame);
}
```

### Triple Buffer (Latest-Value Pattern)

For "reader always gets latest value, writer never blocks":

```rust
use triple_buffer::TripleBuffer;

let (mut writer, mut reader) = TripleBuffer::new(&GameState::default()).split();

// Game logic thread (writer)
std::thread::spawn(move || {
    loop {
        let mut state = GameState::default();
        update_game(&mut state);
        writer.write(state); // never blocks
    }
});

// Render thread (reader) — always gets latest complete state
loop {
    reader.update(); // swap to latest buffer
    let state = reader.read();
    render(state);
}
```

## Thread Pinning & Priority

### Thread Affinity (Linux)

```rust
use core_affinity;

fn pin_to_core(core_id: usize) {
    let core_ids = core_affinity::get_core_ids().unwrap();
    if let Some(id) = core_ids.get(core_id) {
        core_affinity::set_for_current(*id);
    }
}

// Pin render thread to core 2, audio to core 3
std::thread::Builder::new()
    .name("render".into())
    .spawn(move || {
        pin_to_core(2);
        set_realtime_priority();
        render_loop();
    })?;
```

### Real-Time Scheduling (Linux)

```rust
fn set_realtime_priority() -> Result<(), std::io::Error> {
    #[cfg(target_os = "linux")]
    {
        let param = libc::sched_param { sched_priority: 80 };
        let ret = unsafe {
            libc::sched_setscheduler(0, libc::SCHED_FIFO, &param)
        };
        if ret != 0 {
            return Err(std::io::Error::last_os_error());
        }
    }
    Ok(())
}
```

**Priority inversion prevention:**
- Never hold a lock in a high-priority thread that a low-priority thread also needs
- Use lock-free structures or `try_lock` with fallback
- If you must lock, use priority inheritance mutexes (`PTHREAD_PRIO_INHERIT`)

## Spin-Wait and Timing

### Frame Budget Timing

```rust
use std::time::{Duration, Instant};

const FRAME_BUDGET: Duration = Duration::from_micros(11_111); // 90fps VR

fn frame_loop(state: &mut State) {
    loop {
        let start = Instant::now();

        process_frame(state);

        let elapsed = start.elapsed();
        let remaining = FRAME_BUDGET.saturating_sub(elapsed);

        if remaining > Duration::from_millis(2) {
            // Sleep for bulk of wait (OS timer resolution ~1-15ms)
            std::thread::sleep(remaining - Duration::from_millis(1));
        }
        // Spin for the last bit (sub-ms precision)
        while start.elapsed() < FRAME_BUDGET {
            std::hint::spin_loop();
        }
    }
}
```

### Adaptive Quality

```rust
struct FrameStats {
    budget: Duration,
    avg_time: Duration,
    quality: QualityLevel,
}

impl FrameStats {
    fn update(&mut self, frame_time: Duration) {
        // Exponential moving average
        self.avg_time = Duration::from_nanos(
            (self.avg_time.as_nanos() as f64 * 0.9 + frame_time.as_nanos() as f64 * 0.1) as u64
        );

        // Adjust quality to hit frame budget
        let headroom = self.budget.as_micros() as f64 / self.avg_time.as_micros() as f64;
        self.quality = match headroom {
            h if h < 0.9 => self.quality.lower(), // over budget — reduce
            h if h > 1.3 => self.quality.raise(), // plenty of headroom — increase
            _ => self.quality,                     // in range — keep
        };
    }
}
```

## Zero-Copy Patterns

### Borrowed Slices from C Buffers

```rust
/// Frame data borrowed from the C decoder. Valid until next decode call.
pub struct BorrowedFrame<'a> {
    data: &'a [u8],
    width: u32,
    height: u32,
}

impl Decoder {
    /// Returns a frame that borrows the decoder's internal buffer.
    /// The frame is invalidated on the next call to `decode`.
    pub fn decode_borrowed(&mut self) -> Result<BorrowedFrame<'_>, Error> {
        let mut ptr: *const u8 = std::ptr::null();
        let mut len: usize = 0;
        let ret = unsafe { ffi::decode(self.ptr, &mut ptr, &mut len) };
        if ret < 0 { return Err(Error::Decode(ret)); }

        // SAFETY: ptr/len valid until next decode call. &mut self prevents
        // concurrent decode calls, so the borrow is sound.
        let data = unsafe { std::slice::from_raw_parts(ptr, len) };
        Ok(BorrowedFrame { data, width: self.width, height: self.height })
    }
}
```

### DMA-buf / GPU Buffer Mapping

```rust
// Conceptual pattern for GPU buffer access (e.g., via Vulkan/ash)
pub struct MappedBuffer<'a> {
    ptr: *mut u8,
    len: usize,
    device: &'a Device,
    memory: vk::DeviceMemory,
}

impl<'a> MappedBuffer<'a> {
    pub fn as_slice(&self) -> &[u8] {
        // SAFETY: mapped for duration of MappedBuffer lifetime
        unsafe { std::slice::from_raw_parts(self.ptr, self.len) }
    }

    pub fn as_mut_slice(&mut self) -> &mut [u8] {
        unsafe { std::slice::from_raw_parts_mut(self.ptr, self.len) }
    }
}

impl Drop for MappedBuffer<'_> {
    fn drop(&mut self) {
        unsafe { self.device.unmap_memory(self.memory); }
    }
}
```

## Pipeline Architecture

### Channel-Based Media Pipeline

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Capture  │───>│ Decode   │───>│ Process  │───>│ Encode   │
│ (thread) │ ch │ (thread) │ ch │ (thread) │ ch │ (thread) │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     bounded(2)      bounded(4)       bounded(2)
```

```rust
fn build_pipeline() -> Result<PipelineHandle, Error> {
    let (cap_tx, cap_rx) = bounded::<RawPacket>(2);
    let (dec_tx, dec_rx) = bounded::<DecodedFrame>(4);
    let (proc_tx, proc_rx) = bounded::<ProcessedFrame>(2);

    let capture = std::thread::Builder::new()
        .name("capture".into())
        .spawn(move || capture_loop(cap_tx))?;

    let decode = std::thread::Builder::new()
        .name("decode".into())
        .spawn(move || decode_loop(cap_rx, dec_tx))?;

    let process = std::thread::Builder::new()
        .name("process".into())
        .spawn(move || process_loop(dec_rx, proc_tx))?;

    let encode = std::thread::Builder::new()
        .name("encode".into())
        .spawn(move || encode_loop(proc_rx))?;

    Ok(PipelineHandle {
        threads: vec![capture, decode, process, encode],
    })
}

fn decode_loop(rx: Receiver<RawPacket>, tx: Sender<DecodedFrame>) {
    let mut decoder = Decoder::new().unwrap();

    while let Ok(packet) = rx.recv() {
        match decoder.decode(&packet) {
            Ok(frame) => {
                if tx.try_send(frame).is_err() {
                    // Downstream full — drop frame, don't block
                    log::debug!("decode: dropped frame (downstream full)");
                }
            }
            Err(e) => log::warn!("decode error: {e:?}"), // skip, don't crash
        }
    }
}
```

### Graceful Shutdown

```rust
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

struct Pipeline {
    running: Arc<AtomicBool>,
    threads: Vec<JoinHandle<()>>,
}

impl Pipeline {
    fn shutdown(&mut self) {
        // Signal all threads
        self.running.store(false, Ordering::Release);

        // Drop channel senders (unblocks recv loops)
        // (handled by dropping the sender halves)

        // Join with timeout
        for handle in self.threads.drain(..) {
            let name = handle.thread().name().unwrap_or("?").to_string();
            match handle.join() {
                Ok(()) => log::info!("{name} stopped"),
                Err(e) => log::error!("{name} panicked: {e:?}"),
            }
        }
    }
}
```

## Testing Real-Time Code

### Deterministic Testing (No Timing)

```rust
#[cfg(test)]
mod tests {
    // Test pipeline logic without threads or timing
    fn test_decode_handles_corrupt_frame() {
        let mut decoder = Decoder::new().unwrap();
        let corrupt = RawPacket::from_bytes(&[0xFF; 100]);
        assert_eq!(decoder.decode(&corrupt), Err(FrameError::DecodeFailed));
    }

    // Test channel behavior
    fn test_pipeline_drops_when_full() {
        let (tx, rx) = bounded(1);
        tx.send(Frame::test()).unwrap();

        // Channel full — try_send should fail
        assert!(tx.try_send(Frame::test()).is_err());

        // Consumer gets the first frame
        assert!(rx.recv().is_ok());
    }
}
```

### Stress Testing

```rust
#[test]
#[ignore] // run with: cargo test -- --ignored
fn stress_test_pipeline_throughput() {
    let pipeline = build_test_pipeline();
    let start = Instant::now();
    let frames = 10_000;

    for i in 0..frames {
        pipeline.submit(Frame::synthetic(i));
    }
    pipeline.flush();

    let elapsed = start.elapsed();
    let fps = frames as f64 / elapsed.as_secs_f64();
    assert!(fps > 60.0, "Pipeline too slow: {fps:.1} fps");
}
```

## Crate Recommendations

| Category | Crate | Notes |
|----------|-------|-------|
| Lock-free SPSC | `ringbuf` | Ring buffer, audio/video |
| Lock-free MPMC | `crossbeam-queue` | `ArrayQueue`, `SegQueue` |
| Lock-free map | `dashmap` | Concurrent HashMap (cold path only) |
| Channels | `crossbeam-channel`, `flume` | Bounded, select, sync+async |
| Atomics | `std::sync::atomic` | Built-in, no deps |
| Arena allocator | `bumpalo` | Bump allocation, batch free |
| Stack collections | `arrayvec`, `heapless` | No-alloc Vec, String |
| Shared memory | `memmap2` | Memory-mapped files, IPC |
| Thread pinning | `core_affinity` | CPU core pinning |
| Fast hashing | `rustc-hash` | `FxHashMap`, non-crypto |
| Byte casting | `bytemuck` | Safe transmute for `#[repr(C)]` |
| Triple buffer | `triple_buffer` | Latest-value, non-blocking |
| Profiling | `tracy-client` | Frame-level, real-time |
