from pydantic import BaseModel

# Modelo para validar la entrada
class EmbeddingRequest(BaseModel):
    document_id: str

class QueryRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    document_id: str
    # title: str
    content_snippet: str
    similarity_score: float

    # Modelo para la solicitud
class AskRequest(BaseModel):
    question: str