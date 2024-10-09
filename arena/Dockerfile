FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED True

COPY arena/requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PORT=8080

EXPOSE ${PORT}

COPY arena/ ./app

CMD ["python", "app/app.py"]

