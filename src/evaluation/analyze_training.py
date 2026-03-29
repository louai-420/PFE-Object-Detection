"""
Analyse et visualisation des résultats d'entraînement YOLOv8.

Génère :
  1. Courbes enrichies (loss, mAP, P/R) pour chaque version de modèle
  2. Graphique comparatif multi-modèles (v1=yolov8s, v2=yolov8m, v3=yolov8m+split)
  3. Tableau de métriques finales
  4. Rapport JSON de synthèse

Note skill : toujours df.columns.str.strip() sur les CSV Ultralytics (espaces cachés).

Usage :
    python -m src.evaluation.analyze_training
"""

from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "outputs" / "analysis"

# Chemins des CSV d'entraînement pour chaque version
MODEL_RUNS = {
    "v1 (YOLOv8s)": ROOT / "outputs" / "models" / "gas_flare_yolov8s" / "results.csv",
    "v2 (YOLOv8m)": ROOT / "outputs" / "models" / "gas_flare_yolov8m_v2" / "results.csv",
    "v3 (YOLOv8m + split 3-way)": ROOT / "outputs" / "models" / "gas_flare_yolov8m_v3" / "results.csv",
}

# Résultats d'évaluation sur test (depuis les JSON)
EVAL_RESULTS = {
    "v2 (YOLOv8m)": {
        "mAP50": 0.9449, "mAP50_95": 0.7242,
        "split": "val (valid_balanced)",
    },
    "v3 (YOLOv8m + split 3-way)": {
        "mAP50": 0.936, "mAP50_95": 0.6973,
        "split": "test3 (jamais vu)",
    },
}

COLORS = {
    "v1 (YOLOv8s)": "#e67e22",
    "v2 (YOLOv8m)": "#3498db",
    "v3 (YOLOv8m + split 3-way)": "#2ecc71",
}


def load_results_csv(csv_path: Path) -> pd.DataFrame | None:
    """Charge un CSV de résultats Ultralytics avec nettoyage des colonnes."""
    if not csv_path.exists():
        print(f"  [WARN] Non trouvé : {csv_path}")
        return None
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # ← skill : espaces cachés dans les headers
    return df


def plot_training_curves_per_model():
    """Courbes individuelles pour chaque modèle (loss + métriques)."""
    for model_name, csv_path in MODEL_RUNS.items():
        df = load_results_csv(csv_path)
        if df is None:
            continue

        safe_name = model_name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        out_dir = OUTPUT / safe_name
        out_dir.mkdir(parents=True, exist_ok=True)

        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        fig.suptitle(f"Courbes d'entraînement — {model_name}", fontsize=14, fontweight="bold")

        col = COLORS.get(model_name, "#7f8c8d")

        # Row 1 : Losses
        for ax, (train_col, val_col, title) in zip(
            axes[0],
            [
                ("train/box_loss", "val/box_loss", "Box Loss"),
                ("train/cls_loss", "val/cls_loss", "Class Loss"),
                ("train/dfl_loss", "val/dfl_loss", "DFL Loss"),
            ]
        ):
            if train_col in df.columns:
                ax.plot(df["epoch"], df[train_col], label="Train", color=col, linewidth=1.5)
            if val_col in df.columns:
                ax.plot(df["epoch"], df[val_col], label="Val", color=col,
                        linestyle="--", linewidth=1.5, alpha=0.7)
            ax.set_title(title, fontsize=11)
            ax.set_xlabel("Epoch")
            ax.legend(fontsize=9)
            ax.grid(alpha=0.3)

        # Row 2 : Métriques
        metric_cols = [
            ("metrics/mAP50(B)", "mAP@0.50", "#27ae60"),
            ("metrics/mAP50-95(B)", "mAP@0.50:0.95", "#2980b9"),
        ]
        for ax, (metric_col, title, mcolor) in zip(axes[1, :2], metric_cols):
            if metric_col in df.columns:
                ax.plot(df["epoch"], df[metric_col], color=mcolor, linewidth=2)
                # Marquer le meilleur
                best_idx = df[metric_col].idxmax()
                ax.scatter(df["epoch"][best_idx], df[metric_col][best_idx],
                           color=mcolor, s=80, zorder=5)
                ax.annotate(
                    f"Best: {df[metric_col][best_idx]:.4f}",
                    xy=(df["epoch"][best_idx], df[metric_col][best_idx]),
                    xytext=(10, -15), textcoords="offset points", fontsize=8,
                )
            ax.set_title(title, fontsize=11)
            ax.set_xlabel("Epoch")
            ax.grid(alpha=0.3)

        # Precision + Recall sur le même axe
        ax = axes[1, 2]
        if "metrics/precision(B)" in df.columns:
            ax.plot(df["epoch"], df["metrics/precision(B)"],
                    label="Precision", color="#e74c3c", linewidth=1.5)
        if "metrics/recall(B)" in df.columns:
            ax.plot(df["epoch"], df["metrics/recall(B)"],
                    label="Recall", color="#9b59b6", linewidth=1.5)
        ax.set_title("Precision / Recall", fontsize=11)
        ax.set_xlabel("Epoch")
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)

        fig.tight_layout(rect=[0, 0, 1, 0.96])
        out_path = out_dir / "training_curves.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  ✔ {model_name} → {out_path}")


