#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

mod python_bridge;

use serde::{Deserialize, Serialize};
use std::fs::File;
use std::path::PathBuf;
use std::sync::Mutex;
use tauri::State;

#[derive(Debug, Serialize, Deserialize)]
struct CsvData {
    messages: Vec<String>,
}

struct NotebookPath(Mutex<PathBuf>);

#[tauri::command]
async fn read_csv(path: String) -> Result<CsvData, String> {
    let file = File::open(path).map_err(|e| e.to_string())?;
    let mut rdr = csv::Reader::from_reader(file);
    let mut messages = Vec::new();

    for result in rdr.records() {
        let record = result.map_err(|e| e.to_string())?;
        if let Some(message) = record.get(0) {
            messages.push(message.to_string());
        }
    }

    Ok(CsvData { messages })
}

#[tauri::command]
async fn analyze_data(
    csv_path: String,
    model_type: String,
    notebook_path: State<'_, NotebookPath>,
) -> Result<python_bridge::AnalysisResult, String> {
    let notebook = notebook_path.0.lock().unwrap();
    python_bridge::run_analysis(&csv_path, &model_type, notebook.to_str().unwrap())
        .map_err(|e| e.to_string())
}

fn main() {
    // Initialize Python
    python_bridge::init_python().expect("Failed to initialize Python");

    // Get the project root directory (3 levels up from the current executable)
    let exe_dir = std::env::current_exe().expect("Failed to get executable path");
    let project_root = exe_dir
        .parent()
        .unwrap() // target/debug
        .parent()
        .unwrap() // target
        .parent()
        .unwrap() // src-tauri
        .parent()
        .unwrap() // vector-analyzer
        .parent()
        .unwrap() // gui
        .parent()
        .unwrap(); // project root

    // Construct the path to the notebook
    let notebook_path = project_root
        .join("notebooks")
        .join("LinFormer_AutoML_on_AE_sysmon_dataset_(Excel_implant_C2).ipynb");

    if !notebook_path.exists() {
        panic!("Notebook not found at: {}", notebook_path.display());
    }

    let notebook_path = NotebookPath(Mutex::new(notebook_path));

    tauri::Builder::default()
        .manage(notebook_path)
        .invoke_handler(tauri::generate_handler![read_csv, analyze_data])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
