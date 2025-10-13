# ==============================================================================
# DOCKERWARTS - Makefile
# ==============================================================================
# Easy orchestration commands for the infrastructure
# ==============================================================================

.PHONY: help setup start stop restart status logs clean backup restore health

# Default target
help:
	@echo "╔════════════════════════════════════════════════════════════════════╗"
	@echo "║            🧙 DOCKERWARTS Infrastructure Commands 🧙               ║"
	@echo "╚════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make setup          - Initial setup (run once)"
	@echo "  make start          - Start all services"
	@echo "  make stop           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make status         - Show status of all services"
	@echo "  make logs           - Follow logs from all services"
	@echo "  make logs-SERVICE   - Follow logs from specific service"
	@echo "  make health         - Check health of all services"
	@echo "  make clean          - Stop and remove containers (keeps data)"
	@echo "  make clean-all      - Stop, remove containers and volumes (deletes data!)"
	@echo "  make backup         - Backup all volumes"
	@echo "  make restore        - Restore from backup"
	@echo "  make update         - Pull latest images and restart"
	@echo ""
	@echo "Examples:"
	@echo "  make logs-grafana   - Follow Grafana logs"
	@echo "  make logs-cassandra - Follow Cassandra logs"
	@echo ""

# Initial setup
setup:
	@echo "🧙 Running initial setup..."
	@./scripts/setup.sh

# Start services
start:
	@echo "🚀 Starting all services..."
	@docker-compose up -d
	@echo "✓ Services started"
	@make health

# Stop services
stop:
	@echo "🛑 Stopping all services..."
	@docker-compose stop
	@echo "✓ Services stopped"

# Restart services
restart:
	@echo "🔄 Restarting all services..."
	@docker-compose restart
	@echo "✓ Services restarted"

# Show status
status:
	@echo "📊 Service status:"
	@docker-compose ps

# Follow all logs
logs:
	@docker-compose logs -f

# Follow specific service logs
logs-%:
	@echo "📜 Following logs for $*..."
	@docker-compose logs -f $*

# Health check
health:
	@echo "🏥 Checking service health..."
	@echo ""
	@echo "Traefik:         $$(docker inspect --format='{{.State.Status}}' dockerwarts-traefik 2>/dev/null || echo 'not running')"
	@echo "GLPI:            $$(docker inspect --format='{{.State.Status}}' dockerwarts-glpi 2>/dev/null || echo 'not running')"
	@echo "Elasticsearch:   $$(docker inspect --format='{{.State.Status}}' dockerwarts-elasticsearch-master 2>/dev/null || echo 'not running')"
	@echo "Kibana:          $$(docker inspect --format='{{.State.Status}}' dockerwarts-kibana 2>/dev/null || echo 'not running')"
	@echo "Cassandra-1:     $$(docker inspect --format='{{.State.Status}}' dockerwarts-cassandra-node1 2>/dev/null || echo 'not running')"
	@echo "Cassandra-2:     $$(docker inspect --format='{{.State.Status}}' dockerwarts-cassandra-node2 2>/dev/null || echo 'not running')"
	@echo "Grafana:         $$(docker inspect --format='{{.State.Status}}' dockerwarts-grafana 2>/dev/null || echo 'not running')"
	@echo "Prometheus:      $$(docker inspect --format='{{.State.Status}}' dockerwarts-prometheus 2>/dev/null || echo 'not running')"
	@echo ""

# Clean containers
clean:
	@echo "🧹 Stopping and removing containers (keeping data)..."
	@docker-compose down
	@echo "✓ Cleanup complete"

# Clean everything including volumes
clean-all:
	@echo "⚠️  WARNING: This will delete ALL data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "🧹 Stopping and removing containers and volumes..."; \
		docker-compose down -v; \
		echo "✓ Complete cleanup done"; \
	else \
		echo "Cancelled"; \
	fi

