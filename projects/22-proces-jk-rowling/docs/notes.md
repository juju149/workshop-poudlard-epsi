# 📝 Notes de Développement - Défi 22

## 🎯 Objectif du Projet

Créer un pipeline d'analyse textuelle complet pour extraire et visualiser des statistiques amusantes et révélatrices des 7 livres Harry Potter.

---

## ✅ Réalisations

### Infrastructure
- ✅ Structure de projet conforme à `agents/AGENTS.md`
- ✅ Pipeline Python entièrement fonctionnel
- ✅ Dockerisation complète avec docker-compose
- ✅ Scripts de tests automatisés
- ✅ Documentation exhaustive

### Analyses Implémentées
1. ✅ Cicatrice de Harry (78 occurrences détectées)
2. ⚠️ Hermione dit "Mais" (0 détection - patterns à améliorer)
3. ✅ Interventions de Dumbledore (26 détections)
4. ✅ Comparaison dialogues Harry/Ron/Hermione (523 prises de parole)
5. ✅ Rogue mystérieux (12 occurrences)
6. ✅ Actes répréhensibles (3,400 détections!)
7. ✅ Statistiques par livre
8. ✅ Normalisation par 100 pages

### Visualisations
- ✅ 5 graphiques haute résolution (300 DPI)
- ✅ Export CSV et JSON
- ✅ Résultats détaillés dans docs/resultats.md

---

## 🔧 Défis Techniques Rencontrés

### 1. Extraction PDF
**Problème**: Certaines pages des PDFs ont des problèmes d'encodage.

**Solution**: Gestion d'erreurs robuste avec `try/except` au niveau page.

```python
try:
    text += page.extract_text() + "\n"
except Exception:
    continue  # Skip problematic pages
```

### 2. Patterns Regex pour Hermione
**Problème**: Aucune détection de "Hermione dit Mais".

**Hypothèses**:
- Traduction française utilise d'autres formulations
- Guillemets français (« ») vs anglais (" ")
- Contexte plus complexe que prévu

**Patterns testés**:
```python
r'Hermione.*?[«"][^»"]{0,200}\bMais\b[^»"]{0,200}[»"]'
r'[«"].*?\bMais\b.*?[»"].*?dit Hermione'
r'— Mais.*?(?:dit|déclara|répondit|s\'écria) Hermione'
```

**Solutions potentielles**:
- Parser XML/structure du PDF plus finement
- Utiliser spaCy pour analyse syntaxique
- Extraction des dialogues avec NLP
- Analyser les chapitres pour identifier les sections de dialogue

### 3. Chemins de Fichiers
**Problème initial**: Paths relatifs incorrects depuis différents contextes d'exécution.

**Solution**: Utiliser `Path(__file__).parent` pour paths relatifs au script.

```python
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BOOKS_DIR = PROJECT_ROOT / "../../context/books"
```

### 4. Emojis dans Matplotlib
**Avertissement**: Certains emojis ne sont pas supportés par la font DejaVu Sans.

**Impact**: Minimal - les emojis sont affichés comme [?] dans les titres.

**Solution possible**: Installer font-awesome ou utiliser unicode characters.

---

## 📊 Résultats Intéressants

### Surprise #1: Ron > Hermione en dialogues!
Ron parle presque 2× plus qu'Hermione (125 vs 72 prises de parole), contredisant l'image populaire.

### Surprise #2: Escalade criminelle
Les actes répréhensibles passent de 203 (livre 1) à 893 (livre 7), soit une augmentation de 340%!

### Surprise #3: Cicatrice explosive au livre 7
44 occurrences au livre 7, soit 56% du total - l'horcruxe vivant se manifeste.

### Surprise #4: Dumbledore le plus manipulateur au livre 6
14 interventions arbitraires, préparant Harry pour la mission finale.

---

## 🔄 Améliorations Possibles

### Court Terme (Rapide à implémenter)

1. **Améliorer patterns Hermione**
   ```python
   # Tester patterns plus simples
   r'Hermione[^.]*\bMais\b'
   r'— Mais.*?Hermione'
   ```

2. **Ajouter analyse de sentiment**
   - Classifier actes par gravité (léger/moyen/grave)
   - Sentiment de Rogue (positif/négatif/neutre)

3. **Export HTML interactif**
   - Dashboard avec Plotly
   - Graphiques zoomables
   - Filtres dynamiques

4. **Tests unitaires**
   - pytest pour chaque fonction d'analyse
   - Tests de régression
   - Coverage > 80%

### Moyen Terme (Nécessite développement)

1. **NLP avec spaCy**
   ```python
   import spacy
   nlp = spacy.load("fr_core_news_sm")
   doc = nlp(text)
   # Extraction dialogues avec analyse syntaxique
   ```

