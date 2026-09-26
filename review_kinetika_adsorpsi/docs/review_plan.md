# Review Plan: Adsorption Kinetics (Liquid-Phase Batch)

## Decisions (2026-09-26)
| Topic | Decision |
|---|---|
| Language | English (American) |
| Type | Narrative review |
| Angle | **A + B**: practitioner's workflow (design, fitting, selection, reporting) and a unifying framework that organizes models by rate-limiting step and shows how they relate |
| Differentiator | Reproducible re-analysis of 3–5 published datasets, with open Python code in `analysis/` |
| Scope | **Liquid-phase, batch, single-solute** only. Fixed-bed column and gas-phase kinetics are excluded |
| Target | International journal, still to be decided |
| Length | ~8,000–10,000 words, 5–6 figures, 4 tables |

## Why this angle
Existing reviews already cover:
- a catalog of 16 models (Wang & Guo, 2020);
- the PFO vs PSO comparison (Simonin, 2016);
- common mistakes (Tran et al., 2017).

None of them links each model's physical basis to a tested, end-to-end workflow.

## Section plan
| # | Section | Key content | Figures/Tables |
|---|---|---|---|
| 1 | Introduction | Why PSO "always wins"; gap; scope | — |
| 2 | Physical basis | Batch mass balance, resistances in series, diagnosing the controlling step | Fig. 1 schematic |
| 3 | Surface-reaction models | Langmuir kinetics (parent), PFO, PSO, mixed/nth order, Elovich, Avrami | — |
| 4 | Diffusion models | Film, Boyd, Weber–Morris, HSDM | — |
| 5 | Linking the models | Limiting cases; one curve fitted by many models | Fig. 2 model map, Fig. 3 synthetic fits |
| 6 | Parameter estimation | Linear vs non-linear, AICc/BIC, residuals, uncertainty, experimental design | Fig. 4 workflow |
| 7 | Re-analysis | 3–5 published datasets refitted | Tables 2–3, Fig. 5 |
| 8 | Pitfalls and checklist | Reporting checklist | Table 4 |
| 9 | Outlook | Open solvers, multicomponent systems, data-driven selection | — |
| 10 | Conclusions | — | — |
| — | Model summary | — | Table 1 |

## Open items
- [ ] Choose target journal (candidates to compare: scope, length limits, APC)
- [ ] Find and verify original sources: Lagergren 1898, Weber & Morris 1963, Boyd et al. 1947,
      Elovich, Avrami, Azizian 2004 (Langmuir-kinetics limits), mixed-order model
- [ ] Select re-analysis datasets (need tabulated q_t vs t, or supplementary data)
- [ ] Re-verify all BibTeX entries via CrossRef (blocked in cloud environment)
