# Intelligent Document Question Answering System (RAG)

## 📌 Problem Statement
Organizations store critical information in unstructured documents such as PDFs
(policies, manuals, research papers). Extracting accurate answers from these documents
is time-consuming and inefficient.

This project aims to build an intelligent document-aware question answering system
that retrieves relevant information from uploaded documents and generates grounded,
context-aware answers while minimizing hallucinations using Retrieval-Augmented
Generation (RAG).

---

## 🧠 Why RAG?
Large Language Models alone can hallucinate or provide outdated information.
RAG improves reliability by:
- Retrieving relevant document context
- Grounding answers in source material
- Providing traceability to original documents

---

## 🏗️ System Architecture (High-Level)

PDF Documents  
↓  
Text Extraction  
↓  
Text Chunking  
↓  
Embeddings  
↓  
Vector Database  
↓  
Retriever  
↓  
LLM Answer Generation  

---

## 🛠️ Tech Stack
- Python
- PyMuPDF (PDF parsing)
- Sentence Transformers (Embeddings)
- FAISS / Chroma (Vector search)
- OpenAI / Llama (LLM)
- Streamlit (UI)

---

## 🚧 Project Status
✅ Phase 0: Project Setup  
✅ Phase 1: Document Ingestion  
⬜ Phase 2: Text Chunking  
⬜ Phase 3: Embeddings  
⬜ Phase 4: Retrieval  
⬜ Phase 5: Answer Generation  

---

## 📂 Repository Structure
intelligent-doc-qa-rag/
├── data/
├── src/
├── app.py
└── README.md


---

## 📌 Note
This project focuses on **engineering correctness and explainability**, not just library usage.

## ⚠️ Phase 1 Notes & Limitations
- Text is extracted page-wise to preserve document traceability.
- Some PDFs with tables or complex layouts lose structural formatting.
- Scanned/image-only PDFs are not supported in the current pipeline.
- OCR-based extraction is planned as a future enhancement.


## ✂️ Phase 2: Text Chunking
- Documents are split into sentence-preserving, overlapping chunks.
- Chunk size and overlap are configurable.
- Metadata (document name, page number) is preserved for traceability.
- This improves retrieval accuracy and reduces hallucination risk.
