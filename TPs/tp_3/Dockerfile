# Utilisez l'image officielle Python depuis Docker Hub
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt /requirements.txt
# Copier le fichier .env.template dans le conteneur
COPY .env.template .env.template

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Définir le port sur lequel l'application Streamlit fonctionne
ENV PORT=8080

# Exposer le port pour l'application Streamlit
EXPOSE ${PORT}

# Copier tout le code de l'application dans le conteneur
COPY . ./app

# Lancer Streamlit avec le bon port et adresse
ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
