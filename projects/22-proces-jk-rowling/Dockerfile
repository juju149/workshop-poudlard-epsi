FROM python:3.11-slim

LABEL maintainer="Workshop Poudlard"
LABEL description="Pipeline d'analyse textuelle Harry Potter - Défi 22"

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Répertoire de travail
WORKDIR /app

# Copier les requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/
COPY context/books/ ./src/../../context/books/

# Créer les répertoires de sortie
RUN mkdir -p /app/output /app/data

# Point d'entrée
WORKDIR /app/src

CMD ["python", "analyze_corpus.py"]
