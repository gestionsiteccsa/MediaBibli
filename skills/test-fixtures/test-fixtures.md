# Test Fixtures

## Concept

Les fixtures sont des données de test prédéfinies qui permettent de créer un état connu et reproductible pour les tests.

## Pytest Fixtures

### Définition de base
```python
import pytest

@pytest.fixture
def user():
    return User(name="John", email="john@example.com")

def test_user_email(user):
    assert "@" in user.email
```

### Scopes
```python
@pytest.fixture(scope="function")  # Par défaut, nouvelle instance par test
def user():
    return User()

@pytest.fixture(scope="class")  # Une instance par classe de test
def db_connection():
    return create_connection()

@pytest.fixture(scope="module")  # Une instance par module
def api_client():
    return APIClient()

@pytest.fixture(scope="session")  # Une instance pour toute la session
def database():
    return setup_database()
```

### Fixtures avec setup et teardown
```python
@pytest.fixture
def database():
    # Setup
    db = create_database()
    db.connect()
    yield db
    # Teardown
    db.disconnect()
    db.cleanup()
```

### Fixtures paramétrées
```python
@pytest.fixture(params=["mysql", "postgresql", "sqlite"])
def database(request):
    return create_database(request.param)

def test_query(database):
    # Ce test s'exécute 3 fois avec chaque type de DB
    assert database.execute("SELECT 1")
```

### Composition de fixtures
```python
@pytest.fixture
def user():
    return User(name="John")

@pytest.fixture
def authenticated_user(user, auth_service):
    auth_service.login(user)
    return user

@pytest.fixture
def user_with_posts(authenticated_user, post_factory):
    for i in range(5):
        post_factory.create(author=authenticated_user)
    return authenticated_user
```

## Factory Pattern

### Factory Boy (Django)
```python
import factory
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')

class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker('sentence')
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('paragraph')

# Utilisation
def test_article_creation():
    article = ArticleFactory()
    assert article.author is not None
```

### Traits et états
```python
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    is_active = True
    is_staff = False

    class Params:
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True
        )
        inactive = factory.Trait(
            is_active=False
        )

# Utilisation
admin_user = UserFactory(admin=True)
inactive_user = UserFactory(inactive=True)
```

## Django Fixtures (JSON/YAML)

### Génération
```bash
python manage.py dumpdata app.Model --indent 2 > fixtures/model.json
```

### Format JSON
```json
[
  {
    "model": "myapp.article",
    "pk": 1,
    "fields": {
      "title": "Premier article",
      "content": "Contenu de l'article",
      "author": 1
    }
  }
]
```

### Chargement
```python
class ArticleTest(TestCase):
    fixtures = ['users.json', 'articles.json']

    def test_article_count(self):
        self.assertEqual(Article.objects.count(), 5)
```

## conftest.py

```python
# conftest.py - Fixtures partagées
import pytest
from django.test import Client

@pytest.fixture
def api_client():
    return Client()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_login(user)
    return api_client

@pytest.fixture(autouse=True)
def reset_cache():
    # S'exécute automatiquement avant chaque test
    cache.clear()
    yield
    cache.clear()
```

## Bonnes pratiques

- Garder les fixtures simples et focalisées
- Utiliser des factories pour les données complexes
- Éviter les fixtures globales qui créent des dépendances cachées
- Nommer les fixtures de manière descriptive
- Documenter les fixtures complexes
- Préférer la composition à l'héritage
- Nettoyer les ressources dans le teardown
