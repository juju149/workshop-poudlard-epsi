#!/bin/bash
# Test de validation pour le Défi 8 - Chambre des Secrets

set -e  # Arrêter en cas d'erreur

echo "=============================================="
echo "🧪 TEST DE VALIDATION - DÉFI 8"
echo "🏰 OÙ EST LA CHAMBRE DES SECRETS ?"
echo "=============================================="
echo ""

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compteur de tests
TESTS_PASSED=0
TESTS_FAILED=0

# Fonction pour tester une condition
test_step() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "🔍 Test: $test_name ... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Fonction pour afficher un message d'information
info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Déterminer le chemin du projet
if [ -f "build_hogwarts_plan.py" ]; then
    PROJECT_DIR="$(pwd)"
    ROOT_DIR="$(cd ../.. && pwd)"
elif [ -f "projects/8-chambre-des-secrets/build_hogwarts_plan.py" ]; then
    ROOT_DIR="$(pwd)"
    PROJECT_DIR="$ROOT_DIR/projects/8-chambre-des-secrets"
else
    echo -e "${RED}❌ Erreur: Impossible de trouver le répertoire du projet${NC}"
    echo "Exécutez ce script depuis:"
    echo "  - Le répertoire du projet: projects/8-chambre-des-secrets/tests/"
    echo "  - La racine du workshop: workshop-poudlard-epsi/"
    exit 1
fi

echo "📂 Répertoire du projet: $PROJECT_DIR"
echo "📂 Répertoire racine: $ROOT_DIR"
echo ""

# ============================================
# TESTS DE PRÉREQUIS
# ============================================

echo "📋 Étape 1: Vérification des prérequis"
echo "----------------------------------------"

test_step "Fichier plan.json existe" "[ -f '$ROOT_DIR/context/plans/plan.json' ]"

test_step "Script Python existe" "[ -f '$PROJECT_DIR/build_hogwarts_plan.py' ]"

test_step "Blender est installé" "command -v blender"

if command -v blender > /dev/null 2>&1; then
    BLENDER_VERSION=$(blender --version 2>&1 | head -n 1 || echo "Version inconnue")
    info "Version de Blender: $BLENDER_VERSION"
fi

test_step "Python est accessible" "command -v python3"

echo ""

# ============================================
# TESTS DE STRUCTURE
# ============================================

echo "📋 Étape 2: Vérification de la structure"
echo "----------------------------------------"

test_step "Dossier docs/ existe" "[ -d '$PROJECT_DIR/docs' ]"

test_step "Dossier tests/ existe" "[ -d '$PROJECT_DIR/tests' ]"

test_step "Dossier renders/ existe" "[ -d '$PROJECT_DIR/renders' ]"

test_step "README.md existe" "[ -f '$PROJECT_DIR/README.md' ]"

test_step "docs/rendu.md existe" "[ -f '$PROJECT_DIR/docs/rendu.md' ]"

echo ""

# ============================================
# TESTS DE VALIDATION DU JSON
# ============================================

echo "📋 Étape 3: Validation du fichier JSON"
echo "----------------------------------------"

PLAN_JSON="$ROOT_DIR/context/plans/plan.json"

if [ -f "$PLAN_JSON" ]; then
    test_step "JSON est valide" "python3 -m json.tool '$PLAN_JSON'"
    
    # Vérifier la présence de clés essentielles
    test_step "JSON contient 'levels'" "grep -q '\"levels\"' '$PLAN_JSON'"
    
    test_step "JSON contient 'parametric_generation'" "grep -q '\"parametric_generation\"' '$PLAN_JSON'"
    
    # Compter le nombre de niveaux
    LEVELS_COUNT=$(python3 -c "import json; data=json.load(open('$PLAN_JSON')); print(len(data['levels']))" 2>/dev/null || echo "0")
    info "Nombre de niveaux détectés: $LEVELS_COUNT"
fi

echo ""

