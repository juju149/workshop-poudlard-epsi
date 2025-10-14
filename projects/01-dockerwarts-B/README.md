# Infrastructure Big Data dockerisée

## Architecture
Ce projet propose une infrastructure Big Data complète, déployable via Docker Compose, incluant :
- GLPI (ticketing)
- ElasticSearch (cluster 2 nœuds)
- Grafana (monitoring)
- Cassandra (datalake)
- Traefik (pare-feu/proxy HTTPS)

Chaque service est isolé dans son conteneur, connecté au réseau `bigdata_net`, avec volumes persistants et configurations dédiées.

## Déploiement
1. Copier et adapter le fichier `.env` selon vos besoins.
2. Lancer l’infrastructure :
   ```sh
   docker compose up -d
   ```
3. Accéder aux services :
   - GLPI : http://localhost:${GLPI_PORT}
   - Grafana : http://localhost:${GRAFANA_PORT}
   - ElasticSearch : http://localhost:${ELASTICSEARCH_PORT1}
   - Cassandra : port ${CASSANDRA_PORT}
   - Traefik : http(s)://localhost

## Sauvegarde & PRA
- Les scripts de sauvegarde/restauration sont dans `backups/`.
- Pour sauvegarder :
  ```sh
  ./backups/backup.sh
  ```
- Pour restaurer :
  ```sh
  ./backups/restore.sh
  ```

## Monitoring
- Grafana centralise les métriques des services.
- Connectez-vous avec le mot de passe admin défini dans `.env`.

## Sécurité
- Traefik gère l’accès externe et les certificats HTTPS (Let's Encrypt).
- Les mots de passe et ports sont centralisés dans `.env`.

## Documentation
- Le plan de reprise après sinistre est détaillé dans `docs/PRA.md`.
- Le schéma d’architecture est dans `docs/architecture-diagram.png`.

