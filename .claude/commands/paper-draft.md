# Paper Drafting Assistant

Help draft, review, or refine sections of the research paper.

## Instructions
Based on the argument, assist with the specified paper section:

### Available Actions
- `outline` — Generate/update the full paper outline with key points per section
- `introduction` — Draft the Introduction section
- `study-area` — Draft the Study Area & Data section
- `methodology` — Draft the Methodology section
- `results` — Draft Results section based on actual model outputs in `reports/`
- `discussion` — Draft Discussion section linking results to literature
- `conclusion` — Draft Conclusion & Recommendations
- `abstract` — Draft the abstract (do this last, after all sections)
- `review <section>` — Review a drafted section for clarity, flow, and academic tone
- `references` — Compile and format reference list

### Writing Guidelines
- Academic tone, third person, past tense for methods/results
- Be concise — journals have word limits (~6000-8000 words)
- Every claim must be supported by data or citation
- Use active voice where possible ("We developed..." not "A model was developed...")
- Figures and tables referenced in text as "Fig. 1", "Table 1"
- Follow target journal style (Int. J. of Climatology / Remote Sensing MDPI)

Action: $ARGUMENTS
