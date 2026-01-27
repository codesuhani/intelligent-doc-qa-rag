import fitz  # PyMuPDF
from tqdm import tqdm
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_pages = []

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text("text")

        if text.strip():  # ignore empty pages
            extracted_pages.append({
                "document": Path(pdf_path).name,
                "page_number": page_number + 1,
                "text": text
            })

    return extracted_pages


def process_pdf_folder(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_documents = []

    for pdf_file in tqdm(list(input_dir.glob("*.pdf"))):
        pages = extract_text_from_pdf(pdf_file)
        all_documents.extend(pages)

    output_path = output_dir / "extracted_text.json"

    import json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_documents, f, indent=2, ensure_ascii=False)

    print(f"Saved extracted text to {output_path}")
