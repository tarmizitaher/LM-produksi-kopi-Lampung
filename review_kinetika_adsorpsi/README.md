# Review Kinetika Adsorpsi

Narrative review (Bahasa Indonesia, target jurnal terakreditasi SINTA) tentang model
kinetika adsorpsi, mengikuti gaya tinjauan Foo & Hameed (2010) untuk isoterm.
Proyek ini **terpisah** dari riset CHIRPS-ML kopi Lampung di root repo.

## Struktur
```
review_kinetika_adsorpsi/
├── README.md
├── manuscript/
│   ├── main.tex          # Naskah (kerangka + persamaan inti, bagian [TODO] belum ditulis)
│   └── references.bib    # BibTeX (lihat status verifikasi di kepala file)
└── docs/
    └── reference_list.md # Daftar referensi terverifikasi + kandidat yang belum dicek
```

## Kompilasi
Butuh TeX Live (`texlive-latex-extra`, `texlive-lang-other`, `texlive-bibtex-extra`),
`biber`, dan `latexmk`.

```bash
cd review_kinetika_adsorpsi/manuscript
latexmk -pdf main.tex      # hasil: main.pdf
latexmk -c                 # hapus file sementara
```

PDF dan file sementara LaTeX tidak di-commit (lihat `.gitignore`).

## Konvensi
- Bahasa Indonesia baku (PUEBI); abstrak dua bahasa (Indonesia + Inggris).
- Gaya sitasi APA 7 (`biblatex-apa`); kunci sitasi `PenulisTahun_TopikSingkat`.
- **Jangan menulis entri BibTeX dari ingatan.** Ambil dari CrossRef berdasarkan DOI.
- Satuan dengan `siunitx`, tabel gaya tiga garis (`booktabs`).
