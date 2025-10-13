# 📖 Guide Utilisateur - Emploi du Temps McGonagall

## 🎯 Bienvenue

Bienvenue dans l'application **Emploi du Temps McGonagall** ! Cette application vous permet de consulter facilement votre emploi du temps depuis l'API wigorservices dans une interface moderne et intuitive.

## 🚀 Démarrage Rapide

### Installation

1. **Téléchargez l'installateur**
   - Récupérez le fichier `Emploi du Temps McGonagall Setup.exe`
   - Ou buildez depuis les sources : `npm run electron:build`

2. **Installez l'application**
   - Double-cliquez sur l'installateur
   - Suivez les instructions à l'écran
   - L'application sera installée dans `Program Files`

3. **Configurez vos identifiants**
   - Créez un fichier `.env` dans le dossier d'installation
   - Ajoutez vos identifiants :
     ```
     USERNAME=votre_identifiant
     PASSWORD=votre_mot_de_passe
     ```

4. **Lancez l'application**
   - Utilisez le raccourci du bureau
   - Ou lancez depuis le menu Démarrer

## 🎮 Utilisation

### Interface Principale

L'application se compose de trois zones principales :

```
┌─────────────────────────────────────────┐
│  📚 Emploi du Temps McGonagall          │
│  Consultez votre emploi du temps magique│
├─────────────────────────────────────────┤
│  [Date: __/__/____] [Rechercher] [Auj.] │
├─────────────────────────────────────────┤
│                                         │
│         Zone d'affichage                │
│         des cours                       │
│                                         │
└─────────────────────────────────────────┘
```

### 1. Consulter l'Emploi du Temps du Jour

**Méthode la plus simple :**

1. Cliquez sur le bouton **"Aujourd'hui"**
2. L'application récupère automatiquement les cours du jour
3. Les cours s'affichent organisés par jour

### 2. Consulter une Date Spécifique

**Pour voir une autre date :**

1. Cliquez dans le champ de date
2. Entrez la date au format **JJ/MM/AAAA**
   - Exemple : `13/10/2025`
3. Cliquez sur **"Rechercher"**
4. Les cours de cette date s'affichent

### 3. Comprendre l'Affichage

Chaque cours est présenté dans une carte avec :

```
┌─────────────────────────────┐
│ 📚 Nom de la Matière        │
│                             │
│ 👨‍🏫 Nom du Professeur        │
│ 🕐 Horaire du cours         │
│ 📍 Numéro de salle          │
└─────────────────────────────┘
```

**Exemple concret :**

```
┌─────────────────────────────┐
│ 📚 Potions                  │
│                             │
│ 👨‍🏫 Severus Rogue            │
│ 🕐 09:00 - 10:30            │
│ 📍 Salle 101                │
└─────────────────────────────┘
```

## ⚠️ Messages et États

### Chargement

Quand l'application récupère les données :

```
🔮 Récupération de l'emploi du temps magique...
[Animation de chargement]
```

**Que faire ?** Patientez quelques secondes.

### Erreur de Connexion

Si l'application ne peut pas se connecter :

```
⚠️ Erreur
Erreur lors de la récupération de l'emploi du temps
[×]
```

**Solutions :**
1. Vérifiez votre connexion Internet
2. Vérifiez vos identifiants dans le `.env`
3. Réessayez dans quelques instants

### Identifiants Manquants

Au premier lancement sans configuration :

```
⚠️ Veuillez configurer vos identifiants dans le fichier .env
```

**Solution :** Créez le fichier `.env` avec vos identifiants (voir Installation)

### Aucun Cours

Si aucun cours n'est trouvé :

```
📅 Aucun cours trouvé pour cette date
```

**Normal pour :**
- Week-ends
- Jours fériés
- Vacances scolaires

## 💡 Astuces et Conseils

### Format de Date

✅ **Formats acceptés :**
- `13/10/2025` - Avec zéros
- `05/01/2025` - Janvier

