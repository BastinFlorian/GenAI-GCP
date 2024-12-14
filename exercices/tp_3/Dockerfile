# Dockerfile for Streamlit
FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED True

# Set a default value for PORT
ENV PORT 8080

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . .

EXPOSE ${PORT}

# Use the correct entry point
ENTRYPOINT ["streamlit", "run", "--server.port", "8080", "app.py", "--server.address=0.0.0.0"]
