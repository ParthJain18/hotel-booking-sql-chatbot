from services.rag.retrieval.vectorize import vectorize_query, create_or_load_vector_db
from services.rag.retrieval.retrieval_model import retrieve_relevant_chunks
from services.rag.generation.generation import get_response
import json
from config import METADATA_PATH

index, metadata = create_or_load_vector_db()

def load_metadata():
    with open(METADATA_PATH, 'r') as f:
        metadata = json.load(f)
    return metadata

def rag(user_query):
    metadata = load_metadata()
    query_embedding = vectorize_query(user_query)
    relevant_logs = retrieve_relevant_chunks(query_embedding, index=index, metadata=metadata, top_k=3)
    context = " ".join([log['chunk'] for log in relevant_logs])
    response = get_response(user_query, context)

    # print(metadata[0].keys())

    return response


if __name__ == "__main__":
    user_query = "Where is the hotel located?"
    rag(user_query)