import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database credentials
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

# Create MySQL connection URL
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to test connection
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            print(f"Connected to: {result.fetchone()[0]}")
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")

def get_schema():
    query = """
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = :database;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"database": MYSQL_DATABASE})
        schema_info = result.fetchall()
    
    schema_dict = {}
    for table, column, dtype in schema_info:
        if table not in schema_dict:
            schema_dict[table] = []
        schema_dict[table].append(f"{column} ({dtype})")

    return schema_dict


# Run connection test
if __name__ == "__main__":
    test_connection()