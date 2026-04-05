# FFI Patterns — Deep Reference

## bindgen Advanced Configuration

### Opaque Types

When a C struct has private fields or complex layout, treat it as opaque:

```rust
// build.rs
bindgen::Builder::default()
    .header("wrapper.h")
    .opaque_type("InternalState")     // don't generate fields
    .allowlist_function("api_.*")
    .blocklist_type("__.*")           // skip compiler builtins
    .derive_debug(false)              // avoid Debug on large structs
    .generate_comments(false)         // skip C doc comments
    .generate()
```

### Type Mappings

| C Type | Rust FFI Type | Safe Wrapper |
|--------|--------------|--------------|
| `void*` | `*mut c_void` | `Option<NonNull<T>>` |
| `const char*` | `*const c_char` | `&CStr` → `.to_str()` |
| `char*` (owned) | `*mut c_char` | `CString` |
| `int` | `c_int` | `i32` (after validation) |
| `size_t` | `usize` | `usize` |
| `bool` | `bool` | `bool` (C99 `_Bool` only) |
| `enum` | `c_int` or `c_uint` | Rust enum with `TryFrom` |
| `struct S` | `#[repr(C)] struct S` | Newtype wrapper |
| `union` | `#[repr(C)] union` | Safe accessor methods |
| `float[4]` | `[f32; 4]` | `[f32; 4]` |

### Callback Lifetime Management

The most dangerous FFI pattern. C libraries hold function pointers with `void* user_data`:

```rust
/// Registered callback context — must outlive the C library's usage.
struct CallbackCtx {
    sender: Sender<Event>,
    // Other captured state
}

impl Library {
    pub fn set_callback(&mut self, sender: Sender<Event>) -> Result<(), Error> {
        // Heap-allocate and leak intentionally — C lib owns the pointer now
        let ctx = Box::new(CallbackCtx { sender });
        let ctx_ptr = Box::into_raw(ctx) as *mut c_void;

        // Store raw pointer so we can reclaim in Drop
        self.callback_ctx = Some(ctx_ptr);

        unsafe {
            ffi::lib_set_callback(self.handle, Some(callback_trampoline), ctx_ptr);
        }
        Ok(())
    }
}

extern "C" fn callback_trampoline(
    user_data: *mut c_void,
    event_type: c_int,
    data: *const c_void,
    data_len: usize,
) {
    // SAFETY: user_data created from Box::into_raw(Box<CallbackCtx>) in set_callback.
    // Library guarantees single-threaded callback dispatch.
    let ctx = unsafe { &*(user_data as *const CallbackCtx) };

    let event = match Event::from_raw(event_type, data, data_len) {
        Some(e) => e,
        None => return, // unknown event — skip, don't panic
    };

    // try_send: never block in a callback (could deadlock the C library)
    let _ = ctx.sender.try_send(event);
}

impl Drop for Library {
    fn drop(&mut self) {
        // Unregister callback first
        unsafe { ffi::lib_set_callback(self.handle, None, std::ptr::null_mut()); }

        // Now safe to reclaim the context
        if let Some(ptr) = self.callback_ctx.take() {
            // SAFETY: ptr was created by Box::into_raw, callback unregistered above
            unsafe { drop(Box::from_raw(ptr as *mut CallbackCtx)); }
        }

        unsafe { ffi::lib_destroy(self.handle); }
    }
}
```

**Rules for callbacks:**
- Never `panic!` in `extern "C"` — UB (unwind across FFI boundary)
- Use `std::panic::catch_unwind` if callback body can panic
- Never block (mutex, channel send) — use `try_send` / `try_lock`
- Reclaim `Box::into_raw` in `Drop`, after unregistering the callback

### Vendoring C Libraries with cc

```rust
// build.rs — compile C source directly into the Rust binary
fn main() {
    cc::Build::new()
        .file("vendor/codec/src/decode.c")
        .file("vendor/codec/src/encode.c")
        .include("vendor/codec/include")
        .flag("-O3")
        .flag("-fPIC")
        .warnings(false)           // suppress vendor warnings
        .compile("codec");         // produces libcodec.a

    // bindgen against the same headers
    let bindings = bindgen::Builder::default()
        .header("vendor/codec/include/codec.h")
        .generate()
        .unwrap();

    let out = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings.write_to_file(out.join("bindings.rs")).unwrap();
}
```

