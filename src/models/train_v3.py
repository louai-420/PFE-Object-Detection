"""
Training script v3 – Gas Flare Detection (split 3-way rigoureux).

Différence clé par rapport à v2 :
  - Utilise data3.yaml : train3(70%) / val3(15%) / test3(15%)
  - Le test3 n'est JAMAIS vu pendant l'entraînement ni le model selection
  - Les hyperparamètres sont identiques à v2 (déjà optimisés)

Prérequis :
    python -m src.dataset.resplit3way   # génère train3/ val3/ test3/ data3.yaml

Usage :
    python src/models/train_v3.py
"""

from pathlib import Path
from ultralytics import YOLO

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parents[2]
DATA_YAML  = ROOT / "Gas Flaring Detection.v15i.yolov8" / "data3.yaml"
OUTPUT_DIR = ROOT / "outputs" / "models"

# ── Config (identique à v2) ───────────────────────────────────────────────────
MODEL_VARIANT = "yolov8m.pt"
EPOCHS        = 200
IMG_SIZE      = 640
BATCH_SIZE    = 8
PATIENCE      = 40
WORKERS       = 4
DEVICE        = 0
FREEZE_LAYERS = 10


def train():
    if not DATA_YAML.exists():
        raise FileNotFoundError(
            f"YAML introuvable : {DATA_YAML}\n"
            "Lancez d'abord : python -m src.dataset.resplit3way"
        )

    print(f"[INFO] Modèle      : {MODEL_VARIANT}")
    print(f"[INFO] Dataset     : {DATA_YAML}")
    print(f"[INFO] Output dir  : {OUTPUT_DIR}")
    print(f"[INFO] Split       : train3(70%) / val3(15%) / test3(15%)")
    print(f"[INFO] Epochs      : {EPOCHS}  |  Patience : {PATIENCE}")

    model = YOLO(MODEL_VARIANT)

    results = model.train(
        data=str(DATA_YAML),
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        patience=PATIENCE,
        workers=WORKERS,
        device=DEVICE,

        # ── Répertoire de sortie ───────────────────────────────────────────
        project=str(OUTPUT_DIR),
        name="gas_flare_yolov8m_v3",
        exist_ok=True,

        # ── Scheduler ─────────────────────────────────────────────────────
        cos_lr=True,
        lr0=0.01,
        lrf=0.005,
        warmup_epochs=5.0,

        # ── Régularisation ────────────────────────────────────────────────
        weight_decay=0.0005,
        dropout=0.0,
        label_smoothing=0.05,

        # ── Freeze backbone ───────────────────────────────────────────────
        freeze=FREEZE_LAYERS,

        # ── Augmentations couleur ─────────────────────────────────────────
        hsv_h=0.02,
        hsv_s=0.7,
        hsv_v=0.5,

        # ── Augmentations géométriques ────────────────────────────────────
        degrees=10.0,
        translate=0.1,
        scale=0.5,
        shear=2.0,
        perspective=0.0001,
        flipud=0.0,
        fliplr=0.5,

        # ── Augmentations avancées ────────────────────────────────────────
        mosaic=1.0,
        mixup=0.15,
        copy_paste=0.1,
        erasing=0.4,
        close_mosaic=15,

        # ── Logs / sauvegardes ────────────────────────────────────────────
        save=True,
        save_period=10,
        plots=True,
        verbose=True,
    )

    best = OUTPUT_DIR / "gas_flare_yolov8m_v3" / "weights" / "best.pt"
    print("\n[INFO] Entraînement terminé.")
    print(f"[INFO] Meilleurs poids : {best}")
    print(f"\n[INFO] Prochaine étape — évaluation sur le test set (jamais vu) :")
    print(f"       python main.py evaluate --weights {best} --split test")
    return results


if __name__ == "__main__":
    train()
