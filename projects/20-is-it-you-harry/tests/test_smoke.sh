#!/bin/bash
set -e

echo "🧪 Test Smoke - Défi 20: IS IT YOU HARRY?"
echo "=========================================="

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$PROJECT_DIR/src"
DATA_DIR="$PROJECT_DIR/data"
MODELS_DIR="$PROJECT_DIR/models"
DOCS_DIR="$PROJECT_DIR/docs"
TESTS_DIR="$PROJECT_DIR/tests"

echo -e "\n${YELLOW}📍 Répertoire du projet: $PROJECT_DIR${NC}"

# =============================================================================
# 1. Vérification de la structure du projet
# =============================================================================
echo -e "\n${YELLOW}1️⃣  Vérification de la structure du projet${NC}"

required_dirs=("$SRC_DIR" "$DOCS_DIR" "$TESTS_DIR" "$DATA_DIR" "$MODELS_DIR")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ Dossier trouvé: $(basename $dir)/${NC}"
    else
        echo -e "${RED}❌ Dossier manquant: $(basename $dir)/${NC}"
        exit 1
    fi
done

# =============================================================================
# 2. Vérification des fichiers essentiels
# =============================================================================
echo -e "\n${YELLOW}2️⃣  Vérification des fichiers essentiels${NC}"

