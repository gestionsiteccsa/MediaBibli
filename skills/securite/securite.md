# Sécurité Web

## OWASP Top 10

### 1. Injection (SQL, NoSQL, OS, LDAP)
```python
# Vulnérable
query = f"SELECT * FROM users WHERE id = {user_input}"

# Sécurisé - Requêtes paramétrées
cursor.execute("SELECT * FROM users WHERE id = %s", (user_input,))

# Django ORM (sécurisé par défaut)
User.objects.filter(id=user_input)
```

### 2. Broken Authentication
- Implémenter une politique de mots de passe forts
- Limiter les tentatives de connexion (rate limiting)
- Utiliser l'authentification multi-facteurs (MFA)
- Invalider les sessions après déconnexion

```python
# Django - Hasher de mot de passe
from django.contrib.auth.hashers import make_password, check_password
hashed = make_password('password123')
is_valid = check_password('password123', hashed)
```

### 3. Cross-Site Scripting (XSS)
```python
# Vulnérable
return f"<div>{user_input}</div>"

# Sécurisé - Échappement
from django.utils.html import escape
return f"<div>{escape(user_input)}</div>"

# Django templates (échappement automatique)
{{ user_input }}  # Échappé par défaut
{{ user_input|safe }}  # Non échappé - à éviter
```

### 4. Insecure Direct Object References (IDOR)
```python
# Vulnérable
def get_document(request, doc_id):
    return Document.objects.get(id=doc_id)

# Sécurisé - Vérifier l'autorisation
def get_document(request, doc_id):
    document = Document.objects.get(id=doc_id)
    if document.owner != request.user:
        raise PermissionDenied
    return document
```

### 5. Security Misconfiguration
```python
# Django settings pour la production
DEBUG = False
ALLOWED_HOSTS = ['example.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

### 6. Cross-Site Request Forgery (CSRF)
```html
<!-- Django - Token CSRF dans les formulaires -->
<form method="POST">
    {% csrf_token %}
    <input type="text" name="data">
    <button type="submit">Envoyer</button>
</form>
```

```python
# API - Désactiver CSRF pour les endpoints stateless avec JWT
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Uniquement si authentification par token
def api_endpoint(request):
    pass
```

## Authentification et Autorisation

### JWT (JSON Web Tokens)
```python
import jwt
from datetime import datetime, timedelta

# Création
payload = {
    'user_id': user.id,
    'exp': datetime.utcnow() + timedelta(hours=24),
    'iat': datetime.utcnow()
}
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# Vérification
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
except jwt.ExpiredSignatureError:
    # Token expiré
    pass
except jwt.InvalidTokenError:
    # Token invalide
    pass
```

### Permissions Django
```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def protected_view(request):
    pass

@permission_required('app.can_edit')
def edit_view(request):
    pass
```

## Validation des entrées

```python
# Validation avec Pydantic
from pydantic import BaseModel, EmailStr, validator

class UserInput(BaseModel):
    email: EmailStr
    age: int

    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age invalide')
        return v

# Django Forms
class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)
```

## Headers de sécurité

```python
# Django middleware ou décorateur
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", 'cdn.example.com')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
```

## Gestion des secrets

```python
# Variables d'environnement
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

# Fichier .env (avec python-dotenv)
from dotenv import load_dotenv
load_dotenv()
```

## Logging de sécurité

```python
import logging

security_logger = logging.getLogger('security')

def login_view(request):
    if login_failed:
        security_logger.warning(
            f"Tentative de connexion échouée pour {username} depuis {request.META['REMOTE_ADDR']}"
        )
```

## Checklist sécurité

- [ ] Requêtes SQL paramétrées
- [ ] Échappement des sorties HTML
- [ ] Token CSRF sur les formulaires
- [ ] Validation des entrées utilisateur
- [ ] Vérification des autorisations
- [ ] HTTPS en production
- [ ] Headers de sécurité configurés
- [ ] Secrets dans les variables d'environnement
- [ ] Rate limiting sur les endpoints sensibles
- [ ] Logging des événements de sécurité
- [ ] Mise à jour régulière des dépendances
