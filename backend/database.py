import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase

load_dotenv()

def get_db_connection() -> SQLDatabase:
  """
    Initializes the SQLDatabase connection. 
    Checks for the DATABASE_URL and raises an error if missing.

  """
  
  mysql_uri = os.getenv("DATABASE_URL")

  if mysql_uri is None:
    raise ValueError("Database_URL not found! Check your env file")

  return SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info=2)

db = get_db_connection()

def get_Schema() -> str:
  return db.get_table_info()