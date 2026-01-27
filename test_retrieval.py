from src.retrieval.retriever import Retriever

retriever = Retriever(
    index_path="data/vector_store/faiss.index",
    metadata_path="data/vector_store/metadata.json",
    top_k=5,
    score_threshold=0.3
)

query = "What is the objective of the education policy?"

results = retriever.retrieve(query)

for r in results:
    print("-" * 80)
    print(f"Score: {r['score']}")
    print(f"Document: {r['document_name']} | Page: {r['page_number']}")
    print(r["text"])
