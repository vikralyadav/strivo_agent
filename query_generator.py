import os
import openai
import sqlparse
import re
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import engine, get_schema

# Load environment variables
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def clean_sql_output(response_text):
    """Removes markdown formatting and extracts the raw SQL query."""
    # Remove Markdown code block formatting (```sql ... ```)
    clean_query = re.sub(r"```sql\n(.*?)\n```", r"\1", response_text, flags=re.DOTALL)

    # Extract only valid SQL (handles AI explanations)
    sql_match = re.search(r"SELECT .*?;", clean_query, re.DOTALL | re.IGNORECASE)

    return sql_match.group(0) if sql_match else clean_query.strip()

def validate_sql_query(sql_query):
    """Validates the SQL query syntax before execution."""
    try:
        parsed = sqlparse.parse(sql_query)
        if not parsed:
            return False, "Invalid SQL syntax."
        return True, None
    except Exception as e:
        return False, str(e)

def generate_sql_query(nl_query):
    """Converts natural language query to an optimized SQL query."""
    schema = get_schema()

    schema_text = "\n".join([f"{table}: {', '.join(columns)}" for table, columns in schema.items()])

    prompt = f"""
    You are an SQL expert. Convert the following natural language query into an optimized MySQL query.
    Ensure:
    - Proper use of INDEXING where applicable.
    - Use of efficient JOINS instead of nested queries.
    - Use GROUP BY when aggregations are needed.
    - Ensure SQL is valid and optimized for execution.

    Database Schema:
    {schema_text}

    User Request: {nl_query}

    SQL Query:
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a SQL optimization expert."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_sql_query = response.choices[0].message.content.strip()

        # Clean the response to extract only the SQL query
        clean_query = clean_sql_output(raw_sql_query)
        return clean_query

    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def suggest_index(sql_query):
    """Suggests indexes for the executed SQL query."""
    try:
        with engine.connect() as connection:
            explain_query = f"EXPLAIN {sql_query}"
            result = connection.execute(text(explain_query))
            execution_plan = result.fetchall()

        print("\nQuery Execution Plan:")
        for row in execution_plan:
            print(row)

        return "Consider adding an index on frequently used WHERE conditions."
    except Exception as e:
        return f"Could not generate execution plan: {e}"

def execute_query(sql_query):
    """Executes a validated and optimized SQL query."""
    is_valid, error_msg = validate_sql_query(sql_query)
    if not is_valid:
        print(f"SQL Validation Error: {error_msg}")
        return None

    try:
        # Open a separate connection for query execution
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            fetched_results = result.fetchall()

        return fetched_results
    except SQLAlchemyError as e:
        print(f"Database Execution Error: {str(e)}")
        return None

def format_results_as_text(results, original_query):
    """
    Converts database results into plain English explanations.
    Hides technical details and presents data in a friendly, conversational way.
    """
    if not results:
        return "No information available in the database for your question."
    
    # Count results
    result_count = len(results)
    
    # Extract column names from results
    if hasattr(results[0], 'keys'):
        columns = results[0].keys()
    else:
        columns = [f"Column {i+1}" for i in range(len(results[0]))]
    
    # Format single result
    if result_count == 1:
        row = results[0]
        if len(columns) == 1:
            # Single value response (count, total, etc.)
            col_name = list(columns)[0] if hasattr(columns, '__iter__') else columns
            value = row[0] if isinstance(row, tuple) else row[col_name]
            return f"{value}"
        else:
            # Multiple columns in single row
            formatted_parts = []
            for col, val in zip(columns, row):
                formatted_parts.append(f"{col}: {val}")
            return " | ".join(formatted_parts)
    
    # Format multiple results as a list
    response = f"Here are the results:\n\n"
    for idx, row in enumerate(results, 1):
        if len(columns) == 1:
            value = row[0] if isinstance(row, tuple) else row[list(columns)[0]]
            response += f"{idx}. {value}\n"
        else:
            row_data = []
            for col, val in zip(columns, row):
                row_data.append(f"{col}: {val}")
            response += f"{idx}. {' | '.join(row_data)}\n"
    
    return response.strip()

if __name__ == "__main__":
    user_input = input("Enter your question: ")
    sql_query = generate_sql_query(user_input)

    if sql_query:
        execution_results = execute_query(sql_query)
        if execution_results:
            user_friendly_response = format_results_as_text(execution_results, user_input)
            print(f"\n{user_friendly_response}")
        else:
            print("Sorry, I couldn't find that information in the database. Could you ask your question in a different way?")
    else:
        print("I'm having trouble understanding your question. Could you rephrase it?")