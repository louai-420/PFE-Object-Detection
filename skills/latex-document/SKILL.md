---
name: latex-document
description: >
  Creates, compiles, debugs, and structures LaTeX documents (academic memoirs,
  theses, reports, articles). Handles XeLaTeX/pdfLaTeX compilation, figure
  placement, table of contents, bibliography, multilingual support (Arabic/French),
  and INSFP/university formatting standards. Use when the user works with .tex
  files, asks to create/fix/compile LaTeX documents, or needs help with document
  structure. Do NOT use for general text editing, HTML/CSS, or non-LaTeX tasks.
tags: [latex, academic, typesetting, memoir, xelatex, compilation]
version: 1.0.0
---

# LaTeX Document Skill

Expert-level LaTeX document creation, compilation, debugging, and professional formatting for academic and technical documents.

---

## Use this skill when
- User works with `.tex` files or mentions LaTeX/XeLaTeX/pdfLaTeX
- User asks to create, modify, compile, or debug a LaTeX document
- User needs a thesis, memoir, report, or academic paper formatted
- User asks about table of contents, figures, bibliography, or document structure
- User mentions INSFP, mémoire de fin de formation, or Algerian academic standards
- User needs multilingual support (Arabic + French) in LaTeX
- User asks to convert documents (DOCX/Markdown) to LaTeX
- User needs help with LaTeX packages, errors, or compilation issues

## Do NOT use when
- User is working on HTML/CSS web documents (use frontend skills instead)
- User wants general text editing without LaTeX
- User is building slides in PowerPoint (unless converting to Beamer)
- User asks conceptually about LaTeX without wanting a document produced

---

## Instructions

### 1. Analyze the document requirements
- Determine the document type: report, article, book, memoir, beamer
- Identify the compilation engine needed: `pdflatex`, `xelatex`, or `lualatex`
- Check for multilingual needs (Arabic → requires XeLaTeX + `fontspec` + `polyglossia` or `babel`)
- Identify required packages based on content (figures, tables, code, math)

### 2. Choose the correct document class and setup
```latex
% Academic memoir/thesis (INSFP standard):
\documentclass[12pt,a4paper]{report}
\usepackage[margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing  % interligne 1.5

% Short paper/article:
\documentclass[12pt,a4paper]{article}

% Presentation:
\documentclass[aspectratio=169]{beamer}
```

### 3. Handle compilation engine detection
```latex
% Always add engine detection for portability:
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage{lmodern}
\else
  \usepackage{unicode-math}
  \defaultfontfeatures{Scale=MatchLowercase}
\fi
```

### 4. Structure the document properly
For academic memoirs, follow this exact structure:

| Part | LaTeX Command | TOC |
|------|--------------|-----|
| Page de garde | Manual formatting | No |
| Remerciements | `\chapter*{Remerciements}\addcontentsline{toc}{chapter}{Remerciements}` | Yes |
| Dédicaces | `\chapter*{Dédicaces}\addcontentsline{toc}{chapter}{Dédicaces}` | Yes |
| Sommaire | `\tableofcontents` | Auto |
| Liste des figures | `\listoffigures` | Auto |
| Introduction Générale | `\chapter*{Introduction Générale}\addcontentsline{toc}{chapter}{Introduction Générale}` | Yes |
| Chapitres 1-4 | `\chapter{Titre}` | Auto |
| Sections | `\section{Titre}` / `\subsection{Titre}` | Auto |
| Conclusion Générale | `\chapter*{Conclusion Générale}\addcontentsline{toc}{chapter}{Conclusion Générale}` | Yes |
| Bibliographie | `\chapter*{Bibliographie}\addcontentsline{toc}{chapter}{Bibliographie}` | Yes |

**CRITICAL**: NEVER use `\textbf{\ul{...}}` for headings. ALWAYS use `\chapter{}`, `\section{}`, `\subsection{}`. Otherwise `\tableofcontents` will be empty.

### 5. Insert figures correctly
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.90\textwidth]{figures/filename.jpg}
  \caption{Description de la figure}
  \label{fig:label}
\end{figure}
```
Rules:
- Place figures AFTER the paragraph that references them, near `(Voir Figure X)`
- Use `[htbp]` placement — never force `[H]` unless absolutely necessary
- Always add `\caption{}` and `\label{}` for automatic `\listoffigures`
- Prefer PNG/JPG for screenshots, SVG→PNG for diagrams
- Use relative paths: `figures/filename.png`

### 6. Handle tables
```latex
% For tables that need to break across pages:
\usepackage{longtable,booktabs,array}

% For simple tables:
\begin{table}[htbp]
  \centering
  \begin{tabular}{|l|l|l|}
    \hline
    Col 1 & Col 2 & Col 3 \\ \hline
  \end{tabular}
  \caption{Titre du tableau}
  \label{tab:label}
\end{table}
```

### 7. Compile the document
```bash
# Standard compilation (2 passes for TOC/references):
xelatex -interaction=nonstopmode document.tex
xelatex -interaction=nonstopmode document.tex

