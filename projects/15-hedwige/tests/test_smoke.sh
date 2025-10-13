#!/bin/bash

echo "🧪 Test Smoke - Hedwige Email App"
echo "=================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test file existence
test_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ $1 missing${NC}"
        ((TESTS_FAILED++))
    fi
}

# Function to test directory existence
test_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ Directory $1 exists${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ Directory $1 missing${NC}"
        ((TESTS_FAILED++))
    fi
}

echo ""
echo "📁 Testing project structure..."
echo ""

# Test directories
test_dir "src/backend"
test_dir "src/frontend"
test_dir "src/backend/routes"
test_dir "src/backend/tests"
test_dir "src/frontend/src"
test_dir "src/frontend/src/components"
test_dir "src/frontend/src/pages"
test_dir "src/frontend/src/styles"
test_dir "src/frontend/tests"
test_dir "docs"
test_dir "tests"

echo ""
echo "📄 Testing essential files..."
echo ""

# Test root files
test_file "README.md"
test_file "docker-compose.snippet.yml"

# Test backend files
test_file "src/backend/package.json"
test_file "src/backend/server.js"
test_file "src/backend/.env.example"
test_file "src/backend/Dockerfile"
test_file "src/backend/routes/auth.js"
test_file "src/backend/routes/email.js"
test_file "src/backend/tests/api.test.js"
test_file "src/backend/jest.config.js"

# Test frontend files
test_file "src/frontend/package.json"
test_file "src/frontend/index.html"
test_file "src/frontend/vite.config.js"
test_file "src/frontend/Dockerfile"
test_file "src/frontend/nginx.conf"
test_file "src/frontend/src/main.jsx"
test_file "src/frontend/src/App.jsx"

echo ""
echo "🎯 Testing React components..."
echo ""

# Test React components
test_file "src/frontend/src/pages/LoginPage.jsx"
test_file "src/frontend/src/pages/MailboxPage.jsx"
test_file "src/frontend/src/pages/ComposePage.jsx"
test_file "src/frontend/src/components/EmailList.jsx"
test_file "src/frontend/src/components/EmailDetail.jsx"

echo ""
echo "🎨 Testing CSS files..."
echo ""

# Test CSS files
test_file "src/frontend/src/styles/index.css"
test_file "src/frontend/src/styles/App.css"
test_file "src/frontend/src/styles/LoginPage.css"
test_file "src/frontend/src/styles/MailboxPage.css"
test_file "src/frontend/src/styles/EmailList.css"
test_file "src/frontend/src/styles/EmailDetail.css"
test_file "src/frontend/src/styles/ComposePage.css"

echo ""
echo "🧪 Testing test files..."
echo ""

# Test files
test_file "src/frontend/tests/App.test.jsx"
test_file "src/frontend/tests/LoginPage.test.jsx"
test_file "src/frontend/tests/EmailList.test.jsx"

echo ""
echo "📚 Testing documentation..."
echo ""

# Test documentation
test_file "docs/rendu.md"
test_file "docs/api.md"
test_file "docs/test_scenarios.md"
test_file "docs/prompts_used.md"

echo ""
echo "🔍 Checking content..."
echo ""

# Check for OAuth in backend
if grep -q "google" src/backend/routes/auth.js; then
    echo -e "${GREEN}✅ OAuth2 implementation found${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ OAuth2 implementation not found${NC}"
    ((TESTS_FAILED++))
fi

# Check for email routes
if grep -q "gmail" src/backend/routes/email.js; then
    echo -e "${GREEN}✅ Gmail API integration found${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ Gmail API integration not found${NC}"
    ((TESTS_FAILED++))
fi

# Check for React router
if grep -q "react-router-dom" src/frontend/package.json; then
    echo -e "${GREEN}✅ React Router dependency found${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ React Router dependency not found${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "📊 Test Summary"
echo "=============="
echo -e "${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
