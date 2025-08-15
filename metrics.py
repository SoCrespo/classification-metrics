
import pandas as pd
from sklearn.metrics import confusion_matrix, fbeta_score, precision_score, recall_score


def compute_metrics(
    df: pd.DataFrame,
    truth_col: str,
    pred_col: str,
    categories: list[str]|None = None,
    beta: float = 1.0
) -> dict[str, dict[str, float]]:
    """
    Compute confusion matrix, precision, recall, and f-beta score for each category or overall.
    """
    results = {}
    if categories is None:
        categories = sorted(list(set(df[truth_col]) | set(df[pred_col])))
    for cat in categories:
        y_true = (df[truth_col] == cat).astype(int)
        y_pred = (df[pred_col] == cat).astype(int)
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        fbeta = fbeta_score(y_true, y_pred, beta=beta, zero_division=0)
        results[cat] = {
            'confusion_matrix': cm.tolist(),
            'precision': precision,
            'recall': recall,
            f'f{beta}_score': fbeta
        }
    return results

def compute_overall_metrics(
    df: pd.DataFrame,
    truth_col: str,
    pred_col: str,
    beta: float = 1.0
) -> dict[str, list[int]|float]:
    y_true = df[truth_col]
    y_pred = df[pred_col]
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    fbeta = fbeta_score(y_true, y_pred, beta=beta, average='macro', zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    return {
        'confusion_matrix': cm.tolist(),
        'precision': precision,
        'recall': recall,
        f'f{beta}_score': fbeta
    }
