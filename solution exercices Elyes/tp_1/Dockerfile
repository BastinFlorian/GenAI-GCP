FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PORT=8501 

EXPOSE ${PORT}

COPY . ./app

ENTRYPOINT ["streamlit", "run", "--server.port", "8501", "app/app.py", "--server.address=0.0.0.0"]