❌ **Formats non acceptés :**
- `13-10-2025` - Tirets
- `13.10.2025` - Points
- `2025/10/13` - Format US

### Navigation Rapide

| Action | Raccourci |
|--------|-----------|
| Date du jour | Cliquer "Aujourd'hui" |
| Changer de date | Taper directement |
| Rafraîchir | Re-rechercher même date |

### Performance

**L'application est lente ?**
- Première recherche : Normal (connexion + authentification)
- Recherches suivantes : Plus rapides (session active)
- Redémarrage : Réinitialise la session

## 🔧 Résolution de Problèmes

### Problème : L'application ne se lance pas

**Solutions :**
1. Vérifiez que l'installation est complète
2. Redémarrez votre ordinateur
3. Réinstallez l'application

### Problème : "API Electron non disponible"

**Cause :** L'application tourne en mode web (sans Electron)

**Solution :** Utilisez l'exécutable, pas le navigateur web

### Problème : Les cours ne s'affichent pas

**Vérifications :**
1. ✅ Connexion Internet active ?
2. ✅ Identifiants corrects dans `.env` ?
3. ✅ Date au bon format ?
4. ✅ Date avec des cours (pas week-end) ?

### Problème : "Login failed"

**Causes possibles :**
- Identifiants incorrects
- Compte bloqué
- Serveur wigorservices en maintenance

**Solutions :**
1. Vérifiez le USERNAME dans `.env`
2. Vérifiez le PASSWORD dans `.env`
3. Testez la connexion sur le site web wigorservices

## 📱 Support

### Obtenir de l'Aide

1. **Documentation**
   - README.md : Installation et configuration
   - TECHNICAL.md : Détails techniques
   - DELIVERABLES.md : Informations du projet

2. **Logs**
   - Ouvrez la console développeur : `Ctrl+Shift+I`
   - Onglet "Console" pour voir les erreurs

3. **Problème Persistant**
   - Notez le message d'erreur exact
   - Notez les étapes qui causent le problème
   - Contactez le support technique

### Informations Système

Pour le support, préparez :
- Version de Windows
- Message d'erreur complet
- Fichier de log (si disponible)

## 🎓 FAQ

**Q : Puis-je voir plusieurs semaines à la fois ?**  
R : Non, l'application affiche une date à la fois. Vous pouvez rechercher différentes dates successivement.

**Q : Les données sont-elles sauvegardées localement ?**  
R : Non, les données sont récupérées en temps réel à chaque recherche.

**Q : Puis-je exporter mon emploi du temps ?**  
R : Cette fonctionnalité n'est pas encore disponible dans la version 1.0.

**Q : L'application fonctionne-t-elle hors ligne ?**  
R : Non, une connexion Internet est requise pour récupérer les données.

**Q : Puis-je avoir plusieurs emplois du temps (multi-utilisateurs) ?**  
R : Chaque installation utilise un seul compte (défini dans `.env`).

**Q : L'application est-elle gratuite ?**  
R : Oui, totalement gratuite et open source.

## 🔐 Sécurité et Confidentialité

### Vos Données

- **Stockage local uniquement** : Vos identifiants restent sur votre machine
- **Pas de télémétrie** : Aucune donnée n'est envoyée à des tiers
- **Connexion sécurisée** : Communication HTTPS avec wigorservices

### Recommandations

1. Ne partagez pas votre fichier `.env`
2. Gardez vos identifiants confidentiels
3. Fermez l'application sur ordinateur partagé

## 📝 Changelog

### Version 1.0.0 (Octobre 2025)
- ✨ Première version
- 📅 Sélection de date
- 🔐 Authentification automatique
- 🎨 Interface moderne Tailwind
- 🧪 81.65% de couverture de tests

---

**Merci d'utiliser Emploi du Temps McGonagall !** 🦉

*"La connaissance est un trésor, mais la pratique est la clé qui l'ouvre."* - Minerva McGonagall
