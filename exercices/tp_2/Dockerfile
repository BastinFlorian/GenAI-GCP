FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PORT=8080

EXPOSE ${PORT}

COPY . ./app

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]