# Plan de Reprise d’Activité (PRA)

## Sauvegarde
- **Fréquence** : quotidienne recommandée (cron ou conteneur dédié)
- **Méthode** : scripts `backups/backup.sh` et `backups/restore.sh` pour exporter/importer les volumes Docker
- **Stockage** : externaliser les sauvegardes (cloud, NAS, etc.)

## Reprise après sinistre
1. Identifier le service impacté (GLPI, ElasticSearch, Grafana, Cassandra, Traefik)
2. Restaurer le volume correspondant via `restore.sh`
3. Redémarrer le service :
   ```sh
   docker compose restart <service>
   ```
4. Vérifier l’intégrité et la connectivité

## Redéploiement complet
- En cas de perte totale :
  1. Recréer l’infrastructure :
     ```sh
     docker compose up -d
     ```
  2. Restaurer tous les volumes avec `restore.sh`
  3. Vérifier les accès et la cohérence des données

## Points de vigilance
- Tester régulièrement la restauration
- Sécuriser les accès aux sauvegardes
- Documenter toute modification de configuration

