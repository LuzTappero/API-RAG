from pydantic import BaseModel

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


