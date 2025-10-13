# 🔒 Sécurité - DOCKERWARTS

Guide de sécurité pour l'infrastructure DOCKERWARTS.

---

## Modèle de sécurité actuel

### ✅ Mesures implémentées

1. **Isolation réseau**
   - Séparation frontend/backend
   - Services de données isolés sur réseau backend
   - Pas d'exposition directe des bases de données

2. **Pare-feu applicatif**
   - Traefik comme point d'entrée unique
   - Filtrage au niveau HTTP
   - Support rate limiting (à configurer)

3. **Health checks**
   - Détection rapide des services défaillants
   - Restart automatique des services unhealthy

4. **Variables d'environnement**
   - Secrets stockés dans .env (non commité)
   - Template .env.example fourni

5. **Volumes persistants**
   - Données isolées par service
   - Backups réguliers possibles

---

## ⚠️ Points d'attention actuels

### Mode développement (configuration actuelle)

La configuration actuelle est adaptée pour le **développement** mais nécessite des améliorations pour la **production** :

1. **Elasticsearch** : Security désactivée (xpack.security.enabled=false)
2. **Traefik** : Dashboard exposé sans authentification (port 8080)
3. **Pas de SSL/TLS** : Communications en HTTP
4. **Mots de passe par défaut** : Dans .env.example
5. **Secrets en clair** : Variables d'environnement (pas Docker Secrets)

---

## 🛡️ Recommandations pour la production

### 1. SSL/TLS obligatoire

#### Activer Let's Encrypt dans Traefik

```yaml
# docker-compose.yml
traefik:
  command:
    - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
    - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
    - "--certificatesresolvers.letsencrypt.acme.storage=/certs/acme.json"
    - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
    - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
```

#### Ajouter certificats aux services

```yaml
labels:
  - "traefik.http.routers.grafana.tls=true"
  - "traefik.http.routers.grafana.tls.certresolver=letsencrypt"
```

### 2. Activer l'authentification Elasticsearch

```yaml
elasticsearch-master:
  environment:
    - xpack.security.enabled=true
    - ELASTIC_PASSWORD=<strong-password>
```

Puis configurer les utilisateurs et rôles.

### 3. Sécuriser Traefik Dashboard

```yaml
traefik:
  command:
    - "--api.insecure=false"
    - "--api.dashboard=true"
  labels:
    - "traefik.http.routers.dashboard.rule=Host(`traefik.example.com`)"
    - "traefik.http.routers.dashboard.service=api@internal"
    - "traefik.http.routers.dashboard.middlewares=auth"
    - "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$..."
```

Générer le hash du mot de passe :
```bash
htpasswd -nb admin password
```

### 4. Utiliser Docker Secrets

```yaml
# docker-compose.yml
secrets:
  grafana_password:
    file: ./secrets/grafana_password.txt
  
services:
  grafana:
    secrets:
      - grafana_password
    environment:
      - GF_SECURITY_ADMIN_PASSWORD_FILE=/run/secrets/grafana_password
```

### 5. Rate Limiting

```yaml
traefik:
  command:
    - "--api.insecure=false"
    - "--entrypoints.websecure.http.middlewares=rate-limit@docker"
  labels:
    - "traefik.http.middlewares.rate-limit.ratelimit.average=100"
    - "traefik.http.middlewares.rate-limit.ratelimit.burst=50"
```

### 6. WAF (Web Application Firewall)

Ajouter ModSecurity avec Traefik :

```yaml
# Plugin Traefik
experimental:
  plugins:
    modsecurity:
      moduleName: github.com/acouvreur/traefik-modsecurity-plugin
      version: v1.0.0
```

### 7. Scan de vulnérabilités

```bash
# Installer Trivy
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update && sudo apt install trivy

# Scanner toutes les images
docker compose config --images | xargs -I {} trivy image {}

# Automatiser avec cron
0 6 * * * cd /opt/dockerwarts/infra && docker compose config --images | xargs trivy image > /var/log/trivy-scan.log 2>&1
```

