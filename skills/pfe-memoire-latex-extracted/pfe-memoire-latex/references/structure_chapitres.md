# Structure Détaillée des Chapitres du Mémoire

## Introduction Générale

**Objectif :** Contextualiser le domaine, présenter le problème industriel, annoncer la solution
et le plan du mémoire.

**Contenu suggéré :**
1. Contexte général : importance de la vision par ordinateur dans l'industrie
2. Contexte industriel Sonatrach : le rôle des torchères, problématique environnementale et
   sécuritaire, besoin de surveillance automatisée
3. Problématique : limites de la surveillance humaine, intérêt d'un système automatisé
4. Solution proposée : pipeline YOLOv8 + SVM pour détection et classification en temps réel
5. Organisation du mémoire : présentation des 5 chapitres

**Longueur cible :** 2-3 pages

---

## Chapitre 1 : Introduction Générale / Contexte Sonatrach

**Objectif :** Présenter le domaine de la vision industrielle, les torchères et le contexte
Sonatrach.

### Sections suggérées :

#### 1. Introduction (section*)
Annonce du plan du chapitre.

#### 2. La Vision par Ordinateur
- 2.1 Définition et historique
- 2.2 Domaines d'application (médecine, industrie, sécurité, automobile...)
- 2.3 Vision par ordinateur industrielle

#### 3. Les Torchères Industrielles
- 3.1 Définition et rôle des torchères dans l'industrie pétrolière
- 3.2 Problématique environnementale : émissions de CO2, suie, pollution
- 3.3 Réglementations et normes (World Bank Global Gas Flaring Reduction, ISO...)
- 3.4 Méthodes actuelles de surveillance (humaine, capteurs classiques)
- 3.5 Limites des méthodes actuelles

#### 4. Sonatrach et la Surveillance des Torchères
- 4.1 Présentation de Sonatrach
- 4.2 Importance des torchères dans les opérations Sonatrach
- 4.3 Besoin d'un système de surveillance intelligente

#### 5. Conclusion (section*)
Résumé + annonce du chapitre 2.

---

## Chapitre 2 : État de l'Art

**Objectif :** Présenter les techniques existantes en détection d'objets et en classification
d'images, puis les travaux similaires dans la littérature.

### Sections suggérées :

#### 1. Introduction (section*)

#### 2. Détection d'Objets
- 2.1 Approches classiques (Viola-Jones, HOG+SVM)
- 2.2 Réseaux de neurones convolutifs (CNN)
- 2.3 Architectures YOLO (v1 à v8) — évolution et principes
  - 2.3.1 Principe général de YOLO (one-stage detector)
  - 2.3.2 YOLOv8 : architecture, améliorations, performances
- 2.4 Autres architectures : Faster R-CNN, SSD, DETR

#### 3. Classification d'Images
- 3.1 Approches classiques : SVM, Random Forest avec features manuelles
  - 3.1.1 Histogramme de couleur (HSV, RGB)
  - 3.1.2 LBP (Local Binary Patterns)
  - 3.1.3 GLCM (Gray-Level Co-occurrence Matrix)
- 3.2 Réseaux de neurones profonds pour la classification
  - 3.2.1 EfficientNet : architecture et efficacité
  - 3.2.2 Transfer learning et fine-tuning
- 3.3 Approches hybrides CNN+classifieur classique

#### 4. Travaux Connexes — Surveillance par Vision Artificielle
- 4.1 Détection de flammes et de fumée par vision artificielle
- 4.2 Analyse de la qualité de combustion
- 4.3 Surveillance de torchères industrielles
- 4.4 Tableau comparatif des travaux existants

#### 5. Positionnement de Notre Travail
Synthèse des limites des travaux existants et justification de notre approche.

#### 6. Conclusion (section*)

---

## Chapitre 3 : Conception du Système

**Objectif :** Présenter l'architecture globale du système et les choix de conception.

### Sections suggérées :

#### 1. Introduction (section*)

#### 2. Objectif et Cahier des Charges
- Détecter les torchères en temps réel
- Classifier la qualité de combustion (3 niveaux)
- Générer des alertes et logs CSV exploitables par les opérateurs

#### 3. Architecture Globale du Système
Diagramme de l'architecture 2-modules :
- Flux vidéo -> Module A (YOLOv8) -> ROI + Classes YOLO
- ROI + Classes YOLO -> Module B (SVM HSV) -> Qualité de combustion
- Qualité -> Overlay + Log CSV

#### 4. Module A : Détection par YOLOv8
- 4.1 Choix du modèle YOLOv8m
- 4.2 Dataset Gas Flaring Detection : présentation, statistiques, exemples d'images
- 4.3 Les 6 classes YOLO et leur signification physique
- 4.4 Pipeline d'entraînement : préparation données, augmentation, hyperparamètres
- 4.5 Mapping 6 classes -> 3 niveaux de qualité

