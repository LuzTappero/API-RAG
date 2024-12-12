from fastapi import HTTPException
import json
from typing import List, Dict
from utils.extract_text_from_pdf import extract_text_from_pdf


# Archivo para persistir documentos
DOCUMENTS_FILE = "documents.json"

def upload_doc() -> Dict:
    try:
        with open(DOCUMENTS_FILE, "r") as file:
            return json.load(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error occurred: {str(e)}")


# Guardar documentos en un archivo local
def save_documents(documents):
    with open(DOCUMENTS_FILE, "w") as file:
        json.dump(documents, file, indent=4)

docs = upload_doc()