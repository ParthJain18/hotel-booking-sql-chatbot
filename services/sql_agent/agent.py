from services.sql_agent.sql_tool import llm
from typing import Any, Dict
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from services.sql_agent.additional_prompt import system_message
import time
import json
from typing import Any, Dict
from services.sql_agent.tools import tools
from services.sql_agent.graphs import graph_tools

memory = MemorySaver()
tools.extend(graph_tools)
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
    question = "Create a graph displaying the previous result"
    print(query_agent(question, "1"))