def plot_comparison():
    """Graphique comparatif multi-modèles sur mAP50 et mAP50-95."""
    all_dfs = {}
    for name, path in MODEL_RUNS.items():
        df = load_results_csv(path)
        if df is not None:
            all_dfs[name] = df

    if not all_dfs:
        print("  [WARN] Aucun CSV trouvé pour la comparaison.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Comparaison Multi-modèles — Gas Flare Detection (v15i)", fontsize=13)

    for model_name, df in all_dfs.items():
        col = COLORS.get(model_name, "#7f8c8d")
        if "metrics/mAP50(B)" in df.columns:
            axes[0].plot(df["epoch"], df["metrics/mAP50(B)"],
                         label=model_name, color=col, linewidth=2)
        if "metrics/mAP50-95(B)" in df.columns:
            axes[1].plot(df["epoch"], df["metrics/mAP50-95(B)"],
                         label=model_name, color=col, linewidth=2)

    axes[0].set_title("mAP@0.50 vs Epoch", fontsize=11)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("mAP@50")
    axes[0].legend(fontsize=9)
    axes[0].grid(alpha=0.3)

    axes[1].set_title("mAP@0.50:0.95 vs Epoch", fontsize=11)
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("mAP@50-95")
    axes[1].legend(fontsize=9)
    axes[1].grid(alpha=0.3)

    fig.tight_layout()
    out_path = OUTPUT / "model_comparison_curves.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✔ Comparaison → {out_path}")


def plot_final_metrics_bar():
    """Barres des métriques finales (mAP50, mAP50-95) par modèle."""
    if not EVAL_RESULTS:
        return

    models = list(EVAL_RESULTS.keys())
    map50_vals = [EVAL_RESULTS[m]["mAP50"] for m in models]
    map5095_vals = [EVAL_RESULTS[m]["mAP50_95"] for m in models]

    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    bars1 = ax.bar(x - width / 2, map50_vals, width, label="mAP@50",
                   color="#27ae60", edgecolor="white")
    bars2 = ax.bar(x + width / 2, map5095_vals, width, label="mAP@50-95",
                   color="#2980b9", edgecolor="white")

    ax.set_ylabel("Score")
    ax.set_title("Métriques finales par version de modèle (sur test set)", fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", alpha=0.3)

    # Annotations
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{bar.get_height():.3f}", ha="center", fontsize=9, fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{bar.get_height():.3f}", ha="center", fontsize=9, fontweight="bold")

    # Annotations sur le split utilisé
    for i, m in enumerate(models):
        split_label = EVAL_RESULTS[m]["split"]
        ax.text(x[i], -0.06, f"({split_label})", ha="center", fontsize=7.5,
                color="#666", transform=ax.get_xaxis_transform())

    fig.tight_layout()
    out_path = OUTPUT / "final_metrics_comparison.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  ✔ Métriques finales → {out_path}")


def print_summary_table():
    """Affiche le tableau de synthèse dans la console."""
    print("\n" + "=" * 70)
    print("  Tableau de synthèse — Détection YOLOv8")
    print("=" * 70)
    print(f"{'Modèle':<35} | {'Split eval':>18} | {'mAP50':>7} | {'mAP50-95':>9}")
    print("-" * 70)
    for model_name, metrics in EVAL_RESULTS.items():
        print(f"{model_name:<35} | {metrics['split']:>18} | "
              f"{metrics['mAP50']:>7.4f} | {metrics['mAP50_95']:>9.4f}")
    print("=" * 70)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  Analyse des résultats d'entraînement YOLOv8")
    print("=" * 60)
    print(f"\n  Sortie : {OUTPUT}")

    print("\n[1/4] Courbes individuelles par modèle...")
    plot_training_curves_per_model()

    print("\n[2/4] Graphique comparatif multi-modèles...")
    plot_comparison()

    print("\n[3/4] Barres des métriques finales...")
    plot_final_metrics_bar()

    print("\n[4/4] Tableau de synthèse...")
    print_summary_table()

    # Sauvegarder le résumé JSON
    summary = {"models": EVAL_RESULTS}
    with open(OUTPUT / "detection_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Analyse terminée. Fichiers dans : {OUTPUT}")


if __name__ == "__main__":
    main()
