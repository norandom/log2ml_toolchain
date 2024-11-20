use std::process::Command;

fn get_python_lib_path() -> Option<String> {
    // Try to get Python library path using python3.11-config
    if let Ok(output) = Command::new("python3.11")
        .args(&[
            "-c",
            "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))",
        ])
        .output()
    {
        if let Ok(path) = String::from_utf8(output.stdout) {
            return Some(path.trim().to_string());
        }
    }

    // Fallback: try to get it from python3-config
    if let Ok(output) = Command::new("python3")
        .args(&[
            "-c",
            "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))",
        ])
        .output()
    {
        if let Ok(path) = String::from_utf8(output.stdout) {
            return Some(path.trim().to_string());
        }
    }

    None
}

fn main() {
    // Add Python library path for Unix-like systems (macOS and Linux)
    if cfg!(any(target_os = "macos", target_os = "linux")) {
        if let Some(python_lib_path) = get_python_lib_path() {
            println!("cargo:rustc-link-arg=-Wl,-rpath,{}", python_lib_path);
        } else {
            println!("cargo:warning=Could not determine Python library path");
        }

        // Add system library paths for macOS
        if cfg!(target_os = "macos") {
            // Add system library path for libiconv
            println!("cargo:rustc-link-arg=-Wl,-rpath,/usr/lib");
        }
    }

    let status = std::process::Command::new("python3")
        .args([
            "-c",
            "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))",
        ])
        .status();

    match status {
        Ok(_) => (),
        Err(_) => {
            let status = std::process::Command::new("python")
                .args([
                    "-c",
                    "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))",
                ])
                .status()
                .unwrap();
            assert!(status.success());
        }
    }

    tauri_build::build()
}
