from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_into_chunks(text: str):
    """Create chunks from the input text."""
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")

    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=30
        )
        chunks = text_splitter.split_text(text)
        if not chunks:
            raise ValueError("Text could not be split into chunks.")
        return chunks
    except Exception as e:
        raise RuntimeError(f"An error occurred while splitting text into chunks: {str(e)}")