from services.sql_agent.agent import query_agent

def process_query(query_text: str, history_id: str):
    result = query_agent(query_text, history_id)
    
    return {
        "answer": result.get("answer", "Sorry, I couldn't generate an answer."),
        "sql": result.get("query", ""),
        "time_taken": result.get("time_taken", "")
    }