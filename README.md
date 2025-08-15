# Classification Metrics App

A simple Streamlit application for computing and displaying classification metrics. This app allows users to upload CSV or Excel files with prediction data and compute confusion matrices, precision, recall, and F-beta scores.

## Features

- Upload CSV or Excel files
- Select columns for document ID, ground truth, and predicted values
- Choose specific categories to evaluate or get overall performance
- Adjustable beta value for F-beta score
- Visual confusion matrix display
- Supports multi-category classification

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed.

1. Clone the repository
2. Install dependencies:
```bash
uv sync
```

## Usage

1. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser to the provided URL (usually http://localhost:8501)

4. Upload your data file and follow the interface to:
   - Select the appropriate columns for document ID, truth values, and predictions
   - Choose categories to evaluate (optional)
   - Set the beta value for F-beta score
   - Click "Compute Metrics" to see results

## File Structure

- `app.py` - Main Streamlit application
- `metrics.py` - Metrics computation logic
- `plots.py` - Plotting functionality
- `pyproject.toml` - Project configuration and dependencies

## Data Format

Your data file should contain at least three columns:
- Document ID column (any name)
- Ground truth/actual values column
- Predicted values column

The app will automatically detect available columns and let you select which ones to use.