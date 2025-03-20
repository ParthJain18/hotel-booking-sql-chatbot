from langgraph.graph import START, StateGraph
from services.sql_agent.state.agent_state import State
from services.sql_agent.sql_tool import write_query, execute_query, llm
from typing import Any, Dict
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from services.sql_agent.additional_prompt import system_message
import time
import json



memory = MemorySaver()


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


tools = [query_agent]
agent_executor = create_react_agent(llm, tools, prompt=system_message, checkpointer=memory)

def query_agent(question: str, history_id: str) -> Dict[str, Any]:
    initial_state = {"messages": [("user", question)]}
    query = ""
    start_time = time.time()
    response = agent_executor.invoke(
        initial_state, 
        config={"configurable": {"thread_id": history_id}}
        )['messages']

    for message in response[-3:]:
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
    question = "How many bookings have been canceled so far in this year?"
    print(query_agent(question))
    question = "What did I ask before?"
    print(query_agent(question))