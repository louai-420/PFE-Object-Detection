---
name: pfe-memoire-latex
description: >
  Skill spécialisé pour aider à la rédaction, la correction, le peaufinage et la structuration
  d'un mémoire de fin d'études (PFE) Master en LaTeX, en français, pour l'USTHB (Université des
  Sciences et de la Technologie Houari Boumediene), Faculté d'Informatique, spécialité
  Informatique Visuelle. Ce skill doit être utilisé dès que l'utilisateur mentionne : rédiger un
  chapitre, corriger du LaTeX, améliorer un paragraphe, écrire une introduction/conclusion de
  chapitre, formuler des résultats, écrire l'état de l'art, la conception, la réalisation,
  la discussion, les remerciements, le résumé/abstract, ou toute autre section de mémoire.
  Utilise ce skill aussi pour générer des tableaux LaTeX, des commandes figure, des citations
  cite, des listes d'abréviations, et pour reformuler du contenu dans le style académique
  algérien (USTHB).
---

# Skill : Rédaction Mémoire PFE — LaTeX USTHB

## Contexte du projet

Le mémoire porte sur :
**"Surveillance Intelligente des Torchères Industrielles par Vision Artificielle — Détection et
Évaluation de la Qualité de Combustion en Temps Réel"**
- Partenaire industriel : **Sonatrach** (compagnie pétrolière algérienne)
- Diplôme : **Master Informatique Visuelle**, USTHB, Faculté d'Informatique
- Langue : **Français** (mémoire complet en français)
- Outil de rédaction : **LaTeX**, classe `report`
- Environnement : Windows 11, Python 3.10

Pour les détails techniques complets du projet (architecture, résultats, métriques), consulte le
fichier `references/projet_context.md`.

---

## Style académique USTHB — Règles absolues

Ces règles sont extraites de l'analyse croisée de **4 mémoires de référence USTHB** :
BENNACER_MADANY, BENZEID_BENTEBBICHE, NIBOUCHA_TOUABI, SEDDIKI_Tesnyme.
**Respecte-les impérativement.**

### 1. Ton et registre
- Toujours utiliser le **"nous"** (jamais "je") : "nous avons proposé", "nous avons montré"
  - Exception : mémoire solo (SEDDIKI) -> "nous" reste d'usage même pour un auteur unique
- Ton **formel, neutre et scientifique** — éviter tout langage familier
- Phrases **courtes à moyennes** (15-30 mots), bien articulées
- Éviter les superlatifs excessifs ; préférer des formulations mesurées :
  "les résultats montrent que..." plutôt que "notre système est le meilleur..."
- Utiliser le présent de l'indicatif pour les faits généraux, le passé composé pour les actions
  réalisées : "YOLOv8 **est** une architecture..." / "nous **avons entraîné** le modèle..."

### 2. Structure de chaque chapitre (OBLIGATOIRE)
Chaque chapitre suit **exactement** ce schéma :
```
\chapter{Titre du Chapitre}

\section*{Introduction}   % ou 1. Introduction
[Paragraphe d'intro : annonce les sections et le contexte]

\section{...}   % sections de contenu numérotées
...

\section*{Conclusion}   % ou N. Conclusion
[Paragraphe de conclusion : résume + annonce le chapitre suivant]
```

### 3. Formules de transition inter-chapitres
Fin de chapitre -> début suivant (exemples tirés des mémoires réels) :
- "Le chapitre suivant sera consacré à [sujet]."
- "Nous pourrons maintenant passer à [sujet], qui fera l'objet du prochain chapitre."
- "Dans ce contexte, le prochain chapitre abordera [sujet]."
- "Ce chapitre clôture la partie théorique. Le chapitre suivant présente notre contribution."

Début de chapitre :
- "Dans ce chapitre, nous allons [présenter/décrire/analyser]..."
- "Ce chapitre comprend N grandes parties : [liste]."
- "Maintenant que nous avons présenté X, nous pouvons entrer dans le vif du sujet..."
- "Dans un premier temps, nous [section 1]. Ensuite, nous [section 2]. Enfin, nous [section 3]."

### 4. Introduction générale — structure type
1. Contexte large (domaine de la vision par ordinateur, IA industrielle)
2. Problème spécifique (surveillance des torchères, limites des méthodes actuelles)
3. Solution proposée (pipeline YOLOv8 + SVM)
4. **Organisation du mémoire** (liste explicite des chapitres) :
   "Pour réaliser ce projet, nous avons organisé notre mémoire comme suit :
   - **Chapitre 1 :** ... - **Chapitre 2 :** ..."

