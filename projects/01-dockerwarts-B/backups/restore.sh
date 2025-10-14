#!/bin/bash
# Script de restauration des volumes Docker
# Usage : ./restore.sh <volume> <archive>

set -e

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <volume> <archive>"
  exit 1
fi

VOLUME="$1"
ARCHIVE="$2"

docker run --rm -v $VOLUME:/volume -v "$(pwd)":/backup busybox sh -c "cd /volume && tar xzf /backup/$ARCHIVE"

echo "Restauration du volume $VOLUME terminée."
# Variables d'environnement centralisées pour l'infrastructure Big Data

# GLPI
GLPI_PORT=8080
GLPI_DB_USER=glpi
GLPI_DB_PASSWORD=glpi_pass
GLPI_DB_NAME=glpidb
GLPI_DB_ROOT_PASSWORD=glpi_root_pass

# ElasticSearch
ELASTIC_PASSWORD=elastic_pass
ELASTICSEARCH_PORT1=9201
ELASTICSEARCH_PORT2=9202

# Grafana
GRAFANA_PORT=3000
GRAFANA_ADMIN_PASSWORD=grafana_pass

# Cassandra
CASSANDRA_PORT=9042
CASSANDRA_PASSWORD=cassandra_pass

# Traefik
TRAEFIK_HTTP_PORT=80
TRAEFIK_HTTPS_PORT=443
LETSENCRYPT_EMAIL=admin@example.com

