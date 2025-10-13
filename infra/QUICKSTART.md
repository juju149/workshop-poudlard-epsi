# 🚀 Quick Start - DOCKERWARTS

Guide de démarrage rapide pour lancer l'infrastructure en 5 minutes.

---

## ⚡ Démarrage ultra-rapide

```bash
# 1. Cloner le repo
git clone <repo-url>
cd infra

# 2. Lancer l'installation automatique
make setup
```

C'est tout ! L'infrastructure sera prête en quelques minutes. ✨

---

## 📋 Prérequis vérifiés

Avant de commencer, assurez-vous d'avoir :

- ✅ Docker Engine 20.10+ installé
- ✅ Docker Compose 2.0+ installé
- ✅ 8 GB RAM minimum (16 GB recommandé)
- ✅ 20 GB d'espace disque libre
- ✅ Connexion internet pour télécharger les images

### Vérification rapide

```bash
docker --version        # Doit afficher 20.10+
docker compose version  # Doit afficher 2.0+
free -h                 # Vérifier RAM disponible
df -h                   # Vérifier espace disque
```

---

## 🎯 Option 1 : Installation automatique (Recommandé)

### Étape 1 : Cloner

```bash
git clone <repo-url>
cd infra
```

### Étape 2 : Installer

```bash
make setup
```

Le script `setup.sh` va :
- ✅ Vérifier Docker et les prérequis
- ✅ Configurer les variables d'environnement
- ✅ Ajuster les paramètres système (Elasticsearch)
- ✅ Télécharger les images Docker
- ✅ Démarrer tous les services
- ✅ Vérifier la santé des services

### Étape 3 : Configurer /etc/hosts

```bash
echo '127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local' | sudo tee -a /etc/hosts
```

### Étape 4 : Accéder aux services

Ouvrir dans votre navigateur :
- **Grafana** : http://grafana.dockerwarts.local
- **GLPI** : http://glpi.dockerwarts.local
- **Kibana** : http://kibana.dockerwarts.local
- **Traefik** : http://localhost:8080

---

## 🔧 Option 2 : Installation manuelle

Si vous préférez contrôler chaque étape :

### 1. Configuration système (Linux seulement)

```bash
# Augmenter vm.max_map_count pour Elasticsearch
sudo sysctl -w vm.max_map_count=262144

# Rendre permanent
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

### 2. Variables d'environnement

```bash
# Copier le template
cp .env.example .env

# Éditer et changer les mots de passe
nano .env
```

### 3. Démarrer les services

```bash
# Télécharger les images
docker compose pull

# Démarrer en arrière-plan
docker compose up -d

# Vérifier le statut
docker compose ps
```

### 4. Vérifier la santé

```bash
make health
```

Attendre que tous les services affichent "running" ou "healthy".

---

## 📊 Vérifications post-installation

### 1. Vérifier les services

```bash
# Voir le statut
make status

# Ou avec docker compose
docker compose ps
```

Tous les services doivent être "Up" et "healthy" (sauf Prometheus qui peut être juste "Up").

### 2. Tester les endpoints

```bash
# Traefik
curl http://localhost:8080/api/http/routers

# Elasticsearch
curl http://localhost:9200/_cluster/health

# Prometheus
curl http://localhost:9090/-/healthy

# Grafana (doit rediriger)
curl -I http://grafana.dockerwarts.local
```

### 3. Vérifier les clusters

```bash
# Elasticsearch cluster
curl http://localhost:9200/_cat/nodes?v

# Cassandra cluster
docker exec dockerwarts-cassandra-node1 nodetool status
```

---

## 🌐 Accès aux interfaces

### Configurer DNS local

**Option 1 : /etc/hosts (Linux/Mac)**
```bash
sudo sh -c 'echo "127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local" >> /etc/hosts'
```

**Option 2 : hosts (Windows)**
Éditer `C:\Windows\System32\drivers\etc\hosts` (en tant qu'admin) :
```
127.0.0.1 grafana.dockerwarts.local
127.0.0.1 glpi.dockerwarts.local
127.0.0.1 kibana.dockerwarts.local
```

### URLs d'accès

| Service | URL | Credentials par défaut |
|---------|-----|------------------------|
| **Grafana** | http://grafana.dockerwarts.local | admin / changeme_grafana_password |
| **GLPI** | http://glpi.dockerwarts.local | (suivre wizard) |
| **Kibana** | http://kibana.dockerwarts.local | - |
| **Traefik** | http://localhost:8080 | - |

⚠️ **Important** : Changez les mots de passe dès la première connexion !

---

## 🎮 Commandes de base

### Gestion des services

```bash
make start    # Démarrer
make stop     # Arrêter
make restart  # Redémarrer
make status   # Voir le statut
make health   # Vérifier la santé
make logs     # Voir les logs
```

### Logs spécifiques

```bash
make logs-grafana       # Logs Grafana
make logs-elasticsearch # Logs Elasticsearch
make logs-cassandra     # Logs Cassandra
```

### Sauvegarde

```bash
make backup   # Créer un backup
make restore  # Restaurer
```

---

## 🐛 Troubleshooting rapide

### Les services ne démarrent pas

```bash
# Voir les logs
make logs

