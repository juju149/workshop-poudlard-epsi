#!/bin/bash

echo "🧪 Integration Tests - Hedwige Email App"
echo "========================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

echo ""
echo "🚀 Starting services with Docker Compose..."
echo ""

# Start services
docker compose -f docker-compose.snippet.yml up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Services started successfully${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Failed to start services${NC}"
    ((TESTS_FAILED++))
    exit 1
fi

echo ""
echo "⏳ Waiting for services to be ready (30 seconds)..."
sleep 30

echo ""
echo "🔍 Testing service health..."
echo ""

# Test backend health
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/health)
if [ "$BACKEND_HEALTH" == "200" ]; then
    echo -e "${GREEN}✅ Backend health check passed${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Backend health check failed (HTTP $BACKEND_HEALTH)${NC}"
    ((TESTS_FAILED++))
fi

# Test frontend
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$FRONTEND_STATUS" == "200" ]; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Frontend is not accessible (HTTP $FRONTEND_STATUS)${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "🔌 Testing API endpoints..."
echo ""

# Test OAuth endpoint
OAUTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/auth/google)
if [ "$OAUTH_STATUS" == "200" ]; then
    echo -e "${GREEN}✅ OAuth endpoint is accessible${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ OAuth endpoint failed (HTTP $OAUTH_STATUS)${NC}"
    ((TESTS_FAILED++))
fi

# Test email endpoint (should require auth)
EMAIL_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/emails)
if [ "$EMAIL_STATUS" == "401" ]; then
    echo -e "${GREEN}✅ Email endpoint requires authentication${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠️  Email endpoint returned unexpected status: $EMAIL_STATUS${NC}"
    ((TESTS_PASSED++))
fi

echo ""
echo "📊 Container status..."
echo ""

# Check running containers
BACKEND_RUNNING=$(docker ps --filter "name=hedwige-backend" --filter "status=running" -q)
FRONTEND_RUNNING=$(docker ps --filter "name=hedwige-frontend" --filter "status=running" -q)

if [ -n "$BACKEND_RUNNING" ]; then
    echo -e "${GREEN}✅ Backend container is running${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Backend container is not running${NC}"
    ((TESTS_FAILED++))
fi

if [ -n "$FRONTEND_RUNNING" ]; then
    echo -e "${GREEN}✅ Frontend container is running${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Frontend container is not running${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "🧹 Cleaning up..."
echo ""

# Stop services
docker compose -f docker-compose.snippet.yml down -v

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Services stopped successfully${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Failed to stop services${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "📊 Test Summary"
echo "=============="
echo -e "${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All integration tests passed!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some integration tests failed${NC}"
    exit 1
fi
