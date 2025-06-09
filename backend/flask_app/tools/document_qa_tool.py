from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from flask_app.core.services.rag_service import query_document_with_rag

class DocumentQAInput(BaseModel):
    query: str = Field(..., description="Question about the document")
    document_id: str = Field(..., description="ID of the uploaded document")

class DocumentQATool(BaseTool):
    name = "DocumentQA"
    description = "Answers questions about uploaded documents using RAG"
    args_schema = DocumentQAInput

    def _run(self, query: str, document_id: str) -> str:
        return query_document_with_rag(document_id, query)