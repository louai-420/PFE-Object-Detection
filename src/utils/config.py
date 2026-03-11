"""
Central configuration for Gas Flare Detection project.
All paths and hyper-parameters are defined here.
"""

from pathlib import Path

# ── Root ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]   # PFE-Object-Detection/

# ── Dataset ──────────────────────────────────────────────────────────────────
DATA_YAML    = ROOT / "Gas Flaring Detection.v15i.yolov8" / "data_balanced.yaml"
TEST_IMAGES  = ROOT / "Gas Flaring Detection.v15i.yolov8" / "test" / "images"

# ── Model ────────────────────────────────────────────────────────────────────
BEST_WEIGHTS    = ROOT / "outputs" / "models" / "gas_flare_yolov8m_v2" / "weights" / "best.pt"
LAST_WEIGHTS    = ROOT / "outputs" / "models" / "gas_flare_yolov8m_v2" / "weights" / "last.pt"

# ── Output dirs ──────────────────────────────────────────────────────────────
OUTPUT_DIR      = ROOT / "outputs"
PREDICTIONS_DIR = OUTPUT_DIR / "predictions"
LOGS_DIR        = OUTPUT_DIR / "logs"

# ── Classes ──────────────────────────────────────────────────────────────────
CLASS_NAMES = [
    "Dark-Flare",
    "Dark-Smoke",
    "Light-Flare",
    "Light-Smoke",
    "Medium-Flare",
    "Medium-Smoke",
]
NUM_CLASSES = len(CLASS_NAMES)

# ── Inference defaults ───────────────────────────────────────────────────────
IMG_SIZE   = 640
CONF_THRES = 0.25
IOU_THRES  = 0.45
DEVICE     = 0        # 0 = first GPU, "cpu" = CPU
