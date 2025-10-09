import faiss
import numpy as np
from core.embeddings import get_embeddings

index = None
stored_chunks = []

def store_chunks(chunks):
    global index, stored_chunks
    stored_chunks.extend(chunks)
    embeddings = get_embeddings(chunks)
    dim = embeddings.shape[1]
    if index is None:
        index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

def query_chunks(query, k=3):
    query_embedding = get_embeddings([query])[0].reshape(1, -1)
    D, I = index.search(query_embedding, k)
    return [stored_chunks[i] for i in I[0]]