# Utilisez une image de base Python
FROM python:3.11-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copiez tout le contenu actuel dans le répertoire de travail du conteneur
COPY . .

# Exécuter FastAPI lorsque le conteneur démarre
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]