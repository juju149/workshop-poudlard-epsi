# Notes de développement — plan2blend

## Décisions techniques

### Architecture modulaire

Le projet a été conçu avec une architecture modulaire pour faciliter l'évolution :

1. **Scripts indépendants** : Chaque étape du pipeline est un script autonome
2. **Format JSON intermédiaire** : Permet de déboguer et modifier les données entre étapes
3. **Utilitaires réutilisables** : Les fonctions géométriques et I/O sont dans des modules séparés

### Choix de simplification

Pour ce POC (Proof of Concept), certains choix ont été faits pour la rapidité de mise en œuvre :

#### Vectorisation simplifiée
- **Actuel** : Génération de données d'exemple structurées
- **Production** : Utiliser un modèle ML (U-Net, Mask R-CNN) entraîné sur CubiCasa5k ou similaire

#### Blender headless
- **Actuel** : Script Blender Python complet et fonctionnel
- **Amélioration** : Optimisation des boolean operations pour de grands modèles

#### Contrôle qualité
- **Actuel** : Overlay visuel et métriques simples
- **Production** : Calcul de distance de Hausdorff, analyse de surface réelle

## Limites connues

### Détection IA
Le script de vectorisation actuel génère des données d'exemple. Pour un usage réel :
- Intégrer un modèle de détection d'objets architecturaux
- Entraîner sur des plans similaires au bâtiment cible
- Ajuster les seuils de détection selon la qualité du PDF

### Performance Blender
Pour de très grands bâtiments (>100 pièces) :
- Les boolean operations peuvent être lentes
- Considérer l'utilisation de bmesh direct au lieu de modificateurs
- Regrouper les ouvertures similaires

### Échelle et DPI
Le calcul d'échelle assume :
- PDF vectoriel avec échelle lisible
- 600 DPI pour l'export
- Échelle uniforme sur toute la page

## Évolutions futures

### Court terme
- [ ] Détection automatique de l'échelle dans le cartouche
- [ ] Support multi-pages PDF (étages multiples)
- [ ] Amélioration de la détection de contours

### Moyen terme
- [ ] Intégration d'un modèle ML pour la vectorisation
- [ ] Export IFC pour compatibilité BIM
- [ ] Interface web pour upload et visualisation

### Long terme
- [ ] Génération automatique de meubles selon fonction de pièce
- [ ] Animation de visite guidée
- [ ] Rendu photoréaliste avec Cycles

## Tests et validation

### Tests unitaires
- Couverture : ~90% du code utilitaire
- Framework : pytest
- CI/CD : À intégrer (GitHub Actions)

### Tests d'intégration
- Pipeline end-to-end avec données d'exemple
- Validation du format JSON
- Vérification des exports (.blend, .glb)

### Tests de non-régression
- Snapshots visuels à comparer
- Métriques de fidélité à suivre
- Tests de performance sur grands plans

## Ressources utilisées

### Outils open-source
- **Blender** : Génération 3D (GPL)
- **OpenCV** : Traitement d'image (Apache 2.0)
- **Shapely** : Opérations géométriques (BSD)
- **pdf2image** : Conversion PDF (MIT)

### Datasets potentiels
- **CubiCasa5k** : 5000 floor plans annotés
- **RPLAN** : Plans architecturaux synthétiques
- **Floor-SP** : Segmentation de plans d'étage

### Modèles ML
Pour une implémentation production :
- **FloorplanToBlender3D** : GitHub open-source
- **CubiCasa** : Modèles pré-entraînés disponibles
- **Custom U-Net** : À entraîner sur données spécifiques

## Maintenance

### Dépendances
- Maintenir les versions de Blender compatibles (3.6+)
- Mettre à jour OpenCV régulièrement pour les corrections de sécurité
- Surveiller les changements d'API dans les packages Python

### Documentation
- Tenir à jour le README avec les nouvelles fonctionnalités
- Documenter les cas d'usage réels rencontrés
- Partager les prompts Copilot efficaces

## Contributeurs

Projet développé avec l'assistance de GitHub Copilot.
Open-source, contributions bienvenues !
