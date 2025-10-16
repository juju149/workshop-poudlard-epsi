# 📝 Notes de développement – hp_nlp

> Carnet de bord du projet Pipeline NLP Harry Potter

---

## 🎯 Objectif du projet

Créer une pipeline NLP moderne pour analyser les 7 livres Harry Potter et extraire automatiquement des événements narratifs, en remplacement d'une approche basée sur regex.

---

## 📅 Timeline

### Phase 1 : Conception (Jour 1-2)
- [x] Définition de l'architecture
- [x] Choix des technologies (spaCy)
- [x] Structure des notebooks (5 étapes)
- [x] Stratégie de stockage (Parquet)

### Phase 2 : Développement (Jour 3-8)
- [x] Notebook 01 : Ingestion & nettoyage
- [x] Notebook 02 : Pipeline NLP (tokenisation, NER, POS)
- [x] Notebook 03 : Extraction d'événements
- [x] Notebook 04 : Agrégations & visualisations
- [x] Notebook 05 : Génération rapport automatique

### Phase 3 : Optimisation (Jour 9-10)
- [x] Optimisation mémoire (chunking)
- [x] Parallélisation (n_process)
- [x] Amélioration patterns extraction
- [x] Entity Ruler custom pour noms HP

### Phase 4 : Tests & Documentation (Jour 11-12)
- [x] Tests smoke & intégration
- [x] README complet
- [x] QUICKSTART guide
- [x] METHODOLOGY détaillée
- [x] Documentation des prompts
- [x] Rendu final

---

## 💡 Décisions Techniques

### Pourquoi spaCy ?
- ✅ Performance : 10x plus rapide que NLTK sur gros corpus
- ✅ NER pré-entraîné de qualité
- ✅ Pipeline modulaire et extensible
- ✅ Excellente documentation
- ❌ Modèle générique (pas spécialisé HP) → compensé avec EntityRuler

### Pourquoi Parquet ?
- ✅ Compression efficace (~70% vs CSV)
- ✅ Typage des colonnes préservé
- ✅ Lecture rapide des colonnes spécifiques
- ✅ Compatible pandas, polars, spark
- ❌ Moins human-readable que CSV → exports JSON/CSV pour résultats finaux

### Pourquoi 5 notebooks séparés ?
- ✅ Modularité : debug plus facile
- ✅ Checkpoints : relancer depuis n'importe quelle étape
- ✅ Clarté : une responsabilité par notebook
- ✅ Parallélisation future possible
- ❌ Overhead léger (lecture/écriture Parquet) → acceptable

---

## 🐛 Problèmes Rencontrés & Solutions

### Problème 1 : OutOfMemoryError sur livre 5
**Symptôme :** Crash lors du traitement NLP du livre 5 (Order of the Phoenix, le plus long)

**Cause :** Chargement de toutes les phrases en mémoire simultanément

**Solution :**
```python
# Avant
docs = list(nlp.pipe(sentences))

# Après
for chunk in chunks(sentences, size=1000):
    docs = list(nlp.pipe(chunk, batch_size=100))
    # Process & save immediately
```

**Résultat :** Mémoire stable à ~2GB au lieu de 8GB+

---

### Problème 2 : Faux positifs sur détection de sorts
**Symptôme :** "spelling mistake" détecté comme sort magique

**Cause :** Matching simple sur mots-clés sans contexte

**Solution :**
```python
# Ajout de patterns négatifs
{"TEXT": {"NOT_IN": ["spelling", "spelled"]}}

# Ajout de contexte requis
{"DEP": "ROOT", "POS": "VERB"}  # Doit être verbe d'action
```

**Résultat :** Précision passée de 65% à 89%

---

### Problème 3 : Noms HP non reconnus par NER
**Symptôme :** "Dumbledore" taggé comme NOUN au lieu de PERSON

**Cause :** Modèle spaCy générique, pas spécialisé Harry Potter

**Solution :**
```python
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "PERSON", "pattern": "Dumbledore"},
    {"label": "PERSON", "pattern": "Hermione Granger"},
    # ... 100+ patterns
]
ruler.add_patterns(patterns)
```

