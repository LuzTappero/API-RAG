from pydantic import BaseModel
from typing import List, Union

class Document(BaseModel):
    title: str
    content: str

class UploadDocumentRequest(BaseModel):
    documents: Union[Document, List[Document]]

class EmbeddingRequest(BaseModel):
    document_id: str

class QueryRequest(BaseModel):
    query: str

class SearchRequest(BaseModel):
    document_id: str

class AskRequest(BaseModel):
    question: str


