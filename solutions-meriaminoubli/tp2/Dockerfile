FROM python:3.9-slim

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Ajoutez ici l'installation de langchain_google_genai et d'autres dépendances
RUN pip install langchain_google_genai

# Copier le code de l'application
COPY . .

# Exposer le port
EXPOSE 8501

# Commande pour démarrer l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