# Vérifier l'espace disque
df -h

# Vérifier la mémoire
free -h

# Redémarrer
make restart
```

### Elasticsearch ne démarre pas

```bash
# Vérifier vm.max_map_count (doit être >= 262144)
sysctl vm.max_map_count

# Le fixer
sudo sysctl -w vm.max_map_count=262144
```

### Cassandra est lent

C'est normal ! Cassandra prend 2-3 minutes pour démarrer complètement.

```bash
# Attendre et vérifier
docker logs -f dockerwarts-cassandra-node1

# Vérifier le statut
docker exec dockerwarts-cassandra-node1 nodetool status
```

### "Cannot connect to Docker daemon"

```bash
# Vérifier que Docker tourne
sudo systemctl status docker

# Démarrer Docker
sudo systemctl start docker

# Vérifier les permissions
sudo usermod -aG docker $USER
# Puis se déconnecter/reconnecter
```

### Les URLs ne fonctionnent pas

```bash
# Vérifier /etc/hosts
cat /etc/hosts | grep dockerwarts

# Ajouter si manquant
echo '127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local' | sudo tee -a /etc/hosts

# Vérifier Traefik
curl http://localhost:8080/api/http/routers
```

---

## 📖 Premiers pas

### 1. Configurer Grafana

1. Ouvrir http://grafana.dockerwarts.local
2. Login : `admin` / `changeme_grafana_password` (voir .env)
3. Changer le mot de passe
4. Aller dans Dashboards → Browse
5. Ouvrir "Infrastructure Overview"

### 2. Configurer GLPI

1. Ouvrir http://glpi.dockerwarts.local
2. Sélectionner la langue
3. Accepter la licence
4. Configuration BDD :
   - Serveur : `glpi-db`
   - Utilisateur : `glpi_user`
   - Mot de passe : (voir .env)
   - Base : `glpidb`
5. Suivre l'assistant

### 3. Explorer Kibana

1. Ouvrir http://kibana.dockerwarts.local
2. Cliquer sur "Explore on my own"
3. Aller dans Management → Dev Tools
4. Tester : `GET /_cluster/health`

### 4. Vérifier Traefik

1. Ouvrir http://localhost:8080
2. Voir les routers configurés
3. Vérifier les services exposés

---

## 🎓 Tutoriels rapides

### Insérer des données dans Elasticsearch

```bash
# Créer un index
curl -X PUT "localhost:9200/test-index"

# Insérer un document
curl -X POST "localhost:9200/test-index/_doc" -H 'Content-Type: application/json' -d'
{
  "name": "Harry Potter",
  "house": "Gryffindor",
  "year": 7
}'

# Rechercher
curl -X GET "localhost:9200/test-index/_search?pretty"
```

### Créer un keyspace Cassandra

```bash
# Shell CQL
docker exec -it dockerwarts-cassandra-node1 cqlsh

# Dans cqlsh
CREATE KEYSPACE test_keyspace WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 2
};

USE test_keyspace;

CREATE TABLE users (
  id UUID PRIMARY KEY,
  name text,
  email text
);

INSERT INTO users (id, name, email) VALUES (
  uuid(),
  'Harry Potter',
  'harry@poudlard.fr'
);

SELECT * FROM users;
```

### Créer un dashboard Grafana

1. Ouvrir Grafana
2. Cliquer sur "+" → Dashboard
3. Add panel
4. Query :
   ```
   rate(container_cpu_usage_seconds_total[5m])
   ```
5. Sauvegarder

---

## 📚 Documentation complète

Pour aller plus loin :

- **README principal** : `README.md`
- **Architecture** : `docs/architecture.md`
- **Réseau** : `docs/network.md`
- **Volumes et backups** : `docs/volumes.md`
- **Production** : `docs/production.md`
- **Sécurité** : `docs/security.md`
- **Référence commandes** : `COMMANDS.md`

---

## 🆘 Besoin d'aide ?

### Ressources

- Documentation officielle Docker : https://docs.docker.com/
- Docker Compose : https://docs.docker.com/compose/
- Traefik : https://doc.traefik.io/traefik/
- Elasticsearch : https://www.elastic.co/guide/
- Cassandra : https://cassandra.apache.org/doc/
- Grafana : https://grafana.com/docs/

### Commandes utiles

```bash
make help       # Voir toutes les commandes
make status     # État des services
make logs       # Logs en temps réel
make health     # Santé des services
docker compose ps # État détaillé
```

---

**Bon déploiement ! 🚀✨**
