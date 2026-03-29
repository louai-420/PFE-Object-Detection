---
name: memoire-tsi-algerie
description: Méthodologie pour la rédaction et l'aide au mémoire de fin de stage en informatique (TSI, BTS) dans le cadre de la formation professionnelle algérienne (CFPA, INSFP).
---

# Méthodologie du Mémoire de Fin de Stage — Informatique (Algérie)

## Déclencheurs (Quand utiliser ce skill)
Utilise ce skill **TOUJOURS** quand l'utilisateur :
- Parle de son mémoire de fin de stage ou de fin de formation.
- Demande comment rédiger une introduction, problématique, conclusion, ou un chapitre.
- Pose des questions sur la structure d'un mémoire (page de garde, sommaire, bibliographie…).
- Demande de l'aide sur la méthode Merise (MCD, MLD, diagramme de flux, étude de l'existant).
- Veut générer ou corriger une partie de son mémoire.
- Demande des conseils de mise en forme Word pour un document académique.
- Mentionne un organisme d'accueil, un encadreur, un promoteur, une soutenance.
- Demande un modèle ou exemple de page de garde algérienne.
- Pose des questions connexes comme "comment écrire ma problématique", "c'est quoi un MCD", "structure d'un rapport de stage TSI", "comment faire un sommaire Word".

## 1. Contexte d'utilisation
Ce skill couvre la rédaction complète du mémoire de fin de formation pour l'obtention du **Diplôme de Technicien Supérieur en Informatique (ou BTS équivalent)** dans les établissements de formation professionnelle algériens (CFPA, INSFP, instituts privés agréés). 
Le stage se déroule au semestre 5, en alternance entre une entreprise d'accueil et l'établissement.

### Calendrier et organisation du stage
**Avant la fin du semestre 4**
*   Trouver une entreprise d'accueil capable de fournir un sujet adapté (ni trop simple, ni trop complexe).
*   Choisir les deux encadreurs : un côté entreprise, un côté école.
*   Choisir son binôme (critères : niveau, proximité géographique, disponibilité).

**Au début du semestre 5**
*   Valider le sujet auprès de l'école dans les plus brefs délais.
*   Établir une ligne directrice avec le binôme : planning des déplacements, distribution des tâches, langage commun utilisé (Merise, UML…).

**Déroulement**
1.  **Étude et conception** (UML / Merise).
2.  **Rédaction du mémoire** en parallèle.
3.  **Réalisation de l'application** ou mise en place de l'infrastructure.
4.  **Résumé du travail** pour la pré-soutenance.

---

## 2. Structure complète du mémoire
Le mémoire contient les parties suivantes dans cet ordre exact :

| Partie | Détail |
| :--- | :--- |
| **1. Page de garde cartonnée** | Couverture officielle de présentation. |
| **2. Page de garde (feuille)** | Même contenu, papier normal. |
| **3. Remerciements** | 1 page. |
| **4. Dédicaces** | 1 à 2 pages. |
| **5. Sommaire** | + liste des figures si nécessaire. |
| **6. Introduction générale** | Présentation du sujet + Problématique + Objectifs. |
| **7. Chapitre 1** | Présentation de l'organisme d'accueil. |
| **8. Chapitre 2** | Étude de l'existant. |
| **9. Chapitre 3** | Conception du nouveau système (Merise/UML). |
| **10. Chapitre 4** | Réalisation. |
| **11. Conclusion générale** | Bilan et perspectives. |
| **12. Bibliographie** | Citations et sources. |

*Note sur la numérotation des pages :* elle commence au Chapitre 1 mais en tenant compte des pages précédentes. Exemple : 2 pages de garde + remerciements + dédicaces + intro = environ 8 pages ⇒ commencer la numérotation du Chapitre 1 à la page 9.

---

## 3. Contenu détaillé de chaque partie

### Page de garde
Doit obligatoirement contenir :
*   République Algérienne Démocratique et Populaire
*   Ministère de la Formation et de l'Enseignement Professionnels
*   Établissement de formation (ex: INSFP Sétif, CFPA Tizi Ouzou...)
*   Diplôme visé et option (ex : Technicien Supérieur en Base de Données)
*   Thème (titre du projet)
*   Organisme d'accueil
*   Réalisé par (noms des stagiaires), Encadreur (entreprise), Promoteur (école)
*   Année de promotion (ex : 2022 – 2024)

