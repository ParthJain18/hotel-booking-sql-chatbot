import numpy as np

def retrieve_relevant_chunks(query_embedding, index, metadata, top_k=5):
    D, I = index.search(np.array(query_embedding), top_k)
    return [{'chunk': metadata[i]['chunk']} for i in I[0]]