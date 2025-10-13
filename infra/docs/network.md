# 🌐 Configuration Réseau - DOCKERWARTS

## Vue d'ensemble des réseaux

DOCKERWARTS utilise deux réseaux Docker bridge pour séparer les services frontend des services backend.

---

## Réseaux Docker

### Frontend Network

```yaml
networks:
  frontend:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/24
```

**Caractéristiques** :
- **Subnet** : 172.20.0.0/24 (254 adresses disponibles)
- **Gateway** : 172.20.0.1 (automatique)
- **Driver** : bridge (réseau interne Docker)

**Services connectés** :
- Traefik (reverse proxy)
- Grafana (UI monitoring)
- Kibana (UI logs)
- GLPI (UI ticketing)

**Isolation** :
- Accessible depuis l'hôte via ports mappés
- Pas d'accès direct aux services backend

---

### Backend Network

```yaml
networks:
  backend:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.21.0.0/24
```

**Caractéristiques** :
- **Subnet** : 172.21.0.0/24 (254 adresses disponibles)
- **Gateway** : 172.21.0.1 (automatique)
- **Driver** : bridge (réseau interne Docker)

**Services connectés** :
- Prometheus (collecte métriques)
- Elasticsearch (master & data nodes)
- Cassandra (node1 & node2)
- MariaDB (base GLPI)
- Node Exporter (métriques système)
- cAdvisor (métriques containers)
- Traefik (pour accéder aux backends)

**Isolation** :
- Non accessible directement depuis l'extérieur
- Communication inter-services uniquement

---

## Matrice de communication

| Source | Destination | Port | Protocole | Réseau |
|--------|-------------|------|-----------|---------|
| **Internet** | Traefik | 80, 443 | HTTP/HTTPS | Host → Frontend |
| Traefik | Grafana | 3000 | HTTP | Frontend |
| Traefik | Kibana | 5601 | HTTP | Frontend → Backend |
| Traefik | GLPI | 80 | HTTP | Frontend |
| Grafana | Prometheus | 9090 | HTTP | Frontend → Backend |
| Grafana | Elasticsearch | 9200 | HTTP | Frontend → Backend |
| GLPI | MariaDB | 3306 | MySQL | Frontend → Backend |
| Kibana | Elasticsearch | 9200 | HTTP | Backend |
| Prometheus | Traefik | 8080 | HTTP | Backend → Frontend |
| Prometheus | Elasticsearch | 9200 | HTTP | Backend |
| Prometheus | Node Exporter | 9100 | HTTP | Backend |
| Prometheus | cAdvisor | 8080 | HTTP | Backend |
| Elasticsearch Master | Elasticsearch Data | 9300 | TCP | Backend |
| Cassandra Node1 | Cassandra Node2 | 7000 | TCP | Backend |

---

## Configuration des services

### Services multi-réseaux

Certains services sont connectés aux deux réseaux pour servir de pont :

#### Traefik
```yaml
networks:
  - frontend  # Pour recevoir le trafic
  - backend   # Pour accéder aux services backend
```

#### Grafana
```yaml
networks:
  - frontend  # Pour être accessible via Traefik
  - backend   # Pour requêter Prometheus et Elasticsearch
```

#### GLPI
```yaml
networks:
  - frontend  # Pour être accessible via Traefik
  - backend   # Pour accéder à MariaDB
```

#### Kibana
```yaml
networks:
  - frontend  # Pour être accessible via Traefik
  - backend   # Pour requêter Elasticsearch
```

---

## Port Mapping

### Ports exposés sur l'hôte

| Service | Port Hôte | Port Container | Usage |
|---------|-----------|----------------|-------|
| Traefik | 80 | 80 | HTTP |
| Traefik | 443 | 443 | HTTPS (si SSL activé) |
| Traefik | 8080 | 8080 | Dashboard |

### Ports internes (non exposés)

| Service | Port | Protocole | Usage |
|---------|------|-----------|-------|
| Grafana | 3000 | HTTP | Web UI |
| Kibana | 5601 | HTTP | Web UI |
| GLPI | 80 | HTTP | Web UI |
| Prometheus | 9090 | HTTP | API + UI |
| Elasticsearch | 9200 | HTTP | REST API |
| Elasticsearch | 9300 | TCP | Inter-node |
| MariaDB | 3306 | MySQL | Database |
| Cassandra | 9042 | CQL | Native protocol |
| Cassandra | 7000 | TCP | Inter-node |
| Node Exporter | 9100 | HTTP | Métriques |
| cAdvisor | 8080 | HTTP | Métriques |

