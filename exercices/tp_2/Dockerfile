# Use the official Python image from Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Ensure that Python output is sent straight to terminal (without buffering)
ENV PYTHONUNBUFFERED True

# Copy the requirements.txt to the container
COPY requirements.txt /requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Set the default port for the app
ENV PORT=8080

# Expose the port
EXPOSE ${PORT}

# Copy the application code to the container
COPY . ./app

# Start the Streamlit app when the container starts
ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
