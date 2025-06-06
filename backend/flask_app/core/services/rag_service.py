import os
import uuid
from flask_app.core.utils.file_parser import parse_file
from flask_app.core.utils.text_splitter import split_text
from flask_app.core.utils.logger import log
from flask_app.tools.gemini_connector import generate_gemini_response

# In-memory vector store placeholder
VECTOR_STORE = {}

def process_document(file_path: str, doc_id: str = None):
    """
    Parse and chunk the uploaded file, storing in memory under doc_id.
    """
    doc_id = doc_id or str(uuid.uuid4())
    try:
        text = parse_file(file_path)
        chunks = split_text(text, max_chunk_size=500)

        VECTOR_STORE[doc_id] = {
            "path": file_path,
            "chunks": chunks
        }
        log(f"Document processed and stored: {doc_id}")
        return doc_id
    except Exception as e:
        log(f"Error processing document: {e}", level="ERROR")
        return None

def retrieve_relevant_chunks(doc_id: str, query: str, top_k: int = 5):
    """
    Naive semantic search: return top_k most relevant chunks by keyword overlap.
    """
    from difflib import SequenceMatcher

    if doc_id not in VECTOR_STORE:
        log(f"No document with ID {doc_id} found", level="WARNING")
        return []

    chunks = VECTOR_STORE[doc_id]["chunks"]
    scored_chunks = []

    for chunk in chunks:
        score = SequenceMatcher(None, chunk.lower(), query.lower()).ratio()
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True)
    return [chunk for _, chunk in scored_chunks[:top_k]]

def query_document_with_rag(doc_id: str, query: str):
    """
    Main RAG logic: Retrieve chunks + pass to Gemini for grounded answer.
    """
    context_chunks = retrieve_relevant_chunks(doc_id, query)
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant. Use the following extracted content from a document and answer the question in a helpful way.

---DOCUMENT EXCERPTS---
{context}

---USER QUESTION---
{query}
"""
    response = generate_gemini_response(prompt)
    return response