# With bibliography:
xelatex document.tex
biber document        # or bibtex document
xelatex document.tex
xelatex document.tex
```
Always run **at least 2 passes** for proper TOC page numbers.

### 8. Debug common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing \begin{document}` | Preamble syntax error | Check for unclosed braces before `\begin{document}` |
| `Undefined control sequence` | Missing package | Add the required `\usepackage{}` |
| `File not found` | Wrong image path | Check path is relative, case-sensitive |
| `soul package error` (XeLaTeX) | `soul` incompatible with XeLaTeX | Replace `\ul{}` with `\underline{}` or use conditional loading |
| `headheight too small` | `fancyhdr` needs more space | Add `\setlength{\headheight}{15pt}` |
| `lmodern` error (XeLaTeX) | `lmodern` is for pdfLaTeX only | Wrap in `\ifPDFTeX...\fi` |
| Arabic text not rendering | Need XeLaTeX + fontspec | Use `xelatex` compiler, load `fontspec` |
| TOC empty | Headings use `\textbf{}` not `\chapter{}` | Convert to proper structural commands |
| Figures in wrong position | Forced placement or float issue | Use `[htbp]`, add `\clearpage` if needed |

### 9. INSFP / Algerian academic standards
- **Police**: Times New Roman 12pt (or Computer Modern)
- **Marges**: 2.5 cm tous les côtés
- **Interligne**: 1.5
- **Numérotation**: Chapitres en chiffres arabes, Annexes en lettres
- **Sommaire**: Doit contenir chapitres, sections, sous-sections avec N° page
- **Structure obligatoire**: Introduction → 4 Chapitres → Conclusion → Bibliographie
- **Figures**: Numérotées et référencées dans le texte
- **En-tête/pied de page**: N° page en haut à droite via `fancyhdr`

---

## Constraints

- **NEVER** delete or overwrite the user's existing `.tex` file without creating a backup or new version (e.g., `v2.tex`, `v3.tex`)
- **ALWAYS** compile with 2 passes minimum for TOC accuracy
- **NEVER** use `\textbf{\ul{...}}` for structural headings — always use `\chapter`, `\section`, `\subsection`
- **ALWAYS** detect compilation engine (pdfLaTeX vs XeLaTeX) and load packages conditionally
- **NEVER** hardcode page numbers in the sommaire — use `\tableofcontents`
- **DO NOT** include binary files (.pdf, .aux, .log) in suggestions — only edit `.tex` source
- **ALWAYS** preserve the original encoding (UTF-8) and line endings

---

## Examples

### Example 1 — Create a new academic memoir
**Input:** "Crée un mémoire LaTeX pour l'INSFP avec 4 chapitres"
**Expected action:** Create a complete `.tex` file with report class (12pt, a4paper), 2.5cm margins, 1.5 spacing, fancyhdr, page de garde, remerciements, sommaire auto, 4 chapitres avec sections/subsections, conclusion, biblio. Compile with XeLaTeX (2 passes).

### Example 2 — Fix empty table of contents
**Input:** "Le sommaire est vide dans mon PDF"
**Expected action:** Identify that headings use `\textbf{}` instead of `\chapter{}`/`\section{}`. Convert all headings to proper LaTeX commands with `\addcontentsline` for unnumbered chapters. Recompile with 2 passes.

### Example 3 — Insert figures
**Input:** "Place les figures du dossier figures/ dans le mémoire"
**Expected action:** List all images in `figures/`, match them to `(Voir Figure X)` or section titles in the `.tex`, insert `\begin{figure}[htbp]...\end{figure}` blocks with correct captions and labels. Recompile.

### Example 4 — Debug compilation error
**Input:** "J'ai une erreur avec soul et XeLaTeX"
**Expected action:** Add conditional loading: `\ifPDFTeX \usepackage{soul} \else \newcommand{\ul}[1]{\underline{#1}} \fi`. Recompile.

### Example 5 — NOT a LaTeX task (should NOT trigger)
**Input:** "Crée un composant React pour le dashboard"
**Expected action:** Do NOT use this skill. Use a frontend skill instead.

---

## Output Format

When creating or modifying a LaTeX document:
1. **Modified `.tex` file** — with all changes applied
2. **Compilation command** — exact `xelatex`/`pdflatex` command to run
3. **Compilation result** — page count and any warnings
4. **Summary of changes** — bullet list of what was modified

When debugging:
1. **Error diagnosis** — what the error means
2. **Fix applied** — code diff or description
3. **Verification** — successful compilation output

---

## Safety

- Always create a **new version** (`_v2.tex`, `_v3.tex`) rather than overwriting when making major structural changes
- Request confirmation before running compilation commands on user's system
- Never modify files outside the project directory
- Log all figure insertions and heading conversions for user review

---

## Package Reference (Quick)

| Need | Package | Notes |
|------|---------|-------|
| Margins | `geometry` | `\usepackage[margin=2.5cm]{geometry}` |
| Spacing | `setspace` | `\onehalfspacing` |
| Headers | `fancyhdr` | Set `\headheight{15pt}` |
| Figures | `graphicx` | Required for `\includegraphics` |
| Tables | `longtable`, `booktabs` | For multi-page and professional tables |
| Links | `hyperref` | Load LAST, use `hidelinks` option |
| Colors | `xcolor` | For colored text |
| Math | `amsmath`, `amssymb` | Standard math support |
| Code | `listings` or `minted` | Code highlighting |
| Fonts (XeLaTeX) | `fontspec` | System font access |
| Multilingual | `polyglossia` or `babel` | Arabic/French/English |
| Underline | `soul` (pdfLaTeX only) | Use `\underline` for XeLaTeX |
| Bookmarks | `bookmark` | PDF bookmarks |
| URLs | `url`, `xurl` | Line-breaking URLs |
