from pydantic import BaseModel

# Modelo para validar la entrada
class UploadDocumentRequest(BaseModel):
    title: str
    content: str
