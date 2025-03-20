from services.sql_agent.sql_tool import llm
from typing import Any, Dict
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from services.sql_agent.additional_prompt import system_message
import time
import json
from langgraph.graph import START, StateGraph
from services.sql_agent.state.agent_state import State
from services.sql_agent.sql_tool import write_query, execute_query
from langchain_core.tools import tool
from services.rag.rag import rag
from typing import Any, Dict

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
    initial_state = {"question": question}
    
    response = graph.invoke(initial_state)
    
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

memory = MemorySaver()
agent_executor = create_react_agent(llm, tools, prompt=system_message, checkpointer=memory)

def query_agent(question: str, history_id: str) -> Dict[str, Any]:
    initial_state = {"messages": [("user", question)]}
    query = ""

    print("\n=========\n")
    start_time = time.time()
    response = agent_executor.invoke(
        initial_state, 
        config={"configurable": {"thread_id": history_id}}
        )['messages']

    for message in response[-3:]:
        message.pretty_print()
        if '"query":' in message.content:
            message_content = json.loads(message.content)
            query = message_content["query"]

    execution_time = time.time() - start_time
    
    print(response[-1].content)
    print("\n=========\n")

    return {
        "query": query,
        "answer": response[-1].content,
        "time_taken": f"{execution_time:.2f} seconds"
    }

if __name__ == "__main__":
    question = "What pervent of people cancelled last month?"
    print(query_agent(question, "1"))
    question = "what other places can I visit near the hotel"
    print(query_agent(question, "1"))