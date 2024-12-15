# Use official Python image as the base image
FROM python:3.11


# Set the environment variable for unbuffered output (useful for logging)
ENV PYTHONUNBUFFERED=True

# Copy requirements.txt to the container and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Copy the entire app code to the container
COPY . .

# Set the entry point to run the Streamlit app with dynamic port assignment
ENTRYPOINT ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]

# Default to port 8080 if not specified
ENV PORT 8080

# Expose the port (default is 8080)
EXPOSE 8080
