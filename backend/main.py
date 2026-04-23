from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.query_routes import router as query_router

app = FastAPI()

# CORS Setup for the frontend

# will add the exact when setting the frontend
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
  allow_methods=["*"],
  allow_headers=["*"]
)


app.include_router(query_router, prefix="/api/v1")




if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", reload=True)
