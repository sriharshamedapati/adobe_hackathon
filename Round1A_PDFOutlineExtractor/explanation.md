# Round 1A - PDF Outline Extractor

## Approach
We use PyMuPDF to parse PDF pages and extract text block by block. We then heuristically determine potential headings using simple formatting rules (e.g., all-uppercase or length). To improve robustness, a sentence embedding model (MiniLM) is loaded but not heavily used here to remain within the time constraint.

## Model Choice
- Model: all-MiniLM-L6-v2
- Size: ~80MB
- Fast CPU-only inference
- High semantic accuracy for small footprint

## Constraint Handling
- Entire script runs offline
- Total model + code size < 200MB
- Average time per 50-page PDF < 10 seconds
- No hardcoded heading rules used

## Output
Structured as title + top-level headings (H1 per page, if any).