2. **Base de données**
   - PostgreSQL pour historique
   - API REST pour requêtes
   - Cache des résultats

3. **ML pour classification contextuelle**
   - Entraîner modèle pour classifier actes
   - Détection automatique de patterns
   - Fine-tuning BERT sur corpus HP

### Long Terme (Projet complet)

1. **Comparaison multi-séries**
   - Le Seigneur des Anneaux
   - Percy Jackson
   - Hunger Games
   - Benchmarking narratif

2. **Analyse approfondie**
   - Évolution du vocabulaire
   - Complexité syntaxique
   - Arcs narratifs
   - Développement des personnages

3. **Interface Web complète**
   - Frontend React
   - Backend FastAPI
   - Authentification
   - Export personnalisé

---

## 🐛 Bugs Connus

### 1. Hermione "Mais" - Aucune détection
**Statut**: ⚠️ Non résolu  
**Impact**: Métrique incomplète  
**Workaround**: Analyse manuelle suggérée  
**Fix**: Améliorer patterns ou utiliser NLP

### 2. Emojis non affichés dans les graphiques
**Statut**: ⚠️ Mineur  
**Impact**: Esthétique seulement  
**Workaround**: Texte reste lisible  
**Fix**: Installer font avec support emoji

### 3. Temps d'exécution long
**Statut**: ℹ️ Normal  
**Impact**: ~5-10 minutes pour 7 livres  
**Workaround**: Patience ou cache  
**Fix**: Parallélisation avec multiprocessing

---

## 📚 Ressources Utilisées

### Documentation
- [PyPDF2 Docs](https://pypdf2.readthedocs.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [Regex101](https://regex101.com/) - Test patterns

### Outils IA
- GitHub Copilot - Génération de code
- GPT-4 - Suggestions de patterns
- ChatGPT - Documentation

---

## 🎓 Leçons Apprises

### 1. Analyse Textuelle
- Les patterns regex sont puissants mais limités
- Le contexte est crucial pour l'exactitude
- La traduction change beaucoup les patterns
- NLP sera nécessaire pour une analyse précise

### 2. Visualisation de Données
- Seaborn facilite grandement les graphiques
- 300 DPI est essentiel pour qualité professionnelle
- Normalisation (par page) est cruciale pour comparaison
- Couleurs thématiques améliorent la compréhension

### 3. Gestion de Projet
- Structure standardisée (AGENTS.md) accélère le développement
- Documentation continue évite la perte d'information
- Tests automatisés donnent confiance
- Docker assure la reproductibilité

### 4. Python
- pathlib est meilleur que os.path
- pandas est incontournable pour data science
- try/except robuste est essentiel pour PDFs
- Type hints améliorent la maintenabilité

---

## 🔐 Sécurité & Confidentialité

- ✅ Pas de données sensibles dans le code
- ✅ Pas de credentials hardcodés
- ✅ PDFs sources non inclus dans le repo (droit d'auteur)
- ✅ Résultats générés exclus du git (.gitignore)

---

## 📝 Changelog

### v1.0.0 (2025-10-13)
- ✅ Implémentation complète du pipeline
- ✅ 6/7 analyses fonctionnelles
- ✅ 5 visualisations haute qualité
- ✅ Documentation exhaustive
- ✅ Tests smoke validés
- ⚠️ Pattern Hermione à améliorer

---

## 💡 Idées Futures

### Analyses Supplémentaires
- Occurrences de sorts magiques
- Évolution du vocabulaire d'Harry
- Présence de Voldemort (mentions)
- Apparitions de Hedwige
- Scènes de Quidditch
- Moments de romance
- Références à l'amour maternel

### Visualisations Supplémentaires
- Timeline interactive des événements
- Réseau de relations entre personnages
- Wordcloud par livre
- Sentiment analysis par chapitre
- Carte thermique émotionnelle

### Features Techniques
- CLI avec arguments
- Mode batch pour plusieurs corpus
- Export PDF du rapport
- Email automatique des résultats
- Webhook pour notifications

---

## 👥 Contributeurs

**Lead Developer**: Data Copilot  
**Support**: AI Copilot  
**Reviewer**: GitHub Copilot  
**Framework**: agents/AGENTS.md

---

## 📧 Contact

Pour questions, suggestions ou bugs:
- Créer une issue sur le repository
- Consulter `docs/rendu.md` pour détails techniques
- Vérifier `docs/resultats.md` pour les résultats

---

## 📄 Licence

Projet éducatif - Workshop EPSI 2025-2026  
Corpus Harry Potter © J.K. Rowling / Gallimard  
Code source © EPSI Workshop - Usage éducatif uniquement

---

> ⚡ *"After all this time? Always."* - Severus Snape

**Dernière mise à jour**: 13 octobre 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
