from uuid import uuid4
from fastapi import HTTPException
import json
from typing import List, Dict
from models.upload_model import UploadDocumentRequest
from utils.text_utils import split_into_chunks
import os

# Archivo para persistir documentos
DOCUMENTS_FILE = "documents.json"

def upload_doc() -> Dict:

    if not os.path.exists(DOCUMENTS_FILE):
        print ("The documents dile doesn't exist")
        return []
    try:
        with open(DOCUMENTS_FILE, "r") as file:
            data= json.load(file)
            if not isinstance(data, list):
                raise ValueError("The file does not contain a valid list of documents.")
            return data
    except json.JSONDecodeError:
        print("The file is empty or contains invalid JSON. Returning an empty list.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading documents: {str(e)}")
        return []


# Guardar documentos en un archivo local
def save_documents(documents :UploadDocumentRequest ):
    if not isinstance(documents, UploadDocumentRequest):
        raise ValueError("Invalid document format. Expected an UploadDocumentRequest object.")
    if not documents.title:
        raise ValueError("The document title cannot be empty.")
    if not documents.content:
        raise ValueError("The document content cannot be empty.")

    try:
        chunks=split_into_chunks(documents.content)
        if not chunks:
            raise ValueError("No chunks generated from the document content.")
        ids= []
        new_chunks=[]
        saved_chunks = upload_doc()

        if os.path.exists(DOCUMENTS_FILE):
            with open(DOCUMENTS_FILE, "r") as file:
                try:
                    saved_chunks = json.load(file)
                except json.JSONDecodeError:
                    saved_chunks = []
        else:
            saved_chunks = []
        for chunk in chunks:
            document_id = str(uuid4())
            document = {}
            document = {
                "document_id": document_id,
                "title": documents.title,
                "content": chunk,
            }
            new_chunks.append(document)
            ids.append(document_id)
        saved_chunks.extend(new_chunks)
        with open(DOCUMENTS_FILE, "w") as file:
            json.dump(saved_chunks, file, indent=4)
        return {
            "message": "Document successfully uploaded",
            "document_id": ids[0],
        }
    except Exception as e:
        raise RuntimeError(f"An error occurred while saving the document: {str(e)}")
