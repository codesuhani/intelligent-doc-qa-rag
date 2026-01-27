import json
from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class Retriever:
    def __init__(
        self,
        index_path: str,
        metadata_path: str,
        top_k: int = 5,
        score_threshold: float = 0.3
    ):
        self.top_k = top_k
        self.score_threshold = score_threshold

        # Load FAISS index
        self.index = faiss.read_index(index_path)

        # Load metadata
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        # Load embedding model
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding

    def retrieve(self, query: str) -> List[Dict]:
        query_embedding = self.embed_query(query)

        scores, indices = self.index.search(query_embedding, self.top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score < self.score_threshold:
                continue

            chunk = self.metadata[idx]
            chunk_result = {
                "score": float(score),
                "text": chunk["text"],
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"]
            }
            results.append(chunk_result)

        return results
