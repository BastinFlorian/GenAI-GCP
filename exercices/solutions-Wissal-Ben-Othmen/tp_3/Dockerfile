# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Set the environment variable to ensure output is sent straight to terminal (non-buffered)
ENV PYTHONUNBUFFERED=1

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set the port for the Streamlit app
ENV PORT=8080

# Expose the specified port
EXPOSE ${PORT}

# Copy the rest of the application code into the container
COPY . .

# Command to run the Streamlit app
ENTRYPOINT ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]