# ============================================
# TESTS D'EXÉCUTION (OPTIONNEL)
# ============================================

echo "📋 Étape 4: Test d'exécution du script (optionnel)"
echo "----------------------------------------"

info "Ce test peut prendre plusieurs minutes..."
info "Pour ignorer ce test, appuyez sur Ctrl+C"
echo ""

# Demander confirmation
read -p "Voulez-vous exécuter le script Blender ? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Lancement du script Blender..."
    
    cd "$ROOT_DIR"
    
    if blender --background --python "$PROJECT_DIR/build_hogwarts_plan.py" 2>&1 | tee /tmp/blender_output.log; then
        echo -e "${GREEN}✅ Script exécuté avec succès${NC}"
        ((TESTS_PASSED++))
        
        # Vérifier les fichiers générés
        test_step "Fichier .blend généré" "[ -f '$PROJECT_DIR/hogwarts_plan.blend' ]"
        
        test_step "Vidéo MP4 générée" "[ -f '$PROJECT_DIR/renders/plan_turntable.mp4' ]"
        
        if [ -f "$PROJECT_DIR/renders/plan_turntable.mp4" ]; then
            VIDEO_SIZE=$(du -h "$PROJECT_DIR/renders/plan_turntable.mp4" | cut -f1)
            info "Taille de la vidéo: $VIDEO_SIZE"
        fi
        
        if [ -f "$PROJECT_DIR/hogwarts_plan.blend" ]; then
            BLEND_SIZE=$(du -h "$PROJECT_DIR/hogwarts_plan.blend" | cut -f1)
            info "Taille du fichier .blend: $BLEND_SIZE"
        fi
    else
        echo -e "${RED}❌ Échec de l'exécution du script${NC}"
        ((TESTS_FAILED++))
        
        info "Voir les logs dans: /tmp/blender_output.log"
        echo ""
        echo "Dernières lignes du log:"
        tail -n 20 /tmp/blender_output.log
    fi
else
    info "Test d'exécution ignoré"
fi

echo ""

# ============================================
# TESTS DE VALIDATION DU SCRIPT PYTHON
# ============================================

echo "📋 Étape 5: Validation syntaxique du script Python"
echo "----------------------------------------"

test_step "Script Python est syntaxiquement correct" "python3 -m py_compile '$PROJECT_DIR/build_hogwarts_plan.py'"

# Vérifier les imports critiques
test_step "Script importe bpy" "grep -q 'import bpy' '$PROJECT_DIR/build_hogwarts_plan.py'"

test_step "Script importe json" "grep -q 'import json' '$PROJECT_DIR/build_hogwarts_plan.py'"

# Vérifier les fonctions principales
test_step "Fonction load_plan_data() existe" "grep -q 'def load_plan_data' '$PROJECT_DIR/build_hogwarts_plan.py'"

test_step "Fonction create_chamber_of_secrets() existe" "grep -q 'def create_chamber_of_secrets' '$PROJECT_DIR/build_hogwarts_plan.py'"

test_step "Fonction create_animated_camera() existe" "grep -q 'def create_animated_camera' '$PROJECT_DIR/build_hogwarts_plan.py'"

echo ""

# ============================================
# RÉSUMÉ
# ============================================

echo "=============================================="
echo "📊 RÉSUMÉ DES TESTS"
echo "=============================================="
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
SUCCESS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo "Total de tests: $TOTAL_TESTS"
echo -e "Tests réussis: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests échoués: ${RED}$TESTS_FAILED${NC}"
echo "Taux de réussite: $SUCCESS_RATE%"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 TOUS LES TESTS SONT PASSÉS !${NC}"
    echo "✅ Le projet est prêt à être livré"
    exit 0
else
    echo -e "${RED}⚠️  CERTAINS TESTS ONT ÉCHOUÉ${NC}"
    echo "❌ Veuillez corriger les erreurs avant de livrer"
    exit 1
fi