### Remerciements & Dédicaces
*   **Remerciements :** Remercier l'encadreur, le promoteur, le jury et les personnes ayant contribué techniquement au projet. Formule type : *"Nous tenons à adresser nos remerciements..."*
*   **Dédicaces :** Expression de gratitude personnelle (famille, amis). Doit être sobre.

### Introduction générale
Structure en 3 temps :
1.  **Contexte général (1-2 §) :** Apport de l'informatique dans la gestion des entreprises.
2.  **Présentation du travail (1 §) :** Ce qui sera réalisé, présentation rapide du sujet, et la **Problématique** détaillée (voir section 4).
3.  **Annonce du plan :** *"Notre mémoire est structuré en quatre chapitres : …"*

### Chapitre 1 — Présentation de l'organisme d'accueil
*   Historique et mission de l'entreprise.
*   Structure organisationnelle (organigramme détaillé).
*   Situation informatique actuelle (parc matériel et logiciels existants).
*   Moyens humains.

### Chapitre 2 — Étude de l'existant
Étape préalable indispensable comprenant le diagnostic du système actuel :
*   Flux d'information (diagramme de flux + légende + tableau descriptif des flux).
*   Étude des postes de travail.
*   Étude des documents utilisés (formulaires, registres…).
*   Codification existante.
*   **Diagnostic :** critiques et suggestions (points faibles et insuffisances du système actuel).

### Chapitre 3 — Conception du nouveau système (Méthode Merise)
Phase analytique et conceptuelle :
*   Solution informatique projetée.
*   Nouvelle codification proposée.
*   Nouveau diagramme de flux (si le processus métier est modifié).
*   Tableau descriptif des services et tâches automatisées.
*   **Dictionnaire des données** (toutes les données recensées).
*   **Règles de gestion** (contraintes métiers).
*   **MCD** (Modèle Conceptuel des Données).
*   **MLD** (Modèle Logique des Données).

### Chapitre 4 — Réalisation
*   Présentation des outils utilisés (SGBD ex: MySQL, langage/framework ex: Laravel, React).
*   Script de création de la base de données ou schéma physique.
*   Captures d'écran commentées : page d'authentification, accueil, interfaces principales, impressions d'états.

### Conclusion générale
*   Répond à la problématique posée dans l'introduction.
*   Résume les compétences acquises par les stagiaires et le travail réalisé.
*   Ouvre sur des perspectives futures ou des améliorations possibles de l'application.

### Bibliographie
Classer par ordre alphabétique d'auteurs. Format standard :
*   Nom de l'auteur, *Titre de l'ouvrage ou de l'article*, Date de publication.
*   Pour le web : Titre du site, URL, [Date de consultation].

---

## 4. Rédiger la problématique
La problématique identifie les dysfonctionnements du système actuel découverts lors des entretiens.
**Formules courantes :**
*"Suite aux entretiens avec les responsables du département [X], nous avons pu identifier les problèmes suivants :"*
*   Difficulté à suivre / gérer / traiter…
*   Perte de temps / de données lors de la recherche d'informations…
*   Incapacité à produire des statistiques fiables sur…
*   Manque de traçabilité concernant…
*   Absence d'un système centralisé…
*   Processus manuel très lent et sujet aux erreurs humaines…

---

## 5. Méthode Merise — Rappels essentiels

### Diagramme de flux
Représentation graphique des acteurs et de l'information.
*   **Acteurs :** entités internes ou externes (service achats, client, stock).
*   **Flux :** flèches numérotées représentant un document ou une donnée transmise.
*   **Tableau descriptif :** N° Flux | Émetteur | Récepteur | Nature du flux.

### Dictionnaire des données
Tableau recensant toutes les données :
| Mnémonique | Désignation | Type | Taille | Remarque |
| :--- | :--- | :--- | :--- | :--- |
| num_cmd | Numéro de commande | N | 6 | Clé primaire |

### Règles de gestion
Contraintes métier en langage naturel. *(Ex : "Un client peut passer plusieurs commandes. Une commande appartient à un seul client.")*

### MCD (Modèle Conceptuel des Données)
*   **Entité :** Objet réel en MAJUSCULES, au singulier (CLIENT, PRODUIT).
*   **Association :** Lien verbal (passer, contenir, livrer).
*   **Cardinalités :** (0,1), (1,1), (0,N), (1,N).