### 5. Conclusion générale — structure type
1. Rappel du contexte et de la problématique (1 paragraphe)
2. Résumé des contributions (par chapitre ou par module)
3. Résultats clés chiffrés ("accuracy de 97,78%", "+4,3% F1")
4. Limites rencontrées (liste courte, honnête)
5. Perspectives d'amélioration (court terme / long terme)

### 6. Formulation des résultats expérimentaux
- Toujours présenter les métriques dans un **tableau LaTeX** (tabular ou booktabs)
- Commenter chaque tableau/figure **après** son insertion :
  "D'après le tableau \ref{tab:X}, nous observons que..."
  "La figure \ref{fig:X} illustre clairement..."
  "Les résultats obtenus montrent que..."
- Pour comparer des approches :
  "L'approche A surpasse l'approche B de X\% en termes de F1-macro."
  "Motivés par ces résultats, nous avons retenu [approche] comme solution finale."
- Pattern NIBOUCHA : justifier les choix par des **tests comparatifs préalables**
  "Afin de choisir le modèle le plus adéquat, nous avons testé N approches..."

### 7. Présentation de l'environnement de travail (Chapitre Réalisation)
Toujours inclure deux sous-sections :
- **Environnement matériel** : CPU, RAM, GPU (si disponible), OS
- **Environnement logiciel** : langage, frameworks, IDE, plateformes (Google Colab...)
Présenter chaque outil avec : nom + version + rôle dans le projet (1-2 lignes max)

### 8. Références et citations
- Style numérique entre crochets : `\cite{ref}` -> [1], [2], ...
- Toujours citer la source après une définition : "La vision par ordinateur est... [1]."
- Citer après chaque affirmation non triviale ou donnée chiffrée
- Bibliographie en fin de document, format `thebibliography`
- Pour les URLs : inclure la date de consultation ("consulté le JJ/MM/AAAA")

### 9. Présentation des remerciements (page liminaire)
Structure observée dans les 4 mémoires :
1. Remerciement à Allah (formule standard algérienne)
2. Remerciements à l'encadrant(e) (qualités : disponibilité, conseils, encadrement)
3. Remerciements aux membres du jury
4. Remerciements à l'entreprise partenaire (Sonatrach) si applicable
5. Remerciements à la famille et amis

---

## Structure du mémoire (5 chapitres)

Consulte `references/structure_chapitres.md` pour le plan détaillé de chaque chapitre.

| Chapitre | Titre | Nature |
|----------|-------|--------|
| Intro générale | Introduction générale | Contextualisation + plan |
| 1 | Introduction générale / Contexte Sonatrach | Théorique |
| 2 | État de l'art | Théorique |
| 3 | Conception du système | Technique |
| 4 | Implémentation et Expérimentation | Pratique |
| 5 | Discussion et Perspectives | Analytique |
| Conclusion générale | Conclusion générale | Synthèse + perspectives |

---

## Templates LaTeX réutilisables

### Template : Introduction de chapitre
```latex
\chapter{Titre du chapitre}

\section*{Introduction}
Dans ce chapitre, nous abordons [sujet principal du chapitre]. Dans un premier temps, nous
[première section]. Ensuite, nous [deuxième section]. Enfin, nous [dernière section].
```

### Template : Conclusion de chapitre
```latex
\section*{Conclusion}
Dans ce chapitre, nous avons présenté [résumé en 1-2 phrases]. Nous avons également montré
[point clé]. Le chapitre suivant sera consacré à [titre/sujet du chapitre N+1].
```

### Template : Tableau de résultats comparatifs
```latex
\begin{table}[h!]
\centering
\caption{Comparaison des performances des trois approches de classification}
\label{tab:comparaison}
\begin{tabular}{|l|c|c|c|c|}
\hline
\textbf{Approche} & \textbf{Accuracy} & \textbf{F1-macro} & \textbf{Précision} & \textbf{Rappel} \\
\hline
SVM (features HSV/LBP/GLCM) & 0.9778 & 0.9580 & 0.9580 & 0.9580 \\
Hybride CNN+SVM              & 0.9728 & 0.9494 & --     & --     \\
CNN EfficientNet-B0          & 0.9487 & 0.9150 & --     & --     \\
\hline
\end{tabular}
\end{table}

D'après le tableau \ref{tab:comparaison}, l'approche SVM avec features physiques manuelles
obtient les meilleures performances avec une accuracy de 97,78\% et un F1-macro de 95,80\%,
surpassant ainsi les approches à base de réseaux de neurones convolutifs.
```

### Template : Inclusion de figure
```latex
\begin{figure}[h!]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/nom_figure}
    \caption{Description de la figure.}
    \label{fig:nom_figure}
\end{figure}

La figure \ref{fig:nom_figure} illustre [ce que montre la figure].
```

