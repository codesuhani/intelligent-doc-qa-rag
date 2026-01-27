import fitz  # PyMuPDF
import json
from pathlib import Path
from tqdm import tqdm

from src.utils.text_cleaner import clean_text


def extract_text_from_pdf(pdf_path: Path):
    """
    Extracts text page-wise from a single PDF.
    Returns a list of dictionaries with metadata.
    """
    document = fitz.open(pdf_path)
    extracted_pages = []

    for page_index in range(len(document)):
        page = document.load_page(page_index)
        raw_text = page.get_text("text")

        cleaned = clean_text(raw_text)

        if cleaned:
            extracted_pages.append({
                "document_name": pdf_path.name,
                "page_number": page_index + 1,
                "text": cleaned
            })

    return extracted_pages


def ingest_pdf_folder(raw_data_dir: str, output_dir: str):
    raw_data_dir = Path(raw_data_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_documents = []

    pdf_files = list(raw_data_dir.glob("*.pdf"))

    if not pdf_files:
        raise ValueError("No PDF files found in raw_data directory")

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        pages = extract_text_from_pdf(pdf_file)
        all_documents.extend(pages)

    output_path = output_dir / "extracted_text.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_documents, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Extracted text from {len(pdf_files)} PDFs")
    print(f"📄 Total pages processed: {len(all_documents)}")
    print(f"💾 Output saved to: {output_path}")


if __name__ == "__main__":
    ingest_pdf_folder(
        raw_data_dir="data/raw_data",
        output_dir="data/processed_text"
    )
