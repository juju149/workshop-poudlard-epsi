#!/bin/bash
# Test de validation basique pour le projet Professeur Dumbledore

set -e

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Emojis
CHECK="✅"
CROSS="❌"
ROCKET="🚀"
GEAR="⚙️"
TEST="🧪"

echo -e "${BLUE}${ROCKET} Test Smoke - Professeur Dumbledore${NC}"
echo "================================================"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

ERRORS=0

# Fonction pour afficher le succès
success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

# Fonction pour afficher l'erreur
error() {
    echo -e "${RED}${CROSS} $1${NC}"
    ERRORS=$((ERRORS + 1))
}

# Fonction pour afficher l'info
info() {
    echo -e "${YELLOW}${GEAR} $1${NC}"
}

echo ""
info "Vérification de l'environnement..."

# Test 1: Python installé
echo ""
info "Test 1: Vérification de Python"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    success "Python trouvé: $PYTHON_VERSION"
else
    error "Python 3 n'est pas installé"
fi

# Test 2: pip installé
echo ""
info "Test 2: Vérification de pip"
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    success "pip trouvé: $PIP_VERSION"
else
    error "pip n'est pas installé"
fi

# Test 3: Fichiers requis présents
echo ""
info "Test 3: Vérification des fichiers requis"
required_files=(
    "README.md"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.snippet.yml"
    "src/spell_recognition.ipynb"
    "src/inference.py"
    "docs/rendu.md"
    "docs/prompts_used.md"
    "docs/dataset_methodology.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        success "Fichier présent: $file"
    else
        error "Fichier manquant: $file"
    fi
done

# Test 4: Dossiers requis présents
echo ""
info "Test 4: Vérification des dossiers"
required_dirs=(
    "src"
    "data"
    "data/raw"
    "data/processed"
    "models"
    "docs"
    "tests"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        success "Dossier présent: $dir"
    else
        error "Dossier manquant: $dir"
    fi
done

# Test 5: Installation des dépendances (optionnel)
echo ""
info "Test 5: Validation du requirements.txt"
if [ -f "requirements.txt" ]; then
    # Compte le nombre de dépendances
    DEPS_COUNT=$(grep -v '^#' requirements.txt | grep -v '^$' | wc -l)
    if [ "$DEPS_COUNT" -gt 0 ]; then
        success "requirements.txt contient $DEPS_COUNT dépendances"
    else
        error "requirements.txt est vide"
    fi
else
    error "requirements.txt introuvable"
fi

# Test 6: Validation du Dockerfile
echo ""
info "Test 6: Validation du Dockerfile"
if [ -f "Dockerfile" ]; then
    if grep -q "FROM python" Dockerfile; then
        success "Dockerfile utilise une image Python"
    else
        error "Dockerfile ne semble pas utiliser Python"
    fi
    
    if grep -q "requirements.txt" Dockerfile; then
        success "Dockerfile installe les dépendances"
    else
        error "Dockerfile n'installe pas requirements.txt"
    fi
else
    error "Dockerfile introuvable"
fi

# Test 7: Validation du docker-compose
echo ""
info "Test 7: Validation du docker-compose.snippet.yml"
if [ -f "docker-compose.snippet.yml" ]; then
    if grep -q "8888" docker-compose.snippet.yml; then
        success "docker-compose expose le port Jupyter (8888)"
    else
        error "Port Jupyter non exposé dans docker-compose"
    fi
else
    error "docker-compose.snippet.yml introuvable"
fi

# Test 8: Test d'import Python (si environnement disponible)
echo ""
info "Test 8: Test des imports Python (optionnel)"
if command -v python3 &> /dev/null; then
    # Crée un script de test temporaire
    cat > /tmp/test_imports.py << 'EOF'
import sys
try:
    import numpy
    print("✓ numpy")
except ImportError:
    print("✗ numpy")
    sys.exit(1)

try:
    import pandas
    print("✓ pandas")
except ImportError:
    print("✗ pandas")

try:
    import sklearn
    print("✓ scikit-learn")
except ImportError:
    print("✗ scikit-learn")

# Les autres imports sont optionnels pour ce test rapide
EOF
    
    if python3 /tmp/test_imports.py 2>/dev/null; then
        success "Bibliothèques de base disponibles"
    else
        info "Certaines dépendances ne sont pas installées (normal si env vierge)"
    fi
    rm -f /tmp/test_imports.py
fi

# Test 9: Validation du notebook
echo ""
info "Test 9: Validation du notebook Jupyter"
if [ -f "src/spell_recognition.ipynb" ]; then
    if grep -q "Wav2Vec2" src/spell_recognition.ipynb; then
        success "Notebook contient la référence au modèle Wav2Vec2"
    else
        error "Modèle Wav2Vec2 non trouvé dans le notebook"
    fi
    
    if grep -q "expelliarmus" src/spell_recognition.ipynb; then
        success "Notebook contient les formules magiques"
    else
        error "Formules magiques non trouvées dans le notebook"
    fi
else
    error "Notebook introuvable"
fi

# Test 10: Validation du script d'inférence
echo ""
info "Test 10: Validation du script d'inférence"
if [ -f "src/inference.py" ]; then
    if grep -q "SpellRecognizer" src/inference.py; then
        success "Script contient la classe SpellRecognizer"
    else
        error "Classe SpellRecognizer non trouvée"
    fi
    
    if head -1 src/inference.py | grep -q "#!/usr/bin/env python"; then
        success "Script a le shebang Python"
    else
        info "Ajout du shebang recommandé"
    fi
    
    # Vérifie si le script est exécutable
    if [ -x "src/inference.py" ]; then
        success "Script d'inférence est exécutable"
    else
        info "Rendre le script exécutable: chmod +x src/inference.py"
    fi
else
    error "Script d'inférence introuvable"
fi

# Résumé
echo ""
echo "================================================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}${CHECK} Tous les tests sont passés!${NC}"
    echo -e "${BLUE}${ROCKET} Le projet est prêt pour l'entraînement${NC}"
    exit 0
else
    echo -e "${RED}${CROSS} $ERRORS erreur(s) détectée(s)${NC}"
    echo -e "${YELLOW}Veuillez corriger les erreurs avant de continuer${NC}"
    exit 1
fi