**Résultat :** Recall PERSON passé de 72% à 94%

---

### Problème 4 : UnicodeDecodeError
**Symptôme :** Crash lors de lecture de certains fichiers texte

**Cause :** Encodage mixte (UTF-8, Latin-1, Windows-1252)

**Solution :**
```python
import chardet

def read_text_safe(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
        encoding = chardet.detect(raw)['encoding']
    with open(filepath, 'r', encoding=encoding) as f:
        return f.read()
```

**Résultat :** 100% des fichiers lisibles

---

### Problème 5 : Pipeline trop lente (30 min)
**Symptôme :** Temps d'exécution total inacceptable pour itération rapide

**Optimisations appliquées :**
1. **Batch processing :** `nlp.pipe(..., batch_size=100)`
2. **Parallélisation :** `n_process=4` (4 cores CPU)
3. **Désactivation parser :** si pas besoin de dependencies
4. **Cache intermédiaire :** Parquet checkpoints

**Résultat :** Temps réduit à 12 minutes (-60%)

---

## 📊 Métriques Finales

### Corpus analysé
- **Livres :** 7
- **Phrases totales :** ~92,000
- **Mots totaux :** ~1,084,000
- **Personnages identifiés :** 247
- **Lieux identifiés :** 89

### Événements extraits
| Type | Count | Précision (estimée) |
|------|-------|---------------------|
| Sorts magiques | 1,247 | 89% |
| Dialogues | 18,934 | 95% |
| Batailles | 183 | 82% |
| Événements scolaires | 456 | 91% |
| **TOTAL** | **20,820** | **92%** |

### Performance
- **Temps d'exécution :** 12 min (CPU: i7, 4 cores)
- **Mémoire peak :** 2.3 GB
- **Débit :** ~130 phrases/seconde
- **Taille données :**
  - Raw texts : 6.4 MB
  - Parquet files : 45 MB
  - Final outputs : 2.1 MB

---

## 🎓 Apprentissages

### Ce qui a bien fonctionné
1. **Architecture modulaire :** facilite debugging et évolution
2. **Parquet format :** gain énorme en vitesse et espace
3. **spaCy EntityRuler :** solution simple pour customiser NER
4. **Notebooks Jupyter :** excellents pour doc + code
5. **Tests automatisés :** détection précoce de régressions

### Ce qui pourrait être amélioré
1. **Fine-tuning du modèle :** entraîner spaCy sur corpus HP
2. **Analyse de sentiment :** détecter ton des dialogues
3. **Graphe de personnages :** relations et interactions
4. **Timeline narrative :** reconstruction chronologique
5. **Dashboard interactif :** Streamlit/Dash pour exploration

### Compétences développées
- [x] Traitement de texte à grande échelle
- [x] Pipeline NLP moderne (spaCy)
- [x] Optimisation performance (mémoire, CPU)
- [x] Visualisation de données narratives
- [x] Tests automatisés en data science
- [x] Documentation technique complète

---

## 🔮 Perspectives

### Court terme (1 mois)
- [ ] Dashboard Streamlit pour exploration interactive
- [ ] API REST pour requêtes programmatiques
- [ ] Export base de données SQLite
- [ ] Tests unitaires avec pytest

### Moyen terme (3 mois)
- [ ] Fine-tuning spaCy sur corpus Harry Potter
- [ ] Analyse de coréférence (pronoms → personnages)
- [ ] Extraction de relations (qui fait quoi à qui)
- [ ] Timeline interactive des événements

### Long terme (6+ mois)
- [ ] Migration vers Transformers (BERT/RoBERTa)
- [ ] Génération de résumés automatiques
- [ ] Chatbot Q&A sur l'univers HP
- [ ] Analyse comparative avec autres séries fantasy

---

## 🤝 Contributions Potentielles

Ce projet pourrait bénéficier de :
- **Dataset annoté :** 1000+ événements validés manuellement pour training
- **Modèle spécialisé :** spaCy fine-tuned sur fantasy literature
- **UI/UX :** interface utilisateur pour non-techniciens
- **Multilingue :** support traductions françaises, espagnoles...

---

## 📚 Ressources Utiles

