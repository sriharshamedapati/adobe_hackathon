import fitz  # PyMuPDF
import os
import json
from sentence_transformers import SentenceTransformer, util
import torch

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
model = SentenceTransformer("all-MiniLM-L6-v2")

def is_heading(text):
    return len(text.strip()) > 5 and text.strip().isupper()

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                text = " ".join([span["text"] for span in line.get("spans", [])])
                if is_heading(text):
                    outline.append({
                        "level": "H1",
                        "text": text.strip(),
                        "page": page_num
                    })
                    break
    return outline

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_FOLDER, file_name)
            title = os.path.splitext(file_name)[0].replace("_", " ").title()
            outline = extract_outline(pdf_path)
            output = {"title": title, "outline": outline}
            with open(os.path.join(OUTPUT_FOLDER, file_name.replace(".pdf", ".json")), "w") as f:
                json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