### Handling C Enums Safely

```rust
// C: enum status_t { OK = 0, ERR_DECODE = -1, ERR_TIMEOUT = -2 };

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(i32)]
pub enum Status {
    Ok = 0,
    ErrDecode = -1,
    ErrTimeout = -2,
}

impl TryFrom<c_int> for Status {
    type Error = c_int;
    fn try_from(val: c_int) -> Result<Self, c_int> {
        match val {
            0 => Ok(Status::Ok),
            -1 => Ok(Status::ErrDecode),
            -2 => Ok(Status::ErrTimeout),
            other => Err(other),
        }
    }
}

// Usage in safe wrapper
fn decode(&mut self) -> Result<(), DecodeError> {
    let code = unsafe { ffi::decoder_decode(self.ptr) };
    match Status::try_from(code) {
        Ok(Status::Ok) => Ok(()),
        Ok(status) => Err(DecodeError::Status(status)),
        Err(unknown) => Err(DecodeError::Unknown(unknown)),
    }
}
```

## String Handling Across FFI

### Receiving C Strings

```rust
// Borrowed (C owns the memory, valid for some scope)
fn get_name(handle: *mut ffi::Device) -> Option<&str> {
    let ptr = unsafe { ffi::device_get_name(handle) };
    if ptr.is_null() { return None; }
    // SAFETY: ptr valid for lifetime of device, null-terminated
    let cstr = unsafe { CStr::from_ptr(ptr) };
    cstr.to_str().ok()
}

// Owned (Rust must free with C's allocator)
fn get_description(handle: *mut ffi::Device) -> Option<String> {
    let ptr = unsafe { ffi::device_get_description(handle) };
    if ptr.is_null() { return None; }
    let cstr = unsafe { CStr::from_ptr(ptr) };
    let result = cstr.to_string_lossy().into_owned();
    // Free using the C library's deallocator, NOT Rust's
    unsafe { ffi::lib_free(ptr as *mut c_void); }
    Some(result)
}
```

### Passing Strings to C

```rust
fn set_path(handle: *mut ffi::Device, path: &str) -> Result<(), Error> {
    let c_path = CString::new(path)
        .map_err(|_| Error::NullInString)?; // path contained \0
    unsafe { ffi::device_set_path(handle, c_path.as_ptr()); }
    Ok(())
    // c_path lives until end of scope — pointer valid during FFI call
}
```

## Struct Layout Verification

```rust
#[repr(C)]
#[derive(Debug, Clone, Copy)]
pub struct FrameHeader {
    pub timestamp: u64,
    pub width: u32,
    pub height: u32,
    pub format: u32,
    pub data_len: u32,
}

// Compile-time layout assertions
const _: () = {
    assert!(std::mem::size_of::<FrameHeader>() == 24);
    assert!(std::mem::align_of::<FrameHeader>() == 8);
};

// Or use static_assertions crate
static_assertions::assert_eq_size!(FrameHeader, [u8; 24]);
```

## Platform-Specific FFI

```rust
#[cfg(target_os = "linux")]
mod linux {
    use libc::{c_int, ioctl};

    pub fn set_realtime_priority() -> Result<(), std::io::Error> {
        let param = libc::sched_param {
            sched_priority: 80,
        };
        let ret = unsafe {
            libc::sched_setscheduler(0, libc::SCHED_FIFO, &param)
        };
        if ret != 0 {
            return Err(std::io::Error::last_os_error());
        }
        Ok(())
    }
}

#[cfg(target_os = "macos")]
mod macos {
    use std::os::raw::c_int;

    extern "C" {
        fn pthread_set_qos_class_self_np(qos: u32, relative_priority: c_int) -> c_int;
    }

    pub fn set_realtime_priority() -> Result<(), std::io::Error> {
        // QOS_CLASS_USER_INTERACTIVE = 0x21
        let ret = unsafe { pthread_set_qos_class_self_np(0x21, 0) };
        if ret != 0 {
            return Err(std::io::Error::last_os_error());
        }
        Ok(())
    }
}
```
