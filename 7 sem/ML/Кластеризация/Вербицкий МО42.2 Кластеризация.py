import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler


def find_col(df, keys):
    for k in keys:
        k = str(k).lower().strip()
        for c in df.columns:
            if k in str(c).lower():
                return c
    return None


def kde_xy(values, points=300, bandwidth=None):
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size < 2:
        return None, None

    x_min, x_max = float(v.min()), float(v.max())
    if x_min == x_max:
        x_min -= 1.0
        x_max += 1.0

    grid = np.linspace(x_min, x_max, points)

    n = v.size
    std = float(np.std(v, ddof=1)) if n > 1 else float(np.std(v))
    if bandwidth is None:
        if std < 1e-12:
            bandwidth = 1.0
        else:
            bandwidth = 1.06 * std * (n ** (-1.0 / 5.0))
            bandwidth = max(float(bandwidth), 1e-3)

    diffs = (grid[:, None] - v[None, :]) / bandwidth
    dens = np.mean(np.exp(-0.5 * diffs * diffs), axis=1) / (bandwidth * np.sqrt(2.0 * np.pi))
    return grid, dens


def kmeans_grid(X, k_list, init_list, n_init_list, max_iter_list, random_state=42):
    rows = []
    for k in k_list:
        for init in init_list:
            for n_init in n_init_list:
                for max_iter in max_iter_list:
                    km = KMeans(
                        n_clusters=k,
                        init=init,
                        n_init=n_init,
                        max_iter=max_iter,
                        random_state=random_state,
                    )
                    labels = km.fit_predict(X)

                    sil = np.nan
                    dbi = np.nan
                    if k >= 2 and len(np.unique(labels)) > 1:
                        sil = float(silhouette_score(X, labels))
                        dbi = float(davies_bouldin_score(X, labels))

                    rows.append(
                        {
                            "k": k,
                            "init": init,
                            "n_init": n_init,
                            "max_iter": max_iter,
                            "inertia": float(km.inertia_),
                            "silhouette": sil,
                            "davies_bouldin": dbi,
                        }
                    )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = pd.read_csv("Customers.csv")

    gender_col = find_col(df, ["gender", "пол"])
    age_col = find_col(df, ["age", "возраст"])
    income_col = find_col(df, ["annual income", "income", "доход"])
    spending_col = find_col(df, ["spending score", "spending", "траты", "оценка трат"])

    if any(c is None for c in [gender_col, age_col, income_col, spending_col]):
        raise ValueError(f"Не удалось определить ключевые столбцы. Столбцы: {df.columns.tolist()}")

    print("\n1) head(10):")
    print(df.head(10))
    print("\n1) tail(10):")
    print(df.tail(10))

    print("\n2) describe():")
    print(df.describe())
    print("\n2) describe(include='all'):")
    print(df.describe(include="all"))

    print("\n3) info():")
    df.info(memory_usage="deep")

    counts = df[gender_col].value_counts(dropna=False)

    plt.figure(figsize=(7, 4))
    plt.title("Гендерное распределение (столбиковая диаграмма)")
    plt.bar(counts.index.astype(str), counts.values)
    plt.xlabel("Пол")
    plt.ylabel("Количество")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.title("Гендерное распределение (круговая диаграмма)")
    plt.pie(counts.values, labels=counts.index.astype(str), autopct="%1.1f%%", startangle=90)
    plt.tight_layout()
    plt.show()

    ages = pd.to_numeric(df[age_col], errors="coerce").dropna()

    plt.figure(figsize=(7, 4))
    plt.title("Распределение возрастов (гистограмма)")
    plt.hist(ages, bins="auto")
    plt.xlabel("Возраст")
    plt.ylabel("Количество")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(5, 5))
    plt.title("Возраст (ящик с усами)")
    plt.boxplot(ages.values, vert=True)
    plt.ylabel("Возраст")
    plt.tight_layout()
    plt.show()

    inc = pd.to_numeric(df[income_col], errors="coerce").dropna()

    plt.figure(figsize=(7, 4))
    plt.title("Годовой доход (гистограмма)")
    plt.hist(inc, bins="auto")
    plt.xlabel("Доход")
    plt.ylabel("Количество")
    plt.tight_layout()
    plt.show()

    xk, dk = kde_xy(inc.values)
    plt.figure(figsize=(7, 4))
    plt.title("Годовой доход (график плотности)")
    if xk is not None:
        plt.plot(xk, dk)
    plt.xlabel("Доход")
    plt.ylabel("Плотность")
    plt.tight_layout()
    plt.show()

    spend = pd.to_numeric(df[spending_col], errors="coerce")

    plt.figure(figsize=(7, 4))
    plt.title("Оценка трат (гистограмма)")
    plt.hist(spend.dropna(), bins="auto")
    plt.xlabel("Spending Score")
    plt.ylabel("Количество")
    plt.tight_layout()
    plt.show()

    xs, ds = kde_xy(spend.dropna().values)
    plt.figure(figsize=(7, 4))
    plt.title("Оценка трат (график плотности)")
    if xs is not None:
        plt.plot(xs, ds)
    plt.xlabel("Spending Score")
    plt.ylabel("Плотность")
    plt.tight_layout()
    plt.show()

    grouped = []
    labels_g = []
    for g, sub in df.groupby(gender_col):
        v = pd.to_numeric(sub[spending_col], errors="coerce").dropna().values
        if v.size:
            grouped.append(v)
            labels_g.append(str(g))

    plt.figure(figsize=(7, 4))
    plt.title("Оценка трат по полу (boxplot)")
    if grouped:
        plt.boxplot(grouped, labels=labels_g)
    plt.xlabel("Пол")
    plt.ylabel("Spending Score")
    plt.tight_layout()
    plt.show()

    age_num = pd.to_numeric(df[age_col], errors="coerce")
    inc_num = pd.to_numeric(df[income_col], errors="coerce")
    sp_num = pd.to_numeric(df[spending_col], errors="coerce")

    m = inc_num.notna() & sp_num.notna()
    plt.figure(figsize=(7, 5))
    plt.title("Доход vs Оценка трат")
    plt.scatter(inc_num[m], sp_num[m], s=18, alpha=0.85)
    plt.xlabel("Доход")
    plt.ylabel("Spending Score")
    plt.tight_layout()
    plt.show()

    m = age_num.notna() & sp_num.notna()
    plt.figure(figsize=(7, 5))
    plt.title("Возраст vs Оценка трат")
    plt.scatter(age_num[m], sp_num[m], s=18, alpha=0.85)
    plt.xlabel("Возраст")
    plt.ylabel("Spending Score")
    plt.tight_layout()
    plt.show()

    num_df = df.select_dtypes(include=[np.number]).copy()
    if not num_df.empty:
        corr = num_df.corr(numeric_only=True)
        plt.figure(figsize=(7, 6))
        plt.title("Корреляции (тепловая карта)")
        plt.imshow(corr.values, aspect="auto")
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.index)), corr.index)
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    feat = df[[age_col, income_col, spending_col]].copy()
    feat = feat.apply(pd.to_numeric, errors="coerce").dropna()

    scaler = StandardScaler()
    X = scaler.fit_transform(feat.values)

    k_list = list(range(2, 11))
    init_list = ["k-means++", "random"]
    n_init_list = [10, 20]
    max_iter_list = [300, 500]

    res = kmeans_grid(X, k_list, init_list, n_init_list, max_iter_list, random_state=42)

    print("\n8) Топ-10 конфигураций по silhouette:")
    top = res.dropna(subset=["silhouette"]).sort_values(
        ["silhouette", "davies_bouldin", "inertia", "k"],
        ascending=[False, True, True, True],
    ).head(10)
    print(top.to_string(index=False))

    if top.empty:
        raise RuntimeError("Не получилось посчитать silhouette. Попробуйте другой диапазон k или проверьте данные.")

    best = top.iloc[0]
    best_k = int(best["k"])
    best_init = str(best["init"])
    best_n_init = int(best["n_init"])
    best_max_iter = int(best["max_iter"])

    best_per_k = []
    for k in k_list:
        sub = res[res["k"] == k].copy()
        sub2 = sub.dropna(subset=["silhouette"])
        if not sub2.empty:
            sub2 = sub2.sort_values(["silhouette", "davies_bouldin", "inertia"], ascending=[False, True, True])
            best_per_k.append(sub2.iloc[0])
        else:
            sub = sub.sort_values("inertia", ascending=True)
            best_per_k.append(sub.iloc[0])
    best_per_k = pd.DataFrame(best_per_k).sort_values("k")

    plt.figure(figsize=(7, 4))
    plt.title("Метод локтя: inertia по k")
    plt.plot(best_per_k["k"], best_per_k["inertia"], marker="o")
    plt.xlabel("k")
    plt.ylabel("inertia")
    plt.xticks(best_per_k["k"])
    plt.tight_layout()
    plt.show()

    if best_per_k["silhouette"].notna().any():
        plt.figure(figsize=(7, 4))
        plt.title("Silhouette по k")
        plt.plot(best_per_k["k"], best_per_k["silhouette"], marker="o")
        plt.xlabel("k")
        plt.ylabel("silhouette")
        plt.xticks(best_per_k["k"])
        plt.tight_layout()
        plt.show()

    km = KMeans(
        n_clusters=best_k,
        init=best_init,
        n_init=best_n_init,
        max_iter=best_max_iter,
        random_state=42,
    )
    cl = km.fit_predict(X)

    centers_orig = scaler.inverse_transform(km.cluster_centers_)

    plt.figure(figsize=(7, 5))
    plt.title("Кластеры: Доход vs Оценка трат")
    plt.scatter(feat[income_col], feat[spending_col], c=cl, s=18, alpha=0.85)
    plt.scatter(centers_orig[:, 1], centers_orig[:, 2], s=220, marker="X", edgecolors="black", linewidths=1.0)
    plt.xlabel("Доход")
    plt.ylabel("Spending Score")
    plt.tight_layout()
    plt.show()

    pca = PCA(n_components=2, random_state=42)
    Xp = pca.fit_transform(X)
    Cp = pca.transform(km.cluster_centers_)

    plt.figure(figsize=(7, 5))
    plt.title("Кластеры (PCA 2D)")
    plt.scatter(Xp[:, 0], Xp[:, 1], c=cl, s=18, alpha=0.85)
    plt.scatter(Cp[:, 0], Cp[:, 1], s=220, marker="X", edgecolors="black", linewidths=1.0)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.tight_layout()
    plt.show()

    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("Кластеры (3D): Возраст, Доход, Траты")
    ax.scatter(
        feat[age_col].values,
        feat[income_col].values,
        feat[spending_col].values,
        c=cl,
        s=18,
        alpha=0.85,
    )
    ax.scatter(
        centers_orig[:, 0],
        centers_orig[:, 1],
        centers_orig[:, 2],
        s=260,
        marker="X",
        edgecolors="black",
        linewidths=1.0,
    )
    ax.set_xlabel(age_col)
    ax.set_ylabel(income_col)
    ax.set_zlabel(spending_col)
    plt.tight_layout()
    plt.show()
