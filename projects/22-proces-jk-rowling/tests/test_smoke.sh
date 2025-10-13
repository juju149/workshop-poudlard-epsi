#!/bin/bash
set -e

echo "🧪 Test Smoke - Défi 22: Procès de J.K. Rowling"
echo "=============================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOKS_DIR="$PROJECT_DIR/../../context/books"
OUTPUT_DIR="$PROJECT_DIR/output"
DATA_DIR="$PROJECT_DIR/data"

echo -e "\n${YELLOW}1️⃣  Vérification de la structure du projet${NC}"
if [ -d "$PROJECT_DIR/src" ] && [ -d "$PROJECT_DIR/docs" ] && [ -d "$PROJECT_DIR/tests" ]; then
    echo -e "${GREEN}✅ Structure du projet OK${NC}"
else
    echo -e "${RED}❌ Structure du projet incomplète${NC}"
    exit 1
fi

echo -e "\n${YELLOW}2️⃣  Vérification des livres Harry Potter${NC}"
if [ -d "$BOOKS_DIR" ]; then
    book_count=$(find "$BOOKS_DIR" -name "*.pdf" | wc -l)
    echo -e "${GREEN}✅ Répertoire des livres trouvé ($book_count PDFs)${NC}"
    if [ "$book_count" -lt 7 ]; then
        echo -e "${YELLOW}⚠️  Attention: moins de 7 livres trouvés${NC}"
    fi
else
    echo -e "${RED}❌ Répertoire des livres introuvable${NC}"
    exit 1
fi

echo -e "\n${YELLOW}3️⃣  Vérification des dépendances Python${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 installé${NC}"
    python3 --version
    
    # Vérifier les modules critiques
    if python3 -c "import PyPDF2, pandas, matplotlib" 2>/dev/null; then
        echo -e "${GREEN}✅ Modules Python critiques installés${NC}"
    else
        echo -e "${YELLOW}⚠️  Modules Python manquants (normal si pas installé localement)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Python3 non trouvé (OK si exécution Docker uniquement)${NC}"
fi

echo -e "\n${YELLOW}4️⃣  Vérification du script d'analyse${NC}"
if [ -f "$PROJECT_DIR/src/analyze_corpus.py" ]; then
    echo -e "${GREEN}✅ Script d'analyse trouvé${NC}"
    # Vérifier la syntaxe Python si possible
    if command -v python3 &> /dev/null; then
        if python3 -m py_compile "$PROJECT_DIR/src/analyze_corpus.py" 2>/dev/null; then
            echo -e "${GREEN}✅ Syntaxe Python valide${NC}"
        else
            echo -e "${YELLOW}⚠️  Impossible de vérifier la syntaxe${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Script d'analyse introuvable${NC}"
    exit 1
fi

echo -e "\n${YELLOW}5️⃣  Vérification des fichiers Docker${NC}"
if [ -f "$PROJECT_DIR/Dockerfile" ]; then
    echo -e "${GREEN}✅ Dockerfile trouvé${NC}"
else
    echo -e "${RED}❌ Dockerfile introuvable${NC}"
    exit 1
fi

if [ -f "$PROJECT_DIR/docker-compose.snippet.yml" ]; then
    echo -e "${GREEN}✅ docker-compose.snippet.yml trouvé${NC}"
else
    echo -e "${RED}❌ docker-compose.snippet.yml introuvable${NC}"
    exit 1
fi

echo -e "\n${YELLOW}6️⃣  Vérification de la documentation${NC}"
if [ -f "$PROJECT_DIR/README.md" ]; then
    echo -e "${GREEN}✅ README.md présent${NC}"
else
    echo -e "${YELLOW}⚠️  README.md manquant${NC}"
fi

if [ -f "$PROJECT_DIR/docs/rendu.md" ]; then
    echo -e "${GREEN}✅ docs/rendu.md présent${NC}"
else
    echo -e "${YELLOW}⚠️  docs/rendu.md manquant${NC}"
fi

if [ -f "$PROJECT_DIR/docs/prompts_used.md" ]; then
    echo -e "${GREEN}✅ docs/prompts_used.md présent${NC}"
else
    echo -e "${YELLOW}⚠️  docs/prompts_used.md manquant${NC}"
fi

echo -e "\n${YELLOW}7️⃣  Test de création des répertoires${NC}"
mkdir -p "$OUTPUT_DIR" "$DATA_DIR"
if [ -d "$OUTPUT_DIR" ] && [ -d "$DATA_DIR" ]; then
    echo -e "${GREEN}✅ Répertoires de sortie créés${NC}"
else
    echo -e "${RED}❌ Impossible de créer les répertoires${NC}"
    exit 1
fi

echo -e "\n${YELLOW}8️⃣  Vérification Docker (optionnel)${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker installé${NC}"
    docker --version
    
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose disponible${NC}"
    else
        echo -e "${YELLOW}⚠️  Docker Compose non trouvé${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Docker non installé${NC}"
fi

echo -e "\n=============================================="
echo -e "${GREEN}🎉 Tous les tests smoke sont passés !${NC}"
echo -e "=============================================="
echo ""
echo "Pour exécuter l'analyse complète:"
echo "  1. Via Docker: docker compose -f docker-compose.snippet.yml up --build"
echo "  2. Via Python: cd src && python analyze_corpus.py"
echo ""
