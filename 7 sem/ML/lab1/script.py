import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def show_df(name, df, head_n = None):
    try:
        from caas_jupyter_tools import display_dataframe_to_user
        display_dataframe_to_user(name, df.head(head_n) if head_n else df)
    except Exception:
        print(f"\n=== {name} ===")
        print((df.head(head_n) if head_n else df).to_string())


def coerce_numeric_cols(df, cols):
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            continue
        if pd.api.types.is_numeric_dtype(out[c]):
            continue
        s = out[c].astype(str)
        s = s.str.replace("\u00A0", "", regex=False).str.replace(" ", "", regex=False)
        s = s.str.replace(",", ".", regex=False)
        s = s.str.replace(r"[^0-9\.\-eE]", "", regex=True)
        num = pd.to_numeric(s, errors="coerce")
        if num.notna().mean() >= 0.7:  
            out[c] = num
    return out


csv_path = "AA.csv"   
df = pd.read_csv(csv_path)


if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

priority_numeric = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
df = coerce_numeric_cols(df, [c for c in priority_numeric if c in df.columns])

head_df = df.head(10)
tail_df = df.tail(10)

show_df("Первые 10 строк датасета", head_df, head_n=None)
show_df("Последние 10 строк датасета", tail_df, head_n=None)


shape_info = df.shape
columns = df.columns.tolist()
nans_per_col = df.isna().sum()

overview_path = os.path.abspath("dataset_overview.txt")
with open(overview_path, "w", encoding="utf-8") as f:
    f.write("Размерность датасета: {}\n".format(shape_info))
    f.write("Столбцы: {}\n".format(columns))
    f.write("\nКоличество пропусков по столбцам:\n{}\n".format(nans_per_col.to_string()))
    if 'Date' in df.columns:
        f.write("\nДиапазон дат: {} — {}\n".format(df['Date'].min(), df['Date'].max()))

print(f"Обзор сохранён: {overview_path}")

target_col = 'Close' if 'Close' in df.columns else None
if target_col is None:
    raise ValueError("Не найден столбец 'Close' для целевой переменной.")

cols_to_drop = []
if 'Adj Close' in df.columns and target_col != 'Adj Close':
    cols_to_drop.append('Adj Close')

date_series = df['Date'] if 'Date' in df.columns else None

df_clean = df.drop(columns=cols_to_drop)

num_cols_all = df_clean.columns[df_clean.columns.isin(columns)].tolist()
df_clean = coerce_numeric_cols(df_clean, [c for c in df_clean.columns if c != 'Date'])

num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
for c in num_cols:
    median_val = df_clean[c].median()
    df_clean[c] = df_clean[c].fillna(median_val)

if date_series is not None and date_series.isna().any():
    date_series = date_series.fillna(method='ffill')

if target_col and target_col in df_clean.columns and date_series is not None and pd.api.types.is_numeric_dtype(df_clean[target_col]):
    plt.figure(figsize=(10,4))
    plt.plot(date_series, df_clean[target_col])
    plt.title("Изменение цены закрытия во времени")
    plt.xlabel("Дата")
    plt.ylabel("Close")
    plt.tight_layout()
    plt.show()


if target_col and target_col in df_clean.columns and pd.api.types.is_numeric_dtype(df_clean[target_col]):
    plt.figure(figsize=(6,4))
    plt.hist(df_clean[target_col].dropna(), bins=50)
    plt.title("Распределение цены закрытия (Close)")
    plt.xlabel("Close")
    plt.ylabel("Частота")
    plt.tight_layout()
    plt.show()

num_for_corr = df_clean.select_dtypes(include=[np.number])
if num_for_corr.shape[1] >= 2:
    plt.figure(figsize=(7,6))
    corr = num_for_corr.corr()
    im = plt.imshow(corr.values, aspect='auto')
    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Корреляционная матрица признаков")
    plt.tight_layout()
    plt.show()

if target_col is None or not pd.api.types.is_numeric_dtype(df_clean[target_col]):
    raise ValueError("Целевой столбец 'Close' не числовой — обучение невозможно.")

feature_cols = [c for c in df_clean.select_dtypes(include=[np.number]).columns if c != target_col]
if not feature_cols:
    raise ValueError("Нет числовых признаков для обучения.")

X_all = df_clean[feature_cols].copy()
y_all = df_clean[target_col].copy()

if date_series is not None:
    order = np.argsort(pd.Series(date_series).values)
else:
    order = np.arange(len(df_clean))

X_all = X_all.iloc[order].reset_index(drop=True)
y_all = y_all.iloc[order].reset_index(drop=True)
dates_sorted = None
if date_series is not None:
    dates_sorted = pd.Series(date_series).iloc[order].reset_index(drop=True)

