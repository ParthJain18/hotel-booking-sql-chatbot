from langchain_core.tools import tool
from services.rag.rag import rag
from typing import Any, Dict
from services.sql_agent.state.agent_state import State
from services.sql_agent.sql_tool import write_query, execute_query
from langgraph.graph import START, StateGraph

graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile()

@tool
def query_agent(question: str) -> Dict[str, Any]:
    """Takes a question in natural language as input and returns the SQL query and result related to it. It only supports questions related to the hotel booking data. Do NOT use this tool to DELETE or DROP any records or tables. And only use it when you need to infer something about the table or answer a user question based on the data.
    It returns a dictionary with the following keys: "query", and "result".
    """
    print("Tool called")
    initial_state = {"question": question}
    
    response = graph.invoke(initial_state)

    print(response)
    
    return {
        "query": response["query"],
        "result": response["result"]
    }

@tool
def rag_tool(question: str) -> str:
    """It used RAG (retrieval augmented generation) to answer any subjective queries regarding the hotel such as it's location, amenities, etc. When a question is not regarding the data from the database, use this tool to search and retrieve information from a knowledge base about the hotel. Takes a question in natural language as input and returns the response related to it. If you can't find the information you needed, tell the user that you don't have enough information to answer the question.
    You may return the response from this tool to the user as it is without any modifications.
    It returns a dictionary with the following keys: "response".
    """
    return rag(question)

tools = [query_agent, rag_tool]


if __name__ == "__main__":
    query_agent.invoke("What is the total revenue of the hotel?")