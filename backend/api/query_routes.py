from fastapi import APIRouter
from pydantic import BaseModel
from services.langchain_agent import run_sql_agent


router = APIRouter()

class QueryRequest(BaseModel):
  question:str

@router.post("/ask")
async def ask_ai(request: QueryRequest):

  answer = run_sql_agent(request.question)

  return {"answer" : answer}