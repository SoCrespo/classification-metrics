

from dataclasses import dataclass

from sklearn.metrics import confusion_matrix, fbeta_score, precision_score, recall_score


@dataclass
class BinaryMetricsResult:
    confusion_matrix: list[list[int]]
    precision: float
    recall: float
    fbeta_score: float


def compute_binary_metrics(
    y_true,
    y_pred,
    beta: float = 1.0
) -> BinaryMetricsResult:
    """
    Compute confusion matrix, precision, recall, and f-beta score for binary classification.
    y_true and y_pred should be boolean or 0/1 arrays/Series.
    """
    cm = confusion_matrix(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    fbeta = fbeta_score(y_true, y_pred, beta=beta, zero_division=0)
    return BinaryMetricsResult(
        confusion_matrix=cm.tolist(),
        precision=precision,
        recall=recall,
        fbeta_score=fbeta
    )
