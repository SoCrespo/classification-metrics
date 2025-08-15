
import pandas as pd
import streamlit as st

from display_utils import display_matrix_and_metrics

# Page configuration
st.set_page_config(
    page_title="AI Classifier Metrics Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
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
</style>
""", unsafe_allow_html=True)

# Header with emoji and better styling
st.markdown("<h1 class='stTitle'>🎯 AI Classifier Metrics Dashboard</h1>", unsafe_allow_html=True)

# Sidebar styling
sidebar = st.sidebar
sidebar.markdown("### 📁 Data Upload & Configuration")

# File upload section with better styling
sidebar.markdown("""
<div style='background: #f0f2f6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
    <p style='margin: 0; color: #2c3e50;'>
        📤 <strong>Upload Your Data</strong><br>
        <small>Supported formats: CSV, Excel (.xlsx)</small>
    </p>
</div>
""", unsafe_allow_html=True)

file = sidebar.file_uploader(
    'Choose your classification results file', 
    type=['csv', 'xlsx'],
    help="Upload a CSV or Excel file containing your predictions and ground truth data"
)

if file:
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Column selection with enhanced UI
        sidebar.markdown("---")
        sidebar.markdown("### ⚙️ Column Configuration")
        
        columns = df.columns.tolist()
        
        # Better column selectors with help text
        doc_id_col = sidebar.selectbox(
            '🔍 Document ID Column', 
            columns,
            help="Select the column containing unique identifiers for each document/sample"
        )
        
        truth_col = sidebar.selectbox(
            '✅ Ground Truth Column', 
            columns,
            help="Select the column containing the actual/true labels"
        )
        
        pred_col = sidebar.selectbox(
            '🎯 Predicted Values Column', 
            columns,
            help="Select the column containing the model's predictions"
        )
        
        category_col = sidebar.selectbox(
            '📂 Category Column (Optional)', 
            ['None'] + columns,
            help="Select a category column to analyze results by different groups"
        )

        # Category filtering with enhanced UI
        if category_col != 'None':
            unique_categories = sorted(df[category_col].unique())
            sidebar.markdown("### 🏷️ Category Filtering")
            selected_cats = sidebar.multiselect(
                'Select specific categories to analyze', 
                unique_categories,
                help="Leave empty to analyze all categories"
            )
            
            if selected_cats:
                sidebar.success(f"📊 {len(selected_cats)} categories selected")
            else:
                sidebar.info("📈 All categories will be analyzed")

        # Beta parameter with enhanced styling
        sidebar.markdown("---")
        sidebar.markdown("### 📊 Metrics Configuration")
        sidebar.markdown("""
        <div style='background: #fff3cd; padding: 0.8rem; border-radius: 6px; border-left: 3px solid #ffc107;'>
            <small><strong>💡 Beta Parameter Guide:</strong><br>
            • β < 1: Emphasizes Precision (false positives more heavily penalised)<br>
            • β = 1: Balanced F1-Score<br>
            • β > 1: Emphasizes Recall (false negatives more heavily penalised)</small>
        </div>
        """, unsafe_allow_html=True)
        
        beta = sidebar.number_input(
            '⚖️ Beta value for F-β score', 
            min_value=0.1, 
            max_value=5.0, 
            value=1.0, 
            step=0.1,
            help="Adjust the balance between precision and recall in the F-β score"
        )

        # Enhanced compute button
        compute_button = sidebar.button(
            '🚀 Compute Metrics',
            type="primary",
            use_container_width=True,
            help="Click to calculate classification metrics and generate visualizations"
        )

        if not compute_button:
            # Success message with styling - only show when compute button not clicked
            st.markdown("""
            <div class='success-box'>
                ✅ <strong>File uploaded successfully!</strong><br>
                <small>Data loaded and ready for analysis</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Data preview with enhanced styling - only show when compute button not clicked
            with st.expander("📊 **Data Preview**", expanded=True):
                st.dataframe(
                    df.head(10), 
                    use_container_width=True,
                    hide_index=True
                )
                st.caption(f"📈 Dataset contains **{len(df):,}** rows and **{len(df.columns)}** columns")

        if compute_button:
            with st.spinner('🔄 Computing classification metrics...'):
                if category_col != 'None' and selected_cats:
                    st.markdown("## 📊 **Category-wise Analysis Results**")
                    
                    # Create tabs for each category
                    tabs = st.tabs([f"📂 {cat}" for cat in selected_cats])
                    
                    for i, cat in enumerate(selected_cats):
                        with tabs[i]:
                            filtered = df[df[category_col] == cat]
                            st.caption(f"📊 Analyzing {len(filtered):,} samples in this category")
                            display_matrix_and_metrics(filtered, truth_col, pred_col, beta, cat)
                else:
                    st.markdown("## 🎯 **Overall Classification Results**")
                    st.caption(f"📊 Analyzing complete dataset with {len(df):,} samples")
                    display_matrix_and_metrics(df, truth_col, pred_col, beta)
                    
    except Exception as e:
        st.error(f"❌ **Error processing file**: {str(e)}")
        st.info("💡 Please ensure your file has the correct format and contains the expected columns.")
        
else:
    # Add description when no file is uploaded
    st.markdown("""
    <div class='info-box'>
        <strong>📊 Classification Analysis Tool</strong><br>
        Upload your classification results and get metrics analysis and visualizations.
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions when no file is uploaded
    st.markdown("""
    ## 🚀 **Get Started**
    
    To begin your classification analysis:
    
    1. **📤 Upload your data** - Use the sidebar to upload a CSV or Excel file
    2. **⚙️ Configure columns** - Select which columns contain your data
    3. **🎯 Set parameters** - Adjust the beta value for F-β score calculation
    4. **📊 Analyze results** - Click 'Compute Metrics' to see your results
    
    ---
    
    ### 📋 **Required Data Format**
    
    Your file should contain at minimum:
    - **Document ID**: Unique identifier for each sample
    - **Ground Truth**: The actual/correct labels
    - **Predictions**: Your model's predicted labels
    - **Categories** (Optional): Groups for detailed analysis
    
    ### 📈 **What You'll Get**
    
    - **🎯 Confusion Matrix** - Visual representation of prediction accuracy
    - **📊 Key Metrics** - Precision, Recall, and F-β scores
    - **📂 Category Analysis** - Detailed breakdown by different groups
    """)


