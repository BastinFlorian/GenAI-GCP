"""
Configuration settings for the Generative AI application.
Contains credentials and settings for GCP services
including Cloud SQL and Storage.
"""

# GCP Project Settings
PROJECT_ID = "dauphine-437611"
REGION = "europe-west1"

# Cloud SQL Configuration
INSTANCE = "gen-ai-instance"
DATABASE = "gen_ai_db"
DB_USER = "students"
DB_PASSWORD = "|Q46Tr^tTqB8hSpO"

# Cloud Storage Configuration
BUCKET_NAME = "dauphine-bucket"
TABLE_NAME = "fb_table"

# API Configuration
GOOGLE_API_KEY = "AIzaSyA0BJ-l4g5TYK-Gd0fvK6lJMUIroDsr1rI"

# Local Storage
DOWNLOADED_LOCAL_DIRECTORY = "./downloaded_files"
# End-of-file (EOF)
