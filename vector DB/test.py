import os
import re
import pymupdf  
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq
load_dotenv()


def read_file_with_context(file_path):
    """
    Reads a PDF file and combines chunks with half of the next page.
    """
    try:
        doc = pymupdf.open(file_path)
        page_chunks = []
        total_pages = len(doc)

        for page_num in range(total_pages):
            current_page = doc.load_page(page_num)
            current_page_text = current_page.get_text()

            combined_text = current_page_text

            if page_num + 1 < total_pages:
                next_page = doc.load_page(page_num + 1)
                next_text = next_page.get_text()
                combined_text += next_text[:len(next_text) // 2]

            if page_num == total_pages - 1:
                final_chunk = current_page_text
            else:
                final_chunk = combined_text

            final_chunk = re.sub(r"(\w+)-\n(\w+)", r"\1\2", final_chunk)

            if final_chunk.strip():
                page_chunks.append(final_chunk.strip())

        doc.close()
        return page_chunks

    except Exception as e:
        print(f"PDF read error: {e}")
        return []


def generate_embeddings(text_chunks):
    """Generate embeddings using SentenceTransformer."""
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(text_chunks, show_progress_bar=True)
        return embeddings.tolist()
    except Exception as e:
        print("Embedding generation error:", e)
        return []



def setup_faiss(document_embeddings:list=[]):
    ve






    

  



def main():
    chunks = read_file_with_context("myfile.pdf")
    document_vectors = generate_embeddings(chunks)


    print(len(document_vectors))








if __name__ == "__main__":
    main()
