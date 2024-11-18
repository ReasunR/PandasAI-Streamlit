import os
import psycopg2
import duckdb
from pandasai.connectors import PostgreSQLConnector
from pandasai.llm import OpenAI
from pandasai.llm.local_llm import LocalLLM
from pandasai import Agent

from table_description import employees_postgres, informations_postgres

ollama_llm = LocalLLM(api_base="http://localhost:11434/v1", model="llama3")
openai_llm_4o = OpenAI(
    api_token=os.environ.get('OPENAI_API_KEY'),
    model="gpt-4o",
)
openai_llm_gpt4 = OpenAI(
    api_token=os.environ.get('OPENAI_API_KEY'),
    model="gpt-4",
)
openai_llm_gpt35 = OpenAI(
    api_token=os.environ.get('OPENAI_API_KEY'),
    model="gpt-3.5-turbo",
)
openai_llm_40_mini = OpenAI(
    api_token=os.environ.get('OPENAI_API_KEY'),
    model="gpt-4o-mini",
)


def get_list_of_tables_from_sql_db():
    conn = psycopg2.connect(host="localhost", user="checkito950", password="123456", dbname="postgres")
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()

    cursor.close()
    conn.close()

    return [table[0] for table in tables]


def get_df_from_table(table_name):
    return PostgreSQLConnector(
        config={
            "host": "localhost",
            "port": 5432,
            "database": "postgres",
            "username": "checkito950",
            "password": "123456",
            "table": table_name,
        })


employees_df_postgres = PostgreSQLConnector(
    config={
        "host": "localhost",
        "port": 5432,
        "database": "postgres",
        "username": "checkito950",
        "password": "123456",
        "table": "employees",
    })


def get_agent(list_of_dfs):
    flag_has_employees = False
    flag_has_informations = False

    for df in list_of_dfs:
        if df.config.table == "employees":
            flag_has_employees = True
        elif df.config.table == "informations":
            flag_has_informations = True
        if flag_has_employees and flag_has_informations:
            break

    if flag_has_employees and flag_has_informations:
        print('flag 1')
        agent = Agent([employees_postgres, informations_postgres],
                      config={"max_retries": 5, "llm": openai_llm_gpt4, 'direct_sql': True, "verbose": True, "enforce_privacy": True}, description="when using sql join, use table aliases")
    else:
        print('flag 2')
        agent = Agent(list_of_dfs, config={"llm": openai_llm_gpt4, "max_retries": 4, "verbose": True,
                                           "custom_whitelisted_dependencies": ["wordcloud", "utils"]}, description="generate sql query")

    return agent


def ask(user_input, agent):
    return agent.chat(user_input)


def explain(agent):
    return agent.explain()


def get_log_content():
    path = "/Users/checkito950/PycharmProjects/Streamlit_PandasAI/pandasai.log"
    with open(path, "r") as f:
        logs = f.readlines()[-20:]
        logs = "\n".join(logs)
    return logs


def get_code_to_run(user_input):
    code_to_run = ""
    conn = duckdb.connect('/Users/checkito950/PycharmProjects/Streamlit_PandasAI/cache/cache_db_0.11.db')
    result = conn.execute("SELECT * FROM cache;").fetchdf().values
    for ele in result:
        if user_input in ele[0]:
            code_to_run = ele[1]
            break
    conn.close()
    return code_to_run