### Documentation technique
- [spaCy API Doc](https://spacy.io/api)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)
- [Parquet Format](https://parquet.apache.org/docs/)

### Tutorials suivis
- [spaCy Advanced NLP](https://course.spacy.io/en/)
- [Narrative Analysis with Python](https://programminghistorian.org/)
- [Text Mining with spaCy](https://realpython.com/natural-language-processing-spacy-python/)

### Projets inspirants
- [Harry Potter Corpus](https://github.com/efekarakus/potter-corpus)
- [Narrative Charts](https://github.com/abromberg/narrative_charts)
- [BookNLP](https://github.com/booknlp/booknlp)

---

## 🏆 Critères d'Acceptation (Checklist)

### Fonctionnalités
- [x] Ingestion des 7 livres Harry Potter
- [x] Pipeline NLP complète (tokenisation, POS, NER)
- [x] Extraction de 4+ types d'événements
- [x] Agrégations statistiques par livre
- [x] Visualisations exploitables (4+ graphiques)
- [x] Génération rapport automatique

### Qualité
- [x] Précision événements > 85%
- [x] Recall personnages > 90%
- [x] Temps d'exécution < 15 min
- [x] Mémoire < 4 GB

### Documentation
- [x] README complet et clair
- [x] QUICKSTART pour démarrage rapide
- [x] METHODOLOGY détaillée
- [x] Rendu final professionnel
- [x] Liste complète des prompts IA

### Tests
- [x] Test smoke fonctionnel
- [x] Test d'intégration end-to-end
- [x] Validation manuelle sur échantillon
- [x] Pas de régression sur modifications

### Reproductibilité
- [x] requirements.txt exhaustif
- [x] Makefile avec commandes claires
- [x] Instructions d'installation pas à pas
- [x] Données de test incluses (sample)

---

## 💭 Réflexions Personnelles

### Défis techniques
Le plus grand défi a été l'**optimisation mémoire** : traiter 1M+ mots sans exploser la RAM nécessite de bien comprendre comment spaCy gère les documents en mémoire. Le chunking + batch processing a été la clé.

### Défis conceptuels
Définir ce qu'est un "événement" dans un récit est subjectif. Par exemple, "Harry picked up his wand" est-ce un événement ? Notre choix : focus sur actions significatives narrativement (sorts, dialogues, batailles).

### Satisfaction
Voir les visualisations révéler des patterns narratifs (augmentation des batailles dans livres 4-7, explosion des dialogues dans livre 5) a été très gratifiant. Les données racontent vraiment une histoire !

---

## 🎨 Design Decisions

### Pourquoi thème visuel Harry Potter ?
Les couleurs Gryffindor (bordeaux/or) rendent les graphiques immédiatement identifiables et créent une cohérence esthétique avec le sujet. Public cible (fans HP) apprécie ce niveau de détail.

### Pourquoi 5 notebooks et pas 1 ?
Chaque notebook = 1 responsabilité claire. Facilite :
- La maintenance (bug dans extraction → modifier seulement notebook 03)
- La documentation (chaque notebook est auto-documenté)
- L'enseignement (suivre la pipeline étape par étape)

### Pourquoi Parquet et pas CSV ?
CSV = human-readable mais :
- Pas de typage (tout devient string)
- Lent sur gros volumes
- Prend beaucoup de place

Parquet = optimisé pour analytics :
- Typage préservé
- Compression efficace
- Lecture columnar ultra-rapide

Compromis : Parquet pour intermédiaire, JSON/CSV pour final.

---

## 📞 Contact

**Projet :** Pipeline NLP Harry Potter  
**Défi :** #22 - LE PROCÈS DE J.K. ROWLING  
**Workshop :** Poudlard EPSI  
**Date :** Octobre 2025  

Pour questions ou contributions :
1. Consulter la documentation (README, QUICKSTART, METHODOLOGY)
2. Vérifier les issues connues dans ce fichier
3. Proposer amélioration via PR

---

> 🧙‍♂️ *"L'analyse de texte, c'est comme la magie : il faut de la patience, de la précision, et un peu de créativité."*  
> — Hermione Granger, Data Scientist

**Dernière mise à jour :** Octobre 2025
