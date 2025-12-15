import argparse
import glob
import json
import sys
import time
from pathlib import Path

import numpy as np


def parse_args():
    p = argparse.ArgumentParser(description="ЛР9: YOLO (Ultralytics) — детекция, пороги, видео/камера, сравнение, grid, COCO метрики")
    p.add_argument("--out", default="runs/lab9", help="Папка для результатов")

    p.add_argument("--images", nargs="*", default=None, help="Список путей или glob-шаблоны (например data/*.jpg)")
    p.add_argument("--video", default=None, help="Путь к видеофайлу")
    p.add_argument("--webcam", action="store_true", help="Обработка веб-камеры")
    p.add_argument("--cam_index", type=int, default=0, help="Индекс камеры")

    p.add_argument("--model", default="yolov8n.pt", help="Веса модели для основных запусков")
    p.add_argument("--compare_models", nargs="*", default=["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"], help="Модели для сравнения")

    p.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    p.add_argument("--iou", type=float, default=0.7, help="IoU threshold (NMS)")
    p.add_argument("--imgsz", type=int, default=640, help="Размер входа (imgsz)")

    p.add_argument("--conf_list", nargs="*", type=float, default=[0.10, 0.25, 0.40, 0.60], help="Список conf для эксперимента")
    p.add_argument("--iou_list", nargs="*", type=float, default=[0.50, 0.70, 0.85], help="Список iou для grid")
    p.add_argument("--imgsz_list", nargs="*", type=int, default=[416, 640, 960], help="Список imgsz для grid")
    p.add_argument("--repeats", type=int, default=5, help="Повторы замера времени")

    p.add_argument("--coco_ann", default=None, help="COCO json (instances_*.json)")
    p.add_argument("--coco_images", default=None, help="Папка с изображениями COCO")
    p.add_argument("--max_coco_images", type=int, default=0, help="Ограничение на число COCO изображений (0 = без ограничения)")
    p.add_argument("--pr_classes", nargs="*", default=["person", "car", "bicycle"], help="Классы для PR-кривых (по именам COCO)")

    p.add_argument("--install", action="store_true", help="Попытаться установить зависимости через pip")
    p.add_argument("--show", action="store_true", help="Показывать окно OpenCV (видео/камера)")
    p.add_argument("--all", action="store_true", help="Запустить весь набор пунктов (если заданы входные данные)")
    return p.parse_args()


def ensure_packages(required, optional, auto_install: bool, strict_optional: bool):
    def pip_install(pkg: str):
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

    def need(mod: str, pkg: str, is_optional: bool):
        try:
            __import__(mod)
            return True
        except Exception:
            if auto_install:
                try:
                    pip_install(pkg)
                    __import__(mod)
                    return True
                except Exception:
                    return False

            if is_optional and not strict_optional:
                return False

            print(f"Отсутствует пакет: {pkg}")
            print(f"Установка: {sys.executable} -m pip install {pkg}")
            return False

    ok = True
    for mod, pkg in required:
        if not need(mod, pkg, is_optional=False):
            ok = False

    for mod, pkg in optional:
        present = need(mod, pkg, is_optional=True)
        if strict_optional and not present:
            ok = False

    if not ok:
        sys.exit(1)


def pick_images(images_arg):
    if not images_arg:
        try:
            from ultralytics.utils import ASSETS
            base = Path(ASSETS)
            found = []
            for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp"):
                found.extend([str(p) for p in base.glob(ext)])
            found = sorted(found)
            return found[:3]
        except Exception:
            return []

    out = []
    for it in images_arg:
        if any(ch in it for ch in ["*", "?", "[", "]"]):
            out.extend(glob.glob(it))
        else:
            out.append(it)

    out = [p for p in out if Path(p).exists()]
    out = list(dict.fromkeys(out))
    return sorted(out)


def run_predict(model, sources, conf: float, iou: float, imgsz: int):
    return model.predict(source=sources, conf=conf, iou=iou, imgsz=imgsz, verbose=False)


