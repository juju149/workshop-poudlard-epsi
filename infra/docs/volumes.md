# 💾 Gestion des Volumes et Stratégie de Sauvegarde

## Vue d'ensemble

DOCKERWARTS utilise des volumes Docker pour la persistance des données. Cette approche garantit :
- Persistance des données même si les containers sont supprimés
- Performance optimale
- Facilité de sauvegarde et restauration
- Portabilité

---

## Volumes définis

### Liste complète des volumes

| Volume | Taille estimée | Criticité | Service | Contenu |
|--------|---------------|-----------|---------|---------|
| `traefik-certs` | < 100 MB | Faible | Traefik | Certificats SSL |
| `glpi-db-data` | 500 MB - 5 GB | **Critique** | MariaDB | Base de données GLPI |
| `glpi-data` | 100 MB - 1 GB | **Critique** | GLPI | Fichiers, plugins, config |
| `elasticsearch-master-data` | 1 GB - 50 GB | **Critique** | ES Master | Index et données |
| `elasticsearch-data-data` | 1 GB - 50 GB | **Critique** | ES Data | Index et données |
| `kibana-data` | < 100 MB | Moyenne | Kibana | Dashboards, config |
| `cassandra-node1-data` | 5 GB - 500 GB | **Critique** | Cassandra 1 | Données distribuées |
| `cassandra-node2-data` | 5 GB - 500 GB | **Critique** | Cassandra 2 | Données distribuées |
| `grafana-data` | < 500 MB | Moyenne | Grafana | Dashboards, config |
| `prometheus-data` | 1 GB - 10 GB | Faible | Prometheus | Métriques (30j) |

**Total estimé** : 10 GB - 600 GB selon l'utilisation

---

## Configuration des volumes

### Volumes Docker locaux

```yaml
volumes:
  glpi-db-data:
    driver: local
  cassandra-node1-data:
    driver: local
  # etc.
```

**Avantages** :
- ✅ Performance native
- ✅ Gestion automatique par Docker
- ✅ Inspection facile (`docker volume inspect`)

**Localisation** :
```bash
# Sur Linux
/var/lib/docker/volumes/

# Exemple
/var/lib/docker/volumes/infra_glpi-db-data/_data
```

### Options avancées (production)

Pour production, utiliser des drivers spécialisés :

```yaml
volumes:
  cassandra-node1-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/storage/cassandra1

  # Ou avec NFS
  shared-storage:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw
      device: ":/path/to/share"
```

---

## Stratégie de sauvegarde

### Fréquence des sauvegardes

| Type | Volumes | Fréquence | Rétention |
|------|---------|-----------|-----------|
| **Critique** | GLPI, ES, Cassandra | Quotidienne | 30 jours |
| **Moyenne** | Grafana, Kibana | Hebdomadaire | 4 semaines |
| **Faible** | Prometheus, Traefik | Mensuelle | 3 mois |

### Méthode automatique

#### Script de sauvegarde (via Makefile)

```bash
make backup
```

Génère : `backups/dockerwarts_YYYYMMDD_HHMMSS.tar.gz`

**Contenu** :
- Tous les volumes critiques et moyens
- Compressé avec gzip
- Timestamp dans le nom

#### Planification avec cron

```bash
# Éditer crontab
crontab -e

# Ajouter (backup quotidien à 2h du matin)
0 2 * * * cd /path/to/infra && make backup >> /var/log/dockerwarts-backup.log 2>&1

# Cleanup des anciens backups (> 30 jours)
0 3 * * * find /path/to/infra/backups -name "*.tar.gz" -mtime +30 -delete
```

---

## Procédures de sauvegarde

### 1. Sauvegarde complète (tous les volumes)

```bash
cd /path/to/infra
make backup
```

**Résultat** :
```
💾 Creating backup...
Creating backup: backups/dockerwarts_20251013_143000.tar.gz
✓ Backup complete
```

### 2. Sauvegarde individuelle d'un volume

```bash
# Sauvegarde Grafana
docker run --rm \
  -v infra_grafana-data:/data:ro \
  -v $(pwd)/backups:/backup \
  busybox tar czf /backup/grafana-$(date +%Y%m%d).tar.gz /data

# Sauvegarde Cassandra
docker run --rm \
  -v infra_cassandra-node1-data:/data:ro \
  -v $(pwd)/backups:/backup \
  busybox tar czf /backup/cassandra-node1-$(date +%Y%m%d).tar.gz /data
```

