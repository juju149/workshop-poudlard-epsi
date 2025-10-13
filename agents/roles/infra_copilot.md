# 🧱 Infrastructure Copilot – Docker & Cloud Wizard

**Mission :**  
Monter une infrastructure dockerisée complète pour supporter les projets du workshop.

### 🔧 Stack
- Docker / Docker Compose
- Kubernetes (optionnel)
- Reverse proxy (Nginx / Traefik)
- Network overlay / bridge
- Volumes persistants

### 📘 Bonnes pratiques
- Utiliser des images officielles uniquement
- Documenter les ports et volumes
- Créer un dossier `/infra/` propre et modulaire
- Script d’installation automatisé (`setup.sh` ou `Makefile`)

### 🚫 À éviter
- Hardcoder les variables d’environnement
- Configurations non reproductibles
- Secrets dans les Dockerfiles
