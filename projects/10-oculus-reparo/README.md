# 🔧 OCULUS REPARO - Transformation Digitale de l'Emploi du Temps

**Challenge #10** - Cahier des charges pour la refonte de l'outil de gestion des emplois du temps

## 🎯 Objectif

Rédiger un **cahier des charges complet** pour la refonte et la transformation digitale de l'outil interne de gestion des emplois du temps de l'école, actuellement lent, peu ergonomique et source de nombreux bugs.

L'objectif est de proposer une **solution moderne, fluide et responsive**, adaptée aux besoins des étudiants, professeurs et équipes administratives.

## 📦 Livrables

Ce projet contient les livrables suivants :

### 📘 Documents principaux

1. **Cahier des charges complet** (`docs/cahier_des_charges.md`)
   - Analyse de l'existant
   - Recensement des fonctionnalités actuelles
   - Enquête auprès des parties prenantes
   - Identification des problèmes majeurs
   - Axes d'amélioration et recommandations techniques
   - Spécifications fonctionnelles et techniques détaillées

2. **Synthèse commerciale** (`docs/synthese_commerciale.md`)
   - Pitch clair du projet
   - Analyse des bénéfices organisationnels
   - Estimation du ROI (Retour sur Investissement)
   - Arguments de vente

### 📄 Versions PDF

Les versions PDF des documents sont générées dans le dossier `docs/pdf/` :
- `cahier_des_charges.pdf` - Version imprimable du cahier des charges
- `synthese_commerciale.pdf` - Version imprimable de la synthèse commerciale

## 🏗️ Structure du projet

```
10-oculus-reparo/
├── README.md                          # Ce fichier
├── docs/
│   ├── cahier_des_charges.md         # Cahier des charges complet
│   ├── synthese_commerciale.md       # Synthèse commerciale et ROI
│   ├── enquete_stakeholders.md       # Méthodologie et résultats d'enquête
│   ├── rendu.md                      # Document de rendu détaillé
│   ├── prompts_used.md               # Historique des prompts IA utilisés
│   └── pdf/                          # Versions PDF des livrables
│       ├── cahier_des_charges.pdf
│       └── synthese_commerciale.pdf
└── assets/
    ├── diagrams/                     # Diagrammes d'architecture
    └── mockups/                      # Maquettes d'interface (optionnel)
```

## 📋 Exigences traitées

- ✅ Recensement des **fonctionnalités actuelles** de l'outil existant
- ✅ **Enquête** auprès des différentes parties prenantes (étudiants, enseignants, administration)
- ✅ Identification des **problèmes majeurs** (UX, performance, fiabilité)
- ✅ Proposition d'**axes d'amélioration** et de **recommandations techniques**
- ✅ Mise en avant des **avantages commerciaux et organisationnels**

## 🚀 Génération des PDF

Pour générer les versions PDF des documents :

### Méthode 1 : Utiliser Pandoc (recommandé)

