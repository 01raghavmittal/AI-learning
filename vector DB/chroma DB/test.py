import os
import re
import pymupdf  
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from groq import Groq
from fastembed import TextEmbedding
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

# def generate_embeddings(text_chunks):
#     model = TextEmbedding()
#     embedding_list =list(model.embed(text_chunks))
#     return embedding_list

# def generate_embeddings(text_chunks):
#     try:
#         model = SentenceTransformer("google/embeddinggemma-300m")
#         # query_embeddings = model.encode_query(query)
#         document_embeddings = model.encode_document(text_chunks)  
#         return document_embeddings.tolist()
#     except Exception as e:
#         print(e)
#         return []
    


def setup_chromadb(text_vector, document_chunk, query_embedding=None):
    client = chromadb.PersistentClient(path="./chroma_db")

    ids = [f"id{i+1}" for i in range(len(document_chunk))]
    metadatas = [{"page_number": i + 1} for i in range(len(document_chunk))]

    collection = client.get_or_create_collection(name="my_collection",metadata={
        "hnsw:space": "cosine",
        "hnsw:M": 32,
        "hnsw:construction_ef": 200,
        "hnsw:search_ef": 150
    })

    collection.add(
        ids=ids,
        documents=document_chunk,
        metadatas=metadatas,
        embeddings=text_vector
    )

     

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    return results



def format_userquery(response=None,user_query:str=None):

    if response is None:
        response="There is No data is coming from knowledge base"
    
    if response is None:
        response = "User can't enter any Query so greet the user and ask him/her for Query."
    
    formatted_userQuery= (
        f"CONTEXT:\n---\n{response}\n---\n\n"
        f"QUESTION: {user_query}")
    

    return formatted_userQuery


def make_api_call(prompt, system_prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True
    )

    full_response = ""   

    for chunk in chat_completion:
        content = chunk.choices[0].delta.content
        if content: 
            full_response += content

    return full_response  



def main():
    chunks = read_file_with_context("../myfile.pdf")
    document_vectors = generate_embeddings(chunks)
    if document_vectors:
        user_Query="tell me payload of model list price API"
        query_vector_embedding = generate_embeddings(user_Query)
        if query_vector_embedding:
            db_response = setup_chromadb(document_chunk=chunks,text_vector=document_vectors,query_embedding=query_vector_embedding)



        
        system_prompt = (
            "You are a helpful and accurate RAG (Retrieval-Augmented Generation) assistant. "
            "Use the provided context to answer the user's question. "
            "If the answer is not explicitly found in the context, state that you cannot answer based on the provided information. "
            "Do not use external knowledge."
        )

        format_prompt= format_userquery(user_query=user_Query, response = db_response)

        result= make_api_call(system_prompt=system_prompt, prompt= format_prompt)
        print(result)





if __name__ == "__main__":
    main()
