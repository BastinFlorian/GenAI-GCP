FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PORT=8502

EXPOSE 8502

COPY . ./app

ENTRYPOINT ["streamlit", "run", "--server.port", "8502", "--server.address", "0.0.0.0", "app/app.py"]

