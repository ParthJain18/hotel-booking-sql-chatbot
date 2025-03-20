from services.sql_agent.sql_tool import llm

def get_response(data, context):
    messages=[
        {
            "role": "system",
            "content": f"""You are a RAG (Retrieval Augmented Generation) agent. Your job is to answer user queries regarding a hotel named Hotel Royale Heritage - A Luxurious Stay in Jaipur, India. You must respond in a JSON format of this structure:
                    {{
                        "response":"text"
                    }}

                Below is some additional info fetched from a knowledge base. It may or may not be useful to answer the user's query. If the user's query can be answered by the retrieved documents, answer them, otherwise, reply that the system couldn't find relevant information in the document.

                Fetched activities are:
                {context}

            """
        },
        {
            "role": "user",
            "content": data,
        }
    ]
    response = llm.invoke(messages).content

    print(response)

    return response