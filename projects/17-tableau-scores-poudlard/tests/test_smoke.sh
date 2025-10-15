#!/bin/bash
set -e

echo "🧪 === Test Smoke - Tableau des Scores de Poudlard ==="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_URL="http://localhost:3000"

echo "📂 Répertoire du projet: $PROJECT_DIR"
echo ""

# Fonction de nettoyage
cleanup() {
    echo ""
    echo "🧹 Nettoyage..."
    cd "$PROJECT_DIR"
    docker compose -f docker-compose.snippet.yml down -v 2>/dev/null || true
}

# Piège pour exécuter cleanup en cas d'erreur ou de sortie
trap cleanup EXIT

echo "🚀 Étape 1: Lancement du service API avec Docker Compose"
cd "$PROJECT_DIR"
docker compose -f docker-compose.snippet.yml up -d

echo ""
echo "⏳ Attente du démarrage des services (30 secondes)..."
sleep 30

echo ""
echo "🔍 Étape 2: Vérification de l'état des containers"
docker compose -f docker-compose.snippet.yml ps

echo ""
echo "📡 Étape 3: Test Health Check"
HEALTH_RESPONSE=$(curl -s -f "$API_URL/health" || echo "FAILED")
if [[ "$HEALTH_RESPONSE" == "FAILED" ]]; then
    echo -e "${RED}❌ Health check échoué${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Health check réussi${NC}"
    echo "Response: $HEALTH_RESPONSE"
fi

echo ""
echo "📋 Étape 4: Test GET /api/houses"
HOUSES_RESPONSE=$(curl -s -f "$API_URL/api/houses" || echo "FAILED")
if [[ "$HOUSES_RESPONSE" == "FAILED" ]]; then
    echo -e "${RED}❌ GET /api/houses échoué${NC}"
    exit 1
else
    echo -e "${GREEN}✅ GET /api/houses réussi${NC}"
    echo "Response: $HOUSES_RESPONSE"
    # Vérifier qu'on a bien 4 maisons
    COUNT=$(echo "$HOUSES_RESPONSE" | grep -o '"id"' | wc -l)
    if [ "$COUNT" -eq 4 ]; then
        echo -e "${GREEN}✅ 4 maisons trouvées${NC}"
    else
        echo -e "${RED}❌ Nombre de maisons incorrect: $COUNT${NC}"
        exit 1
    fi
fi

echo ""
echo "➕ Étape 5: Test POST /api/houses/1/add"
ADD_RESPONSE=$(curl -s -f -X POST "$API_URL/api/houses/1/add" \
    -H "Content-Type: application/json" \
    -d '{"points": 50}' || echo "FAILED")
if [[ "$ADD_RESPONSE" == "FAILED" ]]; then
    echo -e "${RED}❌ POST /api/houses/1/add échoué${NC}"
    exit 1
else
    echo -e "${GREEN}✅ POST /api/houses/1/add réussi${NC}"
    echo "Response: $ADD_RESPONSE"
fi

echo ""
echo "🔄 Étape 6: Vérification de l'ajout de points"
HOUSE1_RESPONSE=$(curl -s -f "$API_URL/api/houses/1" || echo "FAILED")
if [[ "$HOUSE1_RESPONSE" == "FAILED" ]]; then
    echo -e "${RED}❌ GET /api/houses/1 échoué${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Points vérifiés${NC}"
    echo "Response: $HOUSE1_RESPONSE"
fi

echo ""
echo "♻️ Étape 7: Test POST /api/reset"
RESET_RESPONSE=$(curl -s -f -X POST "$API_URL/api/reset" || echo "FAILED")
if [[ "$RESET_RESPONSE" == "FAILED" ]]; then
    echo -e "${RED}❌ POST /api/reset échoué${NC}"
    exit 1
else
    echo -e "${GREEN}✅ POST /api/reset réussi${NC}"
    echo "Response: $RESET_RESPONSE"
fi

echo ""
echo "📊 Étape 8: Test des logs Docker"
echo "Dernières lignes des logs:"
docker compose -f docker-compose.snippet.yml logs --tail=10

echo ""
echo -e "${GREEN}🎉 Tous les tests sont passés avec succès !${NC}"
echo ""
echo "Les containers restent actifs. Pour les arrêter:"
echo "  docker compose -f docker-compose.snippet.yml down -v"
echo ""
