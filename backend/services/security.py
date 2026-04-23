import re

def is_sql_safe(sql_query) -> bool:
  query = sql_query.upper()

  forbidden_commands = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "RENAME"]

  if not query.strip().startswith("SELECT"):
    return False
  
  pattern = r"\b("+"|".join(forbidden_commands)+ r")\b"      
    # Check for forbidden words anywhere in the string
  if re.search(pattern,query):
    return False
            
  return True