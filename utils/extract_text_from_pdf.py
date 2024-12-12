from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    """
        Hacer args en ingles
    """

    try:
        reader= PdfReader(file_path)
        page_texts = [page.extract_text() for page in reader.pages]
        combined_text = "\n".join(page_texts)
        return combined_text
    except FileNotFoundError:
        # Manejo del error en caso que  no exista el archivo
        print(f"Error: el archivo solicitado '{file_path}' no fue encontrado.")
        return None, None
    except Exception as e:
        # Manejo de cualquier otro tipo de error
        print(f"Error al leer el archivo PDF: {e}")
        return None, None


#pdf_path = 'historias.pdf'
#extract_text_from_pdf(pdf_path)