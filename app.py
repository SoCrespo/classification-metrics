
import pandas as pd
import streamlit as st

from metrics import BinaryMetricsResult, compute_binary_metrics
from plots import plot_confusion_matrix

st.title('Classification Metrics App')

sidebar = st.sidebar

sidebar.write('Upload a CSV or Excel file with your predictions and ground truth.')
file = sidebar.file_uploader('Upload file', type=['csv', 'xlsx'])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    st.write('Preview:', df.head())

    columns = df.columns.tolist()
    doc_id_col = sidebar.selectbox('Select document ID column', columns)
    truth_col = sidebar.selectbox('Select ground truth column', columns)
    pred_col = sidebar.selectbox('Select predicted value column', columns)

    unique_categories = sorted(df['category'].unique()) if 'category' in df.columns else []
    selected_cats = sidebar.multiselect('Select categories to evaluate (leave empty for all)', unique_categories)
    sidebar.write("Select a beta value < 1 to penalize false positives more heavily")
    beta = sidebar.number_input('Beta value for F-beta score', min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    if sidebar.button('Compute Metrics'):
        if selected_cats:
            for cat in selected_cats:
                filtered = df[df['category'] == cat]
                result: BinaryMetricsResult = compute_binary_metrics(filtered[truth_col], filtered[pred_col], beta)
                st.subheader(f'Category: {cat}')
                col1, col2 = st.columns(2)
                with col1:
                    st.write('Confusion Matrix:')
                    fig = plot_confusion_matrix(result.confusion_matrix, [0, 1], f'Confusion Matrix: {cat}')
                    st.pyplot(fig)
                with col2:
                    st.write('Metrics:')
                    st.write({
                        'precision': result.precision,
                        'recall': result.recall,
                        f'fβ={beta} score': result.fbeta_score
                    })
        else:
            result: BinaryMetricsResult = compute_binary_metrics(df[truth_col], df[pred_col], beta)
            st.subheader('Overall Metrics')
            col1, col2 = st.columns(2)
            with col1:
                st.write('Confusion Matrix:')
                fig = plot_confusion_matrix(result.confusion_matrix, [0, 1], 'Overall Confusion Matrix')
                st.pyplot(fig)
            with col2:
                st.write('Metrics:')
                st.write({
                    'precision': result.precision,
                    'recall': result.recall,
                    f'fβ={beta} score': result.fbeta_score
                })


