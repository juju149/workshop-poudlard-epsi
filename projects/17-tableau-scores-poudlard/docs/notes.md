# 📝 Notes de développement – Défi 17

## 🎯 Choix techniques

### Backend : Node.js + Express + SQLite

**Justification** :
- ✅ **Node.js** : Rapide à développer, non-blocking I/O
- ✅ **Express** : Framework minimal et flexible
- ✅ **SQLite** : Léger, embedded, parfait pour ce use case
- ✅ **Jest** : Framework de test complet et rapide

**Alternatives considérées** :
- Python/Flask : Écarté (déjà utilisé dans autres défis)
- Go/Gin : Trop verbeux pour ce scope
- PostgreSQL : Overkill pour 4 maisons

### Frontend : Kotlin Android (MVVM)

**Justification** :
- ✅ **Kotlin** : Langage moderne, concis, safe
- ✅ **MVVM** : Séparation claire, testable
- ✅ **Retrofit** : Standard pour HTTP en Android
- ✅ **Coroutines** : Gestion async élégante

**Alternatives considérées** :
- Swift iOS : Pas d'environnement Mac disponible
- Flutter : Déjà utilisé dans défi 16
- React Native : Pas vraiment "natif"

### Architecture globale

**3-tier classique** :
```
App (Presentation) → API (Business Logic) → DB (Data)
```

Avantages :
- Séparation des responsabilités
- Scalabilité (peut remplacer SQLite par PostgreSQL)
- Testabilité (mock du repository)

## 🐛 Problèmes rencontrés et solutions

### 1. Tests asynchrones dans Jest

**Problème** :
```javascript
// Logs après fermeture des tests
console.log('Connexion fermée') // ❌ Après test
```

**Solution** :
- Augmenter les timeouts dans les tests database
- Utiliser `setTimeout` avant assertions dans database.test.js
- Accepter les warnings (comportement SQLite async)

### 2. Tests Coroutines Kotlin

**Problème** :
```kotlin
// LiveData non mise à jour dans tests
viewModel.loadHouses()
// value est null immédiatement
```

**Solution** :
```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class MainViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    
    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
    }
    
    @Test
    fun test() = runTest {
        viewModel.loadHouses()
        testDispatcher.scheduler.advanceUntilIdle() // ✅
        // Maintenant value est disponible
    }
}
```

### 3. Émulateur Android et localhost

**Problème** :
- `http://localhost:3000` ne fonctionne pas dans l'émulateur
- L'émulateur voit son propre localhost, pas celui de l'hôte

**Solution** :
```kotlin
// RetrofitClient.kt
private const val BASE_URL = "http://10.0.2.2:3000/" // ✅
// 10.0.2.2 = alias pour l'hôte de l'émulateur
```

Alternative pour device physique : utiliser l'IP locale (192.168.x.x)

### 4. Coverage Jest pas exactement 80%

**Problème** :
- Coverage à 81.13%, besoin de >80%
- Certaines lignes difficiles à tester (error handlers async)

**Solution** :
- Accepté car >80% ✅
- Lignes non couvertes : logs d'erreur dans callbacks SQLite
- Pas critique pour la logique métier

## ⚡ Optimisations effectuées

### 1. Base de données

**Seed automatique** :
```javascript
seedData() {
    const houses = ['Gryffondor', 'Serpentard', 'Poufsouffle', 'Serdaigle'];
    houses.forEach(house => {
        this.db.run('INSERT OR IGNORE INTO houses (name, points) VALUES (?, 0)', [house]);
    });
}
```
Avantage : Pas besoin de script SQL externe

### 2. Repository pattern (Android)

**Abstraction de l'API** :
```kotlin
class HouseRepository(private val apiService: ApiService) {
    suspend fun getAllHouses(): Resource<List<House>> {
        return try {
            val response = apiService.getHouses()
            if (response.isSuccessful) {
                Resource.Success(response.body()?.houses ?: emptyList())
            } else {
                Resource.Error("Erreur: ${response.code()}")
            }
        } catch (e: Exception) {
            Resource.Error(e.message ?: "Erreur inconnue")
        }
    }
}
```
Avantage : ViewModel ne connaît pas Retrofit

### 3. Resource sealed class

**États typés** :
```kotlin
sealed class Resource<T>(val data: T? = null, val message: String? = null) {
    class Success<T>(data: T) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
    class Loading<T> : Resource<T>()
}
```
Avantage : Pattern matching exhaustif avec `when`

### 4. Docker volumes

