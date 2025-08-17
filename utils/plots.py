from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_confusion_matrix(cm, categories: list[Any]):
    """Create a professional-looking confusion matrix plot."""
    
    # Set up the figure with better styling
    plt.figure(figsize=(8, 6))
    
    # Set style for professional appearance
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'font.size': 12,
        'font.weight': 'normal',
        'axes.titleweight': 'bold',
        'axes.titlesize': 14
    })
    
    # Create the heatmap with enhanced styling
    ax = sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=categories, 
        yticklabels=categories,
        cbar=False,
        annot_kws={'size': 16, 'weight': 'bold'},
        linewidths=2,
        linecolor='white',
        square=True
    )
    
    # Enhance the plot aesthetics
    plt.xlabel('Predicted Labels', fontsize=13, fontweight='bold', labelpad=10)
    plt.ylabel('True Labels', fontsize=13, fontweight='bold', labelpad=10)
    
    # Customize tick labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontweight='bold')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, va='center', fontweight='bold')
    
    # Add percentage annotations if needed
    total = np.sum(cm)
    for i in range(len(cm)):
        for j in range(len(cm[0])):
            percentage = (cm[i][j] / total) * 100
            ax.text(j + 0.5, i + 0.7, f'({percentage:.1f}%)', 
                   horizontalalignment='center',
                   verticalalignment='center',
                   fontsize=10, 
                   color='gray',
                   fontweight='normal')
    
    # Improve layout
    plt.tight_layout()
    
    # Add a subtle border
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.5)
        spine.set_edgecolor('#cccccc')
    
    return plt.gcf()  # Return the figure for Streamlit to display
