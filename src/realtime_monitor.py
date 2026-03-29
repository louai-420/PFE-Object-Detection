"""
Pipeline de surveillance temps réel des torchères industrielles.

Architecture à deux étages :
  Étage 1 — YOLOv8 : Détection des objets (flammes, fumée)
  Étage 2 — Analyse HSV : Classification qualité de combustion (bonne/moyenne/mauvaise)

Fonctionnalités :
  - Lecture frame-by-frame avec OpenCV
  - Inférence YOLOv8 sur GPU (si disponible)
  - Analyse couleur HSV de chaque ROI détectée
  - Overlay visuel : bboxes colorées, labels, FPS
  - Sauvegarde vidéo annotée (.mp4)
  - Log CSV des détections horodatées

Usage :
    python src/realtime_monitor.py --source data/test_flare.mp4
    python src/realtime_monitor.py --source data/test_flare.mp4 --model outputs/models/gas_flare_yolov8m_v3/weights/best.pt
    python src/realtime_monitor.py --source 0  # webcam

Auteur : PFE Sonatrach — Surveillance Intelligente des Torchères
"""

import argparse
import csv
import os
import sys
import time
from pathlib import Path
from datetime import datetime

import cv2
import numpy as np

# Ajouter le répertoire racine au path pour les imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ── Couleurs par qualité de combustion (BGR pour OpenCV) ─────────────────

QUALITY_COLORS = {
    "bonne":    (0, 200, 80),    # Vert
    "moyenne":  (0, 180, 240),   # Orange (BGR)
    "mauvaise": (0, 60, 230),    # Rouge (BGR)
}

QUALITY_EMOJIS = {
    "bonne":    "[OK]",
    "moyenne":  "[~~]",
    "mauvaise": "[!!]",
}


# ── Analyse HSV + YOLO pour qualité de combustion ───────────────────────

def analyser_qualite_combustion(roi_bgr, cls_name=""):
    """
    Analyse la qualité de combustion d'une ROI.

    Logique à deux niveaux :
      Niveau 1 (priorité) : nom de classe YOLO
        - Dark-Smoke / Dark-Flare   → mauvaise  (cohérent avec le mapping 6→3 du training)
        - Light-Flare / Light-Smoke → bonne
        - Medium-*                  → analyse HSV fine
      Niveau 2 (fallback) : analyse couleur HSV
        - Fumée noire dense (dark_ratio) → mauvaise
        - Flamme claire (flame_ratio + mean_v) → bonne
        - Sinon → moyenne

    Paramètres
    ----------
    roi_bgr : np.ndarray
        Image BGR de la ROI.
    cls_name : str
        Nom de la classe YOLO détectée (ex: 'Dark-Smoke').
    """
    if roi_bgr is None or roi_bgr.size == 0:
        return "moyenne", {"erreur": "ROI vide"}

    # ── Niveau 1 : signal YOLO (prioritaire) ─────────────────────────
    cls_lower = cls_name.lower()
    if "dark" in cls_lower:
        # Dark-Smoke ou Dark-Flare = mauvaise combustion (définition du dataset)
        qualite_yolo = "mauvaise"
    elif "light" in cls_lower:
        # Light-Flare ou Light-Smoke = bonne combustion
        qualite_yolo = "bonne"
    else:
        qualite_yolo = None  # Medium-* ou inconnu → laisser HSV décider

    # ── Niveau 2 : analyse HSV (raffinage ou fallback) ────────────────
    hsv = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    total_pixels = max(h.size, 1)

    # Ratio pixels très sombres (V < 50) → fumée noire
    dark_ratio = float(np.sum(v < 50)) / total_pixels
    # Ratio flamme vive : H ∈ [5,35], S > 80, V > 100
    flame_mask = (h >= 5) & (h <= 35) & (s > 80) & (v > 100)
    flame_ratio = float(np.sum(flame_mask)) / total_pixels
    # Ratio fumée grise : S < 60, V ∈ [30,200]
    smoke_mask = (s < 60) & (v > 30) & (v < 200)
    smoke_ratio = float(np.sum(smoke_mask)) / total_pixels
    # Intensité moyenne normalisée
    mean_v = float(np.mean(v)) / 255.0

    scores = {
        "dark_ratio":    round(dark_ratio, 3),
        "flame_ratio":   round(flame_ratio, 3),
        "smoke_ratio":   round(smoke_ratio, 3),
        "mean_intensity": round(mean_v, 3),
    }

    # Si Niveau 1 donne 'mauvaise' ou 'bonne', confirmer / raffiner avec HSV
    if qualite_yolo == "mauvaise":
        return "mauvaise", scores
    elif qualite_yolo == "bonne":
        # Ré-vérifier : si la ROI est étonnamment sombre, dégrader
        if dark_ratio > 0.4:
            return "moyenne", scores
        return "bonne", scores

    # Medium-* : décision entièrement HSV
    if dark_ratio > 0.30:
        return "mauvaise", scores
    elif dark_ratio > 0.15 and smoke_ratio > 0.30:
        return "mauvaise", scores
    elif flame_ratio > 0.15 and mean_v > 0.45:
        return "bonne", scores
    elif mean_v > 0.5 and dark_ratio < 0.10:
        return "bonne", scores
    else:
        return "moyenne", scores