### MLD (Modèle Logique des Données)
Traduction du MCD vers le modèle relationnel :
1.  Chaque entité devient une table (identifiant = clé primaire soulignée).
2.  Association (1,N)–(0,1 ou 1,1) : La clé primaire côté N migre comme clé étrangère (précédée de #) vers le côté 1.
3.  Association (1,N)–(0,N ou 1,N) : Création d'une table de jonction dont la clé primaire est la concaténation des deux clés étrangères.

---

## 6. Mise en forme Word — Règles académiques algériennes
| Élément | Valeur recommandée |
| :--- | :--- |
| **Police corps de texte** | 12 ou 13 pt, style Normal (Times New Roman ou Arial) |
| **Police titres** | 14 ou 15 pt, Gras + Souligné |
| **Interligne** | 1,5 |
| **Marges** | 2,5 cm partout (haut, bas, gauche, droite) |
| **Alignement** | Justifié |
| **Espacement paragraphes** | 1 à 2 lignes vides entre paragraphes |
| **Retrait 1ère ligne** | Touche Tabulation (alinéa) |

**Règles de ponctuation :**
*   `.` et `,` : pas d'espace avant, un espace après.
*   `:` `;` `?` `!` : un espace avant ET un espace après (règle française stricte).

**Actions Word essentielles :**
*   **Numéro de page :** Insertion → Numéro de page.
*   **Entête/pied différent :** Créer un saut de section (Mise en page → Sauts de page → Section page suivante), puis désactiver "Lier au précédent".
*   **Sommaire automatique :** Appliquer les styles Titre 1, Titre 2, puis Références → Table des matières.

---

## 7. Conseils et Erreurs à éviter
✅ **Bonnes pratiques :**
*   Prendre des notes tout au long du stage, faire des synthèses régulières.
*   Aérer le texte : paragraphes courts, listes à puces, tableaux, captures d'écran.
*   Faire relire le mémoire par un tiers (encadreur) avant validation finale.

❌ **Erreurs critiques :**
*   **Plagiat :** L'utilisation de textes copiés non sourcés est éliminatoire (logiciels anti-plagiat utilisés).
*   **Copier-coller IA brut :** OpenAI dispose d'outils de détection ; le texte doit être retravaillé et personnel.
*   **Dépassement de délai :** Un mémoire fait environ 60 pages, impossible à écrire la dernière semaine.

---

## 8. Génération de contenu — Comportement attendu du LLM (Toi)
Quand l'utilisateur demande de l'aide pour rédiger son mémoire, voici comment tu dois procéder :

1.  **Si l'utilisateur demande un modèle ou un exemple :**
    *   Fournir un exemple concret adapté au contexte algérien (exemples fréquents : gestion de stock, gestion de scolarité, pointage RH, facturation).
2.  **Si l'utilisateur demande de rédiger une section :**
    *   Demander d'abord : le nom de l'entreprise, le secteur d'activité, le sujet précis du projet.
    *   Produire un texte bien structuré, en français académique et professionnel, prêt à être copié dans Word.
3.  **Si l'utilisateur pose une question conceptuelle (MCD, diagramme de flux…) :**
    *   Expliquer brièvement la règle.
    *   Immédiatement proposer un exemple appliqué au projet de l'utilisateur.
4.  **Si l'utilisateur veut corriger ou améliorer un texte existant :**
    *   Corriger l'orthographe, la grammaire, la structure et le style pour qu'il soit académique.
    *   S'assurer que le texte respecte les règles de ponctuation strictes (espaces avant les `:` et `?`).

---

## 9. Exemple de Sommaire Complet
```text
Introduction Générale
  1. Présentation du sujet
  2. Problématique et objectifs

Chapitre N°1 : Présentation de l'organisme d'accueil ............ 9
  1.1 Présentation générale .................................................. 10
  1.2 Organisation et structure ............................................ 12
  1.3 Situation informatique ................................................. 15

Chapitre N°2 : Étude de l'existant ........................................ 18
  2.1 Flux d'information ....................................................... 20
  2.2 Étude des postes et documents .................................... 24
  2.3 Diagnostic de l'existant ............................................... 30

Chapitre N°3 : Conception du nouveau système .................. 34
  3.1 Solution projetée et codification .................................. 36
  3.2 Dictionnaire des données et règles de gestion ............. 40
  3.3 MCD et MLD .............................................................. 47

Chapitre N°4 : Réalisation .................................................... 55
  4.1 Environnement de développement ............................... 57
  4.2 Base de données .......................................................... 60
  4.3 Présentation de l'application ....................................... 64

Conclusion générale
Bibliographie
```
