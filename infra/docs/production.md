# 🚀 Guide de Déploiement en Production

## Prérequis Production

### Infrastructure minimale requise

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 16 GB | 32+ GB |
| **Disque** | 100 GB SSD | 500+ GB SSD/NVMe |
| **Réseau** | 100 Mbps | 1+ Gbps |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

### Logiciels

- Docker Engine 24.0+
- Docker Compose 2.20+
- Fail2ban (sécurité)
- UFW ou iptables (firewall)

---

## Checklist Pré-déploiement

### Sécurité

- [ ] Serveur durci (SSH key-only, désactivation root login)
- [ ] Firewall configuré (UFW/iptables)
- [ ] Fail2ban actif
- [ ] Mises à jour système appliquées
- [ ] Utilisateur non-root pour Docker
- [ ] Certificats SSL/TLS prêts (Let's Encrypt ou commercial)

### Configuration

- [ ] Domaines DNS configurés et validés
- [ ] Mots de passe forts générés pour tous les services
- [ ] Fichier .env créé avec valeurs production
- [ ] Sauvegardes configurées
- [ ] Monitoring externe configuré (uptimerobot, pingdom, etc.)

### Réseau

- [ ] Ports ouverts : 80, 443
- [ ] Domaines pointant vers l'IP du serveur
- [ ] Reverse proxy/CDN configuré (Cloudflare, etc.)

---

## Étape 1 : Préparation du serveur

### 1.1 Connexion et mise à jour

```bash
# Connexion SSH
ssh user@production-server.com

# Mise à jour système
sudo apt update && sudo apt upgrade -y

# Installation des outils de base
sudo apt install -y curl wget git vim htop net-tools
```

### 1.2 Installation Docker

```bash
# Installation Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# Déconnexion/reconnexion pour appliquer
exit
# SSH à nouveau
```

### 1.3 Vérification

```bash
docker --version
docker compose version
```

---

## Étape 2 : Configuration Firewall

### UFW (Ubuntu Firewall)

```bash
# Installation
sudo apt install -y ufw

# Configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Autoriser SSH (IMPORTANT avant d'activer!)
sudo ufw allow 22/tcp

# Autoriser HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activer
sudo ufw enable

# Vérifier
sudo ufw status verbose
```

### Fail2ban

```bash
# Installation
sudo apt install -y fail2ban

# Copier la config par défaut
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Éditer la config
sudo nano /etc/fail2ban/jail.local

# Activer et démarrer
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Vérifier
sudo fail2ban-client status
```

---

## Étape 3 : Configuration système pour Elasticsearch

```bash
# Augmenter vm.max_map_count (permanent)
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Augmenter les limites de fichiers
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* soft memlock unlimited" | sudo tee -a /etc/security/limits.conf
echo "* hard memlock unlimited" | sudo tee -a /etc/security/limits.conf
```

---

## Étape 4 : Déploiement de l'infrastructure

### 4.1 Cloner le repository

```bash
# Créer le répertoire
sudo mkdir -p /opt/dockerwarts
sudo chown $USER:$USER /opt/dockerwarts

# Cloner
cd /opt/dockerwarts
git clone <repo-url> .
cd infra
```

### 4.2 Configuration des variables d'environnement

```bash
# Copier le template
cp .env.example .env

# Générer des mots de passe forts
GLPI_ROOT_PASS=$(openssl rand -base64 32)
GLPI_USER_PASS=$(openssl rand -base64 32)
GRAFANA_PASS=$(openssl rand -base64 32)

# Éditer .env avec les vrais mots de passe
nano .env
```

Contenu `.env` production :
```env
# GLPI Database
GLPI_DB_ROOT_PASSWORD=<mot-de-passe-très-fort-généré>
GLPI_DB_NAME=glpidb
GLPI_DB_USER=glpi_user
GLPI_DB_PASSWORD=<mot-de-passe-très-fort-généré>

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=<mot-de-passe-très-fort-généré>

# Timezone
TIMEZONE=Europe/Paris
```

⚠️ **Sauvegarder ces mots de passe dans un gestionnaire sécurisé (1Password, Bitwarden, etc.)**

### 4.3 Configuration SSL avec Let's Encrypt

Modifier `docker-compose.yml` pour Traefik :

```yaml
traefik:
  command:
    - "--api.insecure=false"  # Désactiver dashboard non sécurisé
    - "--providers.docker=true"
    - "--providers.docker.exposedbydefault=false"
    - "--entrypoints.web.address=:80"
    - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
    - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
    - "--entrypoints.websecure.address=:443"
    - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
    - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"  # CHANGER
    - "--certificatesresolvers.letsencrypt.acme.storage=/certs/acme.json"
    - "--log.level=INFO"
```

Ajouter aux labels des services :
```yaml
labels:
  - "traefik.http.routers.grafana.tls=true"
  - "traefik.http.routers.grafana.tls.certresolver=letsencrypt"
```

### 4.4 Lancer les services

```bash
# Première installation
make setup

# Ou manuellement
docker compose pull
docker compose up -d

# Vérifier
make status
make health
```

---

## Étape 5 : Configuration DNS

### Enregistrements DNS requis

Chez votre registrar/DNS provider, ajouter :

```
Type  Nom                          Valeur                 TTL
A     grafana.example.com          <IP-SERVEUR>          300
A     glpi.example.com             <IP-SERVEUR>          300
A     kibana.example.com           <IP-SERVEUR>          300

# Ou avec wildcard
A     *.dockerwarts.example.com    <IP-SERVEUR>          300
```

### Vérification DNS

```bash
# Attendre la propagation (5-60 minutes)
nslookup grafana.example.com
dig grafana.example.com +short
```

---

## Étape 6 : Configuration des services

### 6.1 GLPI - Première configuration

1. Accéder à `https://glpi.example.com`
2. Suivre l'assistant d'installation
3. Utiliser les credentials de `.env`
4. Créer les utilisateurs et configurer

### 6.2 Grafana - Configuration

```bash
# Accéder à Grafana
open https://grafana.example.com

# Login : admin / <GRAFANA_ADMIN_PASSWORD>

# Étapes :
# 1. Changer le mot de passe admin (si pas déjà fait)
# 2. Vérifier les datasources (Prometheus, Elasticsearch)
# 3. Importer/vérifier les dashboards
# 4. Configurer les alertes
```

### 6.3 Elasticsearch - Vérification

```bash
# Santé du cluster
curl http://localhost:9200/_cluster/health?pretty

# Doit retourner "status": "green" ou "yellow"
```

### 6.4 Cassandra - Vérification

```bash
# Status du cluster
docker exec dockerwarts-cassandra-node1 nodetool status

# Doit afficher UN (Up Normal) pour les 2 nœuds
```

---

## Étape 7 : Sauvegardes automatiques

### 7.1 Configuration cron

```bash
# Éditer crontab
crontab -e

# Ajouter ces lignes :
# Backup quotidien à 2h du matin
0 2 * * * cd /opt/dockerwarts/infra && make backup >> /var/log/dockerwarts-backup.log 2>&1

# Cleanup backups > 30 jours à 3h
0 3 * * * find /opt/dockerwarts/infra/backups -name "*.tar.gz" -mtime +30 -delete

# Sync vers serveur distant à 4h
0 4 * * * rsync -avz /opt/dockerwarts/infra/backups/ backup-server:/backups/dockerwarts/
```

### 7.2 Test manuel

```bash
# Tester le backup
make backup

# Vérifier
ls -lh backups/
```

---

## Étape 8 : Monitoring externe

### 8.1 Uptime monitoring

Services recommandés :
- **UptimeRobot** (gratuit, 50 monitors)
- **Pingdom**
- **StatusCake**

Monitorer :
- https://grafana.example.com
- https://glpi.example.com
- https://kibana.example.com

### 8.2 Alertes

Configurer des alertes email/SMS/Slack pour :
- Services down
- Certificats SSL expirés
- Espace disque < 20%
- Backups échoués

---

## Étape 9 : Hardening sécurité

### 9.1 Authentification renforcée

```bash
# Grafana : Activer OAuth ou LDAP
# Modifier configs/grafana/provisioning/grafana.ini

# GLPI : Activer 2FA
# Via l'interface web GLPI

# Traefik : Activer authentification basique pour dashboard
```

### 9.2 Secrets Docker

Remplacer les variables d'environnement par des secrets :

```yaml
# docker-compose.yml
secrets:
  glpi_db_password:
    file: ./secrets/glpi_db_password.txt

services:
  glpi-db:
    secrets:
      - glpi_db_password
    environment:
      - MYSQL_PASSWORD_FILE=/run/secrets/glpi_db_password
```

### 9.3 Rate limiting

Ajouter dans Traefik :
```yaml
# docker-compose.yml - Traefik
command:
  - "--api.insecure=false"
  - "--middlewares.rate-limit.ratelimit.average=100"
  - "--middlewares.rate-limit.ratelimit.burst=50"
```

---

## Étape 10 : Tests de charge

### 10.1 Test avec Apache Bench

```bash
# Installer
sudo apt install apache2-utils

# Test Grafana (100 requêtes, 10 concurrentes)
ab -n 100 -c 10 https://grafana.example.com/

# Test GLPI
ab -n 100 -c 10 https://glpi.example.com/
```

### 10.2 Test avec k6

```bash
# Installer k6
sudo apt install k6

# Script de test
cat > load-test.js <<'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 10 },
    { duration: '5m', target: 10 },
    { duration: '2m', target: 0 },
  ],
};

export default function () {
  let res = http.get('https://grafana.example.com');
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);
}
EOF

# Lancer
k6 run load-test.js
```

---

## Maintenance

### Mises à jour

```bash
# Mettre à jour les images
cd /opt/dockerwarts/infra
make update

# Ou manuellement
docker compose pull
docker compose up -d
```

### Logs

```bash
# Tous les logs
make logs

# Service spécifique
make logs-grafana

# Suivre en temps réel
make logs | grep ERROR
```

### Monitoring ressources

```bash
# CPU/RAM par container
docker stats

# Espace disque volumes
docker system df -v
```

---

## Rollback en cas de problème

### Rollback rapide

```bash
# Arrêter les nouveaux services
make stop

# Restaurer le backup
make restore

# Redémarrer avec l'ancienne version
git checkout <commit-hash>
make start
```

---

## Checklist Post-déploiement

- [ ] Tous les services sont up et healthy
- [ ] SSL/TLS fonctionne (certificats valides)
- [ ] DNS pointe correctement
- [ ] Accès aux interfaces web fonctionnels
- [ ] Monitoring externe configuré et actif
- [ ] Backups automatiques testés
- [ ] Alertes configurées et testées
- [ ] Documentation à jour avec les URLs de prod
- [ ] Équipe formée aux procédures
- [ ] Plan de disaster recovery documenté
- [ ] Tests de charge passés avec succès

---

## Support et escalade

### Niveaux de support

**Niveau 1** : Vérifications basiques
- Vérifier les logs
- Redémarrer les services
- Vérifier l'espace disque

**Niveau 2** : Investigation
- Analyser les métriques Grafana
- Vérifier la santé des clusters
- Restaurer depuis backup

**Niveau 3** : Escalade
- Problèmes de corruption de données
- Performance dégradée inexpliquée
- Incidents de sécurité

---

## Contacts

- **Admin système** : admin@example.com
- **DevOps Lead** : devops@example.com
- **Support 24/7** : support@example.com

---

**Bonne mise en production ! 🚀**
