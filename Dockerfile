# Image Python officielle
FROM python:3.10-slim

# Créer le dossier de l'app
WORKDIR /app

# Copier les fichiers nécessaires
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l’API
EXPOSE 8000

# Lancer l'API au démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
