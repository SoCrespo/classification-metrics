import pandas as pd
import streamlit as st

from metrics import compute_metrics, compute_overall_metrics
from plots import plot_confusion_matrix

st.title('Classification Metrics App')

st.write('Upload a CSV or Excel file with your predictions and ground truth.')
file = st.file_uploader('Upload file', type=['csv', 'xlsx'])

if file:
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    st.write('Preview:', df.head())

    columns = df.columns.tolist()
    doc_id_col = st.selectbox('Select document ID column', columns)
    truth_col = st.selectbox('Select ground truth column', columns)
    pred_col = st.selectbox('Select predicted value column', columns)

    unique_categories = sorted(list(set(df[truth_col]) | set(df[pred_col])))
    selected_cats = st.multiselect('Select categories to evaluate (leave empty for all)', unique_categories)
    beta = st.number_input('Beta value for F-beta score', min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    if st.button('Compute Metrics'):
        if selected_cats:
            metrics = compute_metrics(df, truth_col, pred_col, selected_cats, beta)
            for cat, vals in metrics.items():
                st.subheader(f'Category: {cat}')
                st.write('Confusion Matrix:')
                st.write(pd.DataFrame(vals['confusion_matrix'], columns=['Pred 0', 'Pred 1'], index=['True 0', 'True 1']))
                st.write({k: v for k, v in vals.items() if k != 'confusion_matrix'})
        else:
            metrics = compute_overall_metrics(df, truth_col, pred_col, beta)
            st.subheader('Overall Metrics')
            st.write('Confusion Matrix:')
            st.write(pd.DataFrame(metrics['confusion_matrix']))
            st.write({k: v for k, v in metrics.items() if k != 'confusion_matrix'})

        # Plot confusion matrix for overall or first selected category
        if selected_cats:
            cat = selected_cats[0]
            fig = plot_confusion_matrix(metrics[cat]['confusion_matrix'], [0, 1], f'Confusion Matrix: {cat}')
        else:
            fig = plot_confusion_matrix(metrics['confusion_matrix'], unique_categories, 'Overall Confusion Matrix')
        st.pyplot(fig)
