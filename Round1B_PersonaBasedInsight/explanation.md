# Round 1B - Persona-Based Insight Extractor

## Persona Use
We embed the interests of the persona into a vector space using MiniLM. For each PDF, we extract full-page text and compute semantic similarity. Any content that scores above a set threshold (0.5) is flagged as relevant insight.

## Model Choice
- Model: all-MiniLM-L6-v2 (~80MB)
- Fast and capable on CPU
- Remains within 1GB model + environment constraint

## Performance
- End-to-end execution per document set: < 60 seconds
- CPU-only inference
- Completely offline

## Output
Returns a JSON list of insights relevant to the persona, each containing a brief snippet, page number, and similarity score.
