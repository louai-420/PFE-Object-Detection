# PFE - Detection de Torchere et Evaluation de la Qualite de Combustion

**Projet de Fin d'Etudes - Master Informatique**
**Specialite : Vision par Ordinateur & Intelligence Artificielle**
**Realise en collaboration avec Sonatrach - Direction R&D, Boumerdes, Algerie**

---

## Contexte

Dans l'industrie petroliere et gaziere, les torcheres (gas flares) sont utilisees pour bruler les gaz excedentaires. Une combustion inefficace produit de la fumee noire et des emissions polluantes. Ce projet vise a developper un systeme intelligent de surveillance automatique des torcheres a partir d'images RGB et de videos.

---

## Objectifs

1. Detecter automatiquement les torcheres dans des images RGB ou des videos.
2. Localiser les flammes via un modele de detection d'objets (YOLOv8).
3. Analyser visuellement la combustion (couleur, fumee, intensite).
4. Evaluer et classifier la qualite de combustion : bonne / moyenne / mauvaise combustion.
5. Evaluer les modeles avec mAP, Precision, Recall, F1-score.

---

## Structure du Projet

    PFE-Object-Detection/
    |-- README.md
    |-- requirements.txt
    |-- .gitignore
    |-- main.py
    |-- data/
    |   |-- raw/
    |   |-- processed/
    |   +-- annotations/
    |-- notebooks/
    |   +-- exploration.ipynb
    |-- src/
    |   |-- dataset/
    |   |   |-- load_dataset.py
    |   |   +-- preprocess.py
    |   |-- models/
    |   |   |-- yolo_model.py
    |   |   |-- train.py
    |   |   +-- predict.py
    |   |-- evaluation/
    |   |   +-- metrics.py
    |   +-- utils/
    |       |-- config.py
    |       +-- helpers.py
    |-- outputs/
    |   |-- models/
    |   |-- predictions/
    |   +-- logs/
    +-- docs/
        +-- rapport.md

---

## Installation

    git clone https://github.com/<username>/PFE-Object-Detection.git
    cd PFE-Object-Detection
    pip install -r requirements.txt

---

## Auteur

**Rayan** - Etudiant Master Informatique, specialite VOIA
Partenaire industriel : Sonatrach - Direction R&D, Boumerdes
