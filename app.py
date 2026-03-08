from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query_generator import generate_sql_query, execute_query, format_results_as_text


app = FastAPI()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str


@app.post("/ask", response_model=QueryResponse)
async def ask_database(request: QueryRequest):
    """
    Answer questions using the database.
    
    Takes a natural language question and returns a plain English answer.
    No technical details or SQL queries are shown to the user.
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Please ask a valid question.")
    
    try:
        # Generate SQL from natural language
        sql_query = generate_sql_query(request.query)
        
        if not sql_query:
            return QueryResponse(
                answer="I'm having trouble understanding your question. Could you rephrase it?"
            )
        
        # Execute the query
        results = execute_query(sql_query)
        
        if results is None:
            return QueryResponse(
                answer="Sorry, I couldn't find that information in the database. Could you ask your question in a different way?"
            )
        
        # Format results in user-friendly plain English
        user_friendly_answer = format_results_as_text(results, request.query)
        
        return QueryResponse(answer=user_friendly_answer)
    
    except Exception as e:
        # Don't expose technical error details to the user
        return QueryResponse(
            answer="Sorry, something went wrong while looking up that information. Please try again."
        )


@app.get("/")
async def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to the Database Assistant!",
        "instruction": "Use POST /ask with a JSON body {'query': 'your question here'} to ask questions about the database."
    }




