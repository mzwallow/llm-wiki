# Zig Build System

**Source:** [Zig Build System](https://ziglang.org/learn/build-system/)
**Added:** 2026-05-02

The Zig Build System is a powerful tool for managing project compilation, dependencies, and complex build steps using Zig code itself. It leverages a Directed Acyclic Graph (DAG) of steps.

## Core Concepts

### Steps and DAG
The build process is modeled as a DAG of steps. The default main step is `install`.
- **Install Step:** Copies build artifacts to the installation prefix (default: `zig-out`).
- **Run Step:** Executes a compiled artifact or a system command.
- **Compile Step:** Orchestrates the compilation of executables, libraries, or objects.

### Artifacts and Output
- `.zig-cache`: Local cache for incremental builds. Safe to delete.
- `zig-out`: The "installation prefix" where final artifacts are placed.

### Build Script (`build.zig`)
The `build` function is the entry point:
```zig
pub fn build(b: *std.Build) void {
    // ...
}
```

## Common Operations

### Adding an Executable
```zig
const exe = b.addExecutable(.{
    .name = "hello",
    .root_module = b.createModule(.{
        .root_source_file = b.path("hello.zig"),
        .target = b.graph.host,
    }),
});
b.installArtifact(exe);
```

### User Options
Users can pass options via `-Dname=value`:
```zig
const windows = b.option(bool, "windows", "Target Microsoft Windows") orelse false;
```
Standard helpers:
- `b.standardTargetOptions(.{})`: Adds `-Dtarget` and `-Dcpu`.
- `b.standardOptimizeOption(.{})`: Adds `-Doptimize` (Debug, ReleaseSafe, ReleaseFast, ReleaseSmall).

### Conditional Compilation
Use `b.addOptions()` to pass values from `build.zig` to your Zig code as a module.

### Testing
Unit tests are split into **Compile** and **Run** steps. Use `b.addTest` and `b.addRunArtifact`.

### Generating Files
- `b.addSystemCommand`: Run external tools like `jq` or `tar`.
- `b.addRunArtifact`: Run tools built as part of the project.
- `b.addWriteFiles`: Generate strings or copy files into the cache.
- `b.addUpdateSourceFiles`: Update files in the source tree (use with caution).

## Linking
- **System Libraries:** Use `exe.root_module.linkSystemLibrary("z", .{})` and `link_libc = true`.
- **Zig Packages:** Managed via the package manager (see `build.zig.zon`).

## See Also
- [[zig-language]]
- [[zig-0.16.0-doc]]
