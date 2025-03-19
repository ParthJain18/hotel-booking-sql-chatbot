from services.sql_agent.agent import query_agent

def process_query(query_text: str):
    result = query_agent(query_text)
    
    return {
        "answer": result.get("answer", "Sorry, I couldn't generate an answer."),
        "sql": result.get("query", ""),
        "result": result.get("result", ""),
        "time_taken": result.get("time_taken", "")
    }