### 3. Sauvegarde avec arrêt des services (plus sûr)

```bash
# Arrêter les services
docker-compose stop

# Backup
make backup

# Redémarrer
docker-compose start
```

⚠️ **Downtime** : Cette méthode cause un arrêt temporaire mais garantit la cohérence des données.

### 4. Sauvegarde à chaud (sans arrêt)

Pour Cassandra :
```bash
# Snapshot Cassandra
docker exec dockerwarts-cassandra-node1 nodetool snapshot

# Copier les snapshots
docker cp dockerwarts-cassandra-node1:/var/lib/cassandra/data/snapshots ./backups/
```

Pour Elasticsearch :
```bash
# Créer un snapshot repository
curl -X PUT "localhost:9200/_snapshot/backup_repo" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/backup"
  }
}'

# Créer un snapshot
curl -X PUT "localhost:9200/_snapshot/backup_repo/snapshot_1"
```

---

## Procédures de restauration

### 1. Restauration complète

```bash
cd /path/to/infra

# Arrêter les services
make stop

# Lister les backups disponibles
ls -lh backups/

# Restaurer (interactif)
make restore

# Ou restaurer un fichier spécifique
docker run --rm \
  -v infra_grafana-data:/backup/grafana-data \
  -v infra_prometheus-data:/backup/prometheus-data \
  -v infra_cassandra-node1-data:/backup/cassandra-node1-data \
  -v infra_cassandra-node2-data:/backup/cassandra-node2-data \
  -v infra_elasticsearch-master-data:/backup/elasticsearch-master-data \
  -v infra_elasticsearch-data-data:/backup/elasticsearch-data-data \
  -v infra_glpi-data:/backup/glpi-data \
  -v infra_glpi-db-data:/backup/glpi-db-data \
  -v $(pwd)/backups:/backups \
  busybox tar xzf /backups/dockerwarts_20251013_143000.tar.gz -C /

# Redémarrer
make start
```

### 2. Restauration d'un volume spécifique

```bash
# Arrêter le service concerné
docker-compose stop grafana

# Restaurer
docker run --rm \
  -v infra_grafana-data:/data \
  -v $(pwd)/backups:/backup \
  busybox sh -c "rm -rf /data/* && tar xzf /backup/grafana-20251013.tar.gz -C /"

# Redémarrer
docker-compose start grafana
```

### 3. Restauration en cas de disaster

Scénario : Le serveur est perdu, restauration sur un nouveau serveur.

```bash
# 1. Installer Docker et Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Cloner le repo
git clone <repo-url>
cd infra

# 3. Copier les backups
scp backup-server:/backups/dockerwarts_*.tar.gz backups/

# 4. Restaurer
make restore

# 5. Démarrer
make setup
```

---

## Vérification des sauvegardes

### Tests réguliers (recommandé mensuel)

```bash
# 1. Créer un environnement de test
mkdir test-restore
cd test-restore
cp -r /path/to/infra/backups .

# 2. Restaurer dans un environnement isolé
docker run --rm \
  -v test_volume:/data \
  -v $(pwd)/backups:/backups \
  busybox tar xzf /backups/dockerwarts_latest.tar.gz -C /

# 3. Démarrer un service de test
docker run --rm -v test_volume:/data busybox ls -la /data

# 4. Vérifier l'intégrité
```

### Vérification automatique

Script de vérification :
```bash
#!/bin/bash
# verify-backup.sh

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found"
    exit 1
fi

# Vérifier que c'est un tar.gz valide
if tar tzf "$BACKUP_FILE" > /dev/null 2>&1; then
    echo "✓ Backup file is valid"
    # Afficher le contenu
    tar tzf "$BACKUP_FILE" | head -20
    exit 0
else
    echo "✗ Backup file is corrupted"
    exit 1
fi
```

Usage :
```bash
./verify-backup.sh backups/dockerwarts_20251013_143000.tar.gz
```

---

## Sauvegardes distantes

### Vers stockage cloud (S3, Azure, GCS)

#### Avec rclone

