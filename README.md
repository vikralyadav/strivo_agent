# Database Assistant - Strivo Agent

An intelligent AI-powered database assistant that answers natural language questions without exposing technical details. Ask questions in plain English, get answers in plain English.

## Features

- 🤖 **Natural Language Processing** - Ask questions in plain English, no SQL knowledge needed
- 🔍 **Smart Query Generation** - Uses AI (GPT-4) to convert natural language to optimized SQL
- 💾 **Database Integration** - Seamlessly works with MySQL databases
- 📊 **User-Friendly Responses** - Converts database results into simple, conversational answers
- 🔒 **Privacy-First** - Never exposes SQL queries, schema, or technical details to users
- ⚡ **Fast & Optimized** - Generates optimized SQL with proper indexing suggestions

## Project Structure

```
strivo_agent/
├── app.py                 # FastAPI application & endpoints
├── database.py            # Database connection & schema management
├── query_generator.py     # Natural language to SQL conversion
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## Installation

### Prerequisites
- Python 3.8+
- MySQL database
- OpenAI API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd strivo_agent
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   MYSQL_HOST=your_mysql_host
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_DATABASE=your_database_name
   MYSQL_PORT=3306
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Test the database connection:**
   ```bash
   python database.py
   ```

## Usage

### Option 1: Run as a CLI Tool

```bash
python query_generator.py
```

Then enter your question:
```
Enter your question: How many users signed up last week?
```

You'll get a simple answer:
```
120 new users joined the platform last week.
```

### Option 2: Run as a Web API

1. **Start the FastAPI server:**
   ```bash
   uvicorn app:app --reload
   ```

2. **Make a request to the API:**
   ```bash
   curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the top 3 selling products?"}'
   ```

3. **Example Response:**
   ```json
   {
     "answer": "The most popular products are laptops, phones, and headphones. Laptops had the highest sales with 320 purchases, followed by phones and headphones."
   }
   ```

## API Endpoints

### POST `/ask`
Ask the database a question in plain English.

**Request:**
```json
{
  "query": "Your question here"
}
```

**Response:**
```json
{
  "answer": "A clear, conversational answer"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "How many active users do we have?"}'
```

### GET `/`
Welcome endpoint with API documentation.

## How It Works

1. **User asks a question** - "How many customers bought in the last month?"
2. **System generates SQL** - Converts the question to an optimized SQL query (hidden from user)
3. **Query executes** - Fetches data from the MySQL database
4. **Results formatted** - Converts raw data into a friendly, readable answer
5. **User receives answer** - "523 customers made purchases last month"

## Core Components

### `app.py`
- FastAPI application
- `/ask` endpoint for questions
- Error handling with user-friendly messages
- Response validation

### `database.py`
- MySQL connection setup using SQLAlchemy
- Schema detection
- Connection testing
- Environment variable management

### `query_generator.py`
- OpenAI GPT-4 integration for natural language to SQL conversion
- SQL validation and cleaning
- Query execution
- Result formatting to plain English
- Optimization suggestions

### `main.py`
- Entry point for the application
- Simple message display

## Guidelines

The assistant follows these principles:

✅ **Do:**
- Explain results in simple, non-technical language
- Use friendly, conversational tone
- Ask for clarification if questions are unclear
- Keep answers short and focused

❌ **Don't:**
- Show SQL queries to users
- Display schema or technical details
- Use jargon or technical terms
- Make assumptions about unclear questions

## Error Handling

The system provides user-friendly error messages:

- **"I'm having trouble understanding your question. Could you rephrase it?"** - When query generation fails
- **"Sorry, I couldn't find that information in the database. Could you ask your question in a different way?"** - When no results found
- **"Please ask a valid question."** - When input is empty or invalid

## Example Questions

```
"How many users signed up last week?"
"What are the top 5 products by revenue?"
"Show me the average order value by month"
"Which customers spent the most in Q1?"
"How many active users do we have right now?"
```

## Requirements

See `requirements.txt` for full dependency list. Key packages:

- **fastapi** - Web framework
- **sqlalchemy** - Database ORM
- **mysql-connector-python** - MySQL driver
- **openai** - GPT-4 integration
- **python-dotenv** - Environment variables
- **sqlparse** - SQL parsing
- **pydantic** - Data validation

## Configuration

All configuration is managed through `.env` file. See the example above for required variables.

## Troubleshooting

**"Connection refused" error:**
- Check MySQL is running
- Verify database credentials in `.env`
- Test with `python database.py`

**"Invalid API key" error:**
- Verify OpenAI API key in `.env`
- Check that the key has API access enabled

**"SQL validation error":**
- The generated SQL may be invalid
- Try rephrasing your question
- Check database schema matches expectations

## License

This project is created for Strivo Brickley.

## Support

For issues or questions, please contact the development team.