### Template : Listing de code Python
```latex
\begin{lstlisting}[language=Python, caption={Description du code}, label={lst:code}]
# Extrait de code ici
\end{lstlisting}
```

### Template : Résumé / Abstract
```latex
% RÉSUMÉ (Français)
[Contexte général en 1-2 phrases.] [Problème spécifique adressé.] [Approche proposée.]
[Résultats clés avec métriques.] [Conclusion et portée.]

\textbf{Mots-clés :} torchère industrielle, détection d'objets, YOLOv8, SVM, qualité de
combustion, vision par ordinateur, temps réel, Sonatrach.

% ABSTRACT (English)
[Same content in English.]

\textbf{Keywords:} industrial gas flare, object detection, YOLOv8, SVM, combustion quality,
computer vision, real-time, Sonatrach.
```

### Template : Tableau comparatif avantages/limites (style NIBOUCHA)
```latex
\begin{table}[h!]
\centering
\caption{Comparaison des approches de [sujet]}
\label{tab:comparaison_approches}
\begin{tabular}{|l|p{5cm}|p{5cm}|}
\hline
\textbf{Approche} & \textbf{Avantages} & \textbf{Limites} \\
\hline
Approche A & Avantage 1. Avantage 2. & Limite 1. \\
\hline
Approche B & Avantage 1. & Limite 1. Limite 2. \\
\hline
\end{tabular}
\end{table}
```

### Template : Présentation d'un outil logiciel (style Réalisation)
```latex
\subsection{Nom de l'outil}
\textbf{Nom de l'outil} est [définition courte]. Il a été utilisé dans notre projet pour
[rôle spécifique] \cite{ref}.

\begin{figure}[h!]
    \centering
    \includegraphics[width=0.3\textwidth]{figures/logo_outil}
    \caption{Logo de [Nom de l'outil].}
    \label{fig:logo_outil}
\end{figure}
```

### Template : Justification du choix d'une méthode (pattern USTHB)
```latex
Afin de choisir l'approche la plus adaptée à notre problématique, nous avons évalué
[N] méthodes sur [critère]. Le tableau \ref{tab:choix} présente les résultats obtenus.

[tableau comparatif]

D'après ces résultats, nous avons retenu [méthode choisie] comme solution finale, en
raison de [raison principale]. Cette approche offre le meilleur compromis entre
[critère 1] et [critère 2].
```

### Template : Remerciements (style USTHB standard)
```latex
\chapter*{Remerciements}
\addcontentsline{toc}{chapter}{Remerciements}

Tout d'abord, nous remercions Allah, le Tout Puissant, de nous avoir accordé la santé,
la force et la persévérance pour mener à bien ce travail.

Nous tenons à exprimer notre profonde gratitude à notre encadrant(e), [Titre Nom],
pour sa disponibilité, ses précieux conseils et la qualité de son encadrement tout au
long de ce projet.

Nous adressons également nos remerciements aux membres du jury, [Titre Nom] et
[Titre Nom], pour l'honneur qu'ils nous ont accordé en acceptant d'évaluer ce travail.

Nos sincères remerciements vont à l'entreprise Sonatrach pour avoir proposé ce sujet
et pour le soutien apporté durant la réalisation de ce projet.

Enfin, nous remercions nos familles et nos amis pour leur soutien inconditionnel et
leurs encouragements tout au long de notre parcours universitaire.
```

---

## Vocabulaire technique du domaine (FR/EN)

| Français | Anglais | Usage dans le texte |
|----------|---------|---------------------|
| Torchère industrielle | Industrial gas flare | "Les torchères industrielles sont..." |
| Détection d'objets | Object detection | "La détection d'objets par..." |
| Qualité de combustion | Combustion quality | "l'évaluation de la qualité de combustion" |
| Boîte englobante | Bounding box | "les boîtes englobantes détectées" |
| Extraction de caractéristiques | Feature extraction | "l'extraction de 113 caractéristiques" |
| Machine à vecteurs de support | Support Vector Machine (SVM) | "un classifieur SVM à noyau RBF" |
| Réseau de neurones convolutif | CNN | "EfficientNet-B0, un CNN pré-entraîné" |
| Ajustement fin | Fine-tuning | "l'ajustement fin du modèle EfficientNet-B0" |
| Régions d'intérêt | ROI (Region of Interest) | "les ROI extraites du dataset" |
| Taux de détection | Detection rate / Recall | |
| Précision | Precision | |
| Rappel | Recall | |
| Score F1 | F1-score | |
| Flux vidéo temps réel | Real-time video stream | "le traitement du flux vidéo en temps réel" |
| Annotation | Annotation / Labeling | "les images annotées avec Roboflow" |
| Étude d'ablation | Ablation study | "l'étude d'ablation montre que..." |
| Histogramme HSV | HSV histogram | "l'histogramme HSV en 96 dimensions" |
| Texture LBP | LBP texture | "le descripteur LBP en 10 dimensions" |
| Matrice GLCM | GLCM matrix | "les 4 features GLCM" |

