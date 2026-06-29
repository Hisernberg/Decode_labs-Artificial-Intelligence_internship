"""
DecodeLabs | AI Industrial Training Kit (Batch 2026)
Project 2  :  Data Classification Using AI

This is the "predictive phase". Instead of writing explicit rules
(Project 1), we provide history (labelled data) and let the machine
DERIVE the logic. This is Supervised Learning.

Pipeline (IPO Framework, straight from the briefing):
    INPUT    -> Iris dataset  +  Feature scaling (StandardScaler)
    PROCESS  -> Train-Test split (80/20, shuffled)  +  KNN algorithm
    OUTPUT   -> Confusion matrix  +  Precision / Recall / F1 score

Why we don't trust accuracy alone:
    "In imbalanced data, accuracy is a lie."  -> we look at the
    confusion matrix and the F1 score (the harmonic mean of
    precision and recall) instead.

Author : <YOUR NAME>     Role: AI Intern @ DecodeLabs     Week: 2
"""

import matplotlib
matplotlib.use("Agg")  # headless backend so plots save anywhere (Kaggle/CI)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    f1_score,
)

RANDOM_STATE = 42   # fixed seed -> reproducible results
TEST_SIZE = 0.20    # 80% train / 20% test  (the "structural split")
DEFAULT_K = 5       # K-Nearest Neighbors, K=5 as in the briefing


# ---------------------------------------------------------------------------
# PHASE 1 (INPUT) — Load and understand the data
# ---------------------------------------------------------------------------
def load_and_explore():
    """Load the Iris benchmark and print a quick summary."""
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name="species")

    print("=" * 60)
    print("PHASE 1 — INPUT: Understanding the data")
    print("=" * 60)
    print(f"Samples      : {X.shape[0]}")
    print(f"Features     : {X.shape[1]}  -> {list(X.columns)}")
    print(f"Classes      : {len(iris.target_names)} -> {list(iris.target_names)}")
    print(f"Balance      : {y.value_counts().to_dict()}  (50 each = balanced)")
    print("\nFirst 5 rows:")
    print(X.head().to_string())
    print()
    return X, y, iris.target_names


# ---------------------------------------------------------------------------
# PHASE 1 (INPUT) — Feature scaling (the "gatekeeper rule")
# ---------------------------------------------------------------------------
def split_and_scale(X, y):
    """
    Split FIRST, then scale. The scaler is fit ONLY on the training
    data so the test set stays a true unseen "locked vault" — no
    information leaks from test into training.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        shuffle=True,        # remove order bias
        stratify=y,          # keep class balance in both sets
    )

    scaler = StandardScaler()                 # mean = 0, variance = 1
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)  # reuse train statistics

    print("=" * 60)
    print("PHASE 2 — PROCESS: Split & scale")
    print("=" * 60)
    print(f"Training samples : {len(X_train)}  ({int((1-TEST_SIZE)*100)}%)")
    print(f"Testing samples  : {len(X_test)}  ({int(TEST_SIZE*100)}%)")
    print("Features scaled with StandardScaler (fit on train only).\n")
    return X_train_scaled, X_test_scaled, y_train, y_test


# ---------------------------------------------------------------------------
# PHASE 2 (PROCESS) — Tune K with the elbow method
# ---------------------------------------------------------------------------
def find_best_k(X_train, y_train, X_test, y_test, k_range=range(1, 26),
                save_path="elbow_plot.png"):
    """
    Try a range of K values and plot the error rate.
    Too small K (1-2) -> noise / overfitting.  Too big K -> underfitting.
    The "elbow" is the sweet spot.

    We PLOT the full range (so both bad extremes are visible), but we
    SELECT only from the stable zone: odd K >= 3. Odd K avoids tie votes,
    and skipping K=1/2 avoids the overfitting trap the briefing warns about.
    """
    error_rates = []
    for k in k_range:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        error_rates.append(np.mean(preds != y_test))

    # Selection pool: odd K, K >= 3
    candidates = [(k, e) for k, e in zip(k_range, error_rates)
                  if k >= 3 and k % 2 == 1]
    best_k = min(candidates, key=lambda pair: (pair[1], pair[0]))[0]

    plt.figure(figsize=(9, 5))
    plt.plot(list(k_range), error_rates, marker="o", linestyle="-")
    plt.axvline(best_k, color="orange", linestyle="--",
                label=f"Chosen K = {best_k}")
    plt.title("Tuning the Engine: Choosing K (Elbow Method)")
    plt.xlabel("K value")
    plt.ylabel("Error rate")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close()

    print(f"Elbow method -> chosen K = {best_k}  "
          f"(odd, K>=3; plot saved: {save_path})\n")
    return best_k


# ---------------------------------------------------------------------------
# PHASE 2/3 — Train the final model and validate the output
# ---------------------------------------------------------------------------
def train_and_evaluate(X_train, y_train, X_test, y_test, target_names,
                       k=DEFAULT_K, save_path="confusion_matrix.png"):
    """The scikit-learn workflow: instantiate -> fit -> predict -> score."""
    model = KNeighborsClassifier(n_neighbors=k)   # INSTANTIATE
    model.fit(X_train, y_train)                   # FIT  (memorize the map)
    predictions = model.predict(X_test)           # PREDICT (apply logic)

    acc = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")

    print("=" * 60)
    print(f"PHASE 3 — OUTPUT: Validation  (K = {k})")
    print("=" * 60)
    print(f"Accuracy  : {acc:.3f}")
    print(f"Macro F1  : {macro_f1:.3f}   (accuracy alone can be a mirage)")
    print("\nClassification report (precision / recall / F1 per class):")
    print(classification_report(y_test, predictions,
                                target_names=target_names))

    # Confusion matrix heatmap
    cm = confusion_matrix(y_test, predictions)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=target_names, yticklabels=target_names)
    plt.title(f"Confusion Matrix (KNN, K={k})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(save_path, dpi=120)
    plt.close()
    print(f"Confusion matrix saved: {save_path}")

    return model, acc, macro_f1


def main():
    X, y, target_names = load_and_explore()
    X_train, X_test, y_train, y_test = split_and_scale(X, y)
    best_k = find_best_k(X_train, y_train, X_test, y_test)
    # Train with the briefing's K=5, then also report the tuned K.
    train_and_evaluate(X_train, y_train, X_test, y_test, target_names,
                       k=DEFAULT_K)
    if best_k != DEFAULT_K:
        print("\n--- Re-running with the elbow-optimal K ---\n")
        train_and_evaluate(X_train, y_train, X_test, y_test, target_names,
                           k=best_k, save_path="confusion_matrix_bestk.png")

    print("\nDone. White-box, traceable, reproducible. 🌸")


if __name__ == "__main__":
    main()