def save_image_results(results, image_paths, out_dir: Path, tag: str):
    import cv2
    import pandas as pd

    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for img_path, r in zip(image_paths, results):
        stem = Path(img_path).stem
        out_img = out_dir / f"{stem}_{tag}.jpg"
        cv2.imwrite(str(out_img), r.plot())

        if r.boxes is None or len(r.boxes) == 0:
            rows.append({"image": str(img_path), "class": None, "confidence": None, "x1": None, "y1": None, "x2": None, "y2": None})
            continue

        names = r.names
        xyxy = r.boxes.xyxy.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        clss = r.boxes.cls.cpu().numpy().astype(int)

        for b, sc, c in zip(xyxy, confs, clss):
            x1, y1, x2, y2 = [float(v) for v in b.tolist()]
            c = int(c)
            rows.append({
                "image": str(img_path),
                "class": names.get(c, str(c)),
                "confidence": float(sc),
                "x1": x1, "y1": y1, "x2": x2, "y2": y2
            })

    pd.DataFrame(rows).to_csv(out_dir / "detections_table.csv", index=False, encoding="utf-8-sig")


def print_example(results, image_paths):
    if not results:
        return
    r0 = results[0]
    print("Пример вывода для первого изображения:", image_paths[0])
    if r0.boxes is None or len(r0.boxes) == 0:
        print("Детекций нет")
        return

    xyxy = r0.boxes.xyxy.cpu().numpy()
    confs = r0.boxes.conf.cpu().numpy()
    clss = r0.boxes.cls.cpu().numpy().astype(int)
    names = r0.names

    for i in range(min(5, len(xyxy))):
        c = int(clss[i])
        box = xyxy[i].round(1).tolist()
        print(f"#{i} class={names.get(c, c)} conf={float(confs[i]):.3f} box={box}")


def conf_experiment(model, image_paths, conf_list, iou, imgsz, out_dir: Path):
    import pandas as pd
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for c in conf_list:
        res = run_predict(model, list(image_paths), conf=c, iou=iou, imgsz=imgsz)
        total = 0
        uniq = set()
        sumc = 0.0
        cnt = 0

        for r in res:
            if r.boxes is None:
                continue
            total += len(r.boxes)
            if len(r.boxes) > 0:
                uniq.update(r.boxes.cls.cpu().numpy().astype(int).tolist())
                sc = r.boxes.conf.cpu().numpy()
                sumc += float(sc.sum())
                cnt += len(sc)

        rows.append({
            "conf": float(c),
            "total_detections": int(total),
            "unique_classes": int(len(uniq)),
            "avg_confidence": float(sumc / cnt) if cnt else 0.0
        })

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "conf_experiment.csv", index=False, encoding="utf-8-sig")

    plt.figure()
    plt.plot(df["conf"], df["total_detections"], marker="o")
    plt.xlabel("confidence threshold")
    plt.ylabel("detections (sum)")
    plt.title("confidence threshold influence")
    plt.tight_layout()
    plt.savefig(out_dir / "conf_vs_detections.png", dpi=160)
    plt.close()


def measure_time(model, image_path, conf, iou, imgsz, repeats: int):
    _ = run_predict(model, [image_path], conf=conf, iou=iou, imgsz=imgsz)
    times = []
    for _ in range(max(1, repeats)):
        t0 = time.perf_counter()
        _ = run_predict(model, [image_path], conf=conf, iou=iou, imgsz=imgsz)
        times.append(time.perf_counter() - t0)
    return float(np.mean(times))


def compare_models(models, image_paths, conf, iou, imgsz, repeats, out_dir: Path):
    import pandas as pd
    import cv2
    from ultralytics import YOLO

    out_dir.mkdir(parents=True, exist_ok=True)

    sample = image_paths[0]
    rows = []
    for w in models:
        m = YOLO(w)
        t = measure_time(m, sample, conf, iou, imgsz, repeats)
        res = run_predict(m, list(image_paths), conf=conf, iou=iou, imgsz=imgsz)
        total = sum(len(r.boxes) if r.boxes is not None else 0 for r in res)

        try:
            img_name = Path(sample).stem
            tag = Path(w).stem
            cv2.imwrite(str(out_dir / f"{img_name}_{tag}.jpg"), res[0].plot())
        except Exception:
            pass

        rows.append({
            "model": w,
            "avg_time_sec_per_image": float(t),
            "total_detections_on_test_images": int(total)
        })

    pd.DataFrame(rows).sort_values("avg_time_sec_per_image").to_csv(out_dir / "models_comparison.csv", index=False, encoding="utf-8-sig")


