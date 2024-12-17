FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Assurer un affichage sans buffer pour les logs
ENV PYTHONUNBUFFERED True

# Copier et installer les dépendances
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Définir le port à exposer
ENV PORT=8501

EXPOSE ${PORT}

# Copier l'intégralité du code source
COPY . .

# Définir le point d'entrée pour Streamlit
ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
