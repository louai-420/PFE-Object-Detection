# Contexte Technique Complet du Projet PFE

## Titre
Surveillance Intelligente des Torchères Industrielles par Vision Artificielle —
Détection et Évaluation de la Qualité de Combustion en Temps Réel

## Informations administratives
- Université : USTHB (Université des Sciences et de la Technologie Houari Boumediene)
- Faculté : Faculté d'Informatique
- Département : Intelligence Artificielle et Science des Données
- Spécialité : Master Informatique Visuelle
- Partenaire industriel : Sonatrach (compagnie pétrolière algérienne, leader en Afrique)
- Encadrant(e) : [à compléter par l'étudiant]
- Année académique : 2023-2024 (à confirmer)

---

## Architecture du Système — 2 Modules

### Module A — Détection par YOLOv8

**Modèle utilisé :**
- Architecture : YOLOv8m (medium) — 25,9M paramètres
- Source : Ultralytics, fine-tuné sur dataset Roboflow

**Dataset :**
- Nom : Gas Flaring Detection v15i (Roboflow)
- 6 classes YOLO :
  1. Dark-Flare (flamme sombre/noire)
  2. Dark-Smoke (fumée noire)
  3. Light-Flare (flamme claire/lumineuse)
  4. Light-Smoke (fumée blanche/claire)
  5. Medium-Flare (flamme orange/moyenne)
  6. Medium-Smoke (fumée grise/moyenne)
- Taille dataset : ~7500 ROI train, 1619 ROI test
- Images : 640x640 pixels

**Paramètres d'entraînement :**
- Epochs : 170
- Optimiseur : AdamW
- Batch size : 16
- Taille images : 640x640
- Environnement : Google Colab (GPU) + machine locale

**Modèle final :**
- Chemin : `outputs/models/gas_flare_yolov8m_v3/weights/best.pt`
- Taille : 49,6 MB

**Métriques YOLOv8 (à compléter selon les courbes d'entraînement) :**
- mAP@0.5 : [valeur]
- mAP@0.5:0.95 : [valeur]

---

### Module B — Classification de la Qualité de Combustion

#### Mapping des 6 classes YOLO vers 3 niveaux de qualité

| Classes YOLO | Niveau de qualité | Signification |
|--------------|-------------------|---------------|
| Light-Flare + Light-Smoke | BONNE | Combustion complète, flamme claire |
| Medium-Flare + Medium-Smoke | MOYENNE | Combustion partielle, flamme orange |
| Dark-Flare + Dark-Smoke | MAUVAISE | Combustion incomplète, fumée noire |

#### Approche 1 : SVM avec Features Physiques Manuelles (MEILLEURE)

**Features extraites (113 dimensions totales) :**
- Histogramme HSV : 96 dimensions (32 bins par canal H, S, V)
- Texture LBP (Local Binary Patterns) : 10 dimensions
- Texture GLCM (Gray-Level Co-occurrence Matrix) : 4 dimensions
  (contraste, corrélation, énergie, homogénéité)
- Ratio de fumée : 1 dimension
- Intensité RGB moyenne : 3 dimensions (R, G, B moyens)
- Ratio de pixels sombres : 1 dimension (seuil < 50)

**Hyperparamètres SVM :**
- Noyau : RBF (Radial Basis Function)
- C : 10
- Gamma : 0.01
- Optimisation : GridSearchCV 5-fold cross-validation

**Résultats sur test3 (1619 ROI) :**
- Accuracy : 0.9778 (97,78%)
- F1-macro : 0.9580 (95,80%)
- Précision macro : 0.9580
- Rappel macro : 0.9580

**Modèle sauvegardé :**
- Chemin : `outputs/classification/svm/svm_model.pkl`
- Taille : 1,5 MB

#### Approche 2 : Hybride CNN+SVM

**Architecture :**
- Extracteur de features : EfficientNet-B0 pré-entraîné sur ImageNet
  (couche de classification retirée, sortie : 1280 features)
- Aucun fine-tuning du CNN (frozen weights)
- Classifieur : SVM RBF (C=100, gamma=scale)

**Résultats sur test3 :**
- Accuracy : 0.9728 (97,28%)
- F1-macro : 0.9494 (94,94%)

**Modèle sauvegardé :**
- Chemin : `outputs/classification/hybrid/hybrid_svm_model.pkl`
- Taille : 29,5 MB

#### Approche 3 : CNN EfficientNet-B0 Fine-tuné

**Stratégie d'entraînement en 2 phases :**
- Phase 1 : 10 epochs, seule la tête de classification est entraînée (LR = 1e-3)
- Phase 2 : 20 epochs, 2 derniers blocs dé-gelés en plus de la tête (LR = 1e-4)
- Optimiseur : Adam
- Fonction de perte : CrossEntropyLoss
- Data augmentation : flip horizontal, rotation, ajustement de luminosité

**Résultats sur test3 :**
- Accuracy : 0.9487 (94,87%)
- F1-macro : 0.9150 (91,50%)

**Modèle sauvegardé :**
- Chemin : `outputs/classification/cnn/best_model.pt`
- Taille : 15,6 MB

---

## Résultat Scientifique Clé — Étude d'Ablation

**Constat principal :** Le SVM avec features manuelles (113 dimensions) SURPASSE le CNN (+4,3%
F1) et l'hybride CNN+SVM (+0,86% F1), malgré un espace de features beaucoup plus petit.

**Étude d'ablation SVM (impact de chaque groupe de features) :**

| Features retirées | Delta F1 | Interprétation |
|-------------------|----------|----------------|
| Histogramme HSV (96 dim) | -0.06 | Feature DOMINANTE |
| Texture LBP (10 dim) | -0.02 | Impact modéré |
| GLCM (4 dim) | -0.01 | Impact faible |
| Ratio fumée + pixels sombres | -0.015 | Impact faible |

**Explication scientifique :**
La qualité de combustion est un problème **chromatique** (couleur), pas morphologique (forme).
Les features HSV capturent directement l'information couleur (teinte, saturation, valeur),
permettant de distinguer clairement :
- Flamme claire (H élevé, S modéré) -> BONNE combustion
- Flamme orange (H moyen, S élevé) -> combustion MOYENNE
- Fumée noire (H faible, S faible, V faible) -> MAUVAISE combustion

Le CNN, lui, doit redécouvrir cette information couleur depuis les pixels bruts avec des données
insuffisantes (~7500 images), ce qui explique ses moins bonnes performances.

---

## Pipeline Temps Réel

**Fichier principal :** `src/realtime_monitor.py`

**Fonctionnement :**
1. Lecture du flux vidéo (fichier ou caméra) avec OpenCV
2. Détection par YOLOv8m (inférence sur chaque frame)
3. Pour chaque détection : extraction de la ROI + classification de qualité (SVM HSV)
4. Logique frame-level :
   - Si Dark-Smoke ou Dark-Flare détecté dans une frame -> frame entière = "MAUVAISE"
5. Overlay visuel :
   - Bounding boxes colorées : vert (BONNE), jaune (MOYENNE), rouge (MAUVAISE)
   - HUD avec FPS en temps réel et compteurs par catégorie
6. Log CSV horodaté de chaque détection (timestamp, classe YOLO, qualité, confiance)

**Validation sur 3 vidéos industrielles réelles :**

| Vidéo | BONNE | MOYENNE | MAUVAISE | Verdict |
|-------|-------|---------|----------|---------|
| Flamme claire | 48,0% | 52,0% | 0,2% | Cohérent |
| Flamme orange | 0,7% | 86,5% | 12,8% | Cohérent |
| Fumée noire dense | 0,4% | 0,5% | 99,1% | Cohérent |

---

## Environnement Technique

- OS : Windows 11
- Python : 3.10
- Environnement virtuel : .venv
- GPU : pas de GPU serveur (entraînement sur machine locale + Google Colab)

**Dépendances principales :**
- ultralytics (YOLOv8)
- torch, torchvision (PyTorch)
- opencv-python (traitement vidéo)
- scikit-learn (SVM, GridSearchCV, métriques)
- scikit-image (LBP, GLCM)
- numpy, matplotlib, seaborn

---

## Structure du Projet

```
PFE-Object-Detection/
├── src/
│   ├── realtime_monitor.py
│   ├── models/train_v3.py
│   ├── classification/
│   │   ├── features.py           # Extraction 113 features
│   │   ├── extract_rois.py
│   │   ├── train_svm.py
│   │   ├── train_cnn.py
│   │   ├── train_hybrid.py
│   │   ├── compare.py
│   │   └── visualize_predictions.py
│   └── evaluation/
│       └── analyze_training.py
├── outputs/
│   ├── models/gas_flare_yolov8m_v3/
│   ├── classification/{svm,cnn,hybrid,comparison,visualizations}/
│   └── realtime/
├── data/
├── setup.ps1
└── requirements.txt
```
