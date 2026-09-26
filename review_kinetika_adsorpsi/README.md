# Adsorption Kinetics Review

Narrative review (English) of adsorption kinetic models, modeled on the style of
Foo & Hameed (2010) for isotherms. This project is **separate** from the CHIRPS-ML
coffee study at the repository root.

## Structure
```
review_kinetika_adsorpsi/
├── README.md
├── manuscript/
│   ├── main.tex          # Manuscript (outline + core equations; [TODO] parts unwritten)
│   └── references.bib    # BibTeX (see verification status at top of file)
└── docs/
    └── reference_list.md # Verified references + unchecked candidates
```

## Build
Requires TeX Live (`texlive-latex-extra`, `texlive-bibtex-extra`), `biber`, and `latexmk`.

```bash
cd review_kinetika_adsorpsi/manuscript
latexmk -pdf main.tex      # output: main.pdf
latexmk -c                 # remove auxiliary files
```

The PDF and LaTeX auxiliary files are not committed (see `.gitignore`).

## Conventions
- American English.
- APA 7 citations (`biblatex-apa`); citation keys `AuthorYear_ShortTopic`.
- **Never write BibTeX entries from memory.** Fetch them from CrossRef by DOI.
- Units with `siunitx`; three-line tables with `booktabs`.
