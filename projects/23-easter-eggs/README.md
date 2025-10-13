# 🎭 EASTER EGGS - Section Chaos

## 🎯 Objectif

Réalisation d'un test de stress sur des modèles d'IA à travers des prompts contradictoires et des requêtes limites, dans le cadre de la recherche en sécurité IA. Ce projet documente scientifiquement les comportements inattendus des modèles de langage face à des situations ambiguës ou paradoxales.

## ⚠️ Avertissement de Sécurité

Ce projet est réalisé dans un cadre éthique et de recherche :
- ✅ Tests effectués sur des APIs publiques avec rate limiting
- ✅ Aucun dommage aux systèmes
- ✅ Documentation scientifique complète
- ✅ Respect des conditions d'utilisation des services
- ❌ Pas de fork bomb ou code malveillant
- ❌ Pas d'attaque réelle de systèmes

## 🧩 Architecture

Le projet comprend :

```
23-easter-eggs/
├── src/
│   ├── ai_stress_test.py      # Script principal de test
│   ├── paradox_generator.py   # Générateur de prompts paradoxaux
│   └── report_generator.py    # Générateur de rapport scientifique
├── docs/
│   ├── rendu.md               # Document de rendu final
│   ├── prompts_used.md        # Historique des prompts IA
│   ├── scientific_report.md   # Rapport scientifique des résultats
│   └── methodology.md         # Méthodologie de test
├── tests/
│   └── test_smoke.sh          # Tests de validation
├── results/                   # Résultats des tests
└── requirements.txt           # Dépendances Python
```

## ⚙️ Technologies utilisées

- **Python 3.11+** : Langage principal
- **Requests** : Appels API
- **Rich** : Affichage formaté des résultats
- **JSON** : Stockage des résultats
- **Docker** : Conteneurisation

## 🚀 Lancement rapide

### Avec Docker (recommandé)

```bash
# Construire l'image
docker compose -f docker-compose.snippet.yml build

# Lancer le test de stress IA
docker compose -f docker-compose.snippet.yml up
```

### Sans Docker

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le test
python src/ai_stress_test.py

# Générer le rapport
python src/report_generator.py
```

## 🧪 Tests

```bash
# Test de validation de la structure
bash tests/test_smoke.sh
```

## 📊 Exemples de Paradoxes Testés

1. **Paradoxe du Menteur** : "Cette phrase est fausse"
2. **Paradoxe du Barbier** : "Le barbier rase tous ceux qui ne se rasent pas eux-mêmes"
3. **Paradoxe du Crocodile** : Dilemmes logiques contradictoires
4. **Prompts Auto-référentiels** : Instructions qui se contredisent
5. **Boucles Infinies Conceptuelles** : Raisonnements circulaires

## 📈 Résultats Attendus

Le projet génère :
- ✅ Rapport scientifique détaillé des comportements observés
- ✅ Classification des types de réponses (cohérente, incohérente, refus, etc.)
- ✅ Analyse statistique des patterns de réponse
- ✅ Documentation des cas limites découverts
- ✅ Recommandations pour améliorer la robustesse des IA

## 🎓 Contexte Pédagogique

Ce projet s'inscrit dans le cadre de l'étude de :
- La sécurité des systèmes d'IA
- Les limitations des modèles de langage
- La robustesse face aux entrées adversariales
- L'éthique en recherche IA

## 📚 Documentation

- [Rendu Final](docs/rendu.md) - Document de rendu complet
- [Rapport Scientifique](docs/scientific_report.md) - Résultats détaillés
- [Méthodologie](docs/methodology.md) - Approche de recherche
- [Prompts Utilisés](docs/prompts_used.md) - Historique des prompts IA

## 👥 Crédits

Projet réalisé dans le cadre du Workshop Poudlard à l'EPSI.

**Copilots impliqués** :
- 🧙 Project Lead (supervision)
- 🔬 Research Copilot (méthodologie scientifique)
- 📊 Documentation Copilot (rapports)

## 📅 Planning

- **Deadline** : 17/10/2025
- **Story Points** : Variable selon l'expérimentation
- **Statut** : En cours

## 🔗 Références

- AI Safety Research
- Prompt Engineering Best Practices
- Adversarial Testing Methodologies
