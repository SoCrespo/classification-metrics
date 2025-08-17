MAIN_CSS = """
<style>
    .main {
        padding-top: 1rem;
    }
    
    .stTitle {
        color: #1f77b4;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    .stSubheader {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    /* Enhanced tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px !important;
        background-color: white;
        border-radius: 8px;
        border: 2px solid #e1e5e9;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        color: #2c3e50 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        min-width: 120px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border-color: #667eea !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }
</style>
"""

SIDEBAR_CSS="""
<div style='background: #f0f2f6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='margin: 0; color: #2c3e50;'>
        📤 <strong>Upload Your Data</strong><br>
        <small>Supported formats: CSV, Excel (.xlsx)</small>
    </p>
</div>
"""


BETA_ZONE = """
    <div style='background: #fff3cd; padding: 0.8rem; border-radius: 6px; border-left: 3px solid #ffc107;'>
        <small><strong>💡 Beta Parameter Guide:</strong><br>
        • β < 1: Emphasizes Precision (false positives more heavily penalised)<br>
        • β = 1: Balanced F1-Score<br>
        • β > 1: Emphasizes Recall (false negatives more heavily penalised)</small>
    </div>
    """