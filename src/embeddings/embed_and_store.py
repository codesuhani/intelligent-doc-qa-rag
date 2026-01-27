import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks(chunk_file: str):
    with open(chunk_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_embeddings(texts, model):
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return embeddings


def build_faiss_index(embeddings: np.ndarray):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity via inner product
    index.add(embeddings)
    return index


def main():
    chunk_path = "data/processed_text/chunked_text.json"
    vector_store_dir = Path("data/vector_store")
    vector_store_dir.mkdir(parents=True, exist_ok=True)

    print("📄 Loading chunked data...")
    chunks = load_chunks(chunk_path)

    texts = [chunk["text"] for chunk in chunks]

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("⚙️ Generating embeddings...")
    embeddings = generate_embeddings(texts, model)

    print("📦 Building FAISS index...")
    index = build_faiss_index(embeddings)

    print("💾 Saving FAISS index...")
    faiss.write_index(index, str(vector_store_dir / "faiss.index"))

    print("💾 Saving metadata...")
    with open(vector_store_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print("✅ Phase 3 complete")
    print(f"🔢 Total vectors stored: {index.ntotal}")


if __name__ == "__main__":
    main()
