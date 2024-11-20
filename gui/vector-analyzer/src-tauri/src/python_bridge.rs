use pyo3::prelude::*;
use pyo3::types::PyDict;
use serde::{Deserialize, Serialize};
use std::path::Path;

#[derive(Debug, Serialize, Deserialize)]
pub struct AnalysisResult {
    pub charts: Vec<ChartData>,
    pub metrics: serde_json::Value,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ChartData {
    pub chart_type: String,
    pub data: serde_json::Value,
}

pub fn init_python() -> PyResult<()> {
    pyo3::prepare_freethreaded_python();
    Ok(())
}

pub fn run_analysis(
    csv_path: &str,
    model_type: &str,
    notebook_path: &str,
) -> PyResult<AnalysisResult> {
    Python::with_gil(|py| {
        // Import the notebook converter
        let converter = PyModule::import(py, "log2ml.utils.notebook_converter")?;

        // Convert notebook to module
        let args = (notebook_path,);
        let (module_path, module_name): (String, String) = converter
            .getattr("convert_notebook_to_module")?
            .call1(args)?
            .extract()?;

        // Add module directory to Python path
        let module_dir = Path::new(&module_path).parent().unwrap();
        let sys = PyModule::import(py, "sys")?;
        let path = sys.getattr("path")?.downcast::<pyo3::types::PyList>()?;
        path.insert(0, module_dir.to_str().unwrap())?;

        // Import the converted module and run analysis
        let analysis_module = PyModule::import(py, module_name.as_str())?;
        let kwargs = PyDict::new(py);
        kwargs.set_item("csv_path", csv_path)?;
        kwargs.set_item("model_type", model_type)?;

        let result = analysis_module
            .getattr("run_analysis")?
            .call((), Some(kwargs))?;
        let result_str = result.to_string();
        let result_dict: serde_json::Value = serde_json::from_str(&result_str).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to parse JSON: {}", e))
        })?;

        Ok(AnalysisResult {
            charts: result_dict["charts"]
                .as_array()
                .unwrap()
                .iter()
                .map(|chart| ChartData {
                    chart_type: chart["type"].as_str().unwrap().to_string(),
                    data: chart["data"].clone(),
                })
                .collect(),
            metrics: result_dict["metrics"].clone(),
        })
    })
}