```bash
# Installer rclone
curl https://rclone.org/install.sh | sudo bash

# Configurer (interactif)
rclone config

# Synchroniser les backups
rclone sync backups/ s3:dockerwarts-backups/

# Automatiser avec cron
0 4 * * * rclone sync /path/to/infra/backups/ s3:dockerwarts-backups/
```

#### Avec AWS S3

```bash
# Installer AWS CLI
pip install awscli

# Configurer
aws configure

# Upload
aws s3 sync backups/ s3://dockerwarts-backups/

# Avec lifecycle policy (suppression auto après 90 jours)
aws s3api put-bucket-lifecycle-configuration \
  --bucket dockerwarts-backups \
  --lifecycle-configuration file://lifecycle.json
```

### Vers serveur distant (rsync)

```bash
# Sync vers serveur de backup
rsync -avz --delete backups/ backup-server:/mnt/backups/dockerwarts/

# Automatiser avec cron
0 5 * * * rsync -avz --delete /path/to/infra/backups/ backup-server:/mnt/backups/dockerwarts/
```

---

## Monitoring des sauvegardes

### Script de monitoring

```bash
#!/bin/bash
# check-backup-health.sh

BACKUP_DIR="backups"
MAX_AGE_HOURS=48

# Trouver le backup le plus récent
LATEST_BACKUP=$(ls -t $BACKUP_DIR/*.tar.gz 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "CRITICAL: No backup found"
    exit 2
fi

# Vérifier l'âge
AGE_HOURS=$(( ( $(date +%s) - $(stat -c %Y "$LATEST_BACKUP") ) / 3600 ))

if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
    echo "WARNING: Latest backup is $AGE_HOURS hours old"
    exit 1
else
    echo "OK: Latest backup is $AGE_HOURS hours old"
    exit 0
fi
```

### Intégration avec Prometheus/Grafana

Exporter les métriques de backup :
```bash
# backup-exporter.sh
echo "dockerwarts_backup_age_hours $(( ( $(date +%s) - $(stat -c %Y backups/*.tar.gz | head -1) ) / 3600 ))" > /var/lib/node_exporter/textfile_collector/backup.prom
echo "dockerwarts_backup_count $(ls -1 backups/*.tar.gz | wc -l)" >> /var/lib/node_exporter/textfile_collector/backup.prom
```

---

## Nettoyage et maintenance

### Rotation des backups

```bash
# Conserver seulement les 30 derniers backups
cd backups
ls -t dockerwarts_*.tar.gz | tail -n +31 | xargs rm -f

# Ou avec find (> 30 jours)
find backups/ -name "dockerwarts_*.tar.gz" -mtime +30 -delete
```

### Compression additionnelle

Pour économiser l'espace :
```bash
# Compresser avec xz (meilleur ratio)
xz backups/dockerwarts_*.tar.gz

# Ou recompresser
gunzip backup.tar.gz
xz -9 backup.tar
```

### Nettoyage des volumes inutilisés

```bash
# Lister les volumes orphelins
docker volume ls -qf dangling=true

# Nettoyer
docker volume prune -f
```

---

## Best Practices

### ✅ À faire

1. **Automatiser** : Mettre en place des backups automatiques
2. **Tester** : Vérifier régulièrement les restaurations
3. **Distribuer** : Sauvegardes locales + distantes
4. **Monitorer** : Alertes si backup échoue ou trop vieux
5. **Documenter** : Procédure de restauration claire
6. **Chiffrer** : Chiffrer les backups sensibles

### ❌ À éviter

1. ❌ Sauvegardes uniquement locales
2. ❌ Jamais tester les restaurations
3. ❌ Backups sans rétention définie
4. ❌ Pas de monitoring des backups
5. ❌ Backups sur le même disque que les données
6. ❌ Pas de procédure documentée

---

## Checklist de production

- [ ] Backups automatiques configurés (cron)
- [ ] Backups distants configurés (cloud/serveur)
- [ ] Rétention définie et appliquée
- [ ] Tests de restauration mensuels
- [ ] Monitoring des backups actif
- [ ] Alertes configurées (échec, âge)
- [ ] Documentation à jour
- [ ] Procédure disaster recovery testée
- [ ] Chiffrement activé si données sensibles
- [ ] Équipe formée aux procédures

---

**Données sécurisées ! 💾🔒**
