from datetime import datetime

import pandas as pd
import streamlit as st

from .logging_config import get_logger
from .metrics import BinaryMetricsResult, compute_binary_metrics
from .plots import plot_confusion_matrix

logger = get_logger(__name__)

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
    logger.info("Displaying matrix and metrics")
    with st.spinner("🔄 Calculating metrics and generating visualizations..."):
        try:
            start = datetime.now()
            logger.info("Computing metrics...")
            result: BinaryMetricsResult = compute_binary_metrics(filtered[truth_col], filtered[pred_col], beta)
            logger.info(f"Metrics computed successfully in {(datetime.now() - start).total_seconds():.2f} seconds")
        except ValueError as e:
            logger.error(f"Error computing metrics: {e}")
            st.error("❌ Error computing metrics: please ensure you have correctly configured the 'ground truth' and 'predicted' columns.")
            st.stop()
        
        # Main content in two equal columns
        metrics_column, confusion_matrix_column = st.columns([1, 1], gap="large")
        
        with confusion_matrix_column:
            
            # Styled HTML confusion matrix (2x2 grid, colored, square cells)
            logger.info("Displaying styled HTML confusion matrix")
            cm = result.confusion_matrix
            tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
            st.markdown("### Confusion Matrix")
            total = int(tn) + int(fp) + int(fn) + int(tp)
            tn_pct = f"{(tn/total*100):.1f}%" if total else "0.0%"
            fp_pct = f"{(fp/total*100):.1f}%" if total else "0.0%"
            fn_pct = f"{(fn/total*100):.1f}%" if total else "0.0%"
            tp_pct = f"{(tp/total*100):.1f}%" if total else "0.0%"
            confusion_matrix_html = f'''
            <style>
            .cm-matrix {{
                border-collapse: collapse;
                margin: 0;
                width: 100%;
                table-layout: fixed;
            }}
            .cm-matrix td {{
                width: 50%;
                aspect-ratio: 1 / 1;
                text-align: center;
                vertical-align: middle;
                font-size: 1.2rem;
                font-weight: bold;
                border: 1px solid #bbb;
                padding: 0;
                margin: 0;
                box-sizing: border-box;
            }}
            .cm-tn, .cm-tp {{ background: #eafaf1; color: #218c4a; }}
            .cm-fp, .cm-fn {{ background: #fdeaea; color: #c0392b; }}
            .cm-desc {{ font-size: 0.95rem; font-weight: 400; color: #555; margin-top: 0.3em; display: block; }}
            .cm-pct {{ font-size: 1.1rem; font-weight: 500; color: #888; display: block; margin-top: 0.1em; }}
            </style>
            <table class="cm-matrix">
                <tr>
                    <td class="cm-tn"><br>True Negative<br>{tn_pct} ({int(tn)} docs)<span class="cm-desc">Engine rejected<br>a bad document</span><br></td>
                    <td class="cm-fp"><br>False Positive<br>{fp_pct} ({int(fp)} docs)<span class="cm-desc">Engine accepted<br>a bad document</span><br></td>
                </tr>
                <tr>
                    <td class="cm-fn"><br>False Negative<br>{fn_pct} ({int(fn)} docs)<span class="cm-desc">Engine rejected<br>a good document</span><br></td>
                    <td class="cm-tp"><br>True Positive<br>{tp_pct} ({int(tp)} docs)<span class="cm-desc">Engine accepted<br>a good document</span><br></td>
                </tr>
            </table>
            '''
            st.markdown(confusion_matrix_html, unsafe_allow_html=True)
            
            # Confusion matrix interpretation
            cm = result.confusion_matrix
            tn, fp, fn, tp = cm[0][0], cm[0][1], cm[1][0], cm[1][1]
            
            
            
        
        with metrics_column:
            logger.info("Creating metrics cards")
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
            logger.info("Metrics cards created successfully")
        st.markdown("---")