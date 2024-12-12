# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set the environment variable to ensure output is sent straight to terminal (non-buffered)
ENV PYTHONUNBUFFERED=1


# Install system dependencies including Rust
RUN apt-get update && \
    apt-get install -y \
        libmagic1 \
        curl \
        build-essential \
        && rm -rf /var/lib/apt/lists/* && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    PATH="/root/.cargo/bin:${PATH}"

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies (removing Windows-specific packages)
RUN . "$HOME/.cargo/env" && \
    pip install --upgrade pip && \
    grep -v -E "python-magic-bin|pywin32|pywinpty" requirements.txt > requirements_cleaned.txt && \
    pip install -r requirements_cleaned.txt && \
    pip install python-magic

    
# Set the port for the Streamlit app
ENV PORT=9000

# Expose the specified port
EXPOSE ${PORT}

# Copy the rest of the application code into the container
COPY . .

# Command to run the Streamlit app
ENTRYPOINT ["sh", "-c", "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]