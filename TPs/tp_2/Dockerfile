# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API file
COPY api.py ./

# Expose the port
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "--server.port", "8080", "app/app.py", "--server.address=0.0.0.0"]
