FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

EXPOSE 8501 

COPY . ./app

ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