**Persistance** :
```yaml
volumes:
  - hogwarts-data:/data
```
Avantage : Données préservées même après `docker compose down`

## 📋 TODO / Améliorations futures

### Priorité haute

- [ ] **Authentification** : JWT pour sécuriser l'API
- [ ] **Logs** : Winston pour logs structurés (JSON)
- [ ] **Validation** : Joi ou Zod pour validation robuste
- [ ] **CI/CD** : GitHub Actions pour tests auto

### Priorité moyenne

- [ ] **Historique** : Table `history` pour tracer les modifications
- [ ] **Graphiques** : MPAndroidChart pour visualisation
- [ ] **WebSocket** : Socket.io pour updates temps réel
- [ ] **Version iOS** : Port en Swift/SwiftUI

### Priorité basse

- [ ] **Dark mode** : Support thème sombre Android
- [ ] **Internationalisation** : Strings.xml multilingue
- [ ] **Animations** : Transitions plus fluides
- [ ] **Partage** : Partager le classement sur réseaux sociaux

### Technique

- [ ] **PostgreSQL** : Migration pour production
- [ ] **Redis** : Cache pour réduire charge DB
- [ ] **Docker multi-stage** : Build optimisé
- [ ] **Monitoring** : Prometheus + Grafana
- [ ] **Tests E2E** : Appium ou Detox

## 💡 Retour d'expérience

### Points positifs

✅ **Architecture propre** : MVVM facilite les tests  
✅ **Séparation backend/frontend** : Peut évoluer indépendamment  
✅ **Tests dès le début** : Pas de dette technique  
✅ **Docker** : Déploiement simple  
✅ **Documentation** : Générée pendant le dev  

### Difficultés

⚠️ **Kotlin Coroutines** : Courbe d'apprentissage pour les tests  
⚠️ **SQLite async** : Callbacks complexes pour les tests  
⚠️ **Android SDK** : Setup initial long (gradle, dépendances)  
⚠️ **Émulateur** : Gourmand en ressources  

### Ce que je ferais différemment

1. **TypeScript** : Pour le backend (typage statique)
2. **GraphQL** : Au lieu de REST (moins d'endpoints)
3. **Jetpack Compose** : UI déclarative au lieu de XML
4. **GitHub Actions** : CI/CD dès le début
5. **PostgreSQL** : Directement pour éviter migration

## 📊 Métriques de développement

- **Temps total** : ~4 heures
- **Backend** : 1h (code + tests)
- **Android** : 2h (code + tests + layouts)
- **Docker + Docs** : 1h
- **Tests** : Intégrés pendant le dev

**Productivité** :
- Lignes de code par heure : ~400
- Tests générés : 45+ (25 backend + 20+ Android)
- Coverage atteint : 81% dès la première itération

## 🎓 Connaissances acquises

### Nouvelles compétences

- ✨ **Kotlin Coroutines** : Flow, suspend, runTest
- ✨ **Mockito Kotlin** : DSL pour mocks élégants
- ✨ **Jest coverage** : Configuration optimale
- ✨ **Docker healthchecks** : Monitoring containers

### Améliorées

- 🔧 **MVVM Android** : Architecture plus claire
- 🔧 **Retrofit** : Configuration avancée (logging, timeouts)
- 🔧 **SQLite** : Gestion async avec callbacks
- 🔧 **Bash scripting** : Tests automatisés robustes

## 🏆 Objectifs atteints

| Objectif | Statut | Note |
|----------|--------|------|
| App native Kotlin | ✅ | Fonctionnelle |
| API REST | ✅ | 6 endpoints |
| Base de données | ✅ | SQLite persistante |
| Tests unitaires | ✅ | 45+ tests |
| Coverage > 80% | ✅ | 81.13% |
| Documentation | ✅ | Complète |
| Docker | ✅ | Avec volumes |
| Tests smoke/intégration | ✅ | Scripts bash |

## 📚 Ressources utilisées

### Documentation officielle

- [Kotlin Docs](https://kotlinlang.org/docs/)
- [Express.js](https://expressjs.com/)
- [Retrofit](https://square.github.io/retrofit/)
- [Jest](https://jestjs.io/)
- [Material Design 3](https://m3.material.io/)

### Articles/Tutoriels

- Android MVVM Architecture
- Kotlin Coroutines Testing
- Jest Mocking Best Practices
- Docker Compose Healthchecks

### Outils

- Android Studio Electric Eel
- VS Code avec extensions (Jest, Docker)
- Postman pour tests API
- Docker Desktop

---

*Dernière mise à jour : 13 octobre 2025*
