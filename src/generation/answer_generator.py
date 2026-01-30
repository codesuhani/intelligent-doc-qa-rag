from typing import List, Dict
from ollama import chat

from src.retrieval.retriever import Retriever


SYSTEM_PROMPT = """
You are an intelligent document assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not present in the context, say:
  "The provided documents do not contain sufficient information to answer this question."
- Do NOT use prior knowledge.
- Cite sources using (Document Name, Page Number).
- Be concise, factual, and neutral.
"""


class AnswerGenerator:
    def __init__(self):
        self.retriever = Retriever(
            index_path="data/vector_store/faiss.index",
            metadata_path="data/vector_store/metadata.json",
            top_k=5,
            score_threshold=0.3
        )

    def build_context(self, retrieved_chunks: List[Dict]) -> str:
        context_blocks = []
        for chunk in retrieved_chunks:
            block = (
                f"[Source: {chunk['document_name']} | Page {chunk['page_number']}]\n"
                f"{chunk['text']}"
            )
            context_blocks.append(block)

        return "\n\n".join(context_blocks)

    def generate_answer(self, query: str) -> str:
        retrieved_chunks = self.retriever.retrieve(query)

        if not retrieved_chunks:
            return "The provided documents do not contain sufficient information to answer this question."

        context = self.build_context(retrieved_chunks)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Question:
{query}

Context:
{context}
"""
            }
        ]

        response = chat(
            model="mistral",
            messages=messages,
            options={
                "temperature": 0.0
            }
        )

        return response["message"]["content"]