---

## Workflow de rédaction

Quand l'utilisateur demande de **rédiger** une section :
1. Identifier le chapitre et la section ciblés
2. Lire `references/projet_context.md` si besoin de données techniques précises
3. Appliquer le style USTHB (voir section "Style académique USTHB")
4. Générer le texte **en LaTeX directement** (pas en Markdown)
5. Inclure les transitions et liens inter-sections appropriés
6. Proposer les citations `\cite{}` aux endroits pertinents (avec un placeholder `[REF]` si la
   référence exacte n'est pas connue)

Quand l'utilisateur demande de **corriger/améliorer** un texte existant :
1. Identifier les problèmes : style non académique, répétitions, mauvaise structure, LaTeX incorrect
2. Proposer une version corrigée **complète** (pas juste les lignes modifiées)
3. Expliquer brièvement les changements majeurs

Quand l'utilisateur demande de **générer un élément LaTeX** (tableau, figure, liste) :
1. Utiliser les templates de ce skill
2. Pré-remplir avec les données du projet si disponibles
3. Ajouter le commentaire de renvoi après l'élément ("D'après le tableau X...")

---

## Patterns de rédaction observés dans les 4 mémoires de référence

### Pattern 1 : Définition + citation immédiate
"[Terme] est [définition courte et précise] [citation]. [Développement en 1-2 phrases]."
Exemple : "La vision par ordinateur est un domaine de l'IA qui consiste à apprendre aux
systèmes informatiques à voir et à interpréter des images comme un être humain [1]."

### Pattern 2 : Présentation d'une architecture/méthode
1. Définition générale + citation
2. Principe de fonctionnement (en prose, 3-5 phrases)
3. Figure illustrative (\includegraphics + \caption)
4. Avantages/limites OU pourquoi nous l'avons choisi

### Pattern 3 : Présentation d'un résultat numérique
"Les résultats obtenus montrent que [méthode] atteint [X\%] de [métrique], ce qui représente
une amélioration de [delta] par rapport à [référence/baseline]."
OU
"D'après le tableau \ref{tab:X}, l'approche [Y] obtient les meilleures performances avec
[X\%] d'accuracy et un F1-macro de [Y\%]."

### Pattern 4 : Conclusion de section (micro-conclusion)
Chaque section importante se termine par une phrase de synthèse :
"À travers cette section, nous avons présenté [sujet]. Dans la section suivante, nous
aborderons [section suivante]."

### Pattern 5 : Introduction d'un tableau ou figure
AVANT le tableau/figure :
"Le tableau \ref{tab:X} [ci-dessous / suivant] présente [ce que le tableau montre]."
OU
"La figure \ref{fig:X} illustre [ce que la figure montre]."
APRÈS le tableau/figure : commentaire d'analyse obligatoire

---

## Checklist qualité avant de soumettre une réponse

**Contenu :**
- [ ] Le texte utilise "nous" (pas "je" ni "on")
- [ ] Le ton est formel et scientifique (pas de langage familier)
- [ ] Les chiffres/métriques cités correspondent aux données du projet (voir projet_context.md)
- [ ] Chaque définition est suivie d'une citation \cite{}
- [ ] Les choix techniques sont justifiés (pas juste décrits)

**Structure :**
- [ ] La section commence par une phrase d'annonce du contenu
- [ ] Les transitions entre paragraphes sont fluides
- [ ] Si c'est une intro/conclusion de chapitre, le template est respecté

**LaTeX :**
- [ ] Le code LaTeX est syntaxiquement correct (accolades fermées, \\\\ en fin de ligne de tableau)
- [ ] Les figures et tableaux sont référencés dans le texte (\ref{})
- [ ] Chaque figure/tableau est introduit AVANT et commenté APRÈS dans le texte
- [ ] Les labels sont cohérents : fig:nom_figure, tab:nom_tableau, lst:nom_code

---

## Références internes

- `references/projet_context.md` — Données techniques complètes du projet (architecture,
  métriques, dataset, résultats vidéo)
- `references/structure_chapitres.md` — Plan détaillé des 5 chapitres avec contenu suggéré
  pour chaque section
