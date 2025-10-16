# Enquête Parties Prenantes - Méthodologie et Résultats

**Projet** : Transformation Digitale de l'Emploi du Temps  
**Date de l'enquête** : Septembre-Octobre 2025  
**Responsable** : Équipe Transformation Digitale

---

## Table des matières

1. [Méthodologie](#méthodologie)
2. [Résultats étudiants](#résultats-étudiants)
3. [Résultats enseignants](#résultats-enseignants)
4. [Résultats administration](#résultats-administration)
5. [Analyse transversale](#analyse-transversale)
6. [Recommandations](#recommandations)

---

## Méthodologie

### Objectifs de l'enquête

1. **Recenser** les fonctionnalités utilisées et attendues
2. **Identifier** les points de douleur principaux
3. **Prioriser** les besoins par type d'utilisateur
4. **Collecter** des retours qualitatifs et quantitatifs
5. **Valider** les hypothèses du cahier des charges

### Population cible

| Groupe | Population totale | Échantillon | Taux de réponse |
|--------|-------------------|-------------|-----------------|
| Étudiants | 2 500 | 250 | 10% |
| Enseignants | 150 | 80 | 53% |
| Administration | 15 | 12 | 80% |
| **TOTAL** | 2 665 | **342** | **12.8%** |

### Approches utilisées

#### 1. Questionnaires en ligne (N=342)

**Outils** : Google Forms, distribution par email et affichage campus

**Durée** : 2 semaines (15 sept - 30 sept 2025)

**Structure** :
- 15 questions fermées (échelle Likert 1-5)
- 5 questions ouvertes (verbatims)
- Temps moyen de complétion : 8 minutes

**Taux de participation** :
- Étudiants : 10% (objectif atteint)
- Enseignants : 53% (excellent)
- Administration : 80% (excellent)

#### 2. Interviews approfondies (N=25)

**Sélection** : Panel représentatif volontaire

**Distribution** :
- 15 étudiants (6 L3, 5 M1, 4 M2)
- 7 enseignants (4 temps plein, 3 intervenants)
- 3 administratifs (planning, direction, IT)

**Format** :
- Durée : 30-45 minutes
- Questions semi-structurées
- Enregistrement avec consentement
- Transcription et analyse thématique

**Thèmes explorés** :
- Utilisation quotidienne de l'outil actuel
- Frustrations et points de blocage
- Attentes et besoins non couverts
- Solutions utilisées en parallèle (workarounds)
- Vision de l'outil idéal

#### 3. Observation terrain (2 semaines)

**Activités** :
- Shadowing des administrateurs (3 jours)
- Analyse des tickets support (6 mois d'historique)
- Mesures de performance (temps de chargement, erreurs)
- Session de travail avec équipe planning

**Données collectées** :
- 178 tickets support sur 6 mois (30/mois en moyenne)
- Temps de chargement moyen : 8.5 secondes (pic : 15s)
- 45 bugs identifiés dont 12 critiques
- Processus de planification : 4h/semaine

#### 4. Benchmark concurrentiel

**Solutions analysées** :
1. **ADE (Adesoft)** - Leader marché français
2. **Hyperplanning** - Alternative populaire
3. **Celcat** - Solution internationale
4. **Primavera** - Gestion projets académiques
5. **Solution custom école partenaire** - Développement interne

**Critères évalués** :
- Fonctionnalités
- Ergonomie et UX
- Performance
- Intégrations
- Coût
- Support

**Résultat** : Aucune solution existante ne répond à 100% de nos besoins spécifiques, mais toutes offrent des fonctionnalités intéressantes à intégrer.

---

## Résultats étudiants

### Profil des répondants (N=250)

- **Niveau d'études** :
  - L3 : 30% (75)
  - M1 : 35% (87)
  - M2 : 35% (88)

- **Fréquence de consultation** :
  - Quotidienne : 68%
  - Hebdomadaire : 28%
  - Mensuelle : 4%

- **Appareil principal** :
  - Smartphone : 65%
  - Ordinateur : 30%
  - Tablette : 5%

### Satisfaction actuelle

**Question** : "Sur une échelle de 1 à 5, à quel point êtes-vous satisfait de l'outil actuel ?"

| Note | Réponses | % |
|------|----------|---|
| 1 (Très insatisfait) | 95 | 38% |
| 2 (Insatisfait) | 78 | 31% |
| 3 (Neutre) | 52 | 21% |
| 4 (Satisfait) | 20 | 8% |
| 5 (Très satisfait) | 5 | 2% |

**Moyenne** : **2.0/5** (40% de satisfaction)

### Problèmes identifiés

**Question** : "Quels sont les principaux problèmes que vous rencontrez ?"

| Problème | Occurrences | % |
|----------|-------------|---|
| **Lenteur de chargement** | 230 | 92% |
| **Non adapté mobile** | 218 | 87% |
| **Pas de notifications** | 195 | 78% |
| **Interface peu intuitive** | 170 | 68% |
| **Bugs fréquents** | 145 | 58% |
| **Export calendrier difficile** | 113 | 45% |
| **Recherche inefficace** | 98 | 39% |

### Besoins exprimés

**Question** : "Quelles fonctionnalités souhaiteriez-vous ?"

| Besoin | Votes | Priorité |
|--------|-------|----------|
| **Application mobile** | 238 | 🔴 Haute |
| **Notifications push** | 225 | 🔴 Haute |
| **Synchronisation calendrier** | 210 | 🔴 Haute |
| **Rapidité < 1s** | 205 | 🔴 Haute |
| **Interface moderne** | 188 | 🟠 Moyenne |
| **Mode hors ligne** | 165 | 🟠 Moyenne |
| **Partage d'emploi du temps** | 120 | 🟡 Basse |
| **Widget** | 95 | 🟡 Basse |

### Verbatims marquants

> "Je ne peux jamais consulter mon emploi du temps sur mon téléphone, c'est frustrant en 2025 !"  
> — Étudiant M1

> "Quand il y a un changement de salle, je ne le sais jamais. J'arrive devant une porte fermée."  
> — Étudiante L3

> "Le site met tellement de temps à charger que je finis par prendre une photo de mon emploi du temps."  
> — Étudiant M2

> "J'ai essayé d'exporter vers Google Calendar, mais ça n'a jamais marché. J'ai abandonné."  
> — Étudiante M1

> "L'interface est tellement moche et old school, on dirait un site des années 2000."  
> — Étudiant L3

### Workarounds identifiés

**Stratégies de contournement utilisées** :
- 68% prennent des captures d'écran de leur emploi du temps
- 45% recopient manuellement dans leur calendrier personnel
- 32% utilisent des applications tierces (EDT, ADE Mobile...)
- 25% demandent à des amis de partager leur emploi du temps
- 18% créent des groupes WhatsApp pour s'alerter des changements

### Adoption attendue

**Question** : "Utiliseriez-vous une application mobile moderne ?"

- Certainement : 78%
- Probablement : 18%
- Peut-être : 3%
- Non : 1%

**Taux d'adoption potentiel : 96%**

---

## Résultats enseignants

### Profil des répondants (N=80)

- **Statut** :
  - Temps plein : 45% (36)
  - Intervenant régulier : 40% (32)
  - Vacataire : 15% (12)

- **Ancienneté** :
  - < 2 ans : 20%
  - 2-5 ans : 35%
  - 5-10 ans : 30%
  - > 10 ans : 15%

- **Fréquence d'utilisation** :
  - Quotidienne : 35%
  - Hebdomadaire : 50%
  - Mensuelle : 15%

### Satisfaction actuelle

**Question** : "Sur une échelle de 1 à 5, évaluez votre satisfaction ?"

| Note | Réponses | % |
|------|----------|---|
| 1 (Très insatisfait) | 25 | 31% |
| 2 (Insatisfait) | 30 | 38% |
| 3 (Neutre) | 18 | 23% |
| 4 (Satisfait) | 6 | 7% |
| 5 (Très satisfait) | 1 | 1% |

**Moyenne** : **2.1/5** (42% de satisfaction)

### Problèmes identifiés

| Problème | Occurrences | % |
|----------|-------------|---|
| **Processus trop complexe** | 68 | 85% |
| **Pas de détection de conflits** | 58 | 72% |
| **Interface mobile inexistante** | 56 | 70% |
| **Pas de statistiques perso** | 46 | 58% |
| **Manque d'intégration** | 40 | 50% |
| **Lenteur** | 35 | 44% |

### Besoins exprimés

| Besoin | Votes | Priorité |
|--------|-------|----------|
| **Simplification saisie dispo** | 72 | 🔴 Haute |
| **Alertes conflits auto** | 65 | 🔴 Haute |
| **Consultation mobile** | 58 | 🔴 Haute |
| **Vue consolidée mes cours** | 55 | 🟠 Moyenne |
| **Statistiques heures** | 48 | 🟠 Moyenne |
| **Export planning perso** | 42 | 🟠 Moyenne |
| **Gestion absences** | 38 | 🟡 Basse |

### Verbatims marquants

> "Il faut 15 clics pour déclarer mes disponibilités. C'est décourageant."  
> — Enseignant temps plein

> "Je me suis retrouvé avec 2 cours en même temps, personne ne m'a prévenu."  
> — Intervenant

> "Impossible de voir rapidement combien d'heures j'ai faites ce mois-ci."  
> — Enseignant temps plein

> "L'outil n'est pas connecté avec Moodle, je dois tout refaire deux fois."  
> — Enseignant

> "En déplacement, je ne peux rien faire depuis mon téléphone. C'est problématique."  
> — Intervenant

### Temps passé

**Question** : "Combien de temps passez-vous sur l'outil ?"

- Déclaration disponibilités : **30 min/mois** en moyenne
- Consultation planning : **10 min/semaine** en moyenne
- Modifications/demandes : **20 min/mois** en moyenne

**Total** : ~3h/mois par enseignant
**Pour 150 enseignants** : 450h/mois = **5 400h/an**

**Gain attendu avec nouvel outil** : -50% = **2 700h/an économisées**

---

## Résultats administration

### Profil des répondants (N=12)

- **Fonction** :
  - Responsable planning : 4
  - Assistant planning : 5
  - Direction pédagogique : 2
  - IT/Support : 1

- **Ancienneté dans la fonction** :
  - < 1 an : 2
  - 1-3 ans : 5
  - 3-5 ans : 3
  - > 5 ans : 2

### Satisfaction actuelle

**Moyenne** : **1.8/5** (36% de satisfaction)

### Problèmes critiques identifiés

| Problème | Votes | Impact |
|----------|-------|--------|
| **Détection conflits manuelle** | 12/12 | 🔴 Critique |
| **Import/Export chronophage** | 11/12 | 🔴 Critique |
| **Plantages fréquents** | 10/12 | 🔴 Critique |
| **Pas d'historique/traçabilité** | 9/12 | 🔴 Critique |
| **Pas d'analytics** | 8/12 | 🟠 Élevé |
| **Processus non optimisés** | 8/12 | 🟠 Élevé |
| **Pas d'API** | 6/12 | 🟡 Moyen |

### Temps passé sur les tâches

**Répartition hebdomadaire moyenne (par personne)** :

| Tâche | Temps | % |
|-------|-------|---|
| Planification manuelle | 6h | 30% |
| Détection/Résolution conflits | 4h | 20% |
| Saisie/Modifications | 3h | 15% |
| Import/Export données | 2.5h | 12.5% |
| Support utilisateurs | 2h | 10% |
| Reporting manuel | 1.5h | 7.5% |
| Autres tâches | 1h | 5% |
| **TOTAL** | **20h** | **100%** |

**Temps total équipe** : 15 personnes × 20h = **300h/semaine** = **15 600h/an**

### Besoins exprimés

| Besoin | Votes | Priorité |
|--------|-------|----------|
| **Détection conflits auto** | 12/12 | 🔴 Critique |
| **Import/Export simplifié** | 11/12 | 🔴 Critique |
| **Historique complet** | 10/12 | 🔴 Critique |
| **Tableaux de bord** | 10/12 | 🔴 Haute |
| **Performance améliorée** | 9/12 | 🔴 Haute |
| **Interface drag & drop** | 9/12 | 🟠 Moyenne |
| **API REST** | 7/12 | 🟠 Moyenne |

### Verbatims marquants

> "Je passe 4 heures par semaine à chercher manuellement des conflits d'horaires. C'est du temps perdu."  
> — Responsable planning

> "L'outil plante systématiquement en période de rentrée quand on a le plus besoin de lui."  
> — Assistant planning

> "Impossible de savoir qui a modifié quoi et quand. C'est un vrai problème de traçabilité."  
> — Direction pédagogique

> "L'import CSV prend 2 heures et échoue une fois sur trois. C'est notre cauchemar."  
> — Responsable planning

> "On n'a aucune vision d'ensemble. Pas de stats, pas de dashboards, rien."  
> — Direction pédagogique

### Incidents et support

**Analyse des tickets support (6 derniers mois)** :

| Type d'incident | Nombre | % |
|-----------------|--------|---|
| Bugs/Erreurs | 78 | 44% |
| Lenteur/Performance | 45 | 25% |
| Conflits horaires | 32 | 18% |
| Import/Export | 15 | 8% |
| Autres | 8 | 5% |
| **TOTAL** | **178** | **100%** |

**Moyenne** : **30 incidents/mois**

**Temps de résolution moyen** : 2.5 heures/incident

**Coût estimé** : 178 incidents × 2.5h × 40€/h = **17 800€ sur 6 mois**

---

## Analyse transversale

### Points de convergence

Les trois groupes d'utilisateurs convergent sur plusieurs problèmes critiques :

#### 1. Performance insuffisante
- **Étudiants** : 92% se plaignent de la lenteur
- **Enseignants** : 44% citent la lenteur
- **Administration** : 100% concernés par les plantages

#### 2. Absence de mobilité
- **Étudiants** : 87% veulent du mobile
- **Enseignants** : 70% veulent consulter en mobilité
- **Administration** : Demande d'accès à distance

#### 3. Manque de notifications
- **Étudiants** : 78% ne sont pas prévenus des changements
- **Enseignants** : Pas d'alertes de conflits
- **Administration** : Pas d'alertes système

#### 4. Interface vieillissante
- **Tous les groupes** : Interface non intuitive, ergonomie médiocre

### Points de divergence

#### Étudiants : Focus sur l'expérience utilisateur
- Rapidité, mobile, esthétique
- Fonctionnalités de confort (partage, widget)

#### Enseignants : Focus sur l'efficacité
- Simplification des processus
- Alertes et prévention
- Statistiques professionnelles

#### Administration : Focus sur la gestion et le pilotage
- Automatisation des tâches répétitives
- Outils de pilotage et analytics
- Fiabilité et traçabilité

### Matrice importance/satisfaction

| Fonctionnalité | Importance | Satisfaction | Action |
|----------------|------------|--------------|--------|
| Performance | 🔴 Très haute | 🔴 Très faible | **Priorité absolue** |
| Mobile | 🔴 Très haute | 🔴 Très faible | **Priorité absolue** |
| Notifications | 🔴 Haute | 🔴 Très faible | **Priorité haute** |
| Détection conflits | 🔴 Haute | 🔴 Très faible | **Priorité haute** |
| Interface | 🟠 Moyenne | 🔴 Faible | **À améliorer** |
| Analytics | 🟠 Moyenne | 🔴 Très faible | **À développer** |

---

## Recommandations

### 1. Priorisation des fonctionnalités (Méthode MoSCoW)

#### Must Have (MVP - Release 1)
✅ **Performance** : Temps de chargement < 1 seconde  
✅ **Responsive Design** : Interface adaptée mobile/tablette/desktop  
✅ **Notifications** : Système de notifications temps réel  
✅ **Détection conflits** : Algorithme automatique  
✅ **Export calendrier** : iCal et Google Calendar  
✅ **Historique** : Traçabilité complète des modifications  

#### Should Have (Release 2)
🟠 **Application mobile native** : iOS et Android  
🟠 **Mode hors ligne** : Consultation sans connexion  
🟠 **Analytics** : Tableaux de bord pour administration  
🟠 **Import/Export avancé** : Processus simplifiés  
🟠 **API REST** : Intégrations tierces  

#### Could Have (Release 3+)
🟡 **IA suggestions** : Optimisation automatique  
🟡 **Partage social** : Partage d'emploi du temps  
🟡 **Widget** : Widget iOS/Android  
🟡 **Chatbot** : Assistant virtuel  

#### Won't Have (Hors scope)
❌ Gestion de la paie enseignants  
❌ Système de notation  
❌ Gestion des inscriptions  

### 2. Cibles de satisfaction

| Groupe | Actuel | Objectif Y1 | Objectif Y2 |
|--------|--------|-------------|-------------|
| Étudiants | 40% | 70% | 85% |
| Enseignants | 42% | 72% | 85% |
| Administration | 36% | 75% | 90% |

### 3. Quick wins à cibler

**Phase Pilote (1 promotion)** :
- Feedback rapide et itérations
- Ambassadeurs utilisateurs
- Communication progressive

**Déploiement général** :
- Formation ciblée par groupe
- Support renforcé (3 mois)
- FAQ et tutoriels vidéo

**Mesure du succès** :
- Enquête satisfaction post-déploiement
- Analyse des tickets support
- Métriques d'usage (connexions, temps passé)
- NPS (Net Promoter Score)

### 4. Change management

#### Communication
- **Avant** : Teasing, implication dans conception
- **Pendant** : Transparence sur l'avancement
- **Après** : Célébration, retours utilisateurs

#### Formation
- **Étudiants** : Tutoriels vidéo, FAQ, support en ligne
- **Enseignants** : Sessions de 1h, documentation
- **Administration** : Formation approfondie (2 jours)

#### Support
- **Helpdesk renforcé** : +2 personnes pendant 3 mois
- **FAQ vivante** : Mise à jour continue
- **Ambassadeurs** : 1 par promotion/département

---

## Conclusion

L'enquête auprès de 342 utilisateurs (12.8% de la population) révèle un **besoin critique de transformation** de l'outil de gestion des emplois du temps.

### Principaux enseignements

1. **Insatisfaction généralisée** : Satisfaction moyenne de 38% seulement
2. **Convergence des besoins** : Performance, mobile, notifications
3. **Impact mesurable** : 15 600h/an passées par l'administration
4. **Fort potentiel d'adoption** : 96% d'adoption attendue pour app mobile

### Prochaines étapes

1. ✅ Validation du cahier des charges
2. ⏳ Constitution de l'équipe projet
3. ⏳ Lancement des workshops de conception
4. ⏳ Développement du MVP

---

**Note** : Les résultats complets de l'enquête (données brutes, verbatims complets) sont disponibles sur demande auprès de l'équipe Transformation Digitale.

*Enquête réalisée dans le cadre du Workshop Poudlard EPSI/WIS 2025*

✨ *"La vérité est une chose magnifique et terrible, qu'il faut manier avec grande précaution."* - Albus Dumbledore

*Les données de cette enquête éclairent le chemin de la transformation.*
