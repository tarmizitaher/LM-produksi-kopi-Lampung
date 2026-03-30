# Manuscript Writing Style Rules

## Language & Spelling
- **American English** throughout (e.g., "analyze" not "analyse", "color" not "colour")
- Be consistent — never mix British and American spellings in the same document

## Tense Conventions
- **Present tense** for established facts and general truths:
  "CHIRPS provides gridded precipitation estimates at 0.05° resolution"
- **Past tense** for specific study results and completed actions:
  "The model achieved an R² of 0.82 on the test set"
  "Marzuki et al. (2025) analyzed 43 years of CHIRPS data"
- **Present perfect** for cumulative research trends:
  "Several studies have demonstrated the utility of satellite precipitation for crop monitoring"
- Never mix tenses within the same paragraph for the same type of statement

## Voice & Tone
- **Objective-analytical tone** — always evaluate, not just describe
- Active voice preferred: "We developed...", "The model predicted...", "Our analysis reveals..."
- Passive voice acceptable for methodology: "Data were preprocessed using..."
- Avoid hedging stacks — one hedge per claim maximum:
  - BAD: "It could possibly be suggested that this might indicate..."
  - GOOD: "This suggests..." or "This may indicate..."

## Sentence Structure
- Vary sentence length. Follow a long complex sentence with a short punchy one
- Avoid starting consecutive sentences with the same word
- No more than 3 items in a running list; use numbered format for 4+ items

## Terminology Consistency
Use these terms consistently throughout — never alternate:

| Use This | NOT This |
|----------|----------|
| CHIRPS (after first mention of full name) | CHIRPSv2, CHIRPS2 |
| precipitation | rainfall (use "precipitation" in technical context, "rainfall" in general) |
| productivity (kg/ha) | yield (unless quoting other studies that use "yield") |
| Robusta coffee | robusta coffee (capitalize cultivar name) |
| machine learning (ML) | Machine Learning, machine-learning |
| Random Forest (RF) | random forest (capitalize model names) |
| XGBoost | XGboost, xgboost (in text; lowercase ok in code) |
| feature importance | variable importance, predictor importance |
| SPI (after first definition) | standardized precipitation index |
| ENSO (after first definition) | El Niño-Southern Oscillation |
| IOD (after first definition) | Indian Ocean Dipole |
| study area | study region, research area |
| ground station / gauge station | weather station (be specific) |
| satellite-based | satellite based (always hyphenated as adjective) |
| Leave-One-Year-Out | leave one year out (hyphenated as compound modifier) |

## Numbers & Units
- Spell out numbers below 10 in running text, unless followed by a unit
- Use "approximately" or "~" but not "about" or "around"
- Precipitation: mm for depth, mm/month or mm/year for rate
- Productivity: kg/ha
- Area: ha (hectares)
- Coordinates: °E, °S with degree symbol
- Model metrics: report to 2-3 decimal places (R² = 0.82, RMSE = 45.3 mm)
- Always specify units with numbers: "117,090 tons" not "117,090"

## Citations
- Citation key format: `AuthorYear_ShortTopic` (e.g., `Funk2015_CHIRPS`)
- Never stack more than 4 citations in one bracket — select the most relevant
- When citing specific data, always cite the original source, not a review that compiled it
- For CHIRPS, always cite: Funk et al. (2015)
- For SPI, always cite: McKee et al. (1993)

## Redundancy Prevention
- Never repeat the same data point in more than one section (cross-reference instead)
- Avoid restating what a table or figure already shows — interpret it instead
- If two paragraphs make the same argument, merge or delete one
- "As mentioned above/earlier" is a sign of redundancy — restructure instead

## Figures & Tables
- Reference as "Fig. 1", "Table 1" (abbreviated in parenthetical, spelled out at sentence start)
- Every figure/table MUST be referenced in the text
- Figures: clear axis labels with units, legible font size, colorblind-friendly palette
- Tables: no vertical lines, minimal horizontal lines (three-line table style)
