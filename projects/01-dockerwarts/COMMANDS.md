# 📖 Guide de Commandes DOCKERWARTS

Guide de référence rapide pour toutes les commandes disponibles.

---

## 🚀 Démarrage rapide

```bash
# Installation initiale (run once)
cd /path/to/infra
make setup

# Démarrer tous les services
make start

# Vérifier le statut
make status

# Accéder aux services
# Ajouter à /etc/hosts : 127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local
```

---

## 📋 Commandes Make

### Gestion des services

```bash
make help        # Afficher l'aide
make setup       # Installation initiale complète
make start       # Démarrer tous les services
make stop        # Arrêter tous les services
make restart     # Redémarrer tous les services
make status      # Afficher le statut de tous les services
make health      # Vérifier la santé de tous les services
```

### Logs

```bash
make logs              # Suivre tous les logs
make logs-grafana      # Logs Grafana uniquement
make logs-elasticsearch # Logs Elasticsearch
make logs-cassandra    # Logs Cassandra
make logs-glpi         # Logs GLPI
make logs-traefik      # Logs Traefik
make logs-prometheus   # Logs Prometheus
```

### Sauvegardes

```bash
make backup      # Créer une sauvegarde complète
make restore     # Restaurer depuis une sauvegarde
```

### Nettoyage

```bash
make clean       # Arrêter et supprimer les containers (garde les données)
make clean-all   # Supprimer tout y compris les volumes (⚠️ PERTE DE DONNÉES)
```

### Mise à jour

```bash
make update      # Mettre à jour les images et redémarrer
```

### Accès rapide (ouvre le navigateur)

```bash
make dev-grafana   # Ouvrir Grafana
make dev-kibana    # Ouvrir Kibana
make dev-glpi      # Ouvrir GLPI
make dev-traefik   # Ouvrir Traefik Dashboard
```

---

## 🐳 Commandes Docker Compose

### Services

```bash
# Démarrer tous les services
docker-compose up -d

# Démarrer un service spécifique
docker-compose up -d grafana

# Arrêter tous les services
docker-compose stop

# Arrêter un service spécifique
docker-compose stop grafana

# Redémarrer un service
docker-compose restart grafana

# Voir le statut
docker-compose ps

# Voir les logs
docker-compose logs -f [service]

# Supprimer les containers (garde les volumes)
docker-compose down

# Supprimer tout (containers + volumes)
docker-compose down -v
```

### Build et pull

```bash
# Télécharger les images
docker-compose pull

# Rebuilder les images (si Dockerfiles modifiés)
docker-compose build

# Pull et rebuild
docker-compose up -d --build
```

---

## 🐋 Commandes Docker natives

### Containers

```bash
# Lister les containers en cours
docker ps

# Lister tous les containers
docker ps -a

# Inspecter un container
docker inspect dockerwarts-grafana

# Logs d'un container
docker logs -f dockerwarts-grafana

# Shell dans un container
docker exec -it dockerwarts-grafana /bin/sh

# Stats CPU/RAM en temps réel
docker stats

# Arrêter un container
docker stop dockerwarts-grafana

# Démarrer un container
docker start dockerwarts-grafana

# Supprimer un container
docker rm dockerwarts-grafana
```

### Volumes

```bash
# Lister les volumes
docker volume ls

# Inspecter un volume
docker volume inspect infra_grafana-data

# Voir l'utilisation disque
docker system df -v

# Nettoyer les volumes orphelins
docker volume prune

# Supprimer un volume spécifique (⚠️ perte de données)
docker volume rm infra_grafana-data
```

### Images

```bash
# Lister les images
docker images

# Supprimer les images non utilisées
docker image prune

# Supprimer une image spécifique
docker rmi grafana/grafana:10.2.0
```

### Networks

```bash
# Lister les réseaux
docker network ls

# Inspecter un réseau
docker network inspect infra_frontend

# Voir les containers sur un réseau
docker network inspect infra_backend | jq '.[0].Containers'
```

---

## 🔍 Commandes de diagnostic

### Elasticsearch

```bash
# Santé du cluster
curl http://localhost:9200/_cluster/health?pretty

# État des nœuds
curl http://localhost:9200/_cat/nodes?v

# État des indices
curl http://localhost:9200/_cat/indices?v

# Shell dans Elasticsearch
docker exec -it dockerwarts-elasticsearch-master /bin/bash
```

### Cassandra

```bash
# Status du cluster
docker exec dockerwarts-cassandra-node1 nodetool status

# Info du nœud
docker exec dockerwarts-cassandra-node1 nodetool info

# Vérifier la réplication
docker exec dockerwarts-cassandra-node1 nodetool ring

# Shell CQL
docker exec -it dockerwarts-cassandra-node1 cqlsh

# Inside cqlsh
DESCRIBE KEYSPACES;
```

### Prometheus

```bash
# Vérifier la santé
curl http://localhost:9090/-/healthy

# Vérifier les targets
curl http://localhost:9090/api/v1/targets | jq

# Requête métrique
curl 'http://localhost:9090/api/v1/query?query=up' | jq
```

### Grafana

```bash
# Vérifier la santé
curl http://localhost:3000/api/health

# Lister les datasources (avec auth)
curl -u admin:password http://localhost:3000/api/datasources
```

