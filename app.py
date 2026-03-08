from fastapi import FastAPI, HTTPException
from pydantic import BaseModel



app = FastAPI()


class QueryRequest(BaseModel):
    query : str




@app.post("/generate_sql")
async def generate_sql(request: QueryRequest):
    """Generate SQL query from natural language input."""




