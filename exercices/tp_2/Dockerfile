# Utiliser une image de base Python
FROM python:3.11-slim

# Installer Streamlit
RUN pip install streamlit

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application dans le conteneur
COPY . .

# Exposer le port que Streamlit utilisera
EXPOSE 8080

# Lancer Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
