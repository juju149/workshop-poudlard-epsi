#!/bin/bash

echo "🧪 Test Smoke - Wizard Quiz App"
echo "================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test
test_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 exists${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ $1 missing${NC}"
        ((TESTS_FAILED++))
    fi
}

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
test_dir "src/wizard_quiz"
test_dir "src/wizard_quiz/lib"
test_dir "src/wizard_quiz/lib/models"
test_dir "src/wizard_quiz/lib/screens"
test_dir "src/wizard_quiz/lib/utils"
test_dir "docs"
test_dir "tests"

echo ""
echo "📄 Testing essential files..."
echo ""

# Test essential files
test_file "README.md"
test_file "Dockerfile"
test_file "docker-compose.snippet.yml"
test_file "src/wizard_quiz/pubspec.yaml"
test_file "src/wizard_quiz/lib/main.dart"

echo ""
echo "🎯 Testing Flutter source files..."
echo ""

# Test Flutter files
test_file "src/wizard_quiz/lib/models/question.dart"
test_file "src/wizard_quiz/lib/models/wizard_type.dart"
test_file "src/wizard_quiz/lib/screens/welcome_screen.dart"
test_file "src/wizard_quiz/lib/screens/quiz_screen.dart"
test_file "src/wizard_quiz/lib/screens/result_screen.dart"
test_file "src/wizard_quiz/lib/utils/quiz_data.dart"

echo ""
echo "📚 Testing documentation..."
echo ""

# Test documentation
test_file "docs/rendu.md"
test_file "docs/gamification.md"
test_file "docs/prompts_used.md"

echo ""
echo "🔍 Checking content..."
echo ""

# Check for 20 questions in quiz_data.dart
if [ -f "src/wizard_quiz/lib/utils/quiz_data.dart" ]; then
    QUESTION_COUNT=$(grep -c "Question(" src/wizard_quiz/lib/utils/quiz_data.dart)
    if [ "$QUESTION_COUNT" -ge 20 ]; then
        echo -e "${GREEN}✅ Found $QUESTION_COUNT questions (minimum 20 required)${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ Only $QUESTION_COUNT questions found (minimum 20 required)${NC}"
        ((TESTS_FAILED++))
    fi
fi

# Check for 6 wizard types
if [ -f "src/wizard_quiz/lib/models/wizard_type.dart" ]; then
    WIZARD_COUNT=$(grep -c "static final" src/wizard_quiz/lib/models/wizard_type.dart)
    if [ "$WIZARD_COUNT" -ge 6 ]; then
        echo -e "${GREEN}✅ Found $WIZARD_COUNT wizard types (minimum 4 required, 6 provided)${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠️  Only $WIZARD_COUNT wizard types found (minimum 4 required)${NC}"
        ((TESTS_FAILED++))
    fi
fi

echo ""
echo "================================"
echo "📊 Test Results"
echo "================================"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    exit 1
fi
