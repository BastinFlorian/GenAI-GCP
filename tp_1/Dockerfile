FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=True

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PORT 8501git clone 

EXPOSE ${PORT}

COPY . ./app

ENTRYPOINT ["sh", "-c", "streamlit run --server.port=${PORT} --server.address=0.0.0.0 app/app.py"]

