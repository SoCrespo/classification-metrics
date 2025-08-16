import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from display_utils import display_matrix_and_metrics
from generate_sample import generate_sample
from scroll import scroll_to_column_config
from style import BETA_ZONE, MAIN_CSS, SIDEBAR_CSS

# Page configuration
st.set_page_config(
    page_title="AI Classifier Metrics Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(MAIN_CSS, unsafe_allow_html=True)
st.markdown("<h1 class='stTitle'> AI Classifier Metrics Dashboard</h1>", unsafe_allow_html=True)
sidebar = st.sidebar
sidebar.markdown("### 📁 Data Upload & Configuration")

# File upload 
sidebar.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

file = sidebar.file_uploader(
    'Choose your classification results file', 
    type=['csv', 'xlsx'],
    help="Upload a CSV or Excel file containing your predictions and ground truth data"
)

# Toggle button for fake data generation
sidebar.markdown("---")
button_text = "🎲 Generate fake data instead" if not st.session_state.get('show_fake_data_section', False) else "❌ Hide fake data options"
show_fake_data = sidebar.button(
    button_text,
    type="secondary",
    use_container_width=True,
    help="click to generate random sample data for testing" if not st.session_state.get('show_fake_data_section', False) else None
)

# Initialize session state for fake data visibility
if 'show_fake_data_section' not in st.session_state:
    st.session_state.show_fake_data_section = False

# Toggle the visibility when button is clicked
if show_fake_data:
    st.session_state.show_fake_data_section = not st.session_state.show_fake_data_section

# Fake data generation section (conditionally displayed)
if st.session_state.show_fake_data_section:
    sidebar.markdown("---")    
    # Input fields for fake data generation
    num_lines = sidebar.number_input(
        '📊 Number of lines',
        min_value=10,
        value=1000,
        step=1000,
        help="Number of rows to generate in the sample dataset"
    )
    
    num_categories = sidebar.number_input(
        '🏷️ Number of categories',
        min_value=2,
        max_value=20,
        value=5,
        step=1,
        help="Number of different categories to include in the dataset"
    )
    
    # Generate and load button
    generate_button = sidebar.button(
        '🎲 Generate and Load',
        type="primary",
        use_container_width=True,
        help="Generate fake data with specified parameters and load it for analysis"
    )
else:
    generate_button = False
    # Default values for when fake data section is not visible
    num_lines = 1000
    num_categories = 5

# Clear generated data button (only show if there's generated data)
if 'generated_data' in st.session_state:
    clear_button = sidebar.button(
        '🗑️ Clear Generated Data',
        type="secondary",
        use_container_width=True,
        help="Remove the currently generated data"
    )
    if clear_button:
        del st.session_state['generated_data']
        st.success("✅ Generated data cleared!")
        st.rerun()

# Handle fake data generation
if generate_button:
    with st.spinner(f'🔄 Generating fake dataset of {num_lines:,} rows with {num_categories} categories...'):
        df = generate_sample(sample_size=num_lines, nb_categories=num_categories)
        st.session_state['generated_data'] = df
        st.session_state['should_scroll_to_config'] = True

# Check if we have generated data or uploaded file
df = None
data_source = None

# Handle generated data
if 'generated_data' in st.session_state:
    df = st.session_state['generated_data']
    data_source = "Generated Data"

# Handle uploaded file
if file is not None:
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        data_source = "Uploaded File"
        # Clear any previously generated data when file is uploaded
        if 'generated_data' in st.session_state:
            del st.session_state['generated_data']
        st.session_state['should_scroll_to_config'] = True
    except Exception:
        st.error("❌ **Error processing file**")
        st.info("💡 Please ensure your data has the correct format and that columns are properly selected in Column Configuration.")
        df = None

if df is not None:
    # Column selection with enhanced UI
    sidebar.markdown("---")
    sidebar.markdown('<div id="column-config-anchor"></div>', unsafe_allow_html=True)
    sidebar.markdown("### ⚙️ Column Configuration")
    
    # Check if we should scroll to this section
    if st.session_state.get('should_scroll_to_config', False):
        scroll_to_column_config(components)
        st.session_state['should_scroll_to_config'] = False
    
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
    if category_col != 'None':
        selected_cats = sorted(df[category_col].unique()) 
    else:
        selected_cats = None


    # Beta parameter with enhanced styling
    sidebar.markdown("---")
    sidebar.markdown("### 📊 Metrics Configuration")
    sidebar.markdown(BETA_ZONE, unsafe_allow_html=True)
    
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
        if data_source == "Generated Data":
            st.markdown("""
            <div class='success-box'>
                ✅ <strong>Fake data generated successfully!</strong><br>
                <small>Sample data loaded and ready for analysis</small>
            </div>
            """, unsafe_allow_html=True)
        else:
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
                
                # Create tabs for "All Categories" plus each individual category
                tab_names = ["📈 All Categories"] + [f"📂 {cat}" for cat in selected_cats]
                tabs = st.tabs(tab_names)
                
                # First tab: All Categories (overall results)
                with tabs[0]:
                    display_matrix_and_metrics(df, truth_col, pred_col, beta, "All Categories")
                
                # Remaining tabs: Individual categories
                for i, cat in enumerate(selected_cats):
                    with tabs[i + 1]:
                        filtered = df[df[category_col] == cat]
                        display_matrix_and_metrics(filtered, truth_col, pred_col, beta, cat)
            else:
                st.markdown("## 📊 **Overall Classification Results**")
                display_matrix_and_metrics(df, truth_col, pred_col, beta)

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
