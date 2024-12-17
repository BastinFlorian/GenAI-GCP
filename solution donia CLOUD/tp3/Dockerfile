# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans l'image
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source dans l'image
COPY . .

# Exposer le port de l'application
EXPOSE 8787

# Commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8787", "--server.address=0.0.0.0"]