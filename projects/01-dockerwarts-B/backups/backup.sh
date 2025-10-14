#!/bin/bash
# Script de sauvegarde des volumes Docker
# Usage : ./backup.sh

set -e

VOLUMES=(glpi_data elasticsearch_data1 elasticsearch_data2 grafana_data cassandra_data)
BACKUP_DIR="$(dirname "$0")/archives"
mkdir -p "$BACKUP_DIR"

for VOLUME in "${VOLUMES[@]}"; do
  echo "Sauvegarde du volume $VOLUME..."
  docker run --rm -v $VOLUME:/volume -v "$BACKUP_DIR":/backup busybox tar czf /backup/${VOLUME}_$(date +%F).tar.gz -C /volume .
done

echo "Sauvegarde terminée dans $BACKUP_DIR"