required_files=(
    "$PROJECT_DIR/README.md"
    "$PROJECT_DIR/requirements.txt"
    "$PROJECT_DIR/Dockerfile"
    "$PROJECT_DIR/docker-compose.snippet.yml"
    "$PROJECT_DIR/.gitignore"
    "$SRC_DIR/character_recognition.ipynb"
    "$DOCS_DIR/rendu.md"
    "$DOCS_DIR/prompts_used.md"
    "$DOCS_DIR/dataset_guide.md"
    "$TESTS_DIR/test_smoke.sh"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ Fichier trouvé: $(basename $file)${NC}"
    else
        echo -e "${RED}❌ Fichier manquant: $(basename $file)${NC}"
        exit 1
    fi
done

# =============================================================================
# 3. Vérification de Python
# =============================================================================
echo -e "\n${YELLOW}3️⃣  Vérification de Python${NC}"

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 installé${NC}"
    python3 --version
else
    echo -e "${RED}❌ Python3 non trouvé${NC}"
    exit 1
fi

# =============================================================================
# 4. Vérification du notebook Jupyter
# =============================================================================
echo -e "\n${YELLOW}4️⃣  Vérification du notebook Jupyter${NC}"

NOTEBOOK="$SRC_DIR/character_recognition.ipynb"
if [ -f "$NOTEBOOK" ]; then
    echo -e "${GREEN}✅ Notebook trouvé: character_recognition.ipynb${NC}"
    
    # Vérifier que c'est un fichier JSON valide
    if python3 -c "import json; json.load(open('$NOTEBOOK'))" 2>/dev/null; then
        echo -e "${GREEN}✅ Format JSON du notebook valide${NC}"
    else
        echo -e "${RED}❌ Format JSON du notebook invalide${NC}"
        exit 1
    fi
    
    # Vérifier la présence de cellules
    cell_count=$(python3 -c "import json; print(len(json.load(open('$NOTEBOOK'))['cells']))")
    echo -e "${GREEN}✅ Nombre de cellules: $cell_count${NC}"
    
    if [ "$cell_count" -lt 10 ]; then
        echo -e "${YELLOW}⚠️  Peu de cellules détectées (< 10)${NC}"
    fi
else
    echo -e "${RED}❌ Notebook non trouvé${NC}"
    exit 1
fi

# =============================================================================
# 5. Vérification des dépendances Python (si venv activé)
# =============================================================================
echo -e "\n${YELLOW}5️⃣  Vérification des dépendances Python${NC}"

critical_modules=("numpy" "pandas" "tensorflow" "PIL" "matplotlib")
missing_modules=()

for module in "${critical_modules[@]}"; do
    # Convert PIL to pillow for pip check
    check_module=$module
    if [ "$module" == "PIL" ]; then
        check_module="pillow"
    fi
    
    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✅ Module $module disponible${NC}"
    else
        echo -e "${YELLOW}⚠️  Module $module non installé${NC}"
        missing_modules+=("$check_module")
    fi
done

if [ ${#missing_modules[@]} -gt 0 ]; then
    echo -e "\n${YELLOW}💡 Pour installer les modules manquants:${NC}"
    echo -e "${YELLOW}   pip install -r requirements.txt${NC}"
fi

# =============================================================================
# 6. Vérification de la structure du dataset
# =============================================================================
echo -e "\n${YELLOW}6️⃣  Vérification de la structure du dataset${NC}"

dataset_dirs=("$DATA_DIR/train" "$DATA_DIR/val" "$DATA_DIR/test")
for dir in "${dataset_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ Répertoire dataset trouvé: $(basename $dir)/${NC}"
    else
        echo -e "${YELLOW}⚠️  Répertoire dataset manquant: $(basename $dir)/ (sera créé par le notebook)${NC}"
        mkdir -p "$dir"
    fi
done

# Compter les images si présentes
for split in train val test; do
    split_dir="$DATA_DIR/$split"
    if [ -d "$split_dir" ]; then
        image_count=$(find "$split_dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) 2>/dev/null | wc -l)
        if [ "$image_count" -gt 0 ]; then
            echo -e "${GREEN}   ℹ️  Images dans $split/: $image_count${NC}"
        else
            echo -e "${YELLOW}   ℹ️  Aucune image dans $split/ (dataset de démo sera créé par le notebook)${NC}"
        fi
    fi
done

# =============================================================================
# 7. Vérification de Docker (optionnel)
# =============================================================================
echo -e "\n${YELLOW}7️⃣  Vérification Docker (optionnel)${NC}"

if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker installé${NC}"
    docker --version
    
    if docker compose version &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ Docker Compose disponible${NC}"
        docker compose version
    elif command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose disponible (standalone)${NC}"
        docker-compose --version
    else
        echo -e "${YELLOW}⚠️  Docker Compose non trouvé${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Docker non installé (optionnel pour développement local)${NC}"
fi

# =============================================================================
# 8. Vérification des fichiers Docker
# =============================================================================
echo -e "\n${YELLOW}8️⃣  Vérification des fichiers Docker${NC}"

if [ -f "$PROJECT_DIR/Dockerfile" ]; then
    echo -e "${GREEN}✅ Dockerfile présent${NC}"
    
    # Vérifier la syntaxe de base
    if grep -q "FROM" "$PROJECT_DIR/Dockerfile" && grep -q "WORKDIR" "$PROJECT_DIR/Dockerfile"; then
        echo -e "${GREEN}✅ Dockerfile contient FROM et WORKDIR${NC}"
    else
        echo -e "${YELLOW}⚠️  Dockerfile potentiellement incomplet${NC}"
    fi
fi

if [ -f "$PROJECT_DIR/docker-compose.snippet.yml" ]; then
    echo -e "${GREEN}✅ docker-compose.snippet.yml présent${NC}"
fi

# =============================================================================
# 9. Vérification de la documentation
# =============================================================================
echo -e "\n${YELLOW}9️⃣  Vérification de la documentation${NC}"

docs=(
    "$PROJECT_DIR/README.md:README principal"
    "$DOCS_DIR/rendu.md:Document de rendu"
    "$DOCS_DIR/prompts_used.md:Prompts IA"
    "$DOCS_DIR/dataset_guide.md:Guide dataset"
)

for doc_info in "${docs[@]}"; do
    IFS=':' read -r doc_path doc_name <<< "$doc_info"
    if [ -f "$doc_path" ]; then
        word_count=$(wc -w < "$doc_path")
        echo -e "${GREEN}✅ $doc_name ($word_count mots)${NC}"
    fi
done

# =============================================================================
# 10. Vérification des permissions
# =============================================================================
echo -e "\n${YELLOW}🔟  Vérification des permissions${NC}"

if [ -x "$TESTS_DIR/test_smoke.sh" ]; then
    echo -e "${GREEN}✅ test_smoke.sh est exécutable${NC}"
else
    echo -e "${YELLOW}⚠️  test_smoke.sh n'est pas exécutable${NC}"
    echo -e "${YELLOW}   Exécuter: chmod +x $TESTS_DIR/test_smoke.sh${NC}"
fi

# =============================================================================
# Résumé final
# =============================================================================
echo -e "\n${GREEN}=========================================="
echo "✅ Tous les tests sont passés avec succès!"
echo -e "==========================================${NC}"

echo -e "\n${YELLOW}📚 Prochaines étapes:${NC}"
echo ""
echo "1️⃣  Installer les dépendances (si pas déjà fait):"
echo "   python -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo ""
echo "2️⃣  Lancer Jupyter:"
echo "   jupyter notebook src/character_recognition.ipynb"
echo ""
echo "3️⃣  Ou utiliser Docker:"
echo "   docker compose -f docker-compose.snippet.yml up -d"
echo "   Accéder à http://localhost:8888"
echo ""
echo "4️⃣  Exécuter le notebook de bout en bout pour:"
echo "   - Créer le dataset de démonstration"
echo "   - Entraîner le modèle CNN"
echo "   - Évaluer les performances"
echo "   - Générer les visualisations"
echo ""
echo -e "${GREEN}🧙‍♂️  Que la magie du Deep Learning soit avec vous!${NC}"
echo ""

exit 0
