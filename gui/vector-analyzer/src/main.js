import { invoke } from '@tauri-apps/api/tauri';
import { open } from '@tauri-apps/api/dialog';
import Chart from 'chart.js/auto';

let csvPath = null;
let selectedModel = null;
let charts = [];

// File upload handling
document.getElementById('upload-btn').addEventListener('click', async () => {
    try {
        const selected = await open({
            multiple: false,
            filters: [{
                name: 'CSV',
                extensions: ['csv']
            }]
        });
        
        if (selected) {
            csvPath = selected;
            const fileName = csvPath.split('/').pop();
            document.getElementById('file-name').textContent = `Selected file: ${fileName}`;
            document.getElementById('error').textContent = '';
            
            // Validate CSV structure
            try {
                const data = await invoke('read_csv', { path: csvPath });
                if (data.messages.length === 0) {
                    throw new Error('No messages found in CSV');
                }
            } catch (e) {
                document.getElementById('error').textContent = `Error: ${e}`;
                csvPath = null;
                document.getElementById('file-name').textContent = '';
            }
        }
    } catch (e) {
        document.getElementById('error').textContent = `Error: ${e}`;
    }
});

// Model selection handling
document.querySelectorAll('.model-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.model-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedModel = btn.dataset.model;
        document.getElementById('selected-model').textContent = `Selected model: ${selectedModel}`;
    });
});

function createChart(container, chartData) {
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: chartData.chart_type,
        data: chartData.data,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    charts.push(chart);
    return chart;
}

// Analysis handling
document.getElementById('analyze-btn').addEventListener('click', async () => {
    if (!csvPath) {
        document.getElementById('error').textContent = 'Please upload a CSV file first';
        return;
    }
    
    if (!selectedModel) {
        document.getElementById('error').textContent = 'Please select a model first';
        return;
    }
    
    document.getElementById('error').textContent = '';
    const dialog = document.getElementById('analysis-dialog');
    const chartsContainer = dialog.querySelector('.charts-container');
    dialog.style.display = 'block';
    
    try {
        chartsContainer.innerHTML = '<p>Analysis in progress...</p>';
        
        // Destroy existing charts
        charts.forEach(chart => chart.destroy());
        charts = [];
        
        // Run analysis
        const result = await invoke('analyze_data', {
            csvPath,
            modelType: selectedModel
        });
        
        // Clear loading message
        chartsContainer.innerHTML = '';
        
        // Create charts
        result.charts.forEach(chartData => {
            const chartDiv = document.createElement('div');
            chartDiv.className = 'chart-container';
            chartsContainer.appendChild(chartDiv);
            createChart(chartDiv, chartData);
        });
        
    } catch (e) {
        document.getElementById('error').textContent = `Analysis error: ${e}`;
        chartsContainer.innerHTML = `<p class="error">Analysis failed: ${e}</p>`;
    }
});

// Dialog close button
document.querySelector('.close-btn').addEventListener('click', () => {
    document.getElementById('analysis-dialog').style.display = 'none';
});