# ── Overlay visuel ───────────────────────────────────────────────────────

def dessiner_detection(frame, x1, y1, x2, y2, cls_name, conf, qualite):
    """
    Dessine une bounding box annotée sur la frame.

    Éléments :
      - Rectangle coloré selon la qualité
      - Label : nom_classe (conf%) | qualité
      - Fond semi-transparent pour le texte
    """
    color = QUALITY_COLORS.get(qualite, (255, 255, 255))
    emoji = QUALITY_EMOJIS.get(qualite, "")

    # Bounding box
    thickness = 2
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

    # Label texte
    label = f"{cls_name} {conf:.0%} | {qualite} {emoji}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    font_thickness = 1
    (tw, th), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)

    # Fond du label (rectangle semi-transparent)
    label_y1 = max(y1 - th - 10, 0)
    label_y2 = y1
    cv2.rectangle(frame, (x1, label_y1), (x1 + tw + 6, label_y2), color, -1)
    cv2.putText(frame, label, (x1 + 3, label_y2 - 4),
                font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    # Petite barre de qualité en bas de la bbox
    bar_h = 4
    bar_width = x2 - x1
    cv2.rectangle(frame, (x1, y2), (x2, y2 + bar_h), color, -1)

    return frame


def dessiner_hud(frame, fps, frame_idx, total_frames, stats_qualite):
    """
    Dessine le HUD (Head-Up Display) avec les infos de monitoring.

    Inclut : FPS, numéro de frame, statistiques de qualité.
    """
    h, w = frame.shape[:2]

    # Fond semi-transparent pour le HUD (en haut)
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 65), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    # Titre
    cv2.putText(frame, "SONATRACH - Surveillance Torcheres", (10, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    # FPS et progression
    progress = f"Frame {frame_idx}"
    if total_frames > 0:
        pct = frame_idx / total_frames * 100
        progress += f"/{total_frames} ({pct:.0f}%)"
    cv2.putText(frame, f"FPS: {fps:.1f} | {progress}", (10, 48),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA)

    # Stats de qualité (en haut à droite)
    x_right = w - 200
    y_start = 20
    for i, (q, count) in enumerate(stats_qualite.items()):
        color = QUALITY_COLORS.get(q, (255, 255, 255))
        text = f"{q}: {count}"
        cv2.putText(frame, text, (x_right, y_start + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    return frame


# ── Pipeline principal ───────────────────────────────────────────────────

def trouver_meilleur_modele():
    """Cherche le meilleur modèle YOLOv8 dans le projet."""
    candidats = [
        ROOT / "outputs" / "models" / "gas_flare_yolov8m_v3" / "weights" / "best.pt",
        ROOT / "outputs" / "models" / "gas_flare_yolov8m_v2" / "weights" / "best.pt",
        ROOT / "outputs" / "models" / "gas_flare_yolov8s" / "weights" / "best.pt",
    ]
    for c in candidats:
        if c.exists():
            return str(c)
    # Fallback : modèle pré-entraîné
    return "yolov8s.pt"


def run_pipeline(source, model_path=None, conf=0.4, output_dir=None, show=False):
    """
    Lance le pipeline de surveillance temps réel.

    Paramètres
    ----------
    source : str
        Chemin vidéo ou '0' pour webcam.
    model_path : str
        Chemin vers le modèle YOLOv8 (.pt).
    conf : float
        Seuil de confiance pour la détection.
    output_dir : str
        Répertoire de sortie pour les résultats.
    show : bool
        Afficher la fenêtre OpenCV (désactivé en mode headless).
    """
    from ultralytics import YOLO

    # ── Configuration ─────────────────────────────────────────────────
    if model_path is None:
        model_path = trouver_meilleur_modele()

    if output_dir is None:
        output_dir = ROOT / "outputs" / "realtime"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 65)
    print("  SONATRACH — Pipeline Surveillance Torchères")
    print("=" * 65)
    print(f"  Modèle   : {model_path}")
    print(f"  Source    : {source}")
    print(f"  Conf      : {conf}")
    print(f"  Output    : {output_dir}")

    # ── Charger le modèle ─────────────────────────────────────────────
    print("\n[1/4] Chargement du modèle YOLOv8...")
    model = YOLO(model_path)
    class_names = model.names
    print(f"  Classes : {class_names}")

    # ── Ouvrir la vidéo ───────────────────────────────────────────────
    print("\n[2/4] Ouverture de la source vidéo...")
    # Si source est un nombre, c'est une webcam
    src = int(source) if source.isdigit() else source
    cap = cv2.VideoCapture(src)

    if not cap.isOpened():
        print(f"  [ERREUR] Impossible d'ouvrir : {source}")
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_video = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"  Résolution : {w}×{h}")
    print(f"  FPS source : {fps_video:.1f}")
    print(f"  Frames     : {total_frames}")
    print(f"  Durée      : {total_frames / fps_video:.1f}s")

    # ── Préparer la sortie ────────────────────────────────────────────
    output_video_path = output_dir / f"realtime_output_{timestamp_str}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output_video_path), fourcc, fps_video, (w, h))

    csv_path = output_dir / f"detections_log_{timestamp_str}.csv"
    csv_file = open(csv_path, "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([
        "frame_idx", "timestamp_sec", "class_name", "confidence",
        "qualite", "x1", "y1", "x2", "y2",
        "dark_ratio", "flame_ratio", "smoke_ratio", "mean_intensity",
    ])

    # ── Boucle d'inférence ────────────────────────────────────────────
    print("\n[3/4] Traitement en cours...")

    stats_qualite = {"bonne": 0, "moyenne": 0, "mauvaise": 0}
    total_detections = 0
    fps_history = []
    frame_idx = 0

    try:
        while True:
            t0 = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1
            timestamp_sec = frame_idx / fps_video

            # Inférence YOLOv8
            results = model.predict(
                frame, conf=conf, iou=0.45,
                verbose=False, stream=False,
            )[0]

            # ── Pass 1 : collecter toutes les détections de la frame ─────
            frame_detections = []
            for box in results.boxes:
                cls_id = int(box.cls[0])
                cls_name = class_names[cls_id]
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                roi = frame[y1:y2, x1:x2]
                _, scores = analyser_qualite_combustion(roi, cls_name=cls_name)
                frame_detections.append({
                    "cls_name": cls_name, "conf": confidence,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "scores": scores,
                })

            # ── Raisonnement au niveau frame ──────────────────────────────
            # Logique : si la frame contient de la fumée noire (Dark-*)
            # alors la combustion est globalement mauvaise.
            all_classes = [d["cls_name"].lower() for d in frame_detections]
            has_dark = any("dark" in c for c in all_classes)
            has_medium = any("medium" in c for c in all_classes)

            if has_dark:
                frame_qualite = "mauvaise"
            elif has_medium:
                frame_qualite = "moyenne"
            else:
                frame_qualite = "bonne"

            # ── Pass 2 : dessiner et logger avec la qualité frame ─────────
            for det in frame_detections:
                total_detections += 1
                stats_qualite[frame_qualite] += 1

                dessiner_detection(frame, det["x1"], det["y1"],
                                   det["x2"], det["y2"],
                                   det["cls_name"], det["conf"], frame_qualite)

                csv_writer.writerow([
                    frame_idx,
                    f"{timestamp_sec:.3f}",
                    det["cls_name"],
                    f"{det['conf']:.4f}",
                    frame_qualite,
                    det["x1"], det["y1"], det["x2"], det["y2"],
                    det["scores"].get("dark_ratio", ""),
                    det["scores"].get("flame_ratio", ""),
                    det["scores"].get("smoke_ratio", ""),
                    det["scores"].get("mean_intensity", ""),
                ])

            # Calculer le FPS
            elapsed = time.time() - t0
            fps_current = 1.0 / max(elapsed, 1e-6)
            fps_history.append(fps_current)

            # HUD overlay
            dessiner_hud(frame, fps_current, frame_idx, total_frames, stats_qualite)

            # Sauvegarder la frame annotée
            writer.write(frame)

            # Affichage (optionnel)
            if show:
                cv2.imshow("Sonatrach - Surveillance Torcheres", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("  [INFO] Arrêt par l'utilisateur (touche Q)")
                    break

            # Progression (toutes les 100 frames)
            if frame_idx % 100 == 0:
                avg_fps = sum(fps_history[-100:]) / min(len(fps_history), 100)
                pct = frame_idx / max(total_frames, 1) * 100
                print(f"  Frame {frame_idx}/{total_frames} ({pct:.0f}%) "
                      f"| FPS: {avg_fps:.1f} | Détections: {total_detections}")

    except KeyboardInterrupt:
        print("\n  [INFO] Arrêt par Ctrl+C")
    finally:
        cap.release()
        writer.release()
        csv_file.close()
        if show:
            cv2.destroyAllWindows()

    # ── Résultats ─────────────────────────────────────────────────────
    fps_moyen = sum(fps_history) / max(len(fps_history), 1)

    print("\n" + "=" * 65)
    print("  [4/4] RÉSULTATS")
    print("=" * 65)
    print(f"  Frames traitées    : {frame_idx}")
    print(f"  FPS moyen          : {fps_moyen:.1f}")
    print(f"  Détections totales : {total_detections}")
    print(f"\n  Distribution qualité :")
    for q in ["bonne", "moyenne", "mauvaise"]:
        count = stats_qualite[q]
        pct = count / max(total_detections, 1) * 100
        bar = "█" * int(pct / 2)
        print(f"    {q:<12}: {count:>5} ({pct:>5.1f}%)  {bar}")
    print(f"\n  Vidéo sortie : {output_video_path}")
    print(f"  Log CSV      : {csv_path}")
    print("=" * 65)

    return {
        "frames": frame_idx,
        "fps_moyen": round(fps_moyen, 1),
        "detections": total_detections,
        "qualite": stats_qualite,
        "video": str(output_video_path),
        "csv": str(csv_path),
    }


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline surveillance torchères — Sonatrach PFE",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--source", type=str, required=True,
        help="Chemin vidéo ou '0' pour webcam",
    )
    parser.add_argument(
        "--model", type=str, default=None,
        help="Chemin modèle YOLOv8 (.pt). Auto-détecté si non spécifié.",
    )
    parser.add_argument(
        "--conf", type=float, default=0.4,
        help="Seuil de confiance (défaut: 0.4)",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Répertoire de sortie (défaut: outputs/realtime/)",
    )
    parser.add_argument(
        "--show", action="store_true",
        help="Afficher la fenêtre OpenCV en temps réel",
    )

    args = parser.parse_args()
    run_pipeline(
        source=args.source,
        model_path=args.model,
        conf=args.conf,
        output_dir=args.output,
        show=args.show,
    )


if __name__ == "__main__":
    main()
