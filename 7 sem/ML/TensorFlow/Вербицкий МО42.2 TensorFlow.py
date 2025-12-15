import os
import time
from dataclasses import dataclass

import numpy as np
import tensorflow as tf


@dataclass
class Cfg:
    name: str
    epochs: int
    batch: int
    lr: float
    blocks: int
    base_filters: int
    dropout: float
    l2: float
    bn: bool
    aug: bool


def build_model(cfg: Cfg, input_shape, num_classes: int) -> tf.keras.Model:
    reg = tf.keras.regularizers.l2(cfg.l2) if cfg.l2 > 0 else None

    inputs = tf.keras.Input(shape=input_shape)
    x = inputs

    if cfg.aug:
        x = tf.keras.Sequential(
            [
                tf.keras.layers.RandomFlip("horizontal"),
                tf.keras.layers.RandomTranslation(0.05, 0.05),
                tf.keras.layers.RandomRotation(0.05),
            ]
        )(x)

    f = cfg.base_filters
    for _ in range(cfg.blocks):
        x = tf.keras.layers.Conv2D(f, 3, padding="same", kernel_regularizer=reg)(x)
        if cfg.bn:
            x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)

        x = tf.keras.layers.Conv2D(f, 3, padding="same", kernel_regularizer=reg)(x)
        if cfg.bn:
            x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)

        x = tf.keras.layers.MaxPooling2D(2)(x)
        if cfg.dropout > 0:
            x = tf.keras.layers.Dropout(cfg.dropout)(x)

        f *= 2

    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(256, activation="relu", kernel_regularizer=reg)(x)
    if cfg.dropout > 0:
        x = tf.keras.layers.Dropout(cfg.dropout)(x)

    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs, name=cfg.name)
    return model


def run_experiment(cfg: Cfg, x_train, y_train, x_test, y_test, class_names, root_dir: str, seed: int):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(x_train))
    val_size = int(0.1 * len(x_train))
    val_idx = idx[:val_size]
    tr_idx = idx[val_size:]

    x_tr, y_tr = x_train[tr_idx], y_train[tr_idx]
    x_val, y_val = x_train[val_idx], y_train[val_idx]

    model = build_model(cfg, input_shape=x_train.shape[1:], num_classes=len(class_names))
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=cfg.lr),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    stamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = os.path.join(root_dir, f"{cfg.name}_{stamp}")
    os.makedirs(run_dir, exist_ok=True)

    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir=os.path.join(run_dir, "tb"), histogram_freq=1),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(run_dir, "best.keras"),
            monitor="val_loss",
            save_best_only=True,
            mode="min",
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True, verbose=1),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-6, verbose=1),
    ]

    t0 = time.time()
    hist = model.fit(
        x_tr, y_tr,
        validation_data=(x_val, y_val),
        epochs=cfg.epochs,
        batch_size=cfg.batch,
        callbacks=callbacks,
        verbose=1
    )
    train_time = time.time() - t0

    loss, acc = model.evaluate(x_test, y_test, batch_size=cfg.batch, verbose=0)
    probs = model.predict(x_test, batch_size=cfg.batch, verbose=0)
    y_pred = np.argmax(probs, axis=1).astype(np.int64)
    cm = tf.math.confusion_matrix(y_test, y_pred, num_classes=len(class_names)).numpy()

    return {
        "name": cfg.name,
        "loss": float(loss),
        "accuracy": float(acc),
        "train_time_sec": float(train_time),
        "confusion_matrix": cm,
        "history": hist.history,
        "run_dir": run_dir,
    }


if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    tf.random.set_seed(seed)

    (x_tr0, y_tr0), (x_te0, y_te0) = tf.keras.datasets.cifar10.load_data()
    x = np.concatenate([x_tr0, x_te0], axis=0).astype(np.float32) / 255.0
    y = np.concatenate([y_tr0, y_te0], axis=0).reshape(-1).astype(np.int64)

    class_names = [
        "airplane", "automobile", "bird", "cat", "deer",
        "dog", "frog", "horse", "ship", "truck"
    ]

    n = len(x)
    idx = np.random.default_rng(seed).permutation(n)
    n_train = int(0.8 * n)
    train_idx = idx[:n_train]
    test_idx = idx[n_train:]

    x_train, y_train = x[train_idx], y[train_idx]
    x_test, y_test = x[test_idx], y[test_idx]

    root_dir = "runs_lab8"
    os.makedirs(root_dir, exist_ok=True)

    configs = [
        Cfg(name="baseline", epochs=8, batch=128, lr=1e-3, blocks=3, base_filters=32, dropout=0.0, l2=0.0, bn=False, aug=False),
        Cfg(name="bn_dropout", epochs=10, batch=128, lr=1e-3, blocks=3, base_filters=32, dropout=0.25, l2=1e-4, bn=True, aug=True),
        Cfg(name="deeper_l2", epochs=10, batch=128, lr=8e-4, blocks=4, base_filters=32, dropout=0.30, l2=2e-4, bn=True, aug=True),
    ]

    results = []
    for cfg in configs:
        r = run_experiment(cfg, x_train, y_train, x_test, y_test, class_names, root_dir=root_dir, seed=seed)
        results.append(r)
        print(cfg.name, "loss=", f"{r['loss']:.4f}", "acc=", f"{r['accuracy']:.4f}", "time=", f"{r['train_time_sec']:.1f}s")
        print(r["confusion_matrix"])
        print("tensorboard:", os.path.join(r["run_dir"], "tb"))

    results_sorted = sorted(results, key=lambda d: d["accuracy"], reverse=True)
    best = results_sorted[0]
    print("\nbest:", best["name"], "acc=", f"{best['accuracy']:.4f}")
    print("ideas: больше эпох, подбор lr, усилить/ослабить dropout и l2, менять глубину/фильтры, аугментация.")
