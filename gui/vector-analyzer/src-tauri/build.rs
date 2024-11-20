use std::process::Command;

fn main() {
    // Run tauri build
    tauri_build::build();

    // Get Python library directory
    let python_cmd = if Command::new("python3").output().is_ok() {
        "python3"
    } else {
        "python"
    };

    let python_libdir = Command::new(python_cmd)
        .args([
            "-c",
            "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))",
        ])
        .output()
        .expect("Failed to get Python library directory");

    let python_libdir = String::from_utf8_lossy(&python_libdir.stdout)
        .trim()
        .to_string();

    if !python_libdir.is_empty() {
        println!("cargo:rustc-link-search=native={}", python_libdir);
    }

    // Add system library paths for macOS
    if cfg!(target_os = "macos") {
        // Add system library path for Python
        println!("cargo:rustc-link-arg=-Wl,-rpath,/usr/local/lib");
        println!("cargo:rustc-link-arg=-Wl,-rpath,/usr/lib");
    }
}
