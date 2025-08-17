import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from utils.display_utils import display_matrix_and_metrics
from utils.generate_sample import generate_sample
from utils.logging_config import get_logger, setup_logging
from utils.scroll import scroll_to_column_config
from utils.style import BETA_ZONE, MAIN_CSS, SIDEBAR_CSS

# Set up centralized logging configuration
setup_logging()
logger = get_logger(__name__)



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
    logger.info("Toggling fake data section visibility")
    st.session_state.show_fake_data_section = not st.session_state.show_fake_data_section

# Fake data generation section (conditionally displayed)
if st.session_state.show_fake_data_section:
    sidebar.markdown("---")    
    # Input fields for fake data generation
    num_lines = sidebar.number_input(
        '📊 Number of lines',
        min_value=10,
        max_value=1_000_000,
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
    logger.info(f"Generating fake dataset with {num_lines:,} rows and {num_categories} categories")
    with st.spinner(f'🔄 Generating fake dataset of {num_lines:,} rows with {num_categories} categories...'):
        df = generate_sample(sample_size=num_lines, nb_categories=num_categories)
        st.session_state['generated_data'] = df
        st.session_state['should_scroll_to_config'] = True
    logger.info("Fake data generated successfully")

# Check if we have generated data or uploaded file
df = None
data_source = None

# Handle generated data
if 'generated_data' in st.session_state:
    df = st.session_state['generated_data']
    data_source = "Generated Data"

# Handle uploaded file
if file is not None:
    logger.info(f"Processing uploaded file: {file.name}")
    try:
        if file.name.endswith('.csv'):
            logger.info("Reading CSV file")
            df = pd.read_csv(file)
        else:
            logger.info("Reading Excel file")
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

    if not compute_button and not st.session_state.get('metrics_computed', False):
        # Success message with styling - only show when compute button not clicked and metrics not computed
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
        
        # Data preview with enhanced styling - only show when compute button not clicked and metrics not computed
        with st.expander("📊 **Data Preview**", expanded=True):
            st.dataframe(
                df.head(10), 
                use_container_width=True,
                hide_index=True
            )
            st.caption(f"📈 Dataset contains **{len(df):,}** rows and **{len(df.columns)}** columns")

    if compute_button:
        # Store computed state in session
        logger.info("Computing metrics...")
        st.session_state['metrics_computed'] = True
        st.session_state['df_computed'] = df
        st.session_state['truth_col_computed'] = truth_col
        st.session_state['pred_col_computed'] = pred_col
        st.session_state['beta_computed'] = beta
        st.session_state['category_col_computed'] = category_col
        st.session_state['selected_cats_computed'] = selected_cats

    # Show results if metrics have been computed
    if st.session_state.get('metrics_computed', False):

        # Get the stored values
        df_stored = st.session_state['df_computed']
        truth_col_stored = st.session_state['truth_col_computed']
        logger.info(f"Using ground truth column: {truth_col_stored}")
        pred_col_stored = st.session_state['pred_col_computed']
        logger.info(f"Using predicted column: {pred_col_stored}")
        beta_stored = st.session_state['beta_computed']
        logger.info(f"Using beta value: {beta_stored}")
        category_col_stored = st.session_state['category_col_computed']
        logger.info(f"Using category column: {category_col_stored}")
        selected_cats_stored = st.session_state['selected_cats_computed']
        logger.info(f"Selected categories: {selected_cats_stored}")
        
        if category_col_stored != 'None' and selected_cats_stored:
            st.markdown("## 📊 **Category-wise Analysis Results**")
            
            # Create a selectbox for category selection
            category_options = ["📈 All Categories"] + [f"📂 {cat}" for cat in selected_cats_stored]
            selected_category = st.selectbox(
                "🔍 **Select Category to Analyze:**",
                options=category_options,
                index=0,
                help="Choose which category to analyze. Select 'All Categories' for overall results.",
                key="category_selector"
            )
            logger.info(f"Selected category for analysis: {selected_category}")
            # Display results based on selection
            if selected_category == "📈 All Categories":
                display_matrix_and_metrics(df_stored, truth_col_stored, pred_col_stored, beta_stored, "All Categories")
            else:
                # Extract category name (remove emoji prefix)
                cat_name = selected_category.replace("📂 ", "")
                filtered = df_stored[df_stored[category_col_stored] == cat_name]
                display_matrix_and_metrics(filtered, truth_col_stored, pred_col_stored, beta_stored, cat_name)
        else:
            st.markdown("## 📊 **Overall Classification Results**")
            display_matrix_and_metrics(df_stored, truth_col_stored, pred_col_stored, beta_stored)

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
