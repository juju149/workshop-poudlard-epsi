FROM python:3.9-slim

# Métadonnées
LABEL maintainer="Workshop Poudlard EPSI/WIS"
LABEL description="Reconnaissance vocale de formules magiques Harry Potter"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installe les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crée le répertoire de travail
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY src/ ./src/
COPY data/ ./data/
COPY models/ ./models/

# Expose le port pour Jupyter
EXPOSE 8888

# Commande par défaut: lance Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
