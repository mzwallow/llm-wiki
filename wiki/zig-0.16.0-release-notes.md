# Zig 0.16.0 Release Notes

Zig 0.16.0 (May 2026) represents a major milestone with the introduction of the new I/O interface and significant language refinements.

## Major Highlights

### I/O as an Interface (`std.Io`)
All input and output functionality now requires being passed an `Io` instance. This decouples I/O operations from their implementations.
- **Implementations**:
    - `Io.Threaded`: Standard thread-based I/O (default).
    - `Io.Evented`: Experimental stackful coroutines / green threads.
    - `Io.Uring`, `Io.Kqueue`, `Io.Dispatch`: Platform-specific asynchronous backends.
- **New Concepts**: `Future`, `Group`, `Batch`, and `Select` for managing concurrency and cancelation.

### "Juicy Main"
The `main` function can now accept `std.process.Init`, providing a pre-initialized environment:
```zig
pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const gpa = init.gpa;
    // ...
}
```

### Language Changes
- **Builtin Type Reification**: `@Type` is replaced by specific builtins like `@Int`, `@Struct`, `@Union`, `@Enum`, `@Pointer`, `@Fn`, `@Tuple`, and `@EnumLiteral`.
- **@cImport Deprecation**: C translation is moving to the Build System (`b.addTranslateC`).
- **Safety Improvements**: Returning addresses of local variables is now a compile error. Runtime vector indexing is forbidden.
- **Ergonomics**: Small integers now coerce to floats if the value fits perfectly. Unary float builtins (`@sqrt`, etc.) now forward result types.

### Standard Library
- **Memory**: `std.mem.indexOf` renamed to `std.mem.find`. Added `cut` functions for string/slice splitting.
- **Allocators**: `ArenaAllocator` is now thread-safe and lock-free. `ThreadSafeAllocator` wrapper is removed.
- **Compression**: Native Deflate compression added.
- **Windows**: Networking migrated to direct AFD access, removing the `ws2_32.dll` dependency. Full migration to `NtDll` for most syscalls.

## Breaking Changes & Migrations
- **Environment/Args**: No longer global. Access via `std.process.Init`.
- **I/O Parameters**: Most `std.fs` and `std.net` functions now require an `Io` parameter.
- **Packed Types**: Packed unions now require explicit backing integers in extern contexts. Pointers are forbidden in packed types.

## See Also
- [[zig-language]]
- [[zig-0.16.0-doc]]
