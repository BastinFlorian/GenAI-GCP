import os
from sqlalchemy import create_engine

# Cloud SQL and database configuration
PROJECT_ID = "dauphine-437611"
REGION = "europe-west1"

# Database configuration
INSTANCE = "gen-ai-instance"
DATABASE = "gen_ai_db"
TABLE_NAME = "ae_table"
DB_USER = "students"
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Ensure this is set in the environment
DB_HOST = "127.0.0.1"  # Localhost address used with cloud-sql-proxy
DB_PORT = 3306  # Default port for MySQL

# Cloud Storage
BUCKET_NAME = "dauphine-bucket"

# Build the connection URL for SQLAlchemy
db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}"

# SQLAlchemy engine
try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        print("Connected successfully!")
except Exception as e:
    print(f"Connection failed: {e}")
