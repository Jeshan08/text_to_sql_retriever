from database import db, get_Schema
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
from services.security import is_sql_safe

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def run_sql_agent(question: str) -> str:
    # Generating the sql chain 
    schema = get_Schema()
    sql_prompt = ChatPromptTemplate.from_template("""
    You are a SQL expert. Based on the schema below, write a MySQL query.
    Schema: {schema}
    Question: {question}
    SQL Query:
    """)
    # so the sql chain in invoked with schema n question from user
    sql_chain = sql_prompt | llm.bind(stop=["\nSQLResult:"]) | StrOutputParser()
    raw_response = sql_chain.invoke({"schema": schema, "question": question})
    
    # once the sql is generated we will clean using regex and get the sql query only
    match = re.search(r"```sql\n(.*?)\n```", raw_response, re.DOTALL)
    clean_sql = match.group(1).strip() if match else raw_response.strip()
    
    #Strickt checking and only allowing if the query is for select 

    if not is_sql_safe(clean_sql):
      return f"Modyfying is not allowed."


    print(f"Sql generated is {clean_sql}")
    # getting the data from mysql db
    try:
      db_result = db.run(clean_sql)
    except Exception as e:
      return f"Database error: {str(e)}"
    
    #  now we sending the question and the data from db to llm again to get answer for the non tech user
    response_prompt = ChatPromptTemplate.from_template("""
    You are a professional Business Intelligence Assistant. 

    USER QUESTION: {question}
    RAW DATABASE DATA: {result}

    INSTRUCTIONS:
    1. Use the RAW DATABASE DATA to provide a concise, natural language answer.
    2. If the data is empty (e.g., '[]'), state that no records were found.
    3. Always format currency as '$XX,XXX.XX' and round to two decimal places.
    4. Do not mention the database or the query; just answer the user directly.
    5. Use **bolding** for names and dollar amounts to make them stand out.
    6. If there are 3 or more items, use a bulleted list.

    FINAL ANSWER:
    """)
    
    response_chain = response_prompt | llm | StrOutputParser()
    return response_chain.invoke({"question": question, "result": db_result})