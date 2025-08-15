from typing import Any, List

import matplotlib.pyplot as plt
import seaborn as sns


def plot_confusion_matrix(cm, categories: List[Any], title: str = 'Confusion Matrix'):
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=categories, yticklabels=categories)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(title)
    plt.tight_layout()
    return plt.gcf()  # Return the figure for Streamlit to display
