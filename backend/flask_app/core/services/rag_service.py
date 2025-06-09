import os
import uuid
from typing import List, Dict, Optional
from flask_app.core.utils.file_parser import parse_file
from flask_app.core.utils.text_splitter import split_text
from flask_app.core.utils.logger import log
from flask_app.tools.gemini_connector import generate_gemini_response

class RAGService:
    def __init__(self):
        self.vector_store: Dict[str, Dict] = {}
        
    def process_document(self, file_path: str, doc_id: Optional[str] = None) -> Optional[str]:
        """
        Parse and chunk the uploaded file, storing in memory under doc_id.
        Returns document ID if successful, None otherwise.
        """
        doc_id = doc_id or str(uuid.uuid4())
        try:
            text = parse_file(file_path)
            chunks = split_text(text, max_chunk_size=500)

            self.vector_store[doc_id] = {
                "path": file_path,
                "chunks": chunks
            }
            log(f"Document processed and stored: {doc_id}")
            return doc_id
        except Exception as e:
            log(f"Error processing document: {e}", level="ERROR")
            return None

    def retrieve_relevant_chunks(self, doc_id: str, query: str, top_k: int = 5) -> List[str]:
        """
        Naive semantic search: return top_k most relevant chunks by keyword overlap.
        """
        from difflib import SequenceMatcher

        if doc_id not in self.vector_store:
            log(f"No document with ID {doc_id} found", level="WARNING")
            return []

        chunks = self.vector_store[doc_id]["chunks"]
        scored_chunks = []

        for chunk in chunks:
            score = SequenceMatcher(None, chunk.lower(), query.lower()).ratio()
            scored_chunks.append((score, chunk))

        scored_chunks.sort(reverse=True)
        return [chunk for _, chunk in scored_chunks[:top_k]]

    def query_document(self, doc_id: str, query: str) -> str:
        """
        Main RAG logic: Retrieve chunks + pass to Gemini for grounded answer.
        """
        context_chunks = self.retrieve_relevant_chunks(doc_id, query)
        context = "\n\n".join(context_chunks)

        prompt = f"""
You are an AI assistant. Use the following extracted content from a document and answer the question in a helpful way.

---DOCUMENT EXCERPTS---
{context}

---USER QUESTION---
{query}
"""
        return generate_gemini_response(prompt)

# Global instance for backward compatibility
_rag_service = RAGService()

# Legacy functions (deprecated but kept for compatibility)
def process_document(file_path: str, doc_id: str = None):
    return _rag_service.process_document(file_path, doc_id)

def retrieve_relevant_chunks(doc_id: str, query: str, top_k: int = 5):
    return _rag_service.retrieve_relevant_chunks(doc_id, query, top_k)

def query_document_with_rag(doc_id: str, query: str):
    return _rag_service.query_document(doc_id, query)