import streamlit as st
import pandas as pd

from metrics import BinaryMetricsResult, compute_binary_metrics
from plots import plot_confusion_matrix



def display_matrix_and_metrics(filtered: pd.DataFrame, truth_col: str, pred_col: str, beta: float, category: str | None = None):
    result: BinaryMetricsResult = compute_binary_metrics(filtered[truth_col], filtered[pred_col], beta)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write('### Confusion Matrix')
        message = f'Confusion Matrix: {category}' if category else 'Confusion Matrix'
        fig = plot_confusion_matrix(result.confusion_matrix, [0, 1], message)
        st.pyplot(fig)
    with col2:
        st.write('### Metrics')
        st.write(f'Precision: {result.precision:.2f}')
        st.write(f'Recall: {result.recall:.2f}')
        st.write(f'F-β score: {result.fbeta_score:.2f}')