#### 5. Module B : Classification de la Qualité de Combustion
- 5.1 Extraction des ROI depuis les détections YOLO
- 5.2 Approche 1 : SVM avec features physiques manuelles
  - 5.2.1 Extraction des 113 features (HSV, LBP, GLCM, ratios)
  - 5.2.2 Architecture du classifieur SVM
- 5.3 Approche 2 : Hybride CNN+SVM (EfficientNet-B0)
- 5.4 Approche 3 : CNN EfficientNet-B0 fine-tuné
- 5.5 Stratégie d'évaluation : dataset test3, métriques

#### 6. Pipeline Temps Réel
- 6.1 Architecture du pipeline realtime_monitor.py
- 6.2 Logique frame-level de décision de qualité
- 6.3 Interface visuelle (overlay, HUD)
- 6.4 Système de logging CSV

#### 7. Conclusion (section*)

---

## Chapitre 4 : Implémentation et Expérimentation

**Objectif :** Présenter l'environnement de travail, les résultats expérimentaux et leur analyse.

### Sections suggérées :

#### 1. Introduction (section*)

#### 2. Environnement de Travail
- 2.1 Environnement matériel (PC, GPU, RAM...)
- 2.2 Environnement logiciel (Windows 11, Python 3.10, PyTorch, Ultralytics...)
- 2.3 Outils utilisés (Roboflow, Google Colab, VS Code...)

#### 3. Implémentation du Module A — YOLOv8
- 3.1 Préparation du dataset (Roboflow)
- 3.2 Entraînement YOLOv8m (170 epochs, AdamW)
- 3.3 Courbes d'entraînement (loss, métriques)
- 3.4 Résultats de détection : mAP, exemples visuels

#### 4. Implémentation du Module B — Classification
- 4.1 Extraction des ROI du dataset
- 4.2 Implémentation du SVM (features.py, train_svm.py)
  - GridSearchCV et sélection des hyperparamètres
  - Matrice de confusion
- 4.3 Implémentation CNN EfficientNet-B0 (train_cnn.py)
  - Courbes d'entraînement
  - Matrice de confusion
- 4.4 Implémentation Hybride CNN+SVM (train_hybrid.py)

#### 5. Étude Comparative des Trois Approches
- Tableau comparatif (Accuracy, F1-macro, Précision, Rappel, Taille modèle)
- Analyse : pourquoi le SVM surpasse le CNN (argument chromatique/HSV)
- Étude d'ablation : importance relative des features

#### 6. Validation sur Vidéos Réelles
- 6.1 Présentation des 3 vidéos industrielles de test
- 6.2 Résultats par vidéo (tableau des distributions par qualité)
- 6.3 Exemples de frames annotées (captures d'écran)
- 6.4 Analyse des performances en conditions réelles

#### 7. Conclusion (section*)

---

## Chapitre 5 : Discussion et Perspectives

**Objectif :** Analyser les résultats, discuter les limites et proposer des améliorations.

### Sections suggérées :

#### 1. Introduction (section*)

#### 2. Discussion des Résultats
- 2.1 Analyse critique des performances du Module A (YOLOv8)
- 2.2 Analyse critique des performances du Module B (SVM vs CNN)
- 2.3 Interprétation du résultat inattendu (SVM > CNN)
- 2.4 Adéquation du système aux besoins Sonatrach

#### 3. Limites du Système
- 3.1 Dépendance à la qualité de la caméra
- 3.2 Conditions d'éclairage extrêmes (nuit, contre-jour)
- 3.3 Dataset limité en taille et diversité
- 3.4 Absence de GPU serveur pour le déploiement temps réel optimal

#### 4. Perspectives d'Amélioration
- 4.1 Court terme : augmentation du dataset, fine-tuning YOLOv8 sur données Sonatrach
- 4.2 Moyen terme : déploiement embarqué (Jetson Nano, FPGA), intégration SCADA
- 4.3 Long terme : détection multi-torchères, prédiction des pannes, système d'alerte automatique

#### 5. Conclusion (section*)

---

## Conclusion Générale

**Contenu suggéré :**
1. Rappel du contexte et de la problématique
2. Résumé des contributions principales :
   - Système de détection en temps réel basé sur YOLOv8m
   - Comparaison rigoureuse de 3 approches de classification
   - Résultat scientifique : SVM HSV surpasse CNN avec +4,3% F1
   - Validation sur vidéos industrielles réelles
3. Portée applicative pour Sonatrach
4. Perspectives générales et ouverture

**Longueur cible :** 1-2 pages
