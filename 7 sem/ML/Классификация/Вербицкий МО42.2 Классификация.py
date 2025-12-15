import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)


@dataclass
class SplitData:
    X_train: pd.DataFrame
    X_val: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_val: pd.Series
    y_test: pd.Series


def load_wine_dataset(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path, sep=';')


def make_binary_target(df: pd.DataFrame, quality_col: str = "quality", threshold: int = 7):
    if quality_col not in df.columns:
        raise ValueError(f"Колонка '{quality_col}' не найдена. Колонки: {list(df.columns)}")
    y = (df[quality_col] >= threshold).astype(int)
    X = df.drop(columns=[quality_col])
    return X, y


def print_basic_stats(df: pd.DataFrame, y: pd.Series) -> None:
    print("Размер датасета:", df.shape)
    print("Пропуски (сумма по колонкам):")
    print(df.isna().sum().sort_values(ascending=False).head(10))
    print()
    print("Распределение классов (good_wine):")
    print(y.value_counts(dropna=False))
    print("Доля класса 1:", round(float(y.mean()), 4))
    print()


def split_train_val_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    val_size_from_train: float = 0.25,
    random_state: int = 42
) -> SplitData:
    X_tmp, X_test, y_tmp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_tmp, y_tmp, test_size=val_size_from_train, random_state=random_state, stratify=y_tmp
    )
    return SplitData(
        X_train=X_train, X_val=X_val, X_test=X_test,
        y_train=y_train, y_val=y_val, y_test=y_test
    )


def build_models(random_state: int = 42):
    return {
        "logreg": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=random_state
            ))
        ]),
        "knn": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", KNeighborsClassifier(n_neighbors=15))
        ]),
        "tree": DecisionTreeClassifier(
            max_depth=6,
            min_samples_leaf=10,
            random_state=random_state
        ),
        "rf": RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1
        )
    }


def predict_scores(model, X: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    if hasattr(model, "decision_function"):
        scores = model.decision_function(X)
        return 1.0 / (1.0 + np.exp(-scores))
    raise ValueError("Модель не умеет выдавать вероятности/скоры.")


def compute_metrics(y_true: pd.Series, y_pred: np.ndarray, y_score: np.ndarray | None):
    res = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    res["roc_auc"] = roc_auc_score(y_true, y_score) if y_score is not None else np.nan
    return res


def evaluate_models(models: dict, split: SplitData, threshold: float = 0.5):
    rows = []
    fitted = {}

    for name, model in models.items():
        model.fit(split.X_train, split.y_train)
        fitted[name] = model

        y_score = predict_scores(model, split.X_test)
        y_pred = (y_score >= threshold).astype(int)

        m = compute_metrics(split.y_test, y_pred, y_score)
        cm = confusion_matrix(split.y_test, y_pred)

        rows.append({
            "model": name,
            **{k: round(v, 4) for k, v in m.items()},
            "cm": cm
        })

    results = pd.DataFrame(rows).sort_values(by="roc_auc", ascending=False)
    return results, fitted


def best_threshold_by_f1(y_true: pd.Series, y_score: np.ndarray, grid: np.ndarray | None = None):
    if grid is None:
        grid = np.linspace(0.05, 0.95, 19)

    best_t = 0.5
    best_f1 = -1.0
    f1s = []

    for t in grid:
        y_pred = (y_score >= t).astype(int)
        f = f1_score(y_true, y_pred, zero_division=0)
        f1s.append(f)
        if f > best_f1:
            best_f1 = f
            best_t = float(t)

    return best_t, np.array(grid), np.array(f1s)


def plot_f1_threshold_curve(thresholds: np.ndarray, f1s: np.ndarray, best_t: float):
    plt.figure(figsize=(8, 4))
    plt.plot(thresholds, f1s)
    plt.axvline(best_t, linestyle="--")
    plt.title("F1 в зависимости от порога")
    plt.xlabel("threshold")
    plt.ylabel("F1")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def print_confusion_matrices(results_df: pd.DataFrame):
    for _, row in results_df.iterrows():
        print(f"== {row['model']} ==")
        print(row["cm"])
        print()


if __name__ == "__main__":
    DATA_PATH = "winequality-red.csv"

    df = load_wine_dataset(DATA_PATH)
    X, y = make_binary_target(df, quality_col="quality", threshold=7)

    print_basic_stats(df, y)

    split = split_train_val_test(X, y, test_size=0.2, val_size_from_train=0.25, random_state=42)

    models = build_models(random_state=42)

    results, fitted = evaluate_models(models, split, threshold=0.5)
    print("Сравнение моделей (threshold=0.5):")
    print(results.drop(columns=["cm"]).to_string(index=False))
    print()
    print_confusion_matrices(results)

    best_model_name = results.iloc[0]["model"]
    best_model = fitted[best_model_name]
    print("Лучшая модель по ROC-AUC:", best_model_name)

    val_scores = predict_scores(best_model, split.X_val)
    best_t, grid, f1s = best_threshold_by_f1(split.y_val, val_scores)
    print("Лучший порог по F1 на val:", round(best_t, 4))

    plot_f1_threshold_curve(grid, f1s, best_t)

    test_scores = predict_scores(best_model, split.X_test)
    test_pred = (test_scores >= best_t).astype(int)
    final_metrics = compute_metrics(split.y_test, test_pred, test_scores)

    print("\nИтоговые метрики на test (с подобранным порогом):")
    for k, v in final_metrics.items():
        print(f"{k}: {v:.4f}")

    print("\nConfusion matrix (test):")
    print(confusion_matrix(split.y_test, test_pred))