---

## 🔐 Gestion des secrets

### Hiérarchie de sécurité

1. **❌ Pire** : Secrets hardcodés dans docker-compose.yml
2. **⚠️ Moyen** : Secrets dans .env (actuel)
3. **✅ Bien** : Docker Secrets
4. **🌟 Meilleur** : Vault (HashiCorp) ou cloud secrets manager

### Créer des secrets Docker

```bash
# Créer le répertoire
mkdir -p secrets
chmod 700 secrets

# Créer les fichiers secrets
echo "strong-password-here" > secrets/grafana_password.txt
echo "strong-password-here" > secrets/glpi_db_password.txt
chmod 600 secrets/*

# Ajouter à .gitignore (déjà fait)
echo "secrets/" >> .gitignore
```

### Rotation des secrets

```bash
#!/bin/bash
# rotate-secrets.sh

# Générer nouveaux mots de passe
NEW_GRAFANA_PASS=$(openssl rand -base64 32)
NEW_GLPI_PASS=$(openssl rand -base64 32)

# Sauvegarder les anciens
cp secrets/grafana_password.txt secrets/grafana_password.txt.old
cp secrets/glpi_db_password.txt secrets/glpi_db_password.txt.old

# Écrire les nouveaux
echo "$NEW_GRAFANA_PASS" > secrets/grafana_password.txt
echo "$NEW_GLPI_PASS" > secrets/glpi_db_password.txt

# Redémarrer les services
docker compose up -d --force-recreate grafana glpi-db

echo "Secrets rotated successfully"
```

---

## 🔍 Audit et logging

### 1. Logs centralisés

Envoyer tous les logs vers Elasticsearch :

```yaml
# docker-compose.yml
x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
    tag: "{{.Name}}"

services:
  grafana:
    <<: *default-logging
```

### 2. Audit trail

Activer l'audit dans les services critiques :

**Elasticsearch** :
```yaml
environment:
  - xpack.security.audit.enabled=true
```

**Grafana** :
```ini
[log]
level = info
mode = file

[security]
admin_password = ${GF_SECURITY_ADMIN_PASSWORD}
login_remember_days = 7
cookie_secure = true
cookie_samesite = strict
```

### 3. Monitoring des accès

Créer des alertes dans Grafana pour :
- Tentatives de connexion échouées
- Accès non autorisés
- Modifications de configuration

---

## 🚨 Détection d'intrusion

### Fail2ban pour Docker

```bash
# Installer fail2ban
sudo apt install fail2ban

# Créer un filtre pour Traefik
sudo cat > /etc/fail2ban/filter.d/traefik-auth.conf <<EOF
[Definition]
failregex = ^<HOST> .* ".*" 401
            ^<HOST> .* ".*" 403
ignoreregex =
EOF

# Créer une jail
sudo cat > /etc/fail2ban/jail.d/traefik.conf <<EOF
[traefik-auth]
enabled = true
port = http,https
filter = traefik-auth
logpath = /var/lib/docker/containers/*/*.log
maxretry = 5
bantime = 3600
findtime = 600
EOF

# Redémarrer
sudo systemctl restart fail2ban
```

### Monitoring avec Prometheus

Créer des alertes :

```yaml
# prometheus/alerts.yml
groups:
  - name: security
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"4..|5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High HTTP error rate"
          
      - alert: UnauthorizedAccess
        expr: rate(http_requests_total{status="401"}[5m]) > 10
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Multiple unauthorized access attempts"
```

---

## 🔒 Hardening par service

### Traefik

```yaml
command:
  # Désactiver API non sécurisée
  - "--api.insecure=false"
  # Headers de sécurité
  - "--entrypoints.websecure.http.middlewares=security-headers@docker"
labels:
  - "traefik.http.middlewares.security-headers.headers.sslredirect=true"
  - "traefik.http.middlewares.security-headers.headers.stsSeconds=31536000"
  - "traefik.http.middlewares.security-headers.headers.stsIncludeSubdomains=true"
  - "traefik.http.middlewares.security-headers.headers.stsPreload=true"
  - "traefik.http.middlewares.security-headers.headers.contentTypeNosniff=true"
  - "traefik.http.middlewares.security-headers.headers.browserXssFilter=true"
```

