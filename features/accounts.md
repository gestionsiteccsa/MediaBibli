# Feature : Accounts - Gestion des utilisateurs MediaBib

## Récapitulatif de la demande

Système d'authentification à 3 niveaux pour MediaBib :
- **Superadmin** : Premier utilisateur, gère tout le projet
- **Médiathèque** : Créée par superadmin, peut gérer lecteurs
- **Lecteur** : Créé par médiathèque/superadmin, accède à son compte + API OPAC

## Tâches

### Phase 1 : Configuration de base
- [x] Mettre à jour `requirements.txt` (DRF, SimpleJWT)
- [x] Configurer `app/settings.py` (AUTH_USER_MODEL, apps, REST_FRAMEWORK, JWT)

### Phase 2 : Modèles
- [x] Créer modèle `User` (AbstractUser avec user_type, library FK)
- [x] Créer modèle `Library` (nom, code, adresse, contact, audit RGPD)
- [x] Créer modèle `ReaderProfile` (carte, infos perso, consentement RGPD)
- [x] Exécuter migrations
- [x] Configurer `accounts/admin.py`

### Phase 3 : Permissions et formulaires
- [x] Créer `accounts/permissions.py` (mixins SuperadminRequired, LibraryStaffRequired)
- [x] Créer `accounts/forms.py` (LibraryForm, ReaderCreationForm, etc.)

### Phase 4 : Vues web authentification
- [x] Créer vues login/logout personnalisées
- [x] Créer vue profil utilisateur
- [x] Créer templates authentification
- [x] Configurer `accounts/urls.py`
- [x] Créer système d'inscription en ligne pour lecteurs

### Phase 5 : Gestion médiathèques (superadmin)
- [x] Créer vues CRUD Library (list, create, detail, update, delete)
- [x] Créer formulaire création médiathèque + utilisateur associé
- [x] Créer templates médiathèque

### Phase 6 : Gestion lecteurs (médiathèque)
- [x] Créer vues CRUD Reader (list, create, detail, update, delete)
- [x] Implémenter génération mot de passe avec affichage
- [x] Implémenter envoi email mot de passe (optionnel)
- [x] Créer templates lecteur

### Phase 7 : API REST
- [x] Créer `accounts/api/serializers.py` (User, Library, ReaderProfile, JWT custom)
- [x] Créer `accounts/api/views.py` (ReaderMeViewSet, LibraryViewSet)
- [x] Créer endpoints préparés (loans, reservations, history - listes vides)
- [x] Créer `accounts/api/urls.py`
- [x] Configurer routes API dans `app/urls.py`

### Phase 8 : Tests
- [x] Tests modèles (User, Library, ReaderProfile)
- [x] Tests vues web (authentification, CRUD)
- [x] Tests API (JWT, endpoints lecteur)
- [x] Tests permissions

### Phase 9 : Finalisation
- [x] Créer fichier `features/accounts.md` selon workflow projet
- [x] Vérifier conformité RGPD (consentement, audit)
- [x] Test intégration complet (44 tests passent)

---

## Structure des fichiers créés

```
accounts/
├── __init__.py
├── admin.py              # Configuration admin Django
├── apps.py
├── forms.py              # Formulaires web
├── models.py             # User, Library, ReaderProfile
├── permissions.py        # Mixins de permissions
├── tests.py              # 33 tests
├── urls.py               # Routes web
├── views.py              # Vues web
├── api/
│   ├── __init__.py
│   ├── serializers.py    # Sérialiseurs API
│   ├── urls.py           # Routes API
│   └── views.py          # Vues API
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
└── templates/accounts/
    ├── login.html
    ├── register.html
    ├── register_success.html
    ├── profile.html
    ├── profile_edit.html
    ├── library/
    │   ├── list.html
    │   ├── create.html
    │   ├── detail.html
    │   ├── update.html
    │   └── delete.html
    └── reader/
        ├── list.html
        ├── create.html
        ├── created.html
        ├── detail.html
        ├── update.html
        ├── delete.html
        ├── password_reset.html
        └── password_reset_done.html
```

---

## Structure API

```
POST /api/v1/auth/token/           → JWT login
POST /api/v1/auth/token/refresh/   → Refresh token
POST /api/v1/auth/token/verify/    → Verify token

GET  /api/v1/readers/me/           → Profil lecteur connecté
PATCH /api/v1/readers/me/          → Mise à jour profil
GET  /api/v1/readers/me/loans/     → Prêts en cours (placeholder)
GET  /api/v1/readers/me/reservations/ → Réservations (placeholder)
GET  /api/v1/readers/me/history/   → Historique (placeholder)

GET  /api/v1/libraries/            → Liste médiathèques (public)
GET  /api/v1/libraries/{id}/       → Détail médiathèque (public)
```

---

## Conformité RGPD

- ✅ Champ `gdpr_consent` obligatoire pour créer un lecteur
- ✅ Horodatage du consentement (`gdpr_consent_date`)
- ✅ Consentement newsletter séparé
- ✅ Champs d'audit (`created_at`, `updated_at`) sur tous les modèles
- ✅ Les données personnelles sont stockées uniquement dans `ReaderProfile`

---

## Vérification manuelle

### Tests manuels
1. Créer superadmin via `python manage.py createsuperuser`
2. Se connecter à l'admin Django, vérifier user_type
3. Créer une médiathèque + son utilisateur via interface web
4. Se connecter en tant que médiathèque
5. Créer un lecteur, vérifier affichage mot de passe
6. Tester API : obtenir JWT token pour lecteur
7. Tester endpoint `/api/v1/readers/me/`

### Tests automatisés
```bash
python manage.py test accounts
# 44 tests OK
```
