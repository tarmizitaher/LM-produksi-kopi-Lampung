# Reference & Bibliography Rules

## Golden Rule
**NEVER generate BibTeX entries from memory.** All bibliographic data has hallucination risk — wrong year, wrong volume, wrong authors, wrong page numbers. Even if you "know" a reference, you must verify.

## Required Workflow

### When adding a reference:
1. **DOI available** → Fetch from CrossRef API:
   ```
   curl -sL "https://api.crossref.org/works/{DOI}/transform/application/x-bibtex"
   ```
2. **DOI not available** → Search CrossRef by title:
   ```
   curl -sL "https://api.crossref.org/works?query.title={TITLE}&rows=3"
   ```
   Then confirm the correct match with the user before fetching the BibTeX.

3. **CrossRef returns nothing** → Flag to user. Do NOT fabricate the entry. Suggest the user manually export from Scopus/Google Scholar.

### Quality checks after fetching:
- Verify author names look correct (no encoding artifacts)
- Verify year matches what the paper says
- Verify journal name is not abbreviated inconsistently
- Add `doi = {}` field if missing from the fetched result

## Storing References
- All BibTeX entries go in `docs/references.bib`
- Maintain a human-readable reference list in `docs/reference_list.md` with: Author (Year), Title, Journal, DOI
- When citing in manuscripts/reports, use the citation key from the .bib file

## Citation Key Format
- Pattern: `AuthorYear_ShortTopic` (e.g., `Funk2015_CHIRPS`, `Marzuki2025_IndonesiaRainfall`)
- For 3+ authors: first author only + "etal" is acceptable in discussion, not in bib entry

## What IS allowed without CrossRef:
- Citation keys in manuscript text — these are just labels
- Suggesting which papers to cite — this is intellectual, not bibliographic
- Discussing paper content and findings
- Noting DOIs from web search results (these are machine-provided, not hallucinated)

## What is NOT allowed:
- Writing `@article{...}` blocks from memory
- Guessing volume, issue, or page numbers
- Filling in incomplete BibTeX fields with assumed data
- Copying BibTeX from training data (it may be outdated or wrong)

## Web Search for References
When searching for papers:
1. **Always use WebSearch** — never rely solely on training data for recent papers
2. **Verify paper exists** — confirm via DOI link or publisher URL
3. **Record the DOI immediately** — DOI is the ground truth identifier
4. **Note access status** — open access vs paywalled affects user's ability to read
5. **Prefer recent papers** (2020-2026) but include foundational references (e.g., Funk et al. 2015 for CHIRPS)
6. **Search multiple queries** — try different keyword combinations to avoid missing relevant work:
   - Topic-specific: "CHIRPS machine learning crop yield"
   - Method-specific: "random forest precipitation prediction tropical"
   - Region-specific: "rainfall Indonesia Lampung Sumatra"
7. **Cross-check citing papers** — if a key paper is found, check who cited it for more recent work

## Reference Categories for This Project
Maintain references organized by topic:
- **CHIRPS validation** — studies validating CHIRPS against ground stations
- **ML crop yield** — ML/DL approaches for crop yield prediction
- **Coffee & climate** — climate impact on coffee production
- **Drought indices** — SPI, SPEI methodology and applications
- **ENSO/IOD Indonesia** — teleconnection impacts on Indonesian rainfall
- **Satellite precipitation** — general satellite rainfall comparison studies
