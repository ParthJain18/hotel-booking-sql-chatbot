from langgraph.graph import START, StateGraph
from services.sql_agent.state.agent_state import State
from services.sql_agent.sql_tool import write_query, execute_query, generate_answer, db, llm, tools, query_prompt_template
import time
from typing import Any, Dict
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver



memory = MemorySaver()
graph_builder = StateGraph(State).add_sequence(
    [write_query, execute_query, generate_answer]
)
graph_builder.add_edge(START, "write_query")
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "3"}}


def query_agent(question: str) -> Dict[str, Any]:
    initial_state = {"question": question}
    
    start_time = time.time()
    response = graph.invoke(initial_state, config=config)
    # response = agent_executor.invoke(initial_state)
    # system_message = query_prompt_template.format(dialect="SQLite", top_k=5, table_info=db.get_table_info(), input=question)
    # agent_executor = create_react_agent(llm, tools, prompt=system_message)

    # for step in agent_executor.stream({"messages": [{"role": "user", "content": question}]}, stream_mode="values",):
    #     step["messages"][-1].pretty_print()


    execution_time = time.time() - start_time
    
    # print(response)
    # print("\n=========\n")

    return {
        "answer": response.get("answer", ""),
        "query": response.get("query", ""),
        "result": response.get("result", ""),
        "time_taken": f"{execution_time:.2f} seconds"
    }

if __name__ == "__main__":
    question = "What percent of customers have cancelled in the past year?"
    result = query_agent(question)
    
    print(f"\nTime taken: {result['time_taken']}")
    print(f"\nQuestion: {question}")
    print(f"\nSQL Query:\n{result['query']}")
    print(f"\nSQL Result:\n{result['result']}")
    print(f"\nAnswer:\n{result['answer']}")