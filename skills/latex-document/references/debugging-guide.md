# LaTeX Debugging Guide — Quick Reference

## Compilation Order
```bash
# Standard (2 passes):
xelatex doc.tex && xelatex doc.tex

# With bibliography (4 passes):
xelatex doc.tex && biber doc && xelatex doc.tex && xelatex doc.tex
```

## Error — "Missing \begin{document}"
**Cause**: Syntax error in the preamble (unclosed brace, bad package option).
**Fix**: Check every line between `\documentclass` and `\begin{document}`. Look for unmatched `{`.

## Error — "soul" / XeLaTeX conflict
```latex
\ifPDFTeX
  \usepackage{soul}
\else
  \newcommand{\ul}[1]{\underline{#1}}
\fi
```

## Error — "lmodern" / XeLaTeX conflict
```latex
\ifPDFTeX
  \usepackage{lmodern}
\fi
```

## Error — "headheight too small"
```latex
\setlength{\headheight}{15pt}  % After loading fancyhdr
```

## Error — TOC is empty
All headings must use `\chapter{}`, `\section{}`, `\subsection{}`.
For unnumbered chapters that should appear in TOC:
```latex
\chapter*{Title}
\addcontentsline{toc}{chapter}{Title}
```

## Error — Figures not showing
1. Check path: `figures/name.png` (case-sensitive!)
2. Check format: XeLaTeX supports PNG, JPG, PDF (not EPS)
3. Check file exists: `ls figures/`

## Error — Arabic text not rendering
- Must use `xelatex` (not `pdflatex`)
- Load `fontspec` package
- For Arabic-specific fonts, use `polyglossia` with `\setotherlanguage{arabic}`

## Warning — "Float too large for page"
```latex
\includegraphics[width=0.85\textwidth]{...}  % Reduce width
% Or use \clearpage before/after large floats
```

## Warning — "Underfull \hbox"
Usually harmless. If bothersome:
```latex
\setlength{\emergencystretch}{3em}
\sloppy  % More aggressive line breaking
```
