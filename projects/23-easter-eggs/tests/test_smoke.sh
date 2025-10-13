#!/bin/bash

# 🧪 Test Smoke - Easter Eggs Challenge
# Vérifie la structure et les dépendances du projet

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${BLUE}🎭 Easter Eggs - Smoke Test${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}\n"

# Function to check file existence
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ PASS:${NC} $2"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL:${NC} $2"
        ((FAILED++))
        return 1
    fi
}

# Function to check directory existence
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ PASS:${NC} $2"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL:${NC} $2"
        ((FAILED++))
        return 1
    fi
}

# Function to check content
check_content() {
    if grep -q "$2" "$1"; then
        echo -e "${GREEN}✅ PASS:${NC} $3"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL:${NC} $3"
        ((FAILED++))
        return 1
    fi
}

echo -e "${YELLOW}📁 Checking project structure...${NC}\n"

# Check directories
check_dir "src" "Directory 'src' exists"
check_dir "docs" "Directory 'docs' exists"
check_dir "tests" "Directory 'tests' exists"

echo ""

# Check essential files
echo -e "${YELLOW}📄 Checking essential files...${NC}\n"
check_file "README.md" "README.md exists"
check_file "Dockerfile" "Dockerfile exists"
check_file "docker-compose.snippet.yml" "docker-compose.snippet.yml exists"
check_file "requirements.txt" "requirements.txt exists"
check_file "src/ai_stress_test.py" "Main script exists"

echo ""

# Check documentation
echo -e "${YELLOW}📚 Checking documentation...${NC}\n"
check_file "docs/rendu.md" "docs/rendu.md exists"
check_file "docs/prompts_used.md" "docs/prompts_used.md exists"

echo ""

# Check content in key files
echo -e "${YELLOW}🔍 Checking file content...${NC}\n"
check_content "README.md" "EASTER EGGS" "README contains project name"
check_content "README.md" "Avertissement" "README contains safety warning"
check_content "src/ai_stress_test.py" "AIStressTest" "Main script contains AIStressTest class"
check_content "requirements.txt" "rich" "requirements.txt contains rich library"

echo ""

# Check Python syntax if Python is available
if command -v python3 &> /dev/null; then
    echo -e "${YELLOW}🐍 Checking Python syntax...${NC}\n"
    if python3 -m py_compile src/ai_stress_test.py 2>/dev/null; then
        echo -e "${GREEN}✅ PASS:${NC} Python syntax is valid"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL:${NC} Python syntax error"
        ((FAILED++))
    fi
    echo ""
fi

# Check Docker files
echo -e "${YELLOW}🐳 Checking Docker configuration...${NC}\n"
check_content "Dockerfile" "python:3.11" "Dockerfile uses Python 3.11"
check_content "docker-compose.snippet.yml" "easter-eggs" "Docker Compose has service definition"

echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${BLUE}📊 Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"
echo -e "${BLUE}Total:  $((PASSED + FAILED))${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    exit 1
fi