---

## Routage Traefik

### Configuration Host-based routing

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.SERVICE.rule=Host(`SERVICE.dockerwarts.local`)"
  - "traefik.http.routers.SERVICE.entrypoints=web"
  - "traefik.http.services.SERVICE.loadbalancer.server.port=PORT"
```

### Routes configurées

| Host | Service | Port Backend |
|------|---------|--------------|
| `grafana.dockerwarts.local` | Grafana | 3000 |
| `kibana.dockerwarts.local` | Kibana | 5601 |
| `glpi.dockerwarts.local` | GLPI | 80 |

---

## DNS et /etc/hosts

### Configuration locale

Pour accéder aux services en local, ajouter à `/etc/hosts` :

```bash
127.0.0.1 grafana.dockerwarts.local
127.0.0.1 kibana.dockerwarts.local
127.0.0.1 glpi.dockerwarts.local
```

Ou en une ligne :
```bash
127.0.0.1 grafana.dockerwarts.local kibana.dockerwarts.local glpi.dockerwarts.local
```

### Configuration production

En production, utiliser un vrai DNS :
- Enregistrements A pointant vers le serveur
- Wildcard DNS : `*.dockerwarts.company.com`

---

## Sécurité réseau

### Isolation

1. **Frontend network** : Seuls les services UI sont accessibles
2. **Backend network** : Services de données isolés
3. **Pas de port direct** : Tout passe par Traefik

### Recommandations

#### Pour développement (actuel)
✅ Configuration actuelle suffisante

#### Pour production
- [ ] Activer SSL/TLS (Let's Encrypt)
- [ ] Configurer rate limiting dans Traefik
- [ ] Ajouter authentification sur Traefik dashboard
- [ ] Utiliser Docker Swarm overlay networks pour multi-host
- [ ] Implémenter network policies si Kubernetes

---

## Troubleshooting réseau

### Vérifier la connectivité inter-services

```bash
# Depuis un container vers un autre
docker exec dockerwarts-grafana ping prometheus

# Tester une connexion HTTP
docker exec dockerwarts-grafana curl http://prometheus:9090/-/healthy
```

### Inspecter les réseaux

```bash
# Lister les réseaux
docker network ls | grep dockerwarts

# Inspecter un réseau
docker network inspect infra_frontend
docker network inspect infra_backend

# Voir les containers sur un réseau
docker network inspect infra_backend | jq '.[0].Containers'
```

### Vérifier les routes Traefik

```bash
# Dashboard Traefik
open http://localhost:8080

# API Traefik
curl http://localhost:8080/api/http/routers | jq
```

### Tester la résolution DNS interne

```bash
# Depuis un container
docker exec dockerwarts-grafana nslookup prometheus
docker exec dockerwarts-grafana getent hosts prometheus
```

---

## Diagramme de flux réseau

```
                    Internet
                       │
                       ▼
           ┌───────────────────────┐
           │   Host Machine NIC    │
           │    (eth0/wlan0)       │
           └───────────┬───────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        │    Docker Bridge (docker0)  │
        │                             │
        └──┬─────────────────────┬────┘
           │                     │
  ┌────────▼─────────┐  ┌───────▼──────────┐
  │ Frontend Network │  │ Backend Network  │
  │  172.20.0.0/24   │  │  172.21.0.0/24   │
  └──────────────────┘  └──────────────────┘
           │                     │
     ┌─────┼─────┐         ┌────┼─────┐
     │     │     │         │    │     │
  Traefik  │  Kibana    Prometheus  │ 
  Grafana  │  GLPI         ES     Cassandra
           │                      MariaDB
     (services exposés)      (services internes)
```

---

## Performance réseau

### MTU (Maximum Transmission Unit)

Docker utilise par défaut MTU=1500 pour les réseaux bridge.

Pour optimiser :
```yaml
networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.driver.mtu: 1500
```

### Latence attendue

Entre containers sur le même réseau :
- **Latence** : < 1ms (localhost)
- **Bande passante** : limitée par CPU/RAM, pas par le réseau

---

## Évolution

### Multi-host (Docker Swarm)

```yaml
networks:
  frontend:
    driver: overlay
    attachable: true
  backend:
    driver: overlay
    attachable: true
```

### Kubernetes

Équivalent en Kubernetes :
- NetworkPolicies pour isolation
- Services pour discovery interne
- Ingress pour routage externe

---

**Documentation réseau complète ! 🌐**
