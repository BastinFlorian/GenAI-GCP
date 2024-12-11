FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

EXPOSE 8080

COPY . ./app

ENTRYPOINT ["streamlit", "run", "--server.port", "8080", "app/app.py", "--server.address=0.0.0.0"]