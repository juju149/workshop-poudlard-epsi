FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Workshop Poudlard EPSI"
LABEL description="Easter Eggs - AI Stress Test"

# Répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copier le code source
COPY src/ ./src/

# Créer le dossier résultats
RUN mkdir -p /app/results

# Rendre le script exécutable
RUN chmod +x /app/src/ai_stress_test.py

# Commande par défaut
CMD ["python", "src/ai_stress_test.py"]