### Elasticsearch

```yaml
environment:
  # Activer security
  - xpack.security.enabled=true
  - xpack.security.transport.ssl.enabled=true
  - xpack.security.http.ssl.enabled=true
  # Mots de passe forts
  - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
  - KIBANA_PASSWORD=${KIBANA_PASSWORD}
```

### Grafana

```yaml
environment:
  # Désactiver signup
  - GF_USERS_ALLOW_SIGN_UP=false
  # Forcer HTTPS
  - GF_SERVER_PROTOCOL=https
  # Session sécurisée
  - GF_SECURITY_COOKIE_SECURE=true
  # OAuth2
  - GF_AUTH_GENERIC_OAUTH_ENABLED=true
```

### Cassandra

```yaml
environment:
  # Activer authentification
  - CASSANDRA_AUTHENTICATOR=PasswordAuthenticator
  - CASSANDRA_AUTHORIZER=CassandraAuthorizer
  # SSL
  - CASSANDRA_INTERNODE_ENCRYPTION=all
```

---

## 📋 Checklist sécurité production

### Pré-déploiement

- [ ] SSL/TLS activé partout
- [ ] Mots de passe forts générés (32+ caractères)
- [ ] Docker Secrets implémentés
- [ ] Traefik dashboard sécurisé
- [ ] Elasticsearch security activée
- [ ] Rate limiting configuré
- [ ] Headers de sécurité HTTP configurés
- [ ] Fail2ban installé et configuré
- [ ] Firewall (UFW/iptables) configuré
- [ ] Scan de vulnérabilités effectué

### Post-déploiement

- [ ] Audit logging activé
- [ ] Monitoring des accès en place
- [ ] Alertes de sécurité configurées
- [ ] Procédure d'incident documentée
- [ ] Rotation des secrets planifiée
- [ ] Backups chiffrés
- [ ] Tests de pénétration effectués
- [ ] Documentation sécurité à jour

---

## 🆘 Procédure en cas d'incident

### 1. Détection

- Alertes Grafana
- Logs Elasticsearch
- Fail2ban notifications
- Monitoring externe

### 2. Isolation

```bash
# Isoler un service compromis
docker compose stop <service>

# Couper l'accès réseau
docker network disconnect infra_frontend dockerwarts-<service>
```

### 3. Investigation

```bash
# Examiner les logs
docker compose logs <service> --since 1h > incident-logs.txt

# Sauvegarder l'état
docker commit dockerwarts-<service> <service>-incident-$(date +%Y%m%d)

# Analyser le container
docker run --rm -it <service>-incident-$(date +%Y%m%d) /bin/sh
```

### 4. Restauration

```bash
# Arrêter le service
docker compose stop <service>

# Restaurer depuis backup
make restore

# Recréer le service
docker compose up -d --force-recreate <service>
```

### 5. Post-mortem

- Documenter l'incident
- Identifier la cause racine
- Implémenter des corrections
- Tester les corrections
- Mettre à jour la documentation

---

## 📚 Ressources

### Standards et frameworks

- **OWASP Top 10** : https://owasp.org/www-project-top-ten/
- **CIS Docker Benchmark** : https://www.cisecurity.org/benchmark/docker
- **NIST Cybersecurity Framework** : https://www.nist.gov/cyberframework

### Outils

- **Trivy** : Scanner de vulnérabilités
- **Fail2ban** : Protection contre brute force
- **ModSecurity** : WAF
- **Vault** : Gestion des secrets

### Formation

- Docker Security (Docker official)
- Kubernetes Security Specialization (Linux Foundation)
- OWASP courses

---

**Sécurité renforcée ! 🔒🛡️**
