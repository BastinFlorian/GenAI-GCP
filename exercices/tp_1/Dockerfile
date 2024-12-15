FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=True

# Copy the requirements file and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Set the port to 8080
ENV PORT=8080

# Expose port 8080 to the outside world
EXPOSE ${PORT}

# Copy all files to the app directory
COPY . /app

# Run the Streamlit app using the specified port and address
ENTRYPOINT ["streamlit", "run", "--server.port", "${PORT}", "app/app.py", "--server.address=0.0.0.0"]