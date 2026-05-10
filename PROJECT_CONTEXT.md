# Projet PFE — Contexte Complet

Tu es un assistant qui aide à finaliser un mémoire de fin d'études (PFE) pour le diplôme Master en informatique visuelle en collaboration avec Sonatrach (compagnie pétrolière algérienne). Voici le contexte complet du projet :

## Titre
Surveillance Intelligente des Torchères Industrielles par Vision Artificielle — Détection et Évaluation de la Qualité de Combustion en Temps Réel

## Objectif
Développer un pipeline automatisé de vision par ordinateur capable de :
1. Détecter les torchères (gas flares) dans des flux vidéo industriels
2. Évaluer la qualité de combustion (bonne / moyenne / mauvaise) en temps réel
3. Générer des alertes et des logs exploitables par les opérateurs Sonatrach

## Architecture du Système (2 modules)

### Module A — Détection (YOLOv8)
- Modèle : YOLOv8m (medium), fine-tuné sur un dataset Roboflow (Gas Flaring Detection v15i)
- 6 classes YOLO : Dark-Flare, Dark-Smoke, Light-Flare, Light-Smoke, Medium-Flare, Medium-Smoke
- Entraînement : 170 epochs, AdamW, images 640×640, batch 16
- Modèle final : `outputs/models/gas_flare_yolov8m_v3/weights/best.pt` (49.6 MB)

### Module B — Classification de la qualité de combustion
Trois approches ont été comparées sur un jeu de test (test3, 1619 ROI) :

**1. SVM avec features physiques manuelles (🥇 MEILLEUR)**
- 113 features : Histogramme HSV (96 dim), Texture LBP (10 dim), GLCM (4 dim), ratio fumée, intensité RGB, ratio pixels sombres
- Hyperparamètres : SVM RBF, C=10, γ=0.01 (GridSearchCV 5-fold)
- Résultats : Accuracy=0.9778, F1-macro=0.9580, Precision=0.9580, Recall=0.9580
- Modèle : `outputs/classification/svm/svm_model.pkl` (1.5 MB)

**2. Hybride CNN+SVM (🥈)**
- Extracteur : EfficientNet-B0 pré-entraîné ImageNet (sans fine-tuning), 1280 features
- Classifieur : SVM RBF (C=100, γ=scale)
- Résultats : Accuracy=0.9728, F1-macro=0.9494
- Modèle : `outputs/classification/hybrid/hybrid_svm_model.pkl` (29.5 MB)

**3. CNN EfficientNet-B0 fine-tuné (🥉)**
- Fine-tuning 2 phases : 10 epochs tête seule (LR=1e-3) + 20 epochs 2 blocs dégelés (LR=1e-4)
- Résultats : Accuracy=0.9487, F1-macro=0.9150
- Modèle : `outputs/classification/cnn/best_model.pt` (15.6 MB)

### Résultat scientifique clé
Le SVM avec features manuelles (113 dim) **SURPASSE** le CNN (+4.3% F1) et l'hybride CNN+SVM (1280 dim). L'étude d'ablation montre que l'histogramme HSV est la feature dominante (ΔF1 = -0.06 sans elle). Explication : la qualité de combustion est un problème **chromatique** (couleur), pas morphologique (forme). Les features HSV capturent directement cette information, tandis que le CNN doit la redécouvrir avec des données insuffisantes.

### Pipeline Temps Réel (`realtime_monitor.py`)
- Traite des flux vidéo avec YOLOv8 + classification HSV/YOLO
- Logique frame-level : si Dark-Smoke/Dark-Flare est détecté dans une frame → toute la frame = "mauvaise"
- Overlay visuel : bounding boxes colorées (vert/jaune/rouge), HUD avec FPS et compteurs
- Log CSV horodaté de chaque détection
- Validé sur 3 vidéos industrielles réelles :
  - Flamme claire → 48% bonne, 52% moyenne, 0.2% mauvaise ✅
  - Flamme orange → 0.7% bonne, 86.5% moyenne, 12.8% mauvaise ✅
  - Fumée noire dense → 0.4% bonne, 0.5% moyenne, 99.1% mauvaise ✅

## Mapping des classes (6→3)
Les 6 classes YOLO sont mappées vers 3 niveaux de qualité de combustion :
- Light-Flare + Light-Smoke → **BONNE** (combustion complète, flamme claire)
- Medium-Flare + Medium-Smoke → **MOYENNE** (combustion partielle, flamme orange)
- Dark-Flare + Dark-Smoke → **MAUVAISE** (combustion incomplète, fumée noire)

## Structure du code
```
PFE-Object-Detection/
├── src/
│   ├── realtime_monitor.py          # Pipeline temps réel (Module A+B)
│   ├── models/train_v3.py           # Entraînement YOLOv8
│   ├── classification/
│   │   ├── features.py              # Extraction des 113 features physiques
│   │   ├── extract_rois.py          # Extraction des ROI depuis le dataset YOLO
│   │   ├── train_svm.py             # Entraînement SVM + GridSearch + ablation
│   │   ├── train_cnn.py             # Fine-tuning EfficientNet-B0
│   │   ├── train_hybrid.py          # Hybride CNN+SVM
│   │   ├── compare.py               # Comparaison des 3 approches
│   │   └── visualize_predictions.py # Grilles visuelles (style val_batch YOLO)
│   └── evaluation/
│       └── analyze_training.py      # Analyse courbes YOLOv8
├── outputs/
│   ├── models/gas_flare_yolov8m_v3/ # Modèle YOLO final
│   ├── classification/{svm,cnn,hybrid,comparison,visualizations}/
│   └── realtime/                    # Vidéos annotées + logs CSV
├── data/                            # Vidéos test + ROI extraites
├── setup.ps1                        # Script d'installation automatique
└── requirements.txt                 # Dépendances Python
```

## Mémoire LaTeX
Le mémoire est dans `Memoire/USTHB_Thesis/` avec 5 chapitres :
- Chapitre 1 : Introduction générale / contexte Sonatrach
- Chapitre 2 : État de l'art (détection d'objets, classification, vision industrielle)
- Chapitre 3 : Conception du système (architecture proposée)
- Chapitre 4 : Implémentation et Expérimentation (résultats remplis avec nos données)
- Chapitre 5 : Discussion et Perspectives

## Dépendances principales
ultralytics, torch, torchvision, opencv-python, scikit-learn, scikit-image, numpy, matplotlib, seaborn

## Contraintes
- Environnement Windows 11 + Python 3.10 + .venv
- Pas de GPU serveur disponible (entraînement fait sur machine locale/Colab)
- Dataset de taille modérée (~7500 ROI train, 1619 ROI test)
- Le mémoire est en français (LaTeX, classe report)