split_idx = int(len(X_all) * 0.8)
X_train, X_test = X_all.iloc[:split_idx], X_all.iloc[split_idx:]
y_train, y_test = y_all.iloc[:split_idx], y_all.iloc[split_idx:]
if dates_sorted is not None:
    dates_train, dates_test = dates_sorted.iloc[:split_idx], dates_sorted.iloc[split_idx:]
else:
    dates_train, dates_test = None, None


linreg_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LinearRegression())
])

linreg_pipeline.fit(X_train, y_train)
y_pred_lin = linreg_pipeline.predict(X_test)

rf = RandomForestRegressor(random_state=42, n_estimators=150, n_jobs=1)  
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

def evaluate(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return rmse, r2

rmse_lin, r2_lin = evaluate(y_test, y_pred_lin)
rmse_rf, r2_rf = evaluate(y_test, y_pred_rf)

print("Оценка качества (тест):")
print(f"Линейная регрессия: RMSE={rmse_lin:.4f}, R2={r2_lin:.4f}")
print(f"Случайный лес:      RMSE={rmse_rf:.4f}, R2={r2_rf:.4f}")

plt.figure(figsize=(6,6))
plt.scatter(y_test, y_pred_lin, s=10, label="LinearRegression")
plt.scatter(y_test, y_pred_rf, s=10, label="RandomForest")
min_v = min(y_test.min(), y_pred_lin.min(), y_pred_rf.min())
max_v = max(y_test.max(), y_pred_lin.max(), y_pred_rf.max())
plt.plot([min_v, max_v], [min_v, max_v])
plt.xlabel("Фактические значения Close")
plt.ylabel("Предсказанные значения Close")
plt.title("Фактические vs предсказанные")
plt.legend()
plt.tight_layout()
plt.show()

if dates_test is not None:
    plt.figure(figsize=(10,4))
    plt.plot(dates_test, y_test.values, label="Факт")
    plt.plot(dates_test, y_pred_lin, label="LinearRegression")
    plt.plot(dates_test, y_pred_rf, label="RandomForest")
    plt.title("Предсказания на тесте во времени")
    plt.xlabel("Дата")
    plt.ylabel("Close")
    plt.legend()
    plt.tight_layout()
    plt.show()

lin_coef = linreg_pipeline.named_steps['model'].coef_
lin_features = feature_cols
coef_df = pd.DataFrame({"feature": lin_features, "coef": lin_coef}).sort_values("coef", key=abs, ascending=False)
show_df("Коэффициенты линейной регрессии", coef_df)

rf_imp = pd.DataFrame({"feature": feature_cols, "importance": rf.feature_importances_}).sort_values("importance", ascending=False)
show_df("Важности признаков (RandomForest)", rf_imp)

param_grid = {
    "n_estimators": [100, 150, 200],
    "max_depth": [None, 8, 16],
    "min_samples_leaf": [1, 2]
}
tscv = TimeSeriesSplit(n_splits=3)
gbrf = GridSearchCV(
    RandomForestRegressor(random_state=42),
    param_grid=param_grid,
    cv=tscv,
    scoring="neg_mean_squared_error",
    n_jobs=1
)
gbrf.fit(X_train, y_train)

best_rf = gbrf.best_estimator_
y_pred_best = best_rf.predict(X_test)
rmse_best, r2_best = evaluate(y_test, y_pred_best)

print("\nЛучшие гиперпараметры RF:", gbrf.best_params_)
print(f"После настройки: RMSE={rmse_best:.4f}, R2={r2_best:.4f}")

report_path = os.path.abspath("ml_stock_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("Задание: Предсказание цен на акции\n")
    f.write(f"Дата выполнения: {datetime.now()}\n\n")
    f.write(f"Размерность датасета: {shape_info}\n")
    f.write(f"Столбцы: {columns}\n\n")
    if 'Date' in df.columns:
        f.write(f"Диапазон дат: {df['Date'].min()} — {df['Date'].max()}\n\n")
    f.write("Оценка качества (тест):\n")
    f.write(f"- Линейная регрессия: RMSE={rmse_lin:.4f}, R2={r2_lin:.4f}\n")
    f.write(f"- Случайный лес:      RMSE={rmse_rf:.4f}, R2={r2_rf:.4f}\n")
    f.write("Лучшие гиперпараметры RandomForest: {}\n".format(gbrf.best_params_))
    f.write(f"После настройки: RMSE={rmse_best:.4f}, R2={r2_best:.4f}\n\n")
    f.write("Примечание: Целевая переменная — Close. Признаки масштабированы для линейной регрессии. "
            "Разделение выполнено по времени (80/20). Пропуски в числовых столбцах заполнены медианой.\n")

print(f"Отчёт сохранён: {report_path}")

import pathlib
from sklearn.model_selection import learning_curve

PLOTS_DIR = pathlib.Path("plots")
PLOTS_DIR.mkdir(exist_ok=True)

res_lin = y_test - y_pred_lin
res_rf  = y_test - y_pred_rf

plt.figure(figsize=(6,5))
plt.scatter(y_pred_lin, res_lin, s=10, label="LR")
plt.axhline(0, linestyle="--")
plt.xlabel("Fitted (LR)"); plt.ylabel("Residuals")
plt.title("Residuals vs Fitted (LinearRegression)")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "residuals_vs_fitted_lr.png", dpi=150)
plt.show()

plt.figure(figsize=(6,5))
plt.scatter(y_pred_rf, res_rf, s=10, label="RF")
plt.axhline(0, linestyle="--")
plt.xlabel("Fitted (RF)"); plt.ylabel("Residuals")
plt.title("Residuals vs Fitted (RandomForest)")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "residuals_vs_fitted_rf.png", dpi=150)
plt.show()