def grid_experiment(model, image_paths, imgsz_list, conf_list, iou_list, repeats, out_dir: Path):
    import pandas as pd
    import matplotlib.pyplot as plt

    out_dir.mkdir(parents=True, exist_ok=True)

    sample = image_paths[0]
    rows = []
    for s in imgsz_list:
        for c in conf_list:
            for u in iou_list:
                t = measure_time(model, sample, c, u, s, repeats)
                res = run_predict(model, list(image_paths), conf=c, iou=u, imgsz=s)
                total = sum(len(r.boxes) if r.boxes is not None else 0 for r in res)
                rows.append({
                    "imgsz": int(s),
                    "conf": float(c),
                    "iou": float(u),
                    "avg_time_sec_per_image": float(t),
                    "total_detections": int(total)
                })

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "inference_grid.csv", index=False, encoding="utf-8-sig")

    med = float(df["total_detections"].median()) if len(df) else 0.0
    filt = df[df["total_detections"] >= max(1.0, 0.6 * med)].copy()
    best = filt.sort_values("avg_time_sec_per_image").head(1)
    best.to_json(out_dir / "best_params.json", orient="records", force_ascii=False, indent=2)

    plt.figure()
    plt.scatter(df["avg_time_sec_per_image"], df["total_detections"])
    plt.xlabel("sec/image")
    plt.ylabel("detections (sum)")
    plt.title("speed vs detections (grid)")
    plt.tight_layout()
    plt.savefig(out_dir / "speed_vs_detections_grid.png", dpi=160)
    plt.close()


def process_capture(model, cap, out_path: str, conf, iou, imgsz, show: bool):
    import cv2

    writer = None
    if out_path:
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        r = model.predict(frame, conf=conf, iou=iou, imgsz=imgsz, verbose=False)[0]
        vis = r.plot()
        if writer is not None:
            writer.write(vis)
        if show:
            cv2.imshow("YOLO", vis)
            if (cv2.waitKey(1) & 0xFF) == 27:
                break

    if writer is not None:
        writer.release()
    cap.release()
    if show:
        cv2.destroyAllWindows()


