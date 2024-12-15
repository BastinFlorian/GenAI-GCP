# Utiliser une image Python comme base
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les dépendances nécessaires
COPY requirements.txt /requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Copier tout le code source dans le conteneur
COPY . .

# Exposer le port pour Streamlit
EXPOSE 8602

# Commande pour exécuter l'application Streamlit chnowa y affichi qui nexecuti streamlit 
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8602", "--server.address=0.0.0.0"]
