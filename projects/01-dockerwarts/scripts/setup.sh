#!/bin/bash

# ==============================================================================
# DOCKERWARTS - Infrastructure Setup Script
# ==============================================================================
# This script sets up the complete Docker infrastructure for the big data platform
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "=============================================================================="
    echo "$1"
    echo "=============================================================================="
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    print_header "Checking Docker installation"
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is installed: $(docker --version)"
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is installed"
}

# Check system requirements
check_requirements() {
    print_header "Checking system requirements"
    
    # Check available memory
    total_mem=$(free -g | awk '/^Mem:/{print $2}')
    if [ "$total_mem" -lt 8 ]; then
        print_warning "System has less than 8GB RAM. Some services may not work properly."
    else
        print_success "System has $total_mem GB RAM"
    fi
    
    # Check available disk space
    available_disk=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ "$available_disk" -lt 20 ]; then
        print_warning "Less than 20GB disk space available. Consider freeing up space."
    else
        print_success "Available disk space: ${available_disk}GB"
    fi
}

# Create environment file
setup_env() {
    print_header "Setting up environment variables"
    
    if [ ! -f .env ]; then
        cp .env.example .env
        print_success ".env file created from .env.example"
        print_warning "Please edit .env file and update the passwords before starting services"
        read -p "Do you want to edit .env now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} .env
        fi
    else
        print_info ".env file already exists"
    fi
}

# Set system parameters for Elasticsearch
setup_system_params() {
    print_header "Configuring system parameters for Elasticsearch"
    
    # Check if running on Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Set vm.max_map_count
        current_value=$(sysctl -n vm.max_map_count 2>/dev/null || echo 0)
        if [ "$current_value" -lt 262144 ]; then
            print_info "Setting vm.max_map_count to 262144 (required for Elasticsearch)"
            if [ "$EUID" -eq 0 ]; then
                sysctl -w vm.max_map_count=262144
                echo "vm.max_map_count=262144" >> /etc/sysctl.conf
                print_success "vm.max_map_count set to 262144"
            else
                print_warning "Run with sudo to set vm.max_map_count permanently"
                print_info "Or run manually: sudo sysctl -w vm.max_map_count=262144"
            fi
        else
            print_success "vm.max_map_count is already set correctly"
        fi
    else
        print_info "Not on Linux, skipping system parameter configuration"
        print_info "For Docker Desktop, increase memory allocation to at least 4GB in settings"
    fi
}

# Pull Docker images
pull_images() {
    print_header "Pulling Docker images (this may take a while)"
    
    docker-compose pull 2>/dev/null || docker compose pull
    
    print_success "Docker images pulled successfully"
}

# Start services
start_services() {
    print_header "Starting Docker services"
    
    print_info "Starting services in detached mode..."
    docker-compose up -d 2>/dev/null || docker compose up -d
    
    print_success "Services started successfully"
}

# Wait for services to be healthy
wait_for_services() {
    print_header "Waiting for services to be ready"
    
    print_info "This may take a few minutes..."
    
    services=(
        "dockerwarts-traefik"
        "dockerwarts-grafana"
        "dockerwarts-prometheus"
        "dockerwarts-elasticsearch-master"
        "dockerwarts-glpi"
        "dockerwarts-cassandra-node1"
    )
    
    for service in "${services[@]}"; do
        echo -n "Waiting for $service... "
        timeout=300
        elapsed=0
        while [ $elapsed -lt $timeout ]; do
            if docker inspect "$service" &> /dev/null; then
                health=$(docker inspect --format='{{.State.Health.Status}}' "$service" 2>/dev/null || echo "unknown")
                if [ "$health" = "healthy" ] || [ "$health" = "unknown" ]; then
                    running=$(docker inspect --format='{{.State.Running}}' "$service")
                    if [ "$running" = "true" ]; then
                        print_success "Ready"
                        break
                    fi
                fi
            fi
            sleep 5
            elapsed=$((elapsed + 5))
        done
        
        if [ $elapsed -ge $timeout ]; then
            print_warning "Timeout waiting for $service"
        fi
    done
}

# Display access information
display_info() {
    print_header "🎉 DOCKERWARTS Infrastructure is ready!"
    
    echo ""
    echo "Access URLs (add these to /etc/hosts pointing to 127.0.0.1):"
    echo ""
    echo -e "${GREEN}Traefik Dashboard:${NC}   http://localhost:8080"
    echo -e "${GREEN}Grafana:${NC}              http://grafana.dockerwarts.local (admin/changeme_grafana_password)"
    echo -e "${GREEN}GLPI:${NC}                 http://glpi.dockerwarts.local"
    echo -e "${GREEN}Kibana:${NC}               http://kibana.dockerwarts.local"
    echo ""
    echo "Direct access (without Traefik):"
    echo -e "${GREEN}Elasticsearch:${NC}        http://localhost:9200"
    echo -e "${GREEN}Cassandra:${NC}            localhost:9042"
    echo ""
    echo "To add hosts entries, run:"
    echo -e "${YELLOW}echo '127.0.0.1 grafana.dockerwarts.local glpi.dockerwarts.local kibana.dockerwarts.local' | sudo tee -a /etc/hosts${NC}"
    echo ""
    echo "View logs: docker-compose logs -f [service-name]"
    echo "Stop all:  docker-compose down"
    echo "Stop and remove volumes: docker-compose down -v"
    echo ""
}

# Main execution
main() {
    print_header "🧙 DOCKERWARTS Infrastructure Setup 🧙"
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    check_docker
    check_requirements
    setup_env
    setup_system_params
    pull_images
    start_services
    wait_for_services
    display_info
    
    print_success "Setup complete! Enjoy your Big Data infrastructure! 🚀"
}

# Run main function
main "$@"