# Backup volumes
backup:
	@echo "💾 Creating backup..."
	@mkdir -p backups
	@BACKUP_DATE=$$(date +%Y%m%d_%H%M%S); \
	echo "Creating backup: backups/dockerwarts_$$BACKUP_DATE.tar.gz"; \
	docker run --rm \
		-v dockerwarts_grafana-data:/backup/grafana-data:ro \
		-v dockerwarts_prometheus-data:/backup/prometheus-data:ro \
		-v dockerwarts_cassandra-node1-data:/backup/cassandra-node1-data:ro \
		-v dockerwarts_cassandra-node2-data:/backup/cassandra-node2-data:ro \
		-v dockerwarts_elasticsearch-master-data:/backup/elasticsearch-master-data:ro \
		-v dockerwarts_elasticsearch-data-data:/backup/elasticsearch-data-data:ro \
		-v dockerwarts_glpi-data:/backup/glpi-data:ro \
		-v dockerwarts_glpi-db-data:/backup/glpi-db-data:ro \
		-v $$(pwd)/backups:/backups \
		busybox tar czf /backups/dockerwarts_$$BACKUP_DATE.tar.gz /backup
	@echo "✓ Backup complete"

# Restore from backup
restore:
	@echo "📥 Restoring from backup..."
	@ls -1t backups/*.tar.gz 2>/dev/null || (echo "No backups found" && exit 1)
	@echo "Available backups:"
	@ls -1t backups/*.tar.gz
	@read -p "Enter backup filename: " BACKUP_FILE; \
	if [ -f "$$BACKUP_FILE" ]; then \
		echo "Restoring from $$BACKUP_FILE..."; \
		docker run --rm \
			-v dockerwarts_grafana-data:/backup/grafana-data \
			-v dockerwarts_prometheus-data:/backup/prometheus-data \
			-v dockerwarts_cassandra-node1-data:/backup/cassandra-node1-data \
			-v dockerwarts_cassandra-node2-data:/backup/cassandra-node2-data \
			-v dockerwarts_elasticsearch-master-data:/backup/elasticsearch-master-data \
			-v dockerwarts_elasticsearch-data-data:/backup/elasticsearch-data-data \
			-v dockerwarts_glpi-data:/backup/glpi-data \
			-v dockerwarts_glpi-db-data:/backup/glpi-db-data \
			-v $$(pwd)/backups:/backups \
			busybox tar xzf /backups/$$(basename $$BACKUP_FILE) -C /; \
		echo "✓ Restore complete"; \
	else \
		echo "Backup file not found: $$BACKUP_FILE"; \
		exit 1; \
	fi

# Update images and restart
update:
	@echo "🔄 Updating images..."
	@docker-compose pull
	@echo "🔄 Restarting services..."
	@docker-compose up -d
	@echo "✓ Update complete"

# Development commands
dev-grafana:
	@echo "🔗 Opening Grafana: http://grafana.dockerwarts.local"
	@xdg-open http://grafana.dockerwarts.local 2>/dev/null || open http://grafana.dockerwarts.local 2>/dev/null || echo "Please open http://grafana.dockerwarts.local in your browser"

dev-kibana:
	@echo "🔗 Opening Kibana: http://kibana.dockerwarts.local"
	@xdg-open http://kibana.dockerwarts.local 2>/dev/null || open http://kibana.dockerwarts.local 2>/dev/null || echo "Please open http://kibana.dockerwarts.local in your browser"

dev-glpi:
	@echo "🔗 Opening GLPI: http://glpi.dockerwarts.local"
	@xdg-open http://glpi.dockerwarts.local 2>/dev/null || open http://glpi.dockerwarts.local 2>/dev/null || echo "Please open http://glpi.dockerwarts.local in your browser"

dev-traefik:
	@echo "🔗 Opening Traefik Dashboard: http://localhost:8080"
	@xdg-open http://localhost:8080 2>/dev/null || open http://localhost:8080 2>/dev/null || echo "Please open http://localhost:8080 in your browser"
