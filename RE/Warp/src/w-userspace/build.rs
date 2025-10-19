use std::{env, fs, path::Path, process::Command};

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();
    let ebpf_dir = Path::new("../w-ebpf");

    // Check if we're in a dependency-only build (common in Nix/Crane builds)
    let is_deps_only = env::var("CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_DEBUG").is_ok()
        || env::var("CRANE_BUILD_DEPS_ONLY").is_ok()
        || !ebpf_dir.exists()
        || !ebpf_dir.join("Makefile").exists();

    // Always set up rerun-if-changed for the eBPF directory if it exists

    for file in visit_dir(ebpf_dir) {
        println!("cargo:rerun-if-changed={}", file);
    }

    // TODO: include btf file fetching to pass to the make on systems that don't have btf headers
    // Skip eBPF compilation if this is a dependency-only build or eBPF files are missing
    if is_deps_only {
        println!(
            "cargo:warning=Skipping eBPF compilation (dependency-only build or missing eBPF files)"
        );

        // Create a dummy output file so the build doesn't fail
        let dummy_output = Path::new(&out_dir).join("dummy_ebpf.o");
        std::fs::write(dummy_output, b"").expect("Failed to create dummy eBPF output");

        return;
    }

    // Run the actual eBPF compilation
    println!("cargo:warning=Starting eBPF compilation");

    let output = Command::new("make")
        .arg(format!("OUT_DIR={}", out_dir))
        .current_dir(ebpf_dir)
        .output()
        .expect("Failed to run make");

    let stderr_content = String::from_utf8_lossy(&output.stderr);
    let stdout_content = String::from_utf8_lossy(&output.stdout);

    if !output.status.success() {
        panic!(
            "make command failed.\nstdout: {}\nstderr: {}",
            stdout_content, stderr_content
        );
    }

    println!("cargo:warning=eBPF side finished compiling");
}

fn visit_dir(dir: &Path) -> Vec<String> {
    let mut files = Vec::new();
    if let Ok(entries) = fs::read_dir(dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_file() {
                files.push(path.display().to_string());
            } else if path.is_dir() {
                // don't rebuild if libbpf changes
                if path.file_name().unwrap() != "libbpf" {
                    files.extend(visit_dir(&path));
                }
            }
        }
    }
    files
}
