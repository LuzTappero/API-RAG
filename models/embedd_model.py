from pydantic import BaseModel

# Modelo para validar la entrada
class UploadDocumentRequest(BaseModel):
    title: str
    content: str

class EmbeddingRequest(BaseModel):
    document_id: str

class QueryRequest(BaseModel):
    query: str

class SearchRequest(BaseModel):
    document_id: str

class AskRequest(BaseModel):
    question: str

class SearchResult(BaseModel):
    document_id: str
    # title: str
    content_snippet: str
    similarity_score: float