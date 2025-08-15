
import pandas as pd
import streamlit as st

from display_utils import display_matrix_and_metrics

st.title('AI Classifier Metrics')

sidebar = st.sidebar

sidebar.write('Upload a CSV or Excel file with your predictions and ground truth.')
file = sidebar.file_uploader('Upload file', type=['csv', 'xlsx'])

if file:
    if file.name.endswith('.csv'):
        df: pd.DataFrame = pd.read_csv(file)
    else:
        df: pd.DataFrame = pd.read_excel(file)
    st.write('Preview:', df.head())

    columns = df.columns.tolist()
    doc_id_col = sidebar.selectbox('Select document ID column', columns)
    truth_col = sidebar.selectbox('Select ground truth column', columns)
    pred_col = sidebar.selectbox('Select predicted value column', columns)
    category_col = sidebar.selectbox('Select category column (if exists)', ['None'] + columns)

    unique_categories = sorted(df[category_col].unique()) if category_col != 'None' else []
    selected_cats = sidebar.multiselect('Select categories to evaluate (leave empty for all)', unique_categories)
    sidebar.write("Select a beta value < 1 to penalize false positives more heavily")
    beta = sidebar.number_input('Beta value for F-beta score', min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    if sidebar.button('Compute Metrics'):
        if selected_cats:
            for cat in selected_cats:
                filtered = df[df['category'] == cat]
                st.subheader(f'Category: {cat}')
                display_matrix_and_metrics(filtered, truth_col, pred_col, beta, cat)
        else:
            st.subheader('Overall Results')
            display_matrix_and_metrics(df, truth_col, pred_col, beta)