```bash
# Installation de Pandoc (si nécessaire)
# Ubuntu/Debian
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# macOS
brew install pandoc basictex

# Génération des PDF
cd docs
pandoc cahier_des_charges.md -o pdf/cahier_des_charges.pdf --pdf-engine=xelatex -V geometry:margin=1in
pandoc synthese_commerciale.md -o pdf/synthese_commerciale.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

### Méthode 2 : Utiliser un convertisseur en ligne

- [Markdown to PDF](https://www.markdowntopdf.com/)
- [Dillinger](https://dillinger.io/) - Export PDF
- [HackMD](https://hackmd.io/) - Export PDF

### Méthode 3 : Imprimer depuis votre navigateur

1. Ouvrir le fichier Markdown dans votre IDE préféré avec prévisualisation
2. Utiliser la fonction "Imprimer" du navigateur
3. Sélectionner "Enregistrer au format PDF"

## 📊 Contenu du Cahier des Charges

Le cahier des charges comprend :

1. **Contexte et enjeux**
   - Présentation de l'outil actuel
   - Problématiques identifiées
   - Objectifs de la transformation

2. **Analyse de l'existant**
   - Fonctionnalités actuelles
   - Architecture technique
   - Points de douleur utilisateurs

3. **Étude des besoins**
   - Méthodologie d'enquête
   - Besoins par type d'utilisateur
   - Priorisation des demandes

4. **Solution proposée**
   - Vision de la nouvelle solution
   - Fonctionnalités prioritaires
   - Roadmap de déploiement

5. **Spécifications techniques**
   - Architecture système
   - Technologies recommandées
   - Intégrations et API
   - Sécurité et conformité

6. **Contraintes et risques**
   - Contraintes techniques et organisationnelles
   - Analyse des risques
   - Plan de mitigation

## 💼 Contenu de la Synthèse Commerciale

La synthèse commerciale comprend :

1. **Pitch du projet**
   - Vision en 3 minutes
   - Valeur ajoutée
   - Différenciation

2. **Bénéfices organisationnels**
   - Gain de temps mesurable
   - Amélioration de la satisfaction
   - Valorisation de l'image

3. **Estimation du ROI**
   - Coûts estimés
   - Économies et gains
   - Retour sur investissement

4. **Planning et jalons**
   - Phases du projet
   - Timeline
   - Quick wins

## 👥 Parties prenantes consultées

L'enquête a ciblé trois groupes principaux :

1. **Étudiants** (utilisateurs finaux)
   - Accès à l'emploi du temps
   - Notifications de changements
   - Intégration calendrier

2. **Enseignants** (créateurs de contenu)
   - Gestion des cours
   - Disponibilités
   - Salles et ressources

3. **Administration** (gestionnaires)
   - Planification globale
   - Gestion des conflits
   - Reporting et statistiques

## 🎓 Méthodologie

Le cahier des charges a été élaboré selon une méthodologie structurée :

1. **Analyse de l'existant** - Audit de l'outil actuel
2. **Collecte des besoins** - Enquêtes et interviews
3. **Benchmark** - Comparaison avec solutions du marché
4. **Priorisation** - MoSCoW (Must/Should/Could/Won't)
5. **Spécification** - Rédaction détaillée
6. **Validation** - Revue avec parties prenantes

## ⏱️ Informations

- **Story Points** : 5
- **Deadline** : 15/10/2025
- **Challenge #10** - OCULUS REPARO
- **Copilots recommandés** : Documentation Copilot (lead), Project Lead

## 📚 Documentation complémentaire

- [Rendu complet](docs/rendu.md) - Document de rendu détaillé
- [Enquête stakeholders](docs/enquete_stakeholders.md) - Méthodologie et résultats
- [Prompts utilisés](docs/prompts_used.md) - Historique des prompts IA

## 💡 Points clés de la transformation

### Problèmes identifiés
- ⚠️ Interface vieillissante et peu intuitive
- ⚠️ Temps de chargement lents (>5 secondes)
- ⚠️ Bugs fréquents lors des modifications
- ⚠️ Non responsive (problèmes sur mobile)
- ⚠️ Notifications inexistantes ou non fiables
- ⚠️ Manque d'intégration avec autres outils

### Solutions proposées
- ✅ Interface moderne et ergonomique (Material Design / Fluent UI)
- ✅ Performance optimisée (<1 seconde de chargement)
- ✅ Tests automatisés pour réduire les bugs
- ✅ Design responsive (mobile first)
- ✅ Système de notifications en temps réel
- ✅ API REST pour intégrations tierces

### Bénéfices attendus
- 📈 Gain de temps : **30% de réduction** des tâches administratives
- 😊 Satisfaction utilisateur : objectif **>85%**
- 🎯 Réduction des erreurs : **-70%** de bugs signalés
- 💰 ROI estimé : **18 mois**

## 🔗 Ressources utiles

- [Guide de rédaction d'un cahier des charges](https://www.redacteur.com/blog/cahier-des-charges/)
- [Méthodologie ADKAR pour le change management](https://www.prosci.com/adkar)
- [Calcul du ROI d'un projet IT](https://www.cio.com/article/3268379/how-to-calculate-roi-for-it-projects.html)

## 📝 Notes

Ce document a été rédigé dans le cadre du Workshop "Poudlard à l'EPSI/WIS" 2025.

L'outil actuel de gestion des emplois du temps représente un point de friction majeur pour l'ensemble de la communauté éducative. Cette transformation digitale vise à moderniser l'expérience utilisateur tout en améliorant l'efficacité opérationnelle de l'établissement.

---

**Note importante** : Ce cahier des charges est un document vivant qui devra être mis à jour régulièrement en fonction des retours des parties prenantes et de l'évolution du contexte.

✨ *"Il faut beaucoup de courage pour tenir tête à ses ennemis, mais il en faut tout autant pour tenir tête à ses amis."* - Albus Dumbledore

*La transformation digitale nécessite courage et détermination.*