### Traefik

```bash
# Dashboard
open http://localhost:8080

# API - Lister les routers
curl http://localhost:8080/api/http/routers | jq

# API - Lister les services
curl http://localhost:8080/api/http/services | jq
```

---

## 💾 Commandes de sauvegarde

### Sauvegarde manuelle

```bash
# Sauvegarde complète
make backup

# Sauvegarde d'un volume spécifique
docker run --rm \
  -v infra_grafana-data:/data:ro \
  -v $(pwd)/backups:/backup \
  busybox tar czf /backup/grafana-$(date +%Y%m%d).tar.gz /data
```

### Restauration

```bash
# Restauration interactive
make restore

# Restauration d'un volume spécifique
docker run --rm \
  -v infra_grafana-data:/data \
  -v $(pwd)/backups:/backup \
  busybox sh -c "rm -rf /data/* && tar xzf /backup/grafana-20251013.tar.gz -C /"
```

### Snapshot Cassandra

```bash
# Créer un snapshot
docker exec dockerwarts-cassandra-node1 nodetool snapshot

# Lister les snapshots
docker exec dockerwarts-cassandra-node1 nodetool listsnapshots

# Copier le snapshot
docker cp dockerwarts-cassandra-node1:/var/lib/cassandra/data/snapshots ./backups/
```

### Snapshot Elasticsearch

```bash
# Créer un repository
curl -X PUT "localhost:9200/_snapshot/backup_repo" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/backup"
  }
}'

# Créer un snapshot
curl -X PUT "localhost:9200/_snapshot/backup_repo/snapshot_$(date +%Y%m%d)"

# Lister les snapshots
curl "localhost:9200/_snapshot/backup_repo/_all?pretty"
```

---

## 🔧 Commandes de maintenance

### Mise à jour des services

```bash
# Pull nouvelles images
docker-compose pull

# Recréer les containers avec nouvelles images
docker-compose up -d

# Ou en une commande
make update
```

### Nettoyage système

```bash
# Nettoyer tout ce qui est inutilisé
docker system prune -a

# Nettoyer uniquement les volumes
docker volume prune

# Nettoyer uniquement les images
docker image prune -a

# Voir l'espace utilisé
docker system df
```

### Logs rotation

```bash
# Tronquer les logs d'un container
truncate -s 0 $(docker inspect --format='{{.LogPath}}' dockerwarts-grafana)

# Configurer la rotation dans docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## 🌐 Commandes réseau

### Test de connectivité

```bash
# Ping entre containers
docker exec dockerwarts-grafana ping prometheus

# Test HTTP
docker exec dockerwarts-grafana curl http://prometheus:9090/-/healthy

# DNS lookup
docker exec dockerwarts-grafana nslookup prometheus
```

### Inspection réseau

```bash
# Inspecter un réseau
docker network inspect infra_frontend

# Voir les containers sur un réseau
docker network inspect infra_backend --format='{{range .Containers}}{{.Name}} {{end}}'
```

---

## 🔒 Commandes de sécurité

### Scanner les vulnérabilités

```bash
# Installer Trivy
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update && sudo apt install trivy

# Scanner une image
trivy image grafana/grafana:10.2.0

# Scanner toutes les images
docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" | xargs -I {} trivy image {}
```

### Vérifier les secrets

```bash
# Chercher des secrets exposés
docker inspect dockerwarts-grafana | grep -i password

# Vérifier les variables d'environnement
docker exec dockerwarts-grafana env | grep -i password
```

---

## 📊 Monitoring

### Métriques Prometheus

```bash
# CPU usage
curl 'http://localhost:9090/api/v1/query?query=container_cpu_usage_seconds_total' | jq

# Memory usage
curl 'http://localhost:9090/api/v1/query?query=container_memory_usage_bytes' | jq

# Disk usage
curl 'http://localhost:9090/api/v1/query?query=node_filesystem_avail_bytes' | jq
```

### Alertes

```bash
# Lister les alertes actives
curl http://localhost:9090/api/v1/alerts | jq

# Lister les règles
curl http://localhost:9090/api/v1/rules | jq
```

---

## 🆘 Dépannage

### Service ne démarre pas

```bash
# Voir les logs détaillés
docker-compose logs [service]

# Inspecter le container
docker inspect dockerwarts-[service]

# Vérifier la santé
docker inspect --format='{{.State.Health.Status}}' dockerwarts-[service]

# Recréer le container
docker-compose up -d --force-recreate [service]
```

### Problème de volume

```bash
# Vérifier le volume
docker volume inspect infra_[volume-name]

# Voir le contenu
docker run --rm -v infra_[volume-name]:/data busybox ls -la /data

# Réparer les permissions
docker run --rm -v infra_[volume-name]:/data busybox chown -R 1000:1000 /data
```

### Réseau cassé

```bash
# Recréer les réseaux
docker-compose down
docker network prune
docker-compose up -d
```

---

## 📚 Ressources

- Documentation complète: `README.md`
- Architecture: `docs/architecture.md`
- Réseau: `docs/network.md`
- Volumes: `docs/volumes.md`
- Production: `docs/production.md`

---

**Référence rapide créée ! 📖✨**
