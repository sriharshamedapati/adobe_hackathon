import os
import json
import fitz
from sentence_transformers import SentenceTransformer, util

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_persona():
    with open(os.path.join(INPUT_FOLDER, "persona1.json"), "r") as f:
        return json.load(f)

def extract_text_by_relevance(texts, persona_vector):
    results = []
    for text, page in texts:
        embedding = model.encode(text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(embedding, persona_vector).item()
        if score > 0.5:
            results.append({"section": text[:80], "page": page, "score": score})
    return results

def process_documents(persona):
    interests = " ".join(persona["interests"])
    persona_vector = model.encode(interests, convert_to_tensor=True)

    insights = []
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(".pdf"):
            doc = fitz.open(os.path.join(INPUT_FOLDER, file_name))
            texts = []
            for i, page in enumerate(doc):
                text = page.get_text()
                texts.append((text, i))
            insights.extend(extract_text_by_relevance(texts, persona_vector))
    return {"persona": persona["name"], "insights": insights}

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    persona = load_persona()
    result = process_documents(persona)
    with open(os.path.join(OUTPUT_FOLDER, "insights.json"), "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