def coco_metrics_and_pr(model, coco_ann, coco_images, out_dir: Path, conf, iou, imgsz, max_images, pr_classes):
    try:
        from pycocotools.coco import COCO
        from pycocotools.cocoeval import COCOeval
        import matplotlib.pyplot as plt
    except Exception:
        print("Модуль pycocotools недоступен; расчёт COCO метрик и PR-кривых пропущен.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    coco_gt = COCO(coco_ann)
    cats = coco_gt.loadCats(coco_gt.getCatIds())
    name_to_id = {c["name"].lower(): int(c["id"]) for c in cats}
    imgs = coco_gt.loadImgs(coco_gt.getImgIds())
    file_to_imgid = {im["file_name"]: int(im["id"]) for im in imgs}

    files = list(file_to_imgid.keys())
    if max_images and max_images > 0:
        files = files[:max_images]

    preds = []
    cls_to_cat = {}
    batch = 16
    for s in range(0, len(files), batch):
        part = files[s:s + batch]
        paths = [str(Path(coco_images) / f) for f in part]
        keep = [(p, f) for p, f in zip(paths, part) if Path(p).exists()]
        if not keep:
            continue

        paths = [p for p, _ in keep]
        part = [f for _, f in keep]
        results = model.predict(paths, conf=conf, iou=iou, imgsz=imgsz, verbose=False)

        for f_name, r in zip(part, results):
            img_id = file_to_imgid.get(f_name)
            if img_id is None:
                continue
            if r.boxes is None or len(r.boxes) == 0:
                continue

            names = r.names
            xyxy = r.boxes.xyxy.cpu().numpy()
            scores = r.boxes.conf.cpu().numpy()
            clss = r.boxes.cls.cpu().numpy().astype(int)

            for box, sc, c in zip(xyxy, scores, clss):
                c = int(c)
                cname = str(names.get(c, "")).lower().strip()
                if not cname:
                    continue
                if c not in cls_to_cat:
                    cid = name_to_id.get(cname)
                    if cid is None:
                        continue
                    cls_to_cat[c] = int(cid)

                x1, y1, x2, y2 = box.tolist()
                preds.append({
                    "image_id": int(img_id),
                    "category_id": int(cls_to_cat[c]),
                    "bbox": [float(x1), float(y1), float(x2 - x1), float(y2 - y1)],
                    "score": float(sc)
                })

    pred_path = out_dir / "coco_predictions.json"
    with open(pred_path, "w", encoding="utf-8") as f:
        json.dump(preds, f, ensure_ascii=False)

    coco_dt = coco_gt.loadRes(str(pred_path))
    ev = COCOeval(coco_gt, coco_dt, iouType="bbox")
    ev.evaluate()
    ev.accumulate()
    ev.summarize()

    st = ev.stats
    metrics = {
        "AP_50_95": float(st[0]),
        "AP_50": float(st[1]),
        "AP_75": float(st[2]),
        "AR_1": float(st[6]),
        "AR_10": float(st[7]),
        "AR_100": float(st[8]),
    }
    with open(out_dir / "coco_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    pr_ids = []
    for nm in pr_classes:
        cid = name_to_id.get(nm.lower())
        if cid is not None:
            pr_ids.append(int(cid))
    if not pr_ids:
        ann = coco_gt.dataset.get("annotations", [])
        freq = {}
        for a in ann:
            cid = int(a.get("category_id", -1))
            if cid >= 0:
                freq[cid] = freq.get(cid, 0) + 1
        pr_ids = [cid for cid, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]]

    prec = ev.eval["precision"]
    rec = ev.params.recThrs
    ious = ev.params.iouThrs
    cat_ids = ev.params.catIds

    t = int(np.where(np.isclose(ious, 0.5))[0][0]) if np.any(np.isclose(ious, 0.5)) else 0
    a = 0
    m = 2

    plt.figure()
    for cid in pr_ids:
        if cid not in cat_ids:
            continue
        k = int(cat_ids.index(cid))
        pr = prec[t, :, k, a, m]
        pr = np.where(pr < 0, np.nan, pr)
        nm = coco_gt.loadCats([cid])[0]["name"]
        plt.plot(rec, pr, label=nm)

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision–Recall (IoU=0.5)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "pr_curves_iou_0_5.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    args = parse_args()

    required = [
        ("ultralytics", "ultralytics"),
        ("cv2", "opencv-python"),
    ]
    optional = [
        ("pandas", "pandas"),
        ("matplotlib", "matplotlib"),
        ("yaml", "pyyaml"),
        ("pycocotools", "pycocotools"),
    ]

    strict_optional = bool(args.all)
    ensure_packages(required, optional, auto_install=args.install, strict_optional=strict_optional)

    from ultralytics import YOLO

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    images = pick_images(args.images)
    if not images:
        print("Не найдены входные изображения. Необходимо указать --images (пути или glob-шаблон).")
        print(r"Пример: --images data\*.jpg")
        sys.exit(1)

    model = YOLO(args.model)

    img_out = out_dir / "images"
    tag = f"{Path(args.model).stem}_c{args.conf}_i{args.iou}_s{args.imgsz}"
    res = run_predict(model, list(images), conf=args.conf, iou=args.iou, imgsz=args.imgsz)
    save_image_results(res, images, img_out, tag)
    print_example(res, images)

    try:
        conf_experiment(model, images, args.conf_list, args.iou, args.imgsz, img_out)
    except Exception:
        if args.all:
            raise

    if args.video:
        import cv2
        cap = cv2.VideoCapture(args.video)
        if not cap.isOpened():
            print(f"Ошибка: не удалось открыть видеофайл: {args.video}")
        else:
            vdir = out_dir / "video"
            vdir.mkdir(parents=True, exist_ok=True)
            process_capture(model, cap, str(vdir / "video_annotated.mp4"), args.conf, args.iou, args.imgsz, args.show)

    if args.webcam:
        import cv2
        cap = cv2.VideoCapture(args.cam_index)
        if not cap.isOpened():
            print(f"Ошибка: не удалось открыть камеру (index={args.cam_index})")
        else:
            cdir = out_dir / "webcam"
            cdir.mkdir(parents=True, exist_ok=True)
            process_capture(model, cap, str(cdir / "webcam_annotated.mp4"), args.conf, args.iou, args.imgsz, args.show)

    if args.compare_models:
        try:
            compare_models(args.compare_models, images, args.conf, args.iou, args.imgsz, args.repeats, out_dir / "compare")
        except Exception:
            if args.all:
                raise

    if args.all:
        try:
            grid_experiment(model, images, args.imgsz_list, args.conf_list, args.iou_list, args.repeats, out_dir / "grid")
        except Exception:
            raise

        if args.coco_ann and args.coco_images:
            coco_metrics_and_pr(model, args.coco_ann, args.coco_images, out_dir / "metrics_coco",
                                args.conf, args.iou, args.imgsz, args.max_coco_images, args.pr_classes)
        else:
            print("Для расчёта COCO метрик необходимо указать --coco_ann и --coco_images.")
            print(f"Пример: {Path(sys.argv[0]).name} --all --coco_ann instances_val2017.json --coco_images val2017")

    print("Результаты сохранены в:", str(out_dir))
