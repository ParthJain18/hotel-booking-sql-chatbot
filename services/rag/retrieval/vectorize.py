from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from config import EMBEDDING_MODEL, VECTOR_DB_PATH, METADATA_PATH, DOCUMENT_PATH

model = SentenceTransformer(EMBEDDING_MODEL)

def create_or_load_vector_db():
    if os.path.exists(VECTOR_DB_PATH):
        print("Loading existing vector database...")
        index = faiss.read_index(VECTOR_DB_PATH)
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
    else:
        print("Creating new vector database...")
        index = None
        metadata = []

        document = ""
        with open(DOCUMENT_PATH, 'r') as f:
            document = f.read()
        
        if document:
            chunks = chunk_document(document)

            print(f"Document chunked into {len(chunks)} pieces")
            
            index = create_vector_db(chunks)
            
            with open(METADATA_PATH, 'r') as f:
                metadata = json.load(f)

    return index, metadata

def chunk_document(document, chunk_size=500, overlap=50):

    if not document:
        return []
    
    words = document.split()
    chunks = []
    
    if len(words) <= chunk_size:
        return [document] 
    
    i = 0
    while i < len(words):
        chunk_end = min(i + chunk_size, len(words))
        chunk = ' '.join(words[i:chunk_end])
        chunks.append(chunk)
        i += chunk_size - overlap
    
    return chunks

def create_vector_db(processed_data: list[str]):
    embeddings = model.encode(processed_data)

    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings))

    faiss.write_index(index, VECTOR_DB_PATH)

    with open(METADATA_PATH, 'w') as f:
        json.dump([{'chunk': chunk, 'embedding': embedding.tolist()} 
                   for chunk, embedding in zip(processed_data, embeddings)], f)
    
    return index

def vectorize_query(query):
    query_embedding = model.encode([query])
    return query_embedding