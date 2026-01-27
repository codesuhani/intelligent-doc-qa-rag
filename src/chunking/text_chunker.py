import json
from pathlib import Path
from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 150,
    overlap: int = 30
) -> List[str]:
    """
    Splits text into overlapping chunks based on word count.
    """
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start = end - overlap  # move back for overlap
        if start < 0:
            start = 0

    return chunks


def chunk_documents(
    input_path: str,
    output_path: str,
    chunk_size: int = 150,
    overlap: int = 30
):
    """
    Reads extracted_text.json and outputs chunked_text.json
    with full metadata.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    with open(input_path, "r", encoding="utf-8") as f:
        documents = json.load(f)

    chunked_records = []
    chunk_id = 0

    for doc in documents:
        chunks = chunk_text(
            doc["text"],
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk in chunks:
            chunked_records.append({
                "chunk_id": chunk_id,
                "document_name": doc["document_name"],
                "page_number": doc["page_number"],
                "text": chunk
            })
            chunk_id += 1

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunked_records, f, indent=2, ensure_ascii=False)

    print(f"✅ Chunking complete")
    print(f"📦 Total chunks created: {len(chunked_records)}")
    print(f"💾 Output saved to: {output_path}")


if __name__ == "__main__":
    chunk_documents(
        input_path="data/processed_text/extracted_text.json",
        output_path="data/processed_text/chunked_text.json"
    )