plt.figure(figsize=(6,4))
plt.hist(res_lin, bins=50)
plt.title("Residuals distribution (LR)")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "residuals_hist_lr.png", dpi=150)
plt.show()

plt.figure(figsize=(6,4))
plt.hist(res_rf, bins=50)
plt.title("Residuals distribution (RF)")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "residuals_hist_rf.png", dpi=150)
plt.show()

try:
    from scipy import stats
    plt.figure(figsize=(5,5))
    stats.probplot(res_lin, dist="norm", plot=plt)
    plt.title("QQ-plot residuals (LR)")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "qqplot_residuals_lr.png", dpi=150)
    plt.show()

    plt.figure(figsize=(5,5))
    stats.probplot(res_rf, dist="norm", plot=plt)
    plt.title("QQ-plot residuals (RF)")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "qqplot_residuals_rf.png", dpi=150)
    plt.show()
except Exception:
    print("SciPy недоступен — QQ-plot пропущен.")


importances_df = pd.DataFrame({
    "feature": feature_cols,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False)

plt.figure(figsize=(max(8, min(14, 0.35*len(importances_df))), 5))
plt.bar(range(len(importances_df)), importances_df["importance"])
plt.xticks(range(len(importances_df)), importances_df["feature"], rotation=90)
plt.title("Feature importances (RandomForest)")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "rf_feature_importances.png", dpi=150)
plt.show()

TOP_N = min(6, len(importances_df))  
top_feats = importances_df["feature"].iloc[:TOP_N].tolist()
try:
    from pandas.plotting import scatter_matrix
    sm_df = pd.concat([X_all[top_feats], y_all.rename("Target")], axis=1)
    axes = scatter_matrix(sm_df, figsize=(1.8*TOP_N, 1.8*TOP_N), diagonal='hist')
    
    plt.suptitle("Scatter Matrix (top features + target)", y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "scatter_matrix_top_features.png", dpi=150, bbox_inches="tight")
    plt.show()
except Exception as e:
    print(f"Scatter matrix не построен: {e}")


tscv_lc = TimeSeriesSplit(n_splits=3)
train_sizes, train_scores, val_scores = learning_curve(
    estimator=RandomForestRegressor(random_state=42, n_estimators=150, n_jobs=1),
    X=X_train, y=y_train,
    cv=tscv_lc,
    train_sizes=np.linspace(0.2, 1.0, 5),
    scoring="neg_mean_squared_error",
    n_jobs=1
)
train_rmse = np.sqrt(-train_scores.mean(axis=1))
val_rmse   = np.sqrt(-val_scores.mean(axis=1))

plt.figure(figsize=(7,4))
plt.plot(train_sizes, train_rmse, marker="o", label="Train RMSE")
plt.plot(train_sizes, val_rmse, marker="o", label="CV RMSE")
plt.xlabel("Train size"); plt.ylabel("RMSE")
plt.title("Learning Curve (RandomForest, TimeSeriesSplit)")
plt.legend()
plt.tight_layout()
plt.savefig(PLOTS_DIR / "learning_curve_rf.png", dpi=150)
plt.show()

preds_df = pd.DataFrame({
    "index": y_test.index,
    "y_true": y_test.values,
    "y_pred_lin": y_pred_lin,
    "y_pred_rf": y_pred_rf
})
if dates_sorted is not None:
    preds_df["date"] = dates_test.values
preds_df = preds_df[["date","y_true","y_pred_lin","y_pred_rf"]] if "date" in preds_df.columns else preds_df[["index","y_true","y_pred_lin","y_pred_rf"]]
preds_csv = os.path.abspath("predictions.csv")
preds_df.to_csv(preds_csv, index=False)
print(f"Предсказания сохранены: {preds_csv}")

print(f"Папка с графиками: {PLOTS_DIR.resolve()}")
