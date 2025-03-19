from langchain_community.agent_toolkits import SQLDatabaseToolkit
from models.database import DATABASE_URL
from services.sql_agent.state.agent_state import State, QueryOutput
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from services.sql_agent.additional_prompt import additional_prompt
from langchain_core.prompts import PromptTemplate, StringPromptTemplate


load_dotenv()

db = SQLDatabase.from_uri(DATABASE_URL)
llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
query_prompt_template += additional_prompt

tools = toolkit.get_tools()

def write_query(state: State):
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"],
        }
    )

    additional_prompt_value = (prompt.to_string() + additional_prompt)

    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(additional_prompt_value)
    return {"query": result["query"]}

def execute_query(state: State):
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

def generate_answer(state: State):
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}

if __name__ == "__main__":
    # print(tools)
    # print(query_prompt_template)
    print(generate_answer({"question": "How many total bookings have been cancelled so far?"}))