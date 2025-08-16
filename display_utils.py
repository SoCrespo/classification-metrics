import pandas as pd
import streamlit as st

from metrics import BinaryMetricsResult, compute_binary_metrics
from plots import plot_confusion_matrix


def create_metric_card(title: str, value: float | int, color: str, description: str = "", format_as_percentage: bool = False):
    """Create a professional metric card with styling."""
    # Format value based on type and percentage preference
    if isinstance(value, int):
        formatted_value = f"{value:,}"
    elif format_as_percentage:
        formatted_value = f"{value * 100:.1f}%"
    else:
        formatted_value = f"{value:.3f}"
    
    return f"""
    <div style='
        background: linear-gradient(135deg, {color}20, {color}10);
        border: 1px solid {color}40;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    '>
        <div style='color: #2c3e50; font-size: 1rem; font-weight: 600; margin-bottom: 0.3rem;'>
            {title}
        </div>
        <div style='color: {color}; font-size: 2.2rem; font-weight: bold; margin-bottom: 0.3rem;'>
            {formatted_value}
        </div>
        <div style='color: #7f8c8d; font-size: 0.85rem; line-height: 1.3;'>
            {description}
        </div>
    </div>
    """


def display_matrix_and_metrics(filtered: pd.DataFrame, truth_col: str, pred_col: str, beta: float, category: str | None = None):
    """Display confusion matrix and metrics with enhanced professional styling."""
    
    try:
        result: BinaryMetricsResult = compute_binary_metrics(filtered[truth_col], filtered[pred_col], beta)
    except ValueError as e:
        st.error(f"❌ Error computing metrics: please ensure you have correctly configured the 'ground truth' and 'predicted' columns.")
        st.stop()
    # Main content in two equal columns
    col2, col1 = st.columns([1, 1], gap="large")
    
    with col1:
        
        # Enhanced confusion matrix
        fig = plot_confusion_matrix(result.confusion_matrix, [0, 1])
        st.pyplot(fig, use_container_width=True)
        
        # Confusion matrix interpretation
        cm = result.confusion_matrix
        tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
        
        st.markdown("### 📋 **Matrix Breakdown**")
        
        # Create a small interpretation table
        matrix_data = {
            "Metric": ["True Negatives (TN)", "False Positives (FP)", "False Negatives (FN)", "True Positives (TP)"],
            "Count": [int(tn), int(fp), int(fn), int(tp)],
            "Description": [
                "Correctly rejected (predicted as wrong category)",
                "Incorrectly accepted (predicted as good category)", 
                "Incorrectly rejected (predicted as wrong category)",
                "Correctly accepted (predicted as good category)"
            ]
        }
        
        matrix_df = pd.DataFrame(matrix_data)
        st.dataframe(
            matrix_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Metric": st.column_config.TextColumn("Metric", width="medium"),
                "Count": st.column_config.NumberColumn("Count", width="small"),
                "Description": st.column_config.TextColumn("Description", width="large")
            }
        )
    
    with col2:
        
        # Sample count card (full width)
        total_samples = len(filtered)
        accuracy = (tp + tn) / total_samples
        
        sample_count_html = create_metric_card(
            "Sample Count", 
            total_samples, 
            "#34495e",
            "Total number of samples analyzed"
        )
        st.markdown(sample_count_html, unsafe_allow_html=True)
        
        # 2x2 grid of metric cards
        metric_col1, metric_col2 = st.columns(2, gap="small")
        
        with metric_col1:
            accuracy_html = create_metric_card(
                "Accuracy", 
                accuracy, 
                "#f39c12",
                "Correctly classified",
                format_as_percentage=True
            )
            st.markdown(accuracy_html, unsafe_allow_html=True)
            
            recall_html = create_metric_card(
                "Recall", 
                result.recall, 
                "#3498db", 
                "Of actual positives found",
                format_as_percentage=True
            )
            st.markdown(recall_html, unsafe_allow_html=True)
        
        with metric_col2:
            precision_html = create_metric_card(
                "Precision", 
                result.precision, 
                "#2ecc71",
                "Of predicted positives correct",
                format_as_percentage=True
            )
            st.markdown(precision_html, unsafe_allow_html=True)
            
            fbeta_html = create_metric_card(
                f"F{beta:.1f}-Score", 
                result.fbeta_score, 
                "#9b59b6",
                f"Balanced metric (β={beta:.1f})",
                format_as_percentage=True
            )
            st.markdown(fbeta_html, unsafe_allow_html=True)
    
    st.markdown("---")