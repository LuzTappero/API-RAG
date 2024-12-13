from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
import os

CHUNK_SIZE= int(os.getenv("CHUNK_SIZE",2000))#2000
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP",100))#100

def split_into_chunks(text: str):
    """Create chunks from the input text."""
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = text_splitter.split_text(text)
        if not chunks:
            raise ValueError("Text could not be split into chunks.")
        return chunks
    except Exception as e:
        raise RuntimeError(f"An error occurred while splitting text into chunks: {str(e)}")